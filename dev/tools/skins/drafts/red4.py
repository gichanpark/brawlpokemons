# 시즌 1(붉은색) 트로피 마켓 스킨 초안 4종 — 원본 해상도, 부위를 테마로 바꿈, 빛 왼쪽 위, 포켓몬 외곽선
# 사용: red4.py <원본 png 폴더> → r4_<키>.png
import sys,os
from PIL import Image
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));import pkoutline
D=sys.argv[1];H=lambda s:tuple(int(s[i:i+2],16) for i in (1,3,5))+(255,);hx=lambda p:'#%02x%02x%02x'%p[:3]
def make(k,M,stamps=(),pad=(0,0,0,0),region=None):
    src=Image.open(f'{D}/{k}.png').convert('RGBA');L,T,Rr,B=pad
    im=Image.new('RGBA',(src.width+L+Rr,src.height+T+B));im.paste(src,(L,T));q=im.load()
    for y in range(src.height):
        for x in range(src.width):
            p=src.getpixel((x,y))
            if p[3]<128:continue
            c=hx(p);n=(region(x,y,c) if region else None) or M.get(c)
            if n:q[x+L,y+T]=H(n)
    for x,y,c in stamps:
        X,Y=x+L,y+T
        if 0<=X<im.width and 0<=Y<im.height:q[X,Y]=H(c)
    out=pkoutline.fix(im,lambda c:c[:3] in [(0x31,0x31,0x31),(0x21,0x21,0x21),(0x14,0x10,0x18)],orig=src,oy=T)
    return out
O='#313131'
# 1 진홍 닌자 개굴닌자 (이로치=검은 몸이라 겹치지 않게): 남색 몸 → 진홍 닌자복, 혀 목도리 → 검은 목도리, 머리 줄무늬 → 금 이마 보호대, 검은 띠 매듭이 뒤로 날림
g=make('greninja',{'#4263ad':'#c42a3a','#314a8c':'#7d1424','#52d6ef':'#f5c542','#f78c9c':'#4a4054','#ad4a5a':'#241e2c','#948c52':'#241e2c','#c5bd6b':'#4a4054'},
  stamps=[(19,2,'#4a4054'),(20,1,'#4a4054'),(21,1,'#241e2c'),(20,2,O),(21,0,O),(22,1,O),(22,2,O),(19,1,O),(18,0,O),(21,2,O),(11,2,'#fff1a8')],pad=(0,0,1,0))
g.save(f'{D}/r4_ninja.png')
# 2 홍룡 한카리아스: 청보라 몸 → 진홍 비늘, 빨간 배 → 금빛 배(비늘 줄), 노란 지느러미 → 금
c=make('garchomp',{'#7b84f7':'#e0414a','#6363ce':'#a51f2e','#525252':'#5c0c18','#ffe63a':'#f5c542','#bdb59c':'#c9a227','#ff6b4a':'#f8dc9a','#ff9c3a':'#e8b04a'},
  region=lambda x,y,c:('#c9963a' if c=='#ff6b4a' and y%2==1 else None))
c.save(f'{D}/r4_dragon.png')
# 3 진홍 드레스 가디안: 흰 드레스 → 진홍 드레스(주름은 진한 단계), 밑단 흰 레이스, 가슴 뿔 → 금, 머리에 장미
gd=make('gardevoir',{'#e65273':'#f5c542','#944263':'#b0841a'},
  region=lambda x,y,c:(None if y<12 else ('#fdf2f8' if c=='#ffffff' and y>=20 and x%2==0 else {'#ffffff':'#d42a3a','#bdbdce':'#8e1028','#ced6ef':'#f26a6a','#7b7b7b':'#5c0c18'}.get(c))),   # 얼굴(12줄 위)은 흰색 그대로
  stamps=[(10,2,'#e0313f'),(11,2,'#ff6b6b'),(12,2,'#e0313f'),(10,3,'#8e1028'),(11,3,'#e0313f'),(12,3,'#8e1028'),(11,1,'#ff9aa2')])
gd.save(f'{D}/r4_rose.png')
# 4 흑염 리자몽: 주황 몸 → 검붉은 비늘, 크림 배 → 불씨 빨강, 날개 안쪽 → 진홍, 꼬리 불꽃 → 검은 불꽃 + 붉은 심지
def flame(x,y,c):
    if x>=22 and y<=9:return {'#ff5a3a':'#2a0a10','#f79429':'#5c0c18','#ffe629':'#ff3b4a'}.get(c)
ch=make('charizard',{'#f79429':'#c4303c','#d66342':'#8e1f2c','#b5423a':'#5c1420','#f7d673':'#ffb08a','#d6b563':'#e0704a','#316b5a':'#3a1018','#4a8473':'#6e1824','#ff5a3a':'#c4303c','#ffe629':'#ff8a6a'},region=flame,
  stamps=[(14,8,'#ff6b4a'),(18,12,'#ff6b4a'),(9,14,'#c43a48')])
ch.save(f'{D}/r4_blackflame.png')
