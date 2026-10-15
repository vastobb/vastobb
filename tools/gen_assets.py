#!/usr/bin/env python3
"""Generates hand-tuned animated SVGs for the vastobb profile (retro x Material 3)."""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)

FONT = 'ui-monospace, &quot;SFMono-Regular&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace'
# Use single-quoted XML attribute instead, to keep double quotes simple:

GREY = "#9AA3B8"
DIM = "#6C7387"
INK = "#E6E8F0"
P = "#7C4DFF"   # primary
PC = "#9A7DFF"  # primary container
S = "#00D4FF"   # secondary
T = "#33E1B5"   # tertiary
RED = "#FF5D73"

def head(w, h, title, desc):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" font-family='{FONT}'>
<title>{title}</title><desc>{desc}</desc>'''

# ---------------------------------------------------------------- hero.svg ---
def hero():
    w, h = 1024, 400
    # typed line + clip reveal values (monospace: uniform char pitch)
    phrase = "mobile systems · virtual displays · native mods"
    n = len(phrase)
    step = 9.0  # 15px mono advance
    start_ms_text = 64
    type_seg = 0.5
    kt = ["0"] + [f"{0.06 + (i - 1) * (type_seg / (n - 1)):.5f}" for i in range(1, n + 1)] + ["0.99", "1"]
    vals_w = ["0"] + [f"{i * step:.0f}" for i in range(1, n + 1)] + [f"{n * step:.0f}", f"{n * step:.0f}"]
    vals_x = [f"{start_ms_text}"] + [f"{start_ms_text + i * step:.0f}" for i in range(1, n + 1)] + [f"{start_ms_text + n * step:.0f}"] * 2
    kt_attr = ";".join(kt)
    vw_attr = ";".join(vals_w)
    vx_attr = ";".join(vals_x)
    typed_dur = "12s"

    # equalizer bars
    hs = [16,30,44,26,38,20,46,32,18,42,28,36,22,44,30,16,40,26,34,20,46,24,38,18]
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

    # floor grid
    vs = []
    for i in range(-6, 7):
        xb = 512 + i * 80
        xt = 512 + i * 19.4
        vs.append(f'<line x1="{xt:.0f}" y1="300" x2="{xb}" y2="400"/>')
    verts = "\n      ".join(vs)
    hors = "\n      ".join(f'<line x1="0" y1="{y}" x2="1024" y2="{y}"/>' for y in (300, 316, 336, 360, 390))

    def slice_clip(cid, ys, dur):
        vals = ";".join(str(v) for v in ys)
        return (f'<clipPath id="{cid}"><rect x="0" y="{ys[0]}" width="1024" height="13">'
                f'<animate attributeName="y" values="{vals}" dur="{dur}" repeatCount="indefinite" calcMode="discrete"/>'
                f'</rect></clipPath>')

    title_text = 'VASTOBB'
    return f'''{head(w, h, "VASTOBB — retro profile banner", "Animated retro x Material 3 banner: android internals, virtual displays, reverse engineering, graphics")}
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#0E1119"/><stop offset="1" stop-color="#0B0D13"/>
  </linearGradient>
  <radialGradient id="blobP"><stop offset="0" stop-color="{P}" stop-opacity=".5"/><stop offset="1" stop-color="{P}" stop-opacity="0"/></radialGradient>
  <radialGradient id="blobC"><stop offset="0" stop-color="{S}" stop-opacity=".34"/><stop offset="1" stop-color="{S}" stop-opacity="0"/></radialGradient>
  <radialGradient id="blobM"><stop offset="0" stop-color="{T}" stop-opacity=".3"/><stop offset="1" stop-color="{T}" stop-opacity="0"/></radialGradient>
  <linearGradient id="metaLine" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{P}" stop-opacity="0"/><stop offset=".5" stop-color="{P}" stop-opacity=".55"/><stop offset="1" stop-color="{S}" stop-opacity="0"/></linearGradient>
  <linearGradient id="bar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{P}"/><stop offset=".55" stop-color="{S}"/><stop offset="1" stop-color="{T}"/></linearGradient>
  <radialGradient id="vig"><stop offset=".62" stop-color="#000000" stop-opacity="0"/><stop offset="1" stop-color="#000000" stop-opacity=".5"/></radialGradient>
  <pattern id="scan" width="3" height="3" patternUnits="userSpaceOnUse"><rect width="3" height="1" fill="#FFFFFF" opacity="0.035"/></pattern>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="7"/></filter>
  <clipPath id="typeClip"><rect id="typeRect" x="64" y="282" width="0" height="24">
    <animate attributeName="width" values="{vw_attr}" keyTimes="{kt_attr}" dur="{typed_dur}" begin="1.2s" repeatCount="indefinite" calcMode="discrete" fill="freeze"/>
  </rect></clipPath>
  {slice_clip("sliceA", [92, 150, 104, 160, 120, 108], "5s")}
  {slice_clip("sliceB", [122, 96, 148, 110, 136, 88], "6.1s")}
</defs>

<rect width="{w}" height="{h}" fill="url(#bg)"/>

<g stroke="{P}" stroke-width="1" opacity=".8" fill="none">
  <g opacity=".14">
      {verts}
  </g>
  <g opacity=".10">
      {hors}
  </g>
  <animate attributeName="opacity" values=".6;1;.6" dur="9s" repeatCount="indefinite"/>
</g>

<g>
  <circle cx="800" cy="170" r="170" fill="url(#blobP)"/>
  <animateTransform attributeName="transform" type="translate" values="0 0;24 -14;0 0" dur="19s" repeatCount="indefinite"/>
</g>
<g>
  <circle cx="660" cy="300" r="150" fill="url(#blobC)"/>
  <animateTransform attributeName="transform" type="translate" values="0 0;-22 10;0 0" dur="23s" repeatCount="indefinite"/>
</g>
<g>
  <circle cx="930" cy="280" r="130" fill="url(#blobM)"/>
  <animateTransform attributeName="transform" type="translate" values="0 0;14 16;0 0" dur="27s" repeatCount="indefinite"/>
</g>

<g font-size="13" letter-spacing="1">
  <rect x="40" y="38" width="88" height="26" rx="13" fill="{P}" opacity=".16"/>
  <rect x="40" y="38" width="88" height="26" rx="13" fill="none" stroke="{P}" opacity=".35"/>
  <text x="54" y="55" fill="#B7A6FF">● 64-BIT</text>
  <rect x="138" y="38" width="90" height="26" rx="13" fill="{S}" opacity=".13"/>
  <rect x="138" y="38" width="90" height="26" rx="13" fill="none" stroke="{S}" opacity=".3"/>
  <text x="152" y="55" fill="#7FE3FF">■ AMOLED</text>
  <rect x="238" y="38" width="100" height="26" rx="13" fill="{T}" opacity=".12"/>
  <rect x="238" y="38" width="100" height="26" rx="13" fill="none" stroke="{T}" opacity=".3"/>
  <text x="252" y="55" fill="#8CE9C9">▲ NO ROOT</text>
</g>

<g font-size="84" font-weight="700" letter-spacing="6">
  <text x="40" y="152" fill="{P}" opacity=".45" filter="url(#soft)">{title_text}</text>
  <text x="43" y="151" fill="{P}" opacity=".8">{title_text}
    <animateTransform attributeName="transform" type="translate" values="3 -2;-3 2;2 -1;-1 1;0 0" dur="5.6s" repeatCount="indefinite" calcMode="discrete"/>
  </text>
  <text x="40" y="152" fill="{S}" opacity=".6">{title_text}
    <animateTransform attributeName="transform" type="translate" values="-3 1;2 -2;-2 2;1 -1;0 0" dur="6.4s" repeatCount="indefinite" calcMode="discrete"/>
  </text>
  <g clip-path="url(#sliceA)" opacity=".85">
    <text x="40" y="152" fill="{S}">{title_text}</text>
    <animateTransform attributeName="transform" type="translate" values="4 0;-5 0;3 0;0 0" dur="5s" repeatCount="indefinite" calcMode="discrete"/>
  </g>
  <g clip-path="url(#sliceB)" opacity=".85">
    <text x="40" y="152" fill="{PC}">{title_text}</text>
    <animateTransform attributeName="transform" type="translate" values="-4 0;5 0;-2 0;0 0" dur="6.1s" repeatCount="indefinite" calcMode="discrete"/>
  </g>
  <text x="40" y="152" fill="#F4F6FC">{title_text}</text>
</g>

<text x="41" y="188" font-size="16" letter-spacing="0.6" fill="{GREY}">android internals · virtual displays · reverse engineering · graphics</text>

<g>
  <rect x="40" y="214" width="520" height="138" rx="20" fill="#12151D" opacity=".94" stroke="#2A2F3D"/>
  <circle cx="64" cy="229" r="4" fill="{RED}" opacity=".9"/>
  <circle cx="80" cy="229" r="4" fill="#FFD166" opacity=".85"/>
  <circle cx="96" cy="229" r="4" fill="{T}" opacity=".85"/>
  <text x="114" y="233" font-size="12" fill="{GREY}">~/vastobb — zsh</text>
  <text x="546" y="233" font-size="11" fill="{GREY}" text-anchor="end">REC</text>
  <circle cx="518" cy="229" r="4" fill="{RED}">
    <animate attributeName="opacity" values="1;.15;1" keyTimes="0;.5;1" dur="1.8s" calcMode="discrete" repeatCount="indefinite"/>
  </circle>
  <line x1="40" y1="244" x2="560" y2="244" stroke="#2A2F3D"/>
  <g font-size="15">
    <text x="64" y="271"><tspan fill="{T}">vastobb@fedora</tspan><tspan fill="{GREY}">:~/profile$ </tspan><tspan fill="{INK}">whoami</tspan></text>
    <g clip-path="url(#typeClip)">
      <text x="64" y="298" fill="#8CE9C9">{phrase}</text>
    </g>
    <rect x="64" y="284" width="8" height="17" fill="{T}">
      <animate attributeName="x" values="{vx_attr}" keyTimes="{kt_attr}" dur="{typed_dur}" begin="1.2s" repeatCount="indefinite" calcMode="discrete" fill="freeze"/>
      <animate attributeName="opacity" values="1;0;1" keyTimes="0;.5;1" dur="1s" calcMode="discrete" repeatCount="indefinite"/>
    </rect>
    <text x="64" y="325"><tspan fill="{GREY}">status:</tspan><tspan fill="{INK}"> building the quiet kind of magic</tspan></text>
  </g>
</g>

<g>
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
<g>
  <rect x="640" y="62" width="132" height="34" rx="17" fill="none" stroke="{S}" opacity=".55"/>
  <text x="706" y="84" font-size="13" fill="#7FE3FF" text-anchor="middle">127.0.0.1:43110</text>
</g>

<g>
    {bars_svg}
</g>

<line x1="40" y1="374" x2="984" y2="374" stroke="url(#metaLine)"/>
<text x="40" y="391" font-size="12" fill="{DIM}">© 2026 · built by hand in a terminal</text>
<text x="984" y="391" font-size="12" fill="{DIM}" text-anchor="end">amoled · 60fps · retro-m3</text>

<rect width="{w}" height="{h}" fill="url(#vig)"/>
<rect x="0" y="-3" width="{w}" height="{h+6}" fill="url(#scan)">
  <animateTransform attributeName="transform" type="translate" values="0 0;0 3" dur="0.5s" repeatCount="indefinite"/>
</rect>
</svg>
'''

# ------------------------------------------------------------ divider.svg ---
def divider():
    w, h = 1024, 44
    dl = f'stroke-dasharray="3 11" stroke-linecap="round" stroke-width="2" fill="none"'
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

# ------------------------------------------------------------- footer.svg ---
def footer():
    w, h = 1024, 110
    return f'''{head(w, h, "loading next build", "retro loading bar animation")}
<defs>
  <linearGradient id="bar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{P}"/><stop offset=".55" stop-color="{S}"/><stop offset="1" stop-color="{T}"/></linearGradient>
</defs>
<text x="434" y="36" font-size="13" fill="{GREY}" letter-spacing="1">LOADING NEXT BUILD</text>
<rect x="600" y="24" width="8" height="14" fill="{T}">
  <animate attributeName="opacity" values="1;0;1" keyTimes="0;.5;1" dur="1s" calcMode="discrete" repeatCount="indefinite"/>
</rect>
<rect x="312" y="56" width="400" height="12" rx="6" fill="#12151D" stroke="#2A2F3D"/>
<rect x="315" y="59" width="36" height="6" rx="3" fill="url(#bar)">
  <animate attributeName="width" values="36;358;36" keyTimes="0;.6;1" keySplines=".45 0 .55 1;.45 0 .55 1" calcMode="spline" dur="7s" repeatCount="indefinite"/>
</rect>
<text x="512" y="94" font-size="12" fill="{DIM}" text-anchor="middle">INSERT COIN ▸ <tspan fill="#7FE3FF">github.com/vastobb</tspan></text>
</svg>
'''

for name, fn in (("hero.svg", hero), ("divider.svg", divider), ("footer.svg", footer)):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(fn())
    print("wrote", path, os.path.getsize(path), "bytes")
