<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>CTF: Safe Upload? — Don’t Panic</title>
<style>
  :root{
    --bg:#0b0f17;
    --fg:#e6fff2;
    --accent:#00ff9c;
    --accent-2:#42c6ff;
    --muted:#8aa0a6;
    --card:#111728cc;
    --glow:0 0 30px rgba(0,255,156,.25), 0 0 8px rgba(66,198,255,.2);
  }
  *{box-sizing:border-box}
  html,body{height:100%}
  body{
    margin:0; color:var(--fg); background:radial-gradient(1200px 600px at 75% -10%, rgba(66,198,255,.12), transparent 60%),
    radial-gradient(900px 700px at -10% 30%, rgba(0,255,156,.12), transparent 60%), var(--bg);
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Hiragino Kaku Gothic ProN", "Noto Sans JP", "BIZ UDPGothic", "Helvetica Neue", Arial, "Apple Color Emoji", "Segoe UI Emoji";
    line-height:1.6;
    overflow-x:hidden;
  }

  /* Starfield */
  .stars, .stars:after, .stars:before{
    content:"";
    position:absolute; inset:0;
    background-repeat:repeat;
    background-image:
      radial-gradient(2px 2px at 20px 30px, rgba(255,255,255,.9) 50%, transparent 51%),
      radial-gradient(1px 1px at 150px 80px, rgba(255,255,255,.7) 50%, transparent 51%),
      radial-gradient(1.5px 1.5px at 90px 120px, rgba(255,255,255,.8) 50%, transparent 51%),
      radial-gradient(1px 1px at 250px 200px, rgba(255,255,255,.6) 50%, transparent 51%);
    animation: drift 120s linear infinite;
    opacity:.4;
  }
  .stars:before{ animation-duration: 160s; opacity:.3; filter: blur(0.5px);}
  .stars:after{ animation-duration: 220s; opacity:.2; filter: blur(1px);}
  @keyframes drift{
    from{ background-position:0 0, 0 0, 0 0, 0 0; }
    to{   background-position:2000px 1000px, -1500px 800px, 1500px -1200px, -2000px -1600px; }
  }

  .wrap{position:relative; min-height:100%; display:grid; place-items:center; padding:6vmin 3vmin;}
  .panel{
    width:min(720px, 94vw);
    background:linear-gradient(180deg, rgba(17,23,40,.9), rgba(17,23,40,.8));
    border:1px solid rgba(66,198,255,.2);
    border-radius:20px;
    box-shadow: var(--glow);
    padding:clamp(20px,4vmin,36px);
    backdrop-filter: blur(6px);
  }

  .title{
    display:flex; align-items:center; gap:14px; margin:0 0 10px;
    font-weight:800; letter-spacing:.4px; text-transform:uppercase;
  }
  .title .badge{
    font-size:12px; color:#001a12; background:var(--accent); padding:4px 8px; border-radius:999px;
    letter-spacing:.8px; box-shadow:0 0 0 2px rgba(0,255,156,.2) inset;
  }
  .title h1{
    margin:0; font-size:clamp(22px, 3.2vmin, 30px); font-weight:800;
    background: linear-gradient(90deg, var(--accent), var(--accent-2));
    -webkit-background-clip:text; background-clip:text; color:transparent;
    text-shadow: 0 0 18px rgba(0,255,156,.2);
  }

  .dontpanic{
    position:absolute; top:14px; right:14px;
    font-weight:900; font-size:14px; color:#001a12; background:var(--accent);
    border-radius:12px; padding:6px 10px; transform: rotate(3deg);
    box-shadow:0 6px 18px rgba(0,255,156,.25);
  }

  .subtitle{
    margin:6px 0 18px; color:var(--muted);
  }

  form{
    margin-top:14px; display:grid; gap:14px;
    background: rgba(255,255,255,.02);
    border:1px dashed rgba(66,198,255,.35);
    border-radius:16px; padding:16px;
  }
  label{
    font-size:14px; color:var(--fg);
  }
  .picker{
    display:flex; align-items:center; gap:10px; flex-wrap:wrap;
  }
  input[type="file"]{ display:none; }
  .file-btn{
    appearance:none; border:none; cursor:pointer; border-radius:12px;
    padding:12px 16px; font-weight:700; color:#02130c; background:var(--accent);
    box-shadow:0 8px 20px rgba(0,255,156,.25);
  }
  .file-name{
    min-height:1.4em; color:var(--muted); font-family:ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  }
  .submit{
    display:flex; justify-content:flex-end;
  }
  .submit button{
    appearance:none; border:none; cursor:pointer; border-radius:14px;
    padding:12px 18px; font-weight:900; letter-spacing:.3px;
    color:#06131f; background:linear-gradient(90deg, var(--accent), var(--accent-2));
    box-shadow:0 10px 24px rgba(66,198,255,.28), inset 0 0 0 1px rgba(255,255,255,.15);
    transition: transform .08s ease, box-shadow .2s ease;
  }
  .submit button:hover{ transform: translateY(-1px); }
  .submit button:active{ transform: translateY(0); box-shadow:0 6px 14px rgba(66,198,255,.22); }

  .foot{
    margin-top:16px; display:flex; justify-content:space-between; align-items:center; gap:8px; color:var(--muted); font-size:12px;
  }
  .chip{
    display:inline-flex; align-items:center; gap:6px; padding:6px 10px; border-radius:999px;
    border:1px solid rgba(66,198,255,.25); color:var(--fg); background:rgba(66,198,255,.07);
    font-family:ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  }
</style>
</head>
<body>
<div class="stars" aria-hidden="true"></div>
<div class="wrap">
  <div class="panel">
    <div class="dontpanic">DON’T PANIC</div>

    <div class="title">
      <span class="badge">42</span>
      <h1>CTF: Safe Upload? — The Hitchhiker’s Uploader</h1>
    </div>

    <p class="subtitle">Even if I get lost somewhere in the universe,<em>Mostly Harmless</em> is ok. If it's dangerous, the guidebook (YARA) will gently stop you.</p>

    <form method="post" action="/upload.php" enctype="multipart/form-data">
      <label for="file">Submissions for the guide</label>
      <div class="picker">
        <label class="file-btn" for="file">🛸 Choose your file</label>
        <input id="file" type="file" name="file" required />
        <span class="file-name" id="fileName">Nothing is selected.</span>
      </div>
      <div class="submit">
        <button type="submit">Send</button>
      </div>
    </form>

    <div class="foot">
      <span class="chip">yarayara</span>
      <span class="chip">planet: Earth (mostly)</span>
    </div>
  </div>
</div>

<script>
  const input = document.getElementById('file');
  const nameEl = document.getElementById('fileName');
  input.addEventListener('change', () => {
    nameEl.textContent = input.files?.[0]?.name || 'Nothing is selected.';
  });
</script>
</body>
</html>
