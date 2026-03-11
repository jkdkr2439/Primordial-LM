
const chatStream = document.getElementById('chat-stream');
const userInput = document.getElementById('user-input');
const btnSend = document.getElementById('btn-send');
const btnInit = document.getElementById('btn-init');
const weightsDir = document.getElementById('weights-dir');
const setupPanel = document.getElementById('setup-panel');
const statTime = document.getElementById('stat-time');
const statOrgans = document.getElementById('stat-organs');

// Marked.js Configuration
marked.setOptions({
    highlight: function(code, lang) {
        if (Prism.languages[lang]) {
            return Prism.highlight(code, Prism.languages[lang], lang);
        }
        return code;
    },
    breaks: true
});

function appendMessage(role, content) {
    const row = document.createElement('div');
    row.className = `message-row ${role}`;
    
    const container = document.createElement('div');
    container.className = 'message-content';
    
    const avatar = document.createElement('div');
    avatar.className = `avatar ${role}`;
    avatar.textContent = role === 'user' ? 'U' : 'P';
    
    const textDiv = document.createElement('div');
    textDiv.className = 'text-content';
    
    // Render Markdown
    textDiv.innerHTML = marked.parse(content);
    
    container.appendChild(avatar);
    container.appendChild(textDiv);
    row.appendChild(container);
    chatStream.appendChild(row);
    
    // Highlight Code
    row.querySelectorAll('pre code').forEach((block) => {
        Prism.highlightElement(block);
    });
    
    chatStream.scrollTop = chatStream.scrollHeight;
}

async function typeWriter(role, content) {
    const row = document.createElement('div');
    row.className = `message-row ${role}`;
    const container = document.createElement('div');
    container.className = 'message-content';
    const avatar = document.createElement('div');
    avatar.className = `avatar ${role}`;
    avatar.textContent = 'P';
    const textDiv = document.createElement('div');
    textDiv.className = 'text-content';
    
    container.appendChild(avatar);
    container.appendChild(textDiv);
    row.appendChild(container);
    chatStream.appendChild(row);

    let currentText = "";
    const speed = 20; // ms per char
    
    for (let i = 0; i < content.length; i++) {
        currentText += content[i];
        textDiv.innerHTML = marked.parse(currentText);
        chatStream.scrollTop = chatStream.scrollHeight;
        await new Promise(r => setTimeout(r, speed));
    }
    
    // Final Highlight
    row.querySelectorAll('pre code').forEach((block) => {
        Prism.highlightElement(block);
    });
}

async function initialize() {
    const path = weightsDir.value || "D:\\models\\Qwen2.5-7B-Instruct";
    const load4bit = document.getElementById('load-4bit').checked;
    btnInit.textContent = "Infiltrating...";
    btnInit.disabled = true;
    
    try {
        const response = await fetch('/api/init', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ weights_dir: path, load_in_4bit: load4bit })
        });
        
        const data = await response.json();
        if (response.ok) {
            setupPanel.style.display = 'none';
            userInput.disabled = false;
            btnSend.disabled = false;
            document.getElementById('active-model').textContent = data.model;
        } else {
            alert(`Infiltration failed: ${data.detail}`);
            btnInit.textContent = "Infiltrate";
            btnInit.disabled = false;
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
        btnInit.disabled = false;
    }
}

async function sendMessage() {
    const msg = userInput.value.trim();
    if (!msg) return;
    
    appendMessage('user', msg);
    userInput.value = '';
    userInput.style.height = 'auto';
    btnSend.disabled = true;
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
        });
        
        const data = await response.json();
        if (response.ok) {
            await typeWriter('bot', data.response);
            statTime.textContent = data.stats.state_changes;
            statOrgans.textContent = data.stats.organs;
        } else {
            appendMessage('bot', `System Error: ${data.detail}`);
        }
    } catch (error) {
        appendMessage('bot', `Connection Lost: ${error.message}`);
    } finally {
        btnSend.disabled = false;
    }
}

// UI Event Handling
userInput.addEventListener('input', () => {
    userInput.style.height = 'auto';
    userInput.style.height = (userInput.scrollHeight) + 'px';
});

userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

btnInit.onclick = initialize;
btnSend.onclick = sendMessage;

const telemetryContent = document.getElementById('telemetry-content');
const telemetryStatus = document.getElementById('telemetry-status');

function setupTelemetry() {
    const eventSource = new EventSource('/api/telemetry');
    
    eventSource.onopen = () => {
        telemetryStatus.textContent = "CONNECTED";
        telemetryStatus.style.color = "#0f0";
    };
    
    eventSource.onmessage = (event) => {
        const div = document.createElement('div');
        div.className = 'telemetry-log';
        if (event.data.includes('[primordial]') || event.data.includes('[cycle]')) {
            div.classList.add('accent');
        }
        div.textContent = `> ${event.data}`;
        telemetryContent.appendChild(div);
        
        // Auto-scroll to bottom
        const panel = document.getElementById('telemetry-panel');
        panel.scrollTop = panel.scrollHeight;
        
        // Keep logs from growing too large
        if (telemetryContent.children.length > 100) {
            telemetryContent.removeChild(telemetryContent.firstChild);
        }
    };
    
    eventSource.onerror = () => {
        telemetryStatus.textContent = "DROPPED - RECONNECTING";
        telemetryStatus.style.color = "red";
    };
}


// --- OUROBOROS PANEL ---
const ouroPanel = document.getElementById('ouroboros-panel');
const ouroStatus = document.getElementById('ouro-status');
const ouroCycles = document.getElementById('ouro-cycles');
const ouroLearnings = document.getElementById('ouro-learnings');
const btnOuroToggle = document.getElementById('btn-ouro-toggle');
let ouroRunning = false;

async function pollOuroboros() {
    try {
        const res = await fetch('/api/ouroboros');
        if (!res.ok) return;
        const data = await res.json();
        ouroPanel.style.display = 'block';
        ouroRunning = data.running;
        ouroStatus.textContent = data.running ? 'Active' : 'Paused';
        ouroStatus.style.color = data.running ? '#0f0' : '#f80';
        ouroCycles.textContent = data.cycle_count;
        ouroLearnings.textContent = data.total_learnings;
        btnOuroToggle.textContent = data.running ? '⏸ Pause Loop' : '▶ Resume Loop';
    } catch(e) {}
}

btnOuroToggle.addEventListener('click', async () => {
    const endpoint = ouroRunning ? '/api/ouroboros/stop' : '/api/ouroboros/start';
    try {
        await fetch(endpoint, { method: 'POST' });
        await pollOuroboros();
    } catch(e) {}
});

window.onload = async () => {
    setupTelemetry();
    try {
        const res = await fetch('/api/session');
        const data = await res.json();
        
        // Handle Unified Core (The Merger)
        if (data.has_internal) {
            document.getElementById('core-status').style.display = 'block';
            weightsDir.value = "INTERNAL_CORE_SUBSTRATE";
            weightsDir.disabled = true;
            document.getElementById('load-4bit').checked = true; // Optimization recommended for merged core
        } else if (data.last_config) {
            if (data.last_config.last_weights_dir) {
                weightsDir.value = data.last_config.last_weights_dir;
            }
            if (data.last_config.last_load_in_4bit !== undefined) {
                document.getElementById('load-4bit').checked = data.last_config.last_load_in_4bit;
            }
        }

        if (data.status === "ready") {
            setupPanel.style.display = 'none';
            userInput.disabled = false;
            btnSend.disabled = false;
            statTime.textContent = data.state_changes;
            data.history.forEach(m => appendMessage(m.role, m.content));
            // Start polling Ouroboros
            pollOuroboros();
            setInterval(pollOuroboros, 5000);
        }
    } catch (e) {
        console.error("Session load failed:", e);
    }
};
