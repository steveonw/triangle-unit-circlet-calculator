from pathlib import Path
import sys, os
from playwright.sync_api import sync_playwright
pfile=Path(sys.argv[1] if len(sys.argv)>1 else 'Trig_Atlas_v4_1_Reliability.html').resolve()
output=Path('browser_screenshots');output.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH'),headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1440,'height':1000}); page.set_default_timeout(4000);errors=[]; page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(pfile.read_text()); page.wait_for_timeout(200)
 assert not errors,errors
 assert page.locator('#eyeExpr').input_value()==''
 assert not page.locator('#challengePanel').is_visible()
 page.screenshot(path=str(output/'v41_default.png'),full_page=True)
 page.click('#viewExample');assert page.locator('#eyeAnswer').inner_text()=='cos'
 page.click('#viewAxis'); assert 'no longer visible' in page.locator('#crossVisible').inner_text()
 page.locator('[data-stop-angle="0"]').click(); assert 'removable hole' in page.locator('#eyeValue').inner_text()
 page.locator('#eyeExpr').fill('(1-sin)^4 / cos^8'); page.locator('#angleExact').fill('89.99');page.locator('#angleExact').press('Enter');assert abs(float(page.locator('#eyeValue').inner_text())-.0625000019038589)<1e-9
 assert '90°: hole; limit 0.0625' in page.locator('#singularityNote').inner_text();assert '270°: pole (order 8)' in page.locator('#singularityNote').inner_text()
 page.screenshot(path=str(output/'v41_stability.png'),full_page=True)
 page.click('#practiceToggle');assert page.locator('#eyeExpr').input_value()=='';assert page.locator('#viewExample').is_disabled();assert not page.locator('#exprExamples').is_visible()
 page.click('#taskCheck');assert 'Not yet' in page.locator('#taskFeedback').inner_text()
 for f in ['sin','sec','cot']:page.locator(f'#eyeKeys [data-key="{f}"]').click()
 page.click('#taskCheck');assert 'Correct' in page.locator('#taskFeedback').inner_text()
 page.click('#taskNext');assert page.locator('#eyeExpr').input_value()==''
 cid=page.evaluate('eye.marks.find(m=>TA.compile(m.v.join("*")).text==="cos")?.id'); assert cid
 page.locator(f'#crossList [data-cross="{cid}"]').click();page.click('#taskCheck');assert 'Correct' in page.locator('#taskFeedback').inner_text()
 page.click('#taskNext');assert page.locator('#angleExact').input_value()=='45';page.click('#taskCheck');assert 'Not yet' in page.locator('#taskFeedback').inner_text();page.locator('[data-stop-angle="0"]').click();page.click('#taskCheck');assert 'Correct' in page.locator('#taskFeedback').inner_text()
 page.click('#taskNext');assert page.locator('#eyeExpr').input_value()=='';page.locator('#eyeExpr').fill('sin^2+cos^2');page.click('#taskCheck');assert 'Correct' in page.locator('#taskFeedback').inner_text()
 page.click('#taskNext');assert page.locator('#eyeExpr').input_value()=='';page.locator('#eyeExpr').fill('sec^2-tan^2');page.click('#taskCheck');assert '5 of 5 complete' in page.locator('#taskScore').inner_text();page.screenshot(path=str(output/'v41_practice.png'),full_page=True)
 page.click('#practiceToggle');assert page.locator('#eyeExpr').input_value()==''
 page.locator('button[data-workspace="reference"]').click();assert page.locator('#graphs').is_visible();page.locator('#tabs [data-tab="edge"]').click();page.locator('#chips [data-type="edge"][data-id="0"]').click();assert '½ sin 2θ' in page.locator('#inspector').inner_text()
 page.locator('button[data-workspace="calculus"]').click();assert page.locator('#calclab').is_visible();page.locator('#angleExact').fill('37');page.locator('#angleExact').press('Enter');assert page.locator('#recovered').inner_text()=='37.00°';assert page.locator('#sideSum').inner_text()=='4.000';page.screenshot(path=str(output/'v41_calculus.png'),full_page=True)
 page.locator('button[data-workspace="eye"]').click();assert not page.locator('#graphs').is_visible();assert page.locator('#eyeExpr').input_value()==''
 print('Browser desktop: crossing, exact angle, hole/pole, 5 practice tasks, reference, calculus PASS; errors',errors)
 assert not errors,errors
 mob=b.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,device_scale_factor=1);mob.set_content(pfile.read_text());mob.wait_for_timeout(200);assert mob.evaluate('document.documentElement.scrollWidth <= innerWidth');mob.screenshot(path=str(output/'v41_mobile.png'),full_page=True)
 print('Mobile 390px: no horizontal overflow');b.close()
