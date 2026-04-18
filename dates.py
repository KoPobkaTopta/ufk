s1 = "31/01/2025"
s2 = "01/12/2025"

d1 = s1.split("/")
d2 = s2.split("/")

date1 = (int(d1[2]), int(d1[1]), int(d1[0]))
date2 = (int(d2[2]), int(d2[1]), int(d2[0]))

print(date1 > date2)
