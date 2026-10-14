# -*- coding:utf8 -*-
from pathlib import Path
import json,sys,re
import fitz
BASE=Path(__file__).resolve().parent
pkg=json.loads((BASE/'unit_scope_item_bank.json').read_text(encoding='utf8'))
report=json.loads((BASE/'QA_RENDERING.json').read_text(encoding='utf8'))
kp={x['id']:x for x in pkg['knowledge_points']};its=pkg['items'];sources=pkg['sources'];o=BASE/'output'
errs=[];checks=[]
def t(label,ok):
 checks.append(dict(check=label,passed=bool(ok)))
 if not ok:errs.append(label)
t('All 46 source knowledge points are explicitly listed',len(kp)==46)
t('All three requested units are present',set(pkg['scope'])>=set(['Starter','Unit 1','Unit 2']))
t('All 185 questions have unique ID',len(its)==185 and len({x['id'] for x in its})==185)
t('All knowledge points have at least one traceable item',all(any(x['kp']==k for x in its) for k in kp))
t('Every item references an existing source and has an answer',all(x['answer'] and x['rationale'] and set(x['source_refs']).issubset(sources) for x in its))
t('All check/delayed items carry no explicit author hints',all(not x.get('hint') for x in its if x['stage'] in ('check','delayed')))
t('Retained legacy Starter PR8 has 16 exact source records',sum(bool(x.get('legacy_preserved')) for x in its)==16)
t('Vocabulary Word Bank Unit1 exactly 29 and Unit2 36',len(pkg['word_banks']['Unit 1'])==29 and len(pkg['word_banks']['Unit 2'])==36)
t('No audio-dependent question is falsely marked as listening-validated',len(pkg['audio_gaps'])==4 and all(x['state']=='AUDIO_PENDING' for x in pkg['audio_gaps']))
t('No contradictory official release claim',pkg['status']=='DRAFT_FOR_TEACHER_REVIEW' and pkg['source_status']=='READY_WITH_LIMITS')
t('All required printable output files exist',all((o/(x+'.pdf')).is_file() for x in ['student_practice','teacher_complete','answer_key','independent_check_teacher_hold','delayed_teacher_hold','vocabulary_companion','source_matrix','starter_student','unit1_student','unit2_student']))
t('No page content overflow reported',report['overflow_count']==0)
t('All PDF counts match their explicit A4 HTML page layouts',all(q['html_pages']==q['pdf_pages'] and not q['page_size_errors'] for q in report['rendered']))
main=fitz.open(o/'student_practice.pdf'); check=fitz.open(o/'independent_check_teacher_hold.pdf'); delayed=fitz.open(o/'delayed_teacher_hold.pdf'); teacher=fitz.open(o/'teacher_complete.pdf');ans=fitz.open(o/'answer_key.pdf')
student_txt='\n'.join(p.get_text() for p in main)
check_txt='\n'.join(p.get_text() for p in check)
delayed_txt='\n'.join(p.get_text() for p in delayed)
teacher_txt='\n'.join(p.get_text() for p in teacher)
ans_txt='\n'.join(p.get_text() for p in ans)
t('Student practice does not contain teacher-only answer/rationale labels','答案：' not in student_txt and '觀察：' not in student_txt)
t('All check items excluded from guided student booklet',all(x['id'] not in student_txt for x in its if x['stage']=='check'))
t('All delayed IDs excluded from student practice and check booklet',all(x['id'] not in student_txt and x['id'] not in check_txt for x in its if x['stage']=='delayed'))
t('Every item is covered in teacher or answer key',all(x['id'] in teacher_txt and x['id'] in ans_txt for x in its))
vocab_pdf=fitz.open(o/'vocabulary_companion.pdf');vocab_txt='\n'.join(p.get_text() for p in vocab_pdf)
t('All 65 vocabulary source entries are present in student vocabulary handout',all(en in vocab_txt for words in pkg['word_banks'].values() for en,zh in words))
t('Print PDFs are no larger than 2 MB each',all(q['bytes'] < 2_000_000 for q in report['rendered']))
summary={"date":"2026-10-15","status":"STATIC_AND_RENDER_QA_ONLY_NOT_FORMAL_RELEASE","tests":len(checks),"passed":len(checks)-len(errs),"failures":errs,"checklist":checks,"knowledge_points":len(kp),"items":len(its),"vocabulary":{k:len(v) for k,v in pkg['word_banks'].items()},"audio_pending":len(pkg['audio_gaps']),"pages":{q['file']:q['pdf_pages'] for q in report['rendered']}}
(BASE/'QA_FINAL.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
print('QA',len(checks)-len(errs),'/',len(checks),'failures:',errs)
if errs:sys.exit(1)