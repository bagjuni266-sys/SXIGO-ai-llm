path = r'C:\Users\gamju\AppData\Local\Temp\opencode\SXIGOai.html'

models = [
    "qwen2.5-coder:7b", "llama3:latest", "qwen3.5:9b",
    "llama3.2-vision:latest", "kimi-k2.6:cloud", "gpt-oss:20b",
    "llama3:8b", "deepseek-r1:8b", "llama3.1:8b",
    "deepseek-r1:latest", "phi4:latest", "qwen2.5:latest",
    "qwen:latest", "qwen3:8b", "phi4:14b",
    "deepseek-coder:6.7b", "qwen2.5:7b", "phi3:medium"
]
MO = ''.join(f'<option>{m}</option>' for m in models)

template = open(path, 'r', encoding='utf-8').read() if False else None

html = r'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
<meta name="theme-color" content="#000">
<title>SXIGOai · Premium</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{--s:14px;--bg:#000;--bg2:#06060a;--bg3:#0c0c12;--bg4:#14141c;--t:#eeeef2;--t2:#7a7a8a;--t3:#555566;--t4:#333344;--g1:linear-gradient(135deg,#667eea,#764ba2);--g2:linear-gradient(135deg,#f093fb,#f5576c,#4facfe);--gb:rgba(255,255,255,.04);--gb2:rgba(255,255,255,.06);--hue:0deg;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI Variable","Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:var(--s);color:var(--t);--r1:10px;--r2:14px;--r3:18px;--r4:24px}
body{background:#000;overflow:hidden;height:100dvh;display:flex;align-items:center;justify-content:center;padding:0}
::-webkit-scrollbar{width:3px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,.05);border-radius:2px}
*{scrollbar-width:thin;scrollbar-color:rgba(255,255,255,.05) transparent}
.rgb-bg{position:fixed;inset:0;z-index:0;overflow:hidden;pointer-events:none}
.rgb-bg::before{content:'';position:absolute;inset:-60%;background:conic-gradient(from var(--hue) at 50% 50%,#667eea22,#764ba222,#f093fb22,#f5576c22,#4facfe22,#00f5d422,#667eea22);animation:rgbSpin 7s linear infinite;filter:blur(100px)}
@keyframes rgbSpin{to{--hue:360deg}}
@property --hue{syntax:'<angle>';initial-value:0deg;inherits:false}
.app{width:100%;height:100dvh;display:flex;flex-direction:column;background:var(--bg2);position:relative;overflow:hidden;margin:0 auto;max-width:100%}
@media(min-width:500px){.app{max-width:520px;border-radius:24px;margin:10px auto;height:calc(100dvh - 20px);box-shadow:0 16px 48px rgba(0,0,0,.5)}}
@media(min-width:900px){.app{max-width:640px;border-radius:28px;margin:16px auto;height:calc(100dvh - 32px);box-shadow:0 20px 64px rgba(0,0,0,.6)}}
.hdr{display:flex;align-items:center;gap:8px;padding:12px 16px;min-height:50px;background:rgba(0,0,0,.35);backdrop-filter:blur(40px);border-bottom:1px solid rgba(255,255,255,.03);z-index:10}
.hdr h1{font-size:15px;font-weight:600;flex:1;background:var(--g1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:-.3px}
.hdr .act{display:flex;gap:4px}
.hdr .act button{width:32px;height:32px;border-radius:8px;border:none;background:rgba(255,255,255,.05);color:var(--t2);font-size:13px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:.15s}
.hdr .act button:hover{background:rgba(255,255,255,.1);color:var(--t)}
.hdr .act button:active{transform:scale(.9)}
.mbar{display:flex;align-items:center;gap:6px;padding:6px 16px;background:var(--bg3);border-bottom:1px solid rgba(255,255,255,.03);z-index:9;overflow-x:auto}
.mbar .l{font-size:11px;color:var(--t3);font-weight:500;white-space:nowrap}
.mbar .d{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.mbar .d.g{background:#30d158;box-shadow:0 0 6px rgba(48,209,88,.3)}
.mbar .d.r{background:#ff453a}
.mbar .st{font-size:10px;color:var(--t3);white-space:nowrap}
.mbar select{-webkit-appearance:none;appearance:none;background:rgba(255,255,255,.06);border:none;border-radius:7px;color:var(--t);font-size:12px;padding:4px 22px 4px 8px;cursor:pointer;min-width:120px;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='9' height='9' viewBox='0 0 24 24' fill='none' stroke='%23888' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 6px center;font-family:inherit}
.mbar select:hover{background:rgba(255,255,255,.1)}
.mbar select option{background:var(--bg3)}
.msgs{flex:1;overflow-y:auto;overflow-x:hidden;padding:12px 14px 6px;scroll-behavior:smooth}
.msgs-in{max-width:100%;margin:0;display:flex;flex-direction:column;gap:4px}
.welcome{text-align:center;padding:36px 20px 20px;display:flex;flex-direction:column;align-items:center;gap:10px}
.welcome .ic{width:56px;height:56px;border-radius:18px;background:var(--g1);display:flex;align-items:center;justify-content:center;font-size:26px;box-shadow:0 8px 24px rgba(102,126,234,.3);animation:f 6s ease-in-out infinite}
@keyframes f{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.welcome h2{font-size:20px;font-weight:600;letter-spacing:-.4px}
.welcome p{font-size:13px;color:var(--t2);line-height:1.5;max-width:320px}
.welcome .chips{display:flex;flex-wrap:wrap;gap:5px;justify-content:center;margin-top:8px}
.welcome .chips button{padding:5px 12px;border-radius:16px;border:1px solid rgba(255,255,255,.06);background:rgba(255,255,255,.03);color:var(--t2);font-size:12px;cursor:pointer;transition:.2s;font-family:inherit}
.welcome .chips button:hover{background:rgba(255,255,255,.08);color:var(--t);border-color:rgba(102,126,234,.2);transform:scale(1.03)}
.welcome .tips{font-size:11px;color:var(--t3);margin-top:6px}
.msg{display:flex;gap:8px;padding:3px 8px 3px 6px;animation:up .25s ease}
@keyframes up{from{opacity:0;transform:translateY(6px)}}
.msg.u{flex-direction:row-reverse}
.msg .av{width:26px;height:26px;border-radius:8px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:11px;margin-top:2px}
.msg.u .av{background:var(--g1)}
.msg.a .av{background:var(--g2)}
.msg .b{max-width:86%;padding:9px 13px;border-radius:14px;font-size:13.5px;line-height:1.5;word-wrap:break-word;position:relative}
.msg.u .b{background:linear-gradient(135deg,#667eea,#764ba2);border-bottom-right-radius:3px;color:#fff}
.msg.a .b{background:rgba(255,255,255,.05);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,.03);border-bottom-left-radius:3px;color:var(--t)}
.msg .b p{margin:3px 0}
.msg .b pre{background:rgba(0,0,0,.3);border-radius:7px;padding:10px;overflow-x:auto;margin:5px 0;font-size:12px;border:1px solid rgba(255,255,255,.04)}
.msg .b code{font-family:"SF Mono","Cascadia Code","JetBrains Mono",monospace;font-size:12px}
.msg .b :not(pre)>code{background:rgba(255,255,255,.06);padding:1px 5px;border-radius:3px}
.msg .b .tm{font-size:9px;color:var(--t3);margin-top:3px;text-align:right;opacity:.6}
.typing{display:flex;gap:3px;padding:4px 0}
.typing span{width:5px;height:5px;border-radius:50%;background:var(--t3);animation:tp 1.4s infinite}
.typing span:nth-child(2){animation-delay:.2s}
.typing span:nth-child(3){animation-delay:.4s}
@keyframes tp{0%,60%,100%{opacity:.3}30%{opacity:1}}
.cb{animation:bl 1s step-end infinite;color:#667eea}
@keyframes bl{0%,100%{opacity:1}50%{opacity:0}}
.inp-w{padding:6px 14px 14px;z-index:10;background:linear-gradient(0deg,rgba(0,0,0,.96) 60%,transparent)}
.inp-i{display:flex;align-items:flex-end;gap:6px;background:rgba(255,255,255,.06);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.07);border-radius:22px;padding:3px 3px 3px 14px;transition:.2s}
.inp-i:focus-within{border-color:rgba(102,126,234,.3);background:rgba(255,255,255,.09)}
.inp-i textarea{flex:1;background:none;border:none;outline:none;color:var(--t);font-size:15px;font-family:inherit;resize:none;max-height:100px;line-height:1.4;padding:6px 0}
.inp-i textarea::placeholder{color:var(--t4)}
.inp-i .s{border:none;background:none;color:var(--t3);font-size:14px;cursor:pointer;width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:.15s}
.inp-i .s:hover{color:var(--t2);background:rgba(255,255,255,.05)}
.inp-i .sd button{width:36px;height:36px;border-radius:50%;background:var(--g1);border:none;color:#fff;font-size:14px;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(102,126,234,.35);transition:.15s}
.inp-i .sd button:hover{transform:scale(1.05);box-shadow:0 6px 20px rgba(102,126,234,.4)}
.inp-i .sd button:active{transform:scale(.9)}
.inp-e{display:flex;gap:4px;padding:4px 12px 0;font-size:10px;color:var(--t3)}
.inp-e span{cursor:pointer;padding:2px 8px;border-radius:5px;background:rgba(255,255,255,.03);transition:.15s;display:flex;align-items:center;gap:3px}
.inp-e span:hover{background:rgba(255,255,255,.06);color:var(--t2)}
.over{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:100;opacity:0;pointer-events:none;transition:.3s}
.over.s{opacity:1;pointer-events:auto}
.set{position:fixed;left:0;bottom:0;width:100%;max-height:85dvh;background:rgba(28,28,32,.96);backdrop-filter:blur(50px);border-radius:22px 22px 0 0;z-index:101;transform:translateY(100%);transition:.45s cubic-bezier(.32,.72,0,1);overflow-y:auto;padding:20px}
.set.s{transform:translateY(0)}
.set .gr{width:36px;height:4px;border-radius:2px;background:rgba(255,255,255,.12);margin:0 auto 16px}
.set h2{font-size:17px;font-weight:600;margin-bottom:16px;letter-spacing:-.3px}
.sg{margin-bottom:18px}
.sg label{display:block;font-size:12px;color:var(--t2);margin-bottom:5px;font-weight:500}
.sg select,.sg input[type=text],.sg input[type=number]{width:100%;padding:9px 12px;border-radius:9px;border:1px solid rgba(255,255,255,.06);background:rgba(255,255,255,.05);color:var(--t);font-size:13px;font-family:inherit}
.sg select{appearance:none;-webkit-appearance:none}
.sg .sl{display:flex;align-items:center;gap:10px}
.sg input[type=range]{flex:1;-webkit-appearance:none;height:3px;border-radius:2px;background:rgba(255,255,255,.1)}
.sg input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:16px;height:16px;border-radius:50%;background:var(--g1);cursor:pointer;box-shadow:0 2px 6px rgba(0,0,0,.3)}
.tg{display:grid;grid-template-columns:repeat(4,1fr);gap:5px}
.tg button{aspect-ratio:1;border-radius:10px;border:2px solid transparent;cursor:pointer;transition:.2s;position:relative;overflow:hidden}
.tg button.a{border-color:#fff;transform:scale(1.06);box-shadow:0 0 16px rgba(255,255,255,.1)}
.tg button .lb{position:absolute;bottom:3px;left:50%;transform:translateX(-50%);font-size:8px;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.6);pointer-events:none;white-space:nowrap}
.tc{position:fixed;top:14px;left:50%;transform:translateX(-50%);z-index:200;display:flex;flex-direction:column;gap:5px;pointer-events:none;align-items:center}
.toast{padding:8px 18px;border-radius:12px;font-size:12px;background:rgba(28,28,32,.94);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.06);color:var(--t);animation:ti .25s ease;pointer-events:auto;box-shadow:0 4px 20px rgba(0,0,0,.4)}
@keyframes ti{from{opacity:0;transform:translateY(-8px) scale(.95)}}
.side{position:fixed;left:0;top:0;bottom:0;width:260px;background:rgba(20,20,26,.98);backdrop-filter:blur(40px);z-index:90;transform:translateX(-100%);transition:.4s cubic-bezier(.32,.72,0,1);display:flex;flex-direction:column;border-right:1px solid rgba(255,255,255,.04)}
.side.s{transform:translateX(0)}
.side-h{padding:16px;display:flex;align-items:center;gap:8px;border-bottom:1px solid rgba(255,255,255,.04)}
.side-h h3{font-size:13px;font-weight:600;color:var(--t2);text-transform:uppercase;letter-spacing:.5px}
.side-h button{background:none;border:none;color:var(--t3);font-size:16px;cursor:pointer;margin-left:auto;width:28px;height:28px;border-radius:6px;display:flex;align-items:center;justify-content:center}
.side-h button:hover{background:rgba(255,255,255,.06);color:var(--t)}
.side-l{flex:1;overflow-y:auto;padding:8px}
.side-i{padding:8px 12px;border-radius:8px;cursor:pointer;transition:.12s;margin-bottom:2px;font-size:12px;color:var(--t2);display:flex;align-items:center;gap:6px}
.side-i:hover{background:rgba(255,255,255,.05);color:var(--t)}
.so{position:absolute;inset:0;z-index:50;background:rgba(0,0,0,.9);display:none;flex-direction:column;padding:16px}
.so.s{display:flex}
.so input{width:100%;padding:10px 14px;border-radius:10px;border:1px solid rgba(255,255,255,.08);background:rgba(255,255,255,.05);color:var(--t);font-size:14px;outline:none;font-family:inherit}
.so .sr{flex:1;overflow-y:auto;margin-top:10px}
.sri{padding:10px 12px;border-radius:8px;background:rgba(255,255,255,.03);cursor:pointer;font-size:12px;color:var(--t2);margin-bottom:3px}
.sri:hover{background:rgba(255,255,255,.06)}
.sh{position:absolute;inset:0;z-index:60;background:rgba(0,0,0,.8);backdrop-filter:blur(24px);display:none;flex-direction:column;align-items:center;justify-content:center;padding:40px}
.sh.s{display:flex}
.sh .c{background:rgba(28,28,32,.96);border-radius:22px;padding:24px;max-width:360px;width:100%;border:1px solid rgba(255,255,255,.05)}
.sh .c h2{font-size:16px;font-weight:600;margin-bottom:14px}
.sr2{display:flex;align-items:center;justify-content:space-between;padding:6px 0;font-size:12px;color:var(--t2);border-bottom:1px solid rgba(255,255,255,.03)}
.sr2:last-child{border-bottom:none}
.sr2 kbd{background:rgba(255,255,255,.06);padding:3px 8px;border-radius:5px;font-size:11px;font-family:inherit;color:var(--t);border:1px solid rgba(255,255,255,.04)}
.pg{position:absolute;inset:0;z-index:55;background:rgba(0,0,0,.93);backdrop-filter:blur(30px);display:none;flex-direction:column;padding:14px}
.pg.s{display:flex}
.pg-t{display:flex;gap:4px;margin-bottom:8px}
.pg-t button{padding:5px 12px;border-radius:7px;border:none;background:rgba(255,255,255,.04);color:var(--t2);font-size:11px;cursor:pointer;font-family:inherit}
.pg-t button.a{background:rgba(255,255,255,.09);color:var(--t)}
.pg-p{flex:1;display:none;flex-direction:column}
.pg-p.s{display:flex}
.pg-p textarea{flex:1;background:rgba(0,0,0,.3);border:1px solid rgba(255,255,255,.05);border-radius:9px;padding:10px;color:var(--t);font-family:monospace;font-size:12px;resize:none;outline:none}
.pg-p iframe{flex:1;background:#fff;border-radius:9px;border:none}
.pg-c{position:absolute;top:14px;right:14px;width:28px;height:28px;border-radius:50%;background:rgba(255,255,255,.08);border:none;color:#fff;font-size:12px;cursor:pointer;display:flex;align-items:center;justify-content:center}
.ctx{position:fixed;z-index:150;background:rgba(28,28,32,.96);backdrop-filter:blur(30px);border-radius:12px;border:1px solid rgba(255,255,255,.05);padding:4px;min-width:140px;display:none;box-shadow:0 8px 32px rgba(0,0,0,.5)}
.ctx.s{display:block}
.ctx button{display:block;width:100%;padding:7px 14px;border:none;background:none;color:var(--t2);font-size:12px;text-align:left;cursor:pointer;border-radius:7px;font-family:inherit}
.ctx button:hover{background:rgba(255,255,255,.05);color:var(--t)}
.ctx .sp{height:1px;background:rgba(255,255,255,.03);margin:4px 8px}
[d-t=ocean]{--bg2:#000d1a;--bg3:#001226;--g1:linear-gradient(135deg,#00b4d8,#0077b6)}
[d-t=sunset]{--bg2:#1a0005;--bg3:#28000a;--g1:linear-gradient(135deg,#f72585,#b5179e)}
[d-t=forest]{--bg2:#000a05;--bg3:#00120a;--g1:linear-gradient(135deg,#52b788,#2d6a4f)}
[d-t=neon]{--bg2:#04040e;--bg3:#080818;--g1:linear-gradient(135deg,#00ff88,#0088ff)}
[d-t=midnight]{--bg2:#080810;--bg3:#0e0e1a;--g1:linear-gradient(135deg,#89b4fa,#b4befe)}
[d-t=aurora]{--bg2:#000a14;--bg3:#001226;--g1:linear-gradient(135deg,#00f5d4,#f15bb5)}
[d-t=candy]{--bg2:#12000a;--bg3:#1c0010;--g1:linear-gradient(135deg,#ff6b6b,#ffd43b)}
[d-t=mono]{--bg2:#040404;--bg3:#0a0a0a;--g1:linear-gradient(135deg,#888,#555)}
[d-t=ios]{--bg2:#f2f2f7;--bg3:#e5e5ea;--t:#000;--t2:#666;--t3:#999;--t4:#bbb}
[d-t=android]{--bg2:#1c1b1f;--bg3:#2b2930;--g1:linear-gradient(135deg,#d0bcff,#381e72);--t:#e6e1e5;--t2:#938f99;--t3:#7a7585}
@media(prefers-color-scheme:light){.app{background:#f2f2f7}.hdr{background:rgba(255,255,255,.7)}.msg.a .b{background:rgba(255,255,255,.7);border-color:rgba(0,0,0,.05)}.inp-i{background:rgba(255,255,255,.8);border-color:rgba(0,0,0,.08)}.inp-i textarea::placeholder{color:#aaa}.set{background:rgba(245,245,247,.96)}.mbar{background:#e5e5ea}.mbar select{background-color:rgba(0,0,0,.05);color:#000}.side{background:rgba(245,245,247,.98)}.toast{background:rgba(245,245,247,.94);color:#000}.sh .c{background:rgba(245,245,247,.96)}.ctx{background:rgba(245,245,247,.96)}.tg button.a{border-color:#000}}
@media(max-width:400px){.hdr{padding:8px 12px;min-height:44px}.hdr h1{font-size:14px}.mbar{padding:4px 12px}.mbar select{min-width:90px;font-size:11px}.msgs{padding:8px 10px 4px}.msg .b{padding:7px 10px;font-size:13px}.inp-w{padding:4px 10px 10px}.inp-i textarea{font-size:15px}.inp-i{border-radius:18px;padding:2px 2px 2px 10px}.welcome{padding:24px 14px 14px}.welcome .ic{width:48px;height:48px;font-size:22px}}
</style>
</head>
<body>
<div class="rgb-bg"></div>
<div class="app">
  <div class="hdr">
    <button style="background:none;border:none;color:var(--t2);font-size:16px;padding:4px;cursor:pointer;border-radius:6px" onclick="tSide()">☰</button>
    <h1>SXIGOai</h1>
    <div class="act">
      <button onclick="tSrch()">🔍</button>
      <button onclick="tPG()">▶</button>
      <button onclick="tShort()">⌘</button>
      <button onclick="newChat()">✕</button>
      <button onclick="tSet()">⚙</button>
    </div>
  </div>
  <div class="mbar">
    <span class="l">Model</span>
    <span class="d g" id="mD"></span>
    <span class="st" id="mS">ready</span>
    <select id="mSel">__MODELS__</select>
  </div>
  <div class="msgs" id="msgs">
    <div class="msgs-in" id="msgsIn">
      <div class="welcome" id="welc">
        <div class="ic">✦</div>
        <h2>SXIGOai</h2>
        <p>Premium AI chat • instant streaming<br>powered by your local Ollama models</p>
        <div class="chips">
          <button onclick="qp('Hello! Who are you?')">👋 Hello</button>
          <button onclick="qp('Explain quantum computing simply')">⚛ Quantum</button>
          <button onclick="qp('Write a poem about AI')">📝 Poem</button>
          <button onclick="qp('What is the meaning of life?')">🌌 Life</button>
        </div>
        <div class="tips">Select a model above & start chatting</div>
      </div>
    </div>
  </div>
  <div class="inp-w">
    <div class="inp-i">
      <textarea id="inp" rows="1" placeholder="Message SXIGOai..." onkeydown="onK(event)"></textarea>
      <button class="s" onclick="document.getElementById('fI').click()">📎</button>
      <input type="file" id="fI" style="display:none" multiple onchange="onF(this.files)">
      <div class="sd"><button id="sB" onclick="snd()">↑</button></div>
    </div>
    <div class="inp-e">
      <span onclick="vIn()">🎤 Voice</span>
      <span onclick="clearChat()">🗑 Clear</span>
      <span onclick="exp('md')">📥 Export</span>
    </div>
  </div>
</div>

<div class="side" id="side">
  <div class="side-h"><h3>History</h3><button onclick="tSide()">✕</button></div>
  <div class="side-l" id="sideL"></div>
</div>

<div class="over" id="over" onclick="tSet()"></div>
<div class="set" id="set">
  <div class="gr"></div>
  <h2>Settings</h2>
  <div class="sg"><label>Server URL</label><input type="text" id="sv" value="http://localhost:11434" placeholder="http://localhost:11434"></div>
  <div class="sg"><label>Default Model</label><select id="sM">__MODELS__</select></div>
  <div class="sg"><label>Temperature <span id="tpV" style="color:var(--t)">0.7</span></label><div class="sl"><input type="range" id="tp" min="0" max="2" step="0.05" value="0.7"></div></div>
  <div class="sg"><label>Max Tokens <span id="tkV" style="color:var(--t)">2048</span></label>
    <div style="display:flex;gap:6px;align-items:center">
      <input type="range" id="tkR" min="128" max="32768" step="128" value="2048" style="flex:1;-webkit-appearance:none;height:3px;border-radius:2px;background:rgba(255,255,255,.1)">
      <input type="number" id="tkN" value="2048" min="128" max="999999" style="width:80px;padding:6px 8px;border-radius:7px;border:1px solid rgba(255,255,255,.06);background:rgba(255,255,255,.05);color:var(--t);font-size:12px;font-family:inherit;text-align:center">
    </div>
  </div>
  <div class="sg"><label>Theme</label><div class="tg" id="tG"></div></div>
</div>

<div class="tc" id="tc"></div>
<script>
var m='qwen2.5-coder:7b',u='http://localhost:11434',tp=0.7,mt=2048,th='default',ab=null,st=false,cv=[],cl=[],ci=Date.now().toString();
try{var s=JSON.parse(localStorage.getItem('sx'));if(s){u=s.u||u;m=s.m||m;tp=s.t??0.7;mt=s.tk||2048;th=s.th||th}}catch(e){}
document.documentElement.setAttribute('d-t',th);
u=u.replace(/[^\x00-\x7f]/g,'');
var ts=[{i:'default',g:'linear-gradient(135deg,#667eea,#764ba2)'},{i:'ocean',g:'linear-gradient(135deg,#00b4d8,#0077b6)'},{i:'sunset',g:'linear-gradient(135deg,#f72585,#b5179e)'},{i:'forest',g:'linear-gradient(135deg,#52b788,#2d6a4f)'},{i:'neon',g:'linear-gradient(135deg,#00ff88,#0088ff)'},{i:'midnight',g:'linear-gradient(135deg,#89b4fa,#b4befe)'},{i:'aurora',g:'linear-gradient(135deg,#00f5d4,#f15bb5)'},{i:'candy',g:'linear-gradient(135deg,#ff6b6b,#ffd43b)'},{i:'mono',g:'linear-gradient(135deg,#888,#555)'},{i:'ios',g:'linear-gradient(135deg,#007aff,#5856d6)'},{i:'android',g:'linear-gradient(135deg,#d0bcff,#381e72)'}];
var tg=document.getElementById('tG');if(tg){ts.forEach(function(t){var b=document.createElement('button');b.style.background=t.g;b.onclick=function(){sT(t.i)};var l=document.createElement('span');l.className='lb';l.textContent=t.i;b.appendChild(l);if(t.i===th)b.classList.add('a');tg.appendChild(b)})}
var ms=document.getElementById('mSel'),sm=document.getElementById('sM');
if(ms)ms.value=m;if(sm)sm.value=m;
var sv=document.getElementById('sv');if(sv)sv.value=u;
var te=document.getElementById('tp');if(te){te.value=tp;var tv=document.getElementById('tpV');if(tv)tv.textContent=tp}
var tkr=document.getElementById('tkR'),tkn=document.getElementById('tkN');
if(tkr){tkr.value=mt}if(tkn){tkn.value=mt}
function svS(){try{localStorage.setItem('sx',JSON.stringify({u:u,m:m,t:tp,tk:mt,th:th}))}catch(e){}}
if(ms)ms.onchange=function(){m=this.value;if(sm)sm.value=this.value;svS();tst('Model: '+m)};
if(sm)sm.onchange=function(){m=this.value;if(ms)ms.value=this.value;svS();tst('Model: '+m)};
if(sv)sv.onchange=function(){u=this.value.replace(/[^\x00-\x7f]/g,'');svS()};
if(te){te.oninput=function(){tp=parseFloat(this.value);var tv=document.getElementById('tpV');if(tv)tv.textContent=tp;svS()}}
if(tkr){tkr.oninput=function(){mt=parseInt(this.value);if(tkn)tkn.value=mt;var tv=document.getElementById('tkV');if(tv)tv.textContent=mt;svS()}}
if(tkn){tkn.onchange=function(){var v=parseInt(this.value)||2048;if(v<128)v=128;this.value=v;mt=v;if(tkr)tkr.value=v;var tv=document.getElementById('tkV');if(tv)tv.textContent=v;svS()}}
function sT(t){th=t;document.documentElement.setAttribute('d-t',t);svS();if(tg)tg.querySelectorAll('button').forEach(function(b){b.classList.toggle('a',b.textContent.trim()===t)})}
function tst(m){var c=document.getElementById('tc'),t=document.createElement('div');t.className='toast';t.textContent=m;c.appendChild(t);setTimeout(function(){t.style.opacity='0';t.style.transition='.25s';setTimeout(function(){t.remove()},250)},2000)}
function tSet(){var p=document.getElementById('set'),o=document.getElementById('over');if(p)p.classList.toggle('s');if(o)o.classList.toggle('s')}
function tSide(){document.getElementById('side').classList.toggle('s')}
function addMsg(r,c){var i=document.getElementById('msgsIn'),w=document.getElementById('welc');if(w)w.style.display='none';var d=document.createElement('div');d.className='msg '+(r==='u'?'u':'a');var a=document.createElement('div');a.className='av';a.textContent=r==='u'?'👤':'✦';var b=document.createElement('div');b.className='b';b.innerHTML=c;var tm=document.createElement('div');tm.className='tm';tm.textContent=new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});b.appendChild(tm);if(r==='u'){d.appendChild(b);d.appendChild(a)}else{d.appendChild(a);d.appendChild(b)}i.appendChild(d);sB();return b}
function sB(){requestAnimationFrame(function(){var m=document.getElementById('msgs');if(m)m.scrollTop=m.scrollHeight})}
function es(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function fm(t){return es(t).replace(/\n/g,'<br>').replace(/### (.+)/g,'<h3>$1</h3>').replace(/## (.+)/g,'<h2>$1</h2>').replace(/# (.+)/g,'<h1>$1</h1>').replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>').replace(/\*(.+?)\*/g,'<em>$1</em>').replace(/```(\w*)\n([\s\S]*?)```/g,'<pre><code>$2</code></pre>').replace(/`(.+?)`/g,'<code>$1</code>').replace(/^\- (.+)/gm,'<li>$1</li>').replace(/^\d+\. (.+)/gm,'<li>$1</li>')}
function onK(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();snd()}}
function qp(t){document.getElementById('inp').value=t;snd()}
async function snd(){if(st)return;var i=document.getElementById('inp'),t=i.value.trim();if(!t)return;i.value='';i.style.height='auto';addMsg('u','<p>'+es(t)+'</p>');var b=addMsg('a','<div class="typing"><span></span><span></span><span></span></div>');sB();st=true;var btn=document.getElementById('sB');if(btn){btn.textContent='■';btn.style.background='#ff453a'};ab=new AbortController();try{var r=await fetch(u+'/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model:m,messages:[{role:'user',content:t}],stream:true,options:{temperature:tp}}),signal:ab.signal});if(!r.ok){b.innerHTML='<p style="color:#ff453a">Error '+r.status+'</p>';st=false;rB();return}var rd=r.body.getReader(),dc=new TextDecoder(),full='',buf='';while(true){var rr=await rd.read();if(rr.done)break;var ch=dc.decode(rr.value,{stream:true});buf+=ch;var ls=buf.split('\n');buf=ls.pop()||'';for(var i=0;i<ls.length;i++){var ln=ls[i].trim();if(!ln)continue;try{var j=JSON.parse(ln);if(j.message&&j.message.content){full+=j.message.content;b.innerHTML=fm(full)+'<span class="cb">|</span>';sB()}}catch(e){}}}if(buf.trim()){try{var j=JSON.parse(buf);if(j.message&&j.message.content){full+=j.message.content;b.innerHTML=fm(full)}}catch(e){}}b.innerHTML=fm(full);cv.push({role:'user',content:t},{role:'assistant',content:full});svC()}catch(e){if(e.name==='AbortError'){b.innerHTML=fm(full)+'<br><em style="color:var(--t3)">[stopped]</em>'}else{b.innerHTML='<p style="color:#ff453a">'+es(e.message)+'</p>'}}st=false;rB()}
function rB(){var btn=document.getElementById('sB');if(btn){btn.textContent='↑';btn.style.background=''}}
function newChat(){if(cv.length>0)svCur();if(st&&ab){ab.abort();st=false;rB()}ci=Date.now().toString();document.getElementById('msgsIn').innerHTML='<div class="welcome" id="welc"><div class="ic">✦</div><h2>SXIGOai</h2><p>Premium AI chat • instant streaming<br>powered by your local Ollama models</p><div class="chips"><button onclick="qp(\\'Hello! Who are you?\\')">👋 Hello</button><button onclick="qp(\\'Explain quantum computing simply\\')">⚛ Quantum</button><button onclick="qp(\\'Write a poem about AI\\')">📝 Poem</button><button onclick="qp(\\'What is the meaning of life?\\')">🌌 Life</button></div><div class="tips">Select a model above & start chatting</div></div>';cv=[]}
function clearChat(){newChat();tst('Cleared')}
function svC(){try{localStorage.setItem('sx_c_'+ci,JSON.stringify(cv))}catch(e){svCur()}}
function svCur(){var t=cv.length>0?es(cv[0].content).slice(0,35):'Chat';var ex=cl.findIndex(function(c){return c.id===ci});if(ex>=0){cl[ex].title=t;cl[ex].ts=Date.now()}else{cl.push({id:ci,title:t,ts:Date.now()})};try{localStorage.setItem('sx_l',JSON.stringify(cl))}catch(e){};rSide()}
function rSide(){var l=document.getElementById('sideL');if(!l)return;l.innerHTML='';cl.slice().reverse().forEach(function(c){var i=document.createElement('div');i.className='side-i';i.innerHTML='<span>💬</span><span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+es(c.title||'Chat')+'</span>';i.onclick=function(){lC(c.id)};l.appendChild(i)})}
function lC(id){if(cv.length>0)svCur();try{var d=JSON.parse(localStorage.getItem('sx_c_'+id));if(d&&d.length){cv=d;ci=id;document.getElementById('msgsIn').innerHTML='';cv.forEach(function(m){addMsg(m.role==='user'?'u':'a',m.content)})}}catch(e){};var s=document.getElementById('side');if(s)s.classList.remove('s')}
try{var cl_=JSON.parse(localStorage.getItem('sx_l'));if(cl_&&cl_.length){cl=cl_;rSide()}}catch(e){}
function tSrch(){var el=document.getElementById('sO');if(!el){el=document.createElement('div');el.id='sO';el.className='so';el.innerHTML='<input id="sI" placeholder="Search..." oninput="doS(this.value)" onkeydown="if(event.key===\\'Escape\\')this.parentElement.classList.remove(\\'s\\')"><div class="sr" id="sR"></div>';document.querySelector('.app').appendChild(el)}el.classList.toggle('s');if(el.classList.contains('s'))setTimeout(function(){document.getElementById('sI').focus()},100)}
function doS(q){var r=document.getElementById('sR');if(!q.trim()){r.innerHTML='';return}var ma=[];cv.forEach(function(msg,i){if(msg.content.toLowerCase().includes(q.toLowerCase())){ma.push({i:i,r:msg.role,c:msg.content,p:msg.content.slice(0,100)})}});r.innerHTML=ma.length?ma.map(function(x){return'<div class="sri" onclick="jM('+x.i+')"><strong>'+es(x.r)+'</strong>: '+es(x.p)+'</div>'}):'<div style="text-align:center;padding:16px;color:#555">No results</div>'}
function jM(idx){var m=document.querySelectorAll('.msg');if(m[idx]){m[idx].scrollIntoView({behavior:'smooth',block:'center'});m[idx].style.transition='background .4s';m[idx].style.background='rgba(102,126,234,.12)';setTimeout(function(){m[idx].style.background=''},1500)}var el=document.getElementById('sO');if(el)el.classList.remove('s')}
function tShort(){var el=document.getElementById('shM');if(!el){el=document.createElement('div');el.id='shM';el.className='sh';el.innerHTML='<div class="c"><h2>Keyboard Shortcuts</h2><div class="sr2"><span>New chat</span><kbd>⌘N</kbd></div><div class="sr2"><span>Search</span><kbd>⌘⇧F</kbd></div><div class="sr2"><span>Settings</span><kbd>⌘,</kbd></div><div class="sr2"><span>Playground</span><kbd>⌘⇧P</kbd></div><div class="sr2"><span>Sidebar</span><kbd>⌘B</kbd></div><div class="sr2"><span>Clear</span><kbd>⌘⇧C</kbd></div><div style="text-align:center;margin-top:14px"><button onclick="this.parentElement.parentElement.parentElement.classList.remove(\\'s\\')" style="padding:7px 24px;border-radius:9px;border:none;background:var(--g1);color:#fff;cursor:pointer;font-family:inherit;font-size:13px">Close</button></div></div>';document.querySelector('.app').appendChild(el)}el.classList.toggle('s')}
function tPG(){var el=document.getElementById('pG');if(!el){el=document.createElement('div');el.id='pG';el.className='pg';el.innerHTML='<button class="pg-c" onclick="this.parentElement.classList.remove(\\'s\\')">✕</button><div class="pg-t"><button class="a" onclick="swPG(\\'html\\',this)">HTML</button><button onclick="swPG(\\'css\\',this)">CSS</button><button onclick="swPG(\\'js\\',this)">JS</button><button onclick="swPG(\\'pv\\',this)">▶</button></div><div class="pg-p s" id="pH"><textarea id="pHt" placeholder="HTML..."></textarea></div><div class="pg-p" id="pC"><textarea id="pCt" placeholder="CSS..."></textarea></div><div class="pg-p" id="pJ"><textarea id="pJt" placeholder="JS..."></textarea></div><div class="pg-p" id="pP"><iframe id="pF"></iframe></div>';document.querySelector('.app').appendChild(el)}el.classList.toggle('s');upPG()}
function swPG(t,btn){document.querySelectorAll('.pg-p').forEach(function(p){p.classList.remove('s')});document.querySelectorAll('.pg-t button').forEach(function(b){b.classList.remove('a')});var ids={html:'pH',css:'pC',js:'pJ',pv:'pP'};document.getElementById(ids[t]).classList.add('s');if(btn)btn.classList.add('a');if(t==='pv')upPG()}
function upPG(){var h=document.getElementById('pHt').value||'',c=document.getElementById('pCt').value||'',j=document.getElementById('pJt').value||'',f=document.getElementById('pF'),d=f.contentDocument||f.contentWindow.document;d.open();d.write('<!DOCTYPE html><html><head><style>'+c+'</style></head><body>'+h+'<script>'+j+'<\\/script></body></html>');d.close()}
function exp(f){if(!cv.length){tst('Nothing to export');return}var tx='';if(f==='md'){tx='# SXIGOai\n\n';cv.forEach(function(m){tx+='**'+m.role+'**: '+m.content+'\n\n'})}else{tx=JSON.stringify({date:new Date().toISOString(),model:m,messages:cv},null,2)}var ext=f==='md'?'md':'json';var b=new Blob([tx],{type:'text/plain'}),u_=URL.createObjectURL(b),a=document.createElement('a');a.href=u_;a.download='sxigo.'+ext;a.click();URL.revokeObjectURL(u_);tst('Exported')}
function vIn(){var SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR){tst('Voice unsupported');return}var r=new SR();r.lang='ko-KR';r.interimResults=true;tst('Listening...');r.onresult=function(e){var t='';for(var i=e.resultIndex;i<e.results.length;i++){t+=e.results[i][0].transcript}document.getElementById('inp').value+=t};r.onend=function(){tst('Voice done')};r.onerror=function(e){tst('Voice: '+e.error)};r.start()}
function onF(files){if(!files.length)return;var n=Array.from(files).map(function(f){return f.name}).join(', ');var i=document.getElementById('inp');if(i)i.value+=' [Attached: '+n+'] ';tst('Attached: '+files.length+' file(s)')}
document.addEventListener('contextmenu',function(e){var b=e.target.closest('.b');if(b){e.preventDefault();var m=document.getElementById('cM');if(!m){m=document.createElement('div');m.id='cM';m.className='ctx';m.innerHTML='<button onclick="cMC(this)">Copy</button><button onclick="exp(\\'md\\')">Export</button><div class="sp"></div><button onclick="this.parentElement.classList.remove(\\'s\\')">Close</button>';document.body.appendChild(m)}m.style.left=Math.min(e.clientX,document.body.clientWidth-140)+'px';m.style.top=e.clientY+'px';m.classList.add('s');window._cT=b;setTimeout(function(){document.addEventListener('click',function h(){m.classList.remove('s');document.removeEventListener('click',h)},{once:true})},10)}});
function cMC(){var t=window._cT?window._cT.textContent:'';if(navigator.clipboard)navigator.clipboard.writeText(t).then(function(){tst('Copied')})}
async function ckS(){var d=document.getElementById('mD'),st=document.getElementById('mS');try{var r=await fetch(u.replace(/[^\x00-\x7f]/g,'')+'/api/version',{signal:AbortSignal.timeout(3000)});if(r.ok){var j=await r.json();if(d){d.className='d g'};if(st)st.textContent='v'+(j.version||'ok')}else{if(d)d.className='d r';if(st)st.textContent='err'}}catch(e){if(d){d.className='d r'};if(st)st.textContent='off'}}
ckS();setInterval(ckS,15000);
async function pullM(name){tst('Pulling '+name+'...');try{var r=await fetch(u.replace(/[^\x00-\x7f]/g,'')+'/api/pull',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:name,stream:true})});var rd=r.body.getReader(),dc=new TextDecoder();while(true){var rr=await rd.read();if(rr.done)break;var ls=dc.decode(rr.value,{stream:true}).split('\n').filter(function(l){return l.trim()});for(var i=0;i<ls.length;i++){try{var j=JSON.parse(ls[i]);if(j.status)tst(j.status)}catch(e){}}}ckS();tst('Pull complete!')}catch(e){tst('Pull failed: '+e.message)}}
var inp=document.getElementById('inp');if(inp){inp.focus();inp.addEventListener('input',function(){this.style.height='auto';this.style.height=Math.min(this.scrollHeight,100)+'px'})};
document.addEventListener('paste',function(e){var fl=e.clipboardData.files;if(fl&&fl.length){var n=Array.from(fl).map(function(f){return f.name}).join(', ');var i=document.getElementById('inp');if(i)i.value+=' [Attached: '+n+'] ';tst('Attached '+(fl.length+' file(s)'))}});
document.addEventListener('keydown',function(e){var c=e.ctrlKey||e.metaKey,sh=e.shiftKey;if(c&&sh&&e.key==='F'){e.preventDefault();tSrch()}if(c&&sh&&e.key==='C'){e.preventDefault();clearChat()}if(c&&e.key==='b'){e.preventDefault();tSide()}if(c&&sh&&e.key==='P'){e.preventDefault();tPG()}if(c&&sh&&e.key==='/'){e.preventDefault();tShort()}if(c&&e.key==='n'){e.preventDefault();newChat()}if(c&&e.key===','){e.preventDefault();tSet()}if(e.key==='Escape'){var so=document.getElementById('sO');if(so&&so.classList.contains('s'))so.classList.remove('s');if(st&&ab){ab.abort();st=false;rB()};var sp=document.getElementById('set');if(sp&&sp.classList.contains('s'))tSet()}});
console.log('%cSXIGOai','font-size:16px;font-weight:bold;background:linear-gradient(135deg,#667eea,#764ba2);-webkit-background-clip:text;-webkit-text-fill-color:transparent');
</script>
</body>
</html>'''

html = html.replace('__MODELS__', MO)

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

line_count = html.count('\n')
print(f'Written: {line_count} lines')
print(f'Models: {len(models)}')
