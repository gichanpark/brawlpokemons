# 육군 아미 타이거 어흥염 — 원본 23x24 도트를 2배(46x48)로 키운 뒤 군복·전투모·군화·태극기 패치를 손도트로 찍음
# 사용: python3 incineroar_army.py <n.png 23x24 원본> <p.png 40x40 초상화> <출력폴더>
import sys,colorsys
from PIL import Image
H=lambda s:tuple(int(s[i:i+2],16) for i in (1,3,5))+(255,)
OL=H('#141410')
OLV=['#38451f','#55672f','#748842','#94a85a']   # 올리브 기본
DKG=['#121808','#1c2610','#283518','#354522']   # 진한 녹색 얼룩
BRN=['#3a2612','#56381a','#714b24','#8c6132']   # 갈색 얼룩
KHK=['#7d7250','#a39566','#c4b682','#e0d3a0']   # 카키 얼룩
BLK=['#0e0e0e','#1d1d1d','#2e2e2e','#454545']   # 군화
BELT=['#2a2a18','#3a3a22','#4d4d2d','#606038']
lum=lambda p:colorsys.rgb_to_hls(*[v/255 for v in p[:3]])[1]
def rp(R,t):t=max(0,min(.999,t));return H(R[int(t*len(R))])
# 위장 얼룩(손으로 배치): (x,y,가로,세로,색) — 46x48 격자 기준
BLOBS=[(14,24,5,3,DKG),(20,26,4,2,BRN),(25,24,3,3,KHK),(16,29,4,2,KHK),(23,30,5,2,DKG),(13,31,3,2,BRN),
       (28,28,3,2,BRN),(19,33,3,2,DKG),(26,33,4,2,KHK),(15,39,4,2,DKG),(21,40,3,2,BRN),(27,39,3,3,KHK),
       (14,42,3,2,KHK),(25,42,4,2,DKG),(2,24,3,2,DKG),(5,27,3,2,BRN),(1,28,2,2,KHK),(31,26,3,2,DKG),
       (34,29,3,2,KHK),(37,32,3,2,BRN),(33,34,3,2,DKG),(36,37,2,2,KHK),(39,30,2,2,DKG),(17,36,0,0,DKG),(13,37,3,2,DKG),(28,36,3,2,BRN),(18,44,0,0,KHK),(4,22,2,2,BRN),(41,34,2,2,KHK),(30,31,3,2,KHK),(17,21,0,0,KHK)]
def camo(x,y,l):
    for bx,by,bw,bh,R in BLOBS:
        # 모서리를 깎은 둥근 얼룩
        if bx<=x<bx+bw and by<=y<by+bh and not ((x in(bx,bx+bw-1)) and (y in(by,by+bh-1)) and bw>2 and bh>2):
            return rp(R,(l-.12)/.55)
    return rp(OLV,(l-.12)/.55)
def sprite(src):
    a=Image.open(src).convert('RGBA');bp=a.load();W,Hh=46,48
    o=a.resize((W,Hh),Image.NEAREST);q=o.load()
    def region(bx,by):
        if by>=19:return 'leg'
        if 17<=by<=18 and 7<=bx<=15:return 'belt'
        if by>=12 and 7<=bx<=14:return 'torso'
        if by>=11 and bx<=6:return 'arm'
        if by>=12 and bx>=15:return 'arm'
        return 'head'
    for y in range(Hh):
        for x in range(W):
            bx,by=x//2,y//2;p=bp[bx,by]
            if p[3]<128:continue
            if p[:3]==(0x21,0x21,0x21):q[x,y]=OL;continue
            rg=region(bx,by);l=lum(p)
            if p[:3]==(0xff,0xff,0xff) and rg in('torso','head'):continue   # 이빨·수염 그대로
            if rg=='torso' or rg=='arm':q[x,y]=camo(x,y,l)
            elif rg=='belt':q[x,y]=rp(BELT,(l-.2)/.6)
            elif rg=='leg':q[x,y]=rp(BLK,(l-.1)/.6) if by>=21 else camo(x,y,l)
    P=lambda x,y,c:q.__setitem__((x,y),H(c)) if 0<=x<W and 0<=y<Hh else None
    # 전투모 (머리 위): 챙 + 위장무늬 + 계급장
    cap={2:(15,22),3:(13,25),4:(11,27),5:(10,28),6:(10,28),7:(9,29)}
    for y,(x0,x1) in cap.items():
        for x in range(x0,x1+1):P(x,y,'#141410' if x in(x0,x1) or y==2 else ('#5d6b38' if (x+y)%7 else '#364425'))
    for x in range(13,17):P(x,4,'#364425')
    for x in range(20,24):P(x,5,'#5f4729')
    for x in range(8,31):P(x,8,'#141410')
    for x in range(9,30):P(x,9,'#2c3519' if x<29 else '#141410')
    P(8,9,'#141410');P(30,8,'#141410')
    # 계급장(검은 바탕 금 줄 — 병장)
    for y in range(4,8):P(19,y,'#0e0e0e');P(20,y,'#0e0e0e')
    P(19,4,'#facc15');P(20,4,'#facc15');P(19,6,'#facc15');P(20,6,'#facc15')
    # 셔츠 단추·주머니
    for y in (26,30,34):P(21,y,'#1c2412')
    for x in range(15,19):P(x,27,'#28331a')
    for x in range(24,28):P(x,27,'#28331a')
    # 인식표 줄 + 군번줄
    for (x,y) in [(17,24),(18,25),(19,26),(25,24),(24,25),(23,26)]:P(x,y,'#cbd5e1')
    P(20,27,'#e2e8f0');P(21,27,'#94a3b8');P(20,28,'#94a3b8');P(22,27,'#e2e8f0')
    # 버클
    for (x,y) in [(19,35),(20,35),(21,35),(22,35),(19,36),(22,36),(19,37),(20,37),(21,37),(22,37)]:P(x,y,'#d4a017')
    P(20,36,'#3a3a22');P(21,36,'#fde68a')
    # 태극기 패치 (오른팔)
    for x in range(34,38):P(x,27,'#f8fafc');P(x,30,'#f8fafc')
    P(34,28,'#f8fafc');P(37,28,'#f8fafc');P(34,29,'#f8fafc');P(37,29,'#f8fafc')
    P(35,28,'#dc2626');P(36,28,'#dc2626');P(35,29,'#1d4ed8');P(36,29,'#1d4ed8')
    for x in range(33,39):P(x,26,'#141410');P(x,31,'#141410')
    for y in range(26,32):P(33,y,'#141410');P(38,y,'#141410')
    # 군화 끈
    for (x,y) in [(16,43),(17,44),(26,43),(27,44)]:P(x,y,'#6b7280')
    return o
def portrait(src):
    a=Image.open(src).convert('RGBA');o=a.copy();q=o.load();px=a.load();W=40
    P=lambda x,y,c:q.__setitem__((x,y),H(c)) if 0<=x<W and 0<=y<W else None
    # 가슴(회색) → 위장 군복
    for y in range(24,40):
        for x in range(W):
            p=px[x,y];h,l,s=colorsys.rgb_to_hls(*[v/255 for v in p[:3]])
            if s<.12 and .3<l<.7 and y>=26:
                c=OLV
                for bx,by,bw,bh,R in [(6,30,6,3,DKG),(15,28,5,3,BRN),(24,31,6,3,KHK),(10,35,5,3,KHK),(20,35,6,3,DKG),(30,34,4,3,BRN),(2,36,4,3,BRN),(33,28,4,3,DKG)]:
                    if bx<=x<bx+bw and by<=y<by+bh:c=R
                q[x,y]=rp(c,(l-.2)/.5)
    # 옷깃 (V자)
    for i in range(6):P(14+i,26+i,'#141410');P(26-i,26+i,'#141410');P(15+i,26+i,'#7d8a4e');P(25-i,26+i,'#7d8a4e')
    # 태극기 패치
    for x in range(30,35):
        for y in range(33,37):P(x,y,'#f8fafc')
    P(31,34,'#dc2626');P(32,34,'#dc2626');P(33,34,'#dc2626');P(31,35,'#1d4ed8');P(32,35,'#1d4ed8');P(33,35,'#1d4ed8')
    P(30,33,'#141410');P(34,33,'#141410');P(30,36,'#141410');P(34,36,'#141410')
    # 전투모
    rows={1:(12,27),2:(10,29),3:(9,30),4:(8,31),5:(8,31),6:(7,32)}
    for y,(x0,x1) in rows.items():
        for x in range(x0,x1+1):
            P(x,y,'#141410' if x in (x0,x1) or y==1 else ('#5d6b38' if (x*3+y*5)%11 else ('#364425' if x%2 else '#5f4729')))
    for x in range(6,34):P(x,7,'#141410')
    for x in range(5,35):P(x,8,'#2c3519')
    for x in range(4,36):P(x,9,'#141410')
    for (x,y,w,c) in [(11,3,3,'#364425'),(23,4,3,'#5f4729'),(16,5,2,'#7a7255'),(27,2,2,'#364425')]:
        for i in range(w):P(x+i,y,c)
    for y in range(2,7):P(19,y,'#0e0e0e');P(20,y,'#0e0e0e')
    P(19,3,'#facc15');P(20,3,'#facc15');P(19,5,'#facc15');P(20,5,'#facc15')
    return o
s=sprite(sys.argv[1]);p=portrait(sys.argv[2]);d=sys.argv[3]
s.save(d+'/s_army.png');p.save(d+'/p_army.png')
cv=Image.new('RGBA',(46*6+40*6+30,48*6+10),(40,44,56,255))
cv.paste(s.resize((276,288),Image.NEAREST),(5,5),s.resize((276,288),Image.NEAREST));cv.paste(p.resize((240,240),Image.NEAREST),(295,5))
cv.save(d+'/prev.png')
