# 브롤포켓몬즈 개발 인수인계 (새 세션용)

새 세션에서 이 저장소(`gichanpark/brawlpokemons`)를 연결하고 **이 파일부터 읽으면** 이어서 작업할 수 있어요.

## 1. 한눈에 보기
- 브롤스타즈풍 포켓몬 대전 HTML 게임. 한 파일(`index.html`)로 동작.
- 배포: GitHub Pages → https://gichanpark.github.io/brawlpokemons/
- 백엔드: Supabase 프로젝트 `fidocivflebjwpjndlue` (계정·저장·우편·공지·친구·랭킹·1대1 내기). 멀티는 Supabase Realtime 채널.
- 관리자 계정: `outislove`
- 현재 버전: **v1.21.22** (소스의 `const VER='...'`) · 2026-11-27 기준

## 1-1. 최근 상태 요약 (v1.21.x, 2026-11-27)
- **포켓증권(주식)**: 서버 시세(pb_stock*). 금구슬주 8 + 혜성조각주 6. 10분마다 가격 결정(매수·매도 금액/인원 + 노이즈 + 뉴스 + 기본가치 회귀), 조롤컴퍼니는 사인파(kind='sine'). 상점 '투자' 섹션과 로비 '주식' 버튼에서 열림(`stockOpen`). 자세한 건 아래 v1.21.16~20 항목.
  - 종목을 지우거나 통화를 바꾸기 전에 **반드시 `pb_stock_hold` 보유자 확인** (v1.21.18에 보유자 있는 종목을 지웠다가 복구한 적 있음). `execute_sql`은 여러 문장이면 **마지막 결과만** 돌려주니 확인 쿼리는 따로 실행.
  - pb_stock에 `cur` 컬럼이 있으니 plpgsql 변수명으로 `cur` 쓰지 말 것.
- **선물(pb_gift2)**: 재화 + 가방 아이템 + 스킨. 서버가 보내는 사람 세이브에서 차감.
- **조롤패스**: 관리자 우편으로 pass_paid(프리미엄), pass_xp(+100) 지급 가능(ADMK 목록).
- **브롤볼**: 골 세리머니·킥오프·연장전·공 들고 골인·공 잡으면 화면 테두리 파란빛.
- **아머드 뮤츠**(크로마틱): 상향 + 강한 유도(spec `homeT`, 목표 고정).
- **스킨 규칙**: 색만 바꾸는 필터 금지 → 도트를 직접 찍을 것(`dev/tools/legend_hand/`, `dev/tools/skins/blastoise_pirate.py` 참고). 패스 보상 스킨은 테마에 `pass:1` (상자 드롭 제외).
- **삭제한 계정**: 영구정지 복사 계정 19개 삭제(사용자 승인). 기간정지 3개(asdf, joyongsibal, parkjunho)는 남김.
- 남은 아이디어(사용자 결정 대기): 아머드 뮤츠 이벤트 확장(갑옷 파괴·보스전·해방 스킨 등), 지우개굴닌자/챔피언 두드리짱 출시, 세이브 봉인 strict 전환.

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
- 이미지·이펙트·배너는 전부 **도트(픽셀)** 느낌으로. 아머드 뮤츠 기술명은 코드명 그대로(E8YS92RM 등).
- 분류기가 막으면 이유 설명하고 사용자에게 물어볼 것.

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
- 그림(이펙트·아이콘·배너)은 모두 도트(픽셀) 느낌으로. **스킨·도트 그리기 전에 dev/PIXEL_GUIDE.md 를 먼저 읽을 것.**
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

## v1.20.11
- 관통(thru) 투사체도 상자(타일4) 피해 (아르세우스 쇼다운 큐브 버그)
- 쇼다운: 상자 후보칸 중 절반만 생성, 사망 시 큐브 round(n/2) 드랍
- 신규 맵: 보석(섬과 섬/덤불 미로/돌벽 회랑), 녹아웃(물웅덩이 결투장/기둥 숲), 쇼다운 테마(얼음 호수/미로 숲/탁 트인 평원)

## v1.20.12
- 봇 피해 보정(botMul) 제거 → 봇 피해 항상 100% (난이도는 err/react/fg/supP만)
- 길찾기 개선: walkGoal(벽/물 목표→가까운 빈칸), fNext + 경로 당기기(시야 되는 먼 칸까지 직선), 이동 벡터가 벽 향하면 필드 벡터로 대체, 금고 우회, 끼임 탈출을 진행방향 수직으로
- 측정(봇 벽 끼임 초, 5모드×6판×45초): 164s → 75s

## v1.20.13
- 트로피 로드 제거 → **조롤패스** (PASS_N=60, 단계당 100xp, 시즌 PASS_SEASON=1). SAVE.pass={s,xp,f,p,paid} (f/p = 받은 칸 '0/1' 문자열)
  - 경험치: 팀전 승40/무25/패20, 쇼다운 순위별 40~15, 60단계 이후 100마다 금구슬 100
  - 무료: 1 피카츄 / 3·9 스타팅 / 6 잠만보 / 12 루가루암 (이미 있으면 금구슬 100), 15 영웅 선택권, 30 마스터볼+30, 45 하이퍼볼×2+50, 60 조롤패스 프레임+1000
  - 프리미엄(2,900원 표기만, 결제 없음): 1 백귀야행 기라티나 스킨, 15 랜덤 스킨+마스터볼, 30 신화 선택권, 45 랜덤 스킨+100, 60 전설 선택권+황금 조롤패스 프레임
  - 관리자 우편 아이템 `pass_paid` = 프리미엄 열기, `fr_jpass`/`fr_jpassg` 프레임
  - ROAD 상수/SAVE.road 는 남아 있으나 사용 안 함
- 크로마틱 등급 GRADE.cr (LTD(g) = sp|cr → 뽑기·스카우트·상자·보석 해금 제외, 이벤트/관리자 지급만)
- 미출시 변형 에셋: dev/assets/variants/ (아머드뮤츠·지우개굴닌자 = 크로마틱 예정, 챔피언 두드리짱 = 황금망치). 컨셉은 사용자가 따로 알려줄 예정

## v1.20.14
- 로비 왼쪽 아래 큰 조롤패스 버튼(.lb-pass: Lv·경험치 막대·받을 보상 배지), 로고는 위로, 조작 도움말 숨김, 사이드 패스 버튼·트로피 아래 막대 제거
- 조롤패스 퀘스트: 매일 3개(QPOOL, 날짜+닉 해시로 고정), 전부 깨면 +100. SAVE.pass.q={d,L:[[id,진행]],b}. 끝난 판에서 questTick → 패스 경험치에 더함. 추적: G.pDmg(내가 준 피해), G.pSup(필살기), P.kills
- 보상 인상(인플레이션 대응): 판 보상 금구슬 ×5(승150/무80/패50, 쇼다운 200~20), 혜성조각 승리 6, 무료 선물 200~500(+혜성 8~15), 상자 금구슬 ×4·혜성 ×3, 패스 금구슬 ×5·혜성 ×4, 중복 포켓몬 500
- 가격: 몬스터볼 상자 120→400, 파워 업 비용 레벨×25→×100, 금구슬 교환 750/4500

## v1.20.15
- 친구 선물: RPC `pb_gift(token,to,c,g,msg)` — 친구(또는 30분 안 친선전 상대)에게만, 하루 10번(pb_gift_log), 서버 저장에서 차감+rev 증가 후 받는 쪽 우편. 클라는 flushSave() 후 호출, 성공 시 로컬 차감+rev 맞춤. 친구 목록 '선물' 버튼(giftOpen)
- 친선전 판돈으로 상대가 재화 0이 되면 승자에게 '후원하기' 창: `pb_broke(token,duel_id)` 2.5초 간격 3번 확인 → sponsorAsk
- 궁극 선택권 sel7_u / sel_u (g:'u', 스페셜·크로마틱 제외 전부, GRX 로 이름·색)
- (v1.20.20 에서 상점 티켓 섹션 숨김, 가격표는 되팔기·회수용으로 유지) 슬롯머신 공개(SHOW_SLOT, 포켓증권은 계속 숨김)
- 슬롯: 꽝으로 두 재화 모두 0 → 마지막 베팅 75% 반올림 환급 + SAVE.slotBan=1 (영구 출입 금지)
- 물가: 스카우트 10000, 상자 600금/40/90/180 혜성, 보석 해금 400~5000, 금구슬 교환 600/3500

## v1.20.16
- 가방 되팔기: sellP(k)=상점가(선택권·티켓은 tk 항목, 상자 티켓은 상자값)의 40%, 같은 재화. sellItem → 1개/전부 팔기. 상점에 값이 없는 아이템(프레임·스킨 등)은 팔기 버튼 없음

## v1.20.17
- 정지 기간: pb_users.ban_until, `pb_admin_ban(token,user,msg,p_hours)` (0=영구). 기간 지나면 pb_login 에서 자동 해제. 로그인 거절 시 'until'(ms) 반환 → 남은 기간 표시. 관리자 목록에 '정지 · N일 남음/영구'

## v1.20.18
- 정지 즉시 반영: pb_admin_ban 이 ban_token 에 마지막 토큰 저장 → pb_ping(p_token,p_ver) 가 banned 정보 반환 → banKick (로그아웃 + 정지 안내)
- 강제 업데이트: pb_cfg('ver'). 관리자가 새 버전으로 접속해 ping 하면 자동 갱신 → 낮은 버전 클라는 판 밖에서 '새 버전' 안내 후 4초 뒤 새로고침 (verCheck)
- 몰수에 가방 추가: pb_take_apply(u,c,g,pks,items jsonb,vals jsonb,msg) 공용 — 서버 저장에서 아이템 빼고, 모자라면 vals(상점가) 만큼 재화 차감. take_items 컬럼 → pb_save 'ti' / login·session note 'i' → 클라 takeItemsLocal 같은 규칙 ('@k' = 기간제 포켓몬, 스킨·프레임·패스도 회수)
- 전체우편 회수: pb_admin_bc_list / pb_admin_recall(token, created_at, msg, vals). 안 받은 우편 삭제 + pb_mail_bc 삭제, 받은 사람은 pb_take_apply. 이제 전체 발송은 항상 pb_mail_bc 기록(until null 허용)
- 되팔기 25%

## v1.20.19
- 무한다이노 패스 전용 스킨 3종 (THEMES.eternatus: galaxy 은하수 / aurora 오로라 / plat 백금, pass:1 → 상자 드롭 제외). SKINX 에 spr·por·gmax(무한다이맥스) 추가. 생성: dev/tools/eter*.py (색 분류 리컬러 + 성운 노이즈 + 별)
- 무한다이빔 색: EBP[skin] 팔레트로 빔·링·섬광 교체
- 조롤패스: 프리미엄 30 = 신화 선택권 + 황금 조롤패스 프레임, 60 = 무한다이노 스킨 3개 중 택1(pick 보상 → passPickUI, 모두 받기에서는 건너뜀) + 전설 선택권
- 무한다이노 너프: 체력 5000→4500, 다이맥스포 1050→880·사거리 7.5→7·체력비례 최대 1.5→1.3배, 무한다이빔 2.5→2초·피해 3900→3300·범위 1.8→1.6·끌어당김 2.4→1.9·무적 → 받는 피해 50% 감소

## v1.20.21
- 상자 열기 연출 강화: BXFX(캔버스 반해상도 도트 파티클 — burst/ring/rain(이미지)/suck/rise). 3단계 흔들림(가장 좋은 보상 색으로 힌트: 새 포켓몬 등급색·스킨 무지개·파워 초록) → 볼이 위아래로 쪼개지며 폭발. 금구슬/혜성조각 비, 파워 화살표, 새 포켓몬 실루엣은 빛 빨아들임 → 등급색 폭발·빛기둥, 신화·전설은 2차 폭발+별비, 스킨은 무지개

## v1.20.22
- AI 성격(aiPersona, PERSONA): 보통 40 / 상남자형 20(붙어 싸움 pref .45, 12%까지 안 도망, 추적 1.6배, 필살기 자주, 조준 약간 나쁨) / 쫄보형 20(최대 사거리 .95, 55%면 도망, 추적 .8배, 필살기 덜 씀) / 잘하는형 20(조준 오차 ×.55, 반응 빠름, 좌우 무빙 강함, 약한 적 집중, 맞힐 만할 때만 필살기). 결과 화면 이름 앞에 [상남자]/[쫄보]/[고수] 표시
- 시뮬(쇼다운·젬 8판) 봇당 킬/데스: 고수 1.9/1.1, 상남자 1.2/2.1, 쫄보 0.5/1.3, 보통 1.9/1.3

## v1.20.23
- 성격 태그 숨김(psTag → '', 원본은 psTag0)
- 성격 추가: 숨숨형(가까운 부쉬에 숨어 매복, aiBush), 수집가형(아이템 22칸까지 찾아감·덜 싸움), 복수형(마지막으로 때린 적 12초 추적, damage에서 ai.rev 기록), 팀플형(팀전만, 체력 낮은 아군 따라다님), 똘끼형(가끔 엉뚱하게 이동, 필살기 막 씀, 도망 기준 랜덤)
- 가중치: 보통25 상남자12 쫄보12 고수12 숨숨10 수집가10 복수7 팀플7 똘끼5

## v1.20.24
- 랭킹 프레임 정리: 아바타 34px·테두리 3px 통일, 무지개/물결/도트/은하수/하이퍼볼 프레임은 :after(안쪽 배경) 유지 → 무늬가 사진 뒤를 덮던 문제 해결, 바깥 무늬 inset -3px, 나뭇잎·이로치·성좌 장식은 랭킹에서 숨김
- .fr-master:after 안쪽 배경 추가(전역), 1~3위 반짝임 띠가 글자·아바타 위를 덮지 않게 .rk>* z-index:1, 접속 점 없는 줄도 자리 확보(.on.off)

## v1.20.25
- 이벤트: 조롤 로또. 로비 왼쪽 노란 '이벤트' 버튼(#bEvent) → openLotto
  - DB: pb_lotto_round(draw_at, nums, carry, pot, drawn, res), pb_lotto_ticket(round_id, username, nums, hit, prize)
  - pb_lotto_tick(): 추첨 시간 지난 회차 추첨(1~20 중 3개 랜덤) → 3개 60%/2개 30%/1개 10% 맞힌 사람끼리 나눔(우편 '조롤 로또'), 당첨자 없는 몫은 다음 회차 carry. 다음 회차 = 다음 월요일 10:00 KST(pb_lotto_next_draw). pb_ping·pb_lotto_info 에서 호출(lazy)
  - pb_lotto_buy(token, nums[3]): 5000 금구슬 서버 차감+rev, 회차당 10장
- 키 작은 화면(H<=470, .lowh)은 로비 로고 숨김

## v1.20.26
- 일괄 정지: 관리자 목록 체크박스(관리자 계정은 선택 불가) + 전체 선택 + '선택 정지'(banForm 배열 → pb_admin_ban_many, 기간·편지 공통) / '선택 정지 해제'(pb_admin_unban_many)

## v1.20.27
- 관리자 회원 상세(adminUser ← pb_admin_user): 기본 정보·재화·대전/우편 기록·패스·로또, 포켓몬(파워·트로피), 스킨·프레임, 가방, 친구, 판돈 친선전, 선물, 같은 세이브(트로피 해시) 계정 경고. 관리자 목록에서 아이디 클릭
- 세이브 복제 버그 수정: 로그아웃 시 SAVE 초기화, 회원가입 시 이전 계정 세이브(acct 있음)는 이어받지 않음 (게스트 진행만)
- flushSave 이름 충돌 수정: 선물·로또용은 flushSaveNow (pagehide keepalive flushSave 복구)
- 조사(11/27): 회원가입 세이브 이어받기로 만든 복제 계정 군 — yunsung1107→jackpot1~4, suki→suuk*/sexy*/riri(10개), dicksuck→dicksuck2~6. 대부분 정지됨. 선물·판돈으로 본계정에 옮긴 흔적 없음
- 서버 세이브 검증(pb_save 급증 감지/제한, pb_flag)은 자동 승인 거부로 미적용 — 사용자 확인 필요

## v1.20.28 (서버 저장 검증)
- pb_save: 관리자 제외. 새 계정 첫 저장이 다른 계정 데이터처럼 보이면(금구슬>3000, 혜성조각>100, 포켓몬>5, 트로피>80, 스킨 보유, acct 다름) 빈 세이브로 초기화 → 'reset' 반환(클라 스타팅 선택) + pb_flag 'clone_reset'
  - 기존 계정: 저장 간 증가량 허용치 = 우편 수령(claimed_at 이후)+지급 + 6000+1500×분 + 기존 잔액×3(슬롯). 넘으면 pb_flag 'jump', 허용치+30만(혜성 +3만) 넘으면 깎고 'fix' 반환. 포켓몬 +8(+우편) 넘게 늘면 기록
- pb_signup: 가입 IP 기록만 (signup_ip). 하루 3계정 제한은 사용자 요청으로 해제
- pb_mail.claimed_at, pb_users.saved_at/signup_ip, pb_flag 테이블, pb_admin_flags(의심 기록 + 같은 트로피 해시 묶음) → 관리자 메뉴 '의심 기록'

## v1.20.29 세이브 봉인
- sealPay(s)/sealOf(s) (md5s, 키 SLK = pb_cfg 'seal') ↔ 서버 pb_seal_pay(jsonb). 서명 대상: 금구슬|혜성조각|own(정렬)|lv합|tro합|이로치수|스킨수|가방(정렬 k:n)|프레임수|패스xp|패스유료
- saveLocal/saveBody 가 sg 를 붙임. 로딩 시 localStorage 서명이 안 맞으면 버림(계정은 서버 세이브 사용, 게스트는 초기화). 로그인 시 로컬 우선은 서명 맞을 때만
- pb_save: pb_cfg seal_on='1' 이면 sg 없거나 틀리면 거부 {seal:true, save:서버} + pb_flag 'seal'(10분 1회) → 클라는 서버 세이브로 교체
- 새 버전 강제 새로고침은 ?v= 붙여 캐시 우회
- 한계: 개발자 도구 콘솔로 메모리 값을 고친 뒤 저장하는 건 못 막음(키가 클라에 있음) → 급증 감시(jump/clamp)로 보완

## v1.20.30 (+서버)
- 봉인 모드 pb_cfg seal_on: 'soft'(현재) = 서명 없음(예전 버전) 저장은 받고 pb_flag 'nosig'(30분 1회), 서명 틀림만 거부 / 'strict' = 서명 없으면 거부 / '0' = 끔. 1.20.29 엄격 모드 때 예전 버전 유저 저장이 거부돼 진행이 되돌아가던 문제 해결
- rev 없는 아주 예전 클라 저장은 거부({legacy:true}) — 옛 캐시 버전이 최신 세이브를 덮어써 '일정 시점으로 되돌아가는' 원인 차단
- 클라: 봉인 전(서명 없는) 로컬 세이브는 버리지 않고 이어감, 서명 틀림만 버림
- 로또 3개 맞춤: 당첨 우편에 pass_paid(조롤패스 프리미엄) 같이 지급(당첨금 0이어도 발송)

## v1.21.0 아머드 뮤츠 + 이벤트
- 신캐 armewtwo(아머드 뮤츠, 크로마틱 cr, id 'armewtwo' — SPR/POR 에 문자열 키로 추가): 평타 E8YS92RM(에스퍼, 유도 4연발 gap .2) / 필살기 JOF511JAJ32TA(강철 nova aoe3, 기절1, 취약3초 vulnC c:1) / 가젯 EBIC881JUD(e.armT=5: 주는 피해·받는 피해·이동·장전 1.2배 + 탄환 가득) / 특성 프레셔
- 이벤트 '아머드 뮤츠 구출': 판마다 SAVE.ashard +10~50, 이벤트 창(로또 아래) rescueHTML/ASH_SHOP: 아머드 뮤츠 1000, 상자 티켓·스카우트·금구슬·혜성조각·전설 7일 선택권. 로비 이벤트 버튼 배지 '구출'
- 가방 상자 티켓 '모두 열기'(openAllBox, 합산 결과창)
- 관리자 계정 트로피 0 고정(endMatch d=0·tro={}, 로그인 시 tro={})
- 공지 배너 notice/v1210.png (dev/tools/banner_v1210.py)

## v1.21.2
- 뮤츠 구출은 로비 별도 버튼(#bRescue, 진행 % 배지) → openRescue. 로또 창에서 분리
- 구출 상점 칸 112×122 고정 그리드. 키 작은 화면(.lowh)은 왼쪽 버튼들 높이 축소

## v1.21.3
- 슬롯 출입 금지 1시간(v1.21.4): SAVE.slotBan = 해제 시각(ms). slotBanned() — 예전 값 1/true 나 1시간 넘게 남은 값은 지금+1시간으로, 지나면 삭제

## v1.21.5
- 관리자 슬롯 금지 해제: pb_admin_slot_unban(token, users[]) — 서버 세이브에서 slotBan 삭제 + pb_users.cmd {slotUnban} → pb_save 응답 'cmd' 로 접속 중 클라에도 반영 후 비움. 관리자 목록 '슬롯 해제'(금지 중인 회원만) + '선택 슬롯 해제'
- pb_users.cmd: 서버→클라 1회성 명령 통로 (pb_save 가 돌려주고 비움)

## v1.21.6
- 랭킹: pb_rank limit 10 → 300 (정지·관리자·테스트 계정 제외 전원)
- 새 아이템: maxlv(만렙 티켓, maxLvPick → lv 11), pull10(10연속 추출 티켓, 스카우트 가중치로 10번 givePk, 5×2 결과 격자). 관리자 우편 키 그대로 사용 가능
- 갑옷 조각 상점: 만렙 티켓 500, 10연속 추출 400 추가, '여러 개' 수량 교환(rescueQty: ±1/±10/최대), 칸 112×140

## v1.21.7 전설 고유 스킨
- 전설 8종 테마 스킨(상자 드롭 가능, 관리자 sk_ 키): 흑요석 뮤츠(obsid) · 창공 레쿠쟈(sky, 메가 포함) · 흑빙 큐레무(onyx, f1/f2) · 순백 질서 지가르데(order, 10%/50%/퍼펙트) · 일식 네크로즈마(eclipse, f1~f3) · 홍염 아르세우스(flame) · 벚꽃 버드렉스(sakura, f1/f2) · 월식 솔가레오(lunar). 기라티나(백귀야행)·무한다이노(패스 3종)는 기존 것
- 생성: dev/tools/legend_skins.py + legend_themes.json (색상 계열 분류 → 테마 램프, 초상화 배경은 가장자리 flood fill 로 보존)
- IMGX 는 SKINX 의 모든 이미지 키(f1~f3, mega, gmax) 로드, megaImg 도 테마 지원
- 갑옷 조각 가격: 만렙 티켓 500→700, 10연속 추출 400→1500
- v1.21.8: 레쿠쟈 gold→sky(창공), 큐레무 magma→onyx(흑빙), 아르세우스 abyss→flame(홍염) 교체. 예전 키는 SKREN 으로 cleanSave 때 새 키로 바꿔줌
- v1.21.9: 슬롯머신 숨김 (SHOW_SLOT=false)
- v1.21.10: 로비 조롤패스 버튼 위에 패스 스킨 진열(#lpSkins: 백귀야행 기라티나 + 무한다이노 3종, 누르면 패스), 로고 위로 이동
- v1.21.11: 패스 진열을 큰 무한다이노 하나로 — 은하수→오로라→백금 2.6초마다 번쩍이며 교체, 아래 스킨 이름

## v1.21.12
- 관리자 우편 아이템 목록 ADMK(=스킨 제외 전부): 조롤패스 프리미엄(pass_paid), 신규 pass_xp(조롤패스 경험치 +100/개, invAdd→passGain, 회수 시 xp 차감).
- 전설 8종 스킨 도트 수작업: dev/tools/legend_hand/ (hp.py=색 외곽선·림라이트·테마 패턴, hand.py=스탬프(결정/구름/고드름/육각/왕관/불꽃/벚꽃/달) 좌표 지정, run.py→out.pkl, apply.py→skins.js 반영). 폼(f1~f3/mega)은 hp.py 절차 처리만.

## v1.21.13
- 브롤볼 연출: 골 세리머니(배너·득점자 초상화·자책골·플래시·슬로모·꽃가루·폭죽·골망 출렁), 킥오프(하늘에서 공 낙하, 매치 포인트), 연장전(동점 시 60초 서든데스, G.ot), 마지막 10초 비프·타이머 깜빡, 공 회전(90도 도트)·궤적·강슛 불꽃 꼬리·킥 높이 바운드, 소유팀 화살표, 화면 밖 공 방향 표시, 경기장 라인/골대/골망. 멀티: bl 스냅샷에 ot·z·sk 추가, ev GL/OT/BK 클라 처리. drawBallHUD().
- 벽 관통(thru) 탄환이 탄 반경(최대 0.45타일) 십자 샘플로 사탕돌(타일4) 판정 → 아르세우스 음파가 돌 가장자리 스쳐도 부서짐.

## v1.21.14
- 브롤볼: 내가 공을 잡으면 화면 테두리 옅은 파란 도트 글로우. 공을 든 채 상대 골대 입구(가장자리 0.8타일)로 들어가면 골 판정(자기 골대로 들고 가면 무효).

## v1.21.15
- 아머드 뮤츠 상향: HP 5200, 속도 1.0, 장전 rl 1.1, 충전 2400, 평타 440×4·사거리 8, 궁 2300·반경 3.6·기절 1.3·취약 4초, 가젯 6초, 패시브 받는 피해 -12
## v1.21.15
- 아머드 뮤츠 상향: HP 5200, 속도 1.0, 장전 rl 1.1, 충전 2400, 평타 440x4 사거리 8, 궁 2300 반경 3.6 기절 1.3 취약 4초, 가젯 6초, 패시브 받는 피해 -12%.
- 유도 강화: spec homeT(선회율, 기본 7) + 목표 고정(p.lk). 아머드 뮤츠 home 5.5 / homeT 16.

## v1.21.16 포켓 주식
- DB: pb_stock(종목: price/prev/fund(기본가치)/vol/fl(유동주식=보유한도, 유동성 L=price*fl)/tick_at/news), pb_stock_hist(24h+ 차트, 3일 보관), pb_stock_flow(이번 10분 유저별 매수·매도 금액), pb_stock_hold(username,sid,qty,cost), pb_stock_log.
- pb_stock_tick(): 10분 경계(date_bin) 지연 처리(최대 36틱 따라잡기). 변화 = 군중 0.10*tanh(유저별 순매수(±0.15L로 제한) 합/L) + 인원 심리 0.4%/명(±3%) + 노이즈 vol + 기본가치 회귀 5%*ln(f/p) + 뉴스(2.5% 확률 ±4~14%, 고변동주 1.6배). 틱당 ±25% 제한.
- pb_stock_list(token), pb_stock_trade(token,sid,qty(+매수/-매도)): 서버가 save.coins 직접 증감+rev+1 (로또와 같은 방식, 클라는 flushSaveNow 후 호출하고 coins/rev 반영). 수수료 1%(최소 1), 보유 한도 fl주.
- 클라: 로비 상단 '주식' 버튼(#bStock, STK_ICO 도트 아이콘), openStock() 목록/상세(도트 차트 stkChart, 카운트다운 후 자동 갱신). 상승=빨강▲, 하락=파랑▼ (색약 대비 기호 병기).

## v1.21.17 포켓증권 화면 교체
- 옛 혜성조각/공매도 포켓증권(클라 보유 SAVE.stk·sht, pb_stock(p_n) 1분 틱) 클라 코드 제거 → #stock 화면을 새 서버 시세(pb_stock_list/trade, 금구슬)로 다시 만듦. (옛 DB pb_stock_co/pb_stock_px·함수 pb_stock(int)는 남아 있지만 안 씀)
- 상점 '투자' 섹션에 포켓증권 항상 노출(슬롯은 SHOW_SLOT로만), 로비 #bStock도 stockOpen('menu').
- 차트 stChart: 6시간(10분봉)/1일(30분봉)/3일(2시간봉), 캔들·라인, 가격축·시간축, 거래대금 막대(산 사람≥판 사람이면 빨강), 평단선, 현재가 태그, 최고/최저 표시, 십자선 툴팁(시고저종·거래대금·인원).
- DB: pb_stock_hist에 vol/nb/ns 추가, pb_stock_news(뉴스 기록), list가 3일치 [t,price,vol,nb,ns] + 최근 뉴스 12개 반환.

## v1.21.18
- 주식 종목을 포켓몬 세계 실제 회사로(공식 한국어명): 실프주식회사, 데봉 코포레이션, 매크로코스모스, 프렌들리숍, 포켓치주식회사(PTCH), 플라드리 래버러토리(FLDR), 대보라홀딩스(MAUV) + 조롤컴퍼니(JROL, pb_stock.kind='sine': 중심값 f는 매매로 움직이고 기준값 base로 회귀, 가격=f*(1+amp*sin(ph)), ph는 틱마다 2π/(10~14) 증가 → 약 2시간 주기 ±20%).
- .ico 아이콘 width:auto (높이만 바꾸던 곳에서 금구슬이 찌그러지던 문제).

## v1.21.19
- 지어낸 종목(이상한사탕제과 cndy, 로켓홀딩스 rckt, 잉어킹수산 karp) 복구: 주주 보유분이 남아 있었음. 마지막 거래가(394/157/32)로 재상장, 지난 차트는 지워져서 다시 생성. ord 9~11.

## v1.21.20
- 선물(pb_gift2: 금구슬·혜성조각 + 가방 아이템·스킨 최대 50개). 서버가 보내는 사람 save.inv/shy/skn에서 빼고(장착 중 스킨 sk도 해제) rev+1, 받는 사람 우편 items로 감. 상대가 이미 가진 스킨은 has_skin 거절. 후원하기(sponsorAsk)는 재화만(noItems). 옛 pb_gift는 남아 있음.
- 주식 통화 분리: pb_stock.cur('coin'|'gem'). 혜성조각주: 에테르재단 AETH(공식명) · 혜성광업 COMT · 별의모래상사 SAND(지어냄). trade는 cur에 따라 save.coins/gems 증감, coins·gems 둘 다 반환. 화면 탭: 금구슬주/혜성조각주/내 주식, 계좌·모아보기도 통화별.
- 주의: pb_stock에 'cur' 컬럼이 생겨서 plpgsql 변수명 cur 쓰면 ambiguous → tick/list 변수 vcur로 바꿈.

- (DB만) 매크로코스모스·프렌들리숍·플라드리 래버러토리를 혜성조각주로 이동(보유자 없던 종목). 가격·차트를 비율로 축소(45/25/15), fl 60/100/200.

## v1.21.21
- 백귀야행 기라티나(yako)에 pass:1 → 상자 스킨 드롭(dropShy)에서 제외 (무한다이노 3종은 원래 pass:1).
- 새 스킨 해적선장 거북왕(blastoise_pirate): dev/tools/skins/blastoise_pirate.py (원본 25x24 도트에 영역별 색(바다색 몸·나무판자 등껍질·황동 대포·크림 배) + 빨간 두건·안대·해골 문양·해적 깃발·대포 구멍 손도트, 초상화 40x40에 삼각 해적모자·안대·금귀걸이). 상자에서 나옴.

## v1.21.23
- 관리자 '보낸 우편'(pb_admin_sent_list: 개별+전체, bc_id 또는 created_at+msg로 묶음, 300개) — 줄마다 삭제/회수. 삭제 = pb_admin_mail_del(token,at,msg): pb_mail_bc + 안 받은/받은 기록 모두 지움, 재화 회수 없음 (삭제 후엔 회수 불가)

## v1.21.24 다계정 대책
- 선물(pb_gift, pb_gift2 → 후원 포함): 보내는 계정이 가입 3일 미만이면 거절 err 'new_acct'(at=풀리는 시각). 관리자 제외
- 친선전 판돈(pb_duel_open): 판돈이 있으면 양쪽 모두 pb_mcount(u)(=pb_pick 판 수, 11/21부터 기록) 20판 이상 필요, err 'few_games'
- 같은 IP 차단은 안 함 (사용자: 같은 와이파이 쓰는 경우 많음)
## v1.21.25 포켓증권 숨김
- `SHOW_STOCK=false` → 상점 투자 칸·로비 주식 버튼 숨김. 다시 열려면 true + `pb_cfg`에 `stock_on='1'` 넣기(없으면 pb_stock_trade가 'closed' 거절).
- 종료 시 보유 주식 전부 산 가격(cost 기준, 수수료 제외)으로 우편 환불: 11명, 금구슬 159,565 · 혜성조각 662, pb_stock_hold 비움. 시세 테이블·함수는 그대로 남아 있음.

## v1.21.26 새 업데이트 알림
- build.py가 저장소 루트에 `ver.json`({"v":VER})도 만듦 → 같이 커밋·배포해야 함.
- 클라 `updPoll()`: 8초 뒤 + 1분마다 + 화면 돌아올 때 `ver.json?t=` 확인, 지금 VER보다 높으면 화면 위 띠(#updBar) 표시. 로비: [새로고침](저장 후 ?v= 붙여 다시 열기)/[나중에](10분 뒤 다시). 판 중: 띠만 보이고 판 끝나면 버튼 생김.
- 옛 강제 업데이트(pb_cfg 'ver' → verCheck)는 그대로 있음.

## v1.21.27 오토에임 개선
- autoTarget: 이동 예측을 고정 0.15초 → 실제 도달 시간(shot: 거리/탄속, lob·zone·meteor: s.fl)으로 2번 반복 계산, 사거리 밖이면 사거리로 자름. 벽에 막힌 적은 1.7배 먼 것으로 쳐서 바로 맞힐 수 있는 적 우선. 탭 인정 시간 300→550ms.
- 테스트(훈련장, 3·5칸, 230px/s로 위아래 이동): 이전 피카츄 6/10·이상해꽃 2/10·팬텀 2/10·망나뇽 6/10 → 지금 사거리 안이면 전부 10/10.

## v1.21.28 공격 개편 (특색 없던 11마리)
- 평타(atk)도 ty:'dash'(돌진 공격, e.dash.atk=1 → 맞히면 필살기 충전) / ty:'nova'(내 주위 범위 공격) 가능: spawnShots 앞부분. 돌진 vulnC는 확률(c) 적용.
- 마자용 카운터(주변 범위) · 에브이 관통+거리비례(최대 1.8배) · 블래키/샤크니아/돌핀맨/솔가레오 돌진 공격 · 너트령 가시 파편(shatter) · 해무기 되돌아오는 물(boomer) · 메테노 3갈래 · 카푸꼬꼬꼭 2번 튀는 번개(chain) · 날개치는머리 3갈래 탄막.
- 공지 #26(배너 notice/v1228.png).

## v1.21.29 멀티 종목 선택
- 3대3 멀티 방에서 방장이 종목 선택(ROOM_MODES: gem/bounty/heist/ball, NET.tmode → 방장 presence meta `tm`) → hostStart가 R.kind로 보냄. 1대1 내기 친선전(ko)은 그대로.
- 스냅샷에 `bs`(바운티 별 점수 + 엔티티별 현상금) 추가. 하이스트 금고는 엔티티라 원래 동기화됨, 브롤볼은 bl.
- 가짜 멀티 테스트(dev/mptest/fake.js)로 세 종목 모두 호스트·참가자 모드·점수·시간 일치 확인.

## v1.21.30 전설 너프
- BAL_FIX 다음에 `NERF` 표([체력, 평타, 필살기] 배율, 폼 포함): 무한다이노 .88/.85/.85 · 기라티나 .92/.9/.88 · 아르세우스 .9/.9/.9 · 지가르데 .95/.9/.9 · 네크로즈마 .95/.92/.92 · 다크라이 .95/.92/.92(다크홀 수면 1.6→1.2초) · 아머드 뮤츠 .92/.9/.9.
- 근거: pb_pick 사용률 + 쇼다운 평균 순위(무한다이노 2.2등). 팀전 승률은 봇 상대라 다 90%+라서 기준으로 안 씀.

## v1.21.31
- 아머드 뮤츠 너프 취소(이벤트 한정). NERF 표에서 뺌.
- 아머드 뮤츠 구출 이벤트 종료: `RESCUE_END` = 2026-11-30 23:59:59 KST(기기 시각 기준). 이후 갑옷 조각 지급 안 함, 로비 '뮤츠 구출' 버튼 숨김, 창은 '이벤트 종료'. 이벤트 창에 남은 시간 표시.

## v1.21.32
- pb_ping이 `now`(서버 시각 ms)도 돌려줌 → 클라 `SRVOFF`/`srvNow()`. 구출 이벤트 종료(rescueOn/rescueLeft)는 서버 시각 기준(로그인 안 했거나 핑 전에는 기기 시각).

## (서버) pb_ping 고장 수정 (11/28)
- pb_ping 끝의 `select count(*) from pb_friend where b=me` 가 변수 b(pb_users)와 컬럼 b가 겹쳐 매번 에러 → 11/27 08:49 KST쯤부터 핑 전부 실패(접속 표시·초대·친구 요청 알림·정지 즉시 반영·서버 시각 안 됨). `pb_friend fq where fq.b=me` 로 수정. plpgsql 변수명 b 쓰는 함수에서 테이블 컬럼 b 쓸 때 별칭 필수.

## v1.21.33 오류·이상 상태 자동 기록
- 증상 제보(폰, AI 혼자 판): 갑자기 다른 포켓몬·체력바가 전부 안 보이고 맵과 내 포켓몬만 보임. 판은 계속 진행(킬 피드·투사체는 보임). PC 헤드리스로는 재현 안 됨.
- 테이블 pb_err(at, username, ver, ua(+화면크기@DPR), kind, d) 14일 보관, RPC pb_err_log(token|null, ver, kind, d, ua) (분당 전체 60, 유저당 시간당 30).
- 클라: errLog(kind,d) — 같은 종류는 세션당 1번. kind: 'loop'(루프 try/catch 예외), 'onerror', 'reject', 'ghost'.
- ghost 감지 ghostChk: 판 중 1초마다, 내 주변 7타일에 살아 있는 포켓몬 2마리 이상인데 render가 그린 엔티티 수(G.dbgN, render의 L 루프에서 셈)가 1 이하인 상태가 3초 연속이거나 좌표가 NaN이면 ghostSnap(엔티티별 alive/좌표/invisT/digT/stealth/bush/visibleTo/이미지 등) 전송. 판마다 1번.
- 확인: `select * from pb_err order by at desc`

## v1.21.34 포켓몬 안 보임 버그 수정
- 원인(pb_err ghost 기록으로 확인): v1.21.28의 평타 돌진(atk ty:'dash')은 스펙에 kb가 없는데 moveEnt 돌진 접촉에서 `o.kbx=D.dx*D.s.kb*...` → NaN 넉백 → 좌표 NaN → 충돌 밀어내기로 다른 포켓몬·나에게 번짐 → 안 그려짐(맵·UI만 보임).
- 수정: kb 있을 때만 넉백. 안전장치: moveEnt 시작에 kbx/kby NaN이면 0, 좌표 NaN이면 마지막 정상 좌표(e.gx/gy, 없으면 스폰)로 복구.
- 검증: 가변 dt로 젬·하이스트·볼·바운티·쇼다운·녹아웃 수십 판 돌리며 x/y/kb/v 세터에 NaN 트랩 → 0건 (수정 전 하이스트 25판 중 4판 발생).

## v1.21.35 이벤트: 초희귀 챌린지
- SAVE.srm=1(챌린지 켬) / SAVE.srt(초희귀 토큰). **v1.21.36: 아직 시작 안 함** — `SR_START=null`이면 이벤트 꺼짐(버튼 숨김·srMode 꺼짐). 시작: SR_START에 시각(또는 0), 끝: SR_END. 공지(pb_notice)도 아직 안 올림. srOn()/srMode().
- 켜면: 선택창은 초희귀(gr 's')만 보임(위에 '챌린지 끄기' 줄), startMatch에서 초희귀 아니면 막고 선택창으로, pickRoster 봇·AI 파티도 초희귀만. 켤 때 지금 포켓몬이 초희귀가 아니면 보유 초희귀 중 트로피 높은 걸로 바꿈(초희귀 0마리면 못 켬).
- 보상: endMatch에서 srMode && 내 포켓몬 초희귀 && (팀전 승리 || 쇼다운 1등) → 토큰 10~50 (G.result.srt, 결과 화면 표시). 훈련장 제외.
- 교환(openSr, SR_SHOP): 500 → 초희귀 프레임(fr_srare, FRAMES 'srare', CSS .fr-srare 파란 테두리+도트 다이아). 1000개 보상 스킨은 미정(v1.21.37에서 육군 아미 타이거 어흥염 삭제 — 사용자 요청, 받은 사람 없음).
- 로비 왼쪽 '초희귀' 버튼(#bSr, 아이콘·배지=토큰, 켜져 있으면 ON + 깜빡임). 토큰 아이콘 SRT_ICO. 공지 배너는 스킨 정해지면 다시 만들 것.

## v1.21.38 초희귀 챌린지 스킨 5종 + 랜덤 초희귀 스킨 박스 (이벤트는 아직 꺼짐)
- 스킨(THEMES, pass:1 + ev:'초희귀 챌린지' → 일반 상자 드롭 제외): 마술사 후딘(alakazam_magic) · 산타 라프라스(lapras_santa) · 사이버 쥬피썬더(jolteon_cyber) · 흡혈귀 블래키(umbreon_vamp) · 해적 갑판장 누리레느(primarina_pirate). 사무라이 핫삼은 초안만(사용자: 제외).
- 도트: dev/tools/skins/drafts/draft7.py(스프라이트, 원본 해상도·부위 바꾸기) + portraits7.py(40x40 초상화) — 원본 png는 drafts/src/. skins.js에는 spr ×4(오른쪽 여백만큼 왼쪽도 채워 가운데 맞춤), por.
- SR_SHOP 'srbox' 1000토큰: srBoxPool() = 초희귀(gr 's') 포켓몬의 안 가진 스킨(이로치·테마) 전부, 이벤트 스킨 가중치 6 · 나머지 1 (전부 미보유일 때 이벤트 스킨 1종 9%, 5종 합 45%, 이로치 1종 1.5%). 다 모으면 버튼 '✓ 다 모음'. 포켓몬이 없어도 스킨은 받음(안내 문구).
- v1.21.39: 해적 갑판장 누리레느 초상화를 사용자가 준 그림으로 교체 (drafts/src/primarina_pirate_por_user.png)

## v1.21.40 시즌 1 마감(11/30 24시) 준비
- 초희귀 챌린지 시작: `SR_START = 2026-12-01 00:00 KST` (서버 시각 srvNow 기준). 같은 시각에 랭킹 이벤트(EV_END)·뮤츠 구출(RESCUE_END) 끝남. evOn도 srvNow 사용. srvNow는 SRVOFF 선언 전 호출돼도 NaN 안 나게 `(SRVOFF||0)`.
- 서버 스냅샷: pb_season(id=1, top jsonb) + pb_season_snap() — 12/1 00:00 이후 첫 pb_ping/pb_season_top 호출 때 1~3등(pb_rank와 같은 조건) 저장, 한 번만. pb_season_top() 공개 RPC.
- 로비 랭킹 위 #rkSeason: 12/1~12/8 동안 3등→2등→1등 번갈아(1등 6초, 나머지 3.5초), 누르면 프로필. seasonShow()/seasonStep().
- 프레임: 2등 '은빛 트로피 성좌'(fr_star2) · 3등 '동빛 트로피 성좌'(fr_star3) — fr-star CSS·이미지를 은/동색으로 다시 칠해 복제(.fr-star2/.fr-star3, frsg2/3, frst2/3). 관리자 우편 아이템으로 보낼 수 있음.
- 보상 자동 지급: pb_season_snap 이 스냅샷 직후 1~3등에게 우편(fr_star/fr_star2/fr_star3 + pb_cfg `season1_pk` 포켓몬). **한정 포켓몬은 새로 만들기로 함(미정) — 만들면 pb_cfg 에 season1_pk 넣어야 우편에 포켓몬이 들어감.**

## v1.22.0 시즌 1 보상 크로마틱 3종 (gr 'cr', 뽑기·상자 제외)
- gtinkaton 황금 망치 두드리짱(1등) — 도트는 dev/assets/variants/champion_tinkaton_* (원래 있던 것) / scorvi 은빛 갑주 아머까오(2등) / bferro 황동 가시 너트령(3등) — dev/tools/skins/chromatic_s1.py (원본 해상도: 남색 깃털→은빛 갑판+왼쪽 위 광택+이마 사파이어 / 회색 몸→황동, 덩굴→구리, 바깥으로 뻗는 가시 8개, 눈은 청록). 결과 png는 variants/silver_corviknight_*, brass_ferrothorn_*.
- CH 에 `base:'tinkaton'|'corviknight'|'ferrothorn'` 표시. 원본의 특성·가젯 코드를 같이 쓰게 case 라벨 추가: 철가시(bferro 25%), 필살기 충전(gtinkaton 1.4배), 미러아머(scorvi, 받는 피해 ×0.8), 철벽·택시·자이로볼 가젯, AI 택시. 평타 플래그(bigBonus/flinch/gyro)는 스펙에 직접.
- 서버: pb_cfg season1_pk1/2/3 = gtinkaton/scorvi/bferro → pb_season_snap 이 등수별로 우편에 넣음.
- 결과 발표 카드·랭킹 안내 문구에 보상 포켓몬 이름·스프라이트. 공지 배너 notice/v1220.png (dev/tools/banner_v1220.py).
- v1.22.1: 황금 망치 두드리짱 초상화 망치 금색 명암 다시 칠함(dev/tools/skins/gtinkaton_por_gold.py, 원본은 variants/champion_tinkaton_por_orig.png). **크로마틱 3종 특성·기술은 사용자 확인 전 임시값 — 사용자가 정해줄 예정**
- v1.22.2: 두드리짱 초상화 망치 다시 칠함 — 망치 덩어리만(노랑·주황 들어간 연결 덩어리, 갈색뿐인 몸 외곽선 제외) 위·왼쪽/아래·오른쪽 거리 비율로 5단계 금색. v1.22.0 공지(#28) 삭제(사용자 요청).
- v1.22.3: 두드리짱 초상화를 사용자가 준 그림으로 교체 (variants/champion_tinkaton_por.png)
- v1.22.4: 브롤볼 AI 자책골 금지 — kickBall 전에 ballOwnGoal(e,ang,v)로 2.5초 굴려봄(벽 튕김 포함), AI(e!==P && !e.owner)가 자기 골대로 들어갈 각이면 상대 골대 쪽 각(±0.35~π/2 순서)으로 다시 조준. 사람은 그대로.
- v1.22.5: 브롤볼 공 잘 보이게(반지름 14→18, 검은 테두리, 발밑에 도는 노랑 점선 링) + AI 패스(decide에서 0.5초마다: 2.5~8.5칸 안, 앞쪽·주변 빈·패스 길에 적 없는 아군 점수, 상대가 붙어 있으면 55%·아니면 12%, 받는 쪽 움직임 0.25초 앞으로 차줌, '패스!' 문구). 10판 시뮬: 패스 33번, 자책골 0.
