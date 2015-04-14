from attribute import Attribute
attr = Attribute()
line = '03  C-G-C-RB            PIC S9(14)V(4)  COMP-3.'
pic = line.split('PIC')[1].replace('.','').split()
att = attr.attribute_json(pic[0], pic[1])
print att
line = '03  C-G-C-RB            PIC S9(4)  COMP.'
pic = line.split('PIC')[1].replace('.','').split()
att = attr.attribute_json(pic[0], pic[1])
print att
line = '03  C-G-C-RB            PIC X(24).'
pic = line.split('PIC')[1].replace('.','').split()
att = attr.attribute_json(pic[0])
print att
