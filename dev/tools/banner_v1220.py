# v1.22.0 시즌 1 보상 크로마틱 배너 (1200x380, 도트) — 금·은·동 받침대 위 세 마리
from PIL import Image,ImageDraw,ImageFont
import random,json,base64,io
random.seed(1220)
R='/home/claude/brawlpokemons/'
W,H=1200,380;S=3;w,h=W//S,H//S
bg=Image.new('RGBA',(w,h));d=ImageDraw.Draw(bg)
for y in range(h):
    t=y/h;d.line([(0,y),(w,y)],fill=(int(30+20*t),int(16+10*t),int(44+24*t),255))
for _ in range(80):
    x,y=random.randrange(w),random.randrange(h);d.point((x,y),fill=random.choice([(253,224,71,255),(255,255,255,255),(244,114,182,255)]))
def outl(im,col,r=1):
    a=im.split()[3].point(lambda v:255 if v>100 else 0);o=Image.new('RGBA',(im.width+2*r,im.height+2*r))
    for dx in range(2*r+1):
        for dy in range(2*r+1):
            if (dx-r)**2+(dy-r)**2<=r*r:o.paste(col,(dx,dy,dx+a.width,dy+a.height),a)
    o.paste(im,(r,r),im);return o
t=open(R+'dev/assets/icons.js').read();spr=json.loads(t[t.index('{'):t.rindex('}')+1])
def base(k,f):
    im=Image.open(io.BytesIO(base64.b64decode(spr[k].split(',')[1]))).convert('RGBA');return im.resize((im.width//f,im.height//f),Image.NEAREST)
# 받침대: 2등 왼쪽 · 1등 가운데(높게) · 3등 오른쪽
for (cx,top,col,dk,k,f,sc,nm) in [(70,92,(203,213,225),(100,116,139),'scorvi',3,2,'2'),(200,78,(250,204,21),(161,98,7),'gtinkaton',4,2,'1'),(330,100,(217,138,78),(120,64,24),'bferro',4,2,'3')]:
    d.rectangle([cx-30,top,cx+30,h],fill=dk);d.rectangle([cx-30,top,cx+30,top+4],fill=col);d.rectangle([cx-30,top,cx+30,h],outline=(17,17,17))
    m=base(k,f);m=outl(m.resize((m.width*sc,m.height*sc),Image.NEAREST),col+(255,),1)
    bg.alpha_composite(m,(cx-m.width//2,top-m.height+4))
big=bg.resize((W,H),Image.NEAREST);d=ImageDraw.Draw(big);d.fontmode='1'
fp=R+'dev/assets/gfont.ttf'
def ct(txt,x,y,sz,fill,o=3):
    f=ImageFont.truetype(fp,sz);tw=d.textlength(txt,font=f);x=x-tw/2
    for dx in range(-o,o+1,2):
        for dy in range(-o,o+1,2):d.text((x+dx,y+dy),txt,font=f,fill=(12,8,20))
    d.text((x,y),txt,font=f,fill=fill)
ct('v1.22.0  ·  시즌 1 보상',600,22,28,(251,207,232))
ct('한정 크로마틱 공개!',600,60,56,(255,255,255),4)
for (x,y,t,c) in [(210,300,'2등 은빛 갑주 아머까오',(226,232,240)),(600,262,'1등 황금 망치 두드리짱',(253,224,71)),(990,318,'3등 황동 가시 너트령',(240,180,120))]:ct(t,x,y,24,c)
big.convert('RGB').save(R+'notice/v1220.png')
