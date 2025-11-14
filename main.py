#{{{ config
HIDE_SN = ['8804', '9002', '9001', '8800', '8802', '8799', '853']
ALEFBET = 'אבגדהוזחטיכלמנסעפצקרשת'
TAIL_MAP = {'ך': 'כ', 'ם': 'מ', 'ן': 'נ', 'ף': 'פ', 'ץ': 'צ'}
#}}}

class Hebrew: #{{{
    def sn2hb(self, sn): # sn -> hb
        sn = str(sn).zfill(5)
        return DICT.get(sn, {}).get('orig', False)

    def trim(self, hb): # hb -> 无元音标记&替换尾型hb
        hb = ''.join([ TAIL_MAP.get(c, c) for c in hb ])
        return ''.join([ c for c in hb if c in ALEFBET + ' -\n' ])

    def split(self, hb): # 'aa bb-cc' -> ['aa', 'bb', 'cc']
        return list({ part:1 for part in re.split(r'[\s\-]', hb) })

    def sn2hb_lst(self, sn):
        hb = self.sn2hb(sn)
        if not hb:
            return []
        hb = self.trim(hb)
        return self.split(hb)
    
    def atbash(self, hb): # abc => zyx
        return ''.join([ ALEFBET[21-ALEFBET.index(c)] for c in hb ])
#}}}
H = Hebrew()

DICT = json.load(open('dict.json'))
BOOK = json.load(open('book.json'))

#{{{ init: plst_hb
r_sn = re.compile(r'{?<[A-Z]+0*([0-9]+?)>}?')

plst_sn = {}
for book, info in BOOK.items():
  for cpt, secs in enumerate(info['cpts'], 1):
    key = (book, cpt)
    for i, sec in enumerate(secs, 1):
      for sn in r_sn.findall(sec['sn']):
        plst_sn.setdefault(sn, {}).setdefault(key, []).append(i)

plst_hb = {}
for sn, hits in plst_sn.items():
  for hb in H.sn2hb_lst(sn):
    for key, sec_ids in hits.items():
      plst_hb.setdefault(hb, {}).setdefault(key, []).extend(sec_ids)
#}}}

tabs = [ {'book': '创', 'cpt': 2, 'marks': {11,12,13,14}} ]
tab_id = 0
words = [] # dict: sn&id / hb

render()
page['#loading'].classes.add('!hidden')
