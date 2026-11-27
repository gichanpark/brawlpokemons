import sys,pickle,json,re,io,base64
sys.path.insert(0,'/tmp/hp')
from PIL import Image
D=pickle.load(open('out.pkl','rb'));TH=json.load(open('themes.json'))
def uri(im):
    b=io.BytesIO();im.save(b,'PNG',optimize=True);return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
P='/home/claude/brawlpokemons/dev/assets/skins.js';s=open(P).read()
for k,fs in D.items():
    key=k+'_'+TH[k]['id']
    i=s.index('"%s": {'%key);j=s.index('}',i)
    old=json.loads(s[i+len('"%s": '%key):j+1])
    for f,(b,sz) in fs.items():
        assert f in old,(key,f)
        old[f]=uri(Image.frombytes('RGBA',sz,b))
    s=s[:i]+'"%s": '%key+json.dumps(old)+s[j+1:]
    print(key,list(fs))
open(P,'w').write(s)
