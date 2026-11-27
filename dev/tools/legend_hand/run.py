import sys;sys.path.insert(0,'/tmp/hp')
from hp import *
FORMS={'kyurem':{'f1':'10022','f2':'10023'},'zygarde':{'base':'zy10','f1':'718','f2':'zy100'},'necrozma':{'f1':'10155','f2':'10156','f3':'10157'},'calyrex':{'f1':'cxice','f2':'cxsh'},'rayquaza':{'mega':'mega384'}}
IDS={'mewtwo':'150','rayquaza':'384','kyurem':'646','zygarde':'718','necrozma':'800','arceus':'493','calyrex':'898','solgaleo':'791'}
try:HAND=__import__('hand')
except Exception as ex:print('nohand',ex);HAND=None
def make(k,key,form,por=False):
    T=TH[k];orig=get(pc if por else ic,key)
    s,n=(1,orig) if por else scale_of(orig)
    BGM=bgmask(n) if por else set()
    C=classify(n,BGM);im=recolor(n,T,por);e=Ed(im,C,T)
    if not por:
        shade(e,OL[k]);MOT[k](e,T,form)
    else:
        for (x,y),v in C.items():
            if v=='O':im.load()[x,y]=h(OL[k])
    if HAND:
        f=getattr(HAND,k+('_por' if por else '_'+form),None)
        if f:f(e,T)
    return im,s,recolor(n,T,por)
if __name__=='__main__':
    out={};prev=[]
    for k in TH:
        T=TH[k];fm=FORMS.get(k,{});base=fm.get('base',IDS[k])
        a,s,a0=make(k,base,'spr');p,_,p0=make(k,IDS[k],'por',True)
        prev.append((k,a,a0,p,p0))
        e={'spr':a.resize((a.width*s,a.height*s),Image.NEAREST),'por':p}
        for f,sk in fm.items():
            if f=='base':continue
            b,s2,_=make(k,sk,f);e[f]=b.resize((b.width*s2,b.height*s2),Image.NEAREST)
        out[k]=e
    import pickle;pickle.dump({k:{f:(im.tobytes(),im.size) for f,im in v.items()} for k,v in out.items()},open('out.pkl','wb'))
    for k,a,a0,p,p0 in prev:
        Z=8;W=max(a.width*Z*2+40,0)
        cv=Image.new('RGBA',(a.width*Z*2+30+p.width*4*2+30,max(a.height*Z,p.height*4)+20),(40,44,56,255))
        cv.paste(a0.resize((a.width*Z,a.height*Z),Image.NEAREST),(10,10),a0.resize((a.width*Z,a.height*Z),Image.NEAREST))
        A=a.resize((a.width*Z,a.height*Z),Image.NEAREST);cv.paste(A,(a.width*Z+20,10),A)
        x0=a.width*Z*2+30;cv.paste(p0.resize((160,160),Image.NEAREST),(x0,10));cv.paste(p.resize((160,160),Image.NEAREST),(x0+170,10))
        cv.save('cmp_'+k+'.png')
