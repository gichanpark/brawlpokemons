# 사용법: python3 dev/build.py  (저장소 루트에서) → index.html 생성
import os
D=os.path.dirname(os.path.abspath(__file__));A=os.path.join(D,'assets')
s=open(os.path.join(D,'game.src.html'),encoding='utf-8').read()
for k,f in [('SPRITES','icons.js'),('TILES','tiles.js'),('POR','por.js'),('SHINY','shiny.js'),('FONT','font.b64'),('LOGO','logo.uri'),('ICON','icon.uri'),('NUGGET','nugget.uri'),('BALLS','balls.js'),('SHARD','shard.uri'),('STARP','starp.uri'),('LOCKC','lockc.uri'),('CANDY','candy.uri'),('DUSK','dusk.uri')]:
    s=s.replace('/*'+k+'*/',open(os.path.join(A,f),encoding='utf-8').read())
open(os.path.join(D,'..','index.html'),'w',encoding='utf-8').write(s)
print('built index.html',len(s))
