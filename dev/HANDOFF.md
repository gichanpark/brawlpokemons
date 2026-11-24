# 브롤포켓몬즈 개발 인수인계 (새 세션용)

새 세션에서 이 저장소(`gichanpark/brawlpokemons`)를 연결하고 **이 파일부터 읽으면** 이어서 작업할 수 있어요.

## 1. 한눈에 보기
- 브롤스타즈풍 포켓몬 대전 HTML 게임. 한 파일(`index.html`)로 동작.
- 배포: GitHub Pages → https://gichanpark.github.io/brawlpokemons/
- 백엔드: Supabase 프로젝트 `fidocivflebjwpjndlue` (계정·저장·우편·공지·친구·랭킹·1대1 내기). 멀티는 Supabase Realtime 채널.
- 관리자 계정: `outislove`
- 현재 버전: **v1.20.10** (소스의 `const VER='...'`)

## 2. 파일 구조
```
index.html            ← 빌드 결과물 (배포되는 파일). 직접 고치지 말 것
dev/game.src.html     ← 실제 소스. 여기만 고침
dev/build.py          ← 소스 + assets 를 합쳐 index.html 생성
dev/assets/           ← icons.js(SPR 박스 스프라이트), por.js(POR 미스터리던전 초상화),
                        tiles.js, balls.js, font.b64(게임 폰트), *.uri(아이콘), gfont.ttf(배너용 폰트)
dev/data/             ← PokeAPI CSV (move_names.csv, sp.csv=종 이름, abil.csv). 한국어=local_language_id 3, 영어=9
dev/tools/            ← test_chars.py(캐릭터 공격/가젯/궁 자동 테스트), banner.py(패치노트 배너 예시)
notice/               ← 패치노트 배너 이미지 (공지 img 컬럼에 URL로 연결)
```
빌드: `python3 dev/build.py` (저장소 루트에서) → `index.html` 갱신.
JS 문법 검사: index.html 의 `<script>` 들을 뽑아 `node --check`.

## 3. 작업 규칙 (사용자 요청 사항)
- **한국어로 짧고 간결하게** 답할 것. 사용자는 **색약** → 빨강/초록만으로 구분하지 말 것.
- 수정할 때마다: 빌드 → 테스트 → GitHub 커밋·푸시 → **HTML 파일을 사용자에게 전달**.
- **버전 규칙**: 캐릭터 추가 = 가운데 숫자(+0.1.0), 오류 수정·작은 변경 = 마지막 숫자. 사용자가 "버전 올리지 마"라고 하면 그대로 둠.
- **패치노트**: 캐릭터 추가 등 큰 업데이트 때 `pb_notice` 에 직접 insert (author=`outislove`).
  - 제목 `[vX.Y.Z] ...`, 끝에 등급별 마릿수 + `ps. 신 캐릭터 요청은 supoioqus@gmail.com 로 해주세요`
  - 가로로 긴 배너(1200×380): 가운데 제목, 양옆에 새 포켓몬 실루엣 → `notice/vXXX.png` 로 커밋, img 컬럼에 Pages URL.
  - 잉어킹 비밀 챌린지 관련은 패치노트 금지. 스티브(한정 스페셜)는 패치노트·마릿수에서 제외.
- 포켓몬·기술 이름은 **공식 한국어 이름**만 (dev/data CSV로 확인). 지역폼은 "가라르/히스이" 접두어 붙이지 않음.
- DB 데이터·테스트 계정 삭제는 사용자 확인 후에만. 비밀값 커밋 금지.

## 4. 소스 구조 핵심 (dev/game.src.html)
- `CH=[...]` 캐릭터 목록: `{k,id,nm,fnm,role,el,gr,col,hp,spd,rl,charge,atk:{...},sup:{...}}`
  - gr: r 희귀 / s 초희귀 / e 영웅 / m 신화 / l 전설 / sp 스페셜(뽑기 불가, 미보유 시 선택창 숨김)
  - el 은 `EL` 키만 사용 (fight, ice, ghost … — 'fighting' 아님!)
  - 플래그: `noble:1`(히스이 주인, 배지), `horse:1`(왕의 애마, 배지), `rface:1`(스프라이트가 오른쪽을 봄)
- 특성/가젯 설명: `TRG={k:{t:[이름,설명],g:[이름,설명]}}` — **모든 CH에 필요**
- 가젯 동작: `useGadget` 의 `switch(k)`, AI 가젯: 같은 이름의 AI switch. `GADN(k)` 99 = 무제한.
- 폼 시스템: `FORMS={k:[폼배열]}`, 폼 배열은 `SPECS=[]` 등록줄(`CH.concat(XXF.slice(1),...)`)에도 추가. 폼 스프라이트는 `IMG[k+'_f'+form]` 매핑 리스트, 초상화는 `formPor`.
- 세트 캐릭터 일반화: `SETX` (볼트로스 3마리, 라티 2마리) — trioSet/trioNext/trioSave.
- 피해 배율: `dmgOut(src)`, `dmgIn(src,tgt,dot)`. 히트 효과: `hitEff`. 상태 타이머: `TIMERS` 배열.
- 네트워크 스냅샷: 엔티티 배열 인덱스 a[0..33] (폼, 세트 HP, 다이브, 스티브 제작대 등), 플래그 비트(…131072 헤롱헤롱, 262144 보호막).
- 저장: `save()` → localStorage + 서버 `pb_save`(rev 버전 체크로 오래된 창 덮어쓰기 방지, `adoptServer`가 병합).
- 특수 캐릭터: 스티브(채굴·제작대·핫바 UI `drawSteveUI`), 기라티나(그림자·섀도다이브), 버드렉스(`calyMount`, `CXF`), 아르세우스(`nobleN`), 러브로스(헤롱헤롱 `loveT`).

## 5. Supabase
- pb_notice.hidden=true 면 공지 목록에서 숨김
- 테이블: pb_pick(판마다 고른 캐릭터 기록 — `endMatch`에서 pb_pick_log, 관리자 메뉴 '캐릭터 사용률'에서 pb_pick_stats), pb_stock_co(주식 종목·뉴스 문구), pb_stock_px(1분 틱 시세, 5일 보관), pb_users, pb_mail(+bc_id, until), pb_mail_bc(전체 배포 기간), pb_notice(+img), pb_notice_cmt, pb_friend, pb_invite, pb_duel, pb_secret
- 함수: pb_stock(p_n) — 호출 시 밀린 1분 틱을 서버에서 생성(랜덤워크+평균회귀+뉴스 — 뉴스는 그 틱에 뜨고 효과는 pb_stock_co.pend/pend_n 으로 다음 4분에 나눠 반영) 후 최근 시세 반환, pb_signup/login/session/me/save/ping/logout, pb_mail_list/claim/claim_all, pb_admin_* (mail[p_days 수령기간], notice, code, tro, take, ban, act, list), pb_notice_*, pb_friend_*, pb_invite*, pb_duel_*, pb_rank, pb_profile, pb_code_check, pb_tot
- 클라이언트는 anon 키로 RPC만 호출 (모든 함수 security definer, 토큰 검사).

## 6. 에셋 출처
- 박스 스프라이트: pokesprite gen8 regular (`raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/<이름>.png`), bbox 자른 뒤 ×3 (gen7 아이콘은 ×4)
- 초상화: PMDCollab SpriteCollab `portrait/XXXX[/000N]/Normal.png`
- 공식 아트(배너 실루엣): PokeAPI `sprites/pokemon/other/official-artwork/<id>.png`
- 스티브 관련 마인크래프트 아이콘: minecraft.wiki `Special:FilePath/Invicon_<이름>.png`, 휩쓸기 `Sweep_(texture_N)_JE3.png`
- icons.js / por.js 는 JSON 맵 → 파이썬으로 load → 키 추가 → dump.

## 7. 테스트
- Playwright + `/usr/bin/google-chrome` (헤드리스). `dev/tools/test_chars.py` 의 `for(const k of [...])` 목록을 바꿔 실행하면 캐릭터별 평타/가젯/궁 피해가 출력됨.
- 훈련장에서 `SAVE.mode='train';SAVE.sel='<k>';startGame(pickRoster())` 후 `update(1/60)` 반복으로 시뮬레이션.

## 8. 최근 작업 이력 (요약)
v1.9 라티아스·라티오스/기라티나 → v1.10 가방(인벤토리)·선택권·스티브(한정) → v1.11 러브로스 → v1.12 히스이 주인 4종+아르세우스, 선택창 정렬, 아군 봇(멀티 방·혼자 팀전·로비 양옆 AI 파티), 기간제 파워 9 고정 → v1.13 버드렉스·블리자포스·레이스포스, 우편 수령 기간(전체 배포는 기간 내 신규 가입자도 수령)
v1.14 패러독스 6마리(고대활성: 체력 50%↑ / 쿼크차지: 필살기 후 6초, `PDXB`), 가젯 횟수 버그 수정, 휘두르기 도트 아트(`ARTI`), 선택창 스크롤 바(`scrollBar`), 슬롯머신(`slotOpen`/`slotOdds` — 많이 걸수록 잭팟↑, 전설 선택권은 금구슬 1000개어치 이상 베팅 시만, 이 기준은 화면에 표시하지 말 것) → v1.15 포켓증권(`stockOpen`, 보유 `SAVE.stk={SYM:{n,c}}`, 공매도 `SAVE.sht={SYM:{n,c,liq,t,ck}}` — 담보로 잠긴 매도대금, +50% 오르면 반대매매 `stLiq`, 혜성조각 음수면 신용불량 → `openShop` 차단), 캔들 차트, 내 주식 탭

## 9. 추가 규칙
- 그림(이펙트·아이콘·배너)은 모두 도트(픽셀) 느낌으로.
- 답변은 항상 한국어로.
- **현재 슬롯머신·포켓증권은 숨김 상태** (`const SHOW_GAMBLE=false`). 사용자가 다시 추가하라고 하면 true로 바꾸면 됨 (공매도 반대매매 백그라운드 검사도 같이 멈춰 있음).
- v1.15.0 공지(pb_notice id 17)는 hidden=true 로 숨김. 슬롯·주식 다시 켤 때 같이 false 로.
- v1.15.7: 빠르모트·토게데마루·마릴리·바우첼·야돈 삭제(보유자 없었음). 부스터(열기 `heat`)·블래키(낙인 `markT`)·아머까오(미러아머·택시)·이븐곰(껴안기 `carryT`)·리피아(부쉬 게이지) 고유 능력 추가.
- 랭킹 이름 숨김: v1.19.3에서 해제 (pb_rank hide=false 고정). 다시 숨기려면 pb_rank의 hide 식을 되살리면 됨.
- 설정의 AI 닉네임 순화 모드(SAVE.clean): 켜면 봇 이름이 CLEAN_VERB+포켓몬이름, 주식 전광판 동네 소식도 빠짐.
- 새로 회원가입하는 계정은 순화 모드가 기본으로 켜짐 (applyAccount에서 nick이 있을 때 SAVE.clean=true). 기존 계정은 꺼진 상태 유지.
- v1.16.0 무한다이노(전설) 추가. 판매 안 하기로 해서 v1.16.1부터 일반 전설처럼 획득 가능. (`paid:1` 플래그를 달면 상자·스카우트·선택권·봇에서 빠지는 기능은 남아 있음)
- 밸런스: v1.16.3부터 자동 등급 보정 없음. `BAL_FIX`(v1.15.5 기준 배율 고정 표)만 적용. 새 캐릭터는 CH에 적은 수치 그대로 쓰임.

## v1.16.16 스티브 자원 사용처
- 돌 블록: 핫바 6번 칸(PC 6) → `steveBlock(e)`. 타일 4 재사용 + `G.map.stn[idx]=1`(Uint8Array, 지연 생성), HP `STONE_HP=1500`, 1인 최대 `STONE_MAX=6`(`e.blks` FIFO). 이벤트 `ev('SB',i)` 설치 / `ev('W',i)` 제거. `hitBox` 파괴 시 이제 `ev('W')`도 보냄(기존 상자 동기화 누락 수정). 돌 블록은 큐브 드롭 없음, AI 상자 타깃에서 제외. 원격 입력 `p.s===5`.
- 도구 4개 완성 후 제작칸 → `CRAFT2`(방패 e.sblk=3 / 황금사과 / 날카로움 e.sharp dmgOut×1.2 / TNT sc+50%). `steveCraftT`가 allTools면 `steveCraft2`. 방패 판정 `steveShield(p,e)`(투사체 명중 직전, 바라보는 방향 `steveFace` 기준 ±70°). 사망 시 sblk·sharp 초기화. 스냅샷 a[33][7]=sblk, [8]=sharp.
- ORE_PACK에서 돌 압축 제거.
- v1.16.17: 다이아 과잉 → 광물 가중치 돌47·철28·금20(다이아 5%), ORE_PACK 철10·금8 (분당 다이아 약 19.5→6.5개)
- v1.16.18: 제작대 옮기기 `steveMoveTab(e)` (제작대에서 멀 때 핫바 1번 아래 칸 / PC 7, 쿨 10초 `e.ctabT`, 원격 p.s===6)
- v1.16.19: 황금사과 보관 `e.gapN`(최대 3, 사망해도 유지) → `steveEat(e)` (돌 블록 칸 아래 버튼 / PC 8, 1초 간격, 원격 p.s===7, 스냅샷 a[33][9])
- v1.16.20: 스티브 도구·방패를 손 위치(중심 ±18, 발밑 -16, bob 반영)에 정확히 배치. 날카로움 인챈트 시 도구·핫바 아이콘에 보라색 픽셀 글린트(`glintImg`/`drawGlint`) + 반짝이
- v1.16.21: 스티브 처치 시 모든 광물 +1 (`kdCount`, 더미 제외)
- v1.16.22: 광물 확률 전부 25%, 채굴 6~7개(같은 광물 최대 2개), 다이아 압축 제거(ORE_PACK=[]), 처치 보상 +2
- v1.16.23: 다이아 사용처 추가 — CRAFT2[0] 보호 인챈트(다이아2, e.prot dmgIn×0.85), CRAFT2[5] 효율 인챈트(다이아1+철1, e.eff 채굴 0.8초/쿨 1.2초). 제작칸이 슬롯 0~5 전부 사용, 황금사과 먹기 버튼은 핫바 왼쪽으로 이동. 스냅샷 a[33][10]=prot,[11]=eff
- v1.16.24: 활 화살 = 마크 위키 Invicon_Arrow (fx 'mcarrow', MCI.arrow), 채굴 시 돌은 1회당 2개
- v1.16.25: 따라큐 평타 → 치근거리기(키트식 달라붙기). atk.latch → `startLatch/latchTick/endLatch`, `e.lt` 상태(호스트에서 진행), 8연타×280 · 0.2초 간격 · 둔화. 플래그 1<<27(=e.ltOn) 먼지구름 연출
- v1.16.26: 따라큐 평타는 섀도클로로 복구, 필살기를 치근거리기(latch)로 교체(길동무 제거). 10연타×500, 2초, 사거리 6.5
- v1.16.28 친선전 전수 점검(119종, 팀전·1대1 KO 2라운드): `dev/mptest/mp.py` (Supabase를 BroadcastChannel로 흉내 내는 fake.js + 두 탭). 사용: `python3 dev/mptest/mp.py <키,...> <병렬수> [gem|ko]`
  - 수정: 바위 파편 스펙(shardSpec)이 호스트에서만 런타임 생성돼 SPECS 번호가 어긋남 → 시작 시 미리 생성 / 따라큐 필살기 스펙 _id 유실 / 따라큐 달라붙기 상태명 e.lt가 참가자 보간 타이머와 충돌 → e.lch / 사망 시 무한다이빔·달라붙기·채굴 정리 / KO 라운드 리셋 때 진행 중인 빔·대기열·대시·TNT 정리
  - 남는 '실패'는 상태 조건 때문(거리 내 적 필요, 껍질·땅굴·잠 중 필살기 불가, 메타몽 변신 대상 없음)이라 정상
- v1.16.29: 교대형 너프 — 삼신(trio) 한 마리 체력 ×0.6, 라티 ×0.85 (TRF/LTF hp 직접 조정), 대기 회복 4%/초 → 1.5%/초
- v1.17.0: 영웅·신화·전설 40종 평타/필살기에 원작 기술 효과 부여 (`// 영웅·신화·전설 기술 특색` 블록, U(k,'atk'|'sup',플래그,설명추가) — 같은 이름의 폼 스펙도 함께 수정). 능력치는 그대로.
  - 새 플래그: sleepBonus, gyro, rageFist(e.hitsTaken), firstImp(e.fiArm), bigBonus, thru(벽 통과, 이전엔 미구현), dashInv, refund, selfStun(e.recoil→stun), healPct(buff), 돌진 접촉 exec/ls/vulnC. 메타그로스도 recD 누적(counter).
- v1.18.0: 초희귀 솔록(338) 추가 — 불꽃세례(화상) / 솔라빔(`windup` 0.6초 충전 후 발사, bq 사용·충전 중 태양 링 연출) / 특성 부유(swim)·태양의 힘(화상 적 +20%, dmgIn) / 가젯 쾌청(게이지 30%+빨라짐). 배너 notice/v1180.png
- v1.19.0 '태암이 오다': 전설 솔가레오(791) — 사이코팽(shieldBreak: 보호막·리플렉터·철벽 제거 시 1.3배) / 메테오드라이브(돌진, 벽 파괴·기절·방어 무시) / 메탈프로텍트(hitEff 래퍼 → hitEff0, 둔화·방어/공격 하락·혼란 무효) / 아침햇살. 배너 notice/v1190.png
  - 버그 수정: v1.17.0에서 fireSuper의 refund/selfStun 줄이 dash if와 else-if 사슬 사이에 끼어, 돌진형 필살기가 투사체까지 쏘고(2배 피해) 갸라도스·개굴닌자 필살기가 안 나가던 문제. 돌진 접촉에 stun 적용 추가. 갑주무사 평타 firstImp 중복 제거(특성에 이미 있음)
- v1.19.1: 부서진 지형 잔해 — `G.map.rub[i]`(1 벽·2 상자·3 돌 블록) → `drawRubble`(바닥 위 도트 조각, 타일 위치로 고정 난수). breakTile/hitBox/스티브 블록 제거/참가자 'W' 이벤트에서 `setRub`, 돌 블록을 놓으면 지움
- v1.19.2: 시즌 1등 '트로피 성좌' 프레임(.fr-star) 도트 리디자인 — 금테 9-slice border-image(모서리 보석), 위에 1등 트로피, 반짝이 2프레임 교대, 금빛 drop-shadow 맥동 (이미지는 CSS data URI)
- v1.19.3: 랭킹 이름 공개, 랭킹 1~3등 줄에 금·은·동 테두리·빛 줄기·도트 반짝이 + 숫자 메달(.rk.r1~r3)
- v1.19.4: 11/30 랭킹 1위 이벤트 상품 문구를 '특별 프레임 + 한정 포켓몬'으로 변경 (로딩 화면 #ldEv, 랭킹 #rkEv)
- v1.19.5: 랭킹 접속 중 표시 — pb_rank 가 o(last_seen 30초 이내, 핑은 7초마다)를 보냄 → 이름 옆 초록 도트(.rk .on)
- v1.19.6: 지형 파괴 타격감 — setRub에서 `crumble`(G.crumb) 호출: 나무는 번쩍 후 맞은 반대쪽으로 쓰러지며 착지 먼지·흔들림, 상자·돌은 흔들리다 터짐, 파편(중력)·나뭇잎 파티클, 'crash' 효과음
- v1.19.7: 모바일 랭킹 창(모달)에서 1~3등 줄이 납작하게 찌그러지던 문제 — .rk 에 flex:none·min-height 38px
- v1.20.0 이로치 스킨: dev/assets/shiny.js (`SPRS`/`PORS`, 포켓몬 키별, 118종 — 볼트로스·라티·스티브 제외). 만든 방법: pokesprite regular↔shiny(없으면 공식 아트 일반↔이로치) 픽셀 대응으로 색 지도를 만들어 게임 스프라이트·초상화에 적용, 초상화는 PMDCollab 이로치(portrait/XXXX/0000/0001)가 있으면 그대로 사용 (/tmp 스크립트 → 재생성 시 같은 방식)
  - SAVE.shy(보유 배열), SAVE.sk({k:1} 장착). hasShy/skinOn/sprOf/porOf/entImg. 상자 칸마다 이로치 확률 BOXT.s(1~3%) → dropShy(보유 포켓몬 중 미보유 이로치). 선택창 상세에 스킨 버튼, 카드에 ✦
  - 멀티: myMeta.sk → 로스터 sk → e.skin. 봇은 nid·맵 해시로 1/33 확률(모든 화면 같음)
- v1.20.1 테마 스킨: dev/assets/skins.js (`SKINX['k_id']={spr,por,gmax}`, `SOCCER` 축구공 도트). `THEMES={cinderace:[spurs 토트넘 에이스번, korea 국가대표 에이스번]}` (색만 바꾼 도트, ball:1 → 평타·필살기 투사체가 축구공, 거다이맥스도 축구공 무늬). 보유 SAVE.skn, 장착 SAVE.sk[k]='s'|테마id (예전 1=이로치). skinId/hasSkin/gmaxImg/ballSkin. 상자 스킨 드롭은 이로치+테마 통합(dropShy)
- v1.20.2: 에이스번 테마 스킨 거다이맥스 불덩이를 직접 찍은 도트 축구공(구 음영·오각형 무늬, 정이십면체 투영)으로 교체, 투사체 공도 같은 방식. 생성 스크립트 dev/tools/skin_ball_gmax.py · skin_ball_small.py (skins.js 백업본 기준으로 실행)
- v1.20.3: 관리자 우편으로 스킨 지급 — 아이템 키 `sk_<포켓몬>_<s|테마id>`(ITEMS에 자동 등록, 관리자 아이템 목록에서는 숨김), 받으면 invAdd에서 바로 SAVE.shy/skn 에 추가. 관리자 패널 '스킨' 줄: 포켓몬·스킨 고르고 추가 → 보내기
- v1.20.4: 에이스번 테마 스킨 가슴에 등번호 7 (토트넘 네이비 / 국가대표 흰색) — skins.js spr 직접 수정(원본 1/3 해상도 x7~9, y23~26)
- v1.20.5: 기라티나 그림자 부활 — kill에서 e.deadAt 기록, 기라티나(메타몽 제외)가 적을 쓰러뜨리면 `giraRevive`: 5초 안에 쓰러진 아군(가장 최근) 1명을 적이 쓰러진 자리에서 체력 50%로 부활, e.shadowRv(스냅샷 플래그 1<<28) → 보라 그림자 필터 + 도트 연기. 다음에 쓰러지면 해제
- v1.20.6: 백귀야행 기라티나 스킨(THEMES.giratina yako, skins.js spr·f1·por) — 칠흑+은빛+진홍. 테마 fx → SPECS에 스펙 복제(SKMAP, skSpec: spawnShots·fireSuper 에서 교체, palO로 pal() 덮어씀), 보라 하드코딩 색은 YK 표로 진홍 치환(yc/ycl: 섀도볼·영혼·섀도다이브·오리진 변신·가젯·화면 틴트 G.purpC). 폼 스킨 이미지 formImg. 스킨 공지 배너 notice/v1206.png (dev/tools/banner_v1206.py)
- v1.20.7: 드레디어 '동백꽃 필 무렵' 스킨(THEMES.hlil dongbaek) — 흰 한복+검은 가지(등 뒤에서 뻗음)+노란 꽃, 캔버스 46x44 블록(×3). fx: palO 노랑, edge(리프블레이드 테두리 검정)+petal(노란 꽃잎 파티클, 승리의춤 때 꽃비). 생성 dev/tools/skin_hlil_dongbaek.py
- v1.20.8: 스킨 필살기 때 스킨 이름 문구 제거 (동백꽃 필 무렵, 백귀야행 오리진폼 문구는 원래 문구로)
- v1.20.9: 모바일 랭킹 창(모달)에서 줄을 눌러도 프로필이 안 열리던 문제 — 모달 안 .rk 에도 openPlayer 연결
- v1.20.10: 폼 체인지 포켓몬 이로치 — shiny.js 에 SPRSF(k_fN, k_gmax, k_mega; pokesprite 폼 짝 또는 기본 색 지도) 추가, formImg/megaImg/gmaxImg 가 이로치면 IMGSF 사용. 지가르데 기본(10%) 이로치도 zy10 기준으로 교체. 생성: /tmp 스크립트(forms.py) 방식 — 볼트로스·라티는 여전히 제외
