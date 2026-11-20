from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
W,H=1200,380
bg=Image.new('RGBA',(W,H))
d=ImageDraw.Draw(bg)
for y in range(H):
    t=y/H
    d.line([(0,y),(W,y)],fill=(int(18+12*t),int(24+6*t),int(50-6*t),255))
# radial glow center
gl=Image.new('L',(W,H),0);gd=ImageDraw.Draw(gl);gd.ellipse((W/2-330,H/2-150,W/2+330,H/2+150),fill=150);gl=gl.filter(ImageFilter.GaussianBlur(70))
bg=Image.composite(Image.new('RGBA',(W,H),(60,120,90,255)),bg,gl)
# stripes
st=Image.new('RGBA',(W,H),(0,0,0,0));sd=ImageDraw.Draw(st)
for x in range(-H,W,38):sd.line([(x,H),(x+H,0)],fill=(255,255,255,14),width=10)
bg=Image.alpha_composite(bg,st)
def sil(path,h,col,glow,flip=False):
    im=Image.open(path).convert('RGBA');im=im.crop(im.getbbox())
    if flip:im=im.transpose(Image.FLIP_LEFT_RIGHT)
    r=h/im.height;im=im.resize((int(im.width*r),h),Image.LANCZOS)
    a=im.split()[3].point(lambda v:255 if v>100 else 0)
    pad=30;A=Image.new('L',(im.width+pad*2,im.height+pad*2),0);A.paste(a,(pad,pad))
    g=A.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(9)).point(lambda v:min(255,v*2))
    out=Image.new('RGBA',A.size,(0,0,0,0))
    out=Image.composite(Image.new('RGBA',A.size,glow),out,g)
    out=Image.composite(Image.new('RGBA',A.size,col),out,A)
    return out
def paste(im,x,y):
    global bg;L=Image.new('RGBA',(W,H),(0,0,0,0));L.paste(im,(int(x),int(y)),im);bg=Image.alpha_composite(bg,L)
D=(12,10,30,255)
a=sil('cx/art10193.png',330,D,(186,230,253,255));paste(a,-30,H-a.height+40)
b=sil('cx/art10194.png',330,D,(196,181,253,255),flip=True);paste(b,W-b.width+30,H-b.height+40)
d=ImageDraw.Draw(bg)
f1=ImageFont.truetype('/tmp/gfont.ttf',64);f2=ImageFont.truetype('/tmp/gfont.ttf',30);f3=ImageFont.truetype('/tmp/gfont.ttf',26)
def ct(txt,y,f,fill,sh=(0,0,0,255),o=4):
    w=d.textlength(txt,font=f);x=(W-w)/2
    for dx in range(-o,o+1,2):
        for dy in range(-o,o+1,2):d.text((x+dx,y+dy),txt,font=f,fill=sh)
    d.text((x,y),txt,font=f,fill=fill)
ct('v1.13.0',70,f2,(253,224,71,255),o=3)
ct('풍요의 왕',120,f1,(255,255,255,255))
ct('전설 버드렉스  /  신화 블리자포스 · 레이스포스',215,f3,(233,213,255,255),o=3)
bg.convert('RGB').save('/home/claude/notice_v1130.png')
