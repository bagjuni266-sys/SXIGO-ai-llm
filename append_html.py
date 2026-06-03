# appends HTML body content to SXIGOai.html
path = r'C:\Users\gamju\AppData\Local\Temp\opencode\SXIGOai.html'

parts = []

# ===== MAIN CONTENT =====
parts.append(r'''</div> <!-- end sidebar -->''')

parts.append(r'''<div class="main-content" id="mainContent">''')

# Model info bar
parts.append(r'''<div class="model-info-bar">''')
parts.append(r'''<div class="model-info-bar-inner">''')
parts.append(r'''<div class="status-dot pulse-dot"></div>''')
parts.append(r'''<span>Model: </span><strong id="modelNameDisplay">llama3.2:3b</strong>''')
parts.append(r'''<span class="model-rate-badge" id="modelRateBadge">~30 tok/s</span>''')
parts.append(r'''<span class="info-sep">|</span>''')
parts.append(r'''<span id="tokenCountDisplay">0 tokens</span>''')
parts.append(r'''<span class="info-sep">|</span>''')
parts.append(r'''<span id="connectionQuality" class="connection-good">&#x1F7E2; Connected</span>''')
parts.append(r'''</div>''')
parts.append(r'''</div>''')

# Chat header
parts.append(r'''<div class="chat-header">''')
parts.append(r'''<div class="chat-header-left">''')
parts.append(r'''<button class="sidebar-collapse-btn mobile-only" onclick="toggleSidebar()">&#x2630;</button>''')
parts.append(r'''<span id="chatTitle">Welcome to SXIGOai V2.0</span>''')
parts.append(r'''</div>''')
parts.append(r'''<div class="chat-header-right">''')
parts.append(r'''<button class="header-btn" onclick="openPullModel()" title="Pull Model">&#x1F4E5;</button>''')
parts.append(r'''<button class="header-btn" onclick="openCompare()" title="Compare">&#x1F4CB;</button>''')
parts.append(r'''<button class="header-btn" onclick="searchMessages()" id="searchBtn" title="Search"><span>&#x1F50D;</span></button>''')
parts.append(r'''<button class="header-btn" onclick="openNotifications()" title="Notifications"><span>&#x1F514;</span><span class="badge-count" id="headerNotifBadge">0</span></button>''')
parts.append(r'''<button class="header-btn" onclick="openSettings()" title="Settings">&#x2699;&#xFE0F;</button>''')
parts.append(r'''</div>''')
parts.append(r'''</div>''')

# Messages container
parts.append(r'''<div class="messages-container" id="messagesContainer">''')

# Welcome screen
parts.append(r'''<div class="welcome-screen" id="welcomeScreen">''')
parts.append(r'''<div class="welcome-logo">SXIGOai</div>''')
parts.append(r'''<div class="welcome-title">Welcome to V2.0</div>''')
parts.append(r'''<div class="welcome-subtitle">Experience next-generation AI chat with glassmorphism design, RGB dynamic effects, and a premium interface that redefines what's possible.</div>''')
parts.append(r'''<div class="welcome-grid">''')
parts.append(r'''<div class="welcome-card" onclick="suggestPrompt('Explain quantum computing')"><div class="card-icon">&#x1F4A1;</div><div class="card-title">Explain Concepts</div><div class="card-desc">Quantum computing, neural networks, and more</div></div>''')
parts.append(r'''<div class="welcome-card" onclick="suggestPrompt('Write a Python script to sort files')"><div class="card-icon">&#x1F4DD;</div><div class="card-title">Write Code</div><div class="card-desc">Scripts, algorithms, and full programs</div></div>''')
parts.append(r'''<div class="welcome-card" onclick="suggestPrompt('Summarize the plot of Inception')"><div class="card-icon">&#x1F3AC;</div><div class="card-title">Summarize</div><div class="card-desc">Movies, books, articles, and more</div></div>''')
parts.append(r'''<div class="welcome-card" onclick="suggestPrompt('What are the best practices for REST APIs?')"><div class="card-icon">&#x1F527;</div><div class="card-title">Get Advice</div><div class="card-desc">Best practices and design patterns</div></div>''')
parts.append(r'''<div class="welcome-card" onclick="suggestPrompt('Write a poem about AI')"><div class="card-icon">&#x1F3B5;</div><div class="card-title">Creative Writing</div><div class="card-desc">Poems, stories, and creative content</div></div>''')
parts.append(r'''<div class="welcome-card" onclick="suggestPrompt('Help me debug my code')"><div class="card-icon">&#x1F41B;</div><div class="card-title">Debug</div><div class="card-desc">Find and fix bugs in your code</div></div>''')
parts.append(r'''</div>''')
parts.append(r'''<div class="prompt-chips">''')
parts.append(r'''<div class="chip-category"><span class="cat-label">Quick</span><span class="prompt-chip" onclick="suggestPrompt('Hello!')">Hello</span><span class="prompt-chip" onclick="suggestPrompt('What is AI?')">What is AI?</span><span class="prompt-chip" onclick="suggestPrompt('Tell me a joke')">Joke</span></div>''')
parts.append(r'''</div>''')
parts.append(r'''</div>''')

parts.append(r'''</div> <!-- end messages -->''')

# Input area with file drop zone
parts.append(r'''<div class="input-area">''')
parts.append(r'''<div class="attach-preview-bar" id="attachPreviewBar"></div>''')
parts.append(r'''<div class="input-wrapper" id="inputWrapper">''')
parts.append(r'''<div class="file-drop-zone" id="fileDropZone"><div><div class="drop-icon">&#x1F4C2;</div><div class="drop-text">Drop files here</div><div class="drop-hint">Images, code files, documents</div></div></div>''')
parts.append(r'''<textarea id="messageInput" rows="1" placeholder="Message SXIGOai..." oninput="autoResize(this)" onkeydown="handleKeyDown(event)" autofocus></textarea>''')
parts.append(r'''<div class="input-tools">''')
parts.append(r'''<button class="tool-btn" onclick="toggleVoice()" id="voiceBtn" title="Voice input">&#x1F3A4;</button>''')
parts.append(r'''<button class="tool-btn" onclick="document.getElementById('fileInput').click()" title="Attach file">&#x1F4CE;</button>''')
parts.append(r'''<input type="file" id="fileInput" multiple style="display:none" onchange="handleFiles(this.files)">''')
parts.append(r'''</div>''')
parts.append(r'''<button class="send-btn" id="sendBtn" onclick="sendMessage()">&#x25B6;</button>''')
parts.append(r'''<button class="stop-btn" id="stopBtn" onclick="stopStreaming()">&#x25A0;</button>''')
parts.append(r'''<div class="input-progress" id="inputProgress"></div>''')
parts.append(r'''<div class="voice-wave" id="voiceWave"><div class="wave-bar"></div><div class="wave-bar"></div><div class="wave-bar"></div><div class="wave-bar"></div><div class="wave-bar"></div></div>''')
parts.append(r'''</div>''')
parts.append(r'''</div>''')

parts.append(r'''</div> <!-- end main-content -->''')
parts.append(r'''</div> <!-- end app-container -->''')

# ===== SETTINGS PANEL =====
parts.append(r'''<div class="settings-overlay" id="settingsOverlay" onclick="closeSettings()"></div>''')
parts.append(r'''<div class="settings-panel" id="settingsPanel">''')
parts.append(r'''<div class="settings-header"><h2>&#x2699;&#xFE0F; Settings</h2><button class="close-settings" onclick="closeSettings()">&#x2716;</button></div>''')

# Settings tabs
parts.append(r'''<div class="settings-tab-bar">''')
parts.append(r'''<button class="settings-tab active" data-tab="general" onclick="switchSettingsTab('general',this)">General</button>''')
parts.append(r'''<button class="settings-tab" data-tab="theme" onclick="switchSettingsTab('theme',this)">Theme</button>''')
parts.append(r'''<button class="settings-tab" data-tab="model" onclick="switchSettingsTab('model',this)">Model</button>''')
parts.append(r'''<button class="settings-tab" data-tab="about" onclick="switchSettingsTab('about',this)">About</button>''')
parts.append(r'''</div>''')

# General tab
parts.append(r'''<div class="settings-section active" id="settingsGeneral">''')
parts.append(r'''<div class="setting-group"><label class="setting-label">Server URL</label><input class="setting-input" id="serverUrl" value="http://localhost:11434" onchange="saveSettings()"></div>''')
parts.append(r'''<div class="setting-group"><label class="setting-label">System Prompt</label><textarea class="setting-textarea" id="systemPrompt" onchange="saveSettings()">You are SXIGOai V2.0, an advanced AI assistant. Respond helpfully and concisely.</textarea></div>''')
parts.append(r'''<div class="setting-group"><label class="setting-label">Context Length</label><select class="setting-select" id="contextLength" onchange="saveSettings()"><option value="2048">2048</option><option value="4096" selected>4096</option><option value="8192">8192</option><option value="16384">16384</option><option value="32768">32768</option></select></div>''')
parts.append(r'''<div class="setting-group"><label class="setting-label">Temperature</label><div class="setting-range-wrap"><input type="range" class="setting-range" id="temperature" min="0" max="2" step="0.1" value="0.7" oninput="updateRangeValue(this,'tempVal');saveSettings()"><span class="setting-range-value" id="tempVal">0.7</span></div></div>''')
parts.append(r'''<div class="setting-group"><label class="setting-label">Max Tokens</label><div class="setting-range-wrap"><input type="range" class="setting-range" id="maxTokens" min="128" max="8192" step="128" value="2048" oninput="updateRangeValue(this,'maxTokVal');saveSettings()"><span class="setting-range-value" id="maxTokVal">2048</span></div></div>''')
parts.append(r'''<div class="setting-group"><label class="setting-label">Font Size</label><div class="font-size-controls"><button class="font-size-btn" onclick="adjustFontSize(-1)">A-</button><span class="font-size-label" id="fontSizeLabel">14px</span><button class="font-size-btn" onclick="adjustFontSize(1)">A+</button></div></div>''')
parts.append(r'''<div class="setting-group"><label class="setting-label">Keyboard Shortcuts</label><button class="modal-btn" onclick="openShortcuts()" style="width:100%;margin-top:4px;">&#x2328; View Shortcuts</button></div>''')
parts.append(r'''</div>''')

# Theme tab
parts.append(r'''<div class="settings-section" id="settingsTheme">''')
parts.append(r'''<div class="setting-group"><label class="setting-label">Theme</label><div class="theme-grid" id="themeGrid"></div></div>''')
parts.append(r'''<div class="setting-group"><label class="setting-label">Glass Depth</label><div class="setting-range-wrap"><input type="range" class="setting-range" id="glassDepth" min="0.02" max="0.25" step="0.01" value="0.06" oninput="updateRangeValue(this,'glassVal');saveSettings()"><span class="setting-range-value" id="glassVal">0.06</span></div></div>''')
parts.append(r'''<div class="setting-group"><label class="setting-label">Custom Theme Colors</label>''')
parts.append(r'''<div class="theme-custom-row"><label>Primary</label><input type="color" id="customPrimary" value="#667eea" onchange="applyCustomColors()"></div>''')
parts.append(r'''<div class="theme-custom-row"><label>Secondary</label><input type="color" id="customSecondary" value="#764ba2" onchange="applyCustomColors()"></div>''')
parts.append(r'''<div class="theme-custom-row"><label>Accent</label><input type="color" id="customAccent" value="#4facfe" onchange="applyCustomColors()"></div>''')
parts.append(r'''<div class="theme-custom-row"><label>Background</label><input type="color" id="customBg" value="#0a0a1a" onchange="applyCustomColors()"></div>''')
parts.append(r'''<div class="theme-custom-row"><button class="modal-btn primary" onclick="saveCustomTheme()" style="width:100%;margin-top:4px;">Save Custom Theme</button></div>''')
parts.append(r'''<p class="setting-help">Custom colors override the selected theme. Save to apply permanently.</p>''')
parts.append(r'''</div>''')

# Model tab
parts.append(r'''<div class="settings-section" id="settingsModel">''')
parts.append(r'''<div class="setting-group"><label class="setting-label">Available Models</label><div id="modelList"></div></div>''')
parts.append(r'''<div class="setting-group"><button class="modal-btn primary" onclick="refreshModels()" style="width:100%;">&#x1F504; Refresh Models</button></div>''')
parts.append(r'''<div class="setting-group"><button class="modal-btn" onclick="openPullModel()" style="width:100%;">&#x1F4E5; Pull New Model</button></div>''')
parts.append(r'''<div class="server-status-grid" id="serverStatus">''')
parts.append(r'''<div class="status-item"><div class="label">Server</div><div class="value" id="srvStatus">Checking...</div></div>''')
parts.append(r'''<div class="status-item"><div class="label">Latency</div><div class="value" id="srvLatency">-</div></div>''')
parts.append(r'''<div class="status-item"><div class="label">Models</div><div class="value" id="srvModels">0</div></div>''')
parts.append(r'''<div class="status-item"><div class="label">Connection</div><div class="value" id="srvConnection">&#x1F7E2; Online</div></div>''')
parts.append(r'''</div>''')
parts.append(r'''</div>''')

# About tab
parts.append(r'''<div class="settings-section" id="settingsAbout">''')
parts.append(r'''<div style="text-align:center;padding:20px 0;"><div style="font-size:40px;font-weight:900;background:linear-gradient(135deg,#f093fb,#f5576c,#4facfe);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">SXIGOai</div><div style="font-size:13px;margin:6px 0;color:var(--text-secondary);">Version 2.0</div><div style="font-size:12px;color:var(--text-muted);">Next-generation AI chat interface with glassmorphism, RGB effects, and premium UX</div></div>''')
parts.append(r'''<div class="setting-group"><label class="setting-label">Activity Log</label><div id="activityLog" style="max-height:200px;overflow-y:auto;"></div></div>''')
parts.append(r'''</div>''')

parts.append(r'''</div> <!-- end settings -->''')

# ===== NOTIFICATION PANEL =====
parts.append(r'''<div class="notification-panel" id="notificationPanel">''')
parts.append(r'''<div class="notif-header"><h3>&#x1F514; Notifications</h3><button class="notif-clear-btn" onclick="clearNotifications()">Clear All</button></div>''')
parts.append(r'''<div class="notif-list" id="notifList"><div class="notif-empty">&#x1F4AC; No notifications yet</div></div>''')
parts.append(r'''</div>''')

# ===== COMPARE VIEW =====
parts.append(r'''<div class="compare-view" id="compareView">''')
parts.append(r'''<div class="compare-header"><h3>&#x1F4CB; Compare Models</h3><div class="model-compare-selects"><select id="compareModelA"></select><select id="compareModelB"></select></div><button class="compare-close-btn" onclick="closeCompare()">&#x2716;</button></div>''')
parts.append(r'''<div class="compare-body"><div class="compare-pane"><div class="compare-pane-header">Model A</div><div class="compare-pane-content" id="comparePaneA">Select a model and send a prompt to compare responses.</div></div><div class="compare-pane"><div class="compare-pane-header">Model B</div><div class="compare-pane-content" id="comparePaneB">Select a model and send a prompt to compare responses.</div></div></div>''')
parts.append(r'''</div>''')

# ===== MODALS =====
# Pull model modal
parts.append(r'''<div class="modal-overlay" id="pullModelOverlay" onclick="if(event.target===this)closePullModel()">''')
parts.append(r'''<div class="modal" onclick="event.stopPropagation()"><div class="modal-header"><h3>&#x1F4E5; Pull Model</h3><button class="modal-close-btn" onclick="closePullModel()">&#x2716;</button></div>''')
parts.append(r'''<div class="modal-body">''')
parts.append(r'''<div class="pull-model-step"><label>Model Name</label><input id="pullModelName" placeholder="e.g., llama3.2:3b, mistral:7b" onkeydown="if(event.key==='Enter')startPull()"></div>''')
parts.append(r'''<div class="pull-model-step"><label>Presets</label><div class="pull-model-presets"><button class="pull-preset-btn" onclick="setPullPreset('llama3.2:3b')">llama3.2:3b</button><button class="pull-preset-btn" onclick="setPullPreset('llama3.2:1b')">llama3.2:1b</button><button class="pull-preset-btn" onclick="setPullPreset('mistral:7b')">mistral:7b</button><button class="pull-preset-btn" onclick="setPullPreset('gemma2:2b')">gemma2:2b</button><button class="pull-preset-btn" onclick="setPullPreset('phi3:3.8b')">phi3:3.8b</button></div></div>''')
parts.append(r'''<button class="modal-btn primary" onclick="startPull()" id="pullStartBtn" style="width:100%;">Pull Model</button>''')
parts.append(r'''<div class="pull-progress" id="pullProgress"><div class="pull-progress-bar"><div class="pull-progress-fill" id="pullProgressFill"></div></div><div class="pull-progress-text" id="pullProgressText">Starting...</div></div>''')
parts.append(r'''</div></div></div>''')

# Shortcuts modal
parts.append(r'''<div class="modal-overlay" id="shortcutsOverlay" onclick="if(event.target===this)closeShortcuts()">''')
parts.append(r'''<div class="modal" onclick="event.stopPropagation()"><div class="modal-header"><h3>&#x2328; Keyboard Shortcuts</h3><button class="modal-close-btn" onclick="closeShortcuts()">&#x2716;</button></div>''')
parts.append(r'''<div class="modal-body"><div class="shortcut-grid">''')
parts.append(r'''<div class="shortcut-item"><span class="desc">New Chat</span><span class="key">Ctrl+N</span></div>''')
parts.append(r'''<div class="shortcut-item"><span class="desc">Send Message</span><span class="key">Enter</span></div>''')
parts.append(r'''<div class="shortcut-item"><span class="desc">New Line</span><span class="key">Shift+Enter</span></div>''')
parts.append(r'''<div class="shortcut-item"><span class="desc">Toggle Sidebar</span><span class="key">Ctrl+B</span></div>''')
parts.append(r'''<div class="shortcut-item"><span class="desc">Search Messages</span><span class="key">Ctrl+F</span></div>''')
parts.append(r'''<div class="shortcut-item"><span class="desc">Open Settings</span><span class="key">Ctrl+,</span></div>''')
parts.append(r'''<div class="shortcut-item"><span class="desc">Pull Model</span><span class="key">Ctrl+P</span></div>''')
parts.append(r'''<div class="shortcut-item"><span class="desc">Toggle Voice</span><span class="key">Ctrl+M</span></div>''')
parts.append(r'''<div class="shortcut-item"><span class="desc">Focus Input</span><span class="key">Escape then /</span></div>''')
parts.append(r'''<div class="shortcut-item"><span class="desc">Stop Streaming</span><span class="key">Escape</span></div>''')
parts.append(r'''</div></div></div></div>''')

# About modal (mini)
parts.append(r'''<div class="modal-overlay" id="aboutOverlay" onclick="if(event.target===this)closeAbout()">''')
parts.append(r'''<div class="modal" onclick="event.stopPropagation()"><div class="modal-header"><h3>&#x2139;&#xFE0F; About</h3><button class="modal-close-btn" onclick="closeAbout()">&#x2716;</button></div>''')
parts.append(r'''<div class="modal-body" style="text-align:center;padding:20px;"><div style="font-size:48px;font-weight:900;background:linear-gradient(135deg,#f093fb,#f5576c,#4facfe);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">SXIGOai</div><div style="font-size:14px;margin:8px 0;color:var(--text-secondary);">Version 2.0</div><div style="font-size:12px;color:var(--text-muted);">Built with glassmorphism, RGB effects, and premium UX design principles. Surpassing traditional interfaces with next-generation AI chat experience.</div></div></div></div>''')

# Dashboard modal
parts.append(r'''<div class="modal-overlay" id="dashboardOverlay" onclick="if(event.target===this)closeDashboard()">''')
parts.append(r'''<div class="modal wide" onclick="event.stopPropagation()"><div class="modal-header"><h3>&#x1F4CA; Dashboard</h3><button class="modal-close-btn" onclick="closeDashboard()">&#x2716;</button></div>''')
parts.append(r'''<div class="modal-body"><div class="dashboard-grid" id="dashGrid">''')
parts.append(r'''<div class="dashboard-card"><div class="dash-value" id="dashMessages">0</div><div class="dash-label">Total Messages</div></div>''')
parts.append(r'''<div class="dashboard-card"><div class="dash-value" id="dashConversations">0</div><div class="dash-label">Conversations</div></div>''')
parts.append(r'''<div class="dashboard-card"><div class="dash-value" id="dashTokens">0</div><div class="dash-label">Total Tokens</div></div>''')
parts.append(r'''<div class="dashboard-card"><div class="dash-value" id="dashModels">0</div><div class="dash-label">Models Available</div></div>''')
parts.append(r'''<div class="dashboard-card"><div class="dash-value" id="dashSessions">0</div><div class="dash-label">Session Duration</div></div>''')
parts.append(r'''<div class="dashboard-card"><div class="dash-value" id="dashAvgResponse">0s</div><div class="dash-label">Avg Response Time</div></div>''')
parts.append(r'''</div><h4 style="font-size:13px;color:var(--text-secondary);margin:8px 0;">Recent Activity</h4>''')
parts.append(r'''<div id="activityList"></div></div></div></div>''')

# ===== TOAST CONTAINER =====
parts.append(r'''<div class="toast-container" id="toastContainer"></div>''')

# ===== STATUS BAR =====
parts.append(r'''<div class="status-bar">''')
parts.append(r'''<div class="status-item"><span class="status-dot online" id="statusBarDot"></span><span id="statusBarServer">Connected</span></div>''')
parts.append(r'''<div class="status-item">&#x1F4E5; <span id="statusBarModel">llama3.2:3b</span></div>''')
parts.append(r'''<div class="status-item">&#x1F4CA; <span id="statusBarTokens">0 tokens</span></div>''')
parts.append(r'''<div class="status-item">&#x23F1; <span id="statusBarLatency">-</span></div>''')
parts.append(r'''<div class="status-item" style="margin-left:auto;">SXIGOai V2.0</div>''')
parts.append(r'''</div>''')

# ===== WATERMARK =====
parts.append(r'''<div class="watermark">Powered by <strong>SXIGOai</strong> V2.0</div>''')

# ===== FILE INPUT (hidden) =====
parts.append(r'''<input type="file" id="hiddenFileInput" style="display:none" multiple onchange="handleFiles(this.files)">''')

with open(path, 'a', encoding='utf-8') as f:
    for part in parts:
        f.write(part + '\n')

print(f'Appended {len(parts)} lines of HTML')
