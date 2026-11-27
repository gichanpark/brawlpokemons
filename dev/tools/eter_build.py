exec(open('eter2.py').read().split("res=[]")[0])
import base64,io,json,re
def uri(im):
    b=io.BytesIO();im.save(b,'PNG');return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
em=Image.open('emax.png').convert('RGBA')
out={}
for key,P,st in [('galaxy',A,['#ffffff','#fde68a','#a5f3fc','#f5d0fe']),('aurora',AU,['#ffffff','#a7f3d0']),('plat',PT,None)]:
    s=recolor(n,P);p=recolor(por,P,BG,seed=2);g=recolor(em,P,seed=5)
    if st:s=stars(s,None,3,st,.08);p=stars(p,BG,4,st,.06);g=stars(g,None,6,st,.025)
    s=s.resize((s.width*3,s.height*3),Image.NEAREST)
    out['eternatus_'+key]={'spr':uri(s),'por':uri(p),'gmax':uri(g)}
    g.save(f'et_{key}_g.png')
f='/home/claude/brawlpokemons/dev/assets/skins.js';t=open(f).read()
i=t.index('};\nconst SOCCER') if '};\nconst SOCCER' in t else t.index('};');body=t[:i];rest=t[i+2:]
for k,v in out.items():
    if '"'+k+'"' in body:continue
    body+=', '+json.dumps(k)+': '+json.dumps(v)
open(f,'w').write(body+'};'+rest)
print('ok',[k for k in out])
