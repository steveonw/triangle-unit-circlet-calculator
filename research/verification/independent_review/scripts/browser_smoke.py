"""Independent browser smoke test (Playwright + Chromium/Chrome).
Usage: python browser_smoke.py <app.html> [--out DIR] [--expect-pretty]
Set CHROMIUM_PATH to use an existing browser executable.
Checks: no page errors; 2- and 6-crossing camera presets; crossing identity text;
near-pole example; empty-input prompt color versus a real error; display of
general-denominator answers; no horizontal overflow at 390 px.
--expect-pretty additionally requires general answers to use ·, − and spaced operators (V4.3.1+).
"""
import json, os, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

html = Path(sys.argv[1]).resolve()
out = Path(sys.argv[sys.argv.index('--out') + 1]) if '--out' in sys.argv else None
expect_pretty = '--expect-pretty' in sys.argv
GENERAL = ['1/(2*sin-1)', 'sin/(1+cos)', '-sin/(1+cos)^2', '(sin^2-cos^2+2)/(sin-cos)']
res, fails = {'app': html.name}, []
with sync_playwright() as p:
    kw = {'executable_path': os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}
    b = p.chromium.launch(args=['--no-sandbox'], **kw)
    pg = b.new_page(viewport={'width': 1400, 'height': 1000})
    errors = []
    pg.on('pageerror', lambda e: errors.append(str(e)))
    pg.goto(html.as_uri()); pg.wait_for_timeout(400)
    color = lambda: pg.evaluate("()=>{const e=document.getElementById('eyeError');return {text:e.textContent,color:getComputedStyle(e).color}}")
    muted = pg.evaluate("()=>{const d=document.createElement('span');d.style.color='var(--muted)';document.body.append(d);const c=getComputedStyle(d).color;d.remove();return c}")
    res['empty_prompt'] = color(); res['muted_color'] = muted
    if res['empty_prompt']['color'] != muted: fails.append('empty prompt is not the muted color')
    pg.fill('#eyeExpr', 'sin +'); pg.wait_for_timeout(100)
    res['error_state'] = color()
    if res['error_state']['color'] == muted: fails.append('real error is shown in the muted color')
    for btn, want in [('#viewTwo', 2), ('#viewSix', 6)]:
        pg.click(btn); pg.wait_for_timeout(150)
        n = int(pg.inner_text('#crossCount').split()[0]); res[btn] = n
        if n != want: fails.append(f'{btn}: {n} crossings, expected {want}')
    pg.click('#viewExample'); pg.wait_for_timeout(150)
    res['example_crossing'] = pg.inner_text('#crossRelation')
    if not res['example_crossing'].endswith('= cos'): fails.append('example crossing does not reduce to cos')
    pg.fill('#eyeExpr', '(1-sin)^4 / cos^8'); pg.wait_for_timeout(150)
    res['stability'] = {'answer': pg.inner_text('#eyeAnswer'), 'note': pg.inner_text('#singularityNote')}
    if '90°: hole; limit 0.0625' not in res['stability']['note'] or '270°: pole (order 8)' not in res['stability']['note']: fails.append('stability example singularities')
    res['general_answers'] = {}
    for e in GENERAL:
        pg.fill('#eyeExpr', e); pg.wait_for_timeout(150)
        ans, err = pg.inner_text('#eyeAnswer'), pg.inner_text('#eyeError')
        res['general_answers'][e] = {'answer': ans, 'error': err}
        if expect_pretty and not err and ('*' in ans or '-' in ans or '^' in ans): fails.append(f'unformatted answer for {e}: {ans}')
    res['page_errors'] = errors
    if errors: fails.append('page errors')
    if out:
        out.mkdir(parents=True, exist_ok=True)
        pg.fill('#eyeExpr', '1/(2*sin-1)'); pg.wait_for_timeout(150)
        pg.screenshot(path=str(out / 'browser_desktop.png'))
    m = b.new_page(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
    m.on('pageerror', lambda e: errors.append('mobile: ' + str(e)))
    m.goto(html.as_uri()); m.wait_for_timeout(300); m.fill('#eyeExpr', '(sin^2-cos^2+2)/(sin-cos)'); m.wait_for_timeout(150)
    res['mobile_scroll_width'] = m.evaluate('document.documentElement.scrollWidth')
    if res['mobile_scroll_width'] > 390: fails.append('horizontal overflow at 390 px')
    if out: m.screenshot(path=str(out / 'browser_mobile.png'), full_page=True)
    b.close()
res['failures'] = fails
print(json.dumps(res, indent=1, ensure_ascii=False))
if out: (out / 'browser_smoke.json').write_text(json.dumps(res, indent=1, ensure_ascii=False) + '\n')
sys.exit(1 if fails else 0)
