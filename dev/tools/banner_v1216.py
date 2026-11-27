from PIL import Image,ImageDraw,ImageFont
import random,math
random.seed(1216)
R='/home/claude/brawlpokemons/'
W,H=1200,380;S=4;w,h=W//S,H//S
bg=Image.new('RGBA',(w,h));d=ImageDraw.Draw(bg)
for y in range(h):
    t=y/h;d.line([(0,y),(w,y)],fill=(int(14+16*t),int(10+12*t),int(30+20*t),255))
for x in range(0,w,15):d.line([(x,0),(x,h)],fill=(255,255,255,14))
for y in range(0,h,15):d.line([(0,y),(w,y)],fill=(255,255,255,14))
# 캔들 차트 (오른쪽)
v=60;x=168
for i in range(26):
    o=v;v=max(34,min(88,v+random.randint(-9,11)));c=v
    up=c<o;col=(239,68,68,255) if up else (59,130,246,255)
    hi=min(o,c)-random.randint(1,5);lo=max(o,c)+random.randint(1,5)
    d.line([(x+2,hi),(x+2,lo)],fill=(17,17,17,255),width=1)
    d.rectangle([x,min(o,c),x+4,max(o,c)+1],fill=col,outline=(17,17,17,255))
    x+=5
# 상승 화살표
pts=[(165,80),(200,52),(220,62),(262,22)]
for a,b in zip(pts,pts[1:]):d.line([a,b],fill=(17,17,17,255),width=5);
for a,b in zip(pts,pts[1:]):d.line([a,b],fill=(253,224,71,255),width=3)
d.polygon([(262,14),(270,28),(256,26)],fill=(253,224,71,255),outline=(17,17,17,255))
big=bg.resize((W,H),Image.NEAREST);d=ImageDraw.Draw(big);d.fontmode='1'
fp=R+'dev/assets/gfont.ttf'
def ct(txt,y,sz,fill,o=4,x0=60):
    f=ImageFont.truetype(fp,sz)
    for dx in range(-o,o+1,2):
        for dy in range(-o,o+1,2):d.text((x0+dx,y+dy),txt,font=f,fill=(10,8,20))
    d.text((x0,y),txt,font=f,fill=fill)
ct('v1.21.16  ·  신규 기능',60,30,(226,232,240),3)
ct('포켓 주식 오픈!',104,72,(255,255,255),4)
ct('10분마다 가격 결정 · 많이 사면 ▲ 많이 팔면 ▼',206,24,(252,165,165),3)
ct('실프 · 데봉 · 매크로코스모스 · 조롤컴퍼니 등 8종목',246,24,(147,197,253),3)
big.convert('RGB').save(R+'notice/v1216.png')
