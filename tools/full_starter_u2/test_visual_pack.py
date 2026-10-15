#!/usr/bin/env python3
"""Standard-library smoke checks for visual-only generation; no PDF tooling needed."""
from pathlib import Path
import subprocess,sys,json,re
root=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(root/'render_visual.py')],cwd=root,check=True)
out=root/'output_visual'
report=json.loads((out/'visual_integrity.json').read_text(encoding='utf8'))
bank=json.loads((root/'unit_scope_item_bank.json').read_text(encoding='utf8'))
assert report['source_data_untouched'] is True
assert len(report['files'])==11
assert len(bank['knowledge_points'])==46 and len(bank['items'])==185
assert len(bank['word_banks']['Unit 1'])+len(bank['word_banks']['Unit 2'])==65
student=(out/'student_practice.html').read_text(encoding='utf8')
check=(out/'independent_check_teacher_hold.html').read_text(encoding='utf8')
delayed=(out/'delayed_teacher_hold.html').read_text(encoding='utf8')
assert 'LESLEY_VISUAL_LAYER_V02' in student and '--slate-12:#1c2024' in student
assert '--student-size:13.5pt' in student
assert '<div class="rule-comparison"' in student
assert 'item handwriting' in student
assert '練習是**文字辨識**' not in student
assert '練習是<strong>文字辨識</strong>' in student
for item in bank['items']:
    if item['stage']=='check': assert item['id'] not in student
    if item['stage']=='delayed': assert item['id'] not in student
assert 'DRAFT' in student
assert '<script src=' not in student and '@import url(' not in student
assert len(re.findall(r'<section class="page"', student)) >= 20
print('PASS: visual-only output, 46 KP, 185 items, 65 words, answer isolation and offline styles.')