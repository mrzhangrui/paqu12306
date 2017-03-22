import requests,re

url='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9001'
r=requests.get(url,verify=False)

data=r.text

s=re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', data)
print(s)
stations={}
for l in s:
	stations[l[0]]=l[1]

return stations