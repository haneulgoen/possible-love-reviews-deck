#!/usr/bin/env python3
"""API 키 없이 헤드리스 Chrome + Canvas 생성형 아트로 슬라이드 이미지(PNG)를 렌더링한다.

뮤트/에디토리얼 팔레트(그레이지·세피아·슬레이트) 버전.
- scenes: hero / theme-class / theme-camera / theme-moon
- 출력: docs/assets/<name>.png (1600x900)
"""
import os
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "docs", "assets")
os.makedirs(OUT, exist_ok=True)

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
]

HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;padding:0;background:#e4e0da;overflow:hidden}canvas{display:block}
</style></head><body><canvas id="c" width="1600" height="900"></canvas>
<script>
const c=document.getElementById('c'),x=c.getContext('2d'),W=1600,H=900;
let seed=1337;function rnd(){seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;}
function rr(a,b){return a+rnd()*(b-a);}
function grain(a=0.05){const d=x.getImageData(0,0,W,H);const p=d.data;
  for(let i=0;i<p.length;i+=4){const n=(rnd()-0.5)*255*a;p[i]+=n;p[i+1]+=n;p[i+2]+=n;}
  x.putImageData(d,0,0);}
function vignette(s=0.5){const g=x.createRadialGradient(W/2,H/2,H*0.25,W/2,H/2,H*0.9);
  g.addColorStop(0,'rgba(20,19,17,0)');g.addColorStop(1,'rgba(20,19,17,'+s+')');x.fillStyle=g;x.fillRect(0,0,W,H);}
function specks(n,col){for(let i=0;i<n;i++){x.beginPath();const r=rr(0.4,1.6);
  x.arc(rr(0,W),rr(0,H*0.72),r,0,7);x.fillStyle=col.replace('A',rr(0.1,0.5).toFixed(2));x.fill();}}
function moon(cx,cy,r){const halo=x.createRadialGradient(cx,cy,r*0.6,cx,cy,r*5);
  halo.addColorStop(0,'rgba(243,237,227,0.5)');halo.addColorStop(1,'rgba(243,237,227,0)');
  x.fillStyle=halo;x.fillRect(0,0,W,H);
  const g=x.createRadialGradient(cx-r*0.35,cy-r*0.35,r*0.1,cx,cy,r);
  g.addColorStop(0,'#f7f2ea');g.addColorStop(0.65,'#e6ddcf');g.addColorStop(1,'#b9ad9c');
  x.beginPath();x.arc(cx,cy,r,0,7);x.fillStyle=g;x.fill();
  x.save();x.beginPath();x.arc(cx,cy,r,0,7);x.clip();
  for(let i=0;i<12;i++){x.beginPath();x.arc(cx+rr(-r,r),cy+rr(-r,r),rr(r*0.04,r*0.16),0,7);
    x.fillStyle='rgba(120,108,92,'+rr(0.05,0.13)+')';x.fill();}
  x.restore();}
function water(y0,c1,c2){const g=x.createLinearGradient(0,y0,0,H);
  g.addColorStop(0,c1);g.addColorStop(1,c2);x.fillStyle=g;x.fillRect(0,y0,W,H-y0);
  for(let l=0;l<5;l++){x.beginPath();const yy=y0+l*((H-y0)/5);
    for(let px=0;px<=W;px+=20){x.lineTo(px,yy+Math.sin(px*0.006+l)*6+rr(-3,3));}
    x.strokeStyle='rgba(90,95,100,'+rr(0.06,0.16)+')';x.lineWidth=rr(1,2.4);x.stroke();}}
function reflect(cx,y0,y1){const g=x.createLinearGradient(0,y0,0,y1);
  g.addColorStop(0,'rgba(243,237,227,0.4)');g.addColorStop(1,'rgba(243,237,227,0)');
  x.fillStyle=g;x.fillRect(cx-70,y0,140,y1-y0);
  for(let i=0;i<40;i++){x.fillStyle='rgba(243,237,227,'+rr(0.06,0.3)+')';const yy=rr(y0,y1);
    x.fillRect(cx+rr(-60,60),yy,rr(8,60),rr(1,2.5));}}
function silhouettes(){x.fillStyle='#4b4843';
  [[640,700,26,42,18],[700,705,24,40,16]].forEach(([cx,cy,rx,ry,cry])=>{
    x.beginPath();x.ellipse(cx,cy,rx,ry,0,0,7);x.fill();
    x.beginPath();x.arc(cx,cy-ry+cry*0.3,cry,0,7);x.fill();});}

function sceneHero(){seed=7;
  const g=x.createLinearGradient(0,0,0,H);g.addColorStop(0,'#cbc6bf');g.addColorStop(0.55,'#a39d95');g.addColorStop(1,'#6f6b65');
  x.fillStyle=g;x.fillRect(0,0,W,H);
  specks(220,'rgba(255,255,255,A)');moon(1120,300,120);water(560,'#8f8b84','#55524d');
  reflect(1120,560,860);silhouettes();vignette(0.42);grain(0.05);}

function sceneClass(){seed=21;
  const l=x.createLinearGradient(0,0,780,H);l.addColorStop(0,'#c3b6a7');l.addColorStop(1,'#9a8b7b');
  x.fillStyle=l;x.fillRect(0,0,780,H);
  const r=x.createLinearGradient(1600,0,820,H);r.addColorStop(0,'#aab2b7');r.addColorStop(1,'#7f8a94');
  x.fillStyle=r;x.fillRect(820,0,780,H);
  for(let i=0;i<70;i++){x.fillStyle='rgba(120,100,80,'+rr(0.03,0.12)+')';
    x.fillRect(rr(40,760),rr(120,820),rr(10,80),rr(6,40));}
  for(let i=0;i<70;i++){x.fillStyle='rgba(70,90,105,'+rr(0.03,0.13)+')';
    x.fillRect(rr(840,1560),rr(90,830),rr(10,90),rr(6,50));}
  const s=x.createLinearGradient(780,0,820,0);s.addColorStop(0,'rgba(240,236,229,0)');
  s.addColorStop(0.5,'rgba(240,236,229,0.85)');s.addColorStop(1,'rgba(240,236,229,0)');
  x.fillStyle=s;x.fillRect(768,0,64,H);
  for(let i=0;i<110;i++){x.beginPath();const px=rnd()<0.5?rr(0,780):rr(820,W);
    x.arc(px,rr(0,H),rr(0.5,2),0,7);x.fillStyle='rgba(255,255,255,'+rr(0.05,0.28)+')';x.fill();}
  vignette(0.4);grain(0.05);}

function sceneCamera(){seed=99;
  x.fillStyle='#2c2b28';x.fillRect(0,0,W,H);
  const cx=1120,cy=450;
  for(let i=0;i<28;i++){x.beginPath();x.arc(cx+rr(-520,520),cy+rr(-360,360),rr(6,44),0,7);
    x.fillStyle='rgba('+(rnd()<0.5?'180,170,158':'150,160,168')+','+rr(0.02,0.08)+')';x.fill();}
  x.beginPath();x.arc(cx,cy,340,0,7);x.fillStyle='#3a3833';x.fill();
  x.lineWidth=12;x.strokeStyle='#54514b';x.stroke();
  const blades=9;x.beginPath();
  for(let i=0;i<blades;i++){const a=(i/blades)*Math.PI*2;const a2=a+Math.PI/blades;
    x.moveTo(cx+Math.cos(a)*250,cy+Math.sin(a)*250);x.lineTo(cx+Math.cos(a2)*110,cy+Math.sin(a2)*110);}
  x.lineWidth=8;x.strokeStyle='#48453f';x.stroke();
  const lg=x.createRadialGradient(cx-60,cy-70,10,cx,cy,250);
  lg.addColorStop(0,'rgba(180,170,158,0.4)');lg.addColorStop(0.4,'rgba(60,58,54,0.7)');lg.addColorStop(1,'rgba(30,29,27,0.95)');
  x.beginPath();x.arc(cx,cy,250,0,7);x.fillStyle=lg;x.fill();
  x.beginPath();x.arc(cx,cy,72,0,7);x.fillStyle='rgba(200,188,170,0.4)';x.fill();
  x.beginPath();x.arc(cx-18,cy-22,22,0,7);x.fillStyle='rgba(247,242,234,0.65)';x.fill();
  for(let i=0;i<3;i++){x.beginPath();x.arc(cx,cy,300+i*22,0,7);
    x.setLineDash([4,16]);x.strokeStyle='rgba(200,196,188,0.2)';x.lineWidth=1.5;x.stroke();}
  x.setLineDash([]);
  x.strokeStyle='rgba(220,214,204,0.22)';
  [[120,90,420,90],[120,90,120,300],[1480,810,1180,810],[1480,810,1480,600]].forEach(p=>{
    x.beginPath();x.moveTo(p[0],p[1]);x.lineTo(p[2],p[3]);x.stroke();});
  vignette(0.55);grain(0.06);}

function sceneMoon(){seed=303;
  const g=x.createLinearGradient(0,0,0,H);g.addColorStop(0,'#bdb8b1');g.addColorStop(1,'#6d6963');
  x.fillStyle=g;x.fillRect(0,0,W,H);
  specks(180,'rgba(255,255,255,A)');moon(800,320,140);water(560,'#8a877f','#4f4c48');reflect(800,560,880);
  x.fillStyle='#5a5750';
  for(let i=0;i<16;i++){const bx=rr(0,W),bw=rr(30,90),bh=rr(30,120);x.fillRect(bx,560-bh,bw,bh);
    for(let w=0;w<4;w++){if(rnd()<0.6){x.fillStyle='rgba(240,230,210,'+rr(0.4,0.85)+')';
      x.fillRect(bx+rr(4,bw-8),560-bh+rr(6,bh-10),rr(2,5),rr(2,5));x.fillStyle='#5a5750';}}}
  silhouettes();
  for(let i=0;i<120;i++){x.beginPath();x.arc(rr(0,W),rr(0,H),rr(0.4,1.6),0,7);
    x.fillStyle='rgba(255,255,255,'+rr(0.05,0.3)+')';x.fill();}
  vignette(0.42);grain(0.05);}

const scenes={hero:sceneHero,'theme-class':sceneClass,'theme-camera':sceneCamera,'theme-moon':sceneMoon};
const which=location.hash.slice(1);
(scenes[which]||sceneHero)();
</script></body></html>
"""


def find_chrome():
    for p in CHROME_CANDIDATES:
        if p and os.path.exists(p) and os.access(p, os.X_OK):
            return p
    return None


def main():
    chrome = find_chrome()
    if not chrome:
        print("Chrome을 찾지 못했습니다. 폴백 SVG를 그대로 사용합니다.")
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "art.html")
        open(page, "w", encoding="utf-8").write(HTML)
        for name in ["hero", "theme-class", "theme-camera", "theme-moon"]:
            out = os.path.join(OUT, f"{name}.png")
            cmd = [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
                   "--hide-scrollbars", "--force-device-scale-factor=1",
                   "--window-size=1600,900", f"--screenshot={out}", f"file://{page}#{name}"]
            subprocess.run(cmd, capture_output=True, timeout=120)
            ok = os.path.exists(out) and os.path.getsize(out) > 10000
            print(f"{'ok ' if ok else 'FAIL'} {name}.png "
                  f"({os.path.getsize(out) if os.path.exists(out) else 0:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
