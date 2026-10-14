import asyncio,json,re,os
from pathlib import Path
from collections import Counter
from playwright.async_api import async_playwright
import fitz
root=Path(__file__).resolve().parent; out=root/'output'
files=['student_practice','starter_student','unit1_student','unit2_student','review_student','independent_check_teacher_hold','delayed_teacher_hold','teacher_complete','answer_key','vocabulary_companion','source_matrix']
async def main():
 overs=[]; printouts=[]
 async with async_playwright() as pl:
  browser=await pl.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'])
  page=await browser.new_page(viewport={'width':1100,'height':900},device_scale_factor=1)
  for name in files:
   html=out/(name+'.html');assert html.exists(),html
   await page.set_content(html.read_text(encoding='utf8'),wait_until='load')
   await page.evaluate('document.fonts.ready')
   details=await page.evaluate('''()=>[...document.querySelectorAll('.page')].map((p,i)=>{let b=p.querySelector('.body');return {page:i+1,bodyClient:b.clientHeight,bodyScroll:b.scrollHeight,excess:b.scrollHeight-b.clientHeight,bodyChild:b.lastElementChild?.getBoundingClientRect().bottom-b.getBoundingClientRect().bottom||0,title:p.querySelector('h1')?.innerText};})''')
   issues=[dict(filename=name,**o) for o in details if o['excess']>3 or o['bodyChild']>4]
   overs.extend(issues)
   pdf=out/(name+'.pdf')
   await page.pdf(path=str(pdf),print_background=True,prefer_css_page_size=True,margin={'top':'0','bottom':'0','left':'0','right':'0'})
   d=fitz.open(pdf)
   maxerr=[]
   for i,p in enumerate(d):
    if abs(p.rect.width-595.28)>3 or abs(p.rect.height-841.89)>3:maxerr.append(i+1)
   printouts.append({'file':name,'html_pages':len(details),'pdf_pages':len(d),'page_size_errors':maxerr,'bytes':pdf.stat().st_size})
   d.close()
   print(name,'HTML',len(details),'PDF',printouts[-1]['pdf_pages'],'overflows',len(issues))
  await browser.close()
 (root/'QA_RENDERING.json').write_text(json.dumps({'overflow_count':len(overs),'overflow_details':overs,'rendered':printouts},ensure_ascii=False,indent=2),encoding='utf8')
 print('OVERFLOWS',len(overs))
 for i in overs[:30]:print(i)
asyncio.run(main())