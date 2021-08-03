from datetime import datetime
# # print(datetime.now().year)
str1 = "2021-07-20T00:00:00"
d = datetime.strptime(str1, '%Y-%m-%dT%H:%M:%S')
d = datetime.strptime("2021-07-20T00:00:00", '%Y-%m-%dT%H:%M:%S')
print(d)
# # d=d.strftime('%Y-%m-%d')
# # d = datetime.fromisoformat("2021-04-15T00:00:00")
# print(str1[0:10])
# # print((datetime.now()-d).days)
# # print("hiii")
# # s = ""
# # print(s)
# # print(s.strip()=="")


s1 = "Gaurav"
s2 = "Pingale"
print(s1 +" "+ s2)