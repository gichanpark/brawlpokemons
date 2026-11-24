import json,base64,io,colorsys,math
from PIL import Image,ImageDraw
SPR=json.loads(open('/home/claude/brawlpokemons/dev/assets/icons.js').read()[len('const SPR='):].rstrip().rstrip(';'))
raw=open('/home/claude/brawlpokemons/dev/assets/skins.js').read()
X=json.loads(raw[len('const SKINX='):raw.index(';const SOCCER=')]);SOC=raw[raw.index('const SOCCER="')+14:raw.rindex('"')]
dec=lambda u:Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGBA')
def enc(im):b=io.BytesIO();im.save(b,'PNG');return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
g0=dec(SPR['gmax815']).resize((53,50),Image.NEAREST);P0=g0.load()
def fire(c):
    r,g,b,a=c
    if a==0:return False
    h,l,s=colorsys.rgb_to_hls(r/255,g/255,b/255);h*=360;return s>.3 and (h<70 or h>330) and l>.3
CX,CY,RR=18.5,34.5,15.6
def ball_layer():
    L=Image.new('RGBA',(53,50),(0,0,0,0));p=L.load()
    K=(24,24,30,255);W=(246,246,250,255);W2=(222,224,232,255);W3=(186,190,204,255);HL=(255,255,255,255);SEAM=(140,146,162,255)
    # pentagons in 3D: centers on sphere (unit vectors), project orthographically
    def rot(v,ax,ay):
        x,y,z=v;cy,sy=math.cos(ay),math.sin(ay);x,z=x*cy+z*sy,-x*sy+z*cy;cx,sx=math.cos(ax),math.sin(ax);y,z=y*cx-z*sx,y*sx+z*cx;return (x,y,z)
    ph=(1+5**.5)/2
    ico=[(0,1,ph),(0,-1,ph),(0,1,-ph),(0,-1,-ph),(1,ph,0),(-1,ph,0),(1,-ph,0),(-1,-ph,0),(ph,0,1),(-ph,0,1),(ph,0,-1),(-ph,0,-1)]
    ico=[tuple(c/math.sqrt(1+ph*ph) for c in v) for v in ico]
    ico=[rot(v,-.35,.25) for v in ico]
    for y in range(50):
        for x in range(53):
            dx=(x+.5-CX)/RR;dy=(y+.5-CY)/RR;d2=dx*dx+dy*dy
            if d2>1:continue
            z=math.sqrt(1-d2);n=(dx,dy,z)
            # nearest icosahedron vertex => pentagon if angle small
            best=max(sum(a*b for a,b in zip(n,v)) for v in ico)
            # seams: near boundary between hexes approximated via second-nearest gap
            dots=sorted((sum(a*b for a,b in zip(n,v)) for v in ico),reverse=True)
            lit=-dx*.55-dy*.65+z*.55
            col=W if lit>.35 else (W2 if lit>-.05 else W3)
            if best>.952:col=K
            elif dots[0]-dots[1]<.035 or (dots[1]-dots[2]<.02 and best<.9):col=SEAM if lit>-.05 else (120,124,140,255)
            if lit>.82 and best<=.952:col=HL
            p[x,y]=col
    # outline
    O=L.copy();po=O.load()
    for y in range(50):
        for x in range(53):
            if p[x,y][3]==0 and any(0<=x+a<53 and 0<=y+b<50 and p[x+a,y+b][3] for a,b in((1,0),(-1,0),(0,1),(0,-1))):po[x,y]=(17,17,17,255)
    return O
B=ball_layer()
for sid in ['spurs','korea']:
    src=dec(X['cinderace_'+sid]['gmax']).resize((53,50),Image.NEAREST);ps=src.load();bp=B.load()
    out=src.copy();po=out.load()
    for y in range(50):
        for x in range(53):
            inb=bp[x,y][3]>0
            if fire(P0[x,y]) and y>=19:po[x,y]=(0,0,0,0)
            if y>=29 and x<=44 and not inb:po[x,y]=(0,0,0,0)
            if inb and (y>=25 or fire(P0[x,y]) or ps[x,y][3]==0):po[x,y]=bp[x,y]
    big=out.resize((159,150),Image.NEAREST);X['cinderace_'+sid]['gmax']=enc(big);big.resize((318,300),Image.NEAREST).save(f'gm3_{sid}.png')
open('/home/claude/brawlpokemons/dev/assets/skins.js','w').write('const SKINX='+json.dumps(X)+';const SOCCER="'+SOC+'";')
a=Image.open('gm3_spurs.png');b=Image.open('gm3_korea.png');W=Image.new('RGBA',(a.width*2+20,a.height),(40,32,70,255));W.paste(a,(0,0),a);W.paste(b,(a.width+20,0),b);W.save('gcmp3.png')
