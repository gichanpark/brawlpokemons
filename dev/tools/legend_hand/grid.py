import sys;sys.path.insert(0,'/tmp/hp')
from run import *
from PIL import ImageDraw,ImageFont
f=ImageFont.truetype('/home/claude/brawlpokemons/dev/assets/gfont.ttf',11)
def grid(im,Z,name):
    w,hh=im.size;cv=Image.new('RGBA',(w*Z+24,hh*Z+24),(30,32,40,255));d=ImageDraw.Draw(cv)
    A=im.resize((w*Z,hh*Z),Image.NEAREST);cv.paste(A,(22,22),A)
    for x in range(w+1):d.line([(22+x*Z,22),(22+x*Z,22+hh*Z)],fill=(70,74,90) if x%5 else (140,140,60))
    for y in range(hh+1):d.line([(22,22+y*Z),(22+w*Z,22+y*Z)],fill=(70,74,90) if y%5 else (140,140,60))
    for x in range(0,w,5):d.text((22+x*Z+2,4),str(x),font=f,fill=(250,230,80))
    for y in range(0,hh,5):d.text((2,22+y*Z+2),str(y),font=f,fill=(250,230,80))
    cv.save(name)
for k in sys.argv[1:]:
    fm=FORMS.get(k,{});a,s,_=make(k,fm.get('base',IDS[k]),'spr');grid(a,18,'g_'+k+'.png')
    p,_,_=make(k,IDS[k],'por',True);grid(p,14,'gp_'+k+'.png')
