# 01 — Virtualisation (Proxmox VE)

## Matériel
- Hôte : PC Acer dédié, nom de nœud `proxmox`, branché en Ethernet via le switch Omada.
- Administration : interface web Proxmox (port 8006) depuis le LAN, écran HDMI en secours.

## Pourquoi Proxmox VE
- Gratuit, basé sur Debian/KVM : très proche de ce qu'on retrouve en entreprise côté hyperviseur open source.
- Gère **les VM (KVM)** et **les conteneurs (LXC)** dans la même interface.
- Snapshots avant chaque manip risquée → on peut casser et revenir en arrière, c'est le principe d'un lab.

## VM ou LXC : comment je choisis
| Besoin | Choix | Raison |
|---|---|---|
| OS différent du noyau Linux (Windows) | VM | Un LXC partage le noyau de l'hôte, donc Linux uniquement |
| Outil offensif / isolé (Kali) | VM | Isolation plus forte qu'un conteneur |
| Petit service Linux (Omada, AdGuard) | LXC | Démarre en secondes, consomme très peu de RAM |

## Inventaire
| ID | Type | Rôle |
|---|---|---|
| 104 | VM | OPNsense — pare-feu du lab |
| 101 | VM | Kali Linux — tests offensifs (vmbr1) |
| 103 | VM | Linux Lite (vmbr1) |
| 102 | LXC | Contrôleur TP-Link Omada |
| 105 | LXC | AdGuard Home |

## Réseau côté Proxmox
- `vmbr0` : relié au LAN, pour les services (Omada, AdGuard) et l'interface WAN du pare-feu.
- `vmbr1` : bridge **sans carte physique**, réservé au lab. Kali et la Linux Lite y sont branchées ; leur seule sortie est la VM **OPNsense** (voir le tableau des règles dans le README).
- Historique : une première version utilisait Sophos Firewall ; je l'ai remplacée par OPNsense.
