# py-bemsh
BESM-6 BEMSH-subset "toy" compiler written in python3 using PLY

Text consts using UTF-8 encoding.

New label aligns code with "МОДА 0" if necessary to fit one machine word which is 48-bits size.

Consts can be define with keyword "КОНК" for semiword sized value and "КОНД" which fit exactly one machine word.

| Type | Example |
|------|---------|
| octal | '245' or в'123' |
| binary | к'1001010' |
| decimal | 99 |
| text | п'Это текст' |
| octal with shift modifier | м10в'432' |

For this example programm:
```
; простейшая программа        
        старт   512
prog    э64     инф64
        пб      (13)
инф64   мода    текст1 ;ntrcn
        мода    текст1
        конк    к'000010000'
        конк    к'100000000'
текст1  текст   п'Приветик! Это автокод БЕМШ.'
        конд    м40b'231'
```

Output is:
```
Дерево разбора:
[[('EMPTY', 0, 0)],
 ('TRAN', 'старт', 512),
 ('LABEL', 'prog'),
 ('OPCODE', 'э64', {'idx': 0, 'offset': ('LABEL', 'инф64')}),
 ('OPCODE', 'пб', {'idx': 13, 'offset': 0}),
 ('LABEL', 'инф64'),
 ('OPCODE', 'мода', {'idx': 0, 'offset': ('LABEL', 'текст1')}),
 ('OPCODE', 'мода', {'idx': 0, 'offset': ('LABEL', 'текст1')}),
 ('TRAN', 'конк', 16),
 ('TRAN', 'конк', 256),
 ('LABEL', 'текст1'),
 ('TRAN', 'текст', 'Приветик! Это автокод БЕМШ.'),
 ('TRAN', 'конд', 168225279049728)]
Warning: Unknown token: [('EMPTY', 0, 0)]
Внутреннее представление:
Address: 00001000 Data: ('OPCODE', 'э64', {'idx': 0, 'offset': ('LABEL', 'инф64')})
Address: 00001000 Data: ('OPCODE', 'пб', {'idx': 13, 'offset': 0})
Address: 00001001 Data: ('OPCODE', 'мода', {'idx': 0, 'offset': ('LABEL', 'текст1')})
Address: 00001001 Data: ('OPCODE', 'мода', {'idx': 0, 'offset': ('LABEL', 'текст1')})
Address: 00001002 Data: ('TRAN', 'конк', 16)
Address: 00001002 Data: ('TRAN', 'конк', 256)
Address: 00001003 Data: ('TRAN', 'конк', b'\xd0\x9f\xd1')
Address: 00001003 Data: ('TRAN', 'конк', b'\x80\xd0\xb8')
Address: 00001004 Data: ('TRAN', 'конк', b'\xd0\xb2\xd0')
Address: 00001004 Data: ('TRAN', 'конк', b'\xb5\xd1\x82')
Address: 00001005 Data: ('TRAN', 'конк', b'\xd0\xb8\xd0')
Address: 00001005 Data: ('TRAN', 'конк', b'\xba! ')
Address: 00001006 Data: ('TRAN', 'конк', b'\xd0\xad\xd1')
Address: 00001006 Data: ('TRAN', 'конк', b'\x82\xd0\xbe')
Address: 00001007 Data: ('TRAN', 'конк', b' \xd0\xb0')
Address: 00001007 Data: ('TRAN', 'конк', b'\xd0\xb2\xd1')
Address: 00001010 Data: ('TRAN', 'конк', b'\x82\xd0\xbe')
Address: 00001010 Data: ('TRAN', 'конк', b'\xd0\xba\xd0')
Address: 00001011 Data: ('TRAN', 'конк', b'\xbe\xd0\xb4')
Address: 00001011 Data: ('TRAN', 'конк', b' \xd0\x91')
Address: 00001012 Data: ('TRAN', 'конк', b'\xd0\x95\xd0')
Address: 00001012 Data: ('TRAN', 'конк', b'\x9c\xd0\xa8')
Address: 00001013 Data: ('TRAN', 'конк', b'.  ')
Address: 00001013 Data: ('TRAN', 'конк', b'   ')
Address: 00001014 Data: ('TRAN', 'конк', 10027008)
Address: 00001014 Data: 0('TRAN', 'конк', 0)
Адреса меток:
Label: prog     Address: 01000
Label: инф64    Address: 01001
Label: текст1   Address: 01003
Вычисленные метки прописаны:
[(1024, ('OPCODE', 'э64', {'idx': 0, 'offset': 513})),
 (1025, ('OPCODE', 'пб', {'idx': 13, 'offset': 0})),
 (1026, ('OPCODE', 'мода', {'idx': 0, 'offset': 515})),
 (1027, ('OPCODE', 'мода', {'idx': 0, 'offset': 515})),
 (1028, ('TRAN', 'конк', 16)),
 (1029, ('TRAN', 'конк', 256)),
 (1030, ('TRAN', 'конк', b'\xd0\x9f\xd1')),
 (1031, ('TRAN', 'конк', b'\x80\xd0\xb8')),
 (1032, ('TRAN', 'конк', b'\xd0\xb2\xd0')),
 (1033, ('TRAN', 'конк', b'\xb5\xd1\x82')),
 (1034, ('TRAN', 'конк', b'\xd0\xb8\xd0')),
 (1035, ('TRAN', 'конк', b'\xba! ')),
 (1036, ('TRAN', 'конк', b'\xd0\xad\xd1')),
 (1037, ('TRAN', 'конк', b'\x82\xd0\xbe')),
 (1038, ('TRAN', 'конк', b' \xd0\xb0')),
 (1039, ('TRAN', 'конк', b'\xd0\xb2\xd1')),
 (1040, ('TRAN', 'конк', b'\x82\xd0\xbe')),
 (1041, ('TRAN', 'конк', b'\xd0\xba\xd0')),
 (1042, ('TRAN', 'конк', b'\xbe\xd0\xb4')),
 (1043, ('TRAN', 'конк', b' \xd0\x91')),
 (1044, ('TRAN', 'конк', b'\xd0\x95\xd0')),
 (1045, ('TRAN', 'конк', b'\x9c\xd0\xa8')),
 (1046, ('TRAN', 'конк', b'.  ')),
 (1047, ('TRAN', 'конк', b'   ')),
 (1048, ('TRAN', 'конк', 10027008)),
 (1049, ('TRAN', 'конк', 0))]
Машинный код
Address:   1000 Data: 0064100167000000
Address:   1001 Data: 0220100302201003
Address:   1002 Data: 0000002000000400
Address:   1003 Data: 6411772140150270
Address:   1004 Data: 6413132055350602
Address:   1005 Data: 6413432056420440
Address:   1006 Data: 6412672140550276
Address:   1007 Data: 1015026064131321
Address:   1010 Data: 4055027664135320
Address:   1011 Data: 5755026410150221
Address:   1012 Data: 6411272047150250
Address:   1013 Data: 1342004010020040
Address:   1014 Data: 4620000000000000
```
