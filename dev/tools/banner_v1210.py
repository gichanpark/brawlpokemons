from PIL import Image,ImageDraw,ImageFont
import random,base64,io
random.seed(1210)
R='/home/claude/brawlpokemons/'
W,H=1200,380;S=3;w,h=W//S,H//S
bg=Image.new('RGBA',(w,h));d=ImageDraw.Draw(bg)
for y in range(h):
    t=y/h;d.line([(0,y),(w,y)],fill=(int(18+22*t),int(20+14*t),int(34+18*t),255))
st=Image.new('RGBA',(w,h));sd=ImageDraw.Draw(st)
for x in range(-h,w,11):sd.line([(x,h),(x+h,0)],fill=(148,163,184,16),width=2)
bg=Image.alpha_composite(bg,st);d=ImageDraw.Draw(bg)
for _ in range(60):
    x,y=random.randrange(w),random.randrange(h);d.point((x,y),fill=random.choice([(192,132,252,255),(255,255,255,255),(148,163,184,255)]))
def outl(im,col,r=1):
    a=im.split()[3].point(lambda v:255 if v>100 else 0);o=Image.new('RGBA',(im.width+2*r,im.height+2*r))
    for dx in range(2*r+1):
        for dy in range(2*r+1):
            if (dx-r)**2+(dy-r)**2<=r*r:o.paste(col,(dx,dy,dx+a.width,dy+a.height),a)
    o.paste(im,(r,r),im);return o
m=Image.open(R+'dev/assets/variants/armored_mewtwo_icon.png').convert('RGBA')
m=outl(m.resize((m.width*5,m.height*5),Image.NEAREST),(192,132,252,255),2)
bg.alpha_composite(m,(w-m.width-14,h-m.height-4))
# shards
rows=['....kkkk....','..kkggggkk..','.kgwwggggdk.','kgwggggggdgk','kgggkkkkggdk','kggk....kgdk','kggk....kgdk','.kgk....kdk.','..kk....kk..'];P={'k':(17,17,17,255),'g':(148,163,184,255),'w':(226,232,240,255),'d':(71,85,105,255)}
sh=Image.new('RGBA',(12,9))
for j,r in enumerate(rows):
    for i,ch in enumerate(r):
        if ch!='.':sh.putpixel((i,j),P[ch])
for (x,y,s) in [(14,70,3),(44,86,2),(24,100,2),(60,60,2)]:
    bg.alpha_composite(sh.resize((12*s,9*s),Image.NEAREST),(x,y))
big=bg.resize((W,H),Image.NEAREST);d=ImageDraw.Draw(big);d.fontmode='1'
fp=R+'dev/assets/gfont.ttf'
def ct(txt,y,sz,fill,o=4,x0=None):
    f=ImageFont.truetype(fp,sz);tw=d.textlength(txt,font=f);x=(W-tw)/2-120 if x0 is None else x0
    for dx in range(-o,o+1,2):
        for dy in range(-o,o+1,2):d.text((x+dx,y+dy),txt,font=f,fill=(10,8,20))
    d.text((x,y),txt,font=f,fill=fill)
ct('v1.21.0  ·  이벤트',62,30,(226,232,240),3)
ct('아머드 뮤츠 구출',104,72,(255,255,255),4)
ct('갑옷 조각 1000개를 모아 크로마틱 아머드 뮤츠를 데려오세요!',206,24,(203,213,225),3)
ct('+ 조롤 로또 · 상자 모두 열기',246,24,(192,132,252),3)
big.convert('RGB').save(R+'notice/v1210.png')
