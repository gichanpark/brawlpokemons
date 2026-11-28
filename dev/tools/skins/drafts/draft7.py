# 초희귀 스킨 초안 v4 — PIXEL_GUIDE.md 규칙: 원본 해상도, 부위를 테마 물건으로 바꿔 그림, 빛 왼쪽 위, 재질별 3단계, 포켓몬 외곽선
# 사용: draft7.py <원본 png 폴더>  → d7_<키>.png
import sys,os
from PIL import Image
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));import pkoutline
H=lambda s:tuple(int(s[i:i+2],16) for i in (1,3,5))+(255,)
hx=lambda p:'#%02x%02x%02x'%p[:3]
D=sys.argv[1]
class Spr:
    def __init__(s,k,top=0,right=0,left=0):
        s.src=Image.open(f'{D}/{k}.png').convert('RGBA');s.top=top;s.left=left
        s.im=Image.new('RGBA',(s.src.width+right+left,s.src.height+top));s.im.paste(s.src,(left,top));s.q=s.im.load();s.op=s.src.load()
    def orig(s,x,y):
        if 0<=x<s.src.width and 0<=y<s.src.height and s.op[x,y][3]>128:return hx(s.op[x,y])
    def recolor(s,f):   # f(x,y,원본색hex)->새 색 or None
        for y in range(s.src.height):
            for x in range(s.src.width):
                c=s.orig(x,y)
                if c:
                    n=f(x,y,c)
                    if n:s.q[x+s.left,y+s.top]=(0,0,0,0) if n=='_' else H(n)
    def P(s,x,y,c):
        X,Y=x+s.left,y+s.top
        if 0<=X<s.im.width and 0<=Y<s.im.height:s.q[X,Y]=(0,0,0,0) if c=='_' else H(c)
    def patch(s,x0,y0,rows,pal):
        for j,r in enumerate(rows):
            for i,ch in enumerate(r):
                if ch!='.':s.P(x0+i,y0+j,'_' if ch=='_' else pal[ch])
    def done(s,name,extra_dark=()):
        out=pkoutline.fix(s.im,lambda c:c[:3] in [(0x31,0x31,0x31),(0x21,0x21,0x21),(0x14,0x10,0x18)]+list(extra_dark),orig=s.src,oy=s.top)
        out.save(f'{D}/d7_{name}.png');return out
OL='#313131'
# ---------------------------------------------------------------- 1 마술사 후딘
s=Spr('alakazam',top=6)
COAT={'b':'#3a3550','c':'#2a2638','e':'#1b1826','d':'#4c4566'}
def f(x,y,c):
    if c in('#8c6b4a','#b5845a'):return '#2a2638' if c=='#8c6b4a' else '#3a3550'     # 갈색 어깨 → 연미복 어깨
    if 13<=y<=20 and 12<=x<=23 and c in('#f7de3a','#c5ad31','#9c8431'):                  # 몸통 → 연미복
        return {'#f7de3a':'#3a3550','#c5ad31':'#2a2638','#9c8431':'#1b1826'}[c]
    if c in('#bdbdb5','#ffffff','#7b7b7b'):                                                # 숟가락 → 마술봉(검은 막대 + 흰 끝)
        return '#f4f1e8' if (x<=6 and y<=10) or (x>=17 and y<=12) else '#1b1826'
s.recolor(f)
# 숟가락 머리 → 가는 마술봉(흰 끝 + 검은 막대), 손잡이 끝도 검게
s.patch(3,8,["_o_","oWo","oWo","oKo","oKo"],{'o':OL,'W':'#f4f1e8','K':'#1b1826'})
s.patch(18,11,[".o.","oWo","oWo","oKo","oKo"],{'o':OL,'W':'#f4f1e8','K':'#1b1826'})
for (x,y) in [(3,18),(3,19),(20,21),(20,22),(24,24)]:
    if s.orig(x,y) in('#bdbdb5','#ffffff'):s.P(x,y,'#1b1826')
# 셔츠 앞섶 + 나비넥타이 (목 아래 가운데)
s.patch(15,12,["rRr","WwW",".W.",".w."],{'r':'#c42a3a','R':'#7d1424','W':'#f4f1e8','w':'#cfc8b8'})
# 실크햇: 두 귀 사이 정수리를 감싸게(챙이 머리 곡선 위에 얹힘)
s.patch(11,-4,[
 "_oooooo_",
 "_okKKKo_",
 "_okKKKo_",
 "_okKKKo_",
 "_orRRRo_",
 "_orRRRo_",
 "ooKKKKKoo",
 ".okkKKKo.",
],{'o':OL,'K':'#2a2638','k':'#4c4566','r':'#e0414a','R':'#9c1c2c'})
for (x,y) in [(21,-2),(23,0),(9,-1)]:s.P(x,y,'#fde68a')                                 # 반짝이
magic=s.done('magic')
# ---------------------------------------------------------------- 2 산타 라프라스
s=Spr('lapras',top=4,right=1)
RED={'g':'#b81d2c','i':'#7a1020','#efe69c':None}
def f(x,y,c):
    if c in('#bdbdb5','#848484','#525252') and x>=11 and 6<=y<=14:                      # 등껍질 → 선물 보따리
        if c=='#525252':return '#5c0c18'
        return '#7a1020' if c=='#848484' else ('#e0414a' if (x+y)<=20 else '#b81d2c')
s.recolor(f)
# 보따리 주름·묶은 금 끈·삐죽 나온 선물
for (x,y,c) in [(14,9,'#7a1020'),(16,11,'#7a1020'),(18,10,'#7a1020'),(13,8,'#f27a7a'),(14,7,'#f27a7a')]:s.P(x,y,c)
s.patch(14,4,["oo.oo","oYoYo",".oYo.","oYyYo"],{'o':OL,'Y':'#d4a72c','y':'#f8e08a'})
s.patch(16,2,["oGGo","oGgo","oooo"],{'o':OL,'G':'#2f8f4e','g':'#62c47a'})        # 선물상자 머리
s.P(17,2,'#f8e08a');s.P(18,3,'#f8e08a')
# 산타 모자: 머리를 감싸고 끝이 뒤(목 쪽)로 접혀 넘어감
s.patch(0,-4,[
 "...ooooo....",
 "..oRRRRro...",
 ".oRRRRRRrooo",
 "oWwWwWwWwRRo",
 "oWwWwWwWwoRo",
 "..........oWo",
],{'o':OL,'R':'#b81d2c','r':'#e0414a','W':'#f4f7fa','w':'#cfd6dc'})
s.patch(11,1,["oWo","oWo","_o_"],{'o':OL,'W':'#f4f7fa'})
santa=s.done('santa')
# ---------------------------------------------------------------- 3 사이버 쥬피썬더
s=Spr('jolteon')
M={'#ffef4a':'#8a96ae','#dec542':'#6a7690','#bd9c3a':'#48526a','#ffffff':'#e6edf5','#c5c5ce':'#a9b4c6','#848473':'#5d6678','#84737b':'#4a4f62','#525252':'#2b3040'}
s.recolor(lambda x,y,c:M.get(c))
CY,CY2='#3ee6ff','#b8f6ff'
# 갈기 끝(뾰족한 털)을 네온 날로: 바깥쪽 끝 픽셀만
for (x,y) in [(4,1),(4,2),(3,3),(16,5),(17,6),(18,7),(17,8),(16,9),(18,10),(1,9),(1,12),(1,14),(16,13),(17,14),(17,16)]:
    if s.orig(x,y) and s.orig(x,y)!='#313131':s.P(x,y,CY)
for (x,y) in [(5,2),(4,3),(17,7),(16,8)]:
    if s.orig(x,y) and s.orig(x,y)!='#313131':s.P(x,y,CY2)
# 회로(옆구리): 진한 선 + 빛나는 노드
for (x,y,c) in [(3,9,'#2b3040'),(4,9,'#2b3040'),(5,9,'#2b3040'),(5,10,'#2b3040'),(6,10,CY),(3,11,'#2b3040'),(3,12,CY),(12,7,'#2b3040'),(12,8,CY)]:s.P(x,y,c)
# 눈 → 바이저
s.P(5,6,'#ff4fd8');s.P(4,6,'#b0309a')
cyber=s.done('cyber')
# ---------------------------------------------------------------- 4 사무라이 핫삼 (v3 그대로 불러옴)
samurai=Image.open(f'{D}/d_samurai_v3.png').convert('RGBA');samurai.save(f'{D}/d7_samurai.png')
# ---------------------------------------------------------------- 5 흡혈귀 블래키
s=Spr('umbreon')
M={'#738484':'#6a5f7c','#526b73':'#4a405a','#84949c':'#857a98','#525252':'#2c2438',
   '#f7d642':'#d8243c','#c5ad29':'#8e1028','#9c3129':'#ff5a5a','#f76352':'#ffd0d0'}
s.recolor(lambda x,y,c:M.get(c))
# 고리 하이라이트(왼쪽 위) + 송곳니 + 목의 박쥐 모양 리본
for (x,y) in [(2,2),(8,5),(17,4),(5,14)]:
    if s.orig(x,y) in('#f7d642',):s.P(x,y,'#ff6b7f')
s.P(2,10,'#f4f1e8');s.P(4,10,'#f4f1e8')
s.patch(5,11,["RoR","oRo"],{'R':'#d8243c','o':'#5c0c18'})
vamp=s.done('vamp')
# ---------------------------------------------------------------- 6 해적 갑판장 누리레느
s=Spr('primarina',top=1,right=2)
RD={'R':'#c42a3a','r':'#e85a5a','D':'#7d1424','W':'#f4f1e8'}
def f(x,y,c):
    if y<=5 and c in('#b5c5f7',):return '#e85a5a' if x<=12 else '#c42a3a'              # 머리 볏(모자처럼 생긴 머리) → 두건
    if y<=6 and c in('#4a4a4a','#94deef') and 15<=x<=19:return '#7d1424'               # 두건 뒤 그림자
    if y>=15 and c in('#ffffff','#cecece'):return '#1e3a8a' if y%2 else '#f4f1e8'       # 흰 옷 → 줄무늬 셔츠
s.recolor(f)
for (x,y) in [(12,2),(14,4),(15,1),(13,5),(16,3)]:
    if s.orig(x,y)=='#b5c5f7':s.P(x,y,'#f4f1e8')
s.patch(18,2,["oRo.","oRRo",".oDRo","..oo"],{'o':'#212121','R':'#c42a3a','D':'#7d1424'})   # 매듭 꼬리
for x in range(10,15):s.P(x,14,'#fdf2f8' if x%2==0 else '#f0abfc')                          # 진주 목걸이
pirate=s.done('pirate',extra_dark=[(0x21,0x21,0x21)])
