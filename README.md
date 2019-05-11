# info [xabcloud.com](https://xabcloud.com)
>在互联网企业里,随着企业业务发展,云上资源越来越多,技术人员也越来越多,一般企业内部的运维平台只会记录关键的资源数据,并不会记录所有数据,而日常技术交流经常会查询一些信息,比如某ECS的公网带宽大小,知道ECS公网IP,想知道对应的内网IP等等,又或者是SLB的挂载信息等等,而企业里并不会给每个技术人员开通云子账号(繁琐也不利于管理维护),所以该工具将云资源数据收集并提供自助式查询

云资源数据汇总写入 Redis, 通过 OpenResty->Lua->Redis 展现数据组成自助式 Web 信息查询工具

- 1.数据收集 [使用云服务商提供的 API 将云资源以 Key-Value 结构写入Redis]
- 2.数据展现 [使用 OpenResty->Lua->Redis 将数据直接 Web 展现和检索]

## 运行环境

CentOS 7.x,需要的基础软件 Python3 和 OpenResty 以及相关依赖软件包,基础软件建议如下安装

```
# 安装Python3
curl -s xabc.io/py3|bash 
# 安装OpenResty
curl -s xabc.io/o|bash 
```

## 数据展现

```
# 我们习惯部署 OpenResty 的路径,可以根据需要自己调整
/opt/openresty/nginx/conf/nginx.conf
/opt/openresty/nginx/conf/lua/info.lua
```

## 数据收集

```
# 执行数据收集器,将云资源数据写入Redis
API/Aliyun/Aliyun-info.py 
...
```

## XABC 企业运维管控平台 QQ 群号: 839212346
