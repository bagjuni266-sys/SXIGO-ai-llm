import os
path = r'C:\Users\gamju\AppData\Local\Temp\opencode\SXIGOai.html'

models = [
    "qwen2.5-coder:7b", "llama3:latest", "qwen3.5:9b",
    "llama3.2-vision:latest", "kimi-k2.6:cloud", "gpt-oss:20b",
    "llama3:8b", "deepseek-r1:8b", "llama3.1:8b",
    "deepseek-r1:latest", "phi4:latest", "qwen2.5:latest",
    "qwen:latest", "qwen3:8b", "phi4:14b",
    "deepseek-coder:6.7b", "qwen2.5:7b", "phi3:medium"
]

models_opts = '\n'.join(f'<option value="{m}">{m}</option>' for m in models)

html = r'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,maximum-scale=1,user-scalable=no">
<meta name="theme-color" content="#000">
<title>SXIGOai — Premium AI Chat</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{
  --s:14px;--r:14px;--r2:20px;--r3:28px;
  --bg:#000;--bg2:#0a0a0a;--bg3:#141414;--bg4:#1a1a1a;
  --t:#fff;--t2:#888;--t3:#555;
  --g1:linear-gradient(135deg,#667eea,#764ba2);
  --g2:linear-gradient(135deg,#f093fb,#f5576c,#4facfe);
  --gb:rgba(255,255,255,.06);--gb2:rgba(255,255,255,.04);
  --gl:0 8px 32px rgba(0,0,0,.5);
  --hue:0deg;
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI Variable","Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  font-size:var(--s);color:var(--t);
}
body{background:#000;overflow:hidden;height:100dvh;display:flex;align-items:center;justify-content:center}
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,.08);border-radius:2px}
.app{width:100%;height:100dvh;max-width:1200px;display:flex;flex-direction:column;background:var(--bg2);position:relative;overflow:hidden;margin:0 auto}
@media(min-width:768px){.app{border-radius:var(--r3);margin:12px auto;height:calc(100dvh - 24px);box-shadow:0 20px 60px rgba(0,0,0,.6)}}

.rgb-bg{position:fixed;inset:0;z-index:0;overflow:hidden;pointer-events:none;background:radial-gradient(ellipse at 20% 50%,rgba(102,126,234,.12) 0,transparent 50%),radial-gradient(ellipse at 80% 20%,rgba(240,147,251,.1) 0,transparent 40%),radial-gradient(ellipse at 50% 80%,rgba(79,172,254,.08) 0,transparent 40%)}
.rgb-bg::before{content:'';position:absolute;inset:-50%;background:conic-gradient(from var(--hue) at 50% 50%,#667eea,#764ba2,#f093fb,#f5576c,#4facfe,#00f5d4,#667eea);opacity:.03;animation:rgbSpin 8s linear infinite}
@keyframes rgbSpin{to{--hue:360deg}}
@property --hue{syntax:'<angle>';initial-value:0deg;inherits:false}

.glass{background:var(--gb);backdrop-filter:blur(20px) saturate(1.4);-webkit-backdrop-filter:blur(20px) saturate(1.4);border:1px solid var(--gb2);border-radius:var(--r2)}

.chat-header{display:flex;align-items:center;gap:10px;padding:10px 16px;min-height:52px;background:rgba(0,0,0,.4);backdrop-filter:blur(30px);-webkit-backdrop-filter:blur(30px);border-bottom:1px solid rgba(255,255,255,.04);z-index:10}
.chat-header .back-btn{display:none;background:none;border:none;color:var(--t);font-size:22px;padding:4px;cursor:pointer;border-radius:8px}
.chat-header .back-btn:hover{background:rgba(255,255,255,.08)}
@media(max-width:767px){.chat-header .back-btn{display:block}}
.chat-header h1{font-size:15px;font-weight:600;flex:1;background:var(--g1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.chat-header .hdr-actions{display:flex;gap:6px;align-items:center}
.chat-header .hdr-btn{background:rgba(255,255,255,.06);border:none;color:var(--t2);width:32px;height:32px;border-radius:8px;font-size:15px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:.2s}
.chat-header .hdr-btn:hover{background:rgba(255,255,255,.12);color:var(--t)}

.model-bar{display:flex;align-items:center;gap:8px;padding:8px 16px;background:var(--bg3);border-bottom:1px solid rgba(255,255,255,.04);z-index:9;overflow-x:auto}
.model-bar select{-webkit-appearance:none;appearance:none;background:rgba(255,255,255,.06);border:none;border-radius:10px;color:var(--t);font-size:13px;padding:6px 28px 6px 12px;cursor:pointer;min-width:160px;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23888' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 8px center;font-family:inherit}
.model-bar select:hover{background:rgba(255,255,255,.1)}
.model-bar .model-label{font-size:12px;color:var(--t3);white-space:nowrap}
.model-bar .status-dot{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.model-bar .status-dot.online{background:#30d158}
.model-bar .status-dot.offline{background:#ff453a}
.model-bar .status-text{font-size:11px;color:var(--t3);white-space:nowrap}

.msgs{flex:1;overflow-y:auto;overflow-x:hidden;padding:12px 12px 8px;scroll-behavior:smooth}
.msgs-inner{max-width:720px;margin:0 auto;display:flex;flex-direction:column;gap:6px}
.welcome{text-align:center;padding:40px 20px;display:flex;flex-direction:column;align-items:center;gap:12px}
.welcome .icon{width:72px;height:72px;border-radius:22px;background:var(--g1);display:flex;align-items:center;justify-content:center;font-size:32px;box-shadow:0 8px 32px rgba(102,126,234,.3)}
.welcome h2{font-size:20px;font-weight:600}
.welcome p{font-size:14px;color:var(--t2);line-height:1.5;max-width:360px}
.welcome .tips{font-size:12px;color:var(--t3);margin-top:8px}

.msg{display:flex;gap:10px;padding:4px 16px 4px 8px;animation:fadeUp .3s ease}
@keyframes fadeUp{from{opacity:0;transform:translateY(8px)}}
.msg.user{flex-direction:row-reverse}
.msg .avatar{width:28px;height:28px;border-radius:10px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:13px;margin-top:2px}
.msg.user .avatar{background:var(--g1)}
.msg.assistant .avatar{background:var(--g2)}
.msg .bubble{max-width:85%;padding:10px 14px;border-radius:16px;font-size:14px;line-height:1.55;word-wrap:break-word;position:relative}
.msg.user .bubble{background:linear-gradient(135deg,#667eea,#764ba2);border-bottom-right-radius:4px;color:#fff}
.msg.assistant .bubble{background:rgba(255,255,255,.06);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,.04);border-bottom-left-radius:4px;color:var(--t)}
.msg .bubble p{margin:4px 0}
.msg .bubble p:first-child{margin-top:0}
.msg .bubble p:last-child{margin-bottom:0}
.msg .bubble pre{background:rgba(0,0,0,.3);border-radius:10px;padding:12px;overflow-x:auto;margin:8px 0;font-size:13px}
.msg .bubble code{font-family:"SF Mono","Cascadia Code","JetBrains Mono",monospace;font-size:13px}
.msg .bubble :not(pre)>code{background:rgba(255,255,255,.08);padding:2px 6px;border-radius:4px}
.msg .time{font-size:10px;color:var(--t3);margin-top:4px;text-align:right}
.msg.user .time{color:rgba(255,255,255,.5)}
.typing-dots{display:flex;gap:4px;padding:6px 0}
.typing-dots span{width:6px;height:6px;border-radius:50%;background:var(--t3);animation:typing 1.4s infinite}
.typing-dots span:nth-child(2){animation-delay:.2s}
.typing-dots span:nth-child(3){animation-delay:.4s}
@keyframes typing{0%,60%,100%{opacity:.3}30%{opacity:1}}

.input-wrap{padding:8px 12px 14px;z-index:10;background:linear-gradient(0deg,rgba(0,0,0,.95) 60%,transparent)}
.input-inner{display:flex;align-items:flex-end;gap:8px;background:rgba(255,255,255,.06);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.08);border-radius:22px;padding:4px 4px 4px 16px;transition:.2s}
.input-inner:focus-within{border-color:rgba(102,126,234,.3);background:rgba(255,255,255,.08)}
.input-inner textarea{flex:1;background:none;border:none;outline:none;color:var(--t);font-size:15px;font-family:inherit;resize:none;max-height:120px;line-height:1.4;padding:8px 0}
.input-inner textarea::placeholder{color:var(--t3)}
.input-inner .send-btn{width:36px;height:36px;border-radius:50%;flex-shrink:0;background:var(--g1);border:none;color:#fff;font-size:16px;cursor:pointer;transition:.2s;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(102,126,234,.3)}
.input-inner .send-btn:hover{transform:scale(1.05);box-shadow:0 6px 20px rgba(102,126,234,.4)}
.input-inner .send-btn:active{transform:scale(.95)}
.input-inner .attach-btn{width:32px;height:32px;border-radius:50%;flex-shrink:0;background:none;border:none;color:var(--t3);font-size:16px;cursor:pointer;transition:.2s;display:flex;align-items:center;justify-content:center}
.input-inner .attach-btn:hover{color:var(--t2);background:rgba(255,255,255,.06)}
.input-extras{display:flex;gap:6px;padding:6px 16px 0;font-size:11px;color:var(--t3)}
.input-extras span{cursor:pointer;padding:2px 8px;border-radius:6px;background:rgba(255,255,255,.04)}
.input-extras span:hover{background:rgba(255,255,255,.08)}

.overlay{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:100;opacity:0;pointer-events:none;transition:.3s}
.overlay.show{opacity:1;pointer-events:auto}
.settings-panel{position:fixed;left:0;bottom:0;width:100%;max-height:80dvh;background:rgba(30,30,30,.96);backdrop-filter:blur(40px);-webkit-backdrop-filter:blur(40px);border-radius:20px 20px 0 0;z-index:101;transform:translateY(100%);transition:.4s cubic-bezier(.32,.72,0,1);overflow-y:auto;padding:20px}
.settings-panel.show{transform:translateY(0)}
.settings-panel .grabber{width:36px;height:4px;border-radius:2px;background:rgba(255,255,255,.15);margin:0 auto 16px}
.settings-panel h2{font-size:18px;font-weight:600;margin-bottom:16px}
.settings-group{margin-bottom:20px}
.settings-group label{display:block;font-size:13px;color:var(--t2);margin-bottom:6px}
.settings-group select,.settings-group input[type=text]{width:100%;padding:10px 12px;border-radius:10px;border:1px solid rgba(255,255,255,.08);background:rgba(255,255,255,.06);color:var(--t);font-size:14px;font-family:inherit}
.settings-group select{appearance:none;-webkit-appearance:none}
.settings-group .slider-row{display:flex;align-items:center;gap:12px}
.settings-group input[type=range]{flex:1;-webkit-appearance:none;height:4px;border-radius:2px;background:rgba(255,255,255,.1)}
.settings-group input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:var(--g1);cursor:pointer}
.theme-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.theme-grid button{aspect-ratio:1;border-radius:12px;border:2px solid transparent;cursor:pointer;transition:.2s;font-size:0;position:relative}
.theme-grid button.active{border-color:#fff;transform:scale(1.05)}
.theme-grid button .label{position:absolute;bottom:4px;left:50%;transform:translateX(-50%);font-size:9px;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,.5);pointer-events:none}

.toast-container{position:fixed;top:20px;left:50%;transform:translateX(-50%);z-index:200;display:flex;flex-direction:column;gap:8px;pointer-events:none;align-items:center}
.toast{padding:10px 20px;border-radius:14px;font-size:13px;background:rgba(30,30,30,.92);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.08);color:var(--t);animation:toastIn .3s ease;pointer-events:auto;box-shadow:0 8px 24px rgba(0,0,0,.4)}
@keyframes toastIn{from{opacity:0;transform:translateY(-10px) scale(.95)}}

@media(min-width:768px){.msgs{padding:16px 24px 12px}.input-wrap{padding:8px 24px 16px}.input-inner{padding:6px 6px 6px 20px}.welcome{padding:60px 40px}.welcome .icon{width:80px;height:80px;font-size:36px}.welcome h2{font-size:24px}}
@media(min-width:1024px){.msgs-inner{max-width:760px}}
@media(max-width:480px){.msg .bubble{max-width:92%}.chat-header{padding:8px 12px}.model-bar{padding:6px 12px;gap:6px}.model-bar select{min-width:120px;font-size:12px}.settings-panel{padding:16px}}
@media(prefers-color-scheme:light){
  .app{background:#f2f2f7}
  .chat-header{background:rgba(255,255,255,.7)}
  :root{--t:#000;--t2:#666;--t3:#999;--bg2:#f2f2f7;--bg3:#e5e5ea;--gb:rgba(255,255,255,.7);--gb2:rgba(255,255,255,.8)}
  .msg.assistant .bubble{background:rgba(255,255,255,.7);border-color:rgba(0,0,0,.06)}
  .input-inner{background:rgba(255,255,255,.8);border-color:rgba(0,0,0,.1)}
  .input-inner textarea::placeholder{color:#999}
  .settings-panel{background:rgba(245,245,247,.96);--gb:rgba(0,0,0,.04);--gb2:rgba(0,0,0,.06)}
  .model-bar{background:rgba(0,0,0,.03)}
  .model-bar select{background-color:rgba(0,0,0,.06);color:#000}
}
</style>
</head>
<body>
<div class="rgb-bg"></div>
<div class="app">
  <div class="chat-header">
    <button class="back-btn" onclick="toggleSettings()">☰</button>
    <h1>SXIGOai</h1>
    <div class="hdr-actions">
      <button class="hdr-btn" onclick="newChat()" title="New chat">✕</button>
      <button class="hdr-btn" onclick="toggleSettings()" title="Settings">⚙</button>
    </div>
  </div>
  <div class="model-bar">
    <span class="model-label">Model</span>
    <span class="status-dot online" id="statusDot"></span>
    <span class="status-text" id="statusText">ready</span>
    <select id="modelSelect">''' + models_opts + '''</select>
  </div>
  <div class="msgs" id="msgs">
    <div class="msgs-inner" id="msgsInner">
      <div class="welcome" id="welcome">
        <div class="icon">✦</div>
        <h2>SXIGOai</h2>
        <p>Premium AI assistant powered by your local models.<br>Ask anything, get instant streaming responses.</p>
        <div class="tips">Select a model above and start chatting</div>
      </div>
    </div>
  </div>
  <div class="input-wrap">
    <div class="input-inner">
      <textarea id="input" rows="1" placeholder="Message..." onkeydown="onInputKey(event)"></textarea>
      <button class="attach-btn" onclick="document.getElementById('fileInput').click()" title="Attach file">📎</button>
      <input type="file" id="fileInput" style="display:none" multiple onchange="handleFiles(this.files)">
      <button class="send-btn" id="sendBtn" onclick="sendMessage()">↑</button>
    </div>
    <div class="input-extras">
      <span onclick="toggleVoice()">🎤 Voice</span>
      <span onclick="clearChat()">🗑 Clear</span>
    </div>
  </div>
</div>
<div class="overlay" id="overlay" onclick="toggleSettings()"></div>
<div class="settings-panel" id="settingsPanel">
  <div class="grabber"></div>
  <h2>Settings</h2>
  <div class="settings-group">
    <label>Server URL</label>
    <input type="text" id="serverUrl" value="http://localhost:11434">
  </div>
  <div class="settings-group">
    <label>Default Model</label>
    <select id="settingsModelSelect">''' + models_opts + '''</select>
  </div>
  <div class="settings-group">
    <label>Temperature</label>
    <div class="slider-row">
      <input type="range" id="temperature" min="0" max="2" step="0.1" value="0.7">
      <span id="tempVal">0.7</span>
    </div>
  </div>
  <div class="settings-group">
    <label>Max Tokens</label>
    <div class="slider-row">
      <input type="range" id="maxTokens" min="256" max="8192" step="256" value="2048">
      <span id="tokenVal">2048</span>
    </div>
  </div>
  <div class="settings-group">
    <label>Theme</label>
    <div class="theme-grid" id="themeGrid"></div>
  </div>
</div>
<div class="toast-container" id="toastContainer"></div>
<script>
var activeModel='qwen2.5-coder:7b',serverUrl='http://localhost:11434',temperature=0.7,maxTokens=2048,theme='default',abortCtrl=null,isStreaming=false,conversation=[];
try{var s=JSON.parse(localStorage.getItem('sxigo_settings'));if(s){serverUrl=s.url||serverUrl;activeModel=s.model||activeModel;temperature=s.temp??0.7;maxTokens=s.tokens||2048;theme=s.theme||theme}}catch(e){}
document.documentElement.setAttribute('data-theme',theme);
var themes=[{id:'default',g:'linear-gradient(135deg,#667eea,#764ba2)'},{id:'ocean',g:'linear-gradient(135deg,#00b4d8,#0077b6)'},{id:'sunset',g:'linear-gradient(135deg,#f72585,#b5179e)'},{id:'forest',g:'linear-gradient(135deg,#52b788,#2d6a4f)'},{id:'neon',g:'linear-gradient(135deg,#00ff88,#0088ff)'},{id:'midnight',g:'linear-gradient(135deg,#89b4fa,#b4befe)'},{id:'aurora',g:'linear-gradient(135deg,#00f5d4,#f15bb5)'},{id:'candy',g:'linear-gradient(135deg,#ff6b6b,#ffd43b)'}];
var tg=document.getElementById('themeGrid');
themes.forEach(function(t){var b=document.createElement('button');b.style.background=t.g;b.onclick=function(){setTheme(t.id)};var l=document.createElement('span');l.className='label';l.textContent=t.id;b.appendChild(l);if(t.id===theme)b.classList.add('active');tg.appendChild(b)});
var ms=document.getElementById('modelSelect'),sms=document.getElementById('settingsModelSelect');
ms.value=activeModel;sms.value=activeModel;
document.getElementById('serverUrl').value=serverUrl;
document.getElementById('temperature').value=temperature;document.getElementById('tempVal').textContent=temperature;
document.getElementById('maxTokens').value=maxTokens;document.getElementById('tokenVal').textContent=maxTokens;
function saveSettings(){localStorage.setItem('sxigo_settings',JSON.stringify({url:serverUrl,model:activeModel,temp:temperature,tokens:maxTokens,theme:theme}))}
ms.addEventListener('change',function(){activeModel=this.value;sms.value=this.value;saveSettings();showToast('Model: '+activeModel)});
sms.addEventListener('change',function(){activeModel=this.value;ms.value=this.value;saveSettings();showToast('Model: '+activeModel)});
document.getElementById('serverUrl').addEventListener('change',function(){serverUrl=this.value;saveSettings()});
document.getElementById('temperature').addEventListener('input',function(){temperature=parseFloat(this.value);document.getElementById('tempVal').textContent=temperature;saveSettings()});
document.getElementById('maxTokens').addEventListener('input',function(){maxTokens=parseInt(this.value);document.getElementById('tokenVal').textContent=maxTokens;saveSettings()});
function setTheme(t){theme=t;document.documentElement.setAttribute('data-theme',t);saveSettings();document.querySelectorAll('#themeGrid button').forEach(function(b){b.classList.toggle('active',b.textContent.trim().toLowerCase()===t)})}
function showToast(msg){var c=document.getElementById('toastContainer'),t=document.createElement('div');t.className='toast';t.textContent=msg;c.appendChild(t);setTimeout(function(){t.style.opacity='0';t.style.transition='.3s';setTimeout(function(){t.remove()},300)},2500)}
function toggleSettings(){document.getElementById('settingsPanel').classList.toggle('show');document.getElementById('overlay').classList.toggle('show')}
function addMessage(role,content){var inner=document.getElementById('msgsInner'),w=document.getElementById('welcome');if(w)w.style.display='none';var div=document.createElement('div');div.className='msg '+role;var a=document.createElement('div');a.className='avatar';a.textContent=role==='user'?'👤':'✦';var b=document.createElement('div');b.className='bubble';b.innerHTML=content;var t=document.createElement('div');t.className='time';t.textContent=new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});b.appendChild(t);if(role==='user'){div.appendChild(b);div.appendChild(a)}else{div.appendChild(a);div.appendChild(b)}inner.appendChild(div);scrollBottom();return b}
function scrollBottom(){requestAnimationFrame(function(){document.getElementById('msgs').scrollTop=document.getElementById('msgs').scrollHeight})}
function escapeHtml(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function marked(t){return escapeHtml(t).replace(/\\n/g,'<br>').replace(/### (.+)/g,'<h3>$1</h3>').replace(/## (.+)/g,'<h2>$1</h2>').replace(/# (.+)/g,'<h1>$1</h1>').replace(/\\*\\*(.+?)\\*\\*/g,'<strong>$1</strong>').replace(/\\*(.+?)\\*/g,'<em>$1</em>').replace(/\`\`\`(\\w*)\\n([\\s\\S]*?)\`\`\`/g,'<pre><code>$2</code></pre>').replace(/\`(.+?)\`/g,'<code>$1</code>').replace(/^\\- (.+)/gm,'<li>$1</li>').replace(/^\\d+\\. (.+)/gm,'<li>$1</li>')}
function onInputKey(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMessage()};var el=e.target;el.style.height='auto';el.style.height=Math.min(el.scrollHeight,120)+'px'}
async function sendMessage(){if(isStreaming)return;var input=document.getElementById('input'),text=input.value.trim();if(!text)return;input.value='';input.style.height='auto';addMessage('user','<p>'+escapeHtml(text)+'</p>');var bubble=addMessage('assistant','<div class="typing-dots"><span></span><span></span><span></span></div>');scrollBottom();isStreaming=true;document.getElementById('sendBtn').textContent='■';document.getElementById('sendBtn').style.background='#ff453a';abortCtrl=new AbortController();try{var res=await fetch(serverUrl+'/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model:activeModel,messages:[{role:'user',content:text}],stream:true,options:{temperature:temperature}}),signal:abortCtrl.signal});if(!res.ok){bubble.innerHTML='<p style="color:#ff453a">Error: '+res.status+'</p>';isStreaming=false;resetBtn();return}var reader=res.body.getReader(),dec=new TextDecoder(),full='';while(true){var rd=await reader.read();if(rd.done)break;var chunk=dec.decode(rd.value,{stream:true}),lines=chunk.split('\\n').filter(function(l){return l.trim()});for(var i=0;i<lines.length;i++){try{var j=JSON.parse(lines[i]);if(j.message&&j.message.content){full+=j.message.content;bubble.innerHTML=marked(full)+'<span style="animation:blink 1s infinite">|</span>';scrollBottom()}}catch(e){}}}bubble.innerHTML=marked(full);conversation.push({role:'user',content:text},{role:'assistant',content:full});try{localStorage.setItem('sxigo_conv',JSON.stringify(conversation))}catch(e){}}catch(e){if(e.name==='AbortError'){bubble.innerHTML=marked(full)+'<br><em style="color:var(--t3)">[stopped]</em>'}else{bubble.innerHTML='<p style="color:#ff453a">'+escapeHtml(e.message)+'</p>'}}isStreaming=false;resetBtn()}
function resetBtn(){var btn=document.getElementById('sendBtn');btn.textContent='↑';btn.style.background=''}
function newChat(){if(isStreaming&&abortCtrl){abortCtrl.abort();isStreaming=false;resetBtn()}document.getElementById('msgsInner').innerHTML='<div class="welcome" id="welcome"><div class="icon">✦</div><h2>SXIGOai</h2><p>Premium AI assistant powered by your local models.<br>Ask anything, get instant streaming responses.</p><div class="tips">Select a model above and start chatting</div></div>';conversation=[]}
function clearChat(){newChat();showToast('Chat cleared')}
function toggleVoice(){if(!('webkitSpeechRecognition'in window||'SpeechRecognition'in window)){showToast('Voice not supported');return}showToast('Voice: click mic in browser','info')}
function handleFiles(files){if(!files.length)return;var names=Array.from(files).map(function(f){return f.name}).join(', ');var input=document.getElementById('input');input.value+=' [Attached: '+names+'] ';input.focus();showToast('Attached: '+files.length+' file(s)')}
async function checkServer(){var dot=document.getElementById('statusDot'),txt=document.getElementById('statusText');try{var res=await fetch(serverUrl+'/api/version',{signal:AbortSignal.timeout(3000)});if(res.ok){var j=await res.json();dot.className='status-dot online';txt.textContent='v'+(j.version||'ok')}else{dot.className='status-dot offline';txt.textContent='error'}}catch(e){dot.className='status-dot offline';txt.textContent='offline'}}
checkServer();setInterval(checkServer,15000);
try{var cd=JSON.parse(localStorage.getItem('sxigo_conv'));if(cd&&cd.length){conversation=cd;cd.forEach(function(m){addMessage(m.role,m.content)})}}catch(e){}
var inp=document.getElementById('input');inp.focus();
inp.addEventListener('input',function(){this.style.height='auto';this.style.height=Math.min(this.scrollHeight,120)+'px'});
document.addEventListener('paste',function(e){var fl=e.clipboardData.files;if(fl.length)handleFiles(fl)});
document.addEventListener('keydown',function(e){if((e.ctrlKey||e.metaKey)&&e.key==='n'){e.preventDefault();newChat()}if((e.ctrlKey||e.metaKey)&&e.key===','){e.preventDefault();toggleSettings()}if(e.key==='Escape'){if(isStreaming&&abortCtrl){abortCtrl.abort();isStreaming=false;resetBtn()};var sp=document.getElementById('settingsPanel');if(sp.classList.contains('show'))toggleSettings()}});
console.log('%cSXIGOai','font-size:24px;font-weight:bold;background:linear-gradient(135deg,#667eea,#764ba2);-webkit-background-clip:text;-webkit-text-fill-color:transparent');
</script>
</body>
</html>'''

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

line_count = html.count('\n')
print(f'Complete rewrite done: {line_count} lines')
print(f'Models included: {len(models)}')
