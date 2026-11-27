"""Exercise V4.3's general-domain UI in Chromium; run with HTML path argument."""
from pathlib import Path
import sys, os, math
from playwright.sync_api import sync_playwright
source=Path(sys.argv[1]).resolve();out=Path('browser_screenshots');out.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH'),headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1440,'height':1050});page.set_default_timeout(5000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(source.read_text());page.wait_for_timeout(120)
 inp=page.locator('#eyeExpr');ans=page.locator('#eyeAnswer');note=page.locator('#singularityNote');value=page.locator('#eyeValue')
 inp.fill('1/(sin^2+cos^2)');assert ans.inner_text()=='1';assert page.locator('#eyeDomain').inner_text()=='All real θ'
 inp.fill('sin/(1+cos)');assert '180°: pole (order 1)' in note.inner_text();assert note.inner_text()=='180°: pole (order 1)';page.locator('[data-stop-angle="0"]').click();assert float(value.inner_text())==0
 inp.fill('1/(sin+cos)^2');assert '135°: pole (order 2)' in note.inner_text() and '315°: pole (order 2)' in note.inner_text();page.locator('[data-stop-angle="135"]').click();assert 'Undefined at 135° — pole'==value.inner_text();page.screenshot(path=str(out/'v43_poles.png'),full_page=True)
 inp.fill('(sin+cos)/(sin+cos)');assert ans.inner_text()=='1';assert '135°: hole; limit 1' in note.inner_text();assert 'removable hole' in value.inner_text();assert page.locator('#eyeGraph circle[stroke="#ffb478"]').count()==2;page.locator('#exactForm summary').click();assert '0° chart: 1' in page.locator('#canonicalAnswer').inner_text();page.screenshot(path=str(out/'v43_holes.png'),full_page=True)
 inp.fill('(3*sin-1)/(3*sin-1)');assert ans.inner_text()=='1';roots=page.evaluate('eye.result.roots.map(r=>r.angle)');assert len(roots)==2;assert abs(roots[0]-math.degrees(math.asin(1/3)))<1e-10
 btn=page.locator('#domainStops button.blocked').first;assert btn.inner_text().startswith('≈');btn.click();assert 'removable hole' in value.inner_text();assert page.evaluate('state.angle===eye.result.roots[0].angle')
 # Adjacent, non-root angle must remain defined (no broad epsilon snapping).
 page.locator('#angleExact').fill(str(roots[0]+1e-7));page.locator('#angleExact').press('Enter');assert float(value.inner_text())==1
 inp.fill('1/(sin^2+cos^2-1)');assert 'identically zero' in page.locator('#eyeError').inner_text()
 inp.fill('1/(2+sin)');assert page.locator('#eyeDomain').inner_text()=='All real θ';assert not note.inner_text()
 inp.fill('1/(3*sin-1)');assert page.locator('#domainStops button.blocked').count()==2;page.locator('#domainStops button.blocked').first.click();assert 'pole' in value.inner_text();page.screenshot(path=str(out/'v43_noncardinal.png'),full_page=True)
 page.locator('button[data-workspace="calculus"]').click();page.locator('#angleExact').fill('37');page.locator('#angleExact').press('Enter');assert page.locator('#recovered').inner_text()=='37.00°';assert page.locator('#sideSum').inner_text()=='4.000'
 assert not errors,errors
 m=b.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,device_scale_factor=1);m.set_content(source.read_text());m.locator('#eyeExpr').fill('(sin+cos)/(sin+cos)');m.locator('[data-stop-angle="135"]').click();assert m.evaluate('document.documentElement.scrollWidth <= innerWidth');m.screenshot(path=str(out/'v43_mobile.png'),full_page=True)
 print('V4.3 desktop: unity divisor, half-angle domain, oblique repeated poles, cancellation holes, exact-form disclosure, irrational root jump, nearby angle, zero-denominator rejection, root-free divisor and calculus PASS; page errors:',errors)
 print('V4.3 mobile 390px: general expression and excluded-angle controls PASS; no horizontal overflow')
 b.close()
