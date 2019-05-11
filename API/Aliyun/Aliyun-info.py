#!/usr/local/bin/python3
#*************************************************
# Description : 云资源数据汇总写入总控机器 Redis,结合总控 OpenResty 组成 Web 信息查询工具
#               常量 AK 为阿里云AK信息字典结构,如果有多个阿里云账号可以一一对应写入
# Version     : 1.0
# Author      : XABCLOUD.COM
#*************************************************
import re,subprocess,redis,threading
#-----------------VAR-----------------------------
AK = {'access_key_id1':'access_key_secret1','access_key_id2':'access_key_secret2',}
DB0 = redis.Redis(host='',password='io')
#-----------------FUN-----------------------------
def CLN():
    P0 = DB0.pipeline()
    for i in DB0.keys("INFO:*"):
        P0.delete(i)
    P0.execute()
def ECS():
    P0 = DB0.pipeline()
    try:
        for access_key_id,access_key_secret in AK.items():
            Regions = eval(subprocess.check_output('./aliyun-ecs.py Action=DescribeRegions Id='+access_key_id+' Secret='+access_key_secret,shell=True).decode().replace("true","True").replace("false","False"))['Regions']['Region']
            for e in Regions:
                RegionId = e['RegionId']
                LocalName = e['LocalName']
                data=eval(subprocess.check_output('./aliyun-ecs.py Action=DescribeInstances Id='+access_key_id+' Secret='+access_key_secret+' RegionId='+RegionId,shell=True).decode().replace("true","True").replace("false","False"))
                EcsCount = data['TotalCount']
                if EcsCount:
                    PageSum = int((EcsCount+100)/100)
                    for PageNumber in range(1,PageSum+1):
                        res = eval(subprocess.check_output('./aliyun-ecs.py Action=DescribeInstances PageSize=100 Id='+access_key_id+' Secret='+access_key_secret+' RegionId='+RegionId+' PageNumber='+str(PageNumber),shell=True).decode().replace("true","True").replace("false","False"))
                        for ecs in res['Instances']['Instance']:
                            k="INFO:ECS: ["+LocalName+" "+RegionId+"] "+ecs['InstanceId']+" ["+ecs['OSName']+"] 配置:["+str(ecs['Cpu'])+"C "+str(ecs['Memory'])+"M] 实例名称:"+ecs['InstanceName']+" VPC私有IP:"+str(ecs['VpcAttributes']['PrivateIpAddress']['IpAddress'])+" 经典内网IP:"+str(ecs['InnerIpAddress']['IpAddress'])+" 公网IP:"+str(ecs['PublicIpAddress']['IpAddress'])+" 弹性公网IP:"+str(ecs['EipAddress']['IpAddress'])+" 公网入带宽最大值:"+str(ecs['InternetMaxBandwidthIn'])+"M 公网出带宽最大值:"+str(ecs['InternetMaxBandwidthOut'])+"M 所属的安全组集合:"+str(ecs['SecurityGroupIds']['SecurityGroupId'])
                            v=ecs['ExpiredTime']
                            P0.set(k,v)
    except:
        pass
    P0.execute()
def RDS():
    P0 = DB0.pipeline()
    try:
        for access_key_id,access_key_secret in AK.items():
            Regions = eval(subprocess.check_output('./aliyun-ecs.py Action=DescribeRegions Id='+access_key_id+' Secret='+access_key_secret,shell=True).decode().replace("true","True").replace("false","False"))['Regions']['Region']
            for e in Regions:
                RegionId = e['RegionId']
                LocalName = e['LocalName']
                data=eval(subprocess.check_output('./aliyun-rds.py Action=DescribeDBInstances Id='+access_key_id+' Secret='+access_key_secret+' RegionId='+RegionId,shell=True).decode().replace("true","True").replace("false","False"))
                RdsCount= data['TotalRecordCount']
                if RdsCount:
                    PageSum = int((RdsCount+100)/100)
                    for PageNumber in range(1,PageSum+1):
                        res = eval(subprocess.check_output('./aliyun-rds.py Action=DescribeDBInstances PageSize=100 Id='+access_key_id+' Secret='+access_key_secret+' RegionId='+RegionId+' PageNumber='+str(PageNumber),shell=True).decode().replace("true","True").replace("false","False"))
                        for i in res['Items']['DBInstance']:
                            res1 = eval(subprocess.check_output('./aliyun-rds.py Action=DescribeDBInstanceAttribute Id='+access_key_id+' Secret='+access_key_secret+' RegionId='+RegionId+' DBInstanceId='+i['DBInstanceId'],shell=True).decode().replace("true","True").replace("false","False"))
                            for rds in res1['Items']['DBInstanceAttribute']:
                                try:
                                    k = "INFO:RDS: ["+LocalName+" "+rds['RegionId']+"] "+rds['DBInstanceId']+" ["+rds['Engine']+" "+rds['EngineVersion']+"] 配置:["+str(rds['DBInstanceMemory'])+"M "+str(rds['DBInstanceStorage'])+"GB 最大每秒IO请求:"+str(rds['MaxIOPS'])+" 最大并发连接:"+str(rds['MaxConnections'])+"] 实例类型:"+rds['DBInstanceType']+" 网络类型:"+rds['InstanceNetworkType']+" 网络连接类型:"+rds['DBInstanceNetType']+" 备注:"+rds['DBInstanceDescription']+" 内网连接地址:"+rds['ConnectionString']+" 端口:"+rds['Port']
                                    v = rds['ExpireTime']
                                    P0.set(k,v)
                                except:
                                    pass
    except:
        pass
    P0.execute()
def SLB():
    P0 = DB0.pipeline()
    try:
        for access_key_id,access_key_secret in AK.items():
            Regions = eval(subprocess.check_output('./aliyun-ecs.py Action=DescribeRegions Id='+access_key_id+' Secret='+access_key_secret,shell=True).decode().replace("true","True").replace("false","False"))['Regions']['Region']
            for e in Regions:
                RegionId = e['RegionId']
                LocalName = e['LocalName']
                data=eval(subprocess.check_output('./aliyun-slb.py Action=DescribeLoadBalancers Id='+access_key_id+' Secret='+access_key_secret+' RegionId='+RegionId,shell=True).decode().replace("true","True").replace("false","False"))
                SlbCount= data['TotalCount']
                if SlbCount:
                    PageSum = int((SlbCount+100)/100)
                    for PageNumber in range(1,PageSum+1):
                        res = eval(subprocess.check_output('./aliyun-slb.py Action=DescribeLoadBalancers PageSize=100 Id='+access_key_id+' Secret='+access_key_secret+' RegionId='+RegionId+' PageNumber='+str(PageNumber),shell=True).decode().replace("true","True").replace("false","False"))
                        for i in res['LoadBalancers']['LoadBalancer']:
                            slb = eval(subprocess.check_output('./aliyun-slb.py Action=DescribeLoadBalancerAttribute Id='+access_key_id+' Secret='+access_key_secret+' RegionId='+RegionId+' LoadBalancerId='+i['LoadBalancerId'],shell=True).decode().replace("true","True").replace("false","False"))
                            k = "INFO:SLB: ["+LocalName+" "+slb['RegionId']+"] "+slb['LoadBalancerId']+" IP:"+slb['Address']+" 后端服务列表:"+str(slb['BackendServers']['BackendServer'])+" "+str(slb['ListenerPorts']['ListenerPort'])+" "+str(slb['ListenerPortsAndProtocol']['ListenerPortAndProtocol'])+" "+slb['LoadBalancerStatus']+" "+slb['AddressType']+" 备注名称:"+slb['LoadBalancerName']
                            v = slb['AddressType']
                            P0.set(k,v)
    except:
        pass
    P0.execute()
def CDN():
    P0 = DB0.pipeline()
    try:
        for access_key_id,access_key_secret in AK.items():
                data=eval(subprocess.check_output('./aliyun-cdn.py Action=DescribeUserDomains Id='+access_key_id+' Secret='+access_key_secret,shell=True).decode().replace("true","True").replace("false","False"))
                CdnCount = data['TotalCount']
                if CdnCount:
                    PageSum = int((CdnCount+20)/20)
                    for PageNumber in range(1,PageSum+1):
                        res = eval(subprocess.check_output('./aliyun-cdn.py Action=DescribeUserDomains PageSize=50 Id='+access_key_id+' Secret='+access_key_secret+' PageNumber='+str(PageNumber),shell=True).decode().replace("true","True").replace("false","False"))
                        for cdn in (res['Domains']['PageData']):
                            k = "INFO:CDN: "+cdn['DomainName']+" "+cdn['Cname']+" "+cdn['DomainStatus']+" "+cdn['CdnType']+" "+cdn['SslProtocol']+" "+str(cdn['Sources'])
                            v = cdn['GmtModified']
                            P0.set(k,v)
    except:
        pass
    P0.execute()
def Redis():
    P0 = DB0.pipeline()
    try:
        for access_key_id,access_key_secret in AK.items():
            Regions = eval(subprocess.check_output('./aliyun-ecs.py Action=DescribeRegions Id='+access_key_id+' Secret='+access_key_secret,shell=True).decode().replace("true","True").replace("false","False"))['Regions']['Region']
            for e in Regions:
                RegionId = e['RegionId']
                LocalName = e['LocalName']
                data=(subprocess.check_output('./aliyun-redis.py Action=DescribeInstances Id='+access_key_id+' Secret='+access_key_secret+' RegionId='+RegionId,shell=True))
                data=eval(subprocess.check_output('./aliyun-redis.py Action=DescribeInstances Id='+access_key_id+' Secret='+access_key_secret+' RegionId='+RegionId,shell=True).decode().replace("true","True").replace("false","False"))
                RedisCount= data['TotalCount']
                if RedisCount:
                    PageSum = int((RedisCount+50)/50)
                    for PageNumber in range(1,PageSum+1):
                        res = eval(subprocess.check_output('./aliyun-redis.py Action=DescribeInstances PageSize=50 Id='+access_key_id+' Secret='+access_key_secret+' RegionId='+RegionId+' PageNumber='+str(PageNumber),shell=True).decode().replace("true","True").replace("false","False"))
                        for redis in res['Instances']['KVStoreInstance']:
                            k = "INFO:Redis: ["+LocalName+" "+RegionId+"] "+redis['InstanceId']+" "+redis['InstanceName']+" ["+redis['InstanceType']+" "+redis['EngineVersion']+"] 配置:[容量"+str(redis['Capacity'])+"MB 带宽"+str(redis['Bandwidth'])+"MB/s 最大连接数"+str(redis['Connections'])+"] 内网连接地址:"+redis['ConnectionDomain']+" 端口:"+str(redis['Port'])
                            v = redis['NetworkType']
                            P0.set(k,v)
    except:
        pass
    P0.execute()
def MongoDB():
    P0 = DB0.pipeline()
    try:
        for access_key_id,access_key_secret in AK.items():
            Regions = eval(subprocess.check_output('./aliyun-ecs.py Action=DescribeRegions Id='+access_key_id+' Secret='+access_key_secret,shell=True).decode().replace("true","True").replace("false","False"))['Regions']['Region']
            for e in Regions:
                RegionId = e['RegionId']
                LocalName = e['LocalName']
                data=eval(subprocess.check_output('./aliyun-mongodb.py Action=DescribeDBInstances Id='+access_key_id+' Secret='+access_key_secret+' RegionId='+RegionId,shell=True).decode().replace("true","True").replace("false","False"))
                MongoCount= data['TotalCount']
                if MongoCount:
                    PageSum = int((MongoCount+100)/100)
                    for PageNumber in range(1,PageSum+1):
                        res = eval(subprocess.check_output('./aliyun-mongodb.py Action=DescribeDBInstances PageSize=100 Id='+access_key_id+' Secret='+access_key_secret+' RegionId='+RegionId+' PageNumber='+str(PageNumber),shell=True).decode().replace("true","True").replace("false","False"))
                        for i in res['DBInstances']['DBInstance']:
                            res1 = eval(subprocess.check_output('./aliyun-mongodb.py Action=DescribeDBInstanceAttribute Id='+access_key_id+' Secret='+access_key_secret+' RegionId='+RegionId+' DBInstanceId='+i['DBInstanceId'],shell=True).decode().replace("true","True").replace("false","False"))
                            for j in res1['DBInstances']['DBInstance']:
                                if 'DBInstanceDescription' in j:
                                    DBInstanceDescription = j['DBInstanceDescription']
                                else:
                                    DBInstanceDescription = ""
                                k = "INFO:MongoDB: ["+LocalName+" "+j['RegionId']+" "+j['ZoneId']+"] "+j['DBInstanceId']+" "+j['Engine']+" "+j['EngineVersion']+" 节点数:"+j['ReplicationFactor']+" 配置:["+str(j['DBInstanceStorage'])+"M "+" 最大每秒IO请求:"+str(j['MaxIOPS'])+" 最大并发连接:"+str(j['MaxConnections'])+"] 实例类型:"+j['DBInstanceType']+" 网络类型:"+j['NetworkType']+" 连接信息:"+str(j['ReplicaSets'])+" "+DBInstanceDescription
                                v = LocalName
                                P0.set(k,v)
    except:
        pass
    P0.execute()
def main():
    CLN()
    t1 = threading.Thread(target=ECS)
    t2 = threading.Thread(target=RDS)
    t3 = threading.Thread(target=SLB)
    t4 = threading.Thread(target=CDN)
    t5 = threading.Thread(target=Redis)
    t6 = threading.Thread(target=MongoDB)
    t1.start(),t2.start(),t3.start(),t4.start(),t5.start(),t6.start()
#-----------------PROG----------------------------
if __name__ == '__main__':
    main()
