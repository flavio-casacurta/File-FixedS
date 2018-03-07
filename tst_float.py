from fixed_files import Fixed_files
ff = Fixed_files(r'C:\BNB\S303\GERADOS\Json\B303W80.json', dic=False, checklength=False)
records = open(r'C:\BNB\S303\GERADOS\Json\B303W80.txt').readlines()
rec_in = []
for record in records:
    rec_in.append(ff.parse(record))
rec_in
for rec in rec_in:
    print rec

for n, r in enumerate(rec_in):
    print ff.unparse(r)
    print ff.unparse(r) == records[n]
