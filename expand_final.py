path = r'C:\Users\gamju\AppData\Local\Temp\opencode\SXIGOai.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

css_extra = '''
:root[data-theme=ocean]{--bg:#000d1a;--bg2:#001429;--bg3:#001a33;--g1:linear-gradient(135deg,#00b4d8,#0077b6);--g2:linear-gradient(135deg,#90e0ef,#00b4d8,#0077b6);--hue:200deg}
:root[data-theme=sunset]{--bg:#1a0005;--bg2:#2a000a;--bg3:#3a000f;--g1:linear-gradient(135deg,#f72585,#b5179e);--g2:linear-gradient(135deg,#ff006e,#f72585,#b5179e);--hue:330deg}
:root[data-theme=forest]{--bg:#000a05;--bg2:#00140a;--bg3:#001e0f;--g1:linear-gradient(135deg,#52b788,#2d6a4f);--g2:linear-gradient(135deg,#95d5b2,#52b788,#2d6a4f);--hue:150deg}
:root[data-theme=neon]{--bg:#050510;--bg2:#0a0a1e;--bg3:#0f0f2a;--g1:linear-gradient(135deg,#00ff88,#0088ff);--g2:linear-gradient(135deg,#00ff88,#00ffcc,#0088ff);--hue:160deg}
:root[data-theme=midnight]{--bg:#0a0a14;--bg2:#10101e;--bg3:#161628;--g1:linear-gradient(135deg,#89b4fa,#b4befe);--g2:linear-gradient(135deg,#b4befe,#89b4fa,#7c3aed);--hue:230deg}
:root[data-theme=aurora]{--bg:#000a14;--bg2:#001428;--bg3:#001e3a;--g1:linear-gradient(135deg,#00f5d4,#f15bb5);--g2:linear-gradient(135deg,#00f5d4,#fee440,#f15bb5);--hue:180deg}
:root[data-theme=candy]{--bg:#14000a;--bg2:#1e0010;--bg3:#2a0016;--g1:linear-gradient(135deg,#ff6b6b,#ffd43b);--g2:linear-gradient(135deg,#ff6b6b,#ffd43b,#ff9ff3);--hue:350deg}
:root[data-theme=mono]{--bg:#050505;--bg2:#0a0a0a;--bg3:#111;--g1:linear-gradient(135deg,#888,#555);--g2:linear-gradient(135deg,#aaa,#888,#666);--hue:0deg}
.glass-1{background:rgba(255,255,255,.03);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.04);border-radius:16px}
.glass-2{background:rgba(255,255,255,.05);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,.06);border-radius:20px}
.glass-3{background:rgba(255,255,255,.07);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);border:1px solid rgba(255,255,255,.08);border-radius:24px}
.glass-4{background:rgba(255,255,255,.04);backdrop-filter:blur(32px);-webkit-backdrop-filter:blur(32px);border:1px solid rgba(255,255,255,.05);border-radius:28px}
.rgb-border{position:relative}
.rgb-border::before{content:'';position:absolute;inset:-2px;border-radius:inherit;background:conic-gradient(from var(--hue) at 50%50%,#667eea,#764ba2,#f093fb,#f5576c,#4facfe,#00f5d4,#667eea);z-index:-1;opacity:.6;animation:rgbSpin 4s linear infinite;padding:2px;-webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);-webkit-mask-composite:xor;mask-composite:exclude}
.rgb-text{background:linear-gradient(135deg,#667eea,#764ba2,#f093fb,#f5576c,#4facfe);background-size:200% 200%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:rgbText 3s ease infinite}
@keyframes rgbText{0%,100%{background-position:0 50%}50%{background-position:100% 50%}}
.rgb-glow::after{content:'';position:absolute;inset:-20px;border-radius:50%;background:conic-gradient(from var(--hue) at 50%50%,#667eea,#764ba2,#f093fb,#f5576c,#4facfe,#00f5d4,#667eea);opacity:.08;filter:blur(30px);animation:rgbSpin 6s linear infinite;z-index:-1;pointer-events:none}
.ios-header{display:flex;align-items:center;gap:8px;padding:12px 16px 8px}
.ios-header h1{font-size:28px;font-weight:700;letter-spacing:-.5px}
.ios-pill{display:inline-flex;align-items:center;gap:4px;padding:4px 12px;border-radius:20px;background:rgba(255,255,255,.06);font-size:12px;color:var(--t2);cursor:pointer;transition:.2s}
.ios-pill:hover{background:rgba(255,255,255,.1)}
.ios-pill.active{background:var(--g1);color:#fff}
.segmented-control{display:inline-flex;background:rgba(255,255,255,.06);border-radius:10px;padding:2px;gap:2px}
.segmented-control button{padding:4px 14px;border-radius:8px;border:none;background:transparent;color:var(--t2);font-size:12px;cursor:pointer;transition:.2s;font-family:inherit}
.segmented-control button.active{background:rgba(255,255,255,.1);color:var(--t)}
.ios-chip{display:inline-flex;align-items:center;gap:4px;padding:6px 12px;border-radius:8px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.06);font-size:12px;color:var(--t2);cursor:pointer;transition:.2s}
.ios-chip:hover{background:rgba(255,255,255,.08)}
.float-particle{position:absolute;border-radius:50%;pointer-events:none;opacity:.15;animation:float 20s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0) scale(1)}33%{transform:translateY(-20px) scale(1.05)}66%{transform:translateY(10px) scale(.95)}}
.depth-1{box-shadow:0 4px 12px rgba(0,0,0,.3)}.depth-2{box-shadow:0 8px 24px rgba(0,0,0,.4)}.depth-3{box-shadow:0 16px 48px rgba(0,0,0,.5)}.depth-4{box-shadow:0 32px 72px rgba(0,0,0,.6)}
.status-bar{display:flex;align-items:center;gap:12px;padding:4px 16px;font-size:10px;color:var(--t3);background:rgba(0,0,0,.2);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px)}
.status-bar .stat{display:flex;align-items:center;gap:4px}
.status-bar .stat-dot{width:4px;height:4px;border-radius:50%}
@media(min-width:768px){.sidebar{width:260px;flex-shrink:0;display:flex;flex-direction:column;background:var(--bg3);border-right:1px solid rgba(255,255,255,.04);z-index:10;overflow:hidden}.main-area{flex:1;display:flex;flex-direction:column;min-width:0}.chat-header{padding:12px 20px}.model-bar{padding:8px 20px}.input-wrap{padding:8px 20px 16px}.msgs{padding:16px 24px 8px}}
@media(max-width:767px){.sidebar{display:none}.app{flex-direction:column}}
.sidebar-header{padding:16px;display:flex;align-items:center;gap:8px;border-bottom:1px solid rgba(255,255,255,.04)}
.sidebar-header h2{font-size:14px;font-weight:600;color:var(--t2)}
.sidebar-header button{background:none;border:none;color:var(--t3);font-size:16px;cursor:pointer;margin-left:auto;width:28px;height:28px;border-radius:6px;display:flex;align-items:center;justify-content:center}
.sidebar-header button:hover{background:rgba(255,255,255,.06);color:var(--t)}
.sidebar-list{flex:1;overflow-y:auto;padding:8px}
.sidebar-item{padding:10px 12px;border-radius:10px;cursor:pointer;transition:.15s;margin-bottom:2px;font-size:13px;color:var(--t2);display:flex;align-items:center;gap:8px}
.sidebar-item:hover{background:rgba(255,255,255,.04);color:var(--t)}
.sidebar-item.active{background:rgba(255,255,255,.06);color:var(--t)}
.search-overlay{position:absolute;inset:0;background:rgba(0,0,0,.85);z-index:50;display:none;flex-direction:column;padding:20px}
.search-overlay.show{display:flex}
.search-overlay input{width:100%;padding:12px 16px;border-radius:12px;border:1px solid rgba(255,255,255,.1);background:rgba(255,255,255,.06);color:var(--t);font-size:16px;outline:none;font-family:inherit}
.search-results{flex:1;overflow-y:auto;margin-top:12px;display:flex;flex-direction:column;gap:8px}
.search-result-item{padding:12px;border-radius:10px;background:rgba(255,255,255,.04);cursor:pointer;font-size:13px;color:var(--t2)}
.search-result-item:hover{background:rgba(255,255,255,.08)}
.shortcuts-modal{position:absolute;inset:0;z-index:60;background:rgba(0,0,0,.8);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);display:none;flex-direction:column;align-items:center;justify-content:center;padding:40px}
.shortcuts-modal.show{display:flex}
.shortcuts-modal .modal-card{background:rgba(30,30,30,.96);border-radius:24px;padding:24px;max-width:400px;width:100%;max-height:80vh;overflow-y:auto;border:1px solid rgba(255,255,255,.06)}
.shortcuts-modal h2{font-size:18px;font-weight:600;margin-bottom:16px}
.shortcut-row{display:flex;align-items:center;justify-content:space-between;padding:8px 0;font-size:13px;color:var(--t2);border-bottom:1px solid rgba(255,255,255,.04)}
.shortcut-row kbd{background:rgba(255,255,255,.08);padding:4px 8px;border-radius:6px;font-size:11px;font-family:inherit;color:var(--t)}
.playground-overlay{position:absolute;inset:0;z-index:55;background:rgba(0,0,0,.9);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);display:none;flex-direction:column;padding:16px}
.playground-overlay.show{display:flex}
.playground-tabs{display:flex;gap:4px;margin-bottom:8px}
.playground-tabs button{padding:6px 14px;border-radius:8px;border:none;background:rgba(255,255,255,.04);color:var(--t2);font-size:12px;cursor:pointer;font-family:inherit}
.playground-tabs button.active{background:rgba(255,255,255,.1);color:var(--t)}
.playground-pane{flex:1;display:none;flex-direction:column}
.playground-pane.show{display:flex}
.playground-pane textarea{flex:1;background:rgba(0,0,0,.3);border:1px solid rgba(255,255,255,.06);border-radius:12px;padding:12px;color:var(--t);font-family:"SF Mono","Cascadia Code","JetBrains Mono",monospace;font-size:13px;resize:none;outline:none}
.playground-pane iframe{flex:1;background:#fff;border-radius:12px;border:none}
.playground-close{position:absolute;top:16px;right:16px;width:32px;height:32px;border-radius:50%;background:rgba(255,255,255,.1);border:none;color:#fff;font-size:16px;cursor:pointer;display:flex;align-items:center;justify-content:center}
.context-menu{position:fixed;z-index:150;background:rgba(30,30,30,.96);backdrop-filter:blur(30px);-webkit-backdrop-filter:blur(30px);border-radius:14px;border:1px solid rgba(255,255,255,.06);padding:4px;min-width:160px;display:none;box-shadow:0 8px 32px rgba(0,0,0,.5)}
.context-menu.show{display:block}
.context-menu button{display:block;width:100%;padding:8px 14px;border:none;background:none;color:var(--t2);font-size:13px;text-align:left;cursor:pointer;border-radius:8px;font-family:inherit}
.context-menu button:hover{background:rgba(255,255,255,.06);color:var(--t)}
.context-menu .sep{height:1px;background:rgba(255,255,255,.04);margin:4px 8px}
@keyframes slideUp{from{opacity:0;transform:translateY(12px)}}
@keyframes slideDown{from{opacity:0;transform:translateY(-12px)}}
@keyframes pop{0%{transform:scale(.8);opacity:0}70%{transform:scale(1.05)}100%{transform:scale(1);opacity:1}}
@keyframes shimmer{0%{background-position:-200% 0}100%{background-position:200% 0}}
@keyframes breathe{0%,100%{transform:scale(1)}50%{transform:scale(1.02)}}
@keyframes gradientShift{0%{background-position:0 50%}50%{background-position:100% 50%}100%{background-position:0 50%}}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}
.welcome .icon{animation:float 6s ease-in-out infinite}
.cursor-blink{animation:blink 1s step-end infinite}
@media(min-width:1440px){.app{max-width:1400px}.msgs-inner{max-width:840px}}
@media(max-width:767px){.chat-header h1{font-size:14px}.input-inner{border-radius:18px;padding:3px 3px 3px 12px}.input-inner textarea{font-size:16px;padding:6px 0}.input-wrap{padding:6px 10px 12px}.model-bar select{min-width:120px;font-size:12px}.welcome .icon{width:60px;height:60px;font-size:28px}.welcome h2{font-size:18px}.settings-panel{padding:16px;max-height:85dvh}}
@media(max-width:380px){.chat-header{padding:6px 10px}.model-bar{padding:4px 10px;gap:4px}.model-bar select{min-width:100px;font-size:11px;padding:4px 24px 4px 8px}.input-inner{padding:2px 2px 2px 8px;border-radius:14px}}
'''

js_extra = '''
var convList=[];try{convList=JSON.parse(localStorage.getItem('sxigo_conv_list'))}catch(e){}
if(!localStorage.getItem('sxigo_conv_list'))localStorage.setItem('sxigo_conv_list','[]');
function saveConvList(){try{localStorage.setItem('sxigo_conv_list',JSON.stringify(convList))}catch(e){}}
var currentConvId=Date.now().toString();
function renderSidebar(){var list=document.getElementById('sidebarList');if(!list)return;list.innerHTML='';convList.forEach(function(c,i){var item=document.createElement('div');item.className='sidebar-item';item.innerHTML='<span>\\uD83D\\uDCAC</span><span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+escapeHtml(c.title||'Chat '+(i+1))+'</span>';item.onclick=function(){loadConversationById(c.id)};list.appendChild(item)})}
function loadConversationById(id){try{var data=JSON.parse(localStorage.getItem('sxigo_conv_'+id));if(data&&data.length){conversation=data;currentConvId=id;document.getElementById('msgsInner').innerHTML='';conversation.forEach(function(m){addMessage(m.role,m.content)})}}catch(e){}}
function saveCurrentConversation(){var title=conversation.length>0?conversation[0].content.slice(0,40):'New Chat';var existing=convList.findIndex(function(c){return c.id===currentConvId});if(existing>=0){convList[existing].title=title;convList[existing].updated=Date.now()}else{convList.push({id:currentConvId,title:title,created:Date.now(),updated:Date.now()})};saveConvList();renderSidebar()}
var origNewChat=newChat;newChat=function(){if(conversation.length>0)saveCurrentConversation();if(isStreaming&&abortCtrl){abortCtrl.abort();isStreaming=false;resetBtn()};currentConvId=Date.now().toString();document.getElementById('msgsInner').innerHTML='<div class="welcome" id="welcome"><div class="icon">\\u2726</div><h2>SXIGOai</h2><p>Premium AI assistant powered by your local models.<br>Ask anything, get instant streaming responses.</p><div class="tips">Select a model above and start chatting</div></div>';conversation=[]};
var origSend=sendMessage;sendMessage=async function(){await origSend();if(conversation.length>0){saveCurrentConversation()}};
function toggleSearch(){var el=document.getElementById('searchOverlay');if(!el){el=document.createElement('div');el.id='searchOverlay';el.className='search-overlay';el.innerHTML='<input id="searchInput" placeholder="Search messages..." oninput="doSearch(this.value)" onkeydown="if(event.key===\\'Escape\\')this.parentElement.classList.remove(\\'show\\')"><div class="search-results" id="searchResults"></div>';document.querySelector('.main-area')||document.querySelector('.app');(document.querySelector('.main-area')||document.querySelector('.app')).appendChild(el)}el.classList.toggle('show');if(el.classList.contains('show')){setTimeout(function(){document.getElementById('searchInput').focus()},100)}}
function doSearch(q){var results=document.getElementById('searchResults');if(!q.trim()){results.innerHTML='';return}var matches=[];conversation.forEach(function(m,i){if(m.content.toLowerCase().includes(q.toLowerCase())){matches.push({idx:i,role:m.role,content:m.content,preview:m.content.slice(0,100)})}});results.innerHTML=matches.length?matches.map(function(m){return'<div class="search-result-item" onclick="jumpToMessage('+m.idx+')"><strong>'+escapeHtml(m.role)+'</strong>: '+escapeHtml(m.preview)+'</div>'}):'<div style="text-align:center;padding:20px;color:var(--t3)">No results</div>'}
function jumpToMessage(idx){var msgs=document.querySelectorAll('.msg');if(msgs[idx]){msgs[idx].scrollIntoView({behavior:'smooth',block:'center'});msgs[idx].style.transition='background .5s';msgs[idx].style.background='rgba(102,126,234,.1)';setTimeout(function(){msgs[idx].style.background=''},2000)}document.getElementById('searchOverlay').classList.remove('show')}
function toggleShortcuts(){var el=document.getElementById('shortcutsModal');if(!el){el=document.createElement('div');el.id='shortcutsModal';el.className='shortcuts-modal';el.innerHTML='<div class="modal-card"><h2>Keyboard Shortcuts</h2><div class="shortcut-row"><span>New chat</span><kbd>\\u2318N</kbd></div><div class="shortcut-row"><span>Settings</span><kbd>\\u2318,</kbd></div><div class="shortcut-row"><span>Search</span><kbd>\\u2318\\u21E7F</kbd></div><div class="shortcut-row"><span>Clear chat</span><kbd>\\u2318\\u21E7C</kbd></div><div class="shortcut-row"><span>Toggle sidebar</span><kbd>\\u2318B</kbd></div><div class="shortcut-row"><span>Playground</span><kbd>\\u2318\\u21E7P</kbd></div><div class="shortcut-row"><span>Shortcuts</span><kbd>\\u2318\\u21E7/</kbd></div><div class="shortcut-row"><span>Fullscreen</span><kbd>\\u2318\\u21E7F</kbd></div><div style="text-align:center;margin-top:16px"><button onclick="this.parentElement.parentElement.parentElement.classList.remove(\\'show\\')" style="padding:8px 24px;border-radius:10px;border:none;background:var(--g1);color:#fff;cursor:pointer;font-family:inherit">Close</button></div></div>';(document.querySelector('.main-area')||document.querySelector('.app')).appendChild(el)}el.classList.toggle('show')}
function togglePlayground(){var el=document.getElementById('playgroundOverlay');if(!el){el=document.createElement('div');el.id='playgroundOverlay';el.className='playground-overlay';el.innerHTML='<button class="playground-close" onclick="this.parentElement.classList.remove(\\'show\\')">\\u2715</button><div class="playground-tabs"><button class="active" onclick="switchPlaygroundTab(\\'html\\',this)">HTML</button><button onclick="switchPlaygroundTab(\\'css\\',this)">CSS</button><button onclick="switchPlaygroundTab(\\'js\\',this)">JS</button><button onclick="switchPlaygroundTab(\\'preview\\',this)">Preview</button></div><div class="playground-pane show" id="pgHtml"><textarea id="pgHtmlCode" placeholder="HTML here..."></textarea></div><div class="playground-pane" id="pgCss"><textarea id="pgCssCode" placeholder="CSS here..."></textarea></div><div class="playground-pane" id="pgJs"><textarea id="pgJsCode" placeholder="JS here..."></textarea></div><div class="playground-pane" id="pgPreview"><iframe id="pgFrame"></iframe></div>';(document.querySelector('.main-area')||document.querySelector('.app')).appendChild(el)}el.classList.toggle('show');updatePlayground()}
function switchPlaygroundTab(tab,btn){document.querySelectorAll('.playground-pane').forEach(function(p){p.classList.remove('show')});document.querySelectorAll('.playground-tabs button').forEach(function(b){b.classList.remove('active')});var id='pg'+tab.charAt(0).toUpperCase()+tab.slice(1);document.getElementById(id).classList.add('show');btn.classList.add('active');if(tab==='preview')updatePlayground()}
function updatePlayground(){var h=document.getElementById('pgHtmlCode').value||'',c=document.getElementById('pgCssCode').value||'',j=document.getElementById('pgJsCode').value||'',f=document.getElementById('pgFrame'),d=f.contentDocument||f.contentWindow.document;d.open();d.write('<!DOCTYPE html><html><head><style>'+c+'</style></head><body>'+h+'<script>'+j+'<\\/script></body></html>');d.close()}
function toggleFullscreen(){if(!document.fullscreenElement){document.documentElement.requestFullscreen()}else{document.exitFullscreen()}}
function exportChat(format){if(!conversation.length){showToast('No messages to export');return}var text='';if(format==='markdown'){text='# SXIGOai Chat Export\\n\\n';conversation.forEach(function(m){text+='**'+m.role+'**: '+m.content+'\\n\\n'})}else if(format==='json'){text=JSON.stringify({exported:new Date().toISOString(),model:activeModel,messages:conversation},null,2)}else{conversation.forEach(function(m){text+=m.role.toUpperCase()+': '+m.content+'\\n\\n'})}var blob=new Blob([text],{type:'text/plain'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='sxigo_export.'+(format==='json'?'json':'md');a.click();URL.revokeObjectURL(url);showToast('Exported as '+format)}
document.addEventListener('keydown',function(e){var c=e.ctrlKey||e.metaKey,sh=e.shiftKey;if(c&&sh&&e.key==='F'){e.preventDefault();toggleSearch()}if(c&&sh&&e.key==='C'){e.preventDefault();clearChat()}if(c&&e.key==='b'){e.preventDefault();var s=document.querySelector('.sidebar');if(s){s.style.display=s.style.display==='none'?'flex':''}}if(c&&sh&&e.key==='P'){e.preventDefault();togglePlayground()}if(c&&sh&&e.key==='/'){e.preventDefault();toggleShortcuts()}});
var recognition=null,isRecording=false;
function toggleVoice(){var SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR){showToast('Voice not supported');return}if(recognition&&isRecording){recognition.stop();isRecording=false;showToast('Voice stopped');return}recognition=new SR();recognition.lang='ko-KR';recognition.continuous=false;recognition.interimResults=true;isRecording=true;showToast('Listening...');recognition.onresult=function(e){var t='';for(var i=e.resultIndex;i<e.results.length;i++){t+=e.results[i][0].transcript}document.getElementById('input').value+=t;document.getElementById('input').dispatchEvent(new Event('input'))};recognition.onend=function(){isRecording=false;showToast('Voice captured')};recognition.onerror=function(e){isRecording=false;showToast('Voice error: '+e.error)};recognition.start()}
document.addEventListener('contextmenu',function(e){var bubble=e.target.closest('.bubble');if(bubble){e.preventDefault();var menu=document.getElementById('ctxMenu');if(!menu){menu=document.createElement('div');menu.id='ctxMenu';menu.className='context-menu';menu.innerHTML='<button onclick="copyMsg(this)">Copy</button><button onclick="exportChat(\\'text\\')">Export</button><div class="sep"></div><button onclick="this.parentElement.classList.remove(\\'show\\')">Close</button>';document.body.appendChild(menu)}menu.style.left=e.clientX+'px';menu.style.top=e.clientY+'px';menu.classList.add('show');window.copyMsgTarget=bubble;setTimeout(function(){document.addEventListener('click',function h(){menu.classList.remove('show');document.removeEventListener('click',h)},{once:true})},10)}});
function copyMsg(btn){var text=window.copyMsgTarget?window.copyMsgTarget.textContent:'';if(navigator.clipboard){navigator.clipboard.writeText(text).then(function(){showToast('Copied')})}}
async function pullModel(name){showToast('Pulling '+name+'...');try{var res=await fetch(serverUrl+'/api/pull',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:name,stream:true})});var reader=res.body.getReader(),dec=new TextDecoder();while(true){var rd=await reader.read();if(rd.done)break;var lines=dec.decode(rd.value,{stream:true}).split('\\n').filter(function(l){return l.trim()});for(var i=0;i<lines.length;i++){try{var j=JSON.parse(lines[i]);if(j.status)showToast(j.status)}catch(e){}}}checkServer();showToast('Pull complete!')}catch(e){showToast('Pull failed: '+e.message)}}
console.log('SXIGOai V2.0 Premium fully loaded');
'''

# Insert CSS before </style>
idx = content.index('</style>')
content = content[:idx] + css_extra + '\n' + content[idx:]

# Insert JS before </script> (last occurrence)
idx = content.rindex('</script>')
content = content[:idx] + js_extra + '\n' + content[idx:]

# Update layout: wrap main content in sidebar + main-area
# Find the <div class="app"> section and restructure
old_layout = '<div class="app">'
new_layout = '''<div class="app">
  <div class="sidebar" id="sidebar">
    <div class="sidebar-header">
      <h2>History</h2>
      <button onclick="newChat()">+</button>
    </div>
    <div class="sidebar-list" id="sidebarList"></div>
  </div>
  <div class="main-area">'''

content = content.replace(old_layout, new_layout, 1)

# Close main-area before closing app
# Find </div> that closes .app (last one before </body>)
body_idx = content.rindex('</body>')
# Find the last </div> before </body> that's not the settings panel or overlay or toast
# Actually the .app div is closed with </div> somewhere. Let me find the right one.
# The structure before our change: <div class="app"> ... </div> </body>
# After our change: <div class="app"><div class="sidebar">...<div class="main-area">...</div></div></body>
# We need to close .main-area before .app closes
# Find </div>\n</body> and insert </div> before it
# close_div is already present

# Also add status bar before input
input_wrap_idx = content.index('<div class="input-wrap">')
status_bar = '<div class="status-bar" id="statusBar"><span class="stat"><span class="stat-dot" style="background:#30d158"></span> Connected</span><span class="stat" id="msgCount">0 msgs</span></div>\n'
content = content[:input_wrap_idx] + status_bar + content[input_wrap_idx:]

# Add header actions: search + playground buttons
# Find hdr-actions and add buttons
hdr_idx = content.index('<div class="hdr-actions">')
hdr_insert = '<button class="hdr-btn" onclick="toggleSearch()" title="Search">🔍</button>\n<button class="hdr-btn" onclick="togglePlayground()" title="Playground">▶</button>\n      <button class="hdr-btn" onclick="toggleShortcuts()" title="Shortcuts">⌘</button>\n      <button class="hdr-btn" onclick="toggleFullscreen()" title="Fullscreen">⛶</button>\n      '
content = content[:hdr_idx + len('<div class="hdr-actions">')] + hdr_insert + content[hdr_idx + len('<div class="hdr-actions">'):]

# Render sidebar after load
script_close = content.rindex('</script>')
init_code = '\nrenderSidebar();\n'
content = content[:script_close] + init_code + content[script_close:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

line_count = content.count('\n')
print(f'Final file: {line_count} lines')
