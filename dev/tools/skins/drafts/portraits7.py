# 초희귀 스킨 5종 던전 초상화(40x40). 원본 PMD 초상화에서 출발, 배경(가장자리 flood fill) 보존
import sys,colorsys
from PIL import Image
D=sys.argv[1]
H=lambda s:tuple(int(s[i:i+2],16) for i in (1,3,5))+(255,)
hls=lambda c:colorsys.rgb_to_hls(*[v/255 for v in c[:3]])
def rp(R,t):t=max(0,min(.999,t));return H(R[int(t*len(R))])
def bgmask(im):
    px=im.load();w,h=im.size
    def isbg(c):
        hh,l,ss=hls(c);return ss>.25 and l>.55 and .2<=hh<=.55
    seen=set();st=[(x,y) for x in range(w) for y in (0,h-1)]+[(x,y) for y in range(h) for x in (0,w-1)]
    while st:
        x,y=st.pop()
        if (x,y) in seen or not(0<=x<w and 0<=y<h) or not isbg(px[x,y]):continue
        seen.add((x,y));st+=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    return seen
class Por:
    def __init__(s,k):
        s.im=Image.open(f'{D}/p_{k}.png').convert('RGBA');s.src=s.im.copy();s.q=s.im.load();s.o=s.src.load();s.bg=bgmask(s.src)
    def each(s,f):
        for y in range(40):
            for x in range(40):
                if (x,y) in s.bg:continue
                n=f(x,y,s.o[x,y],*hls(s.o[x,y]))
                if n:s.q[x,y]=H(n) if isinstance(n,str) else n
    def P(s,x,y,c):
        if 0<=x<40 and 0<=y<40:s.q[x,y]=H(c)
    def patch(s,x0,y0,rows,pal):
        for j,r in enumerate(rows):
            for i,ch in enumerate(r):
                if ch!='.':s.P(x0+i,y0+j,pal[ch])
out={}
COAT=['#16141e','#2a2638','#3a3550','#4c4566']
# 1 마술사 후딘 — 어깨 갑옷 → 연미복, 실크햇, 나비넥타이
s=Por('alakazam')
s.each(lambda x,y,p,h,l,sa: rp(COAT,(l-.15)/.5) if (x<12 or x>29) and y>10 and not(.1<h<.2 and sa>.4) else None)
s.patch(9,0,[
 "...ooooooooooooooo...",
 "...okKKKKKKKKKKKKo...",
 "...okKKKKKKKKKKKKo...",
 "...okKKKKKKKKKKKKo...",
 "...orRRRRRRRRRRRRo...",
 "...oDDDDDDDDDDDDDo...",
 "ooooKKKKKKKKKKKKKoooo",
 "oKkkKKKKKKKKKKKKKKKKo",
 ".oooooooooooooooooo..",
],{'o':'#120e18','K':'#2a2638','k':'#4c4566','R':'#c42a3a','r':'#e85a5a','D':'#7d1424'})
s.patch(16,36,["oRRooRRo.","RrRDDRrR.","oRRooRRo.","WWWWWWWW."],{'o':'#3a0a14','R':'#c42a3a','r':'#e85a5a','D':'#7d1424','W':'#f4f1e8'})
out['magic']=s.im
# 2 산타 라프라스 — 산타 모자(끝이 오른쪽 뒤로 접힘), 등껍질 → 빨간 보따리
s=Por('lapras')
s.each(lambda x,y,p,h,l,sa: rp(['#5c0c18','#8a1424','#b81d2c','#e0414a'],(l-.3)/.55) if x<10 and y>28 and sa<.2 else None)
s.patch(11,0,[
 "....oooooooooo..........",
 "..ooRRRRRRRRrRoooo......",
 ".oRRRRRRRRRRRRRRRRoo....",
 "oRRRRRRRRRRRRRRRRRRRoo..",
 "oRRRRRRRRRRRRRRRRRRRRRo.",
 "oWwWwWwWwWwWwWwWwWwoRRo.",
 "oWWWWWWWWWWWWWWWWWWo.oRo",
 ".ooooooooooooooooooo.oWWo",
 "....................oWWWo",
 ".....................ooo.",
],{'o':'#3a0a14','R':'#b81d2c','r':'#e85a5a','W':'#f4f7fa','w':'#cfd6dc'})
out['santa']=s.im
# 3 사이버 쥬피썬더 — 노란 털 → 금속, 흰 갈기 → 밝은 금속 + 네온 끝, 분홍 눈빛
s=Por('jolteon')
ST=['#2b3040','#48526a','#6a7690','#8a96ae','#b4bfd2']
def f(x,y,p,h,l,sa):
    if .1<h<.2 and sa>.3:return rp(ST,(l-.25)/.6)
    if sa<.15 and l>.7:
        if any((x+dx,y+dy) in s.bg for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):return '#3ee6ff'
        return rp(['#8a96ae','#b4bfd2','#e6edf5'],(l-.7)/.3)
s.each(f)
for (x,y) in [(16,21),(17,21),(28,21),(29,21)]:s.P(x,y,'#ff4fd8')
out['cyber']=s.im
# 4 흡혈귀 블래키 — 고리 → 핏빛, 몸 → 보랏빛 어둠
s=Por('umbreon')
def f(x,y,p,h,l,sa):
    if .08<h<.18 and sa>.4:return rp(['#5c0c18','#8e1028','#d8243c','#ff6b7f'],(l-.25)/.55)
    if .45<h<.6 and l<.45:return rp(['#1e1828','#2c2438','#4a405a','#6a5f7c'],(l-.08)/.4)
s.each(f)
out['vamp']=s.im
# 5 해적 갑판장 누리레느 — 머리 볏(구슬 모양 머리) → 두건, 흰 몸 → 줄무늬 셔츠
s=Por('primarina')
def f(x,y,p,h,l,sa):
    if y<=10 and 8<=x<=30 and max(p[:3])-min(p[:3])<70 and not (h<.05 or h>.9):
        if l<.32:return '#3a0a14'
        return rp(['#7d1424','#a8202f','#c42a3a','#e85a5a'],(l-.35)/.6)
    if y>=33 and max(p[:3])-min(p[:3])<70 and l>.6:return '#1e3a8a' if y%2 else '#f4f1e8'
s.each(f)
for (x,y) in [(12,3),(16,1),(19,5),(14,7),(22,3),(25,7),(27,4),(18,8)]:
    if (x,y) not in s.bg:s.P(x,y,'#f4f1e8')
s.patch(26,7,["RRo..","oRRo.",".oRRo","..oo."],{'o':'#3a0a14','R':'#c42a3a'})
for x in range(14,24):
    if (x,30) not in s.bg:s.P(x,30,'#fdf2f8' if x%2 else '#f0abfc')
out['pirate']=s.im
for k,v in out.items():
    # (15색 줄이기는 MEDIANCUT 양자화가 모자 띠 색을 망가뜨려서 안 함)
    v.save(f'{D}/p7_{k}.png');print(k,len(set(v.get_flattened_data())),'colors')
