# 02 — Réseau

## Topologie physique
- **Freebox Server** (salon) : routeur, DHCP, point d'entrée Internet.
- **Répéteurs Freebox** en mesh Wi-Fi (salle de bain, chambre).
- Dans la chambre : répéteur → **switch TP-Link Omada ES205G** (5 ports, tous utilisés) → PC Acer (Proxmox), NAS Synology, PC d'administration (via un dock Lenovo) et Intel NUC (futur site B).

### Contrainte connue
Le lien répéteur ↔ box passe par le Wi-Fi : le débit dans la chambre plafonne autour de 150 Mb/s.
Tirer un câble jusqu'à la box n'est pas faisable ; piste à tester : **CPL**.

## Switch manageable + contrôleur Omada
- Contrôleur Omada installé dans un **conteneur LXC** sur Proxmox (script community-scripts).
- Le switch ES205G est **adopté** par ce contrôleur.

**Pourquoi un contrôleur ?** Il centralise la config et la supervision des équipements réseau, au lieu de configurer chaque appareil à la main.
C'est le même modèle que Meraki ou les contrôleurs Wi-Fi en entreprise.

**Pourquoi en LXC ?** C'est un service Linux léger qui doit tourner en permanence : un conteneur suffit et consomme peu.

## Segmentation du lab
Le lab offensif est isolé derrière un pare-feu OPNsense virtualisé (détail dans le README).

## Prochaine étape
Créer des **VLAN** sur le switch pour séparer : lab offensif / services / réseau de la maison.

## Adresses fixes : réservations DHCP
Chaque serveur a une IP fixe **et** une réservation DHCP sur la Freebox (adresse MAC → IP), par exemple AdGuard en 192.168.1.53 et Omada en 192.168.1.24.
Pourquoi les deux : l'IP fixe est configurée dans la machine, mais la Freebox ne le sait pas. Sans réservation, elle pourrait attribuer la même adresse à un autre appareil (conflit d'IP, service injoignable par moments).
Les réservations sont nommées (`adguard`, `omada`…) : tous les conteneurs Proxmox ont le même préfixe MAC (`BC:24:11`) et apparaîtraient sinon tous sous le même nom de fabricant.

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
