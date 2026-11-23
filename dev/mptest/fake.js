// 테스트용: Supabase realtime을 BroadcastChannel로 흉내 (두 탭 사이 친선전 동기화 점검)
(()=>{function mkCh(name,cfg){const bc=new BroadcastChannel('f-'+name);const key=cfg&&cfg.config&&cfg.config.presence&&cfg.config.presence.key;const H=[];const pres={};
 const fire=()=>H.filter(h=>h.type==='presence').forEach(h=>{try{h.cb()}catch(e){console.error(e)}});
 const ch={on(type,f,cb){H.push({type,ev:f&&f.event,cb});return ch;},
  send(m){try{bc.postMessage({k:'b',event:m.event,payload:JSON.parse(JSON.stringify(m.payload))});}catch(e){}return Promise.resolve('ok');},
  subscribe(cb){setTimeout(()=>{cb&&cb('SUBSCRIBED');try{bc.postMessage({k:'hello'});}catch(e){}},30);return ch;},
  track(meta){if(key){pres[key]=[meta];bc.postMessage({k:'p',key,meta});fire();}return Promise.resolve('ok');},
  untrack(){return Promise.resolve();},presenceState(){return pres;},unsubscribe(){try{bc.close()}catch(e){}return Promise.resolve();}};
 bc.onmessage=({data})=>{if(data.k==='b')H.filter(h=>h.type==='broadcast'&&h.ev===data.event).forEach(h=>h.cb({payload:data.payload}));
  else if(data.k==='p'){pres[data.key]=[data.meta];fire();}else if(data.k==='hello'&&key&&pres[key])bc.postMessage({k:'p',key,meta:pres[key][0]});};
 return ch;}
window.supabase={createClient(){return {channel:mkCh,removeChannel(c){try{c.unsubscribe()}catch(e){}}};}};})();
// 백그라운드 탭에서도 게임 루프가 돌도록 rAF 대체
window.requestAnimationFrame=cb=>setTimeout(()=>cb(performance.now()),16);
