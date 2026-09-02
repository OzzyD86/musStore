import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

db = sqlite3.connect("music.db")
db.row_factory = dict_factory
cur = db.cursor()

p = cur.execute("sELECT count(*) as `c` FROM `music`")
a = p.fetchone()
print(a)
total = a['c']
spl = total / 4
print(spl)
st = {}
p = cur.execute("sELECT count(*) as `c`, upper(substr(coalesce(`subtitle`, `title`), 1, 1)) as `a` FROM `music` GROUP BY `a` order by `a` ASC")
n = 0
s = 0
ls = 0
ql = {0: 0}
st[s] = []
for i in p:
	n += i['c']
	ql[s] += i['c']
	b = ((spl*(s+1))-ls, (spl*(s+1))-n)
	print(b, i, s)
	st[s].append(i)
	ls = n
	if (b[1] < 0):
		print("Split point reached")
		print(abs(b[0]), abs(b[1]))
		if (abs(b[1]) <= abs(b[0])):
			ql[s] -= i['c']
			print("Move last set to next position")
			ql[s+1] = i['c']
		else:
			ql[s+1] = 0
		s+=1
		st[s] = []
#print(ql)
for i in st:
	print("Folder " + str(i+1) + ":")
	for j in st[i]:
		print(j)