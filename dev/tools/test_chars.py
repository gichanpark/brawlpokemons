from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox']);pg=b.new_page(viewport={'width':1100,'height':560});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file://'+__import__('os').path.abspath(__import__('os').path.join(__import__('os').path.dirname(__file__),'..','..','index.html'))+'');pg.wait_for_timeout(3000)
    print(pg.evaluate("""()=>{const out=[];for(const k of ['armewtwo','mewtwo']){
      SAVE.mode='train';SAVE.sel=k;startGame(pickRoster());G.intro=0;G.tour=0;for(let j=0;j<30;j++)update(1/60);const d=G.ents.find(e=>e!==P&&e.alive);P.x=d.x-3*T;P.y=d.y;const h0=d.hp;
      const step=n=>{for(let j=0;j<n;j++)update(1/60)};
      P.ammo=3;P.cd=0;fireAttack(P,0,3*T);step(60);const h1=d.hp;P.gadCd=0;P.gadN=3;const g=useGadget(P,0,3*T);step(30);
      let sup=[];for(let i=0;i<3;i++){d.hp=d.maxHp;P.sc=1;P.inv=0;if(k==='wobbuffet'){P.recD=1000;}fireSuper(P,0,3*T);step(90);sup.push(d.maxHp-d.hp);if(!P.alive)break;}
      out.push(k+' atk'+(h0-h1)+' gad'+g+' sup'+sup.join('/')+' form'+(P.form||0)+' '+P.ch.nm+' alive'+P.alive);}
      return out.join('\\n')}"""))
    print(errs);b.close()
