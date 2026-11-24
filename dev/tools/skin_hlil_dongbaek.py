import json,base64,io,random
from PIL import Image,ImageDraw,ImageFont
random.seed(21)
SPR=json.loads(open('/home/claude/brawlpokemons/dev/assets/icons.js').read()[len('const SPR='):].rstrip().rstrip(';'))
im=Image.open(io.BytesIO(base64.b64decode(SPR['hlil'].split(',')[1]))).convert('RGBA')
h=lambda s:tuple(int(s[i:i+2],16) for i in (1,3,5))
B={'#f7bbf9':'#facc15','#d582c6':'#eab308','#f6e629':'#f97316','#baa847':'#9a3412','#c5f68b':'#ece6d6','#89bf47':'#cfc6b0','#94bc4a':'#cfc6b0','#96c65b':'#ddd5c2','#4a9c39':'#16181c','#6a9120':'#0b0c0e','#f8f8f8':'#fbf8f0','#cdd6de':'#bdb5a2'}
sm0=im.resize((26,36),Image.NEAREST)
def line(a,b):
    (x0,y0),(x1,y1)=a,b;pts=[];dx=abs(x1-x0);dy=-abs(y1-y0);sx=1 if x0<x1 else -1;sy=1 if y0<y1 else -1;e=dx+dy
    while True:
        pts.append((x0,y0))
        if (x0,y0)==(x1,y1):break
        e2=2*e
        if e2>=dy:e+=dy;x0+=sx
        if e2<=dx:e+=dx;y0+=sy
    return pts
Y1,Y2,Y3,OR=(254,240,138,255),(250,204,21,255),(245,158,11,255),(234,88,12,255)
def flower(q,W,H,cx,cy):
    for dx,dy,c in [(0,-1,Y1),(-1,0,Y2),(1,0,Y2),(0,1,Y3),(0,0,OR),(-1,-1,Y1 if random.random()<.5 else None),(1,1,Y3 if random.random()<.5 else None)]:
        x,y=cx+dx,cy+dy
        if c and 0<=x<W and 0<=y<H:q[x,y]=c
def make(k=1.0):
    M={h(a):h(b) for a,b in B.items()};o=sm0.copy();p=o.load();s0=sm0.load()
    for y in range(o.height):
        for x in range(o.width):
            r,g,b,a=p[x,y]
            if a and (r,g,b) in M:p[x,y]=M[(r,g,b)]+(a,)
    W,H=26+20,36+8;OX,OY=10,8
    back=Image.new('RGBA',(W,H),(0,0,0,0));q=back.load();K=(14,14,16,255)
    O=(23,22)  # 등 한가운데
    ends=[(7,3),(39,2),(2,17),(44,15),(5,29),(42,30)]
    forks=[]
    for e in ends:
        e=(round(O[0]+(e[0]-O[0])*k),round(O[1]+(e[1]-O[1])*k))
        pts=line(O,e)
        for (x,y) in pts:q[x,y]=K
        # 작은 곁가지
        m=pts[len(pts)*2//3];f=(m[0]+(2 if e[0]>O[0] else -2),m[1]-2)
        for (x,y) in line(m,f):
            if 0<=x<W and 0<=y<H:q[x,y]=K
        forks+=[e,f]+pts[len(pts)//2::2]
    for (x,y) in forks:flower(q,W,H,x+random.choice([-1,0,1]),y+random.choice([-1,0]))
    front=Image.new('RGBA',(W,H),(0,0,0,0));front.paste(o,(OX,OY),o)
    out=Image.alpha_composite(back,front)
    # 몸 앞에도 꽃 몇 송이 (어깨·머리)
    q2=out.load()
    for (x,y) in [(14,12),(31,13),(13,24),(33,25)]:flower(q2,W,H,x,y)
    return out
o0=Image.new('RGBA',(46,44),(0,0,0,0));o0.paste(sm0,(10,8),sm0)
outs=[('원본',o0),('B 등에서 뻗는 가지',make(.6)),('B 가지 조금 더 길게',make(.8))]
Wd=Image.new('RGBA',(3*250,30+44*5+10),(250,250,250,255));d=ImageDraw.Draw(Wd);d.fontmode='1';f=ImageFont.truetype('/home/claude/brawlpokemons/dev/assets/gfont.ttf',18)
for i,(n,o) in enumerate(outs):
    o2=o.resize((o.width*5,o.height*5),Image.NEAREST);Wd.paste(o2,(i*250+(250-o2.width)//2,30),o2);tw=d.textlength(n,font=f);d.text((i*250+(250-tw)/2,4),n,font=f,fill=(30,30,30))
Wd.save('/tmp/skd/dongbaek6.png')
outs[1][1].save('/tmp/skd/hlil_B3.png');outs[2][1].save('/tmp/skd/hlil_B4.png')
