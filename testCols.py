from columns import Columns
col = Columns()
cols = col.columns(r'C:\BNB\S303\ORIGINAIS\BOOK\B303001.txt')
for c in cols:
    print c
cols = col.columns(r'C:\BNB\S303\ORIGINAIS\BOOK\B303001.txt', fmt='cob')
for c in cols:
    print c
