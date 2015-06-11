from columns import Columns
col = Columns()
cols = col.columns(r'C:\BNB\S303\ORIGINAIS\BOOK\B303001.txt', signal=False)
for c in cols:
    print c
cols = col.columns(r'C:\BNB\S303\ORIGINAIS\BOOK\B303001.txt', fmt='cob',signal=False)
for c in cols:
    print c
