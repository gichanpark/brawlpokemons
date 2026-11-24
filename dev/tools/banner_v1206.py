from PIL import Image,ImageDraw,ImageFont
import random,json,base64,io
random.seed(1206)
R='/home/claude/brawlpokemons/'
raw=open(R+'dev/assets/skins.js').read();X=json.loads(raw[len('const SKINX='):raw.index(';const SOCCER=')])
dec=lambda u:Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGBA')
W,H=1200,380;S=3;w,h=W//S,H//S
bg=Image.new('RGBA',(w,h));d=ImageDraw.Draw(bg)
for y in range(h):
    t=y/h;d.line([(0,y),(w,y)],fill=(int(22+30*t),int(18+8*t),int(48-10*t),255))
st=Image.new('RGBA',(w,h));sd=ImageDraw.Draw(st)
for x in range(-h,w,13):sd.line([(x,h),(x+h,0)],fill=(255,255,255,14),width=3)
bg=Image.alpha_composite(bg,st);d=ImageDraw.Draw(bg)
for _ in range(50):
    x,y=random.randrange(w),random.randrange(h);d.point((x,y),fill=random.choice([(253,224,71,255),(255,255,255,255),(249,168,212,255),(125,211,252,255)]))
def outl(im,col,r=1):
    a=im.split()[3].point(lambda v:255 if v>100 else 0);o=Image.new('RGBA',(im.width+2*r,im.height+2*r))
    for dx in range(2*r+1):
        for dy in range(2*r+1):
            if (dx-r)**2+(dy-r)**2<=r*r:o.paste(col,(dx,dy,dx+a.width,dy+a.height),a)
    o.paste(im,(r,r),im);return o
def small(u):im=dec(u);return im.resize((im.width//3,im.height//3),Image.NEAREST)
a=outl(small(X['cinderace_spurs']['spr']).resize((42,82),Image.NEAREST),(253,224,71,255))
b=outl(small(X['cinderace_korea']['spr']).resize((42,82),Image.NEAREST),(253,224,71,255))
gi=small(X['giratina_yako']['f1']);gi=outl(gi.transpose(Image.FLIP_LEFT_RIGHT).resize((gi.width*2,gi.height*2),Image.NEAREST),(220,38,38,255))
bg.alpha_composite(a,(16,h-a.height-4));bg.alpha_composite(b,(16+a.width+4,h-b.height-4));bg.alpha_composite(gi,(w-gi.width-6,h-gi.height-2))
big=bg.resize((W,H),Image.NEAREST);d=ImageDraw.Draw(big);d.fontmode='1'
fp=R+'dev/assets/gfont.ttf'
def ct(txt,y,sz,fill,o=4):
    f=ImageFont.truetype(fp,sz);tw=d.textlength(txt,font=f);x=(W-tw)/2
    for dx in range(-o,o+1,2):
        for dy in range(-o,o+1,2):d.text((x+dx,y+dy),txt,font=f,fill=(15,8,20))
    d.text((x,y),txt,font=f,fill=fill)
ct('v1.20.6',70,30,(253,224,71),3)
ct('스킨 업데이트',112,66,(255,255,255),4)
ct('토트넘 · 국가대표 에이스번  /  백귀야행 기라티나',204,26,(254,215,170),3)
ct('+ 모든 포켓몬 이로치',244,26,(186,230,253),3)
big.convert('RGB').save(R+'notice/v1206.png')
