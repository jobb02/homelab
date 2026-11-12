# 01 — Virtualisation (Proxmox VE)

## Matériel
| Hôte | Rôle | Matériel | IP |
|---|---|---|---|
| `pve-sitea` (nom de nœud interne : `proxmox`) | Site A : services + lab derrière OPNsense | PC Acer, Intel Core i5-6400T (4 cœurs), 16 Go de RAM, UEFI avec Secure Boot | 192.168.1.100 |
| `pve-siteb` | Site B : futur FortiGate + lab 10.20.20.0/24 | Intel NUC, i5-10210U (4 cœurs / 8 threads), 16 Go de RAM, SSD 256 Go | 192.168.1.102 |

- Les deux hôtes sont branchés en Ethernet sur le switch Omada.
- **Deux Proxmox indépendants, sans cluster** : avec seulement 2 nœuds, le quorum serait perdu dès qu'un des deux est éteint, et chaque site doit pouvoir fonctionner seul — c'est ce qu'on simule avec un VPN site à site.
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

## Inventaire (site A)
| ID | Type | Nom | Rôle |
|---|---|---|---|
| 104 | VM | `fw-sitea` | OPNsense — pare-feu du lab |
| 101 | VM | — | Kali Linux — tests offensifs (vmbr1) |
| 103 | VM | — | Linux Lite (vmbr1) |
| 102 | LXC | `omada-sitea` | Contrôleur TP-Link Omada |
| 105 | LXC | `dns-sitea` | AdGuard Home |

## VM 104 — OPNsense : choix de configuration
| Réglage | Valeur | Pourquoi |
|---|---|---|
| Type d'OS | Other | OPNsense repose sur FreeBSD, pas sur Linux |
| CPU | 2 cœurs, type `host` | Suffisant pour router un lab ; `host` expose toutes les instructions du processeur réel. Contrepartie : la VM ne pourrait pas migrer vers un hôte au processeur différent (le type par défaut `x86-64-v2-AES` sert justement à cette portabilité) |
| RAM | 4 Go, ballooning désactivé | Marge pour un futur IDS (Suricata) ; un pare-feu ne doit pas se faire reprendre de la mémoire en fonctionnement |
| Disque | 20 Go, VirtIO SCSI, discard + IO thread | Stockage LVM-Thin : le discard rend l'espace libéré par les logs au stockage de l'hôte |
| Cartes réseau | 2 × VirtIO, pare-feu Proxmox désactivé | Paravirtualisées (plus performantes que des cartes émulées) ; pas de second filtrage devant un pare-feu |
| Système de fichiers | UFS | Plus léger que ZFS sur un disque virtuel unique déjà sauvegardé par Proxmox |
| Démarrage auto | Oui | Le lab doit retrouver sa passerelle après un redémarrage de l'hôte |

Instantané Proxmox pris **avant** une mise à jour d'OPNsense : en cas de régression, retour arrière en quelques secondes.

## Réseau côté Proxmox
- `vmbr0` : relié au LAN, pour les services (Omada, AdGuard) et l'interface WAN du pare-feu.
- `vmbr1` : bridge **sans carte physique**, réservé au lab. Kali et la Linux Lite y sont branchées ; leur seule sortie est la VM **OPNsense** (voir le tableau des règles dans le README).
- Historique : une première version utilisait Sophos Firewall ; je l'ai remplacée par OPNsense.

## Mises à jour
- Sans abonnement, le dépôt `pve-enterprise` (réservé aux abonnés) faisait échouer `apt update` : le serveur ne recevait plus de correctifs de sécurité.
- Correction : dépôts enterprise (Proxmox et Ceph) désactivés, dépôt **`pve-no-subscription`** activé, puis mise à niveau complète et redémarrage sur le nouveau noyau.
- Pourquoi `no-subscription` : les paquets y arrivent avant le dépôt enterprise, donc un peu moins éprouvés, mais c'est le choix standard sans abonnement. Ne pas mettre à jour du tout serait bien plus risqué.
- Bonnes pratiques : sauvegarde des VM importantes avant une grosse mise à jour ; les anciens noyaux restent disponibles au démarrage en cas de régression.
- Même configuration appliquée à `pve-siteb` dès l'installation.

### Incident : mise à jour bloquée sans message
Sur les deux hôtes, une mise à jour lancée depuis l'interface est restée figée. `ps -ef` montrait la chaîne `apt-get dist-upgrade` → `apt-listchanges` → `pager` : apt attendait qu'on lise et ferme les notes de version, dans une fenêtre qui n'était plus affichée. Les autres commandes apt restaient bloquées sur le verrou `/var/lib/dpkg/lock-frontend`.
- Diagnostic clé : **aucun processus `dpkg`** dans la liste, donc aucun paquet en cours d'installation (apt-listchanges s'exécute après le téléchargement, avant le dépaquetage). Arrêter la chaîne était sans risque. Si `dpkg` avait été présent, il aurait fallu le laisser finir.
- Correction : arrêt des processus, `dpkg --configure -a` par précaution, puis mise à jour relancée sans pager :
  `apt update && APT_LISTCHANGES_FRONTEND=none apt full-upgrade -y`
