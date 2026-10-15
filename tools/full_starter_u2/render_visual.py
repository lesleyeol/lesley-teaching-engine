#!/usr/bin/env python3
"""Presentation-only adaptive pagination over the unchanged lesson item bank.

An isolated temporary copy of the existing generator changes only page caps.
No question stem, answer, evidence status, source, or Gate is modified.
All generated HTML remains standalone; no CDN/fonts/scripts are required.
"""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile,shutil,re
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parent
ORIGINAL=ROOT/'output'
DEST=ROOT/'output_visual'
STYLE=(ROOT/'visual_design.css').read_text(encoding='utf-8')
# Keep baseline generator release entirely untouched.
subprocess.run([sys.executable,str(ROOT/'render_pack.py')],cwd=ROOT,check=True)
changes={
 "cap=5 if s['display'] in ['family','location','distance'] else 6":"cap=5 if s['display'] in ['family','location','distance'] else 6",
 "if s['id']=='U2-A':cap=7":"if s['id']=='U2-A':cap=7",
 "if s['id']=='U2-C' and stage=='practice':cap=6":"if s['id']=='U2-C' and stage=='practice':cap=4",
 "cap={'S-A':8,'S-C':9,'U1-A':7,'U1-B':6,'U1-C':8,'U1-D':8,'U2-B':8,'R-M':8}[s['id']]":"cap={'S-A':5,'S-C':5,'U1-A':7,'U1-B':3,'U1-C':5,'U1-D':5,'U2-B':5,'R-M':5}[s['id']]",
 "if s['id'] in ('S-CHECK','U2-CHECK') and stage=='check':cap=6":"if s['id'] in ('S-CHECK','U2-CHECK') and stage=='check':cap=6",
 "enumerate(paginate(arr,6))":"enumerate(paginate(arr,5 if unit=='Unit 2' and st=='practice' else 6))",
 "def paginate(lst,n):return [lst[i:i+n] for i in range(0,len(lst),n)]": "def paginate(lst,n):\n    groups=(len(lst)+n-1)//n\n    if not groups:return []\n    base,extra=divmod(len(lst),groups)\n    sizes=[base+(i<extra) for i in range(groups)]\n    pos=0;parts=[]\n    for size in sizes:parts.append(lst[pos:pos+size]);pos+=size\n    return parts",
}

original_code=(ROOT/'render_pack.py').read_text(encoding='utf-8')
visual_code=original_code
for before,after in changes.items():
    assert visual_code.count(before)==1,(before,visual_code.count(before))
    visual_code=visual_code.replace(before,after,1)

# Make comparison independent of CSS and pagination, preserving per-item text and IDs.
class ItemParser(HTMLParser):
    def __init__(self):super().__init__();self.items=[];self.in_item=False;self.cur=[];self.level=0
    def handle_starttag(self,tag,attrs):
        cls=dict(attrs).get('class','').split()
        if tag=='div' and 'item' in cls and not self.in_item:
            self.in_item=True;self.level=1;self.cur=[]
        elif self.in_item and tag=='div':self.level+=1
    def handle_endtag(self,tag):
        if self.in_item and tag=='div':
            self.level-=1
            if self.level==0:
                self.in_item=False
                self.items.append(' '.join(''.join(self.cur).split()))
    def handle_data(self,txt):
        if self.in_item:self.cur.append(txt)

def extract_items(text):
    parser=ItemParser();parser.feed(text)
    # Numbering re-starts at each page and is not pedagogical question content.
    return [re.sub(r'^\d{2}\.\s*','',a) for a in parser.items]

DEST.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory(prefix='lesley_visual_') as td:
    work=Path(td)
    for name in ['author_data.py','legacy_subject_be.items.json','unit_scope_item_bank.json']:
        shutil.copyfile(ROOT/name,work/name)
    (work/'render_pack.py').write_text(visual_code,encoding='utf-8')
    subprocess.run([sys.executable,str(work/'render_pack.py')],cwd=work,check=True)
    report=[]
    for file in sorted((work/'output').glob('*.html')):
        base=(ORIGINAL/file.name).read_text(encoding='utf-8')
        raw=file.read_text(encoding='utf-8')
        if file.name in ['student_practice.html','starter_student.html','unit1_student.html','unit2_student.html','review_student.html','independent_check_teacher_hold.html','delayed_teacher_hold.html']:
            assert extract_items(raw)==extract_items(base), f'Student content changed: {file.name}'
        assert raw.count('</style>')==1
        opt=raw.replace('</style>','\n/* LESLEY_VISUAL_LAYER_V02 */\n'+STYLE+'\n</style>',1)
        # Formatting-only: printed **emphasis** is rendered as bold, not literal markdown punctuation.
        opt=opt.replace('練習是**文字辨識**','練習是<strong>文字辨識</strong>')
        # Guided-only comparison grids: source phrases moved into columns, not rewritten.
        opt=opt.replace('<div class="rule">I–am；he/she/it–is；you/we/they–are。主格作主詞，所有格放名詞前。</div>',
          '<div class="rule-comparison"><div class="rule-cells">'+
          ''.join('<span class="rule-cell">'+v+'</span>' for v in ('I–am','he/she/it–is','you/we/they–are'))+
          '</div><div class="rule-note">主格作主詞，所有格放名詞前。</div></div>')
        opt=opt.replace('<div class="rule">近單 this、近複 these；遠單 that、遠複 those。單數 is，複數 are。</div>',
          '<div class="rule-comparison two"><div class="rule-cells">'+
          ''.join('<span class="rule-cell">'+v+'</span>' for v in ('近單 this、近複 these','遠單 that、遠複 those'))+
          '</div><div class="rule-note">單數 is，複數 are。</div></div>')

        # Letter-case tasks use four-line handwriting guides; stems and accepted answers stay identical.
        for item_id in ('S-A-P01','S-A-P02','S-A-P03','S-CHECK-C01'):
            idx=opt.find('>'+item_id+'</span>')
            if idx>=0:
                start=opt.rfind('<div class="item">',0,idx)
                if start>=0: opt=opt[:start]+opt[start:].replace('<div class="item">','<div class="item handwriting">',1)

        (DEST/file.name).write_text(opt,encoding='utf-8')
        report.append({'file':file.name,'question_content_exact':True if file.name.startswith(('student','starter','unit','review','independent','delayed')) else 'from unchanged bank','item_count':len(extract_items(raw)),'sha256_visual_html':hashlib.sha256(opt.encode('utf-8')).hexdigest()})
    (DEST/'visual_integrity.json').write_text(json.dumps({'status':'DRAFT_FOR_TEACHER_REVIEW','layer':'visual-only','source_data_untouched':True,'page_caps_reduced_for_larger_handwriting_space':True,'files':report},ensure_ascii=False,indent=2),encoding='utf-8')
print('VISUAL HTML:',len(report),'files; original item content preserved')