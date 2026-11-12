#!/usr/bin/env python3
"""Génère docs/schema-homelab.svg — schéma réseau du homelab.

Mise en page verticale (1000 px de large) pour rester lisible sur téléphone :
GitHub réduit l'image à la largeur de l'écran, donc moins de largeur = texte plus gros.
Usage : python3 scripts/gen_schema.py docs/schema-homelab.svg
"""
import sys
from html import escape

W, H = 1000, 2040
FONT = "Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
INK, MUTED, LINE, BORDER, BAND = "#111827", "#6b7280", "#374151", "#d1d5db", "#f3f4f6"
out = []


def t(x, y, s, size=16, weight=400, fill=INK, anchor="start", italic=False):
    st = ' font-style="italic"' if italic else ""
    out.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
               f'fill="{fill}" text-anchor="{anchor}"{st}>{escape(s)}</text>')


def rect(x, y, w, h, fill="#fff", stroke=BORDER, rx=12, dash=False, sw=1.5, shadow=False):
    d = ' stroke-dasharray="8 6"' if dash else ""
    f = ' filter="url(#sh)"' if shadow else ""
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
               f'stroke="{stroke}" stroke-width="{sw}"{d}{f}/>')


def chip(x, y, label, style="outline"):
    w = 8.2 * len(label) + 22
    fill, txt, d = {"outline": ("#fff", INK, ""), "dark": (INK, "#fff", ""),
                    "light": ("#fff", INK, ""), "dash": ("#fff", MUTED, ' stroke-dasharray="4 3"')}[style]
    stroke = MUTED if style == "dash" else INK
    out.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="24" rx="12" fill="{fill}" '
               f'stroke="{stroke}" stroke-width="1.3"{d}/>')
    t(x + w / 2, y + 17, label, 12.5, 700, txt, "middle")
    return w


def card(x, y, w, h, tag, title, sub, sub2=None, dark=False, dash=False):
    if dark:
        rect(x, y, w, h, INK, INK, shadow=True)
        cw = 8.2 * len(tag) + 22
        out.append(f'<rect x="{x+16}" y="{y+14}" width="{cw:.0f}" height="24" rx="12" fill="#fff"/>')
        t(x + 16 + cw / 2, y + 31, tag, 12.5, 700, INK, "middle")
        tc, sc = "#fff", "#d1d5db"
    else:
        rect(x, y, w, h, "#fff", MUTED if dash else BORDER, dash=dash, shadow=not dash)
        chip(x + 16, y + 14, tag, "dash" if dash else "outline")
        tc, sc = (MUTED, MUTED) if dash else (INK, MUTED)
    t(x + 16, y + 66, title, 21, 700, tc)
    if sub:
        t(x + 16, y + 92, sub, 15.5, 400, sc)
    if sub2:
        t(x + 16, y + 114, sub2, 15.5, 400, sc)


def line(pts, dash=None, color=LINE, sw=2.2, arrow=False, arrow_start=False):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = ' marker-end="url(#ar)"' if arrow else ""
    ms = ' marker-start="url(#ar)"' if arrow_start else ""
    p = " ".join(f"{a},{b}" for a, b in pts)
    out.append(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{sw}" '
               f'stroke-linejoin="round"{d}{m}{ms}/>')


def dot(x, y):
    out.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{LINE}"/>')


def pill(cx, cy, s, size=14, color=MUTED, w=None, weight=500):
    w = w or 7.6 * len(s) + 24
    out.append(f'<rect x="{cx-w/2:.0f}" y="{cy-14}" width="{w:.0f}" height="28" rx="14" '
               f'fill="#fff" stroke="{BORDER}"/>')
    t(cx, cy + 5, s, size, weight, color, "middle")


def label(x, y, s):
    t(x, y, s, 14.5, 600, LINE)


# ---------- en-tête ----------
t(40, 58, "Homelab — Mam III Jobb", 32, 800)
t(40, 90, "Deux hyperviseurs Proxmox VE · pare-feu entre la maison et le lab", 17, 400, MUTED)

# ---------- maison : internet -> switch ----------
CX = 640
rect(CX - 72, 118, 144, 46, "#fff", INK, rx=23, sw=2)
t(CX, 147, "Internet", 17, 700, INK, "middle")
line([(CX, 164), (CX, 196)])
card(480, 196, 320, 104, "ROUTEUR · BOX", "Freebox Server", "192.168.1.254 · DHCP · WireGuard")

card(40, 196, 320, 104, "ACCÈS DISTANT", "Admin nomade", "hors du domicile")
line([(360, 252), (480, 252)], dash="3 6", arrow=True)
pill(420, 226, "VPN", w=56)

line([(CX, 300), (CX, 336)], dash="3 6")
pill(CX + 78, 318, "Wi-Fi mesh", w=112)
card(500, 336, 280, 104, "WI-FI", "Répéteur Freebox", "chambre")
line([(CX, 440), (CX, 474)])
card(480, 474, 320, 104, "SWITCH · TRANSIT", "sw-core", "Omada ES205G · 192.168.1.101")

# ---------- bus ethernet ----------
BUS, TRUNK = 616, 22
line([(CX, 578), (CX, BUS)])
line([(TRUNK, BUS), (CX, BUS)], sw=2.8)
for x in (180, 525, CX):
    dot(x, BUS)
for i, txt in enumerate(["Réseau maison", "192.168.1.0/24", "= « Internet »", "entre les deux sites"]):
    t(716, 682 + 22 * i, txt, 15, 600 if i < 2 else 400, LINE if i < 2 else MUTED)

card(40, 656, 290, 120, "POSTE", "PC d'admin", "dock Lenovo", sub2="DNS → dns-sitea")
line([(180, BUS), (180, 656)])
card(360, 656, 330, 120, "STOCKAGE · DNS", "nas-sitea", "Synology DS218 · RAID 1", sub2="192.168.1.117 · zone home.arpa")
line([(525, BUS), (525, 656)])

# tronc vers les deux sites (à gauche)
AY, BY = 820, 1488
line([(TRUNK, BUS), (TRUNK, BY + 34), (40, BY + 34)], sw=2.8)
line([(TRUNK, AY + 34), (40, AY + 34)], sw=2.8)
dot(TRUNK, BUS); dot(TRUNK, AY + 34)


def site_header(y, tagtxt, title, sub):
    chip(64, y + 22, tagtxt, "dark")
    t(150, y + 41, title, 22, 800)
    t(64, y + 76, sub, 15.5, 400, MUTED)


# ---------- site A ----------
rect(40, AY, 900, 618, "#fafafa", INK, rx=18, sw=2)
site_header(AY, "SITE A", "pve-sitea · Proxmox VE 9", "PC Acer · i5-6400T · 16 Go · 192.168.1.100 · DNS → dns-sitea")

rect(60, AY + 98, 860, 156, BAND, BORDER)
t(78, AY + 124, "vmbr0 · réseau maison", 15.5, 700, LINE)
card(78, AY + 138, 405, 104, "LXC 105", "dns-sitea · AdGuard", "192.168.1.53 · amont : DoH")
card(497, AY + 138, 405, 104, "LXC 102", "omada-sitea", "Contrôleur Omada · 192.168.1.24")

FX, FY, FW_ = 290, AY + 296, 400
line([(490, AY + 254), (490, FY)], sw=2.8)
label(504, AY + 281, "WAN 192.168.1.29")
card(FX, FY, FW_, 124, "PARE-FEU", "fw-sitea · OPNsense", "VM 104 · WAN vtnet0 → vmbr0", sub2="LAN vtnet1 → vmbr1", dark=True)
line([(490, FY + 124), (490, AY + 452)], sw=2.8)
label(504, AY + 442, "LAN 10.10.10.1")

rect(60, AY + 452, 860, 156, BAND, BORDER)
t(78, AY + 478, "vmbr1 · lab isolé · 10.10.10.0/24", 15.5, 700, LINE)
card(78, AY + 492, 405, 104, "VM 101", "Kali Linux", "DHCP .100 – .200")
card(497, AY + 492, 405, 104, "VM 103", "Linux Lite", "DHCP .100 – .200")

# ---------- site B ----------
rect(40, BY, 900, 470, "#fafafa", INK, rx=18, sw=2)
site_header(BY, "SITE B", "pve-siteb · Proxmox VE 9", "Intel NUC · i5-10210U · 16 Go · 192.168.1.102 · DNS → dns-sitea")

GY = BY + 136
line([(490, BY + 96), (490, GY)], dash="8 6", color=MUTED, sw=2.2)
card(FX, GY, FW_, 124, "PARE-FEU · PRÉVU", "fw-siteb · FortiGate", "WAN → vmbr0 · réseau maison", sub2="LAN → vmbr1 · 10.20.20.1", dash=True)
line([(490, GY + 124), (490, BY + 300)], dash="8 6", color=MUTED, sw=2.2)
rect(60, BY + 300, 860, 148, "#fff", MUTED, dash=True)
t(78, BY + 326, "vmbr1 · lab site B · 10.20.20.0/24 · prévu", 15.5, 700, MUTED)
card(78, BY + 340, 824, 96, "PRÉVU", "VM de test", "", dash=True)

# ---------- tunnel IPsec ----------
IX = 968
line([(FX + FW_, FY + 62), (IX, FY + 62), (IX, GY + 62), (FX + FW_, GY + 62)],
     dash="10 7", color=INK, sw=2.6, arrow=True, arrow_start=True)
pill(820, BY - 25, "Tunnel IPsec site à site · prévu", 14, INK, w=262, weight=700)

# ---------- légende ----------
LY = 1998
line([(40, LY - 5), (90, LY - 5)], sw=2.8); t(100, LY, "Ethernet", 15, 400, MUTED)
line([(200, LY - 5), (250, LY - 5)], dash="3 6"); t(260, LY, "Wi-Fi / VPN", 15, 400, MUTED)
rect(380, LY - 20, 44, 26, "#fff", MUTED, rx=6, dash=True); t(434, LY, "Prévu", 15, 400, MUTED)
rect(510, LY - 20, 44, 26, INK, INK, rx=6); t(564, LY, "Pare-feu", 15, 400, MUTED)
t(W - 40, LY, "Adresses privées · <rôle>-<site>", 15, 400, MUTED, "end")
t(W - 40, LY + 24, "Mise à jour : novembre 2026", 13.5, 400, MUTED, "end", italic=True)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<defs>
  <filter id="sh" x="-10%" y="-10%" width="120%" height="140%">
    <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#111827" flood-opacity="0.08"/>
  </filter>
  <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/>
  </marker>
</defs>
<rect width="{W}" height="{H}" fill="#ffffff"/>
{chr(10).join(out)}
</svg>
'''
open(sys.argv[1] if len(sys.argv) > 1 else "schema-homelab.svg", "w").write(svg)
