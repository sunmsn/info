-- 读取 Redis 返回查询数据,注意根据需要修改 Redis 密码
local function split(s,p)
	local rt= {}
	string.gsub(s,'[^'..p..']+', function(w) table.insert(rt,w) end )
	return rt
end
local red = redis:new()
local key = split(ngx.var.uri,"/")[1] or '*'
red:connect(red,'127.0.0.1','6379')
red:auth("io")
local res = red:keys("INFO:*"..key.."*")
local x=""
for i,v in ipairs(res) do
	x=x..v.."\n"
end
ngx.say(string.sub(x,0,-2))
red:close()
