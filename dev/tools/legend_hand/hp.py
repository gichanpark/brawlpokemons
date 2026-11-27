import json,colorsys,random,sys
sys.path.insert(0,'/tmp/hp')
from base import *
from PIL import Image,ImageDraw,ImageFont
exec(open('/home/claude/brawlpokemons/dev/tools/legend_skins.py').read().split('def uri')[0].split("ic=open")[0])  # imports
src=open('/home/claude/brawlpokemons/dev/tools/legend_skins.py').read()
ns={};exec(src.split('def uri')[0].replace("ic=open(R+'dev/assets/icons.js').read();pc=open(R+'dev/assets/por.js').read()",""),ns)
recolor=ns['recolor'];H=ns['H'];bgmask=ns['bgmask']
TH=json.load(open('themes.json'))
def L(c):return colorsys.rgb_to_hls(*[v/255 for v in c[:3]])[1]
def mix(a,b,t):return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))+(255,)
def h(s):return H(s)+(255,)
def classify(orig,BGM=set()):
    px=orig.load();w,hh=orig.size;C={}
    for y in range(hh):
        for x in range(w):
            p=px[x,y]
            if p[3]<128 or (x,y) in BGM:C[x,y]='T'
            elif L(p)<.13:C[x,y]='O'
            else:C[x,y]='B'
    return C
def hsh(x,y,s=0):return ((x*73856093)^(y*19349663)^(s*83492791))&0xffff
class Ed:
    def __init__(s,im,C,T):s.im=im;s.px=im.load();s.C=C;s.w,s.h=im.size;s.T=T
    def g(s,x,y):return s.C.get((x,y),'T')
    def set(s,x,y,c):
        if 0<=x<s.w and 0<=y<s.h:s.px[x,y]=c if len(c)==4 else c+(255,);s.C[x,y]=s.C.get((x,y)) if s.C.get((x,y))!='T' else 'X'
    def body(s):return [(x,y) for (x,y),v in s.C.items() if v=='B']
    def edgeTop(s):return [(x,y) for (x,y) in s.body() if s.g(x,y-1)=='O' and s.g(x,y-2) in 'TX' or s.g(x,y-1) in 'TX']
def shade(e,ol,rim=.35,dk=.22,rimc=(255,255,255)):
    px=e.px;C=e.C
    for (x,y),v in list(C.items()):
        if v=='O':
            # exterior outline -> theme line colour
            px[x,y]=h(ol)
    B=e.body();up={(x,y) for x,y in B if e.g(x,y-1)=='O' and e.g(x,y-2)=='T' or e.g(x-1,y)=='O' and e.g(x-2,y)=='T'}
    dn={(x,y) for x,y in B if e.g(x,y+1)=='O' and e.g(x,y+2)=='T'}
    for x,y in up:px[x,y]=mix(px[x,y],rimc,rim)
    for x,y in dn-up:px[x,y]=mix(px[x,y],(0,0,0),dk)
def sparkle(e,x,y,c,c2):
    e.set(x,y,c)
    for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
        if e.g(x+dx,y+dy)=='T':e.set(x+dx,y+dy,c2)
def free(e,x,y,r=1):
    return all(e.g(x+i,y+j)=='T' for i in range(-r,r+1) for j in range(-r,r+1))
# ---------- motifs ----------
def m_mewtwo(e,T,form):
    n=T['n'];B=e.body()
    for x,y in B:  # obsidian glints: short diagonal facet lines
        if (x-y)%7==0 and hsh(x//3,y//3,1)%3==0 and L(e.px[x,y])<.45:e.set(x,y,h(n[3]))
def m_rayquaza(e,T,form):
    for x,y in e.body():
        if (x+2*y)%9==0 and hsh(x,y,2)%2 and L(e.px[x,y])<.6 and e.g(x,y+1)=='B':e.set(x,y,h(T['n'][3]));
def m_kyurem(e,T,form):
    for x,y in e.body():
        if e.g(x,y-1) in 'OT' and L(e.px[x,y])<.5 and hsh(x,y,4)%3==0:e.set(x,y,h(T['p'][2]))
def m_zygarde(e,T,form):
    for x,y in e.body():
        if (y%4==1 and x%4==1) or (y%4==3 and x%4==3):
            if all(e.g(x+i,y+j)=='B' for i in(-1,0,1) for j in(-1,0,1)) and L(e.px[x,y])<.75:e.set(x,y,h(T['p'][2]))
def m_necrozma(e,T,form):
    for x,y in e.body():
        if e.g(x,y-1) in 'OT' and e.g(x,y-2)=='T' :e.set(x,y,mix(e.px[x,y],H(T['p'][2]),.6))
def m_arceus(e,T,form):
    p=T['p']
    for x,y in e.body():
        if e.g(x,y-1)=='O' and e.g(x,y-2)=='T':e.set(x,y,h(p[2]))
    # embers rising above the silhouette
    tops=[(x,y) for (x,y),v in e.C.items() if v=='O' and e.g(x,y-1)=='T']
    for i,(x,y) in enumerate(sorted(tops)):
        if hsh(x,y,6)%5==0:
            if e.g(x,y-1)=='T':e.set(x,y-1,h(p[2]))
            if hsh(x,y,7)%2 and e.g(x,y-2)=='T':e.set(x,y-2,h('#fde047'))
def m_calyrex(e,T,form):
    for x,y in e.body():
        if hsh(x,y,8)%23==0 and e.g(x+1,y)=='B':e.set(x,y,h(T['p'][2]));e.set(x+1,y,h(T['p'][3]))
def m_solgaleo(e,T,form):
    for x,y in e.body():
        if L(e.px[x,y])<.4 and hsh(x,y,10)%17==0 and all(e.g(x+i,y+j)=='B' for i in(-1,0,1) for j in(-1,0,1)):
            e.set(x,y,(255,255,255,255))
def edge_particles(e,c,c2,seed,n,cross=False):
    rnd=random.Random(seed);k=0
    for _ in range(600):
        x=rnd.randrange(1,e.w-1);y=rnd.randrange(1,e.h-1)
        if free(e,x,y,2) and any(e.g(x+i,y+j) not in 'TX' for i in range(-4,5) for j in range(-4,5)):
            if cross:sparkle(e,x,y,c if len(c)==4 else c+(255,),c2)
            else:e.set(x,y,c if len(c)==4 else c+(255,))
            k+=1
            if k>=n:break
MOT={'mewtwo':m_mewtwo,'rayquaza':m_rayquaza,'kyurem':m_kyurem,'zygarde':m_zygarde,'necrozma':m_necrozma,'arceus':m_arceus,'calyrex':m_calyrex,'solgaleo':m_solgaleo}
OL={'mewtwo':'#0b0614','rayquaza':'#0b1d33','kyurem':'#02101c','zygarde':'#0f1724','necrozma':'#120c02','arceus':'#2a0802','calyrex':'#3a0a22','solgaleo':'#0a0c26'}
