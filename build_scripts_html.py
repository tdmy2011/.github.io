import json, os, sys

workspace = r'C:\Users\Administrator\WorkBuddy\2026-05-31-11-24-40'
json_path = os.path.join(workspace, 'YouTube_series_data.json')
html_path = os.path.join(workspace, 'YouTube系列脚本_10期完整版.html')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build the full HTML
h = []
h.append('''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>YouTube系列脚本 10期完整版</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Microsoft YaHei','PingFang SC',sans-serif;background:#0f172a;color:#e2e8f0}
.wrap{display:flex;min-height:100vh}
.side{width:280px;background:#1e293b;padding:24px 0;position:fixed;top:0;left:0;bottom:0;overflow-y:auto;border-right:1px solid #334155;z-index:100}
.side h3{padding:16px 20px;font-size:14px;font-weight:700;color:#38bdf8;border-bottom:1px solid #334155}
.si{display:flex;align-items:center;gap:10px;padding:12px 20px;cursor:pointer;transition:all .2s;font-size:13px;color:#94a3b8;border-left:3px solid transparent;line-height:1.4}
.si:hover{background:#334155;color:#e2e8f0}
.si.on{background:#0f172a;color:#38bdf8;border-left-color:#38bdf8}
.sn{width:24px;height:24px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex-shrink:0}
.si.on .sn{background:#38bdf8!important;color:#0f172a!important}
.st{padding:16px 20px;margin-top:16px;border-top:1px solid #334155;font-size:12px;color:#64748b}
.main{margin-left:280px;flex:1;padding:32px 32px 80px}
.ep{background:#1e293b;border-radius:16px;margin-bottom:32px;border:1px solid #334155;overflow:hidden}
.eh{padding:24px 32px;cursor:pointer;display:flex;align-items:center;gap:16px;transition:background .2s}
.eh:hover{background:#334155}
.en{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:800;color:#fff;flex-shrink:0}
.ei{flex:1}
.et{font-size:20px;font-weight:700;color:#f1f5f9}
.em{font-size:13px;color:#64748b;margin-top:4px;display:flex;gap:16px;flex-wrap:wrap}
.eb{display:inline-block;padding:2px 10px;border-radius:4px;font-size:11px;font-weight:600}
.ebd{display:none;padding:0 32px 32px}
.ep.open .ebd{display:block}
.ep.open .eh{border-bottom:1px solid #334155}
.tabs{display:flex;gap:8px;margin-bottom:24px;padding-top:16px}
.tb{padding:8px 20px;border-radius:8px;font-size:13px;font-weight:600;cursor:pointer;background:#334155;color:#94a3b8;transition:all .2s}
.tb.on{background:#38bdf8;color:#0f172a}
.tc{display:none}.tc.on{display:block}
.sl{font-size:12px;font-weight:600;color:#38bdf8;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;padding:4px 12px;background:rgba(56,189,248,0.1);border-radius:4px;display:inline-block;margin-top:16px}
.stx{font-size:15px;line-height:1.9;color:#cbd5e1;padding:16px 20px;background:#0f172a;border-radius:10px;border-left:3px solid #38bdf8;white-space:pre-wrap;margin-bottom:16px}
.stx b{color:#f59e0b}
.stx em{color:#38bdf8;font-weight:600}
.sg{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.sb{background:#0f172a;border-radius:10px;padding:16px}
.sb h4{font-size:13px;color:#38bdf8;margin-bottom:8px}
.sb p{font-size:13px;color:#94a3b8;line-height:1.6}
.tl{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.ti{background:#334155;padding:4px 10px;border-radius:4px;font-size:11px;color:#94a3b8}
.th{background:#0f172a;border-radius:10px;padding:20px;margin-top:16px}
.th h4{font-size:14px;color:#f59e0b;margin-bottom:8px}
.th p{font-size:13px;color:#94a3b8;line-height:1.6}
.banner{text-align:center;padding:24px;margin-bottom:32px;background:linear-gradient(135deg,#1e3a5f,#312e81);border-radius:16px}
.banner .tag{font-size:14px;color:#38bdf8;font-weight:600;letter-spacing:2px;margin-bottom:12px}
.banner h1{font-size:32px;font-weight:800;color:#fff;margin-bottom:12px}
.banner p{font-size:16px;color:#94a3b8}
.banner .chips{margin-top:16px;display:flex;justify-content:center;gap:12px;flex-wrap:wrap}
.banner .chip{background:rgba(255,255,255,0.1);padding:4px 16px;border-radius:20px;font-size:12px;color:#e2e8f0}
.ytt{margin-bottom:20px}.ytt strong{color:#38bdf8}
.ytt .en{color:#64748b;font-size:13px}
@media(max-width:1024px){.side{display:none}.main{margin-left:0}}
</style></head><body><div class="wrap"><div class="side"><h3>10期系列脚本目录</div>''')

episodes = data if isinstance(data, list) else data.get('episodes', [])

for ep in episodes:
    h.append(f'<div class="si" id="s{ep["num"]}" onclick="go({ep["num"]})"><div class="sn" style="background:{ep["color"]}20;color:{ep["color"]}">{ep["num"]:02d}</div>{ep["title"]}<br><span style="font-size:11px;color:#64748b">{ep["tag"]} | {ep["duration"]}</span></div>\n')

h.append('<div class="st">总时长：约75分钟<br>系列：东南亚安全合规100条<br>节奏：每周2期</div></div><div class="main">')
h.append('<div class="banner"><div class="tag">YOUTUBE SERIES SCRIPTS</div><h1>东南亚工厂安全合规自查清单100条</h1><p>10期系列脚本 · 每期5-8分钟 · 含SEO关键词+标签+缩略图创意</p><div class="chips"><span class="chip">10期完整脚本</span><span class="chip">SEO关键词</span><span class="chip">缩略图创意</span></div></div>')

for ep in episodes:
    n = ep['num']
    h.append(f'<div class="ep" id="ep{n}"><div class="eh" onclick="tog(this.parentElement)"><div class="en" style="background:{ep["color"]}">{n:02d}</div><div class="ei"><div class="et">第{n}期：{ep["title"]}</div><div class="em"><span>{ep["duration"]}</span><span>第{ep["range"]}条</span><span class="eb" style="background:{ep["color"]}30;color:{ep["color"]}">{ep["tag"]}</span></div></div></div><div class="ebd">')

    h.append(f'<div class="tabs"><div class="tb on" onclick="tab(event,\'sc{n}\')">完整脚本</div><div class="tb" onclick="tab(event,\'seo{n}\')">SEO+标签</div><div class="tb" onclick="tab(event,\'th{n}\')">缩略图</div></div>')

    # Script tab
    h.append(f'<div class="tc on" id="sc{n}"><div class="ytt"><strong>YouTube标题：</strong> {ep["yt_title"]}</div>')

    h.append(f'<div class="sl">开场钩子 (10秒)</div><div class="stx">{ep["hook"]}</div>')
    h.append(f'<div class="sl">自我介绍 (5秒)</div><div class="stx">我是安全生产专家，30年实战经验，专注中资出海企业安全合规。</div>')
    h.append(f'<div class="sl">本期概述 (15秒)</div><div class="stx">{ep["outline"]}</div>')

    for sec_title, sec_body in ep['sections']:
        h.append(f'<div class="sl">正文讲解</div><div class="stx"><b>【{sec_title}】</b>\n\n{sec_body}</div>')

    h.append(f'<div class="sl">结尾CTA (30秒)</div><div class="stx" style="border-left-color:#f59e0b">{ep["cta"]}</div></div>')

    # SEO tab
    h.append(f'<div class="tc" id="seo{n}"><div class="sg"><div class="sb"><h4>中文关键词</h4><div class="tl">')
    for kw in ep['keywords'].split(','):
        h.append(f'<div class="ti">{kw.strip()}</div>')
    h.append('</div></div><div class="sb"><h4>YouTube标签</h4><div class="tl">')
    for t in ep['tags'].split(','):
        h.append(f'<div class="ti">{t.strip()}</div>')
    h.append('</div></div></div></div>')

    # Thumbnail tab
    h.append(f'<div class="tc" id="th{n}"><div class="th"><h4>缩略图创意</h4><p>{ep["thumb"]}</p></div></div>')

    h.append('</div></div>')  # close ebd and ep

h.append('</div></div>')  # close main and wrap
h.append('''<script>
function tog(c){c.classList.toggle('open')}
function tab(e,id){let p=e.target.parentElement;while(p&&!p.classList.contains('ebd'))p=p.parentElement;let ts=p.querySelectorAll('.tb'),cs=p.querySelectorAll('.tc');ts.forEach(t=>t.classList.remove('on'));cs.forEach(c=>c.classList.remove('on'));e.target.classList.add('on');document.getElementById(id).classList.add('on')}
function go(n){document.querySelectorAll('.ep').forEach(c=>c.classList.remove('open'));document.getElementById('ep'+n).classList.add('open');document.getElementById('ep'+n).scrollIntoView({behavior:'smooth',block:'start'});document.querySelectorAll('.si').forEach(s=>s.classList.remove('on'));document.getElementById('s'+n).classList.add('on')}
</script></body></html>''')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(''.join(h))

size = os.path.getsize(html_path)
print(f'Generated {len(episodes)} episode scripts')
print(f'Output: {html_path}')
print(f'File size: {size/1024:.1f} KB')
