# 02 — Réseau

## Topologie physique
- **Freebox Server** (salon) : routeur, DHCP, point d'entrée Internet.
- **Répéteurs Freebox** en mesh Wi-Fi (salle de bain, chambre).
- Dans la chambre : répéteur → **switch TP-Link Omada ES205G** (`sw-sitea`, 5 ports, tous utilisés) → `pve-sitea` (PC Acer), `nas-sitea`, PC d'administration (via un dock Lenovo) et `pve-siteb` (Intel NUC).

### Contrainte connue
Le lien répéteur ↔ box passe par le Wi-Fi : le débit dans la chambre plafonne autour de 150 Mb/s.
Tirer un câble jusqu'à la box n'est pas faisable ; piste à tester : **CPL**.

## Switch manageable + contrôleur Omada
- Contrôleur Omada installé dans un **conteneur LXC** sur Proxmox (script community-scripts).
- Le switch ES205G est **adopté** par ce contrôleur.

**Pourquoi un contrôleur ?** Il centralise la config et la supervision des équipements réseau, au lieu de configurer chaque appareil à la main.
C'est le même modèle que Meraki ou les contrôleurs Wi-Fi en entreprise.

**Pourquoi en LXC ?** C'est un service Linux léger qui doit tourner en permanence : un conteneur suffit et consomme peu.

## Pare-feu OPNsense (`fw-sitea`)
Le lab offensif est isolé derrière un pare-feu OPNsense virtualisé (règles et état dans le README).

| Interface | Carte | Bridge | Adresse |
|---|---|---|---|
| WAN | `vtnet0` | `vmbr0` (maison) | 192.168.1.29, en DHCP depuis la Freebox, réservée |
| LAN | `vtnet1` | `vmbr1` (lab) | 10.10.10.1/24, fixe, serveur DHCP du lab |

### Piège rencontré : l'ordre des interfaces
Au premier démarrage, OPNsense a placé son **LAN sur la première carte** (`vtnet0`, côté maison) avec l'adresse par défaut `192.168.1.1` et **son serveur DHCP actif**. Deux risques sur le réseau de la maison : conflit d'adresse et serveur DHCP pirate (des appareils auraient pu recevoir OPNsense comme passerelle).
- Réaction : carte côté maison déconnectée dans Proxmox (équivalent d'un câble débranché) avant toute autre action.
- Correction : réassignation en console (WAN = `vtnet0`, LAN = `vtnet1`), identification des cartes par leur adresse MAC, puis adressage du LAN en 10.10.10.1/24, et seulement ensuite reconnexion du WAN.

### Autres points vérifiés
- **Plage DHCP** : l'assistant web a remplacé la plage définie en console par la sienne (`.41–.245`). Elle est ramenée à `.100–.200` pour réserver `.2–.99` aux IP fixes, sans chevauchement possible. Leçon : vérifier ce qu'un assistant a écrasé.
- **WAN** : trafic entrant bloqué par défaut, « Block private networks » et « Block bogon networks » activés. Conséquence voulue : l'interface d'administration n'est joignable que depuis le lab.
- **Certificat de l'interface web** : auto-signé ; empreinte SHA-256 comparée entre la console et le navigateur avant de l'accepter.

## Prochaine étape
Créer des **VLAN** sur le switch pour séparer : lab offensif / services / réseau de la maison.

## Adresses fixes : réservations DHCP
Chaque serveur a une IP fixe **et** une réservation DHCP sur la Freebox (adresse MAC → IP), par exemple `dns-sitea` (AdGuard) en 192.168.1.53 et `omada-sitea` en 192.168.1.24. Le WAN d'OPNsense, lui, prend son adresse en DHCP : sa réservation garantit qu'elle ne change pas.
Pourquoi les deux : l'IP fixe est configurée dans la machine, mais la Freebox ne le sait pas. Sans réservation, elle pourrait attribuer la même adresse à un autre appareil (conflit d'IP, service injoignable par moments).
Les réservations suivent la convention `<rôle>-<site>` (voir le README) : tous les conteneurs et VM Proxmox ont le même préfixe MAC (`BC:24:11`, identifiant constructeur de Proxmox) et apparaîtraient sinon tous sous le même nom de fabricant.

## IPv6 : maîtriser les adresses publiques
**Le constat.** La Freebox annonce un préfixe IPv6 public (Router Advertisements). Même avec « IPv6 : none » dans Proxmox, les conteneurs Debian se fabriquaient une **adresse IPv6 publique** tout seuls (SLAAC).
- En IPv4, le NAT de la box cache les machines derrière une seule adresse publique. En IPv6, **chaque machine a sa propre adresse joignable depuis Internet** : le pare-feu IPv6 de la box devient la seule barrière.
- Ces adresses étaient au format **EUI-64** : la fin de l'adresse contient l'adresse MAC (avec `ff:fe` au milieu), ce qui révèle le matériel (ici, une machine virtuelle Proxmox).

**La correction.** Sur les conteneurs d'administration (Omada, AdGuard), désactivation des annonces de routeur et de l'autoconfiguration :
```
net.ipv6.conf.all.accept_ra = 0
net.ipv6.conf.all.autoconf = 0
```
(appliqué aussi sur `default` et `eth0`, via `/etc/sysctl.d/`). Après redémarrage, il ne reste que l'adresse lien-local `fe80::`, qui ne sort jamais du réseau local.

**Vérification de l'hôte.** L'hôte Proxmox n'avait pas d'IPv6 publique : son réseau est géré par `ifupdown2` avec une configuration IPv4 statique explicite, qui n'accepte pas les annonces de routeur. Son interface d'administration (port 8006) n'est joignable qu'en IPv4, sur le réseau local.

Principe appliqué : la défense en profondeur. On ne compte pas sur une seule barrière (le pare-feu IPv6 de la box) pour protéger des interfaces d'administration.
