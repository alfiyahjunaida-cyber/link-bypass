#!/usr/bin/env python3
# api/index.py — Bypass Link + Web2APK Tool (Vercel-ready)
from flask import Flask, request, jsonify, render_template_string
import requests
from urllib.parse import quote

app = Flask(__name__)

TIMEOUT = 30


HTML = r'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>⚡ Dev Tools</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
  :root {
    --bg: #050309;
    --glass: rgba(22, 16, 34, 0.7);
    --border: rgba(168, 85, 247, 0.15);
    --border-2: rgba(168, 85, 247, 0.3);
    --text: #ece7f5;
    --text-dim: #9a90ad;
    --text-dim-2: #6b6178;
    --accent: #a855f7;
    --accent-2: #ec4899;
    --green: #10b981;
    --yellow: #f59e0b;
    --red: #ef4444;
    --blue: #3b82f6;
    --cyan: #06b6d4;
  }
  html, body {
    min-height: 100vh;
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', system-ui, sans-serif;
    overflow-x: hidden;
  }
  body::before {
    content: '';
    position: fixed; inset: 0;
    background:
      radial-gradient(ellipse 80% 50% at 20% 0%, rgba(168,85,247,0.25), transparent 50%),
      radial-gradient(ellipse 60% 40% at 80% 10%, rgba(236,72,153,0.18), transparent 50%),
      radial-gradient(ellipse 70% 60% at 50% 100%, rgba(139,92,246,0.15), transparent 60%);
    z-index: -1;
  }
  body::after {
    content: '';
    position: fixed; inset: 0;
    background-image:
      linear-gradient(rgba(168,85,247,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(168,85,247,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    z-index: -1;
    mask-image: radial-gradient(ellipse 70% 70% at 50% 0%, black, transparent 70%);
    -webkit-mask-image: radial-gradient(ellipse 70% 70% at 50% 0%, black, transparent 70%);
  }
  .container { max-width: 820px; margin: 0 auto; padding: 30px 20px 60px; }

  .header { text-align: center; padding: 20px 0 30px; }
  .logo-badge {
    display: inline-flex; align-items: center; gap: 10px;
    padding: 8px 18px;
    background: var(--glass);
    border: 1px solid var(--border-2);
    border-radius: 999px;
    font-size: 11px; font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 0 30px rgba(168,85,247,0.2);
  }
  .logo-badge .pulse {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 12px var(--accent);
    animation: pulse 2s ease-in-out infinite;
  }
  @keyframes pulse {
    0%,100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.85); }
  }
  .title {
    font-size: clamp(30px, 5vw, 42px);
    font-weight: 900;
    letter-spacing: -1.5px;
    line-height: 1;
    background: linear-gradient(135deg, #fff 0%, var(--accent) 50%, var(--accent-2) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 30px rgba(168,85,247,0.4));
    margin-bottom: 12px;
  }
  .subtitle { color: var(--text-dim); font-size: 14px; font-weight: 500; }

  /* TABS */
  .tabs {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
    padding: 6px;
    background: rgba(0,0,0,0.35);
    border-radius: 16px;
    margin-bottom: 16px;
    border: 1px solid var(--border);
  }
  .tab {
    padding: 14px 16px;
    text-align: center;
    font-size: 13px;
    font-weight: 800;
    border-radius: 11px;
    cursor: pointer;
    color: var(--text-dim);
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    user-select: none;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }
  .tab:hover { color: var(--text); }
  .tab.active {
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
    color: white;
    box-shadow: 0 8px 25px rgba(168,85,247,0.4);
  }

  .panel { display: none; }
  .panel.active { display: block; animation: fadeIn 0.3s ease; }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; } }

  .card {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 26px;
    backdrop-filter: blur(20px) saturate(1.2);
    -webkit-backdrop-filter: blur(20px) saturate(1.2);
    box-shadow: 0 20px 60px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
    position: relative;
    overflow: hidden;
    margin-bottom: 16px;
  }
  .card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent), var(--accent-2), transparent);
    opacity: 0.6;
  }
  .card-title {
    display: flex; align-items: center; gap: 12px;
    font-size: 15px; font-weight: 800;
    margin-bottom: 20px; letter-spacing: 0.3px;
  }
  .card-title .icon {
    width: 36px; height: 36px;
    border-radius: 11px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 17px;
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
    box-shadow: 0 6px 20px rgba(168,85,247,0.4);
    flex-shrink: 0;
  }
  label {
    display: block;
    font-size: 11px;
    font-weight: 700;
    color: var(--text-dim);
    margin-bottom: 8px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  input, select {
    width: 100%;
    padding: 15px 16px;
    background: rgba(0,0,0,0.35);
    border: 1.5px solid var(--border);
    border-radius: 12px;
    color: var(--text);
    font-size: 14px;
    font-family: 'JetBrains Mono', monospace;
    outline: none;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 14px;
  }
  input:focus, select:focus {
    border-color: var(--accent);
    background: rgba(168,85,247,0.06);
    box-shadow: 0 0 0 4px rgba(168,85,247,0.12), 0 0 30px rgba(168,85,247,0.15);
  }
  input::placeholder { color: var(--text-dim-2); font-family: 'Inter', sans-serif; }
  select option { background: #1a0f2a; color: var(--text); }

  button {
    width: 100%;
    padding: 16px 20px;
    border: none;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 800;
    cursor: pointer;
    font-family: inherit;
    letter-spacing: 0.5px;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
    color: white;
    box-shadow: 0 8px 30px rgba(168,85,247,0.4);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }
  button:hover { transform: translateY(-2px); box-shadow: 0 12px 40px rgba(168,85,247,0.55); }
  button:active { transform: translateY(0); }
  button:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  @media (max-width: 520px) { .grid-2 { grid-template-columns: 1fr; } }

  .result {
    margin-top: 16px;
    background: #030207;
    border: 1.5px solid var(--border);
    border-radius: 14px;
    padding: 16px;
    min-height: 100px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12.5px;
    line-height: 1.7;
    color: #d1fae5;
    white-space: pre-wrap;
    word-break: break-all;
    display: none;
  }
  .result.show { display: block; }
  .result .row { padding: 4px 0; display: flex; gap: 10px; align-items: flex-start; }
  .result .key { color: var(--accent); font-weight: 700; min-width: 90px; flex-shrink: 0; }
  .result .val { color: #d1fae5; word-break: break-all; }
  .result .val.ok { color: #6ee7b7; font-weight: 700; }
  .result .val.err { color: #fca5a5; }
  .result a { color: var(--cyan); text-decoration: none; word-break: break-all; }
  .result a:hover { text-decoration: underline; }

  .copy-btn {
    margin-top: 12px;
    padding: 12px 16px;
    font-size: 13px;
    width: 100%;
    background: linear-gradient(135deg, var(--green), var(--cyan));
    box-shadow: 0 6px 20px rgba(16,185,129,0.4);
  }
  .dl-btn {
    margin-top: 12px;
    padding: 14px 16px;
    font-size: 14px;
    width: 100%;
    background: linear-gradient(135deg, var(--green), var(--cyan));
    box-shadow: 0 6px 20px rgba(16,185,129,0.4);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    color: white;
  }

  .loader {
    display: none;
    justify-content: center;
    align-items: center;
    gap: 10px;
    padding: 20px;
    color: var(--text-dim);
    font-size: 13px;
  }
  .loader.show { display: flex; }
  .spinner {
    width: 18px; height: 18px;
    border: 2px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  .providers {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-bottom: 14px;
  }
  .provider-tag {
    font-size: 10px;
    padding: 4px 10px;
    background: rgba(168,85,247,0.1);
    border: 1px solid var(--border-2);
    border-radius: 6px;
    color: var(--accent);
    font-weight: 700;
    letter-spacing: 0.5px;
  }

  .footer {
    text-align: center;
    color: var(--text-dim-2);
    font-size: 12px;
    padding: 40px 0 10px;
    letter-spacing: 0.3px;
  }
  .footer b {
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
  }

  @media (max-width: 480px) {
    .container { padding: 20px 14px 40px; }
    .card { padding: 20px 18px; border-radius: 20px; }
    .title { letter-spacing: -1px; }
    .result .key { min-width: 70px; font-size: 11px; }
    .result .val { font-size: 11.5px; }
    .tab { font-size: 12px; padding: 12px 10px; }
  }
</style>
</head>
<body>
<div class="container">

  <div class="header">
    <div class="logo-badge">
      <span class="pulse"></span>
      <span>Dev Tools · v1.1</span>
    </div>
    <h1 class="title">⚡ Dev Tools</h1>
    <p class="subtitle">bypass link & convert web jadi APK</p>
  </div>

  <div class="tabs">
    <div class="tab active" data-tab="bypass">
      <span>🔓</span>
      <span>Bypass Link</span>
    </div>
    <div class="tab" data-tab="web2apk">
      <span>📱</span>
      <span>Web to APK</span>
    </div>
  </div>

  <!-- ═══════════ PANEL: BYPASS ═══════════ -->
  <div class="panel active" id="panel-bypass">
    <div class="card">
      <div class="card-title">
        <span class="icon">🔗</span>
        <span>MASUKIN LINK</span>
      </div>

      <div class="providers">
        <span class="provider-tag">LINKVERTISE</span>
        <span class="provider-tag">MOVE2LINK</span>
        <span class="provider-tag">AUTO-DETECT</span>
      </div>

      <label>Link yang mau di-bypass</label>
      <input type="text" id="bypassUrl" placeholder="https://linkvertise.com/..." autocomplete="off" />

      <label>Provider</label>
      <select id="bypassProvider">
        <option value="auto">🎯 Auto-detect</option>
        <option value="linkvertise">Linkvertise</option>
        <option value="move2link">Move2Link</option>
        <option value="safebypass">SafeBypass (generic)</option>
      </select>

      <button id="bypassBtn" onclick="doBypass()">
        <span>⚡</span>
        <span>BYPASS SEKARANG</span>
      </button>

      <div class="loader" id="bypassLoader">
        <div class="spinner"></div>
        <span>memproses...</span>
      </div>

      <div class="result" id="bypassResult"></div>
    </div>
  </div>

  <!-- ═══════════ PANEL: WEB2APK ═══════════ -->
  <div class="panel" id="panel-web2apk">
    <div class="card">
      <div class="card-title">
        <span class="icon">📱</span>
        <span>CONVERT WEB JADI APK</span>
      </div>

      <div class="providers">
        <span class="provider-tag">WEBVIEW</span>
        <span class="provider-tag">ANDROID</span>
        <span class="provider-tag">AUTO-BUILD</span>
      </div>

      <label>URL Website</label>
      <input type="text" id="apkUrl" placeholder="https://example.com" autocomplete="off" />

      <label>Nama Aplikasi</label>
      <input type="text" id="apkName" placeholder="My App" autocomplete="off" />

      <div class="grid-2">
        <div>
          <label>Package Name</label>
          <input type="text" id="apkPackage" placeholder="com.example.app" autocomplete="off" />
        </div>
        <div>
          <label>Versi</label>
          <input type="text" id="apkVersionName" placeholder="1.0.0" value="1.0.0" autocomplete="off" />
        </div>
      </div>

      <label>Version Code</label>
      <input type="number" id="apkVersionCode" placeholder="1" value="1" min="1" />

      <button id="apkBtn" onclick="doWeb2Apk()">
        <span>📦</span>
        <span>BUILD APK SEKARANG</span>
      </button>

      <div class="loader" id="apkLoader">
        <div class="spinner"></div>
        <span>building APK... (bisa 10-30 detik)</span>
      </div>

      <div class="result" id="apkResult"></div>
    </div>
  </div>

  <div class="footer">
    built with <b>passion</b> · © 2026
  </div>
</div>

<script>
/* =============== TABS =============== */
document.querySelectorAll(".tab").forEach(tab => {
  tab.onclick = () => {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById("panel-" + tab.dataset.tab).classList.add("active");
  };
});

/* =============== UTIL =============== */
function showResult(id, html) {
  const el = document.getElementById(id);
  el.innerHTML = html;
  el.classList.add("show");
}

function esc(s) {
  return String(s).replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
}

function copyLink(url) {
  navigator.clipboard.writeText(url).then(() => {
    alert("✓ link di-copy!");
  }).catch(() => {
    prompt("copy manual:", url);
  });
}

/* =============== BYPASS =============== */
async function doBypass() {
  const url = document.getElementById("bypassUrl").value.trim();
  const provider = document.getElementById("bypassProvider").value;

  if (!url) {
    showResult("bypassResult", '<div class="row"><span class="val err">✗ isi link dulu</span></div>');
    return;
  }
  if (!/^https?:\/\//i.test(url)) {
    showResult("bypassResult", '<div class="row"><span class="val err">✗ link harus dimulai http:// atau https://</span></div>');
    return;
  }

  const btn = document.getElementById("bypassBtn");
  const loader = document.getElementById("bypassLoader");
  const orig = btn.innerHTML;

  btn.disabled = true;
  btn.innerHTML = '<span>⏳</span><span>MEMPROSES...</span>';
  loader.classList.add("show");
  document.getElementById("bypassResult").classList.remove("show");

  try {
    const r = await fetch("/api/bypass", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, provider })
    });
    const d = await r.json();

    if (d.error) {
      showResult("bypassResult",
        '<div class="row"><span class="key">STATUS</span><span class="val err">✗ GAGAL</span></div>' +
        '<div class="row"><span class="key">ERROR</span><span class="val err">' + esc(d.error) + '</span></div>'
      );
    } else {
      const bypassed = d.bypassedUrl || d.result || '-';
      showResult("bypassResult",
        '<div class="row"><span class="key">STATUS</span><span class="val ok">✓ BERHASIL</span></div>' +
        '<div class="row"><span class="key">PROVIDER</span><span class="val">' + esc(d.provider || '-') + '</span></div>' +
        '<div class="row"><span class="key">ORIGINAL</span><span class="val">' + esc(d.originalUrl || url) + '</span></div>' +
        '<div class="row"><span class="key">BYPASSED</span><span class="val"><a href="' + esc(bypassed) + '" target="_blank">' + esc(bypassed) + '</a></span></div>' +
        (d.responseTime ? '<div class="row"><span class="key">SPEED</span><span class="val">' + esc(d.responseTime) + '</span></div>' : '') +
        '<button class="copy-btn" onclick="copyLink(\'' + esc(bypassed).replace(/'/g, "\\'") + '\')">📋 COPY LINK</button>'
      );
    }
  } catch (e) {
    showResult("bypassResult", '<div class="row"><span class="key">ERROR</span><span class="val err">' + esc(e.message) + '</span></div>');
  }

  btn.disabled = false;
  btn.innerHTML = orig;
  loader.classList.remove("show");
}

/* =============== WEB2APK =============== */
async function doWeb2Apk() {
  const url = document.getElementById("apkUrl").value.trim();
  const appName = document.getElementById("apkName").value.trim();
  const packageName = document.getElementById("apkPackage").value.trim();
  const versionName = document.getElementById("apkVersionName").value.trim() || "1.0.0";
  const versionCode = parseInt(document.getElementById("apkVersionCode").value) || 1;

  if (!url) {
    showResult("apkResult", '<div class="row"><span class="val err">✗ isi URL dulu</span></div>');
    return;
  }
  if (!/^https?:\/\//i.test(url)) {
    showResult("apkResult", '<div class="row"><span class="val err">✗ URL harus dimulai http:// atau https://</span></div>');
    return;
  }
  if (!appName) {
    showResult("apkResult", '<div class="row"><span class="val err">✗ isi nama aplikasi</span></div>');
    return;
  }
  if (!packageName || !/^[a-z][a-z0-9_.]*$/.test(packageName)) {
    showResult("apkResult", '<div class="row"><span class="val err">✗ package name salah (contoh: com.example.app)</span></div>');
    return;
  }

  const btn = document.getElementById("apkBtn");
  const loader = document.getElementById("apkLoader");
  const orig = btn.innerHTML;

  btn.disabled = true;
  btn.innerHTML = '<span>⏳</span><span>BUILDING...</span>';
  loader.classList.add("show");
  document.getElementById("apkResult").classList.remove("show");

  try {
    const r = await fetch("/api/web2apk", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, appName, packageName, versionName, versionCode })
    });
    const d = await r.json();

    if (d.error) {
      showResult("apkResult",
        '<div class="row"><span class="key">STATUS</span><span class="val err">✗ GAGAL</span></div>' +
        '<div class="row"><span class="key">ERROR</span><span class="val err">' + esc(d.error) + '</span></div>' +
        (d.raw ? '<div class="row"><span class="key">RAW</span><span class="val">' + esc(JSON.stringify(d.raw).slice(0, 300)) + '</span></div>' : '')
      );
    } else {
      const dlUrl = d.downloadUrl || d.apkUrl || d.url || d.result || '-';
      showResult("apkResult",
        '<div class="row"><span class="key">STATUS</span><span class="val ok">✓ BERHASIL</span></div>' +
        '<div class="row"><span class="key">APP NAME</span><span class="val">' + esc(appName) + '</span></div>' +
        '<div class="row"><span class="key">PACKAGE</span><span class="val">' + esc(packageName) + '</span></div>' +
        '<div class="row"><span class="key">VERSION</span><span class="val">' + esc(versionName) + ' (' + versionCode + ')</span></div>' +
        '<div class="row"><span class="key">URL</span><span class="val">' + esc(url) + '</span></div>' +
        (dlUrl !== '-' ? '<div class="row"><span class="key">APK URL</span><span class="val"><a href="' + esc(dlUrl) + '" target="_blank">' + esc(dlUrl) + '</a></span></div>' : '') +
        (dlUrl !== '-' ? '<a class="dl-btn" href="' + esc(dlUrl) + '" target="_blank" download>📥 DOWNLOAD APK</a>' : '') +
        (d.responseTime ? '<div class="row"><span class="key">SPEED</span><span class="val">' + esc(d.responseTime) + '</span></div>' : '')
      );
    }
  } catch (e) {
    showResult("apkResult", '<div class="row"><span class="key">ERROR</span><span class="val err">' + esc(e.message) + '</span></div>');
  }

  btn.disabled = false;
  btn.innerHTML = orig;
  loader.classList.remove("show");
}

/* enter shortcut */
document.getElementById("bypassUrl").addEventListener("keydown", e => {
  if (e.key === "Enter") doBypass();
});
document.getElementById("apkPackage").addEventListener("keydown", e => {
  if (e.key === "Enter") doWeb2Apk();
});
</script>
</body>
</html>
'''


# =========================================================
# ROUTES
# =========================================================
@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML)


@app.route("/api/bypass", methods=["POST", "GET"])
def api_bypass():
    if request.method == "POST":
        data = request.json or {}
    else:
        data = request.args.to_dict()

    url = (data.get("url") or "").strip()
    provider = (data.get("provider") or "auto").strip().lower()

    if not url:
        return jsonify({"error": "parameter 'url' wajib"}), 400
    if not url.startswith("http"):
        return jsonify({"error": "url harus dimulai http:// atau https://"}), 400

    if provider == "auto":
        low = url.lower()
        if "linkvertise" in low:
            provider = "linkvertise"
        elif "move2link" in low:
            provider = "move2link"
        else:
            provider = "safebypass"

    if provider == "linkvertise":
        target = "https://api.zyvor.my.id/api/bypass/bypasslinkv2?url=" + quote(url, safe="")
    elif provider == "move2link":
        target = "https://api.zyvor.my.id/api/bypass/move2link?url=" + quote(url, safe="")
    else:
        target = "https://safebypass.vercel.app/api/bypass?url=" + quote(url, safe="")

    try:
        r = requests.get(target, timeout=TIMEOUT)

        try:
            raw = r.json()
        except Exception:
            return jsonify({
                "error": "response bukan JSON",
                "provider": provider,
                "raw": r.text[:500],
            }), 502

        bypassed = None
        original = None
        response_time = None

        if isinstance(raw, dict):
            if "result" in raw and isinstance(raw["result"], dict):
                res = raw["result"]
                bypassed = res.get("bypassedUrl") or res.get("bypassed") or res.get("url")
                original = res.get("originalUrl") or res.get("original")
                response_time = res.get("responseTime")
            if not bypassed:
                bypassed = raw.get("bypassed") or raw.get("url") or raw.get("result") or raw.get("link")
            if not original:
                original = raw.get("original") or url
            if not response_time:
                response_time = raw.get("responseTime")

        if not bypassed:
            return jsonify({
                "error": "ga bisa extract bypassedUrl",
                "provider": provider,
                "raw": raw,
            }), 422

        return jsonify({
            "ok": True,
            "provider": provider,
            "originalUrl": original or url,
            "bypassedUrl": bypassed,
            "responseTime": response_time,
        })

    except requests.exceptions.Timeout:
        return jsonify({"error": "upstream timeout", "provider": provider}), 504
    except Exception as e:
        return jsonify({
            "error": "proxy error: " + type(e).__name__ + ": " + str(e),
            "provider": provider,
        }), 500


@app.route("/api/web2apk", methods=["POST", "GET"])
def api_web2apk():
    if request.method == "POST":
        data = request.json or {}
    else:
        data = request.args.to_dict()

    url = (data.get("url") or "").strip()
    app_name = (data.get("appName") or "").strip()
    package_name = (data.get("packageName") or "").strip()
    version_name = (data.get("versionName") or "1.0.0").strip()
    version_code = str(data.get("versionCode") or "1").strip()

    if not url:
        return jsonify({"error": "parameter 'url' wajib"}), 400
    if not url.startswith("http"):
        return jsonify({"error": "url harus dimulai http:// atau https://"}), 400
    if not app_name:
        return jsonify({"error": "parameter 'appName' wajib"}), 400
    if not package_name:
        return jsonify({"error": "parameter 'packageName' wajib"}), 400

    target = (
        "https://api.zyvor.my.id/api/tools/web2apk"
        "?url=" + quote(url, safe="")
        + "&appName=" + quote(app_name, safe="")
        + "&packageName=" + quote(package_name, safe="")
        + "&versionName=" + quote(version_name, safe="")
        + "&versionCode=" + quote(version_code, safe="")
    )

    try:
        r = requests.get(target, timeout=TIMEOUT)

        try:
            raw = r.json()
        except Exception:
            return jsonify({
                "error": "response bukan JSON",
                "raw": r.text[:500],
            }), 502

        download_url = None
        response_time = None

        if isinstance(raw, dict):
            if "result" in raw and isinstance(raw["result"], dict):
                res = raw["result"]
                download_url = res.get("downloadUrl") or res.get("apkUrl") or res.get("url") or res.get("link")
                response_time = res.get("responseTime")
            if not download_url:
                download_url = raw.get("downloadUrl") or raw.get("apkUrl") or raw.get("url") or raw.get("link") or raw.get("result")
            if not response_time:
                response_time = raw.get("responseTime")

        if not download_url:
            return jsonify({
                "error": "ga bisa extract downloadUrl",
                "raw": raw,
            }), 422

        return jsonify({
            "ok": True,
            "downloadUrl": download_url,
            "responseTime": response_time,
            "appName": app_name,
            "packageName": package_name,
            "versionName": version_name,
            "versionCode": version_code,
        })

    except requests.exceptions.Timeout:
        return jsonify({"error": "upstream timeout (APK building bisa lama, coba lagi)"}), 504
    except Exception as e:
        return jsonify({
            "error": "proxy error: " + type(e).__name__ + ": " + str(e),
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
