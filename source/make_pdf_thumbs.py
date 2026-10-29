import re, sys
from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/3610edf1-6436-57cb-a96d-4cc028baa10f/scratchpad/'
thumbs=[int(x) for x in sys.argv[1:]]
s=open('/home/claude/site/index.html').read()
head=s.split('<style>')[0]
secs=re.search(r'<main id="stage"[^>]*>(.*)</main>',s,re.S).group(1)
secs=re.sub(r'<video data-src="[^"]*" poster="([^"]*)"[^>]*style="([^"]*)"></video>',r'<img src="\1" alt="" style="\2">',secs)
css='''<style>*{margin:0;padding:0;box-sizing:border-box}@page{size:1920px 1080px;margin:0}
html,body{background:#fff;font-family:'Plus Jakarta Sans',Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
a{color:inherit;text-decoration:none}ul{padding-left:1.2em}
section{position:relative;width:1920px;height:1080px;overflow:hidden;display:block;break-after:page}section:last-child{break-after:auto}</style></head><body>'''
open('/home/claude/site/print.html','w').write(head+css+secs+'</body></html>')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':1080}); pg.emulate_media(reduced_motion='reduce')
    for k in thumbs:
        pg.goto(f'http://localhost:8765/?t={k}#{k}'); pg.wait_for_timeout(2500)
        pg.add_style_tag(content='#ui,#bar,#snd{display:none!important}#stage{box-shadow:none!important}')
        pg.screenshot(path=S+'t.png'); Image.open(S+'t.png').convert('RGB').resize((960,540),Image.LANCZOS).save(f'/home/claude/site/thumbs/{k}.jpg',quality=82,optimize=True)
    q=b.new_page(viewport={'width':1920,'height':1080})
    q.goto('http://localhost:8765/print.html',wait_until='networkidle'); q.wait_for_timeout(2500)
    q.pdf(path='/home/claude/Mental-Help-Presentation.pdf',width='1920px',height='1080px',print_background=True,margin={'top':'0','right':'0','bottom':'0','left':'0'})
    b.close()
import os; os.remove('/home/claude/site/print.html'); print('done')
