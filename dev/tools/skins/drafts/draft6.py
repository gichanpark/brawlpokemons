# 초희귀 스킨 초안 6종 — 원본 해상도(1픽셀=게임 도트 1칸) 그대로 손도트. 사용: draft6.py <원본 png 폴더>
import colorsys,sys
from PIL import Image
H=lambda s:tuple(int(s[i:i+2],16) for i in (1,3,5))+(255,)
OL='#141018'
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
def rp(R,t):t=max(0,min(.999,t));return R[int(t*len(R))]
class S:
    def __init__(s,src,top=0,right=0):
        b=Image.open(src).convert('RGBA');s.ow,s.oh=b.size
        s.im=Image.new('RGBA',(b.width+right,b.height+top));s.im.paste(b,(0,top));s.oy=top;s.q=s.im.load();s.W,s.H=s.im.size
        s.c=[[cls(s.q[x,y]) for y in range(s.H)] for x in range(s.W)];s.new=set()
    def map(s,f):
        for y in range(s.H):
            for x in range(s.W):
                p=s.q[x,y]
                if p[3]<128:continue
                c=f(x,y-s.oy,s.c[x][y],lum(p))
                if c:s.q[x,y]=H(c)
    def P(s,x,y,c,only=None):
        y+=s.oy
        if 0<=x<s.W and 0<=y<s.H:
            if only=='bg' and s.q[x,y][3]>128:return
            if only=='fg' and s.q[x,y][3]<128:return
            if s.q[x,y][3]<128:s.new.add((x,y))
            s.q[x,y]=H(c)
    def rows(s,spec,c,only=None):   # {y:(x0,x1)}
        for y,(x0,x1) in spec.items():
            for x in range(x0,x1+1):s.P(x,y,c,only)
    def outline(s):   # 새로 칠한 빈칸 둘레만 외곽선
        for (x,y) in list(s.new):
            for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                X,Y=x+dx,y+dy
                if 0<=X<s.W and 0<=Y<s.H and s.q[X,Y][3]<128:s.q[X,Y]=H(OL)
out={}
D=sys.argv[1]
# 1 마술사 후딘 -------------------------------------------------
s=S(D+'/alakazam.png',top=4)
BLK=['#0f0f18','#1c1c2a','#2c2c40','#3f3f58']
s.map(lambda x,y,c,l: rp(BLK,(l-.15)/.5) if c in 'NO' else ('#1c1c2a' if c in 'Wg' and (x<=6 or x>=17) and y>=9 else None))
s.P(3,10,'#f8fafc');s.P(19,12,'#f8fafc')                       # 마술봉 끝
s.P(10,12,'#dc2626');s.P(11,12,'#7f1d1d');s.P(12,12,'#dc2626');s.P(11,13,'#f1f5f9')   # 나비넥타이·셔츠
s.rows({-4:(12,16),-3:(12,16),-2:(12,16),-1:(12,16),0:(12,16)},'#0f0f18')            # 실크햇
s.rows({-1:(12,16)},'#dc2626');s.P(13,-4,'#2c2c40');s.P(13,-3,'#2c2c40')
s.rows({1:(10,18)},'#000000')
s.outline();out['magic']=s.im
# 2 산타 라프라스 -------------------------------------------------
s=S(D+'/lapras.png',top=5)
s.map(lambda x,y,c,l: rp(['#7f1d1d','#b91c1c','#dc2626','#f87171'],(l-.35)/.55) if c in 'gW' and x>=12 and 6<=y<=13 else None)
for y in range(7,13):s.P(16,y,'#facc15','fg')
for x in range(13,20):s.P(x,10,'#facc15','fg')
s.P(15,6,'#facc15');s.P(17,6,'#facc15');s.P(16,7,'#fde68a')
s.rows({0:(3,8),-1:(3,7),-2:(2,6),-3:(1,4),-4:(1,2)},'#dc2626');s.P(5,-1,'#b91c1c');s.P(4,-2,'#b91c1c')
s.rows({1:(2,9)},'#f8fafc');s.P(0,-5,'#f8fafc');s.P(1,-5,'#f8fafc');s.P(0,-4,'#e2e8f0')
s.outline();out['santa']=s.im
# 3 사이버 쥬피썬더 ------------------------------------------------
s=S(D+'/jolteon.png')
NE=['#0e4a5c','#0891b2','#22d3ee','#a5f3fc']
s.map(lambda x,y,c,l: rp(NE,(l-.25)/.6) if c in 'YN' else (rp(['#334155','#64748b','#94a3b8','#e2e8f0'],(l-.3)/.7) if c in 'Wg' else None))
for (x,y) in [(4,8),(5,8),(6,8),(6,9),(13,7),(13,8),(16,9),(16,10),(4,11)]:s.P(x,y,'#0b2530','fg')
for (x,y) in [(7,9),(13,9),(16,11),(4,12)]:s.P(x,y,'#f0abfc','fg')
s.outline();out['cyber']=s.im
# 4 사무라이 핫삼 -------------------------------------------------
s=S(D+'/scizor.png',top=3)
s.map(lambda x,y,c,l: rp(['#3f0d12','#6b1520','#9b1c2c','#c43a48'],(l-.2)/.55) if c in 'RO' else (rp(['#5a3d0c','#9a7414','#d4a72c','#f8dc7a'],(l-.3)/.7) if c in 'Wg' else None))
for (x,y) in [(10,0),(11,1),(12,2),(13,2),(14,2),(15,1),(16,0),(13,3)]:s.P(x,y-3,'#f8dc7a')   # 초승달 투구 장식
for (x,y) in [(13,3)]:s.P(x,y,'#d4a72c')
for (x,y) in [(12,13),(15,13),(13,16),(21,9),(4,9)]:s.P(x,y,'#f8dc7a','fg')                  # 금 리벳
s.outline();out['samurai']=s.im
# 5 흡혈귀 블래키 -------------------------------------------------
s=S(D+'/umbreon.png',right=2)
s.map(lambda x,y,c,l: rp(['#5f0a14','#9f1239','#dc2626','#f87171'],(l-.25)/.6) if c=='Y' else None)
cape={9:(16,17),10:(15,18),11:(16,19),12:(16,20),13:(17,20),14:(17,21),15:(17,20),16:(18,20)}
s.rows(cape,'#0f0f18','bg')
for y in range(10,16):s.P(16 if y<12 else 17,y,'#7f1d1d','bg')
s.P(6,9,'#dc2626');s.P(7,9,'#dc2626')                           # 망토 끈
s.P(1,10,'#f8fafc')                                              # 송곳니
s.outline();out['vamp']=s.im
# 6 해적 갑판장 누리레느 -------------------------------------------
s=S(D+'/primarina.png',top=1)
s.map(lambda x,y,c,l: ('#1e3a8a' if y%2 else '#f8fafc') if c in 'Wg' and y>=13 else None)
for y in range(1,5):
    for x in range(11,20):s.P(x,y,'#dc2626','fg')
for (x,y) in [(12,2),(15,1),(17,3),(14,4)]:s.P(x,y,'#f8fafc','fg')
s.P(20,4,'#dc2626');s.P(21,5,'#b91c1c');s.P(20,5,'#b91c1c')
s.rows({0:(13,16)},'#dc2626')
s.outline();out['pirate']=s.im
for k,v in out.items():v.save(D+'/d_'+k+'.png')
