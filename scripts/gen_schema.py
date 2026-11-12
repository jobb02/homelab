#!/usr/bin/env python3
"""Génère docs/schema-homelab.svg (schéma réseau du homelab)."""
from html import escape

W, H = 1600, 1250
FONT = "Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
INK, MUTED, LINE, BORDER, BAND = "#111827", "#6b7280", "#374151", "#d1d5db", "#f3f4f6"
out = []


def t(x, y, s, size=14, weight=400, fill=INK, anchor="start", italic=False):
    st = ' font-style="italic"' if italic else ""
    out.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
               f'fill="{fill}" text-anchor="{anchor}"{st}>{escape(s)}</text>')


def rect(x, y, w, h, fill="#fff", stroke=BORDER, rx=12, dash=False, sw=1.5, shadow=False):
    d = ' stroke-dasharray="7 5"' if dash else ""
    f = ' filter="url(#sh)"' if shadow else ""
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
               f'stroke="{stroke}" stroke-width="{sw}"{d}{f}/>')


def chip(x, y, label, dark=False, dash=False):
    w = 7.2 * len(label) + 18
    fill, txt, st = (INK, "#fff", INK) if dark else ("#fff", INK, INK)
    d = ' stroke-dasharray="4 3"' if dash else ""
    out.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="20" rx="10" fill="{fill}" '
               f'stroke="{st}" stroke-width="1.2"{d}/>')
    t(x + w / 2, y + 14, label, 10.5, 700, txt, "middle")
    return w


def card(x, y, w, h, tag, title, sub, dark=False, dash=False, sub2=None):
    fill = INK if dark else "#fff"
    rect(x, y, w, h, fill, INK if dark else (MUTED if dash else BORDER), dash=dash, shadow=not dash)
    tc, sc = ("#fff", "#d1d5db") if dark else ((MUTED, MUTED) if dash else (INK, MUTED))
    if dark:
        out.append(f'<rect x="{x+14}" y="{y+12}" width="{7.2*len(tag)+18:.0f}" height="20" rx="10" '
                   f'fill="#fff"/>')
        t(x + 14 + (7.2 * len(tag) + 18) / 2, y + 26, tag, 10.5, 700, INK, "middle")
    else:
        chip(x + 14, y + 12, tag, dash=dash)
    t(x + 14, y + 54, title, 16, 700, tc)
    t(x + 14, y + 75, sub, 13, 400, sc)
    if sub2:
        t(x + 14, y + 94, sub2, 13, 400, sc)


def line(pts, dash=None, color=LINE, sw=2, arrow=False, arrow_start=False):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = ' marker-end="url(#ar)"' if arrow else ""
    ms = ' marker-start="url(#ar)"' if arrow_start else ""
    p = " ".join(f"{a},{b}" for a, b in pts)
    out.append(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{sw}" '
               f'stroke-linejoin="round"{d}{m}{ms}/>')


def pill(cx, cy, s, size=12, color=MUTED, w=None):
    w = w or 6.6 * len(s) + 20
    out.append(f'<rect x="{cx-w/2:.0f}" y="{cy-12}" width="{w:.0f}" height="24" rx="12" '
               f'fill="#fff" stroke="{BORDER}"/>')
    t(cx, cy + 4, s, size, 500, color, "middle")


# ---------- en-tête ----------
t(48, 62, "Homelab — Mam III Jobb", 30, 800)
t(48, 90, "Topologie réseau · deux hyperviseurs Proxmox VE · pare-feu entre la maison et le lab", 15, 400, MUTED)

# ---------- haut : internet -> switch ----------
CX = 800
rect(CX - 70, 118, 140, 44, "#fff", INK, rx=22, sw=1.8)
t(CX, 146, "Internet", 15, 700, INK, "middle")
card(CX - 140, 196, 280, 88, "ROUTEUR · BOX", "Freebox Server", "192.168.1.254 · DHCP · WireGuard")
line([(CX, 162), (CX, 196)])

card(290, 196, 250, 88, "ACCÈS DISTANT", "Poste d'admin nomade", "hors du domicile")
line([(540, 240), (CX - 140, 240)], dash="3 5", arrow=True)
pill(600, 214, "VPN WireGuard", w=112)

card(CX - 120, 322, 240, 88, "WI-FI", "Répéteur Freebox", "chambre")
line([(CX, 284), (CX, 322)], dash="3 5")
pill(CX + 62, 303, "Wi-Fi mesh", w=96)

card(CX - 150, 438, 300, 88, "SWITCH", "sw-sitea", "TP-Link Omada ES205G · 192.168.1.101")
line([(CX, 410), (CX, 438)])

# ---------- bus ethernet ----------
BUS = 560
xA, xADM, xNAS, xB = 250, 905, 1110, 1340
line([(CX, 526), (CX, BUS)])
line([(xA, BUS), (xB, BUS)], sw=2.5)
for x in (xA, xADM, xNAS, xB, CX):
    out.append(f'<circle cx="{x}" cy="{BUS}" r="4.5" fill="{LINE}"/>')
t(CX + 12, BUS - 10, "Ethernet · 192.168.1.0/24", 12, 500, MUTED)

# ---------- site A ----------
AX, AY, AW, AH = 40, 600, 750, 520
rect(AX, AY, AW, AH, "#fafafa", INK, rx=16, sw=1.8)
line([(xA, BUS), (xA, AY)])
chip(AX + 20, AY + 18, "SITE A", dark=True)
t(AX + 100, AY + 33, "pve-sitea · Proxmox VE 9", 17, 800)
t(AX + 20, AY + 62, "PC Acer · i5-6400T · 16 Go · 192.168.1.100", 13, 400, MUTED)

# vmbr0
rect(AX + 20, AY + 82, AW - 40, 134, BAND, BORDER, rx=12)
t(AX + 36, AY + 104, "vmbr0 · réseau maison · 192.168.1.0/24", 12.5, 700, LINE)
card(AX + 36, AY + 116, 330, 88, "LXC 102", "omada-sitea", "Contrôleur Omada · 192.168.1.24")
DNSX, DNSY = AX + 384, AY + 116
card(DNSX, DNSY, 330, 88, "LXC 105", "dns-sitea", "AdGuard Home · 192.168.1.53")

# OPNsense
FX, FY, FW_, FH = AX + 195, AY + 252, 360, 104
line([(FX + FW_ / 2, AY + 216), (FX + FW_ / 2, FY)], sw=2.5)
t(FX + FW_ / 2 + 10, AY + 238, "WAN 192.168.1.29", 12, 600, LINE)
card(FX, FY, FW_, FH, "PARE-FEU", "fw-sitea · OPNsense", "VM 104 · WAN vtnet0 → vmbr0",
     dark=True, sub2="LAN vtnet1 → vmbr1 · 10.10.10.1")
line([(FX + FW_ / 2, FY + FH), (FX + FW_ / 2, AY + 384)], sw=2.5)
t(FX + FW_ / 2 + 10, AY + 374, "LAN 10.10.10.1", 12, 600, LINE)

# vmbr1
rect(AX + 20, AY + 384, AW - 40, 120, BAND, BORDER, rx=12)
t(AX + 36, AY + 406, "vmbr1 · lab isolé · 10.10.10.0/24 · sans carte physique", 12.5, 700, LINE)
card(AX + 36, AY + 416, 330, 74, "VM 101", "Kali Linux", "")
t(AX + 150, AY + 470, "IP par DHCP (.100 – .200)", 12.5, 400, MUTED)
card(DNSX, AY + 416, 330, 74, "VM 103", "Linux Lite", "")
t(DNSX + 114, AY + 470, "IP par DHCP (.100 – .200)", 12.5, 400, MUTED)

# ---------- colonne centrale ----------
card(xADM - 95, 600, 190, 88, "POSTE", "PC d'admin", "via dock Lenovo")
line([(xADM, BUS), (xADM, 600)])
NX, NY = 850, 718
card(NX, NY, 290, 106, "STOCKAGE · DNS", "nas-sitea", "Synology DS218 · RAID 1", sub2="192.168.1.117 · zone home.arpa")
line([(xNAS, BUS), (xNAS, NY)])
rect(NX, 838, 290, 40, "#fff", BORDER, rx=20)
t(NX + 145, 863, "Cloudflare · Quad9 (DNS over HTTPS)", 12.5, 600, INK, "middle")

# flux DNS
DC = "#6b7280"
line([(xADM - 95, 655), (DNSX + 300, 655), (DNSX + 300, DNSY)], dash="2 4", color=DC, arrow=True, sw=1.6)
pill(742, 655, "requêtes DNS", 11.5, w=100)
line([(DNSX + 330, DNSY + 44), (NX, DNSY + 44)], dash="2 4", color=DC, arrow=True, sw=1.6)
pill(802, DNSY + 26, "home.arpa", 11.5, w=82)
line([(DNSX + 330, DNSY + 70), (NX - 40, DNSY + 70), (NX - 40, 858), (NX, 858)], dash="2 4", color=DC, arrow=True, sw=1.6)

# ---------- site B ----------
BX, BY, BW, BH = 1160, 600, 400, 520
rect(BX, BY, BW, BH, "#fafafa", INK, rx=16, sw=1.8)
line([(xB, BUS), (xB, BY)])
chip(BX + 20, BY + 18, "SITE B", dark=True)
t(BX + 100, BY + 33, "pve-siteb · Proxmox VE 9", 17, 800)
t(BX + 20, BY + 62, "Intel NUC · i5-10210U · 16 Go", 13, 400, MUTED)
t(BX + 20, BY + 80, "192.168.1.102", 13, 400, MUTED)

GX, GY, GW, GH = BX + 30, BY + 252, 340, 104
line([(GX + GW / 2, BY + 96), (GX + GW / 2, GY)], dash="7 5", color=MUTED, sw=2)
card(GX, GY, GW, GH, "PARE-FEU · PRÉVU", "fw-siteb · FortiGate VM", "WAN → vmbr0 · réseau maison",
     dash=True, sub2="LAN → vmbr1 · 10.20.20.1")
line([(GX + GW / 2, GY + GH), (GX + GW / 2, BY + 384)], dash="7 5", color=MUTED, sw=2)
rect(BX + 20, BY + 384, BW - 40, 120, "#fff", MUTED, rx=12, dash=True)
t(BX + 36, BY + 406, "vmbr1 · lab site B · 10.20.20.0/24 · prévu", 12.5, 700, MUTED)
card(BX + 36, BY + 416, BW - 72, 74, "PRÉVU", "VM de test", "", dash=True)

# IPsec
IY = FY + 52
line([(FX + FW_, IY), (GX, IY)], dash="9 6", color=INK, sw=2.2, arrow=True, arrow_start=True)
pill((FX + FW_ + GX) / 2, IY + 26, "Tunnel IPsec site à site · prévu", 12, INK, w=236)

# ---------- légende ----------
LY = 1172
t(48, LY, "Légende", 13, 800)
line([(130, LY - 4), (180, LY - 4)], sw=2.5); t(190, LY, "Ethernet", 12.5, 400, MUTED)
line([(270, LY - 4), (320, LY - 4)], dash="3 5"); t(330, LY, "Wi-Fi / VPN", 12.5, 400, MUTED)
line([(430, LY - 4), (480, LY - 4)], dash="2 4", color=DC, arrow=True, sw=1.6); t(492, LY, "Flux DNS", 12.5, 400, MUTED)
rect(580, LY - 16, 40, 22, "#fff", MUTED, rx=6, dash=True); t(630, LY, "Prévu", 12.5, 400, MUTED)
rect(700, LY - 16, 40, 22, INK, INK, rx=6); t(750, LY, "Pare-feu", 12.5, 400, MUTED)
t(W - 48, LY, "Adresses privées uniquement (RFC 1918) · nommage <rôle>-<site>", 12.5, 400, MUTED, "end")
t(W - 48, LY + 22, "Mise à jour : novembre 2026", 12, 400, MUTED, "end", italic=True)

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
import sys
open(sys.argv[1] if len(sys.argv) > 1 else "schema-homelab.svg", "w").write(svg)
