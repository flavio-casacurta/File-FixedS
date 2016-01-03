from columns import Columns
col = Columns()
book = r'E:\GFCT\Evidencias\cpy\GFCTB092.CPY'
bookwrite = open(r'E:\GFCT\Evidencias\cpy\gfctb092.json', 'w')
bookwrite.writelines(col.columns(book, signal=False))
bookwrite.close()
