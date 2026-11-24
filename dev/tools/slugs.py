import json,csv,re
chs=json.load(open('/home/claude/t/chs.json'))
en={}
for row in csv.reader(open('/home/claude/brawlpokemons/dev/data/sp.csv')):
    if len(row)>=3 and row[1]=='9':en[row[0]]=row[2]
def slug(n):
    n=n.lower().replace('♀','-f').replace('♂','-m').replace('é','e').replace('. ','-').replace('.','').replace("'",'').replace(':','').replace(' ','-')
    return n
FORM={'gart':('articuno-galar',10169),'gzap':('zapdos-galar',10170),'gmolt':('moltres-galar',10171),'hlil':('lilligant-hisui',10237),'harc':('arcanine-hisui',10230),'hele':('electrode-hisui',10232),'hava':('avalugg-hisui',10243)}
out=[]
for k,i,nm,gr in chs:
    if k in ('trio','lati','steve'):continue
    if isinstance(i,int):out.append([k,i,slug(en[str(i)]),i])
    else:out.append([k,i,FORM[i][0],FORM[i][1]])
json.dump(out,open('slugs.json','w'));print(len(out));print(out[:5],[o for o in out if '-' in o[2]])
