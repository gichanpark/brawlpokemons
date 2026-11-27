import re,base64,io,json,colorsys,math,sys
sys.path.insert(0,'/tmp/lg')
from PIL import Image
R='/home/claude/brawlpokemons/'
ic=open(R+'dev/assets/icons.js').read();pc=open(R+'dev/assets/por.js').read()
def get(src,k):
    m=re.search(r'"%s":\s*"data:image/png;base64,([^"]+)"'%re.escape(k),src);return Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGBA') if m else None
def scale_of(im):
    for s in (6,5,4,3,2):
        if im.width%s or im.height%s:continue
        n=im.resize((im.width//s,im.height//s),Image.NEAREST)
        if list(n.resize(im.size,Image.NEAREST).getdata())==list(im.getdata()):return s,n
    return 1,im
