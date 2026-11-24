import json,os,subprocess,io,base64
from PIL import Image
exec(open('mk.py').read().split("SP={};PO={};rep=[]")[0])  # reuse ld/dec/enc/pairmap/apply + S,R,SPR,POR
L=[['rayquaza_mega','mega384','rayquaza-mega'],['cinderace_gmax','gmax815','cinderace-gmax'],['eternatus_gmax','emax890','eternatus-eternamax'],['kyurem_f1','10022','kyurem-black'],['kyurem_f2','10023','kyurem-white'],['morpeko_f1','morpeko_h','morpeko-hangry'],['zygarde','zy10','zygarde-10'],['minior_f1','10136','minior-red'],['deoxys_f1','10001','deoxys-attack'],['deoxys_f2','10002','deoxys-defense'],['deoxys_f3','10003','deoxys-speed'],['palafin_f1','pal1',None],['calyrex_f1','cxice','calyrex-ice-rider'],['calyrex_f2','cxsh','calyrex-shadow-rider'],['enamorus_f1','10249','enamorus-therian'],['giratina_f1','10007','giratina-origin'],['necrozma_f1','10155','necrozma-dusk-mane'],['necrozma_f2','10156','necrozma-dawn-wings'],['necrozma_f3','10157','necrozma-ultra'],['zygarde_f1','718','zygarde'],['zygarde_f2','zy100','zygarde-complete'],['ogerpon_f1','og1',None],['ogerpon_f2','og2',None],['ogerpon_f3','og3',None],['aegislash_f1','10026','aegislash-blade'],['darmanitan_f1','10017','darmanitan-zen']]
base={k:(i,slug,aid) for k,i,slug,aid in S}
def get(url,path):
    if os.path.exists(path):return True
    r=subprocess.run(['curl','-sfL','-o',path,url]);ok=r.returncode==0 and os.path.exists(path) and os.path.getsize(path)>100
    if not ok and os.path.exists(path):os.remove(path)
    return ok
out={};rep=[]
for key,sid,fslug in L:
    k=key.split('_')[0]
    if k not in base or str(sid) not in SPR:rep.append((key,'skip'));continue
    M=None;src='base'
    if fslug:
        b='https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/'
        if get(b+'regular/'+fslug+'.png',f'src/F_{key}_n.png') and get(b+'shiny/'+fslug+'.png',f'src/F_{key}_s.png'):
            M=pairmap(Image.open(f'src/F_{key}_n.png'),Image.open(f'src/F_{key}_s.png'));src='form'
    if M is None:
        r=R[k]
        M=pairmap(Image.open(f'src/{k}_n.png'),Image.open(f'src/{k}_s.png')) if r.get('ps') else pairmap(Image.open(f'src/{k}_an.png'),Image.open(f'src/{k}_as.png'),q=8)
    out[key]=enc(apply(dec(SPR[str(sid)]),M,70 if src=='form' or R[k].get('ps') else 45));rep.append((key,src))
json.dump(out,open('forms.json','w'));print(rep)
