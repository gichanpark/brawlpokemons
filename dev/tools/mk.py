import json,base64,io,os
from PIL import Image
from collections import Counter,defaultdict
S=json.load(open('slugs.json'));R=json.load(open('dl.json'))
def ld(f,pre):
    raw=open('/home/claude/brawlpokemons/dev/assets/'+f).read();return json.loads(raw[len(pre):].rstrip().rstrip(';'))
SPR=ld('icons.js','const SPR=');POR=ld('por.js','const POR=')
def dec(u):return Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGBA')
def enc(im):b=io.BytesIO();im.save(b,'PNG');return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
def pairmap(n,s,q=0):
    n=n.convert('RGBA');s=s.convert('RGBA')
    if n.size!=s.size:s=s.resize(n.size,Image.NEAREST)
    M=defaultdict(Counter)
    for a,b in zip(n.getdata(),s.getdata()):
        if a[3]<250 or b[3]<250:continue
        ka=a[:3] if not q else tuple(v//q*q for v in a[:3])
        M[ka][b[:3]]+=1
    out={}
    for k,c in M.items():
        if q:
            tot=sum(c.values());out[k]=tuple(int(sum(col[i]*w for col,w in c.items())/tot) for i in range(3))
        else:out[k]=c.most_common(1)[0][0]
    return out
def apply(im,M,tol=70):
    keys=list(M.keys());cache={};o=im.copy();px=o.load()
    for y in range(o.height):
        for x in range(o.width):
            r,g,b,a=px[x,y]
            if a==0:continue
            c=(r,g,b)
            if c not in cache:
                if c in M:cache[c]=M[c]
                else:
                    best=min(keys,key=lambda k:(k[0]-r)**2+(k[1]-g)**2+(k[2]-b)**2);dd=((best[0]-r)**2+(best[1]-g)**2+(best[2]-b)**2)**.5
                    if dd<tol:
                        s=M[best];cache[c]=tuple(max(0,min(255,s[i]+(c[i]-best[i]))) for i in range(3))
                    else:cache[c]=c
            px[x,y]=cache[c]+(a,)
    return o
SP={};PO={};rep=[]
for k,i,slug,aid in S:
    r=R[k]
    if r.get('ps'):M=pairmap(Image.open(f'src/{k}_n.png'),Image.open(f'src/{k}_s.png'));tol=70
    else:M=pairmap(Image.open(f'src/{k}_an.png'),Image.open(f'src/{k}_as.png'),q=8);tol=45
    sp=dec(SPR[str(i)]);ss=apply(sp,M,tol);SP[k]=enc(ss)
    if r.get('pmd'):
        ps=Image.open(f'src/{k}_ps.png').convert('RGBA');pn=dec(POR[str(i)])
        if ps.size!=pn.size:ps=apply(pn,M,tol)
        PO[k]=enc(ps)
    elif str(i) in POR:PO[k]=enc(apply(dec(POR[str(i)]),M,tol))
    diff=sum(1 for a,b in zip(sp.getdata(),ss.getdata()) if a!=b)/max(1,sum(1 for a in sp.getdata() if a[3]>0))
    rep.append((k,round(diff,2)))
open('/home/claude/brawlpokemons/dev/assets/shiny.js','w').write('const SPRS='+json.dumps(SP)+';const PORS='+json.dumps(PO)+';')
print(len(SP),len(PO));print(sorted(rep,key=lambda x:x[1])[:15])
