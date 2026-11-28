# 포켓몬 도트 외곽선 규칙: 바깥 외곽선 = 원본과 같은 #313131, 안쪽 구분선 = 검정 대신 그 부위 색의 가장 어두운 단계
from collections import Counter
OUT=(0x31,0x31,0x31,255)
def darker(c):
    r,g,b=c[:3];return (int(r*.55),int(g*.55),int(b*.55),255)
def fix(im,dark_like=lambda c:sum(c[:3])<110,orig=None,oy=0):
    # orig: 원본 스프라이트(위 여백 oy). 원본에 원래 있던 안쪽 선은 그대로 둠(포켓몬 원작 선)
    q=im.load();W,H=im.size;ch=[];op=orig.load() if orig else None
    keep=lambda x,y: op is not None and 0<=x<orig.width and 0<=y-oy<orig.height and op[x,y-oy][3]>128 and op[x,y-oy][:3]==(0x31,0x31,0x31)
    for y in range(H):
        for x in range(W):
            p=q[x,y]
            if p[3]<128 or not dark_like(p):continue
            nb=[q[x+dx,y+dy] if 0<=x+dx<W and 0<=y+dy<H else (0,0,0,0) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))]
            if any(n[3]<128 for n in nb):ch.append((x,y,OUT));continue          # 바깥 → 원본 외곽선색
            if keep(x,y):ch.append((x,y,OUT));continue
            cols=[n for n in nb if not dark_like(n)]
            if cols:ch.append((x,y,darker(Counter(cols).most_common(1)[0][0])))   # 안쪽 → 주변 색의 어두운 단계
    for x,y,c in ch:q[x,y]=c
    return im
