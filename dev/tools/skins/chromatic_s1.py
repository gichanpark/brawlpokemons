# 시즌 1 보상 크로마틱: 은빛 갑주 아머까오(scorvi) · 황동 가시 너트령(bferro) — 원본 해상도 손도트 + 초상화
# 사용: chromatic_s1.py <폴더: corviknight.png ferrothorn.png p_corviknight.png p_ferrothorn.png 가 있는 곳>
import sys,os,colorsys
from PIL import Image
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'drafts'));import pkoutline
D=sys.argv[1]
H=lambda s:tuple(int(s[i:i+2],16) for i in (1,3,5))+(255,)
hls=lambda c:colorsys.rgb_to_hls(*[v/255 for v in c[:3]])
def rp(R,t):t=max(0,min(.999,t));return H(R[int(t*len(R))])
SIL=['#2c3340','#4a5466','#6f7b90','#9aa6ba','#c9d2e0','#f1f5fb']
BRS=['#3b2a10','#6e4c1a','#a8782c','#d9a94a','#f5d88a']
COP=['#4a2a12','#7a4420','#b06a34','#d99a5c']
def edge_hi(im,test,col):   # 빛(왼쪽 위): 위나 왼쪽이 외곽선/빈칸이면 가장 밝은 색
    q=im.load();W,Hh=im.size;ch=[]
    for y in range(Hh):
        for x in range(W):
            if not test(q[x,y]):continue
            up=q[x,y-1] if y>0 else (0,0,0,0);lf=q[x-1,y] if x>0 else (0,0,0,0)
            if up[3]<128 or up[:3]==(0x31,0x31,0x31) or lf[3]<128 or lf[:3]==(0x31,0x31,0x31):ch.append((x,y))
    for x,y in ch:q[x,y]=H(col)
# ---------------------------------------------------------- 은빛 갑주 아머까오
src=Image.open(f'{D}/corviknight.png').convert('RGBA');im=src.copy();q=im.load()
for y in range(im.height):
    for x in range(im.width):
        p=q[x,y]
        if p[3]<128 or p[:3]==(0x31,0x31,0x31):continue
        h,l,s=hls(p)
        if .55<h<.85 and s>.12:q[x,y]=rp(SIL,(l-.12)/.55)          # 남색 깃털 → 은빛 갑판
silver=lambda c:c[3]>128 and c[:3] in [H(v)[:3] for v in SIL[1:5]]
edge_hi(im,silver,SIL[5])
# 이마 사파이어 + 볏 끝 광택 + 가슴판 리벳
for (x,y,c) in [(10,4,'#3b82f6'),(9,3,'#93c5fd'),(9,1,SIL[5]),(30,5,SIL[5]),(15,13,'#dbeafe'),(20,15,'#dbeafe'),(12,16,'#dbeafe')]:
    if q[x,y][3]>128:q[x,y]=H(c)
pkoutline.fix(im,lambda c:c[:3]==(0x31,0x31,0x31),orig=src,oy=0).save(f'{D}/s_scorvi.png')
# ---------------------------------------------------------- 황동 가시 너트령
src=Image.open(f'{D}/ferrothorn.png').convert('RGBA');PADL,PADB,PADR=2,2,2
im=Image.new('RGBA',(src.width+PADL+PADR,src.height+PADB));im.paste(src,(PADL,0));q=im.load()
M={'#ceced6':BRS[3],'#adadad':BRS[2],'#7b7b7b':BRS[1],'#525252':BRS[0],'#73c57b':COP[3],'#63ad6b':COP[2],'#4a8452':COP[1],'#ffbd29':'#9ef0ff','#b56b19':'#155e75'}   # 눈: 황동 몸에 묻히지 않게 청록 빛
for y in range(im.height):
    for x in range(im.width):
        p=q[x,y]
        if p[3]<128:continue
        c='#%02x%02x%02x'%p[:3]
        if c in M:q[x,y]=H(M[c])
edge_hi(im,lambda c:c[3]>128 and c[:3] in [H(BRS[2])[:3],H(BRS[3])[:3]],BRS[4])
O='#313131'
def spike(x,y,d):   # 원본 좌표 기준, 바깥으로 뻗는 황동 가시 2칸 (빛: 위·왼쪽 면 밝게)
    x+=PADL
    pts={'D':[((0,0),BRS[3]),((0,1),BRS[1]),((-1,0),O),((1,0),O),((-1,1),O),((1,1),O),((0,2),O)],
         'L':[((0,0),BRS[3]),((-1,0),BRS[1]),((0,-1),O),((0,1),O),((-1,-1),O),((-1,1),O),((-2,0),O)],
         'R':[((0,0),BRS[3]),((1,0),BRS[2]),((0,-1),O),((0,1),O),((1,-1),O),((1,1),O),((2,0),O)]}[d]
    for (dx,dy),c in pts:
        X,Y=x+dx,y+dy
        if 0<=X<im.width and 0<=Y<im.height and (c!=O or q[X,Y][3]<128):q[X,Y]=H(c)
for (x,y,d) in [(14,15,'D'),(17,15,'D'),(20,15,'D'),(3,14,'D'),(-1,11,'L'),(26,21,'D'),(30,18,'R'),(10,14,'D')]:spike(x,y,d)
pkoutline.fix(im,lambda c:c[:3]==(0x31,0x31,0x31),orig=src,oy=0).save(f'{D}/s_bferro.png')
# ---------------------------------------------------------- 초상화
def bgmask(img):
    px=img.load();w,h=img.size
    def isbg(c):
        hh,l,ss=hls(c);return ss>.25 and l>.55 and .2<=hh<=.55
    seen=set();st=[(x,y) for x in range(w) for y in (0,h-1)]+[(x,y) for y in range(h) for x in (0,w-1)]
    while st:
        x,y=st.pop()
        if (x,y) in seen or not(0<=x<w and 0<=y<h) or not isbg(px[x,y]):continue
        seen.add((x,y));st+=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    return seen
p=Image.open(f'{D}/p_corviknight.png').convert('RGBA');bg=bgmask(p);q=p.load()
for y in range(40):
    for x in range(40):
        if (x,y) in bg:continue
        h,l,s=hls(q[x,y])
        if .55<h<.85 and s>.08 and l>.12:q[x,y]=rp(SIL,(l-.1)/.5)
for (x,y,c) in [(22,9,'#3b82f6'),(23,9,'#93c5fd'),(22,10,'#1d4ed8'),(23,10,'#3b82f6')]:q[x,y]=H(c)
p.save(f'{D}/p_scorvi.png')
p=Image.open(f'{D}/p_ferrothorn.png').convert('RGBA');bg=bgmask(p);q=p.load()
for y in range(40):
    for x in range(40):
        if (x,y) in bg:continue
        c=q[x,y];h,l,s=hls(c);ch=max(c[:3])-min(c[:3])
        if ch<30 and l>.3:q[x,y]=rp(BRS,(l-.3)/.65)                 # 회색 몸 → 황동
        elif .2<h<.45 and s>.2:q[x,y]=rp(COP,(l-.2)/.6)              # 초록 덩굴 → 구리
p.save(f'{D}/p_bferro.png')
