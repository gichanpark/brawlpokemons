# 붉은 스킨 4종 PMD 초상화(40x40): 원본 초상화 → 배경 보존, 스프라이트와 같은 색 규칙
import sys,colorsys
from PIL import Image
D=sys.argv[1];H=lambda s:tuple(int(s[i:i+2],16) for i in (1,3,5))+(255,)
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
CR=['#3a0c14','#7d1424','#b0202e','#d8343e','#f06a6a']      # 진홍 (어두움→밝음)
def run(k,f,out,stamps=()):
    im=Image.open(f'{D}/p_{k}.png').convert('RGBA');bg=bgmask(im);q=im.load()
    for y in range(40):
        for x in range(40):
            if (x,y) in bg:continue
            c=q[x,y];h,l,s=hls(c);n=f(x,y,c,h,l,s,max(c[:3])-min(c[:3]))
            if n:q[x,y]=n if isinstance(n,tuple) else H(n)
    for x,y,c in stamps:q[x,y]=H(c)
    im.save(f'{D}/pr4_{out}.png')
# 1 개굴닌자: 파란 몸 → 진홍, 분홍 혀 목도리 → 검은 목도리, 하늘색 줄 → 금
def f1(x,y,c,h,l,s,ch):
    if l<.2:return None
    if .55<h<.72 and s>.25:return rp(CR,(l-.15)/.5)
    if (h>.9 or h<.02) and s>.4 and y>=17:return rp(['#1a1420','#2c2534','#4a4054','#6a5f78'],(l-.35)/.5)
    if .45<h<.55 and s>.3:return rp(['#b0841a','#f5c542','#fff1a8'],(l-.5)/.4)
run('greninja',f1,'ninja')
# 2 한카리아스: 파란 몸 → 진홍, 빨간 턱 → 금빛 크림, 노란 지느러미 → 금
def f2(x,y,c,h,l,s,ch):
    if l<.2:return None
    if .55<h<.75 and s>.2:return rp(CR,(l-.15)/.55)
    if (h<.06 or h>.95) and s>.35:return rp(['#a87a2a','#d9a94a','#f8dc9a'],(l-.3)/.45)
    if .1<h<.18 and s>.5:return rp(['#b0841a','#f5c542','#fff1a8'],(l-.4)/.5)
run('garchomp',f2,'dragon')
# 3 가디안: 얼굴(위쪽)은 흰색 그대로, 30줄 아래 흰·회색 몸 → 진홍 드레스, 가슴 뿔 → 금, 머리에 장미
def f3(x,y,c,h,l,s,ch):
    if y>=30 and ch<40 and l>.45:return rp(CR,(l-.4)/.6)
    if y>=34 and (h>.9 or h<.03) and s>.3:return rp(['#b0841a','#f5c542','#fff1a8'],(l-.2)/.6)
run('gardevoir',f3,'rose',stamps=[(x+(-2),y+5,c) for x,y,c in [(26,4,'#8e1028'),(27,4,'#e0313f'),(28,4,'#8e1028'),(26,5,'#e0313f'),(27,5,'#ff9aa2'),(28,5,'#e0313f'),(27,6,'#8e1028'),(26,6,'#b0202e'),(28,6,'#b0202e'),(27,3,'#3a0c14'),(25,5,'#3a0c14'),(29,5,'#3a0c14'),(27,7,'#3a0c14')]])
# 4 리자몽: 주황 → 진홍(밝게), 크림 → 살구, 청록 → 검붉음
def f4(x,y,c,h,l,s,ch):
    if l<.2:return None
    if .02<h<.11 and s>.35:return rp(['#5c1420','#8e1f2c','#c4303c','#e85a5a','#ffb08a'],(l-.25)/.5)
    if .11<=h<.18 and s>.3:return rp(['#e0704a','#ffb08a','#ffd8c4'],(l-.5)/.4)
    if .45<h<.6 and s>.15 and x<25:return rp(['#2a0a10','#3a1018','#6e1824'],(l-.2)/.5)
run('charizard',f4,'blackflame')
