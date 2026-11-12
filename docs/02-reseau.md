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
