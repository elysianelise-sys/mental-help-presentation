import sys, os
from playwright.sync_api import sync_playwright
page=sys.argv[1]; dur=float(sys.argv[2]); out=sys.argv[3]; ts=[float(x) for x in sys.argv[4:]]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':1080})
    pg.goto(f'file:///home/claude/vid2/{page}'); pg.wait_for_timeout(1500)
    if ts:
        for t in ts: pg.evaluate(f'render({t})'); pg.screenshot(path=f'{out}_{t}.jpg',type='jpeg',quality=80)
    else:
        os.makedirs(out,exist_ok=True)
        for i in range(int(dur*30)): pg.evaluate(f'render({i/30})'); pg.screenshot(path=f'{out}/f{i:04d}.jpg',type='jpeg',quality=92)
    b.close()
