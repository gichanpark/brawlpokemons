# 초희귀 스킨 초안 6종 (원본 도트를 2배로 키운 뒤 색 영역 + 손도트 장식). 초안이라 대충.
import colorsys,sys
from PIL import Image,ImageDraw
H=lambda s:tuple(int(s[i:i+2],16) for i in (1,3,5))+(255,)
OL=H('#141018')
def cls(p):
    if p[3]<128:return '.'
    h,l,s=colorsys.rgb_to_hls(*[v/255 for v in p[:3]]);Hh=h*360
    if l<.18:return 'o'
    if s<.15:return 'W' if l>.8 else ('g' if l>.5 else 'd')
    if Hh<20 or Hh>330:return 'R'
    if Hh<45:return 'N' if l<.5 else 'O'
    if Hh<70:return 'Y'
    if Hh<170:return 'G'
    if Hh<260:return 'B'
    return 'P'
lum=lambda p:colorsys.rgb_to_hls(*[v/255 for v in p[:3]])[1]
def rp(R,t):t=max(0,min(.999,t));return H(R[int(t*len(R))])
class S:
    def __init__(s,src,top=0,right=0):
        b=Image.open(src).convert('RGBA');s.bw,s.bh=b.size;s.top=top
        c=Image.new('RGBA',(s.bw,s.bh+top));c.paste(b,(0,top));c=Image.new('RGBA',(s.bw+right,s.bh+top)) if right else c
        if right:c.paste(b,(0,top))
        s.base=c;s.oy=top*2;s.im=c.resize((c.width*2,c.height*2),Image.NEAREST);s.q=s.im.load();s.bp=c.load();s.W,s.H=s.im.size
    def map(s,f):  # f(bx,by,cls,lum)-> color or None ; by는 원본 좌표(위 여백 뺀)
        for y in range(s.H):
            for x in range(s.W):
                bx,by=x//2,y//2;p=s.bp[bx,by]
                if p[3]<128:continue
                c=f(x,y,bx,by-s.top,cls(p),lum(p))
                if c:s.q[x,y]=H(c) if isinstance(c,str) else c
    def P(s,x,y,c):
        y+=s.oy
        if 0<=x<s.W and 0<=y<s.H:s.q[x,y]=H(c)
    def rect(s,x0,y0,x1,y1,c):
        for y in range(y0,y1+1):
            for x in range(x0,x1+1):s.P(x,y,c)
    def bg(s,x,y,c):  # 빈칸에만
        y+=s.oy
        if 0<=x<s.W and 0<=y<s.H and s.q[x,y][3]<128:s.q[x,y]=H(c)
    def outline(s):
        a=[[s.q[x,y][3]>128 for y in range(s.H)] for x in range(s.W)]
        for y in range(s.H):
            for x in range(s.W):
                if not a[x][y] and any(0<=x+dx<s.W and 0<=y+dy<s.H and a[x+dx][y+dy] for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):s.q[x,y]=OL
D=sys.argv[1]
out={}
# 1. 마술사 후딘 ------------------------------------------------
s=S(D+'/alakazam.png',top=7)
BLK=['#0b0b12','#191926','#2a2a3c','#3d3d55']
def f(x,y,bx,by,c,l):
    if c in 'NO':return rp(BLK,(l-.15)/.5)                 # 어깨 갑옷 → 연미복
    if c in 'Wg' and (bx<=6 or bx>=17):return '#0b0b12'   # 숟가락 → 마술봉
    if c=='Y' and 13<=by<=20 and 9<=bx<=18:return rp(BLK,(l-.3)/.6)   # 몸통 연미복
s.map(f)
# 셔츠·나비넥타이 (목)
s.rect(24,24,31,29,'#f1f5f9');s.rect(24,24,26,25,'#dc2626');s.rect(29,24,31,25,'#dc2626');s.rect(27,24,28,25,'#991b1b')
for y in (27,29):s.P(27,y,'#111111');s.P(28,y,'#111111')
for (x,y) in [(6,19),(7,19),(6,20),(7,20),(38,23),(39,23),(38,24),(39,24)]:s.P(x,y,'#ffffff')
# 실크햇
s.rect(22,-12,35,9,'#0b0b12');s.rect(24,-11,25,4,'#2a2a3c')
s.rect(22,4,35,6,'#dc2626');s.rect(22,6,35,6,'#7f1d1d')
s.rect(19,9,38,10,'#000000');s.rect(19,11,38,11,'#1f1f2e')
for (x,y) in [(41,-8),(44,-3),(16,-6)]:s.bg(x,y,'#fde047')
s.outline();out['magic']=s.im
# 2. 산타 라프라스 ------------------------------------------------
s=S(D+'/lapras.png',top=8,right=0)
def f(x,y,bx,by,c,l):
    if c in 'gW' and bx>=12 and by<=13:return rp(['#7f1d1d','#b91c1c','#dc2626','#ef4444'],(l-.3)/.6)   # 등껍질 → 빨간 선물 보따리
s.map(f)
# 보따리 끈·리본
for x in range(24,42):s.P(x,20,'#fde047')
for y in range(12,30):s.P(33,y,'#fde047')
for (x,y) in [(31,10),(32,11),(34,11),(35,10),(30,9),(36,9),(33,11)]:s.P(x,y,'#fde047')
# 산타 모자 (머리 위, 끝은 왼쪽 위로)
for y in range(-15,3):
    w=(y+15)*12//18+2;x0=13-w//2
    for x in range(x0,x0+w):s.P(x,y,'#dc2626' if (x+y)%5 else '#b91c1c')
for x in range(2,24):s.P(x,2,'#f8fafc');s.P(x,3,'#e2e8f0');s.P(x,4,'#f8fafc')
s.rect(10,-16,14,-13,'#f8fafc')
for (x,y) in [(44,-6),(40,-12),(46,4),(30,-10)]:s.bg(x,y,'#e0f2fe')
s.outline();out['santa']=s.im
# 3. 사이버 쥬피썬더 ----------------------------------------------
s=S(D+'/jolteon.png')
NEON=['#0e4a5c','#0891b2','#22d3ee','#a5f3fc']
def f(x,y,bx,by,c,l):
    if c in 'YN':return rp(NEON,(l-.25)/.6)
    if c in 'Wg':return rp(['#334155','#64748b','#94a3b8','#e2e8f0'],(l-.3)/.7)
s.map(f)
# 회로 무늬 (진한 선 + 분홍 노드)
for (x0,y0,x1,y1) in [(8,16,16,16),(16,16,16,22),(16,22,22,22),(26,12,32,12),(32,12,32,18),(10,20,10,26)]:
    for x in range(x0,x1+1):
        for y in range(y0,y1+1):
            if s.q[x,y][3]>128 and s.q[x,y][:3]!=OL[:3]:s.P(x,y,'#0b2530')
for (x,y) in [(16,16),(22,22),(32,18),(10,26),(26,12)]:s.P(x,y,'#f0abfc')
s.P(9,17,'#f0abfc')   # 눈 빛
s.outline();out['cyber']=s.im
# 4. 사무라이 핫삼 ------------------------------------------------
s=S(D+'/scizor.png',top=4)
CRM=['#3f0d12','#6b1520','#9b1c2c','#c0303e']
def f(x,y,bx,by,c,l):
    if c in 'RO':return rp(CRM,(l-.2)/.55)
    if c in 'Wg':return rp(['#3a2a10','#7a5a18','#c9a227','#f5d76e'],(l-.3)/.7)   # 날개 → 금박
s.map(f)
# 투구 금빛 초승달 장식 (머리 x10~17,y3~6 → 2배, 위 여백 4)
moon=[(18,6),(19,5),(20,4),(21,3),(22,2),(23,2),(24,2),(25,2),(26,2),(27,3),(28,4),(29,5),(30,6),(19,6),(29,6),(20,5),(28,5)]
for (x,y) in moon:s.P(x,y-3,'#f5d76e')
for x in range(18,31):s.P(x,4,'#c9a227')
# 갑옷 줄 + 금 리벳
for y in (32,36):
    for x in range(20,34):
        if s.q[x,y][3]>128 and s.q[x,y][:3]!=OL[:3]:s.P(x,y,'#2a080c')
for (x,y) in [(22,30),(30,30),(22,34),(30,34),(4,24),(46,32)]:s.P(x,y,'#f5d76e')
s.outline();out['samurai']=s.im
# 5. 흡혈귀 블래키 ------------------------------------------------
s=S(D+'/umbreon.png',right=4)
def f(x,y,bx,by,c,l):
    if c=='Y':return rp(['#5f0a14','#9f1239','#dc2626','#f87171'],(l-.25)/.6)
    if c=='B':return rp(['#1a1422','#2b2236','#3d3150','#52436a'],(l-.2)/.6)
s.map(f)
# 망토 (목 뒤에서 오른쪽 아래로) — 빈칸에만
for y in range(14,38):
    w=min(14,(y-14)//1+4)
    for x in range(18,18+w):
        c='#7f1d1d' if x-18<2 else '#0b0b12'
        s.bg(x,y,c)
for x in range(18,33):s.bg(x,38,'#7f1d1d')
s.rect(14,16,19,17,'#dc2626')   # 망토 목 끈
s.P(3,21,'#ffffff');s.P(5,21,'#ffffff')   # 송곳니
s.outline();out['vamp']=s.im
# 6. 해적 갑판장 누리레느 ------------------------------------------
s=S(D+'/primarina.png',top=3)
def f(x,y,bx,by,c,l):
    if c in 'Wg' and by>=13:return '#1e3a8a' if (y//2)%2 else '#f8fafc'   # 줄무늬 셔츠
s.map(f)
# 두건(빨강+흰 물방울)
for y in range(-6,8):
    for x in range(20+max(0,-y),40-max(0,-y-2)):s.P(x,y,'#dc2626')
for (x,y) in [(24,0),(30,-3),(35,2),(27,4),(33,5)]:s.P(x,y,'#ffffff')
for x in range(19,41):s.P(x,8,'#991b1b')
s.rect(40,4,43,6,'#dc2626');s.rect(42,7,45,9,'#b91c1c')
for x in range(18,32,2):s.P(x,27,'#fdf2f8')
s.outline();out['pirate']=s.im
# 미리보기 시트
names=[('magic','마술사 후딘','alakazam'),('santa','산타 라프라스','lapras'),('cyber','사이버 쥬피썬더','jolteon'),('samurai','사무라이 핫삼','scizor'),('vamp','흡혈귀 블래키','umbreon'),('pirate','해적 갑판장 누리레느','primarina')]
for k,_,_ in names:out[k].save(D+'/d_'+k+'.png')
