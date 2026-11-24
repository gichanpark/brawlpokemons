# 브롤포켓몬즈 개발 인수인계 (새 세션용)

새 세션에서 이 저장소(`gichanpark/brawlpokemons`)를 연결하고 **이 파일부터 읽으면** 이어서 작업할 수 있어요.

## 1. 한눈에 보기
- 브롤스타즈풍 포켓몬 대전 HTML 게임. 한 파일(`index.html`)로 동작.
- 배포: GitHub Pages → https://gichanpark.github.io/brawlpokemons/
- 백엔드: Supabase 프로젝트 `fidocivflebjwpjndlue` (계정·저장·우편·공지·친구·랭킹·1대1 내기). 멀티는 Supabase Realtime 채널.
- 관리자 계정: `outislove`
- 현재 버전: **v1.19.1** (소스의 `const VER='...'`)

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
- 랭킹 이름 숨김: pb_rank 가 2026-12-01 0시(KST) 전까지 본인·관리자 외 이름(u,n)을 null로 보냄 → 그 이후 자동 공개.
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
