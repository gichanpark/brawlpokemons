import re,base64,io,json,colorsys,math
from PIL import Image,ImageDraw,ImageFont
R='/home/claude/brawlpokemons/'
ic=open(R+'dev/assets/icons.js').read();pc=open(R+'dev/assets/por.js').read()
def get(src,k):
    m=re.search(r'"%s":\s*"data:image/png;base64,([^"]+)"'%re.escape(k),src);return Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGBA') if m else None
H=lambda s:tuple(int(s[i:i+2],16) for i in (1,3,5))
def lerp(a,b,t):return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
def ramp(cols,t):
    t=max(0,min(1,t))*(len(cols)-1);i=min(len(cols)-2,int(t));return lerp(H(cols[i]),H(cols[i+1]),t-i)
BG={(239,247,183),(127,199,215),(191,223,183)}
def bgcol(p):
    return any(abs(p[0]-b[0])+abs(p[1]-b[1])+abs(p[2]-b[2])<18 for b in BG)
def bgmask(im):
    px=im.load();w,h=im.size;cols=set()
    for x in range(w):
        for y in (0,h-1):cols.add(px[x,y][:3])
    for y in range(h):
        for x in (0,w-1):cols.add(px[x,y][:3])
    def isbg(c):
        hh,l,ss=colorsys.rgb_to_hls(*[v/255 for v in c]);return ss>.28 and l>.6 and .12<=hh<=.55
    cols={c for c in cols if isbg(c)}
    seen=set();st=[(x,y) for x in range(w) for y in (0,h-1)]+[(x,y) for y in range(h) for x in (0,w-1)]
    while st:
        x,y=st.pop()
        if (x,y) in seen or not(0<=x<w and 0<=y<h):continue
        if px[x,y][:3] not in cols:continue
        seen.add((x,y));st+=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    return seen
def recolor(im,T,por=False):
    im=im.copy();px=im.load();w,h=im.size;BGM=bgmask(im) if por else set()
    # dominant hue bucket
    from collections import Counter
    cnt=Counter()
    for y in range(h):
        for x in range(w):
            p=px[x,y]
            if p[3]<128 or (x,y) in BGM:continue
            hh,l,s=colorsys.rgb_to_hls(*[v/255 for v in p[:3]])
            if s>.25 and .15<l<.9:cnt[int(hh*12)%12]+=1
    prim=set(k for k,_ in cnt.most_common(T.get('nprim',1)))
    for y in range(h):
        for x in range(w):
            p=px[x,y]
            if p[3]<128 or (x,y) in BGM:continue
            hh,l,s=colorsys.rgb_to_hls(*[v/255 for v in p[:3]])
            L=l
            if L<.13:continue  # outline
            if s<.25 or L>.9: ramp_=T['n']
            elif int(hh*12)%12 in prim: ramp_=T['p']
            else: ramp_=T['s']
            c=ramp(ramp_,(L-.13)/.8)
            px[x,y]=c+(p[3],)
    return im
def uri(im):
    b=io.BytesIO();im.save(b,'PNG');return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
THEMES=json.load(open('themes.json'))
FORMS={'kyurem':{'f1':'10022','f2':'10023'},'zygarde':{'base':'zy10','f1':'718','f2':'zy100'},'necrozma':{'f1':'10155','f2':'10156','f3':'10157'},'calyrex':{'f1':'cxice','f2':'cxsh'},'rayquaza':{'mega':'mega384'}}
IDS={'mewtwo':'150','rayquaza':'384','kyurem':'646','zygarde':'718','necrozma':'800','arceus':'493','calyrex':'898','solgaleo':'791'}
out={};prev=[]
for k,T in THEMES.items():
    fm=FORMS.get(k,{});base=fm.get('base',IDS[k])
    e={'spr':uri(recolor(get(ic,base),T)),'por':uri(recolor(get(pc,IDS[k]),T,True))}
    prev.append((T['nm'],recolor(get(ic,base),T),recolor(get(pc,IDS[k]),T,True),get(ic,base),get(pc,IDS[k])))
    for f,sk in fm.items():
        if f=='base':continue
        e[f]=uri(recolor(get(ic,sk),T))
    out[k+'_'+T['id']]=e
json.dump(out,open('out.json','w'))
f=ImageFont.truetype(R+'dev/assets/gfont.ttf',16)
cv=Image.new('RGBA',(4*300,2*330),(30,34,44,255));d=ImageDraw.Draw(cv)
for i,(nm,s,p,s0,p0) in enumerate(prev):
    x0=(i%4)*300;y0=(i//4)*330;d.text((x0+150,y0+14),nm,font=f,fill=(255,255,255),anchor='mm')
    sc=min(2,130/max(s.width,s.height)*1.0);S=s.resize((int(s.width*sc),int(s.height*sc)),Image.NEAREST);cv.paste(S,(x0+150-S.width//2,y0+40),S)
    S0=s0.resize((int(s0.width*sc*.5),int(s0.height*sc*.5)),Image.NEAREST);cv.paste(S0,(x0+8,y0+40),S0)
    P=p.resize((120,120),Image.NEAREST);cv.paste(P,(x0+150,y0+200));P0=p0.resize((120,120),Image.NEAREST);cv.paste(P0,(x0+20,y0+200))
cv.save('preview.png')
