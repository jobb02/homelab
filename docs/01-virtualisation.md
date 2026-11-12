# 01 — Virtualisation (Proxmox VE)

## Matériel
- Hôte : PC Acer dédié, nom de nœud `proxmox`, branché en Ethernet via le switch Omada.
- Intel Core i5-6400T (4 cœurs), 16 Go de RAM, démarrage UEFI avec Secure Boot.
- Second hôte prévu : Intel NUC (i5-10210U, 4 cœurs / 8 threads, 16 Go de RAM, SSD 256 Go), futur « site B » sous Proxmox pour un VPN IPsec site à site avec le lab principal. Il sera géré en Proxmox indépendant, sans cluster : avec seulement 2 nœuds, le quorum serait perdu dès qu'un des deux est éteint.
- Dimensionnement : les services légers tournent en LXC pour économiser la RAM ; les VM ne sont allumées que lorsqu'elles servent (Kali).
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

## Mises à jour
- Sans abonnement, le dépôt `pve-enterprise` (réservé aux abonnés) faisait échouer `apt update` : le serveur ne recevait plus de correctifs de sécurité.
- Correction : dépôts enterprise (Proxmox et Ceph) désactivés, dépôt **`pve-no-subscription`** activé, puis mise à niveau complète et redémarrage sur le nouveau noyau.
- Pourquoi `no-subscription` : les paquets y arrivent avant le dépôt enterprise, donc un peu moins éprouvés, mais c'est le choix standard sans abonnement. Ne pas mettre à jour du tout serait bien plus risqué.
- Bonnes pratiques : sauvegarde des VM importantes avant une grosse mise à jour ; les anciens noyaux restent disponibles au démarrage en cas de régression.
