from PIL import Image,ImageDraw,ImageFont
import colorsys,random
H=lambda s:tuple(int(s[i:i+2],16) for i in (1,3,5))+(255,)
def cls(p):
    r,g,b=[v/255 for v in p[:3]];h,l,s=colorsys.rgb_to_hls(r,g,b);L=l*255
    if L<22:return 'K',L
    if s<.18 and L<200:return 'G',L
    hd=h*360
    if s>=.3 and (hd<25 or hd>330):return 'R',L
    if 200<=hd<=290:return 'B',L
    if L>200:return 'W',L
    return 'G',L
def recolor(im,P,bgset=None,fx=None,seed=1):
    random.seed(seed);im=im.convert('RGBA');w,h=im.size;out=im.copy();px=im.load()
    for y in range(h):
        for x in range(w):
            p=px[x,y]
            if p[3]<128:continue
            if bgset and '#%02x%02x%02x'%p[:3] in bgset:continue
            c,L=cls(p)
            edge=any(not(0<=x+dx<w and 0<=y+dy<h) or px[x+dx,y+dy][3]<128 for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))
            if c=='K' and (edge or bgset):
                out.putpixel((x,y),H(P['O']));continue
            pal=P[c] if not callable(P[c]) else P[c](x,y,w,h)
            rng={'K':(0,22),'G':(22,200),'B':(30,200),'R':(60,255),'W':(200,256)}[c]
            t=(L-rng[0])/(rng[1]-rng[0]);t=max(0,min(.999,t))
            col=pal[int(t*len(pal))]
            if c=='K' and P.get('star') and random.random()<P['star']:col=random.choice(P['stars'])
            out.putpixel((x,y),H(col))
    return out
spr=Image.open('SPR_890.png').convert('RGBA');w,h=spr.size;n=spr.resize((w//3,h//3),Image.NEAREST)
por=Image.open('POR_890.png').convert('RGBA');BG={'#eff7b7','#7fc7df','#bfdfb7'}
def grad(cols):
    def f(x,y,w,h):
        i=int((x/w*0.6+y/h*0.4)*len(cols));i=min(len(cols)-1,i);return cols[i]
    return f
A={'O':'#05030f','K':['#120a2e','#1b1145'],'G':['#2a1e5c','#3b2c7a','#5a46a8'],
   'B':grad([['#1e40af','#3b82f6','#7dd3fc'],['#6d28d9','#a855f7','#e9d5ff'],['#be185d','#ec4899','#fbcfe8']]),
   'R':['#22d3ee','#a5f3fc','#ffffff'],'W':['#e0f2fe','#ffffff'],'star':.06,'stars':['#ffffff','#fde68a','#a5f3fc','#f9a8d4']}
B={'O':'#3b2f4a','K':['#e9e4f5','#f8f6ff'],'G':['#b45309','#f59e0b','#fde68a'],
   'B':grad([['#f472b6','#f9a8d4'],['#fbbf24','#fde68a'],['#34d399','#a7f3d0'],['#60a5fa','#bfdbfe'],['#a78bfa','#ddd6fe']]),
   'R':['#f59e0b','#fde047','#fffbeb'],'W':['#ffffff','#ffffff']}
C={'O':'#2a0f1f','K':['#3b1230','#4c1a3d'],'G':['#7a2e55','#a3477a','#d07aa6'],
   'B':['#f472b6','#f9a8d4','#fce7f3'],'R':['#bef264','#ecfccb','#ffffff'],'W':['#fff1f5','#ffffff'],'star':.05,'stars':['#fbcfe8','#ffffff','#f9a8d4']}
res=[]
for nm,P in [('은하수',A),('프리즘',B),('벚꽃',C)]:
    s=recolor(n,P);p=recolor(por,P,BG,seed=2);s.save(f'et_{nm}_n.png');p.save(f'et_{nm}_p.png');res.append((nm,s,p))
f=ImageFont.truetype('/home/claude/brawlpokemons/dev/assets/gfont.ttf',22)
cv=Image.new('RGBA',(1280,640),(30,34,44,255));d=ImageDraw.Draw(cv)
items=[('원본',n,por)]+res
for i,(nm,s,p) in enumerate(items):
    x0=i*320;d.text((x0+160,24),nm,font=f,fill=(255,255,255),anchor='mm')
    S=s.resize((s.width*5,s.height*5),Image.NEAREST);cv.paste(S,(x0+160-S.width//2,60),S)
    P2=p.resize((240,240),Image.NEAREST);cv.paste(P2,(x0+40,330))
cv.save('eter_draft.png')
