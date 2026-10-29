import numpy as np, cv2, sys
from PIL import Image, ImageDraw
M=np.load('/home/claude/qr/M.npy'); n=len(M)
def render(dot=0.09, round_dots=True, eye_r=(2.2,1.5,1.1), logo=0.13, S=40, Q=4, colors=True, orb=True):
    W=(n+2*Q)*S; SS=3
    img=Image.new('RGBA',(W*SS,W*SS),(255,255,255,0)); d=ImageDraw.Draw(img)
    def grad(y):
        a=np.array([0x8F,0x48,0x5B]); b=np.array([0x5E,0x24,0x3A]); t=y/(n-1)
        return tuple(int(v) for v in a+(b-a)*t)+(255,) if colors else (0,0,0,255)
    fnd=lambda r,c:(r<7 and c<7) or (r<7 and c>=n-7) or (r>=n-7 and c<7)
    cx=n/2; lr=n*logo
    for r in range(n):
        for c in range(n):
            if not M[r,c] or fnd(r,c): continue
            if logo and (r+.5-cx)**2+(c+.5-cx)**2 < (lr+0.6)**2: continue
            x=(Q+c)*S*SS; y=(Q+r)*S*SS; p=int(S*SS*dot)
            (d.ellipse if round_dots else d.rectangle)([x+p,y+p,x+S*SS-p,y+S*SS-p],fill=grad(r))
    m=S*SS
    for r0,c0 in [(0,0),(0,n-7),(n-7,0)]:
        x=(Q+c0)*m; y=(Q+r0)*m; col=grad(r0+3)
        d.rounded_rectangle([x,y,x+7*m,y+7*m],radius=int(eye_r[0]*m),fill=col)
        d.rounded_rectangle([x+m,y+m,x+6*m,y+6*m],radius=int(eye_r[1]*m),fill=(255,255,255,255))
        d.rounded_rectangle([x+2*m,y+2*m,x+5*m,y+5*m],radius=int(eye_r[2]*m),fill=(0xC9,0x50,0x7E,255) if colors else (0,0,0,255))
    img=img.resize((W,W),Image.LANCZOS)
    if logo and orb:
        o=Image.open('/home/claude/assets/orb-calm.png').convert('RGBA'); ow=int(2*lr*S*0.95); o=o.resize((ow,ow),Image.LANCZOS)
        ring=Image.new('RGBA',(W,W),(0,0,0,0)); rd=ImageDraw.Draw(ring); c0=W/2; rr=ow/2+S*0.3
        rd.ellipse([c0-rr,c0-rr,c0+rr,c0+rr],fill=(255,255,255,255)); img.alpha_composite(ring); img.alpha_composite(o,(int(c0-ow/2),int(c0-ow/2)))
    return img
def scan(img, bg=(255,255,255), sizes=(600,260,180)):
    t=Image.new('RGB',img.size,bg); t.paste(img,(0,0),img); out=[]
    for s in sizes:
        a=np.array(t.resize((s,s),Image.LANCZOS))[:,:,::-1]
        out.append(cv2.QRCodeDetector().detectAndDecode(a)[0]!='')
    return out
def scan2(img, bg=(255,255,255), sizes=(600,320,240,180,140)):
    t=Image.new('RGB',img.size,bg); t.paste(img,(0,0),img); out=[]
    for s in sizes:
        g=cv2.cvtColor(np.array(t.resize((s,s),Image.LANCZOS))[:,:,::-1],cv2.COLOR_BGR2GRAY)
        _,b=cv2.threshold(g,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        ok=False
        for im in (g,b):
            for scale in (1,2):
                x=cv2.resize(im,None,fx=scale,fy=scale,interpolation=cv2.INTER_NEAREST) if scale>1 else im
                if cv2.QRCodeDetector().detectAndDecode(x)[0]=='https://mental-help-alpha.vercel.app': ok=True
        out.append(ok)
    return out
