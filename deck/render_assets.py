#!/usr/bin/env python3
"""API 키 없이 헤드리스 Chrome + Canvas 생성형 아트로 슬라이드 이미지(PNG)를 렌더링한다.

- scenes: hero / theme-class / theme-camera / theme-moon
- 출력: docs/assets/<name>.png (1600x900)
- Chrome을 찾지 못하면 조용히 건너뛴다(폴백 SVG가 이미 있음).
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
html,body{margin:0;padding:0;background:#05060a;overflow:hidden}canvas{display:block}
</style></head><body><canvas id="c" width="1600" height="900"></canvas>
<script>
const c=document.getElementById('c'),x=c.getContext('2d'),W=1600,H=900;
let seed=1337;function rnd(){seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;}
function rr(a,b){return a+rnd()*(b-a);}
function grain(a=0.05){const d=x.getImageData(0,0,W,H);const p=d.data;
  for(let i=0;i<p.length;i+=4){const n=(rnd()-0.5)*255*a;p[i]+=n;p[i+1]+=n;p[i+2]+=n;}
  x.putImageData(d,0,0);}
function vignette(s=0.85){const g=x.createRadialGradient(W/2,H/2,H*0.2,W/2,H/2,H*0.85);
  g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(0,0,0,'+s+')');x.fillStyle=g;x.fillRect(0,0,W,H);}
function stars(n){for(let i=0;i<n;i++){x.beginPath();const r=rr(0.4,1.8);
  x.arc(rr(0,W),rr(0,H*0.72),r,0,7);x.fillStyle='rgba(255,255,255,'+rr(0.15,0.8)+')';x.fill();}}
function moon(cx,cy,r){const halo=x.createRadialGradient(cx,cy,r*0.6,cx,cy,r*5);
  halo.addColorStop(0,'rgba(242,193,78,0.42)');halo.addColorStop(1,'rgba(242,193,78,0)');
  x.fillStyle=halo;x.fillRect(0,0,W,H);
  const g=x.createRadialGradient(cx-r*0.35,cy-r*0.35,r*0.1,cx,cy,r);
  g.addColorStop(0,'#fffbe9');g.addColorStop(0.6,'#f2c14e');g.addColorStop(1,'#9c6a12');
  x.beginPath();x.arc(cx,cy,r,0,7);x.fillStyle=g;x.fill();
  x.save();x.beginPath();x.arc(cx,cy,r,0,7);x.clip();
  for(let i=0;i<12;i++){x.beginPath();x.arc(cx+rr(-r,r),cy+rr(-r,r),rr(r*0.04,r*0.16),0,7);
    x.fillStyle='rgba(120,80,10,'+rr(0.04,0.12)+')';x.fill();}
  x.restore();}
function water(y0,c1,c2){const g=x.createLinearGradient(0,y0,0,H);
  g.addColorStop(0,c1);g.addColorStop(1,c2);x.fillStyle=g;x.fillRect(0,y0,W,H-y0);
  for(let l=0;l<5;l++){x.beginPath();x.moveTo(0,0);const yy=y0+l*((H-y0)/5);
    for(let px=0;px<=W;px+=20){x.lineTo(px,yy+Math.sin(px*0.006+l)*6+rr(-3,3));}
    x.strokeStyle='rgba(120,170,255,'+rr(0.05,0.14)+')';x.lineWidth=rr(1,2.6);x.stroke();}}
function reflect(cx,y0,y1,col){const g=x.createLinearGradient(0,y0,0,y1);
  g.addColorStop(0,col+'0.35)');g.addColorStop(1,col+'0)');x.fillStyle=g;
  x.fillRect(cx-70,y0,140,y1-y0);
  for(let i=0;i<40;i++){x.fillStyle=col+rr(0.05,0.3)+')';const yy=rr(y0,y1);
    x.fillRect(cx+rr(-60,60),yy,rr(8,60),rr(1,2.5));}}
function silhouettes(){x.fillStyle='#02040a';
  [[640,700,26,42,18],[700,705,24,40,16]].forEach(([cx,cy,rx,ry,cry])=>{
    x.beginPath();x.ellipse(cx,cy,rx,ry,0,0,7);x.fill();
    x.beginPath();x.arc(cx,cy-ry+cry*0.3,cry,0,7);x.fill();});}

function sceneHero(){seed=7;
  const g=x.createLinearGradient(0,0,0,H);g.addColorStop(0,'#0a1226');g.addColorStop(0.6,'#122142');g.addColorStop(1,'#05060a');
  x.fillStyle=g;x.fillRect(0,0,W,H);
  stars(260);moon(1150,290,128);water(560,'#0b1830','#03050a');reflect(1150,560,860,'rgba(242,193,78,');
  silhouettes();vignette(0.8);grain(0.06);}

function sceneClass(){seed=21;
  const l=x.createLinearGradient(0,0,780,H);l.addColorStop(0,'#2a1a0e');l.addColorStop(1,'#5a3a1c');
  x.fillStyle=l;x.fillRect(0,0,780,H);
  const r=x.createLinearGradient(1600,0,820,H);r.addColorStop(0,'#0d1a30');r.addColorStop(1,'#1b2f52');
  x.fillStyle=r;x.fillRect(820,0,780,H);
  for(let i=0;i<60;i++){x.fillStyle='rgba(242,193,78,'+rr(0.02,0.12)+')';
    x.fillRect(rr(40,760),rr(120,820),rr(10,80),rr(6,40));}
  for(let i=0;i<60;i++){x.fillStyle='rgba(122,162,247,'+rr(0.02,0.14)+')';
    x.fillRect(rr(840,1560),rr(90,830),rr(10,90),rr(6,50));}
  const s=x.createLinearGradient(788,0,812,0);s.addColorStop(0,'rgba(0,0,0,0)');
  s.addColorStop(0.5,'rgba(242,193,78,0.9)');s.addColorStop(1,'rgba(0,0,0,0)');
  x.fillStyle=s;x.fillRect(770,0,60,H);
  x.fillStyle='#05060a';x.fillRect(796,0,10,H);
  for(let i=0;i<120;i++){x.beginPath();const px=rnd()<0.5?rr(0,780):rr(820,W);
    x.arc(px,rr(0,H),rr(0.5,2),0,7);x.fillStyle='rgba(255,255,255,'+rr(0.05,0.3)+')';x.fill();}
  vignette(0.75);grain(0.06);}

function sceneCamera(){seed=99;
  x.fillStyle='#06070c';x.fillRect(0,0,W,H);
  const cx=1120,cy=450;
  for(let i=0;i<26;i++){x.beginPath();x.arc(cx+rr(-520,520),cy+rr(-360,360),rr(6,44),0,7);
    x.fillStyle='rgba('+(rnd()<0.5?'122,162,247':'242,193,78')+','+rr(0.02,0.09)+')';x.fill();}
  x.beginPath();x.arc(cx,cy,340,0,7);x.fillStyle='#0a0f1c';x.fill();
  x.lineWidth=12;x.strokeStyle='#1c2740';x.stroke();
  const blades=9;x.beginPath();
  for(let i=0;i<blades;i++){const a=(i/blades)*Math.PI*2;const a2=a+Math.PI/blades;
    x.moveTo(cx+Math.cos(a)*250,cy+Math.sin(a)*250);
    x.lineTo(cx+Math.cos(a2)*110,cy+Math.sin(a2)*110);}
  x.lineWidth=8;x.strokeStyle='#16223c';x.stroke();
  const lg=x.createRadialGradient(cx-60,cy-70,10,cx,cy,250);
  lg.addColorStop(0,'rgba(122,162,247,0.5)');lg.addColorStop(0.4,'rgba(30,45,80,0.6)');
  lg.addColorStop(1,'rgba(5,6,10,0.95)');
  x.beginPath();x.arc(cx,cy,250,0,7);x.fillStyle=lg;x.fill();
  x.beginPath();x.arc(cx,cy,72,0,7);x.fillStyle='rgba(242,193,78,0.4)';x.fill();
  x.beginPath();x.arc(cx-18,cy-22,22,0,7);x.fillStyle='rgba(255,255,255,0.6)';x.fill();
  for(let i=0;i<3;i++){x.beginPath();x.arc(cx,cy,300+i*22,0,7);
    x.setLineDash([4,16]);x.strokeStyle='rgba(122,162,247,0.25)';x.lineWidth=1.5;x.stroke();}
  x.setLineDash([]);
  x.strokeStyle='rgba(242,193,78,0.25)';
  [[120,90,420,90],[120,90,120,300],[1480,810,1180,810],[1480,810,1480,600]].forEach(p=>{
    x.beginPath();x.moveTo(p[0],p[1]);x.lineTo(p[2],p[3]);x.stroke();});
  vignette(0.85);grain(0.07);}

function sceneMoon(){seed=303;
  const g=x.createLinearGradient(0,0,0,H);g.addColorStop(0,'#101a34');g.addColorStop(1,'#05060a');
  x.fillStyle=g;x.fillRect(0,0,W,H);
  stars(200);moon(800,320,140);water(560,'#0c1a33','#03040a');reflect(800,560,880,'rgba(242,193,78,');
  x.fillStyle='#02040a';
  for(let i=0;i<16;i++){const bx=rr(0,W),bw=rr(30,90),bh=rr(30,120);
    x.fillRect(bx,560-bh,bw,bh);
    for(let w=0;w<4;w++){if(rnd()<0.6){x.fillStyle='rgba(242,193,78,'+rr(0.4,0.9)+')';
      x.fillRect(bx+rr(4,bw-8),560-bh+rr(6,bh-10),rr(2,5),rr(2,5));x.fillStyle='#02040a';}}}
  silhouettes();
  for(let i=0;i<140;i++){x.beginPath();x.arc(rr(0,W),rr(0,H),rr(0.4,1.6),0,7);
    x.fillStyle='rgba(255,255,255,'+rr(0.05,0.35)+')';x.fill();}
  vignette(0.8);grain(0.06);}

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
            cmd = [
                chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
                "--hide-scrollbars", "--force-device-scale-factor=1",
                "--window-size=1600,900", f"--screenshot={out}",
                f"file://{page}#{name}",
            ]
            r = subprocess.run(cmd, capture_output=True, timeout=120)
            ok = os.path.exists(out) and os.path.getsize(out) > 10000
            print(f"{'ok ' if ok else 'FAIL'} {name}.png "
                  f"({os.path.getsize(out) if os.path.exists(out) else 0:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
