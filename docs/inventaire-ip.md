# Inventaire des adresses IP

[← 14 · Règles dans le tunnel](14-regles-tunnel.md) · [Sommaire de la documentation](README.md) · [Accueil du dépôt](../README.md)

> Mis à jour le 17 novembre 2026. Uniquement des adresses privées (RFC 1918), non joignables depuis Internet. Les IP fixes sont tenues par des réservations DHCP : la Freebox pour le réseau maison, chaque pare-feu pour son lab.

## Règles d'adressage

- Le 2ᵉ octet des labs indique le site : `10.10` = A, `10.20` = B, `10.30` = C.
- Dans chaque lab : `.1` = pare-feu, `.2–.99` = IP fixes, `.100–.200` = DHCP.
- Toute machine visée par une règle de pare-feu reçoit une réservation : sinon, l'alias ou l'objet qui la désigne peut pointer vers une adresse qui a changé.
- Noms au format `<rôle>-<site>` ; numéros de VM : `1xx` = site A, `2xx` = site B, `3xx` = site C.

## Réseau maison — 192.168.1.0/24

Passerelle : Freebox `192.168.1.254`. Ce réseau joue le rôle d'Internet entre les trois pare-feux.

| IP | Nom | Équipement | Hébergé sur |
| --- | --- | --- | --- |
| `.24` | `omada-sitea` | Contrôleur Omada (LXC 102) | `pve-sitea` |
| `.29` | `fw-sitea` | OPNsense, interface WAN (VM 104) | `pve-sitea` |
| `.30` | `fw-siteb` | FortiGate, port1 = WAN (VM 201) | `pve-siteb` |
| `.31` | `fw-sitec` | Sophos Firewall, Port2 = WAN (VM 301) | `pve-siteb` |
| `.53` | `dns-sitea` | AdGuard Home (LXC 105) | `pve-sitea` |
| `.99` | PC d'admin | Poste d'administration (alias `PC_ADMIN`) | physique |
| `.100` | `pve-sitea` | Proxmox VE, PC Acer | physique |
| `.101` | `sw-core` | Switch Omada ES205G | physique |
| `.102` | `pve-siteb` | Proxmox VE, Intel NUC (sites B et C) | physique |
| `.117` | `nas-sitea` | NAS Synology DS218 | physique |
| `.254` | Freebox | Passerelle et DHCP du réseau maison | physique |

## Site A, le siège — 10.10.10.0/24 (pont `vmbr1` de `pve-sitea`)

| IP | Machine | Attribution |
| --- | --- | --- |
| `.1` | `fw-sitea` (OPNsense, LAN) | statique |
| `.10` | Kali Linux (VM 101) | réservation Dnsmasq |
| `.11` | Linux Lite (VM 103) | réservation Dnsmasq |
| `.100–.200` | autres VM de test | DHCP d'OPNsense |

## Site B, l'agence 1 — 10.20.20.0/24 (pont `vmbr1` de `pve-siteb`)

| IP | Machine | Attribution |
| --- | --- | --- |
| `.1` | `fw-siteb` (FortiGate, port2) | statique |
| `.101` | `poste-siteb` (VM 202) | DHCP du FortiGate, à réserver avant de le viser dans une règle |

## Site C, l'agence 2 — 10.30.30.0/24 (pont `vmbr2` de `pve-siteb`)

| IP | Machine | Attribution |
| --- | --- | --- |
| `.1` | `fw-sitec` (Sophos, Port1) | statique |
| `.100` | `poste-sitec` (VM 302) | DHCP de Sophos, visé par les règles du tunnel ([fiche 14](14-regles-tunnel.md)) : à réserver en priorité |

## À faire

- Réserver les adresses de `poste-siteb` et `poste-sitec`.
- Ajouter un enregistrement dans la zone DNS `home.arpa` pour chaque équipement, pour ne plus dépendre des adresses.

---

[← 14 · Règles dans le tunnel](14-regles-tunnel.md) · [Sommaire de la documentation](README.md) · [Accueil du dépôt](../README.md)
