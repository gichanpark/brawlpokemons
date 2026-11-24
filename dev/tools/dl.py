import json,os,subprocess,concurrent.futures as cf
S=json.load(open('slugs.json'))
os.makedirs('src',exist_ok=True)
def get(url,path):
    if os.path.exists(path)and os.path.getsize(path)>100:return True
    r=subprocess.run(['curl','-sfL','-o',path,url]);ok=r.returncode==0 and os.path.exists(path) and os.path.getsize(path)>100
    if not ok and os.path.exists(path):os.remove(path)
    return ok
def job(x):
    k,i,slug,aid=x;res={}
    base='https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/'
    res['ps']=get(base+'regular/'+slug+'.png',f'src/{k}_n.png') and get(base+'shiny/'+slug+'.png',f'src/{k}_s.png')
    if not res['ps']:
        a='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/'
        res['art']=get(a+f'{aid}.png',f'src/{k}_an.png') and get(a+f'shiny/{aid}.png',f'src/{k}_as.png')
    if isinstance(i,int):
        res['pmd']=get(f'https://raw.githubusercontent.com/PMDCollab/SpriteCollab/master/portrait/{i:04d}/0000/0001/Normal.png',f'src/{k}_ps.png')
    return k,res
with cf.ThreadPoolExecutor(12) as ex:
    R=dict(ex.map(job,S))
json.dump(R,open('dl.json','w'))
print(sum(1 for v in R.values() if v.get('ps')),'pokesprite;',sum(1 for v in R.values() if v.get('art')),'art;',sum(1 for v in R.values() if v.get('pmd')),'pmd shiny portraits')
print('none:',[k for k,v in R.items() if not v.get('ps') and not v.get('art')])
