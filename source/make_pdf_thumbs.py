"""Renders thumbs/N.jpg (phone list view) and exports/Mental-Help-Presentation.pdf from index.html.

Run from anywhere:   python3 source/make_pdf_thumbs.py            (all slides + PDF)
                     python3 source/make_pdf_thumbs.py 3 19 25    (only those thumbs, then the PDF)
Needs: pip install playwright pillow  and  playwright install chromium
"""
import functools, http.server, os, re, sys, tempfile, threading
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
s = open(os.path.join(ROOT, 'index.html')).read()
total = len(re.findall(r'<section id="', s))
thumbs = [int(x) for x in sys.argv[1:]] or list(range(1, total + 1))

# print version of the deck: every slide as one 1920x1080 page
head = s.split('<style>')[0]
secs = re.search(r'<main id="stage"[^>]*>(.*)</main>', s, re.S).group(1)
secs = re.sub(r'<video data-src="[^"]*" poster="([^"]*)"[^>]*style="([^"]*)"></video>', r'<img src="\1" alt="" style="\2">', secs)
css = '''<style>*{margin:0;padding:0;box-sizing:border-box}@page{size:1920px 1080px;margin:0}
html,body{background:#fff;font-family:'Plus Jakarta Sans',Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
a{color:inherit;text-decoration:none}ul{padding-left:1.2em}
section{position:relative;width:1920px;height:1080px;overflow:hidden;display:block;break-after:page}section:last-child{break-after:auto}</style></head><body>'''
print_path = os.path.join(ROOT, 'print.html')
open(print_path, 'w').write(head + css + secs + '</body></html>')

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
handler.log_message = lambda *a, **k: None
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
port = httpd.server_address[1]
threading.Thread(target=httpd.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{port}'
tmp = os.path.join(tempfile.gettempdir(), 'mh-thumb.png')
os.makedirs(os.path.join(ROOT, 'thumbs'), exist_ok=True)
os.makedirs(os.path.join(ROOT, 'exports'), exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    pg.emulate_media(reduced_motion='reduce')
    for k in thumbs:
        pg.goto(f'{base}/?t={k}#{k}')
        pg.wait_for_timeout(2500)
        pg.add_style_tag(content='#ui,#bar,#snd{display:none!important}#stage{box-shadow:none!important}')
        pg.screenshot(path=tmp)
        Image.open(tmp).convert('RGB').resize((960, 540), Image.LANCZOS).save(os.path.join(ROOT, 'thumbs', f'{k}.jpg'), quality=82, optimize=True)
    q = b.new_page(viewport={'width': 1920, 'height': 1080})
    q.goto(f'{base}/print.html', wait_until='networkidle')
    q.wait_for_timeout(2500)
    q.pdf(path=os.path.join(ROOT, 'exports', 'Mental-Help-Presentation.pdf'), width='1920px', height='1080px',
          print_background=True, margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
    b.close()
httpd.shutdown()
os.remove(print_path)
print('done:', len(thumbs), 'thumbs + PDF')
