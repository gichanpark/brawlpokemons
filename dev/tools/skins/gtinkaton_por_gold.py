# 황금 망치 두드리짱 초상화: 망치 금색만 다시 칠하기 (빛 왼쪽 위)
# - 망치 = 노랑/주황/갈색이 4방향으로 이어진 덩어리 중 노랑·주황이 들어 있는 것만 (갈색만 있는 덩어리 = 몸 외곽선 → 그대로)
# - 각 픽셀: 위·왼쪽 가장자리까지 거리 vs 아래·오른쪽까지 거리 비율로 5단계 금색
import sys
from PIL import Image
src,dst=sys.argv[1],sys.argv[2]
im=Image.open(src).convert('RGBA');q=im.load();W,Hh=im.size
H=lambda s:tuple(int(s[i:i+2],16) for i in (1,3,5))+(255,)
hx=lambda x,y:'#%02x%02x%02x'%q[x,y][:3]
Y,O,B='#fcd34d','#e08a0b','#9a4a0a'
cand={(x,y) for x in range(W) for y in range(Hh) if hx(x,y) in (Y,O,B)}
seen=set();ham=set()
for p in cand:
    if p in seen:continue
    st=[p];comp=[]
    while st:
        c=st.pop()
        if c in seen or c not in cand:continue
        seen.add(c);comp.append(c);x,y=c;st+=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    if any(hx(*c) in (Y,O) for c in comp):ham|=set(comp)
R=['#fff6c2','#fcd34d','#f2b632','#d68c14','#9a5a0a']
def run(x,y,dx,dy):
    n=0
    while (x+dx,y+dy) in ham:x+=dx;y+=dy;n+=1
    return n
new={}
for (x,y) in ham:
    a=run(x,y,0,-1)+run(x,y,-1,0)          # 위·왼쪽(빛 쪽)까지
    b=run(x,y,0,1)+run(x,y,1,0)            # 아래·오른쪽(그늘 쪽)까지
    t=a/(a+b) if a+b else .5
    k=0 if a==0 and t<.3 else 1 if t<.35 else 2 if t<.6 else 3 if t<.85 else 4
    new[(x,y)]=R[k]
for p,c in new.items():q[p]=H(c)
im.save(dst)
