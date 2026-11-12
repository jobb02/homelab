# Homelab — Mam III Jobb

Infrastructure personnelle auto-hébergée qui me sert de terrain d'entraînement en **réseau**, **virtualisation** et **sécurité**.
Chaque brique est documentée avec **le pourquoi des choix**, pas seulement le comment.

> Ingénieur cybersécurité — sécurité réseau, gestion des vulnérabilités, intégration.
> [LinkedIn](https://www.linkedin.com/in/jobb-mam-iii/) · Contact : voir CV

---

## Vue d'ensemble

```mermaid
flowchart TB
    Internet((Internet)) --- FBX[Freebox Server · 192.168.1.254<br/>routeur · DHCP · serveur VPN WireGuard]
    ADMDIST[Poste d'admin en déplacement] -. tunnel VPN .-> FBX
    FBX -. Wi-Fi mesh .- REP[Répéteur Freebox<br/>chambre]
    REP -- RJ45 --- SW[Switch TP-Link Omada ES205G<br/>192.168.1.101]
    SW -- RJ45 --- PVE[PC Acer · Proxmox VE<br/>192.168.1.100]
    SW -- RJ45 --- NAS[NAS Synology DS218 · 192.168.1.117<br/>RAID 1 · DNS home.arpa]
    SW -- RJ45 --- ADM[PC d'administration<br/>via dock Lenovo]
    SW -- RJ45 --- NUC[Intel NUC · i5-10210U · 16 Go<br/>futur site B · VPN IPsec]

    subgraph PVE_G [Proxmox VE]
        subgraph SRV [vmbr0 · réseau maison 192.168.1.0/24]
            OMADA[LXC 102 · Contrôleur Omada<br/>192.168.1.24]
            ADG[LXC 105 · AdGuard Home<br/>192.168.1.53]
        end
        FW[VM 104 · pare-feu OPNsense<br/>WAN vmbr0 · LAN 10.10.10.1]
        subgraph LAB [vmbr1 · lab isolé 10.10.10.0/24 · sans carte physique]
            KALI[VM 101 · Kali Linux]
            LIN[VM 103 · Linux Lite]
        end
        SRV --- FW --- LAB
    end
    PVE --- PVE_G
```

### Plan d'adressage

| Réseau | Plage | Passerelle | Rôle |
|---|---|---|---|
| Maison (`vmbr0`) | 192.168.1.0/24 | Freebox 192.168.1.254 | Services, administration, appareils de la maison |
| Lab (`vmbr1`) | 10.10.10.0/24 | OPNsense 10.10.10.1 | VM de test, isolées derrière le pare-feu (DHCP par OPNsense) |
| Site B (NUC, prévu) | 10.20.20.0/24 | FortiGate 10.20.20.1 | Second site relié au lab par VPN IPsec |

Pourquoi une plage différente par réseau : si deux réseaux utilisaient 192.168.1.0/24, le pare-feu ne pourrait pas savoir de quel côté envoyer un paquet. Deux plages distinctes = un routage et des règles sans ambiguïté.

### Segmentation du lab

Les VM de test (dont Kali) sont sur un réseau isolé (`vmbr1`), sans carte physique : la seule sortie passe par le pare-feu OPNsense.

| Flux | Règle | Pourquoi |
|---|---|---|
| Lab → Internet | Autorisé, journalisé | Mises à jour et téléchargement d'outils |
| Lab → réseau maison | **Bloqué** | Un scan ou un exploit lancé par erreur ne touche jamais les appareils de la famille |
| Poste d'admin → lab | Autorisé | Administrer les VM depuis mon PC |
| Reste | Refusé par défaut | Moindre privilège : tout ce qui n'est pas explicitement autorisé est interdit |

## Les briques

| Domaine | Ce qui tourne | Doc |
|---|---|---|
| Virtualisation | Proxmox VE, VM + conteneurs LXC | [docs/01-virtualisation.md](docs/01-virtualisation.md) |
| Réseau | Switch Omada + contrôleur en LXC, pare-feu OPNsense, lab isolé | [docs/02-reseau.md](docs/02-reseau.md) |
| DNS | Zone locale `home.arpa` sur Synology + filtrage AdGuard Home | [docs/03-dns.md](docs/03-dns.md) |
| Accès distant | VPN WireGuard (Freebox) | [docs/04-acces-distant.md](docs/04-acces-distant.md) |
| Stockage & sauvegarde | NAS Synology RAID 1, sauvegarde versionnée PC → NAS | [docs/05-stockage-sauvegarde.md](docs/05-stockage-sauvegarde.md) |
| Déploiement applicatif (réalisé, conteneur retiré depuis) | Appli web Python en LXC, systemd, durcissement, Tailscale | [docs/06-deploiement-appli-web.md](docs/06-deploiement-appli-web.md) |
| Identité cloud | Tenant de test Microsoft 365 / Entra ID | [docs/07-m365-entra-id.md](docs/07-m365-entra-id.md) |

## Feuille de route

Priorité : tout ce qui tourne autour du pare-feu et de l'intégration sécurité réseau.

- [ ] Intel NUC en « site B » : Proxmox, réseau interne 10.20.20.0/24, FortiGate en VM (licence d'évaluation) — préparation Fortinet NSE4
- [ ] VPN IPsec site à site entre OPNsense (site A, 10.10.10.0/24) et FortiGate (site B, 10.20.20.0/24) : interopérabilité entre deux constructeurs, comme chez un client siège + agence
- [ ] IDS/IPS Suricata sur OPNsense, testé avec des scans et attaques depuis Kali
- [ ] Envoi des logs du pare-feu (syslog) vers le NAS Synology (Log Center) pour les conserver hors du pare-feu
- [ ] Scan de vulnérabilités du lab avec Nessus Essentials
- [ ] Segmentation par VLAN (lab / services / maison) via le switch Omada
- [ ] AdGuard Home comme DNS pour tout le réseau
- [ ] Copie de sauvegarde hors site (règle 3-2-1)
- [ ] Accès conditionnel Entra ID (préparation SC-300)

## Règles de publication

Ce dépôt est public : **aucun secret** (mots de passe, clés, tokens), **aucune IP publique**, **aucun identifiant de compte** ni nom de tailnet.
Les adresses en `192.168.x.x` sont des adresses privées, non joignables depuis Internet.
