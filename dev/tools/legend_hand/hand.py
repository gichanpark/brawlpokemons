from hp import h,mix
OLC={'mewtwo':'#0b0614','rayquaza':'#0b1d33','kyurem':'#02101c','zygarde':'#0f1724','necrozma':'#120c02','arceus':'#2a0802','calyrex':'#3a0a22','solgaleo':'#0a0c26'}
def col(T,k):
    if k=='w':return (255,255,255,255)
    if k=='Y':return h('#fde047')
    if k=='G':return h('#f59e0b')
    if k[0] in 'nps':return h(T[k[0]][int(k[1])])
    return h(k)
def stamp(e,T,art,x0,y0,M,ol,outline=True,over=True):
    pts=[]
    for j,row in enumerate(art):
        for i,ch in enumerate(row):
            if ch in '. ':continue
            x,y=x0+i,y0+j
            if not(0<=x<e.w and 0<=y<e.h):continue
            if ch=='o':e.set(x,y,h(ol));continue
            if not over and e.g(x,y)=='B':continue
            e.set(x,y,col(T,M[ch]));pts.append((x,y))
    if outline:
        S=set(pts)
        for x,y in pts:
            for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                q=(x+dx,y+dy)
                if q not in S and e.g(*q)=='T' and 0<=q[0]<e.w and 0<=q[1]<e.h:e.set(q[0],q[1],h(ol))
def line(e,c,pts):
    for x,y in pts:e.set(x,y,c)
# ---------- stamps ----------
SHARD=['..a','.ab','ab.','bc.']          # crystal shard (diagonal)
SHARD2=['a.','ab','bb','bc']
FLAME=['.a.','.a.','aba','bcb','.c.']
FLAME2=['a..','ab.','.ba','bcb']
SAKURA=['.a.','aya','.a.']
SAKURA5=['.a.a.','aaba.','.bYba','.aba.','..a..']
STAR=['.a.','aba','.a.']
MOON=['.aa.','a...','a...','.aa.']
MOON2=['.ab','a..','a..','.ab']
ICE=['.a.','.a.','aba','bcb']
ICEH=['bcb','aba','.a.','.a.']
CLOUD=['.aa..','aaaa.','abbaa','.ccc.']
CROWN=['a.a.a','abcba','.bbb.']
HEX=['.aa.','abba','.aa.']
def mewtwo_spr(e,T):
    O=OLC['mewtwo'];M={'a':'p3','b':'p2','c':'p1'}
    stamp(e,T,SHARD,0,0,M,O)          # head-back crystal
    stamp(e,T,SHARD2,0,8,M,O)         # shoulder crystal
    line(e,col(T,'p2'),[(7,11),(8,12),(9,13)]); e.set(6,8,col(T,'p3'))
def mewtwo_por(e,T):
    O=OLC['mewtwo'];M={'a':'p3','b':'p2','c':'p1'}
    stamp(e,T,['..aa','.abb','abbc','bbc.','bc..'],9,0,M,O)
    stamp(e,T,['.a','ab','bc'],28,0,M,O)
    line(e,col(T,'p2'),[(20,24),(21,25),(21,26),(22,27),(23,28),(23,29),(24,30)]);line(e,col(T,'p3'),[(18,21),(18,22)])
def rayquaza_spr(e,T):
    O=OLC['rayquaza'];M={'a':'w','b':'n3','c':'n2'}
    stamp(e,T,CLOUD,25,5,M,O);stamp(e,T,['..aa...','.aaaa.a','aaabaaa','.bcccb.'],8,21,M,O);stamp(e,T,['.aa.','abba','.cc.'],1,14,M,O)
def rayquaza_por(e,T):
    O=OLC['rayquaza'];M={'a':'w','b':'n3','c':'n2'}
    stamp(e,T,['..aaa..','.aaaaa.','aaabaaa','.bcccb.'],1,30,M,O);stamp(e,T,['.aa..','aaaa.','abbaa','.ccc.'],30,2,M,O)
def kyurem_spr(e,T):
    O=OLC['kyurem'];M={'a':'p3','b':'p2','c':'p1'}
    stamp(e,T,ICE,7,0,M,O);stamp(e,T,ICE,11,1,M,O);stamp(e,T,ICEH,2,22,M,O);stamp(e,T,ICEH,19,21,M,O)
def kyurem_por(e,T):
    O=OLC['kyurem'];M={'a':'p3','b':'p2','c':'p1'}
    stamp(e,T,['.a.','.a.','aba','bcb'],2,1,M,O);stamp(e,T,['bcb','aba','.a.','.a.'],30,33,M,O)
def zygarde_spr(e,T):
    O=OLC['zygarde'];M={'a':'p2','b':'w'}
    stamp(e,T,HEX,12,16,M,O,outline=False);stamp(e,T,HEX,4,11,M,O,outline=False)
    stamp(e,T,['a','a','b'],5,0,{'a':'p2','b':'p3'},O)
def zygarde_por(e,T):
    O=OLC['zygarde'];M={'a':'p2','b':'w'}
    stamp(e,T,['.aa.','abba','abba','.aa.'],18,30,M,O,outline=False)
def necrozma_spr(e,T):
    O=OLC['necrozma'];M={'a':'Y','b':'p2','c':'w'}
    stamp(e,T,CROWN,12,0,M,O);stamp(e,T,STAR,1,2,{'a':'p2','b':'w'},O,outline=False);stamp(e,T,STAR,23,6,{'a':'p2','b':'w'},O,outline=False)
def necrozma_por(e,T):
    O=OLC['necrozma'];M={'a':'Y','b':'p2','c':'w'}
    stamp(e,T,['a..a..a','ab.c.ba','.bbbbb.'],16,0,M,O)
def arceus_spr(e,T):
    O=OLC['arceus'];M={'a':'Y','b':'p2','c':'p1'}
    stamp(e,T,FLAME,0,0,M,O);stamp(e,T,FLAME2,8,0,M,O);stamp(e,T,FLAME,24,1,M,O);stamp(e,T,['a.','ba','cb'],14,12,M,O)
def arceus_por(e,T):
    O=OLC['arceus'];M={'a':'Y','b':'p2','c':'p1'}
    stamp(e,T,['.a.','.a.','aba','bcb','.c.'],3,0,M,O);stamp(e,T,['a..','ab.','.ba','bcb'],33,24,M,O)
def calyrex_spr(e,T):
    O=OLC['calyrex'];M={'a':'p3','y':'Y'}
    for x,y in((9,1),(15,0),(21,1),(3,7),(27,7)):stamp(e,T,SAKURA,x,y,M,O)
def calyrex_por(e,T):
    O=OLC['calyrex'];M={'a':'p3','b':'p2','Y':'Y'}
    stamp(e,T,SAKURA5,1,1,M,O);stamp(e,T,SAKURA5,30,4,M,O);stamp(e,T,SAKURA,5,33,{'a':'p3','y':'Y'},O)
def solgaleo_spr(e,T):
    O=OLC['solgaleo'];M={'a':'Y','b':'w'}
    stamp(e,T,MOON2,20,0,{'a':'Y','b':'w'},O);stamp(e,T,STAR,2,2,{'a':'s2','b':'w'},O,outline=False);stamp(e,T,STAR,31,0,{'a':'s2','b':'w'},O,outline=False)
def solgaleo_por(e,T):
    O=OLC['solgaleo']
    stamp(e,T,['..aaa..','.ab....','ab.....','ab.....','ab.....','.ab....','..aaa..'],1,1,{'a':'Y','b':'#fef3c7'},O);stamp(e,T,STAR,33,3,{'a':'Y','b':'w'},O,outline=False)
# forms reuse base hands where geometry similar: none (procedural only)
