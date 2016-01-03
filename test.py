from fixed_files import Fixed_files
fj = r'E:\GFCT\Evidencias\cpy\gfctb092.json'
ff = Fixed_files(fj)
rt = r'E:\GFCT\Evidencias\ZONAD2.TXT'
records = open(rt).readlines()
rec_in = []
for record in records:
    rec_in.append(ff.parse(record))
rec_in
for rec in rec_in:
    print rec

for n, r in enumerate(rec_in):
    print ff.unparse(r) == records[n]
