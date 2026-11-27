from PIL import Image,ImageDraw,ImageFont
import re,base64,io,random
random.seed(1228)
R='/home/claude/brawlpokemons/'
ic=open(R+'dev/assets/icons.js').read()
def get(k):
    m=re.search(r'"%s":\s*"data:image/png;base64,([^"]+)"'%re.escape(str(k)),ic);return Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGBA')
W,H=1200,380;S=4;w,h=W//S,H//S
bg=Image.new('RGBA',(w,h));d=ImageDraw.Draw(bg)
for y in range(h):t=y/h;d.line([(0,y),(w,y)],fill=(int(30+20*t),int(18+10*t),int(48+20*t),255))
st=Image.new('RGBA',(w,h));sd=ImageDraw.Draw(st)
for x in range(-h,w,9):sd.line([(x,h),(x+h,0)],fill=(255,255,255,14),width=2)
bg=Image.alpha_composite(bg,st)
big=bg.resize((W,H),Image.NEAREST)
ids=[202,196,197,319,598,771,774,785,964,987,791]
for i,k in enumerate(ids):
    try:im=get(k)
    except Exception:continue
    sc=110/max(im.width,im.height);im=im.resize((int(im.width*sc),int(im.height*sc)),Image.NEAREST)
    x=620+(i%4)*140-(i//4)*40+random.randint(-10,10);y=20+(i//4)*115
    big.alpha_composite(im,(x,y))
d=ImageDraw.Draw(big);d.fontmode='1';fp=R+'dev/assets/gfont.ttf'
def ct(txt,y,sz,fill,o=4,x0=50):
    f=ImageFont.truetype(fp,sz)
    for dx in range(-o,o+1,2):
        for dy in range(-o,o+1,2):d.text((x0+dx,y+dy),txt,font=f,fill=(10,8,20))
    d.text((x0,y),txt,font=f,fill=fill)
ct('v1.21.28  ·  공격 개편',60,30,(226,232,240),3)
ct('새로운 공격 방식!',104,64,(255,255,255),4)
ct('돌진 공격 · 주변 범위 공격 · 관통',200,26,(252,211,77),3)
ct('되돌아오는 탄 · 튕기는 번개 · 파편',240,26,(147,197,253),3)
big.convert('RGB').save(R+'notice/v1228.png')
