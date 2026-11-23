import sys, json, time, asyncio
from playwright.async_api import async_playwright

HTML = open('/home/claude/brawlpokemons/index.html', 'rb').read()
FAKE = open('/home/claude/nt/fake.js').read()
ARGS = ['--no-sandbox', '--disable-background-timer-throttling', '--disable-renderer-backgrounding', '--disable-backgrounding-occluded-windows', '--mute-audio']

async def route(r):
    await r.fulfill(status=200, body=HTML, headers={'content-type': 'text/html; charset=utf-8'})

async def newpage(ctx, errs, tag):
    pg = await ctx.new_page()
    await pg.add_init_script(FAKE)
    pg.on('pageerror', lambda e: errs.append(f'{tag}: {e}'))
    await pg.route('http://pb.test/**', route)
    await pg.goto('http://pb.test/index.html')
    await pg.evaluate("""()=>{window._bad=[];window._cnt={a:0,s:0,g:0};for(const [fn,k] of [['fireAttack','a'],['fireSuper','s'],['useGadget','g']]){const o=window[fn];window[fn]=function(e,...r){const v=o.call(this,e,...r);if(v&&e&&e.remote)_cnt[k]++;return v;};}const oe=window.ev;window.ev=function(...a){if(['S','H','B'].includes(a[0])&&(a[1]==null||!SPECS[a[1]]))_bad.push('ev '+a[0]+' '+a[1]+' '+new Error().stack.split('\\n')[2]);return oe.apply(this,a);};
      window.applyEv=eval('('+applyEv.toString().replace('}}catch(e){}','}}catch(e){_bad.push(\\'applyEv \\'+v[0]+\\' \\'+e)}')+')');}""")
    await pg.wait_for_timeout(800)
    return pg

ACT = """async (o)=>{const R={};const me=P;if(!me)return {err:'noP'};
  const host=NET.host;
  // 적 가까이로 이동
  const en=G.ents.filter(x=>x.team!==me.team&&x.alive);
  const t=en.sort((a,b)=>Math.hypot(a.x-me.x,a.y-me.y)-Math.hypot(b.x-me.x,b.y-me.y))[0];
  R.k=me.ch.k;
  const ang=t?Math.atan2(t.y-me.y,t.x-me.x):0,d=t?Math.min(Math.hypot(t.y-me.y,t.x-me.x),(me.ch.atk.range||5)*T):3*T;
  me.ammo=3;me.cd=0;playerFire(false,ang,d);await new Promise(r=>setTimeout(r,700));
  me.sc=1;if(host)me.sc=1;playerFire(true,ang,d);await new Promise(r=>setTimeout(r,2500));
  playerGadget();await new Promise(r=>setTimeout(r,1500));
  return R;}"""

AIM = """(sup)=>{const me=P;const en=G.ents.filter(x=>x.team!==me.team&&x.alive);en.sort((a,b)=>Math.hypot(a.x-me.x,a.y-me.y)-Math.hypot(b.x-me.x,b.y-me.y));const t=en[0];
  const s=sup?me.ch.sup:me.ch.atk;const ang=t?Math.atan2(t.y-me.y,t.x-me.x):0,d=t?Math.min(Math.hypot(t.y-me.y,t.x-me.x),(s.range||5)*T):3*T;playerFire(sup,ang,d);return [me.ammo,me.sc];}"""
HC = "()=>{const c=G.ents.find(e=>e.remote);return c?{cnt:Object.assign({},_cnt),dbg:[c.cd,c.stun,!!c.dash,!!c.leap,!!c.lch,c.bq.length,c.shellT,c.digT,!!c.ebeam,G.intro,G.goalT],ammo:Math.round(c.ammo*100)/100,sc:Math.round(c.sc*100)/100,gadN:c.gadN,gadCd:Math.round((c.gadCd||0)*100)/100,alive:c.alive,form:c.form||0,x:Math.round(c.x),y:Math.round(c.y)}:null}"
HP = "()=>({ammo:Math.round(P.ammo*100)/100,sc:Math.round(P.sc*100)/100,gadN:P.gadN,gadCd:Math.round((P.gadCd||0)*100)/100})"

async def pair(ctx, k, code, out, mode='gem'):
    errs = []
    a = await newpage(ctx, errs, 'host')
    b = await newpage(ctx, errs, 'cli')
    for pg in (a, b):
        await pg.evaluate("k=>{SAVE.sel=k;}", k)
    await a.evaluate("c=>openRoom(c,true,'gem')", code)
    await a.wait_for_timeout(500)
    await b.evaluate("c=>openRoom(c,false)", code)
    await b.wait_for_timeout(2200)
    n = await a.evaluate("members().length")
    if n < 2:
        out[k] = {'err': 'join fail', 'n': n, 'errs': errs}
        await a.close(); await b.close(); return
    if mode=='ko':
        await a.evaluate("()=>{NET.kind='ko';const ms=members();const A=ms.find(m=>m.team===0),B=ms.find(m=>m.team===1)||ms.find(m=>m.id!==NET.id);const R={kind:'ko',mapId:0,blue:[{k:A.ck,lv:A.lv,owner:A.id,name:A.name}],red:[{k:B.ck,lv:B.lv,owner:B.id,name:B.name}]};bc('start',R);netStart(R);}")
    else:
        await a.evaluate("hostStart()")
    await a.wait_for_timeout(2600)
    await a.evaluate("()=>{G.intro=0;const c=G.ents.find(e=>e.remote);for(const e of G.ents){if(e.team!==c.team&&!e.owner){e.x=c.x+(e===G.ents.find(z=>z.team!==c.team&&!z.owner)?3*T:9*T);e.y=c.y;e.aiOff=1;}if(!e.owner){e.stun=1e6;}}P.x=c.x;P.y=c.y+4*T;c.ammo=3;c.sc=1;P.ammo=3;P.sc=1;}")
    await a.wait_for_timeout(900)
    R = {}
    R['c0'] = await a.evaluate(HC)
    R['cf'] = await b.evaluate(AIM, False); await a.wait_for_timeout(900); R['c1'] = await a.evaluate(HC)
    await a.wait_for_timeout(1200)
    R['c2'] = await a.evaluate(HC)
    await b.evaluate("()=>playerGadget()"); await a.wait_for_timeout(1000); R['c3'] = await a.evaluate(HC)
    await a.wait_for_timeout(1500)
    await a.evaluate("()=>{const c=G.ents.find(e=>e.remote);c.sc=1;}"); await a.wait_for_timeout(500)
    R['cs'] = await b.evaluate(AIM, True); await a.wait_for_timeout(1500); R['c4'] = await a.evaluate(HC)
    # host side
    R['h0'] = await a.evaluate(HP)
    await a.evaluate(AIM, False); await a.wait_for_timeout(1500)
    await a.evaluate("()=>playerGadget()"); await a.wait_for_timeout(1000)
    await a.evaluate("()=>{P.sc=1}"); await a.evaluate(AIM, True); await a.wait_for_timeout(1500)
    R['h1'] = await a.evaluate(HP)
    if mode=='ko':
        await a.evaluate("()=>{const c=G.ents.find(e=>e.remote);if(c.alive)kill(c,P);}")
        await a.wait_for_timeout(300)
        await a.evaluate("()=>{G.ko.next=0;koReset();G.intro=0;const c=G.ents.find(e=>e.remote);c.ammo=3;c.sc=1;}")
        await a.wait_for_timeout(1200)
        R['k0'] = await a.evaluate(HC)
        await b.evaluate(AIM, False); await a.wait_for_timeout(900); R['k1'] = await a.evaluate(HC)
        await b.evaluate("()=>playerGadget()"); await a.wait_for_timeout(1000); R['k2'] = await a.evaluate(HC)
        await b.evaluate(AIM, True); await a.wait_for_timeout(1500); R['k3'] = await a.evaluate(HC)
    R['cview'] = await b.evaluate("()=>({n:G.ents.length,alive:G.ents.filter(e=>e.alive).length,snaps:NET.snaps.length})")
    c0, c1, c2, c3, c4 = R['c0'], R['c1'], R['c2'], R['c3'], R['c4']
    prob = []
    if c1['cnt']['a'] < 1: prob.append('client atk not applied')
    if c4['cnt']['s'] < 1: prob.append('client super not applied')
    hg = R['h1']['gadN'] != R['h0']['gadN'] or R['h1']['gadCd'] > 0
    if hg and c3['cnt']['g'] < 1: prob.append('client gadget not applied')
    for pg,tg in ((a,'host'),(b,'cli')):
        bb = await pg.evaluate('()=>[...new Set(_bad)].slice(0,5)')
        if bb: prob.append(tg+' '+' | '.join(bb))
    if mode=='ko' and R.get('k0'):
        k0,k1,k2,k3=R['k0'],R['k1'],R['k2'],R['k3']
        if not k0['alive']: prob.append('ko: client not respawned')
        if k1['cnt']['a'] <= k0['cnt']['a']: prob.append('ko r2: atk not applied')
        if k3['cnt']['s'] <= k2['cnt']['s']: prob.append('ko r2: super not applied')
    R['prob'] = prob
    R['errs'] = errs[:8]
    out[k] = R
    await a.close(); await b.close()

async def main(keys, par):
    out = {}
    async with async_playwright() as p:
        br = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=ARGS)
        ctx = await br.new_context(viewport={'width': 640, 'height': 360})
        q = list(keys); i = 0
        async def worker(w):
            nonlocal i
            while q:
                k = q.pop(0); i += 1
                try:
                    await asyncio.wait_for(pair(ctx, k, 'T%03d' % i, out, MODE), 80)
                except Exception as e:
                    out[k] = {'err': str(e)[:200]}
        await asyncio.gather(*[worker(w) for w in range(par)])
        await br.close()
    return out

MODE='gem'
if __name__ == '__main__':
    MODE = sys.argv[3] if len(sys.argv) > 3 else 'gem'
    keys = sys.argv[1].split(',')
    par = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    res = asyncio.run(main(keys, par))
    json.dump(res, open('/home/claude/nt/res.json', 'w'), ensure_ascii=False, indent=1)
    for k, v in res.items():
        if v.get('prob') or v.get('errs') or v.get('err'):
            print(k, json.dumps({x: v.get(x) for x in ('prob','errs','err','c0','c1','c3','c4','k0','k1','k3')}, ensure_ascii=False)[:900])
        else: print(k, 'OK')
