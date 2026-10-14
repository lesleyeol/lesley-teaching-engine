# -*- coding: utf-8 -*-
"""Teacher-authored, source-bound scope and question bank. NOT an official test release.
No student records or copyrighted source scans included.
"""
import json, re
from pathlib import Path
BASE=Path(__file__).resolve().parent
SOURCES={
'SL':dict(name='翰林國中英文七上 Starter｜字母書寫',file='學校課本Starter & Unit 1.pdf',pdf='5',printed='1–2',note='大小寫、抄寫、拼字與書寫格線'),
'SP':dict(name='Starter｜字母拼讀',file='學校課本Starter & Unit 1.pdf',pdf='6',printed='3–4',note='a/e/i/o/u 短母音、仿讀；聽力無音檔不得驗收'),
'SG':dict(name='Starter｜代名詞與所有格',file='學校課本Starter & Unit 1.pdf',pdf='7',printed='5–6',note='主格／所有格、be 搭配／縮寫、姓名問答'),
'SW':dict(name='Starter｜年齡、數字與書寫',file='學校課本Starter & Unit 1.pdf',pdf='8',printed='7–8',note='年齡、數字、大小寫標點與短對話'),
'U1D':dict(name='Unit 1｜對話與人物／職業',file='學校課本Starter & Unit 1.pdf',pdf='9–11',printed='9–14',note='人物身分與職業、be 肯定／否定／疑問、問候與身分'),
'U1G':dict(name='Unit 1｜形容詞與家庭 Who',file='學校課本Starter & Unit 1.pdf',pdf='12–13',printed='15–18',note='形容詞、問 Who、家族成員與人物指涉'),
'U1R':dict(name='Unit 1｜閱讀 My Dear Family',file='學校課本Starter & Unit 1.pdf',pdf='14',printed='19–20',note='從人物、年齡、職業與學校階段回文定位'),
'U1S':dict(name='Unit 1｜Sounds and Letters',file='學校課本Starter & Unit 1.pdf',pdf='15',printed='21–22',note='初始及尾音字母拼讀；無音檔時只作字形與讀法支架'),
'U1E':dict(name='Unit 1｜Extension Word Power',file='學校課本Starter & Unit 1.pdf',pdf='17',printed='25–26',note='-er 職業構詞；標示延伸，未確認教師採教進度'),
'U1W':dict(name='Unit 1｜Word Bank',file='學校課本Starter & Unit 1.pdf',pdf='18',printed='137–138',note='課本單字與例句，並非單獨的學會證據'),
'U2D':dict(name='Unit 2｜對話與文具／房屋詞彙',file='Unit 2.pdf',pdf='1–3',printed='27–32',note='名詞、房間、物品、單數 What is this/that'),
'U2P':dict(name='Unit 2｜名詞複數、指示詞',file='Unit 2.pdf',pdf='4',printed='33–34',note='-s/-es/-ies/-ves、不規則、近遠與單複數、詞尾讀音'),
'U2L':dict(name='Unit 2｜位置介系詞與 Where',file='Unit 2.pdf',pdf='5–6',printed='35–38',note='房間、in/on/under/behind/between/next to/near/in front of, Where is/are'),
'U2R':dict(name='Unit 2｜閱讀 The Keret House',file='Unit 2.pdf',pdf='7',printed='39–40',note='特別房屋的描述與位置關係、inside/above/right next to/enough'),
'U2S':dict(name='Unit 2｜Sounds and Letters',file='Unit 2.pdf',pdf='8',printed='41–42',note='字形對應與聲音分類；未提供音檔不能當聽辨證據'),
'U2V':dict(name='Unit 2｜Word Bank／Review 1',file='Unit 2.pdf',pdf='10–11,13–14',printed='45–48,139–141',note='Unit 2 詞彙、Starter–U2 螺旋複習、口語目標'),
}
KP={}
def k(id,unit,name,sources,method='practice',kind='Core',comment=''):
    assert id not in KP;KP[id]=dict(id=id,unit=unit,name=name,sources=sources,method=method,kind=kind,comment=comment)
# Starter
k('S01','Starter','A–Z 大小寫對應與正確字形',['SL'])
k('S02','Starter','拼字、大小寫及書寫規範',['SL'])
for i,v in enumerate('aeiou',3):k(f'S{i:02}', 'Starter', f'短母音 {v} 的字形與拼讀辨識',['SP'],kind='Text Only',comment='字母及音節的書面辨識；需另外口頭或正式音檔檢核發音')
k('S08','Starter','主格代名詞 I/you/he/she/it/we/they',['SG'])
k('S09','Starter','所有格 my/your/his/her/its/our/their',['SG'])
k('S10','Starter','主格與 am/is/are 肯定式一致',['SG'])
k('S11','Starter','主格與 be 縮寫與 apostrophe',['SG'])
k('S12','Starter','What is ... name? 姓名問答',['SG'])
k('S13','Starter','How old ...? 年齡問答',['SW'])
k('S14','Starter','0–99 基礎數字、拼寫與連字號',['SW'])
k('S15','Starter','句首、人名、I 大寫及標點／空格',['SW'])
k('S16','Starter','問候與對話角色回應',['SW'],kind='Core / Oral Check')
# Unit 1
k('U101','Unit 1','人物職業與身分單字辨識／拼寫',['U1D','U1W'])
k('U102','Unit 1','家庭親屬關係與指涉',['U1G','U1W'])
k('U103','Unit 1','Who is he/she/that ...? 人物詢問',['U1D','U1G'])
k('U104','Unit 1','be 肯定、否定、Yes/No 問句與簡答',['U1D'])
k('U105','Unit 1','形容詞 be 後與名詞前的語序',['U1G'])
k('U106','Unit 1','用 what job / 身分回答職業',['U1D','U1W'])
k('U107','Unit 1','名詞所有格 ’s 與家屬指涉',['U1D','U1G'])
k('U108','Unit 1','年齡 years old 與人物外貌描述',['U1D','U1G'])
k('U109','Unit 1','家庭介紹閱讀回文找證據',['U1R'])
k('U110','Unit 1','英語清濁輔音拼讀辨識',['U1S'],kind='Text Only',comment='無原始音檔，不能驗證聽辨')
k('U111','Unit 1','-er 人物／職業構詞',['U1E'],kind='Extension',comment='延伸範圍；教師需確認已教')
k('U112','Unit 1','介紹自己／家人並回答問句',['U1D','U1E'],kind='Core / Oral Check')
k('U113','Unit 1','Who／How old／What 的問句功能區辨',['U1D','U1G'])
# Unit 2
k('U201','Unit 2','文具、房間與生活物品詞彙',['U2D','U2V'])
k('U202','Unit 2','單數可數名詞 a／an、one 與 is',['U2D'])
k('U203','Unit 2','複數 -s / -es',['U2P'])
k('U204','Unit 2','複數字尾 y→ies 與 f/fe→ves',['U2P'])
k('U205','Unit 2','不規則複數 mouse/mice、person/people、woman/women',['U2P'])
k('U206','Unit 2','複合名詞複數 pencil boxes／comic books',['U2P'])
k('U207','Unit 2','this/that/these/those 的遠近與數量',['U2D','U2P'])
k('U208','Unit 2','What is／are + 指示詞問答',['U2D','U2P'])
k('U209','Unit 2','單複數主詞、they 與 be 動詞一致',['U2P','U2L'])
k('U210','Unit 2','Where is／are 問位置並以 It/They 回答',['U2L'])
k('U211','Unit 2','in/on/under/next to/near/behind/between/in front of',['U2L'])
k('U212','Unit 2','房間名稱、方位描述及閱讀',['U2L','U2R'])
k('U213','Unit 2','顏色與 favorite color、肯否定短對話',['U2D'])
k('U214','Unit 2','複數 -s 字尾 /s/ /z/ /ɪz/ 讀音區辨',['U2P','U2S'],kind='Text Only',comment='僅書面分類與口頭跟讀，無音檔不做正式聽力')
k('U215','Unit 2','特殊空間屋描述 inside/above/right next to/enough',['U2R','U2V'])
k('U216','Unit 2','Unit 1–2 合併閱讀與跨單元問答',['U2V'])
k('U217','Unit 2','口頭指認物品和位置',['U2L'],kind='Core / Oral Check')

SECTIONS=[]; ITEMS=[]
def section(unit,id,title,summary,kps,rule='',display='worksheet'):
    assert all(x in KP for x in kps); SECTIONS.append(dict(id=id,unit=unit,title=title,summary=summary,kps=kps,rule=rule,display=display))
def item(sec,kp,prompt,answer,rationale,source=None,stage='practice',form='write',opts=None,accepted=None,context='',hint='',diagnosis=''):
    idx=sum(i['section']==sec and i['stage']==stage for i in ITEMS)+1
    unit=next(s['unit'] for s in SECTIONS if s['id']==sec)
    prefix={'practice':'P','check':'C','delayed':'D','teacher':'T'}[stage]
    id=f'{sec}-{prefix}{idx:02}'
    assert kp in KP, id
    refs=source or KP[kp]['sources']
    ITEM=dict(id=id,section=sec,unit=unit,kp=kp,prompt=prompt,answer=answer,rationale=rationale,source_refs=refs,stage=stage,form=form,options=opts or [],accepted=accepted or [answer],context=context,hint=hint,diagnosis=diagnosis or f'若錯，先查核「{KP[kp]["name"]}」的理解，再用未曝光題重測。')
    ITEMS.append(ITEM);return id

# ----------------------------------------- Student guided / practice -----------------------------------------
section('Starter','S-A','字母與拼讀','先辨識大小寫，再把字母和聲音連起來。',['S01','S02','S03','S04','S05','S06','S07'],'小寫變化要保留正確字母形狀。短母音練習是**文字辨識**，真正發音需教師另外聽學生唸。')
item('S-A','S01','請將 B 改成小寫。','b','B 的小寫是 b。')
item('S-A','S01','請將 q 改成大寫。','Q','q 的大寫是 Q。')
item('S-A','S02','將 QUIZ 全部寫成小寫。','quiz','英文大小寫變換不改字母順序。')
for code,baseword,options,ans in [('S03','van','ham / bed','ham'),('S04','bed','red / pig','red'),('S05','pig','kilt / mug','kilt'),('S06','fox','box / wet','box'),('S07','sun','mug / red','mug')]:
 item('S-A',code,f'哪個字與 {baseword} 的短母音相同？請選寫：{options}',''+ans,f'{baseword} 與 {ans} 含相同短母音。',form='short')

section('Starter','S-B','主格、所有格與 be','先判斷「誰」和「誰的」，再選正確的 be。',['S08','S09','S10','S11'], 'I–am；he/she/it–is；you/we/they–are。主格作主詞，所有格放名詞前。',display='guided')
# Restore original PR#8 G01-G03 verbatim (imported by separate pipeline below) and keep own tasks additional
item('S-B','S09','I am Mark. ______ name is Mark.','My','I 的所有格是 my，放 name 前。')
item('S-B','S09','She is Tina. ______ name is Tina.','Her','She 的所有格是 her。')
item('S-B','S09','They are Mr. and Mrs. Lin. ______ son is Ben.','Their','They 的所有格是 their。')
item('S-B','S09','It is Lucky. ______ name is Lucky.','Its','Its 是它的；It’s 是 it is。')
item('S-B','S11','He is Gary. → 寫出縮寫句。',"He's Gary.",'he is 縮寫為 he’s；要保留撇號。',form='rewrite')
item('S-B','S11','We are students. → 寫出縮寫句。',"We're students.",'we are 縮寫為 we’re；students 見原課例句。',form='rewrite')
item('S-B','S08','Gary and Mark 要用哪個主格代名詞？','They','兩名非說話者，用 they。')
item('S-B','S10','You and I ____ students.','are','兩人合稱 we，故用 are；此題不代替視角檢核。')

section('Starter','S-C','姓名、年齡與數字','看到問題，先判斷是問「姓名」還是「年齡」。',['S12','S13','S14'],'姓名：What is ... name?；年齡：How old is ...?。40 拼成 forty。')
item('S-C','S12','Name card: Tina (girl). Q: What is her name? A: ______','Her name is Tina.','her 指女性人物的所有格；答人名 Tina。',form='short')
item('S-C','S12','Name card: Lucky (dog). Q: What is its name? A: ______',"Its name is Lucky.",'its 修飾 name；狗名 Lucky。',form='short')
item('S-C','S12','將「his / name / What / is / ?」重排成問句。','What is his name?','疑問詞 What + is + his name。',form='rewrite')
item('S-C','S13','Age card: Gary, 13. Q: How old is Gary? A: ______','He is thirteen years old.','Gary 為男性，13 讀 thirteen。',form='short')
item('S-C','S13','Age card: Tina, 14. Q: How old is she? A: ______','She is fourteen years old.','第三人稱單數 she 搭配 is。',form='short')
for num,ans in [(40,'forty'),(15,'fifteen'),(82,'eighty-two'),(33,'thirty-three')]:
 item('S-C','S14',f'請將數字 {num} 寫成英文。',ans,'整十字形及二位數連字號要正確。')

section('Starter','S-D','書寫與問候','改正大小寫及標點，最後完成簡短對話。',['S15','S16'],'句首與姓名大寫；問句用 ?；I 永遠大寫。')
for p,a in [('what is your name.','What is your name?'),('my name is kelly.','My name is Kelly.'),('how old is tina?','How old is Tina?')]:
 item('S-D','S15',f'請改正：{p}',a,'句首、人名大寫；句末標點依語氣。',form='rewrite')
item('S-D','S16','A: Hello, Gary. How are you?  B: ______ (我很好，謝謝。)',"I'm fine. Thank you.",'應答詢問近況，可用 I’m fine. Thank you。',form='short')
item('S-D','S16','兩位學生剛見面。寫一句合適的英文打招呼。','Hello.','可接受 Hi. / Hello.；此題不作唯一答案正式檢核。',form='short',accepted=['Hello.','Hi.'])

# Unit1
section('Unit 1','U1-A','職業與人物','先辨識人物，再用職業與身分詞造句。',['U101','U106'],'職業：teacher / nurse / cook / singer / writer / office worker / police officer / housewife；單數職業前使用 a / an。')
for zh,en in [('警察','police officer'),('歌手','singer'),('護士','nurse'),('家庭主婦','housewife'),('辦公室職員','office worker')]:
 item('U1-A','U101',f'把「{zh}」寫成英文。',en,'來自 Unit 1 的 Theme Words。')
item('U1-A','U106','Job card: Zac is a doctor. Q: What is Zac’s job? A: ______','He is a doctor.','依 job card 回答職業，he 指 Zac。',form='short')
item('U1-A','U106','職業卡：Zoe 是 writer。請用一句英文介紹 Zoe。','She is a writer.','she is + a + 職業。',form='short')

section('Unit 1','U1-B','家庭關係與 Who','先看家庭結構，再回答人物關係。',['U102','U103','U107'],'家庭圖：Paul 與 Carol 為父母；Zac 與 Zoe 是他們的兒女；Max 是 Zoe 的兒子。',display='family')
item('U1-B','U102','根據家庭圖：Who is Max’s mother?','Zoe.','Max 是 Zoe 的兒子，因此母親為 Zoe。',form='short')
item('U1-B','U102','根據家庭圖：Zac is Max’s ______.','uncle','Zac 與 Zoe 是兄妹／姊弟；Max 是 Zoe 的兒子，因此 Zac 是舅舅／叔叔。')
item('U1-B','U102','根據家庭圖：Paul is Carol’s ______.','husband','圖中 Paul 與 Carol 為夫妻。')
item('U1-B','U103','問人物：______ is that boy? He is Max.','Who','Who 問人；What 不適合問特定人物身分。')
item('U1-B','U103','A: Who is Zoe? B: ______','She is Max’s mother.','根據已給家庭圖，單數女性用 she。',form='short')
item('U1-B','U107','將「Paul 的兒子」譯成英文名詞片語。',"Paul's son",'單一人物的所有格為 Paul’s。',form='short')

section('Unit 1','U1-C','be 句型與形容詞','肯定、否定、疑問與簡答，要配合主詞。',['U104','U105','U108','U113'],'Yes/No：Is he...? Yes, he is. / No, he isn’t.；形容詞可在 be 後或名詞前。')
item('U1-C','U104','She is a nurse. → 改成否定句。',"She isn't a nurse.",'is not 可縮寫為 isn’t。',form='rewrite',accepted=["She isn't a nurse.","She is not a nurse."])
item('U1-C','U104','They are students. → 改成 Yes/No 問句。','Are they students?','be 提到主詞前。',form='rewrite')
item('U1-C','U104','A: Are you a teacher?  B: ______（否定簡答）',"No, I'm not.",'對 are you 由回答者用 I；否定可答 No, I’m not。',form='short')
item('U1-C','U104','A: Is the boy tall? B: ______（肯定簡答）','Yes, he is.','the boy 用 he；肯定簡答不用縮寫 yes he’s。',form='short')
item('U1-C','U105','將「a / handsome / boy」排成名詞片語。','a handsome boy','形容詞置名詞 boy 前。',form='rewrite')
item('U1-C','U105','將「The girl is happy.」改成「她是個快樂的女孩」。','She is a happy girl.','形容詞名詞前，單數 girl 前加 a。',form='rewrite')
item('U1-C','U108','Age card: Max, 7. 用完整英文句介紹年齡。','Max is seven years old.','數字後接 years old。',form='short')
item('U1-C','U113','要問人物身分，選 Who / How old：______ is that girl?','Who','Who 問身分；How old 問年齡。')

section('Unit 1','U1-D','閱讀、拼讀與構詞','讀短文找證據；構詞與聲音放在獨立的小區塊。',['U109','U110','U111','U112'],'閱讀先定位文字資訊；-er 為本單元 Extension，非全體學生必考。')
READ_U1='Ben is thirteen. His mother is a teacher. His father is a police officer. His sister, Zoe, is an elementary school student. Ben is a junior high school student.'
item('U1-D','U109','依閱讀短文：How old is Ben?','He is thirteen.','文中直接指出 Ben is thirteen。',form='short',context=READ_U1,accepted=['He is thirteen.','He is thirteen years old.'])
item('U1-D','U109','依閱讀短文：Who is a police officer?',"Ben's father.",'文中 His father is a police officer。',form='short',context=READ_U1)
item('U1-D','U109','依閱讀短文：Which school is Zoe in?','Elementary school.','文中 Zoe is an elementary school student。',form='short',context=READ_U1)
item('U1-D','U110','辨識字首聲音：哪個字以字母 b 開頭？ bed / red','bed','此處僅辨認字母／可見字形，不宣稱完成聽辨。',form='short')
item('U1-D','U110','辨識尾音字形：哪個字以字母 t 結尾？ pet / bed','pet','pet 以 t 結尾；屬文字檢核。',form='short')
item('U1-D','U111','延伸構詞（若已教）：teach + er → ______','teacher','-er 表示執行工作的人；本題屬課本 Extension，教師須確認。')
item('U1-D','U111','延伸構詞（若已教）：sing + er → ______','singer','sing 加 er 形成 singer。')
item('U1-D','U112','角色：Zoe 正介紹自己是學生。請寫完整一句。','I am a student.','由 Zoe 自己說話，要用 I；口說能力須另由教師觀察。',form='short')

# Unit2
section('Unit 2','U2-A','文具與名詞複數','先會辨識物品，再觀察一個變多個的詞形。',['U201','U202','U203','U204','U205','U206'],'單數用 a/an；複數常加 -s/-es；有些 y→ies、fe→ves，且 mouse→mice。')
for zh,en in [('鉛筆盒','pencil case'),('筆記本','notebook'),('禮物','gift'),('漫畫書','comic book')]:
 item('U2-A','U201',f'把「{zh}」寫成英文。',en,'屬 Unit 2 Theme Words。')
item('U2-A','U202','____ eraser （填 a / an）','an','eraser 的起始音為母音，使用 an。')
for sg,pl,kid in [('box','boxes','U203'),('watch','watches','U203'),('baby','babies','U204'),('wife','wives','U204'),('mouse','mice','U205'),('person','people','U205'),('pencil box','pencil boxes','U206'),('comic book','comic books','U206')]:
 item('U2-A',kid,f'請寫出 {sg} 的複數。',pl,f'{sg} 的課本對應複數為 {pl}。')

section('Unit 2','U2-B','This / That / These / Those','先看近或遠，再看一個或多個。',['U207','U208','U209'],'近單 this、近複 these；遠單 that、遠複 those。單數 is，複數 are。',display='distance')
for desc,ans,tail in [('近處 1 支 pencil','This','is a pencil.'),('遠處 1 把 ruler','That','is a ruler.'),('近處 2 支 pens','These','are pens.'),('遠處 3 本 notebooks','Those','are notebooks.')]:
 item('U2-B','U207',f'【{desc}】______ {tail}',ans,'按照說話者距離與數量選指示詞。')
item('U2-B','U208','對近處兩個 pencil cases 問「這些是什麼？」寫英文問句。','What are these?','近處複數用 What are these?。',form='short')
item('U2-B','U208','Q: What is that? A: ______（遠處 1 個 comic book）','That is a comic book.','單數 that 對 is，名詞前需 a。',form='short')
item('U2-B','U209','____ two watches on the table.（選 These are / This is）','These are','複數 two watches 對應 these are。',form='short')
item('U2-B','U209','A: Are those your markers? B: ______（肯定簡答）','Yes, they are.','those 為複數，簡答用 they are。',form='short')

section('Unit 2','U2-C','Where 與位置','讀位置圖，回答物品所在。',['U210','U211','U212','U217'],'Where is + 單數? / Where are + 複數?；位置詞看圖而不是猜。',display='location')
item('U2-C','U211','依位置圖：The clock is ______ the table.','above','圖中 clock 在 table 上方，並未接觸桌面。')
item('U2-C','U211','依位置圖：The cat is ______ the table.','under','圖中 cat 位於桌面下方。')
item('U2-C','U211','依位置圖：The notebook is ______ the table.','on','圖中 notebook 放在桌面上。')
item('U2-C','U211','依位置圖：The ruler is ______ the pencil and the eraser.','between','ruler 在 pencil 與 eraser 之間。')
item('U2-C','U211','文字情境：the sofa is behind the table。請寫出「在桌子的後面」。','behind the table','behind = 在……後方。')
item('U2-C','U211','文字情境：the table is in front of the sofa。請寫出「在沙發前面」。','in front of the sofa','in front of = 在……前方。')
item('U2-C','U210','根據圖：Where is the cat? A: ______','It is under the table.','單數 cat 用 It is；圖提供位置證據。',form='short')
item('U2-C','U210','情境：Two pencils are in the pencil case. Q: Where are the pencils? A: ______','They are in the pencil case.','複數 pencils 用 They are；位置在 pencil case。',form='short')
item('U2-C','U212','選出房間名稱：吃飯的房間是 bedroom / dining room？','dining room','dining room 是飯廳，bedroom 是臥室。',form='short')

item('U2-C','U211','用兩個英文單字說「緊鄰客廳」：______ the living room.','next to','next to 表緊鄰；此題限制兩個單字以免多解。')
item('U2-C','U211','用一個介系詞說「在我家附近」：______ my house.','near','near 是在……附近。')

section('Unit 2','U2-D','對話、顏色與閱讀','將文本證據和自己的判斷分開。',['U213','U215','U216'],'先找到原文中的人、物、位置，再回答，不只靠猜測。')
READ_U2='This is Ben\'s house. The living room walls are purple. Purple is Ben\'s favorite color. The kitchen is next to the dining room. His notebook is on the table. Two pencils are in a pencil case.'
item('U2-D','U213','依短文：What color are the living room walls?','Purple.','文中 The living room walls are purple。',context=READ_U2,form='short')
item('U2-D','U215','依短文：Which room is next to the dining room?','The kitchen.','文中 The kitchen is next to the dining room。',context=READ_U2,form='short')
item('U2-D','U210','依短文：Where is Ben’s notebook?','It is on the table.','文中 notebook is on the table。',context=READ_U2,form='short')
item('U2-D','U216','依短文：pencil case 裡有幾支 pencils？','Two.','文中 Two pencils are in a pencil case，答案為 2。',context=READ_U2,form='short',accepted=['Two.','Two pencils.'])
item('U2-D','U215','讀房屋提示：The bedroom is above the kitchen. 哪個房間在下面？','The kitchen.','above the kitchen 表 bedroom 在 kitchen 上方。',form='short')
item('U2-D','U213','A: My favorite color is gray. Q: What is the speaker’s favorite color?','Gray.','favorite color 是最喜歡的顏色。',form='short')

item('U2-D','U215','根據原課閱讀的空間用語：The bathroom is ______ the house.','inside','inside 表在房屋裡面。')
item('U2-D','U215','房屋雖小但足夠一人住：It is ______ for one person.','enough','enough 表足夠的，課文以房屋大小形成對比。')
item('U2-D','U215','把 right、next、to 排成正確的位置片語。','right next to','right next to 表就在……旁邊。',form='rewrite')

section('Unit 2','U2-E','複數讀音與詞形檢查','書面練習字尾讀音分類，補正容易混淆的複數。',['U203','U204','U205','U214'],'-s 字尾有 /s/、/z/、/ɪz/；書面分類不能取代聽力測驗。')
for word,ans,expl in [('notebooks','/s/','books 字尾 /s/'),('rooms','/z/','rooms 字尾 /z/'),('watches','/ɪz/','watches 字尾 /ɪz/')]:
 item('U2-E','U214',f'參照課本表，將 {word} 字尾讀音分類：/s/、/z/、/ɪz/。',ans,expl,form='short')
item('U2-E','U204','依複數規則：family → ______','families','子音+y 改 ies。')
item('U2-E','U205','依課本不規則複數：woman → ______','women','woman 複數為 women。')

# Integrated Review
section('Review','R-M','Starter–Unit 2 統整應用','混合舊知識，但不把新舊能力混成單一診斷。',['S08','S12','S13','U102','U104','U207','U209','U210','U211','U216'],'圈出問句線索：Who / What / How old / Where；再判斷單複數與語境。')
item('R-M','S08','Paul and I are students. ______ are students.','We','Paul + 說話者 I，用 we。')
item('R-M','U104','A: Is Zoe a teacher? B: ______（否定）',"No, she isn't.",'Zoe 用 she，is 否定簡答。',form='short')
item('R-M','S13','Name card: Jamie, age 13. Q: How old is Jamie?','Jamie is thirteen years old.','以年齡 13 回答。',form='short',accepted=['Jamie is thirteen years old.','He is thirteen years old.'])
item('R-M','U207','【遠處 2 本 notebooks】______ are notebooks.','Those','遠＋複數 those。')
item('R-M','U210','情境：The pencils are under the desk. 問：Where are the pencils?','They are under the desk.','複數 they / are；位置 under。',form='short')
item('R-M','U102','Zoe 是 Max 的媽媽。Max 是 Zoe 的 ______（用英文）。','son','家庭關係 son。')
item('R-M','U216','選正確：What are these? A: (They are pencils. / He is a pencil.)','They are pencils.','複數問句配 They are。',form='short')
item('R-M','U211','位置：cat 在 box 裡。Where is the cat?','It is in the box.','Where+is；in the box。',form='short')

item('U2-C','U217','口說練習：指出教室內一項已知物品，問一次 Where is it?，再口頭回答。','含 Where is it? 與一個合適位置答句','教師須現場觀察口說；不能由紙本答案推論口語能力。',form='oral',accepted=['依現場物品位置合理回答'])

# ----------------------------------------- Separate independent-check drafts -----------------------------------------
section('Starter','S-CHECK','Starter 新題檢核','教師先收走學習頁；每項能力分開記錄。',['S01','S08','S09','S10','S11','S12','S13','S14','S15','S16'],'這是獨立檢核的草稿，正式發行仍待來源及教師 Gate 核准。',display='checkpoint')
item('S-CHECK','S01','將小寫 m 改成大寫。','M','m→M。',stage='check')
item('S-CHECK','S09','We are students. ______ teacher is Mr. Lin.','Our','we 的所有格 our；此題 teacher 為課本詞彙。',stage='check')
item('S-CHECK','S09','He is Gary. ______ name is Gary.','His','he 的所有格 his。',stage='check')
item('S-CHECK','S11','They are students. → 寫成縮寫句。',"They're students.",'they are→they’re。',stage='check',form='rewrite')
item('S-CHECK','S12','Name card: Ben (boy). 寫出「他的名字是什麼？」','What is his name?','his name 用 What is 來詢問。',stage='check',form='short')
item('S-CHECK','S13','Age card: Tina, 12. Q: How old is Tina?','She is twelve years old.','用 she is twelve years old。',stage='check',form='short')
item('S-CHECK','S14','將 47 寫成英文。','forty-seven','forty 沒有 u；整十加連字號。',stage='check')
item('S-CHECK','S15','改正：her name is tina.','Her name is Tina.','句首 H、姓名 T 大寫。',stage='check',form='rewrite')
item('S-CHECK','S16','A: How are you? B: ______（我很好。）',"I'm fine.",'狀態問句需回答狀態，不是姓名／年齡。',stage='check',form='short')

section('Unit 1','U1-CHECK','Unit 1 新題檢核','人物與語法新題，不使用練習頁原題。',['U101','U102','U103','U104','U105','U106','U107','U108','U109','U113'],'正式 Gate 仍待教師確認。',display='checkpoint')
item('U1-CHECK','U101','「作家」的英文是什麼？','writer','Unit 1 詞彙 writer。',stage='check')
item('U1-CHECK','U102','根據家庭圖：Carol is Max’s ______.','grandmother','Carol 是 Zoe 的母親；Zoe 是 Max 的母親。',stage='check')
item('U1-CHECK','U103','想問「那個女生是誰？」請寫英文。','Who is that girl?','Who + is + that girl。',stage='check',form='short')
item('U1-CHECK','U104','A: Are they students? B: ______（否定簡答）',"No, they aren't.",'複數 they 搭配 are not。',stage='check',form='short',accepted=["No, they aren't.","No, they are not."])
item('U1-CHECK','U105','重排：is / nurse / a / young / She / .','She is a young nurse.','單數職業前 a；形容詞 young 修飾 nurse。',stage='check',form='rewrite')
item('U1-CHECK','U107','將「Zoe 的兒子」譯成英文。',"Zoe's son",'Zoe’s + son。',stage='check',form='short')
item('U1-CHECK','U108','Age card: Paul, 45. Q: How old is Paul?','He is forty-five years old.','男性 he；forty-five 為 45。',stage='check',form='short')
item('U1-CHECK','U113','A: ______ is that man? B: He is my uncle.','Who','回答人物關係，需用 Who。',stage='check')

section('Unit 2','U2-CHECK','Unit 2 新題檢核','詞形、指示詞、位置與閱讀。',['U201','U202','U203','U204','U205','U206','U207','U208','U209','U210','U211','U212','U213','U215'],'正式 Gate 仍待教師核准。',display='checkpoint')
item('U2-CHECK','U201','「橡皮擦」的英文是什麼？','eraser','Unit 2 文具詞彙。',stage='check')
item('U2-CHECK','U202','____ umbrella（填 a/an）','an','umbrella 起始母音 /ʌ/，故用 an。',stage='check')
item('U2-CHECK','U203','複數：brush → ______','brushes','以 sh 結尾常加 es。',stage='check')
item('U2-CHECK','U204','複數：housewife → ______','housewives','housewife 末尾 wife→wives。',stage='check')
item('U2-CHECK','U205','複數：mouse → ______','mice','不規則。',stage='check')
item('U2-CHECK','U206','複數：living room → ______','living rooms','複合名詞在核心名詞 room 後加 s。',stage='check')
item('U2-CHECK','U207','【近處 2 把 rulers】______ are rulers.','These','近＋複數 these。',stage='check')
item('U2-CHECK','U208','【遠處 2 支 pencils】問「那些是什麼？」','What are those?','遠＋複數 what are those。',stage='check',form='short')
item('U2-CHECK','U209','That ______ a brush.','is','單數 that 用 is。',stage='check')
item('U2-CHECK','U210','位置資料：Three books are in the box. Q: Where are the books?','They are in the box.','複數用 They are，位置 in the box。',stage='check',form='short')
item('U2-CHECK','U211','已知 table 在 sofa 的前面。The sofa is ______ the table.','behind','兩者前後相對：table 在 sofa 前，sofa 就在 table 後方。',stage='check')
item('U2-CHECK','U212','Name a room: 「廚房」的英文是什麼？','kitchen','kitchen 是廚房。',stage='check')
item('U2-CHECK','U213','A: What is your favorite color? B: ______（我最喜歡紫色。）','Purple.','可答 Purple.；若完整句需 My favorite color is purple。',stage='check',form='short',accepted=['Purple.','My favorite color is purple.'])
item('U2-CHECK','U215','The bedroom is above the dining room. 哪個房間在上方？','The bedroom.','above 連接的前方名詞在上。',stage='check',form='short')

section('Review','R-CHECK','跨單元新情境','混合知識時，教師須拆開記錄錯誤原因。',['S08','S09','S12','S14','U102','U103','U104','U207','U210','U216'],'學生先獨立作答，教師判讀哪些技能需要最小修復。',display='checkpoint')
item('R-CHECK','S09','She is my sister. ______ name is Zoe.','Her','she 的所有格 her。',stage='check')
item('R-CHECK','U103','A: ______ is that handsome boy? B: He is my cousin.','Who','詢問人物身份／關係。',stage='check')
item('R-CHECK','U104','A: Is Max a student? B: ______（肯定簡答）','Yes, he is.','he 單數用 is。',stage='check',form='short')
item('R-CHECK','U207','【遠處 1 個 pencil box】______ is a pencil box.','That','遠處單數 that。',stage='check')
item('R-CHECK','U210','Situation: The watches are on the table. Q: Where are the watches?','They are on the table.','複數 they are。',stage='check',form='short')
item('R-CHECK','S14','把 58 寫成英文。','fifty-eight','fifty + eight。',stage='check')
item('R-CHECK','U102','Paul is Zoe’s father. Max is Zoe’s son. Who is Max’s grandfather?','Paul.','母親 Zoe 的父親是 Paul。',stage='check',form='short')
item('R-CHECK','U216','【近處 2 本 comic books】A: What are these? B: ______','They are comic books.','用複數 they are。',stage='check',form='short')

# Delayed as separate teacher-held new items, previous G/I/T/D preserved from prior package separately
section('Starter','S-DELAY','Starter 延後無提示','請記錄兩次施測相隔天數。',['S08','S09','S10','S12','S13','S14'],'如果有提示，應標成 supported practice。',display='delayed')
for kp,p,a,rat in [
('S09','She is Jan. ______ name is Jan.','Her','she→her'),('S10','We ______ Gary and Ben.','are','we→are'),('S12','Name card: Mark (boy). Q: What is his name? A: ______','His name is Mark.','姓名問答'),('S13','Age card: Kelly, 19. Q: How old is Kelly?','She is nineteen years old.','年齡問答'),('S14','將 29 寫成英文。','twenty-nine','數字字形')]:
 item('S-DELAY',kp,p,a,rat,stage='delayed',form='short')
section('Unit 1','U1-DELAY','Unit 1 延後無提示','未曝光新題，與上次練習分開。',['U101','U102','U103','U104','U105','U108'],'教師應分別記錄是否有提示。',display='delayed')
for kp,p,a,r in [
('U101','「廚師」的英文是？','cook','職業詞義提取'),('U102','Zoe is Max’s mother. Max is Zoe’s ______.','son','家屬關係'),('U103','A: ______ is she? B: She is my aunt.','Who','問身份'),('U104','They are happy. → 改為否定句。',"They aren't happy.",'be 的否定'),('U108','Age card: Max, 18. A: How old is he?','He is eighteen years old.','年齡')]:
 item('U1-DELAY',kp,p,a,r,stage='delayed',form='short')
section('Unit 2','U2-DELAY','Unit 2 延後無提示','未曝光新題，與上次練習分開。',['U203','U204','U205','U207','U210','U211'],'不能用當堂再做來冒充延後保留。',display='delayed')
for kp,p,a,r in [
('U203','複數：box → ______','boxes','詞尾 es'),('U204','複數：baby → ______','babies','y→ies'),('U205','複數：woman → ______','women','不規則'),('U207','【近處 1 個 gift】______ is a gift.','This','近處單數'),('U210','Q: Where are the brushes? 資料：They are under the desk.','They are under the desk.','位置答案'),('U211','【新情境：notebook 在桌面上】The notebook is ______ the table.','on','中文情境給關係，需用 on 獨立寫出位置')]:
 item('U2-DELAY',kp,p,a,r,stage='delayed',form='short')

# Integrate the exact 16 PR#8 source items, preserving original item content and answer from repository-exported ZIP
from zipfile import ZipFile
legacyzip=Path('/mnt/data/Starter_Source_Lock_Pilot_v0.1_Source.zip')
if legacyzip.exists():
  with ZipFile(legacyzip) as z:legacy=json.loads(z.read('curriculum/starter/subject-be.items.json'))
else:
  legacyfile=BASE/'legacy_subject_be.items.json'
  if legacyfile.exists(): legacy=json.loads(legacyfile.read_text(encoding='utf8'))
  else: raise FileNotFoundError('PR8 subject-be item map unavailable: legacy 16-item preservation cannot be verified')
if True:
  for orig in legacy['items']:
    stage={'guided':'practice','independent':'check','transfer':'check','delayed':'delayed'}[orig['stage']]
    sec={'guided':'S-B','independent':'S-CHECK','transfer':'S-CHECK','delayed':'S-DELAY'}[orig['stage']]
    # Use native historic ID prefix, preserved verbatim in legacy_original
    ITEMS.append(dict(id='LEG-'+orig['id'],section=sec,unit='Starter',kp='S10' if orig['target']=='pronoun-be' else 'S08',prompt=orig['prompt'],answer=' / '.join(orig['answers']) if len(orig['answers'])>1 else orig['answers'][0],rationale=orig['rationale'],source_refs=['SG'],stage=stage,form='write' if len(orig['answers'])==1 else 'short',options=[],accepted=[' / '.join(orig['answers'])],context=orig.get('context_zh',''),hint='',diagnosis=orig.get('diagnosis',''),legacy_original=orig,legacy_preserved=True))

# Teacher guidance metadata
UNIT_INTRO={
'Starter':'英文字母與短母音、主格／所有格、be、姓名年齡、數字及英文書寫。',
'Unit 1':'人物、職業、家庭關係、Who 問句、be 肯否定與簡答、形容詞、閱讀、字音與構詞。',
'Unit 2':'文具／房間／顏色、名詞單複數、this/that/these/those、Where 與位置、閱讀、複數尾音。',
'Review':'Starter＋Unit 1＋Unit 2 的跨單元運用；錯誤須分開診斷。'
}
AUDIOS=[dict(unit='Starter',source='SP',aspect='短母音字音的實際聽辨與讀音',state='AUDIO_PENDING',action='取得官方 CD 音訊後另出聽力，不以文字選擇替代'),dict(unit='Unit 1',source='U1S',aspect='Sounds and Letters 實際聽辨',state='AUDIO_PENDING',action='需官方音檔／教師現場發音逐題紀錄'),dict(unit='Unit 2',source='U2S',aspect='字尾 /s/ /z/ /ɪz/ 實際聽辨',state='AUDIO_PENDING',action='需官方錄音與獨立聽辨題'),dict(unit='Unit 1/2',source='U1D',aspect='課本對話的聽力題',state='AUDIO_PENDING',action='未附正式音檔，不提供虛構聽力逐字答案')]

WORD_BANKS={
 'Unit 1':[
 ('handsome','英俊的'),('new','新的'),('classmate','同學'),('young','年輕的'),('woman','女人（複數 women）'),('very','非常'),('beautiful','美麗的'),('too','也'),('Nice to meet you.','很高興認識你'),('cousin','堂／表兄弟姊妹'),('really','真的'),('year(s) old','……歲'),('I see.','我知道了'),('singer','歌手'),('office worker','上班族'),('housewife','家庭主婦'),('police officer','警察'),('writer','作家'),('uncle','叔伯舅等男性長輩'),('aunt','姑姨等女性長輩'),('wife','妻子'),('daughter','女兒'),('husband','丈夫'),('son','兒子'),('dear','親愛的'),('family','家庭／家人'),('elementary school','國小'),('junior high school','國中'),('baby','嬰兒；年幼的')
 ],
 'Unit 2':[
 ('house','房子'),('parents','父母親'),('living room','客廳'),('wall','牆壁'),('purple','紫色的'),('favorite','最喜愛的'),('color','顏色'),('kitchen','廚房'),('dining room','飯廳'),('but','但是'),('gray','灰色的'),('brown','棕色的'),('cookie','餅乾'),('mice','老鼠（mouse 複數）'),('maybe','可能'),('sofa','沙發'),('hungry','餓的'),('notebook','筆記本'),('marker','彩色筆／麥克筆'),('brush','刷子／畫筆'),('gift','禮物'),('pencil case','鉛筆盒'),('bathroom','浴室'),('table','桌子'),('bedroom','臥室'),('near','在附近'),('between','在……之間'),('behind','在後面'),('in front of','在前面'),('special','特別的'),('inside','在……裡面'),('right','就；恰好'),('each other','彼此／互相'),('above','在……上方'),('enough','足夠的'),('person','人（複數 people）')
 ]
}
SOURCE_VOCAB_EXTRAS={
 'Starter phonics': ['yam','ham','van','man','wet','jet','red','bed','kilt','quilt','pig','zigzag','cot','dot','fox','box','sun','run','bug','mug'],
 'Unit 1 theme words': ['teacher','nurse','cook','student','grandfather','grandmother','mother','father','brother','sister','police officer','office worker','housewife','singer','writer'],
 'Unit 2 theme words': ['pen','pencil','eraser','ruler','clock','notebook','marker','brush','gift','cookie','comic book','pencil case','bathroom','dining room','kitchen','living room','bedroom','in','on','under','next to','near','between','behind','in front of']
}
PACKAGE=dict(schema='lesley-lesson-through-u2-v0.1',status='DRAFT_FOR_TEACHER_REVIEW',policy='LESLEY_TEACHING_ENGINE_v2.4_STABLE.md',scope=['Starter','Unit 1','Unit 2','Review'],source_status='READY_WITH_LIMITS',not_verified=['學校指定現行課本確切版次/ISBN','老師核准全單元實際進度','當次正式段考通知與特定學生獨立掌握','官方音檔與聽力答案'],source_restrictions=['完整課本掃描與學生筆跡不提交 GitHub','部分原題已批改，不作獨立證據','所有新題都是教師／AI 製作草稿，未取得正式核准','獨立練習題公開後不得視為未曝光正式考卷'],sources=SOURCES,knowledge_points=list(KP.values()),sections=SECTIONS,items=ITEMS,audio_gaps=AUDIOS,unit_intro=UNIT_INTRO,word_banks=WORD_BANKS,source_vocabulary=SOURCE_VOCAB_EXTRAS)

def validate(pkg=PACKAGE):
    error=[];warnings=[]
    ids=[x['id'] for x in pkg['items']]
    if len(ids)!=len(set(ids)):error.append('重複題號')
    for it in pkg['items']:
        if it['kp'] not in KP:error.append(f'{it["id"]} 無對應知識點')
        if not it['answer'] or not it['rationale']:error.append(f'{it["id"]} 無答案或解析')
        if not set(it['source_refs']).issubset(SOURCES):error.append(f'{it["id"]} 無效來源')
        if it['stage'] in ['check','delayed'] and it['hint']:error.append(f'{it["id"]} 檢核出現提示')
        if it.get('legacy_preserved'):
            x=it['legacy_original'];assert x['prompt']==it['prompt'];assert ' / '.join(x['answers'])==it['answer'] or x['answers'][0]==it['answer']
    for k_id in KP:
        if not any(i['kp']==k_id for i in pkg['items']):
            warnings.append(f'{k_id} 僅列知識點，題庫未直接覆蓋')
    # Explicit known exceptional domains: audio and oral need external observation
    # Check copies of identical questions (excluding stages) for leakage risk
    seen={}
    for x in pkg['items']:
        stem=re.sub(r'\s+',' ',x['prompt'].lower().strip())
        if stem in seen and seen[stem]!=x['stage']:
            warnings.append(f'{x["id"]} 題幹與 {seen[stem]} 跨階段相似，施測前注意答案曝光')
        seen[stem]=x['stage']
    return error,warnings

if __name__=='__main__':
 errors,warnings=validate();assert not errors,errors
 (BASE/'unit_scope_item_bank.json').write_text(json.dumps(PACKAGE,ensure_ascii=False,indent=2),encoding='utf8')
 (BASE/'qa_structure.json').write_text(json.dumps(dict(errors=errors,warnings=warnings,count_items=len(ITEMS),count_kp=len(KP),by_unit={u:sum(x['unit']==u for x in ITEMS) for u in UNIT_INTRO},by_stage={s:sum(x['stage']==s for x in ITEMS) for s in ['practice','check','delayed']},audio_gaps=len(AUDIOS)),ensure_ascii=False,indent=2),encoding='utf8')
 print('Saved',len(KP),'knowledge points',len(ITEMS),'items',len(warnings),'warnings')