import re,os,json,shutil
from PIL import Image
S='/tmp/claude-0/-home-claude/3610edf1-6436-57cb-a96d-4cc028baa10f/scratchpad/final/project/'
OUT='/home/claude/site/'
M=json.load(open('/home/claude/redesign/map.json'))
W='/home/claude/wst/st-'
M.update({'9c9ecc658f5d70c78ee2e880f2751833':W+'bolt.png','e77ac89156076a2a2ea713d4efc09828':W+'books.png','d2fab8a0633083541a03e27594b387d5':W+'calendar.png',
'd17b0875bc4a05675c1433195fe6f51d':W+'chart.png','1a59b9e832512be70e7cf88133c70993':W+'chat.png','c1099fe1166f58364b2a4f342528c1c8':W+'clock.png',
'70e2b62fdbd08fa6e21f4dec6ff8d9c8':W+'code.png','64d4506a7e351eb40e1cbe3f5ac04516':W+'coffee.png','fc1b4568b26b839fa071bc5083975ca4':W+'headphones.png',
'4a45fe9ad3e4b49920e20f1598968ef5':W+'heart.png','c23d660e4c1b4078ebbbacf4e7427415':W+'laptop.png','b43cc26382aa4855bdc417e9d9cd2a8f':W+'lock.png',
'4aab8dd57a7cdb7415301d144ae483de':W+'moon.png','8606b2fc95bbb25c388ac730b4832fe1':W+'sparkle.png','acda6c2ba29fbff2c739df285cc4f9cb':W+'users.png',
'b651e50ec366eb9335407f4eb05b9300':W+'wave.png',
'51eee5e9fe8f4604dd8eb88a88743320':'/home/claude/assets/fs-home.jpg','6ed26374072b666f3d5569986fe06b8f':'/home/claude/assets/fs-calm.jpg',
'507aa724ae8b71475e1561c39aefd585':'/home/claude/assets/fs-explore.jpg','0594bf130e8bcc809eb7ab3c49d4f7b6':'/home/claude/assets/fs-sessions.jpg',
'39121d73ce57745a736f47ac03a7a8b4':'/home/claude/assets/fig-checkin-front.png',
'a6270c5b6c288b9a7aeca49a815064fb':'/home/claude/vlog/panel1.jpg','e2b07970a29d83b006de2709085b1bab':'/home/claude/vlog2/panelA.jpg',
'a53bf61fe9337ebc29aa4772bd34e898':'/home/claude/vlog3/panelD.jpg','ced786dab66b1ae31e5709c24b5f3539':'/home/claude/vlog2/panelC.jpg',
'd00785faf0aa982eb7d82f1f80680687':'/home/claude/vid2/still-qr2.jpg','5085ea190092dfd9a469e0413f1846cb':'/home/claude/vid2/mental-help-ending-qr2.mp4'})
ICON={ # simple stroke icons, 24 viewBox
'Check':'<path d="M5 12.5l4.5 4.5L19 7.5"/>',
'Clock':'<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
'Lock':'<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/>',
'Play':'<path d="M8 5.5v13l10.5-6.5z" fill="currentColor"/>',
'Users':'<circle cx="9" cy="8.5" r="3.5"/><path d="M2.5 19.5c.8-3.4 3.4-5.5 6.5-5.5s5.7 2.1 6.5 5.5"/><path d="M16 5.2a3.4 3.4 0 0 1 0 6.6M18 14.4c1.8.8 3 2.6 3.5 5.1"/>',
'Warning':'<path d="M12 3.5L2.5 20h19z"/><path d="M12 10v4.5"/><circle cx="12" cy="17.3" r=".6" fill="currentColor"/>'}
def icon(m):
    name,style=m.group(1),m.group(2)
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="{style};flex:none">{ICON[name]}</svg>'
used={}
def asset(i):
    if i in used: return used[i]
    src=M[i]; ext=os.path.splitext(src)[1].lower()
    dst=f'assets/{i[:10]}{"-qr2" if (ext==".mp4" or i.startswith("d00785")) else ""}{ext}'
    if ext=='.png' and os.path.getsize(src)>900_000:
        im=Image.open(src)
        if im.mode in('RGB',) : dst=dst[:-4]+'.jpg'; im.save(OUT+dst,quality=90)
        else: shutil.copy(src,OUT+dst)
    elif ext=='.jpg' and os.path.getsize(src)>700_000:
        Image.open(src).convert('RGB').save(OUT+dst,quality=88)
    else: shutil.copy(src,OUT+dst)
    used[i]=dst; return dst

COVER_LINKS=[('Progressive assessment','https://docs.google.com/presentation/d/1q6ZNFLUIUtkx79pPJolDO1bx1efU1P__xwaQKM0NXd8/edit?usp=sharing','#F29BB0'),
 ('Figma','https://www.figma.com/design/AUItTBis7M5o89P9dCcskv','#C9A9E6'),
 ('Dribbble','https://dribbble.com/shots/27716037-Mental-Health-Mobile-App','#A99FE0')]
def cover_links():
    chips=''.join(f'<a target="_blank" rel="noopener" href="{u}" style="display:flex;align-items:center;gap:9px;padding:9px 18px 9px 13px;border-radius:999px;background:linear-gradient(180deg,#FFFFFF 0%,#FDF0F5 100%);border:2px solid #FFFFFF;border-bottom:4px solid #EBC3D3;font-size:20px;font-weight:700;color:#2B1D25;white-space:nowrap"><span style="width:12px;height:12px;border-radius:50%;background:{c};flex:none"></span>{t}<span style="color:#9B5C78;font-weight:700">↗</span></a>' for t,u,c in COVER_LINKS)
    return ('<div style="position:absolute;left:176px;top:893px;width:1080px;display:flex;flex-direction:column;gap:10px">'
            '<p style="font-size:16px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:#9B5C78">Project links</p>'
            f'<div style="display:flex;flex-wrap:wrap;gap:10px">{chips}</div></div>')

def qr_card():
    return ('<div style="position:absolute;left:1584px;top:612px;width:296px;display:flex;flex-direction:column;align-items:center;gap:10px;padding:20px 20px 18px;'
            'background:rgba(255,250,252,0.94);border:2px solid #FFFFFF;border-radius:32px;box-shadow:0 24px 50px rgba(113,48,67,0.28)">'
            '<a target="_blank" rel="noopener" href="https://mental-help-alpha.vercel.app" style="display:block;width:252px;height:252px">'
            '<img src="assets/qr-app.png" alt="QR code for mental-help-alpha.vercel.app" style="display:block;width:252px;height:252px"></a>'
            '<p style="font-family:\'Bricolage Grotesque\', Arial, sans-serif;font-size:26px;font-weight:700;line-height:1.1;color:#2B1D25">Scan to try it</p>'
            '<p style="margin-top:-4px;font-size:16px;font-weight:600;color:#9B5C78">mental-help-alpha.vercel.app</p></div>')
deck=json.load(open(S+'deck.json'))
secs=[]
for sid in deck['order']:
    h=open(S+f'slides/{sid}.html').read()
    h=re.sub(r'<aside>.*?</aside>','',h,flags=re.S)
    h=re.sub(r'<x-icon name="(\w+)" style="([^"]*)"></x-icon>',icon,h)
    h=re.sub(r'<img src="/_blob/(\w+)" data-video="/_blob/(\w+)" alt="([^"]*)" style="([^"]*)">',
             lambda m:f'<video data-src="{asset(m.group(2))}" poster="{asset(m.group(1))}" muted playsinline preload="none" aria-label="{m.group(3)}" style="{m.group(4)}"></video>',h)
    h=re.sub(r'/_blob/([0-9a-f]{32})',lambda m:asset(m.group(1)),h)
    h=re.sub(r'<a href=','<a target="_blank" rel="noopener" href=',h)
    assert '/_blob/' not in h and 'x-icon' not in h, sid
    if sid=='cover': h=h.replace('</section>', cover_links()+'\n</section>')
    secs.append(h.strip())
title=deck['title']
allh='\n'.join(secs)
seen=[];
for href,txt in re.findall(r'<a target="_blank" rel="noopener" href="([^"]+)">([^<]+)',allh):
    if href not in [x[0] for x in seen]: seen.append((href,txt.replace('→','').strip()))
names={'mental-help-alpha.vercel.app':'Live app'}
links=''.join(f'<a href="{h}" target="_blank" rel="noopener">{names.get(t,t)} →</a>' for h,t in seen)
html=open('/home/claude/site_tpl.html').read().replace('%%TITLE%%',title).replace('%%SLIDES%%',allh).replace('%%LINKS%%',links)
open(OUT+'index.html','w').write(html)
print(len(secs),'slides', len(used),'assets')
