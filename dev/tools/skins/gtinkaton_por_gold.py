# 황금 망치 두드리짱 초상화: 망치(금색 부분) 명암 다시 칠하기 — 빛은 왼쪽 위
# 가로로 이어진 금색 줄마다 왼쪽→오른쪽으로 밝음→그림자(원통형 손잡이 느낌), 아래 가장자리는 한 단계 어둡게
import sys
from PIL import Image
src,dst=sys.argv[1],sys.argv[2]
im=Image.open(src).convert('RGBA');q=im.load();W,Hh=im.size
H=lambda s:tuple(int(s[i:i+2],16) for i in (1,3,5))+(255,)
GOLD={'#fcd34d','#e08a0b','#9a4a0a'}
G=lambda x,y:0<=x<W and 0<=y<Hh and '#%02x%02x%02x'%q[x,y][:3] in GOLD
R=['#fff3b0','#fcd34d','#f0b429','#d48a12','#9a5a0a']   # 밝음 → 그림자
mask=[[G(x,y) for y in range(Hh)] for x in range(W)]
out={}
for y in range(Hh):
    x=0
    while x<W:
        if not mask[x][y]:x+=1;continue
        x0=x
        while x<W and mask[x][y]:x+=1
        n=x-x0
        for i in range(n):
            t=(i+.5)/n
            k=0 if (i==0 and n>=3) else 1 if t<.4 else 2 if t<.7 else 3
            if n<=2:k=1 if i==0 else 2
            if not(y+1<Hh and mask[x0+i][y+1]):k=min(4,k+1)        # 아래 가장자리
            if not(y>0 and mask[x0+i][y-1]) and k>0:k-=1             # 위 가장자리(빛 받음)
            out[(x0+i,y)]=R[k]
for (x,y),c in out.items():q[x,y]=H(c)
im.save(dst)
