#!/usr/bin/env python3
"""Génère docs/schema-homelab.svg : schéma réseau du homelab (thème sombre).

Disposition symétrique : site A à gauche, réseau maison (« Internet ») au centre, site B à droite.
Le schéma est décrit en code : quand le lab évolue, on modifie quelques lignes et on relance
    python3 scripts/gen_schema.py docs/schema-homelab.svg
Python standard uniquement, sans dépendance.
"""
import sys
from html import escape
FONT = "Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
INK, MUTED, LINE, BORDER, BAND = "#111827", "#6b7280", "#374151", "#d1d5db", "#f3f4f6"
out = []
S = {"title": 21, "sub": 15.5}
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
    t(x + 16, y + 66, title, S["title"], 700, tc)
    if sub:
        t(x + 16, y + 93, sub, S["sub"], 400, sc)
    if sub2:
        t(x + 16, y + 116, sub2, S["sub"], 400, sc)


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



def save(path, W, H):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<defs>
  <filter id="sh" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#111827" flood-opacity="0.08"/></filter>
  <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker>
</defs>
<rect width="{W}" height="{H}" fill="#ffffff"/>
''' + "\n".join(out) + "\n</svg>\n"
    open(path, "w").write(svg)

S.update(title=23, sub=17)
W,H=1400,1260
t(30,58,"Homelab — Mam III Jobb",34,800); t(30,92,"Site A  ·  réseau maison (« Internet »)  ·  Site B",18,400,MUTED)

out.append('<g transform="translate(0,130)">')
# colonne centrale : transit
CX0,CW=520,360; CXm=CX0+CW/2
rect(CX0-10,108,CW+20,960,"#fafafa",BORDER,rx=18,dash=False)
t(CX0+10,138,"MAISON",14,800,LINE); t(CX0+CW-10,138,"192.168.1.0/24",14,800,LINE,"end")
rect(CXm-70,152,140,44,"#fff",INK,rx=22,sw=2); t(CXm,180,"Internet",18,700,INK,"middle")
line([(CXm,196),(CXm,220)])
card(CX0,220,CW,108,"ROUTEUR · BOX","Freebox Server","192.168.1.254 · WireGuard")
line([(CXm,328),(CXm,356)],dash="3 6"); pill(CXm+70,342,"Wi-Fi mesh",w=112)
card(CX0,356,CW,108,"WI-FI","Répéteur Freebox","chambre")
line([(CXm,464),(CXm,490)])
card(CX0,490,CW,108,"SWITCH · TRANSIT","sw-core","Omada ES205G · 192.168.1.101")
SWY=544
# vers sites
line([(CX0,SWY),(490,SWY)],sw=2.8); line([(CX0+CW,SWY),(910,SWY)],sw=2.8)
# vers poste / NAS
TX=536
line([(TX,598),(TX,982),(CX0+30,982)],sw=2.4); line([(TX,832),(CX0+30,832)],sw=2.4)
for yy in (832,982): dot(TX,yy)
card(CX0+30,770,CW-30,124,"POSTE","PC d'admin","dock Lenovo",sub2="DNS → dns-sitea")
card(CX0+30,920,CW-30,124,"STOCKAGE · DNS","nas-sitea","Synology DS218 · RAID 1",sub2="192.168.1.117 · home.arpa")

def header(x,y,tag,title,l1,l2):
    chip(x+22,y+22,tag,"dark"); t(x+108,y+42,title,24,800)
    t(x+22,y+76,l1,17,400,MUTED); t(x+22,y+100,l2,17,400,MUTED)

# site A
AX,AY,AW=30,108,460
rect(AX,AY,AW,960,"#fafafa",INK,rx=18,sw=2)
header(AX,AY,"SITE A","pve-sitea","Proxmox VE · PC Acer · 16 Go","192.168.1.100 · DNS → dns-sitea")
rect(AX+16,AY+124,AW-32,284,BAND,BORDER); t(AX+32,AY+150,"vmbr0 · réseau maison",16.5,700,LINE)
card(AX+32,AY+164,AW-64,108,"LXC 105","dns-sitea · AdGuard","192.168.1.53 · amont DoH")
card(AX+32,AY+284,AW-64,108,"LXC 102","omada-sitea","Contrôleur · 192.168.1.24")
FY=AY+470; cx=AX+AW/2
line([(cx,AY+408),(cx,FY)],sw=2.8); t(cx+12,AY+444,"WAN 192.168.1.29",15.5,600,LINE)
card(AX+40,FY,AW-80,128,"PARE-FEU","fw-sitea · OPNsense","VM 104",sub2="LAN 10.10.10.1",dark=True)
line([(cx,FY+128),(cx,AY+656)],sw=2.8)
rect(AX+16,AY+656,AW-32,288,BAND,BORDER); t(AX+32,AY+682,"vmbr1 · lab isolé · 10.10.10.0/24",16.5,700,LINE)
card(AX+32,AY+696,AW-64,108,"VM 101","Kali Linux","DHCP .100 – .200")
card(AX+32,AY+816,AW-64,108,"VM 103","Linux Lite","DHCP .100 – .200")

# site B
BX=910
rect(BX,AY,AW,960,"#fafafa",INK,rx=18,sw=2)
header(BX,AY,"SITE B","pve-siteb","Proxmox VE · Intel NUC · 16 Go","192.168.1.102 · DNS → dns-sitea")
bx=BX+AW/2
line([(bx,AY+124),(bx,FY)],dash="8 6",color=MUTED); t(bx+12,AY+444,"WAN → réseau maison",15.5,600,MUTED)
card(BX+40,FY,AW-80,128,"PARE-FEU · PRÉVU","fw-siteb · FortiGate","VM prévue",sub2="LAN 10.20.20.1",dash=True)
line([(bx,FY+128),(bx,AY+656)],dash="8 6",color=MUTED)
rect(BX+16,AY+656,AW-32,168,"#fff",MUTED,dash=True); t(BX+32,AY+682,"vmbr1 · lab site B · 10.20.20.0/24",16.5,700,MUTED)
card(BX+32,AY+696,AW-64,108,"PRÉVU","VM de test","",dash=True)

# IPsec à travers le centre
IY=FY+64
line([(AX+AW-40,IY),(BX+40,IY)],dash="10 7",color=INK,sw=2.6,arrow=True,arrow_start=True)
pill(CXm,IY,"Tunnel IPsec · prévu",15,INK,w=210,weight=700)

LY=1104
line([(30,LY-5),(80,LY-5)],sw=2.8); t(90,LY,"Ethernet",16,400,MUTED)
line([(190,LY-5),(240,LY-5)],dash="3 6"); t(250,LY,"Wi-Fi / VPN",16,400,MUTED)
rect(370,LY-20,44,26,"#fff",MUTED,rx=6,dash=True); t(424,LY,"Prévu",16,400,MUTED)
rect(500,LY-20,44,26,INK,INK,rx=6); t(554,LY,"Pare-feu",16,400,MUTED)
t(W-30,LY,"Adresses privées uniquement · nommage <rôle>-<site>",15,400,MUTED,"end")
out.append('</g>')
# accès distant (au-dessus du centre)
card(CX0,100,CW,104,"ACCÈS DISTANT","Admin nomade","hors du domicile")
line([(CXm,204),(CXm,280)],dash="3 6",arrow=True)
pill(CXm+84,222,"VPN WireGuard",14,LINE,w=140,weight=600)


# ---------- thème sombre : le dessin est fait en clair puis les couleurs sont converties ----------
save(sys.argv[1] if len(sys.argv) > 1 else "schema-homelab.svg", W, H)
path = sys.argv[1] if len(sys.argv) > 1 else "schema-homelab.svg"
svg = open(path).read()
CLAIR_VERS_SOMBRE = [  # (couleur claire, couleur sombre) — remplacement en deux passes pour éviter les collisions
    ('#ffffff', '#0d1117'), ('#fafafa', '#11161d'), ('#fff"', '#1c2128"'), ('#111827', '#e6edf3'),
    ('#6b7280', '#8b949e'), ('#374151', '#c9d1d9'), ('#d1d5db', '#30363d'), ('#f3f4f6', '#161b22'),
]
for i, (clair, _) in enumerate(CLAIR_VERS_SOMBRE):
    svg = svg.replace(clair, f"@{i}@" + ('"' if clair.endswith('"') else ''))
for i, (clair, sombre) in enumerate(CLAIR_VERS_SOMBRE):
    svg = svg.replace(f"@{i}@" + ('"' if clair.endswith('"') else ''), sombre)
svg = svg.replace('flood-color="#e6edf3" flood-opacity="0.08"', 'flood-color="#000" flood-opacity="0.4"')
open(path, "w").write(svg)
