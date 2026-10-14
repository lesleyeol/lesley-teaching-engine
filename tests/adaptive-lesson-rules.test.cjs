// Run with: node tests/adaptive-lesson-rules.test.cjs
// No npm packages, API keys, test accounts or student data required.
'use strict';
const assert = require('node:assert/strict');
const path = require('node:path');
const {topics,activities,recommend} = require(path.join(__dirname,'../demos/adaptive-lesson-rules.js'));
const base = {topic:'starter-be',target:topics['starter-be'].target,source:'翰林 Starter Unit（教師來源紀錄）',readiness:'partial',route:'core',goal:'apply',minutes:30,load:'standard'};
let count=0;
function test(name, fn){try{fn(); count++; process.stdout.write('PASS '+name+'\n');}catch(e){process.stderr.write('FAIL '+name+'\n');throw e;}}
function rec(changes){return recommend({...base,...changes});}
test('source missing blocks activities and formal targets',()=>{const x=rec({readiness:'missing'});assert.equal(x.blocked,true);assert.equal(x.activities.length,0);assert.equal(x.status,'BLOCKED');});
test('blank source blocks',()=>{const x=rec({source:'  '});assert(x.blocked);assert(x.gaps.some(z=>z.includes('來源')));});
test('blank goal text blocks',()=>assert.equal(rec({target:''}).blocked,true));
test('no block creates 2 activities in Starter core',()=>assert.deepEqual(rec({}).activities.map(a=>a.id),['compare-subject','sentence-apply']));
test('Starter does not force noun detective',()=>assert(!rec({}).activities.some(a=>a.id.includes('noun'))));
test('Unit 1 family uses relation map',()=>{const x=rec({topic:'unit1-family',target:topics['unit1-family'].target});assert(x.activities.some(a=>a.id==='relation-map'));assert(!x.activities.some(a=>a.id==='location-map'));});
test('Unit 2 location uses spatial task',()=>{const x=rec({topic:'unit2-location',target:topics['unit2-location'].target});assert.equal(x.activities[0].id,'location-map');});
test('Reading uses evidence locator and not spelling task',()=>{const x=rec({topic:'reading',target:topics.reading.target});assert(x.activities.some(a=>a.id==='evidence-locator'));assert(!x.activities.some(a=>a.id==='active-spelling'));});
test('Spelling uses sound and form tasks',()=>{const x=rec({topic:'spelling',target:topics.spelling.target});assert.deepEqual(x.activities.map(a=>a.id),['sound-chunks','active-spelling']);});
test('Repair narrows to confirmed issue and initial scaffold',()=>{const x=rec({route:'repair'});assert.equal(x.activities[0].id,'error-contrast');});
test('Extension does not add more rote practice',()=>{const x=rec({route:'extension'});assert(!x.activities.some(a=>a.id==='compare-subject'));assert(x.activities.some(a=>a.id==='context-explain'));});
test('15 minute route allows just one activity',()=>assert.equal(rec({minutes:15}).activities.length,1));
test('Transfer goal offers context when time allows',()=>{const x=rec({minutes:45,goal:'transfer'});assert(x.activities.some(a=>a.id==='context-explain'));});
test('Support removal and new-item evidence always visible',()=>{for(const topic of Object.keys(topics).filter(x=>x!=='custom')){const x=rec({topic,target:topics[topic].target});assert(x.evidence.some(z=>z.includes('未曝光的新題')));assert(x.evidence.some(z=>z.includes('延後')));assert(x.limitations.includes('Release QA'));}});
test('partial source remains blueprint only',()=>{const x=rec({});assert.equal(x.status,'READY WITH LIMITS');assert(x.limitations.includes('設計草案'));});
test('teacher confirmed is not independently verified',()=>{const x=rec({readiness:'confirmed'});assert.equal(x.status,'TEACHER-DECLARED SOURCE');assert(x.limitations.includes('未驗證'));});
test('custom requires nonempty explicit target',()=>assert(rec({topic:'custom',target:''}).blocked));
test('all recommended IDs are known activities and unique',()=>{for(const topic of Object.keys(topics)){const x=rec({topic,target:topics[topic].target||'已核准的自訂目標'});if(x.blocked)continue;const ids=x.activities.map(y=>y.id);assert.equal(ids.length,new Set(ids).size);ids.forEach(id=>assert(activities[id]));}});
console.log(`${count} tests passed.`);