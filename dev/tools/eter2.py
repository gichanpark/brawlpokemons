exec(open('eter.py').read().split("A={")[0])
import math
def noise(x,y,s=7):
    return (math.sin(x/s*1.7+y/s*0.6)+math.sin(y/s*1.3-x/s*0.9+1.7)+math.sin((x+y)/s*0.8+3.1))/3
def neb(base,glowA,glowB,sc):
    def f(x,y,w,h):
        v=noise(x*40/w,y*40/h,sc)
        if v>.45:return glowA
        if v<-.5:return glowB
        return base
    return f
A={'O':'#04020c','K':['#0b0720','#120b30'],'G':['#2a2068','#43359a','#6d5bd0'],
   'B':neb(['#140c38','#22165a','#36268a','#5a46c2'],['#3b1a6e','#7e3fd1','#c084fc','#f0abfc'],['#0c2a5a','#1d5fa8','#38bdf8','#bae6fd'],6),
   'R':['#22d3ee','#67e8f9','#cffafe','#ffffff'],'W':['#e0f2fe','#ffffff'],'star':0,'stars':[]}
AU={'O':'#03110f','K':['#062420','#0a302b'],'G':['#0f4a44','#16685f','#2a8f83'],
   'B':neb(['#0b3b3a','#105a55','#178077','#25a596'],['#4c1d95','#7c3aed','#c4b5fd','#ede9fe'],['#065f46','#10b981','#6ee7b7','#d1fae5'],5),
   'R':['#f59e0b','#fcd34d','#fef3c7','#ffffff'],'W':['#ecfeff','#ffffff']}
PT={'O':'#2b2440','K':['#cfc8e6','#e6e1f5'],'G':['#8b84a8','#b3abd0','#d9d3ee'],
   'B':['#a8a1c9','#c6c0e3','#e4e0f5','#ffffff'],'R':['#d97706','#f59e0b','#fcd34d','#fffbeb'],'W':['#ffffff','#ffffff']}
def stars(img,bgset,seed,cols,dens):
    random.seed(seed);w,h=img.size;px=img.load();o=img.copy()
    for y in range(1,h-1):
        for x in range(1,w-1):
            p=px[x,y]
            if p[3]<128 or (bgset and '#%02x%02x%02x'%p[:3] in bgset):continue
            c,L=cls(p)
            if L<90 and random.random()<dens:o.putpixel((x,y),H(random.choice(cols)))
    return o
res=[]
for nm,P,st in [('은하수',A,['#ffffff','#fde68a','#a5f3fc','#f5d0fe']),('오로라',AU,['#ffffff','#a7f3d0']),('백금',PT,None)]:
    s=recolor(n,P);p=recolor(por,P,BG,seed=2)
    if st:s=stars(s,None,3,st,.08);p=stars(p,BG,4,st,.06)
    s.save(f'et_{nm}_n.png');p.save(f'et_{nm}_p.png');res.append((nm,s,p))
f=ImageFont.truetype('/home/claude/brawlpokemons/dev/assets/gfont.ttf',22)
cv=Image.new('RGBA',(1280,640),(30,34,44,255));d=ImageDraw.Draw(cv)
for i,(nm,s,p) in enumerate([('원본',n,por)]+res):
    x0=i*320;d.text((x0+160,24),nm,font=f,fill=(255,255,255),anchor='mm')
    S=s.resize((s.width*5,s.height*5),Image.NEAREST);cv.paste(S,(x0+160-S.width//2,60),S)
    P2=p.resize((240,240),Image.NEAREST);cv.paste(P2,(x0+40,330))
cv.save('eter_draft.png')
