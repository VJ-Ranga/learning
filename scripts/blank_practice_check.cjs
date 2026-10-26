const {chromium}=require(process.env.PLAYWRIGHT_PACKAGE || '/home/vjranga/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs');const base=process.env.QUEST_BASE_URL || 'http://127.0.0.1:8001';
(async()=>{const browser=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const page=await browser.newPage({viewport:{width:1440,height:1100}});const errors=[];page.on('pageerror',e=>errors.push(e.message));const values=Object.fromEntries(fs.readFileSync('.env.learners','utf8').trim().split('\n').map(l=>l.split('=')));await page.goto(base+'/login/');await page.locator('#id_username').fill('vjranga');await page.locator('#id_password').fill(values.VJRANGA_PASSWORD);await Promise.all([page.waitForURL(base+'/'),page.getByRole('button',{name:'Continue the quest'}).click()]);await page.goto(base+'/missions/hello/');

 const mission=JSON.parse(await page.locator('#mission-data').textContent());
 if(await page.locator('#code').inputValue()!=='')throw Error('Practice preloads code');
 await page.locator('#load-example').click();
 if(await page.locator('#code').inputValue()!==mission.example)throw Error('Explicit example loading failed');
 await page.locator('#code').fill('print("my saved practice")');await page.locator('#code').dispatchEvent('input');await page.reload();
 if(await page.locator('#code').inputValue()!=='print("my saved practice")')throw Error('Saved practice draft lost');
 page.on('dialog',d=>d.accept());await page.locator('#reset-code').click();
 if(await page.locator('#code').inputValue()!=='')throw Error('Practice reset preloads example');
 await page.reload();if(await page.locator('#code').inputValue()!=='')throw Error('Blank practice draft lost');
 if(errors.length)throw Error(errors.join('\n'));await browser.close();console.log('Blank practice, opt-in example, saved draft restoration and clear reset verified. No marks submitted.');
})().catch(e=>{console.error(e.message);process.exit(1)});
