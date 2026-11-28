# 사무라이 핫삼 초안 v3 — 원본 26x27 해상도에서 손도트.
# 원칙(Derek Yu·Lospec 튜토리얼): 빛은 왼쪽 위 한 방향 / 1픽셀 외곽선 / 갑옷이 몸 형태를 따라가게(머리=투구, 어깨=소데, 몸통=도, 허리=쿠사즈리, 정강이=스네아테)
# 장식을 '얹는' 대신 원래 부위를 갑옷 부위로 바꿔 그림.
import sys
from PIL import Image
H=lambda s:tuple(int(s[i:i+2],16) for i in (1,3,5))+(255,)
PAL={'o':'#1a0f12','K':'#241a22','k':'#4a3644','C':'#6b1520','R':'#a51f2e','r':'#d0434e','G':'#8a6414','Y':'#d4a72c','y':'#f8e08a',
     'S':'#4a5163','s':'#8a93a6','w':'#eef2f7','E':'#ffd23f'}
src=Image.open(sys.argv[1]).convert('RGBA');ox=src.load()
ORIG={'#313131':'o','#ffb5a5':'r','#ef8c73':'R','#d66342':'R','#bd4231':'C','#525252':'K','#7b7b7b':'k','#ffc529':'E','#ffffff':'w','#9c9cb5':'s','#bdbdbd':'S'}
TOP=4;W,Hh=src.width,src.height+TOP
im=Image.new('RGBA',(W,Hh));q=im.load()
for y in range(src.height):
    for x in range(src.width):
        p=ox[x,y]
        if p[3]<128:continue
        c=ORIG['#%02x%02x%02x'%p[:3]]
        if y>=22 and c in 'rRC':c={'r':'w','R':'s','C':'S'}[c]          # 정강이 → 쇠 스네아테
        q[x,y+TOP]=H(PAL[c])
def patch(x0,y0,rows):
    for j,r in enumerate(rows):
        for i,ch in enumerate(r):
            x,y=x0+i,y0+j+TOP
            if ch=='.' or not(0<=x<W and 0<=y<Hh):continue
            q[x,y]=(0,0,0,0) if ch=='_' else H(PAL[ch])
# 투구(카부토) + 초승달 장식(마에다테) + 접힌 귀덮개(후키가에시). 원래 흰 뿔은 지움
patch(7,-4,[
 "_oyo_____oyo_",
 "_oYYo___oYYo_",
 "_oGyYoooYyYGo",
 "__oGYyyyYYGo_",
 "___ooGYGGoo__",
 "___okKGKKo___",
 "__okkKGKKKo__",
 "_okkKKGKKKKo_",
 "okkKKKGKKKKKo",
 "oyYYYYYYYYYGo",
 "oRo._....oRo.",
 "_oo......oo_.",
])
for (x,y) in [(9,6),(9,7),(10,5),(10,6)]:   # 뿔 남은 조각 → 얼굴색
    if q[x,y+TOP][3]>128 and q[x,y+TOP][:3]==H(PAL['S'])[:3] or q[x,y+TOP][:3]==H(PAL['w'])[:3]:q[x,y+TOP]=H(PAL['R'])
# 몸통 갑옷(도) + 금 문장 + 금 허리띠 + 쿠사즈리 3장
patch(8,13,[
 "...oKkKo...",
 "..oKkRRKo..",
 "..okRYRRKo.",
 "..oCCCCCCo.",
 "..okRRRRKo.",
 ".oyYYYYYYGo",
 "okRokRokRo.",
 "okCokCokCo.",
 "ooo.ooo.oo.",
])
# 어깨 갑옷(소데): 가죽끈 줄무늬(빨강/진홍) 위에 금 테
patch(6,12,["oyYYo","okRRo","oCCCo","okRRo","_ooo_"])
patch(16,13,["oYYGo","oRRKo","oCCCo","oRRKo","_ooo_"])
# 날개 → 등에 멘 칼: 금 코등이 + 손잡이
for (x,y,c) in [(19,10,'Y'),(18,11,'G'),(20,9,'w')]:q[x,y+TOP]=H(PAL[c])
sys.path.insert(0,__import__('os').path.dirname(__file__));import pkoutline
pkoutline.fix(im,lambda c:c[:3] in [(0x1a,0x0f,0x12),(0x31,0x31,0x31)],orig=src,oy=TOP).save(sys.argv[2])
