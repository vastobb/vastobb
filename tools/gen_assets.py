#!/usr/bin/env python3
"""Generates the hand-tuned animated SVGs for the vastobb profile.

Everything is pure SMIL + geometry (no scripts survive GitHub's sanitizer, and
<img>-embedded SVGs cannot load external fonts). Layouts are computed for a
monospace advance of 0.6em. Tweak the palette below and re-run:

    python3 tools/gen_assets.py
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)

FONT = 'ui-monospace, &quot;SFMono-Regular&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace'

GREY = "#9AA3B8"
DIM = "#6C7387"
INK = "#E6E8F0"
P = "#7C4DFF"   # primary (violet)
PC = "#9A7DFF"  # primary container
S = "#00D4FF"   # secondary (cyan)
T = "#33E1B5"   # tertiary (mint)
RED = "#FF5D73"
AMBER = "#FFD166"

DUR = "16s"     # hero master loop


def head(w, h, title, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" font-family=\'{FONT}\'>\n'
            f'<title>{title}</title><desc>{desc}</desc>')


def kt_list(times):
    return ";".join(f"{t:.5f}".rstrip("0").rstrip(".") for t in times)


def kt_vals(vals):
    return ";".join(str(v) for v in vals)


# ============================================================== hero.svg ====
def hero():
    w, h = 1024, 410
    FADE = 0.915  # boot lines power down here (fraction of master loop)

    # typed command: prompt is 19 chars -> starts at 64 + 171 = 235
    cmd = "./boot.sh --profile"
    step = 9.0
    cw = len(cmd) * step  # 171
    n = len(cmd)
    cmd_kt = [0.02 + (i - 1) * (0.058 / (n - 1)) for i in range(1, n + 1)]
    cmd_kt_full = [0.0] + cmd_kt + [0.99, 1.0]
    cmd_vals = ["0"] + [f"{i * step:.0f}" for i in range(1, n + 1)] + [f"{cw:.0f}", f"{cw:.0f}"]
    caret_vals = ["239"] + [f"{235 + i * step + 4:.0f}" for i in range(1, n + 1)] + [f"{235 + cw + 4:.0f}"] * 2
    caret_kt = [0, 0.028, 0.033, 0.955, 0.96, 1]
    caret_v = ["0", "0", "1", "1", "0", "0"]

    # boot lines: slide + snap in, fade out at FADE
    def boot_line(i, y, content, a):
        kt = [0, a, a + 0.004, FADE, FADE + 0.004, 1]
        op = ["0", "0", "1", "1", "0", "0"]
        tr = ["0 7", "0 7", "0 0", "0 0", "0 7", "0 7"]
        return (f'<g><text x="64" y="{y}" font-size="15">{content}'
                f'<animate attributeName="opacity" values="{kt_vals(op)}" keyTimes="{kt_list(kt)}" dur="{DUR}" calcMode="discrete" repeatCount="indefinite"/></text>'
                f'<animateTransform attributeName="transform" type="translate" values="{kt_vals(tr)}" keyTimes="{kt_list(kt)}" dur="{DUR}" repeatCount="indefinite"/>'
                f'</g>')

    # equalizer
    hs = [16, 30, 44, 26, 38, 20, 46, 32, 18, 42, 28, 36, 22, 44, 30, 16, 40, 26, 34, 20, 46, 24, 38, 18]
    bars = []
    for i, bh in enumerate(hs):
        x = 620 + i * 16
        pk = min(int(bh * 1.4), 48)
        dur = round(1.1 + (i % 4) * 0.12, 2)
        beg = round(-((i * 0.37) % dur), 2)
        col = [P, S, T][i % 3]
        bars.append(
            f'<rect x="{x}" y="{356-bh}" width="9" height="{bh}" rx="4.5" fill="{col}" opacity=".9">'
            f'<animate attributeName="height" values="{bh};{pk};{bh}" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="{356-bh};{356-pk};{356-bh}" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
            f'</rect>')
    bars_svg = "\n    ".join(bars)

    # storm (16s master): 0.56 .. 0.638
    storm_kt = [0, 0.56, 0.572, 0.583, 0.594, 0.605, 0.616, 0.627, 0.638, 1]
    storm_j = ["0 0", "0 0", "5 -3", "-6 2", "4 1", "-3 -2", "6 -1", "-4 2", "0 0", "0 0"]
    flash_kt = [0, .562, .564, .566, .568, .570, .572, .574, .576, .60, .601, 1]
    flash_v = ["0", "0", ".14", "0", ".09", "0", ".17", "0", ".05", "0", ".03", "0"]

    def slice_clip(cid, ys, dur):
        return (f'<clipPath id="{cid}"><rect x="0" y="{ys[0]}" width="1024" height="13">'
                f'<animate attributeName="y" values="{kt_vals(ys)}" dur="{dur}" repeatCount="indefinite" calcMode="discrete"/>'
                f'</rect></clipPath>')

    vs = "\n      ".join(f'<line x1="{512 + i * 18.4:.0f}" y1="300" x2="{512 + i * 80}" y2="410"/>' for i in range(-6, 7))
    hors = "\n      ".join(f'<line x1="0" y1="{y}" x2="1024" y2="{y}"/>' for y in (300, 318, 342, 370, 404))
    title = "VASTOBB"

    style = """<style>
.chip rect { transition: fill-opacity .25s, stroke-opacity .25s }
.chip:hover rect { fill-opacity: .34; stroke-opacity: .85 }
.chip text { transition: fill .25s }
.chip:hover text { fill: #FFFFFF }
.m3c { transition: transform .3s cubic-bezier(.2,.7,.3,1.1), filter .3s; transform-box: fill-box; transform-origin: center }
.m3c:hover { transform: translateY(-4px) scale(1.03); filter: drop-shadow(0 8px 20px rgba(124,77,255,.5)) }
.m3c rect { transition: stroke .3s }
.m3c:hover rect { stroke: #7C4DFF }
.pill text { transition: opacity .18s }
.pill .alt { opacity: 0 }
.pill:hover .base { opacity: 0 }
.pill:hover .alt { opacity: 1 }
.pill rect { transition: stroke-opacity .25s; pointer-events: all }
.pill:hover rect { stroke-opacity: 1 }
</style>"""

    return f'''{head(w, h, "VASTOBB — retro arcade banner", "Animated retro x Material 3 banner: boot sequence, glitch storm, hover-reactive chips")}
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0E1119"/><stop offset="1" stop-color="#0B0D13"/></linearGradient>
  <radialGradient id="blobP"><stop offset="0" stop-color="{P}" stop-opacity=".5"/><stop offset="1" stop-color="{P}" stop-opacity="0"/></radialGradient>
  <radialGradient id="blobC"><stop offset="0" stop-color="{S}" stop-opacity=".34"/><stop offset="1" stop-color="{S}" stop-opacity="0"/></radialGradient>
  <radialGradient id="blobM"><stop offset="0" stop-color="{T}" stop-opacity=".3"/><stop offset="1" stop-color="{T}" stop-opacity="0"/></radialGradient>
  <linearGradient id="metaLine" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{P}" stop-opacity="0"/><stop offset=".5" stop-color="{P}" stop-opacity=".55"/><stop offset="1" stop-color="{S}" stop-opacity="0"/></linearGradient>
  <linearGradient id="playg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{P}"/><stop offset="1" stop-color="{S}"/></linearGradient>
  <radialGradient id="vig"><stop offset=".62" stop-color="#000000" stop-opacity="0"/><stop offset="1" stop-color="#000000" stop-opacity=".5"/></radialGradient>
  <pattern id="scan" width="3" height="3" patternUnits="userSpaceOnUse"><rect width="3" height="1" fill="#FFFFFF" opacity="0.035"/></pattern>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="7"/></filter>
  <clipPath id="typeClip"><rect x="235" y="259" width="0" height="20">
    <animate attributeName="width" values="{kt_vals(cmd_vals)}" keyTimes="{kt_list(cmd_kt_full)}" dur="{DUR}" repeatCount="indefinite" calcMode="discrete" fill="freeze"/>
  </rect></clipPath>
  {slice_clip("sliceA", [92, 150, 104, 160, 120, 108], "5s")}
  {slice_clip("sliceB", [122, 96, 148, 110, 136, 88], "6.1s")}
</defs>
{style}

<rect width="{w}" height="{h}" fill="url(#bg)" pointer-events="none"/>

<g stroke="{P}" stroke-width="1" opacity=".8" fill="none" pointer-events="none">
  <g opacity=".14">
      {vs}
  </g>
  <g opacity=".10">
      {hors}
  </g>
  <animate attributeName="opacity" values=".6;1;.6" dur="9s" repeatCount="indefinite"/>
</g>

<g style="mix-blend-mode:screen" pointer-events="none">
  <g>
    <circle cx="800" cy="170" r="170" fill="url(#blobP)">
      <animate attributeName="r" values="170;186;170" dur="13s" repeatCount="indefinite"/>
    </circle>
    <animateTransform attributeName="transform" type="translate" values="0 0;24 -14;0 0" dur="19s" repeatCount="indefinite"/>
  </g>
  <g>
    <circle cx="660" cy="300" r="150" fill="url(#blobC)">
      <animate attributeName="r" values="150;162;150" dur="17s" repeatCount="indefinite"/>
    </circle>
    <animateTransform attributeName="transform" type="translate" values="0 0;-22 10;0 0" dur="23s" repeatCount="indefinite"/>
  </g>
  <g>
    <circle cx="930" cy="280" r="130" fill="url(#blobM)">
      <animate attributeName="r" values="130;144;130" dur="21s" repeatCount="indefinite"/>
    </circle>
    <animateTransform attributeName="transform" type="translate" values="0 0;14 16;0 0" dur="27s" repeatCount="indefinite"/>
  </g>
</g>

<g font-size="13" letter-spacing="1">
  <g class="chip">
    <rect x="40" y="38" width="88" height="26" rx="13" fill="{P}" fill-opacity=".16" stroke="{P}" stroke-opacity=".35"/>
    <text x="54" y="55" fill="#B7A6FF">● 64-BIT</text>
  </g>
  <g class="chip">
    <rect x="138" y="38" width="90" height="26" rx="13" fill="{S}" fill-opacity=".13" stroke="{S}" stroke-opacity=".3"/>
    <text x="152" y="55" fill="#7FE3FF">■ AMOLED</text>
  </g>
  <g class="chip">
    <rect x="238" y="38" width="100" height="26" rx="13" fill="{T}" fill-opacity=".12" stroke="{T}" stroke-opacity=".3"/>
    <text x="252" y="55" fill="#8CE9C9">▲ NO ROOT</text>
  </g>
</g>

<g>
  <g font-size="84" font-weight="700" letter-spacing="6">
    <text x="40" y="152" fill="{P}" opacity=".45" filter="url(#soft)">{title}</text>
    <text x="43" y="151" fill="{P}" opacity=".8">{title}
      <animateTransform attributeName="transform" type="translate" values="3 -2;-3 2;2 -1;-1 1;0 0" dur="5.6s" repeatCount="indefinite" calcMode="discrete"/>
    </text>
    <text x="40" y="152" fill="{S}" opacity=".6">{title}
      <animateTransform attributeName="transform" type="translate" values="-3 1;2 -2;-2 2;1 -1;0 0" dur="6.4s" repeatCount="indefinite" calcMode="discrete"/>
    </text>
    <g clip-path="url(#sliceA)" opacity=".85">
      <text x="40" y="152" fill="{S}">{title}</text>
      <animateTransform attributeName="transform" type="translate" values="4 0;-5 0;3 0;0 0" dur="5s" repeatCount="indefinite" calcMode="discrete"/>
    </g>
    <g clip-path="url(#sliceB)" opacity=".85">
      <text x="40" y="152" fill="{PC}">{title}</text>
      <animateTransform attributeName="transform" type="translate" values="-4 0;5 0;-2 0;0 0" dur="6.1s" repeatCount="indefinite" calcMode="discrete"/>
    </g>
    <text x="40" y="152" fill="#F4F6FC">{title}</text>
  </g>
  <animateTransform attributeName="transform" type="translate" values="{kt_vals(storm_j)}" keyTimes="{kt_list(storm_kt)}" dur="{DUR}" repeatCount="indefinite" calcMode="discrete"/>
</g>

<text x="41" y="188" font-size="16" letter-spacing="0.6" fill="{GREY}">android internals · virtual displays · reverse engineering · graphics</text>

<g class="chip">
  <rect x="878" y="38" width="106" height="26" rx="13" fill="url(#playg)"/>
  <text x="931" y="55" font-size="12.5" font-weight="700" fill="#0B0D13" text-anchor="middle">▶ PLAY</text>
  <animate attributeName="opacity" values="1;.75;1" dur="2.2s" repeatCount="indefinite"/>
</g>

<g>
  <rect x="40" y="214" width="520" height="156" rx="20" fill="#12151D" opacity=".94" stroke="#2A2F3D"/>
  <circle cx="64" cy="229" r="4" fill="{RED}" opacity=".9"/>
  <circle cx="80" cy="229" r="4" fill="{AMBER}" opacity=".85"/>
  <circle cx="96" cy="229" r="4" fill="{T}" opacity=".85"/>
  <text x="114" y="233" font-size="12" fill="{GREY}">~/vastobb — zsh</text>
  <text x="546" y="233" font-size="11" fill="{GREY}" text-anchor="end">REC</text>
  <circle cx="518" cy="229" r="4" fill="{RED}">
    <animate attributeName="opacity" values="1;.15;1" keyTimes="0;.5;1" dur="1.8s" calcMode="discrete" repeatCount="indefinite"/>
  </circle>
  <line x1="40" y1="244" x2="560" y2="244" stroke="#2A2F3D"/>
  <g font-size="15">
    <text x="64" y="271"><tspan fill="{T}">vastobb@fedora</tspan><tspan fill="{GREY}">:~$ </tspan></text>
    <g clip-path="url(#typeClip)"><text x="235" y="271" fill="{INK}">{cmd}</text></g>
    <rect x="239" y="258" width="8" height="17" fill="{T}">
      <animate attributeName="x" values="{kt_vals(caret_vals)}" keyTimes="{kt_list(cmd_kt_full)}" dur="{DUR}" repeatCount="indefinite" calcMode="discrete" fill="freeze"/>
      <animate attributeName="opacity" values="{kt_vals(caret_v)}" keyTimes="{kt_list(caret_kt)}" dur="{DUR}" calcMode="discrete" repeatCount="indefinite"/>
    </rect>
    {boot_line(1, 298, f'<tspan fill="{T}">[  OK  ]</tspan><tspan fill="{GREY}"> virtualdisplay 1080×2400 @60hz</tspan>', 0.125)}
    {boot_line(2, 322, f'<tspan fill="{T}">[  OK  ]</tspan><tspan fill="{GREY}"> shizuku daemon → 127.0.0.1:43110</tspan>', 0.175)}
    {boot_line(3, 346, f'<tspan fill="{T}">[  OK  ]</tspan><tspan fill="{GREY}"> ocr pp-ocrv2 · 6.6k labels loaded</tspan>', 0.225)}
  </g>
</g>

<g class="m3c">
  <rect x="760" y="84" width="154" height="154" rx="34" fill="#12151D" stroke="#2A2F3D">
    <animate attributeName="rx" values="34;44;34" keyTimes="0;.5;1" keySplines=".4 0 .2 1;.4 0 .2 1" calcMode="spline" dur="9s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate" values="0 0;0 -8;0 0" dur="7s" repeatCount="indefinite"/>
  </rect>
  <text x="837" y="172" font-size="44" font-weight="700" fill="{PC}" text-anchor="middle" letter-spacing="2">M3</text>
  <rect x="802" y="192" width="70" height="22" rx="11" fill="{P}" opacity=".18"/>
  <text x="837" y="207" font-size="12" fill="#B7A6FF" text-anchor="middle">retro/</text>
</g>
<g>
  <rect x="646" y="228" width="112" height="112" rx="28" fill="none" stroke="{P}" opacity=".5" stroke-width="1.5">
    <animate attributeName="rx" values="28;38;28" keyTimes="0;.5;1" keySplines=".4 0 .2 1;.4 0 .2 1" calcMode="spline" dur="8s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate" values="0 0;0 -6;0 0" dur="9s" begin="-3s" repeatCount="indefinite"/>
  </rect>
</g>
<g>
  <circle cx="956" cy="104" r="16" fill="{T}" opacity=".85">
    <animate attributeName="r" values="16;19;16" dur="3.2s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values=".85;.5;.85" dur="3.2s" repeatCount="indefinite"/>
  </circle>
</g>
<g class="pill">
  <rect x="640" y="62" width="132" height="34" rx="17" fill="none" stroke="{S}" stroke-opacity=".55"/>
  <text class="base" x="706" y="84" font-size="13" fill="#7FE3FF" text-anchor="middle">127.0.0.1:43110</text>
  <text class="alt" x="706" y="84" font-size="13" fill="{T}" text-anchor="middle">● connected</text>
</g>

<g>
    {bars_svg}
</g>

<line x1="40" y1="382" x2="984" y2="382" stroke="url(#metaLine)"/>
<text x="40" y="396" font-size="12" fill="{DIM}">© 2026 · built by hand in a terminal</text>
<text x="984" y="396" font-size="12" fill="{DIM}" text-anchor="end">amoled · 60fps · click anywhere → arcade</text>

<rect width="{w}" height="{h}" fill="url(#vig)" pointer-events="none"/>
<rect x="0" y="-3" width="{w}" height="{h+6}" fill="url(#scan)" pointer-events="none">
  <animateTransform attributeName="transform" type="translate" values="0 0;0 3" dur="0.5s" repeatCount="indefinite"/>
</rect>
<rect x="0" y="-30" width="{w}" height="26" fill="#FFFFFF" opacity=".035" pointer-events="none">
  <animate attributeName="y" values="-30;420" dur="{DUR}" repeatCount="indefinite"/>
</rect>
<rect width="{w}" height="{h}" fill="#FFFFFF" opacity="0" pointer-events="none">
  <animate attributeName="opacity" values="{kt_vals(flash_v)}" keyTimes="{kt_list(flash_kt)}" dur="{DUR}" calcMode="discrete" repeatCount="indefinite"/>
</rect>
</svg>
'''


# ============================================================= cards.svg ====
def card_files():
    """Four separate hover-reactive cards, each wrapped in a real link in the README."""
    defs = [
        ("card-kuro.svg", P, "STAGE 01", "kuro", "isolated app vault · import, run, forget",
         "KOTLIN·COMPOSE", "4.8k", "63 files · 5 workflows", "github.com/vastobb/kuro", 40, 12),
        ("card-shadowauto.svg", S, "STAGE 02", "ShadowAuto-Build", "virtual displays driven by tool calls",
         "JAVA·C++·PY", "42.9k", "268 files · ci pipeline", "github.com/vastobb/ShadowAuto-Build", 40, 12),
        ("card-fedora.svg", T, "STAGE 03", "fedora", ".so loader RE — ghidra runs in CI",
         "C++·PYTHON", "3.0k", "26 files · 2 workflows", "github.com/vastobb/fedora", 40, 12),
        ("card-onigiri.svg", AMBER, "STAGE 04", "onigiri", "temporal renderer for phone GPUs",
         "JAVA·GLSL", "4.9k", "32 files · shader gate", "github.com/vastobb/onigiri", 40, 12),
    ]
    out = []
    for fname, acc, stage, name, tag, chip, loc, meta, url, x, y in defs:
        w, h = 488, 104
        chip_w = len(chip) * 7.8 + 20
        style = (
            "<style>\n"
            ".frame { transition: stroke .25s, filter .25s }\n"
            ".card:hover .frame { stroke: " + acc + "; filter: drop-shadow(0 6px 16px rgba(0,0,0,.55)) }\n"
            ".card { transition: transform .28s cubic-bezier(.2,.7,.3,1.1); transform-box: fill-box; transform-origin: center }\n"
            ".card:hover { transform: translateY(-4px) }\n"
            ".url { opacity: 0; transition: opacity .25s, transform .25s; transform: translateX(-6px) }\n"
            ".card:hover .url { opacity: 1; transform: translateX(0) }\n"
            "</style>")
        svg = f'''{head(w, h, name + " — project card", stage + ": " + tag)}
{style}
<g class="card">
  <rect class="frame" x="0" y="0" width="488" height="104" rx="24" fill="#12151D" stroke="#2A2F3D"/>
  <rect x="16" y="20" width="4" height="64" rx="2" fill="{acc}" opacity=".9"/>
  <text x="34" y="27" font-size="11" letter-spacing="2" fill="{DIM}">{stage}</text>
  <rect x="{458-chip_w:.0f}" y="14" width="{chip_w:.0f}" height="20" rx="10" fill="{acc}" opacity=".12"/>
  <text x="458" y="28" font-size="10.5" fill="{acc}" text-anchor="end" opacity=".95">{chip}</text>
  <text x="34" y="56" font-size="22" font-weight="700" fill="{INK}">{name}</text>
  <text x="34" y="80" font-size="12" fill="{GREY}">{tag}</text>
  <text class="url" x="34" y="97" font-size="11" fill="#7FE3FF">{url}</text>
  <text x="458" y="56" font-size="21" font-weight="700" fill="{acc}" text-anchor="end">{loc}</text>
  <text x="458" y="72" font-size="10.5" fill="{DIM}" text-anchor="end">loc</text>
  <text x="458" y="90" font-size="10.5" fill="{GREY}" text-anchor="end">{meta}</text>
</g>
</svg>
'''
        out.append((fname, svg))
    return out


# ============================================================== play.svg ====
def play_button():
    w, h = 384, 74
    return f'''{head(w, h, "press start", "button linking to the live arcade")}
<style>
.btnrect {{ transition: filter .25s }}
.play:hover .btnrect {{ filter: drop-shadow(0 8px 24px rgba(124,77,255,.65)) }}
.pulse {{ animation: pip 2s ease-in-out infinite }}
@keyframes pip {{ 0%,100% {{ opacity:.5 }} 50% {{ opacity:1 }} }}
</style>
<defs>
  <linearGradient id="pg" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{P}"/><stop offset=".55" stop-color="{S}"/><stop offset="1" stop-color="{T}"/>
  </linearGradient>
</defs>
<g class="play" cursor="pointer">
  <rect class="btnrect" x="0" y="0" width="{w}" height="{h}" rx="24" fill="url(#pg)"/>
  <rect class="pulse" x="4" y="4" width="{w-8}" height="{h-8}" rx="20" fill="none" stroke="#FFFFFF" stroke-opacity=".35"/>
  <text x="{w/2}" y="32" font-size="17" font-weight="700" fill="#0B0D13" text-anchor="middle" letter-spacing="2">▶ PRESS START</text>
  <text x="{w/2}" y="52" font-size="10.5" fill="#0B0D13" text-anchor="middle" opacity=".75" letter-spacing="1">vastobb.github.io/vastobb — real pac-man inside</text>
</g>
</svg>
'''


# =========================================================== cabinet.svg ====
def cabinet():
    w, h = 1024, 320

    # pellets: two rows, pac eats row 1
    pellets = []
    px0, px1, pstep = 384, 656, 17
    pac_t0, pac_t1 = 376, 656
    for row_y in (148, 196):
        i = 0
        x = px0
        while x <= px1:
            if row_y == 148:
                ti = max(0.0, (x - 6 - pac_t0) / (pac_t1 - pac_t0))
                kt = [0, ti, ti + 0.004, 1]
                op = ["1", "1", "0", "0"]
                pellets.append(f'<circle cx="{x}" cy="{row_y}" r="2.2" fill="{INK}" opacity=".8">'
                               f'<animate attributeName="opacity" values="{kt_vals(op)}" keyTimes="{kt_list(kt)}" dur="5.2s" calcMode="discrete" repeatCount="indefinite"/></circle>')
            else:
                pellets.append(f'<circle cx="{x}" cy="{row_y}" r="2.2" fill="{INK}" opacity=".8"/>')
            x += pstep
    pellets_svg = "\n      ".join(pellets)

    # pac mouth frames (local coords, facing right)
    m0 = "M0,-10 A10,10 0 1,0 0,10 A10,10 0 1,0 0,-10"
    m1 = "M0,0 L8.66,-5 A10,10 0 1,1 8.66,5 Z"
    m2 = "M0,0 L9.85,-1.74 A10,10 0 1,1 9.85,1.74 Z"

    # score: discrete stack
    scores = ["0x0000", "0x03F0", "0x07E0", "0x0BD0", "0x0FFF"]
    score_txt = []
    for i, sc in enumerate(scores):
        a = 0.06 + i * 0.14
        kt = [0, a, a + 0.004, 0.97, 0.975, 1]
        op = ["0", "0", "1", "1", "0", "0"]
        score_txt.append(f'<text x="652" y="120" font-size="10" fill="{AMBER}" text-anchor="end">{sc}'
                         f'<animate attributeName="opacity" values="{kt_vals(op)}" keyTimes="{kt_list(kt)}" dur="5.2s" calcMode="discrete" repeatCount="indefinite"/></text>')

    bulbs_a, bulbs_b = [], []
    for i in range(13):
        x = 368 + i * 24
        tgt = bulbs_a if i % 2 == 0 else bulbs_b
        beg = "0s" if i % 2 == 0 else "-0.6s"
        tgt.append(f'<circle cx="{x}" cy="24" r="3.5" fill="{AMBER}">'
                   f'<animate attributeName="opacity" values="1;.15;1" keyTimes="0;.5;1" dur="1.2s" begin="{beg}" calcMode="discrete" repeatCount="indefinite"/></circle>')

    def ghost(gid, fill, vals, beg):
        return f'''<g>
      <g>
        <circle cx="0" cy="0" r="7.5" fill="{fill}"/>
        <circle cx="-4.5" cy="6" r="2.4" fill="{fill}"/><circle cx="0" cy="7.2" r="2.4" fill="{fill}"/><circle cx="4.5" cy="6" r="2.4" fill="{fill}"/>
        <circle cx="-2.4" cy="-2" r="2.4" fill="#FFFFFF"/><circle cx="2.4" cy="-2" r="2.4" fill="#FFFFFF"/>
        <circle cx="-1.8" cy="-2" r="1.1" fill="#0B0D13"/><circle cx="3" cy="-2" r="1.1" fill="#0B0D13"/>
      </g>
      <animateTransform attributeName="transform" type="translate" values="{vals}" dur="5.2s" begin="{beg}" repeatCount="indefinite"/>
    </g>'''

    stroke_dash = 'stroke-dasharray="3 11" stroke-linecap="round" stroke-width="2" fill="none"'
    return f'''{head(w, h, "VASTOBB arcade cabinet", "animated arcade cabinet playing a live mini-game")}
<defs>
  <linearGradient id="cab" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#141824"/><stop offset="1" stop-color="#0E1119"/></linearGradient>
  <linearGradient id="mq" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{P}"/><stop offset=".55" stop-color="{S}"/><stop offset="1" stop-color="{T}"/></linearGradient>
  <radialGradient id="glow"><stop offset="0" stop-color="{P}" stop-opacity=".3"/><stop offset="1" stop-color="{P}" stop-opacity="0"/></radialGradient>
  <pattern id="scan2" width="2" height="2" patternUnits="userSpaceOnUse"><rect width="2" height="1" fill="#FFFFFF" opacity="0.05"/></pattern>
  <clipPath id="scr"><rect x="360" y="104" width="304" height="140" rx="8"/></clipPath>
</defs>

<ellipse cx="512" cy="200" rx="240" ry="150" fill="url(#glow)"/>

<g>
  <rect x="40" y="88" width="248" height="120" rx="24" fill="#12151D" stroke="#2A2F3D"/>
  <text x="64" y="118" font-size="12" letter-spacing="2" fill="{DIM}">HIGH SCORE</text>
  <text x="64" y="158" font-size="30" font-weight="800" fill="{AMBER}">0x1337</text>
  <text x="64" y="182" font-size="11" fill="{GREY}">set by vastobb · unbroken</text>
  <animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="6.5s" repeatCount="indefinite"/>
</g>
<g>
  <rect x="736" y="88" width="248" height="120" rx="24" fill="#12151D" stroke="#2A2F3D"/>
  <text x="760" y="118" font-size="12" letter-spacing="2" fill="{DIM}">CREDITS</text>
  <text x="760" y="158" font-size="30" font-weight="800" fill="{T}">01</text>
  <text x="760" y="182" font-size="11" fill="{GREY}">insert coin → play</text>
  <animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="7.5s" begin="-2s" repeatCount="indefinite"/>
</g>

<rect x="332" y="12" width="360" height="296" rx="28" fill="url(#cab)" stroke="#2A2F3D"/>
<rect x="340" y="20" width="344" height="280" rx="22" fill="none" stroke="#1A1E29"/>
<rect x="346" y="120" width="8" height="150" rx="4" fill="url(#mq)" opacity=".4"/>
<rect x="670" y="120" width="8" height="150" rx="4" fill="url(#mq)" opacity=".4"/>

{"".join(bulbs_a)}
{"".join(bulbs_b)}
<rect x="352" y="32" width="320" height="56" rx="16" fill="url(#mq)" opacity=".16" stroke="#2A2F3D"/>
<text x="512" y="70" font-size="30" font-weight="700" letter-spacing="8" fill="{INK}" text-anchor="middle">VASTOBB</text>

<rect x="352" y="96" width="320" height="156" rx="14" fill="#0B0D13" stroke="#2A2F3D"/>
<rect x="360" y="104" width="304" height="140" rx="8" fill="#05060A" stroke="#1A1E29"/>

<g clip-path="url(#scr)">
  <text x="368" y="120" font-size="10" fill="{RED}">1UP
    <animate attributeName="opacity" values="1;.2;1" keyTimes="0;.5;1" dur="1s" calcMode="discrete" repeatCount="indefinite"/>
  </text>
  {"".join(score_txt)}
  <g>
    {pellets_svg}
  </g>
  <g>
    <path d="{m0}" fill="{AMBER}" stroke="{AMBER}" stroke-width="0.5" stroke-linejoin="round">
      <animate attributeName="d" values="{m0};{m1};{m0};{m2};{m0}" keyTimes="0;.15;.35;.75;.9" dur="0.36s" calcMode="discrete" repeatCount="indefinite"/>
    </path>
    <animateTransform attributeName="transform" type="translate" values="{pac_t0} 148;{pac_t1} 148" dur="5.2s" repeatCount="indefinite"/>
  </g>
  {ghost("g1", RED, "648 196;512 191;376 196", "0s")}
  {ghost("g2", S, "648 191;512 196;376 191", "-2.6s")}
  <rect x="360" y="104" width="304" height="140" fill="url(#scan2)" opacity=".5"/>
  <rect x="360" y="104" width="304" height="12" fill="#FFFFFF" opacity=".045">
    <animate attributeName="y" values="104;232" dur="3.4s" repeatCount="indefinite"/>
  </rect>
  <text x="512" y="238" font-size="8" letter-spacing="2" fill="{DIM}" text-anchor="middle">DEMO PLAY · INSERT COIN</text>
</g>

<rect x="344" y="252" width="336" height="12" rx="6" fill="#1A1E29"/>

<g>
  <ellipse cx="420" cy="286" rx="16" ry="6" fill="#0B0D13" stroke="#2A2F3D"/>
  <rect x="417" y="262" width="6" height="22" rx="3" fill="{GREY}"/>
  <circle cx="420" cy="258" r="8" fill="{RED}"/>
  <animateTransform attributeName="transform" type="rotate" values="-7 420 286;7 420 286;-7 420 286" dur="2.6s" repeatCount="indefinite"/>
</g>
<circle cx="560" cy="282" r="9" fill="{T}">
  <animate attributeName="r" values="9;7.6;9" dur="1.9s" begin="-0.3s" repeatCount="indefinite"/>
</circle>
<circle cx="592" cy="282" r="9" fill="{AMBER}">
  <animate attributeName="r" values="9;7.6;9" dur="1.9s" begin="-1.2s" repeatCount="indefinite"/>
</circle>
<rect x="636" y="276" width="26" height="14" rx="4" fill="#0B0D13" stroke="#2A2F3D"/>
<line x1="642" y1="283" x2="656" y2="283" stroke="{S}" stroke-width="1.5"/>

<text x="512" y="304" font-size="9" letter-spacing="2" fill="{DIM}" text-anchor="middle">VASTOBB ELECTRONICS · MK.3 · PURE SMIL</text>
</svg>
'''


# ========================================================== divider.svg ====
def divider():
    w, h = 1024, 44
    dl = 'stroke-dasharray="3 11" stroke-linecap="round" stroke-width="2" fill="none"'
    return f'''{head(w, h, "section divider", "marching dashes and three pulsing diamonds")}
<line x1="40" y1="22" x2="424" y2="22" stroke="{P}" opacity=".45" {dl}>
  <animate attributeName="stroke-dashoffset" values="0;14" dur="0.9s" repeatCount="indefinite"/>
</line>
<line x1="600" y1="22" x2="984" y2="22" stroke="{S}" opacity=".4" {dl}>
  <animate attributeName="stroke-dashoffset" values="14;0" dur="0.9s" repeatCount="indefinite"/>
</line>
<rect x="473" y="17" width="10" height="10" rx="2" fill="{P}" transform="rotate(45 478 22)">
  <animate attributeName="opacity" values=".35;1;.35" dur="2.4s" repeatCount="indefinite"/>
</rect>
<rect x="507" y="17" width="10" height="10" rx="2" fill="{S}" transform="rotate(45 512 22)">
  <animate attributeName="opacity" values=".35;1;.35" dur="2.4s" begin="-0.8s" repeatCount="indefinite"/>
</rect>
<rect x="541" y="17" width="10" height="10" rx="2" fill="{T}" transform="rotate(45 546 22)">
  <animate attributeName="opacity" values=".35;1;.35" dur="2.4s" begin="-1.6s" repeatCount="indefinite"/>
</rect>
</svg>
'''


builders = [("hero.svg", hero), ("cabinet.svg", cabinet), ("divider.svg", divider), ("play.svg", play_button)]
for name, fn in builders:
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(fn())
    print("wrote", os.path.normpath(path), os.path.getsize(path), "bytes")
for name, svg in card_files():
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", os.path.normpath(path), os.path.getsize(path), "bytes")
