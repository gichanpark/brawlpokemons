# v1.21.35 초희귀 챌린지 배너 (1200x380, 도트)
from PIL import Image,ImageDraw,ImageFont
import random,json,base64,io
random.seed(12135)
R='/home/claude/brawlpokemons/'
W,H=1200,380;S=3;w,h=W//S,H//S
bg=Image.new('RGBA',(w,h));d=ImageDraw.Draw(bg)
for y in range(h):
    t=y/h;d.line([(0,y),(w,y)],fill=(int(12+18*t),int(26+30*t),int(58+40*t),255))
st=Image.new('RGBA',(w,h));sd=ImageDraw.Draw(st)
for x in range(-h,w,11):sd.line([(x,h),(x+h,0)],fill=(96,165,250,18),width=2)
bg=Image.alpha_composite(bg,st);d=ImageDraw.Draw(bg)
for _ in range(70):
    x,y=random.randrange(w),random.randrange(h);d.point((x,y),fill=random.choice([(147,197,253,255),(255,255,255,255),(96,165,250,255)]))
def outl(im,col,r=1):
    a=im.split()[3].point(lambda v:255 if v>100 else 0);o=Image.new('RGBA',(im.width+2*r,im.height+2*r))
    for dx in range(2*r+1):
        for dy in range(2*r+1):
            if (dx-r)**2+(dy-r)**2<=r*r:o.paste(col,(dx,dy,dx+a.width,dy+a.height),a)
    o.paste(im,(r,r),im);return o
s=open(R+'dev/assets/skins.js').read();sk=json.loads(s[s.index('{'):s.rindex('}')+1])['incineroar_army']
im=Image.open(io.BytesIO(base64.b64decode(sk['spr'].split(',')[1]))).convert('RGBA')
im=im.resize((im.width//2,im.height//2),Image.NEAREST)          # 46x48 도트
m=outl(im.resize((im.width*2,im.height*2),Image.NEAREST),(96,165,250,255),2)
bg.alpha_composite(m,(w-m.width-16,h-m.height-6))
m2=outl(im.transpose(Image.FLIP_LEFT_RIGHT).resize((im.width*2,im.height*2),Image.NEAREST),(96,165,250,255),2)
bg.alpha_composite(m2,(14,h-m2.height-6))
# 토큰
rows=['.....k.....','....kwk....','...kwbbk...','..kwbbbbk..','.kwbbbbbdk.','kwbbbbbbddk','.kbbbbbddk.','..kbbbddk..','...kbddk...','....kdk....','.....k.....'];P={'k':(17,17,17,255),'w':(219,234,254,255),'b':(96,165,250,255),'d':(29,78,216,255)}
tk=Image.new('RGBA',(11,11))
for j,r in enumerate(rows):
    for i,ch in enumerate(r):
        if ch!='.':tk.putpixel((i,j),P[ch])
for (x,y,sc) in [(118,16,2),(272,22,2),(104,92,1),(292,96,1)]:bg.alpha_composite(tk.resize((11*sc,11*sc),Image.NEAREST),(x,y))
big=bg.resize((W,H),Image.NEAREST);d=ImageDraw.Draw(big);d.fontmode='1'
fp=R+'dev/assets/gfont.ttf'
def ct(txt,y,sz,fill,o=4):
    f=ImageFont.truetype(fp,sz);tw=d.textlength(txt,font=f);x=(W-tw)/2
    for dx in range(-o,o+1,2):
        for dy in range(-o,o+1,2):d.text((x+dx,y+dy),txt,font=f,fill=(8,12,28))
    d.text((x,y),txt,font=f,fill=fill)
ct('v1.21.35  ·  이벤트',58,30,(191,219,254),3)
ct('초희귀 챌린지',100,76,(255,255,255),4)
ct('초희귀 포켓몬으로 이기고 토큰을 모으세요!',204,26,(219,234,254),3)
ct('500개 초희귀 프레임  ·  1000개 육군 아미 타이거 어흥염',248,24,(147,197,253),3)
big.convert('RGB').save(R+'notice/v12135.png')
