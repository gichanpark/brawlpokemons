from PIL import Image
import colorsys
H=lambda s:tuple(int(s[i:i+2],16) for i in (1,3,5))+(255,)
def L(p):return colorsys.rgb_to_hls(*[v/255 for v in p[:3]])
def ramp(cols,t):
    t=max(0,min(.999,t))*(len(cols));return H(cols[int(t)])
OL=H('#120c0a')
SEA=['#123a5c','#1d5f8c','#2f86b8','#6cc3e6']     # 몸
WOOD=['#3b200c','#5b3413','#8b5a2b','#b9824a']    # 등껍질(배 나무)
ROPE=['#6b4a1f','#a37a3c','#d6b98c','#f3e4c3']
BRASS=['#5c3a06','#a16207','#eab308','#fef08a']
CREAM=['#7c6a48','#b9a578','#e7d3a8','#fff7e0']
def sprite():
    im=Image.open('n.png').convert('RGBA');w,h=im.size;px=im.load();o=im.copy();q=o.load()
    def cl(x,y):
        p=px[x,y]
        if p[3]<128:return '.'
        hh,l,s=L(p)
        if l<.2:return 'o'
        if s<.2:return 'W' if l>.85 else ('g' if l>.55 else 'd')
        Hh=hh*360
        if 190<Hh<250:return 'B'
        if 20<Hh<45 and l<.5:return 'r'
        return 'y'
    for y in range(h):
        for x in range(w):
            c=cl(x,y);p=px[x,y];l=L(p)[1]
            if c=='.':continue
            if c=='o':q[x,y]=OL;continue
            cannon=(y<=5 and x<=10) or (y<=7 and x>=16 and c in 'Wg' and y<8)
            if c=='B':q[x,y]=ramp(SEA,(l-.25)/.6)
            elif c=='y':q[x,y]=ramp(CREAM,(l-.35)/.55)
            elif cannon:q[x,y]=ramp(BRASS,(l-.25)/.7)
            elif c=='r':q[x,y]=ramp(WOOD,(l-.15)/.45) if y%2 else ramp(WOOD,(l-.25)/.45)
            elif c in 'gd' and 12<=x and y<=16:q[x,y]=ramp(ROPE,(l-.2)/.7)
            elif c in 'Wgd':q[x,y]=ramp(['#5a6470','#9aa4b0','#dde3ea','#ffffff'],(l-.2)/.8)
    P=lambda x,y,c:q.__setitem__((x,y),H(c) if isinstance(c,str) else c)
    # 나무 판자 줄무늬(등껍질 짝수 줄을 한 단계 어둡게)
    for y in range(h):
        for x in range(w):
            if cl(x,y)=='r' and y%2==0 and x%4!=1:P(x,y,WOOD[0])
    # 해골 깃발 무늬 (등껍질)
    for (x,y,c) in [(18,9,'#f8fafc'),(19,9,'#f8fafc'),(20,9,'#f8fafc'),(18,10,'#111111'),(19,10,'#f8fafc'),(20,10,'#111111'),(18,11,'#f8fafc'),(20,11,'#f8fafc'),(19,11,'#d6d3d1')]:P(x,y,c)
    # 빨간 두건 (머리 위)
    for x in range(5,10):P(x,6 if x<9 else 7,'#dc2626')
    for x in range(5,10):P(x,7,'#b91c1c')
    P(6,6,'#fff1f2');P(8,7,'#fff1f2');P(5,6,'#ef4444')
    P(10,7,'#991b1b');P(11,8,'#dc2626');P(12,9,'#991b1b')   # 두건 꼬리
    # 안대 + 끈
    P(9,10,'#0a0a0a');P(9,11,'#0a0a0a');P(8,10,'#262626');P(10,9,'#0a0a0a')
    # 대포 구멍
    P(6,1,'#1c1917');P(7,1,'#3f2a14');P(18,3,'#1c1917');P(19,3,'#1c1917')
    # 금 귀걸이
    P(4,11,'#fde047')
    # 해적 깃발 (오른쪽 대포 위)
    for y in range(0,3):P(21,y,'#5b3413')
    for (x,y) in [(22,0),(23,0),(22,1),(23,1)]:P(x,y,'#111111')
    P(22,0,'#f8fafc');P(24,0,OL);P(24,1,OL);P(22,2,OL);P(23,2,OL)
    return o
import colorsys as _c
def bgmask(im):
    px=im.load();w,h=im.size;cols=set()
    for x in range(w):
        for y in (0,h-1):cols.add(px[x,y][:3])
    for y in range(h):
        for x in (0,w-1):cols.add(px[x,y][:3])
    def isbg(c):
        hh,l,ss=colorsys.rgb_to_hls(*[v/255 for v in c]);return ss>.28 and l>.6 and .12<=hh<=.55
    cols={c for c in cols if isbg(c)}
    seen=set();st=[(x,y) for x in range(w) for y in (0,h-1)]+[(x,y) for y in range(h) for x in (0,w-1)]
    while st:
        x,y=st.pop()
        if (x,y) in seen or not(0<=x<w and 0<=y<h):continue
        if px[x,y][:3] not in cols:continue
        seen.add((x,y));st+=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    return seen
def portrait():
    im=Image.open('p.png').convert('RGBA');w,h=im.size;px=im.load();o=im.copy();q=o.load()
    pass
    BG=bgmask(im)
    for y in range(h):
        for x in range(w):
            if (x,y) in BG:continue
            p=px[x,y];hh,l,s=L(p);Hh=hh*360
            if l<.2:q[x,y]=OL;continue
            if s>=.2 and 190<Hh<250:q[x,y]=ramp(SEA,(l-.25)/.6)
            elif s>=.12 and 15<Hh<60:q[x,y]=ramp(CREAM,(l-.35)/.55)
            elif s<.12 and l>.6 and l<.95:q[x,y]=ramp(CREAM,(l-.35)/.55)
    P=lambda x,y,c:q.__setitem__((x,y),H(c)) if 0<=x<w and 0<=y<h else None
    # 삼각 해적 모자 (검정 + 금테두리 + 해골)
    hat=['....kkk...................kkk.....',
         '...kbbbk.....kkkkkkkk.....kbbbk....',
         '...kbbbbkkkkkbbbbbbbbkkkkkbbbbk....',
         '....kbbbbbbbbbbbbbbbbbbbbbbbbbk....',
         '....kbbbbbbbbbbbwwwbbbbbbbbbbk.....',
         '.....kbbbbbbbbbwkwkwbbbbbbbbk......',
         '.....kbbbbbbbbbbwwwbbbbbbbbbk......',
         '....kggggggggggbwbwbgggggggggk.....',
         '...kgyyyyyyyyyyyyyyyyyyyyyyyygk....',
         '...kkkkkkkkkkkkkkkkkkkkkkkkkkkk....']
    C={'k':'#0b0b10','b':'#1f1f2e','g':'#a16207','y':'#fde047','w':'#f8fafc'}
    for j,row in enumerate(hat):
        for i,ch in enumerate(row):
            if ch!='.':P(i+2,j-2,C[ch])
    # 모자 하이라이트
    for i in range(9,16):P(i,1,'#2e2e44')
    # 안대 (왼쪽 눈) + 끈
    for y,(x0,x1) in {10:(15,19),11:(14,20),12:(14,20),13:(15,19)}.items():
        for x in range(x0,x1+1):P(x,y,'#0a0a0a')
    P(16,11,'#3f3f46');P(17,11,'#27272a')
    for (x,y) in [(13,12),(12,12),(11,13),(10,13),(9,14),(21,10),(22,9),(23,8)]:P(x,y,'#0a0a0a')
    # 금 귀걸이
    P(6,17,'#fde047');P(6,18,'#a16207');P(5,18,'#fde047')
    return o
s=sprite();s.save('s_pirate.png');s.resize((s.width*4,s.height*4),Image.NEAREST).save('s_pirate4.png')
p=portrait();p.save('p_pirate.png')
# 미리보기
cv=Image.new('RGBA',(25*8*2+40+40*6*2+30,40*6+20),(40,44,56,255))
a=Image.open('n.png').convert('RGBA').resize((200,192),Image.NEAREST);cv.paste(a,(10,10),a)
b=s.resize((200,192),Image.NEAREST);cv.paste(b,(220,10),b)
cv.paste(Image.open('p.png').resize((240,240),Image.NEAREST),(440,10));cv.paste(p.resize((240,240),Image.NEAREST),(690,10))
cv.save('prev.png')
