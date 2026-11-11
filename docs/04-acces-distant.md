# 04 — Accès distant

## VPN WireGuard (Freebox)
- Usage : administrer **tout le lab** depuis l'extérieur, comme si j'étais à la maison.
- Pourquoi WireGuard : protocole moderne, rapide, configuration simple (une paire de clés par appareil), et déjà intégré à la Freebox.
- Aucun port d'administration (Proxmox, SSH, NAS) n'est exposé directement sur Internet : tout passe par le tunnel.

## Tailscale (utilisé pour un déploiement, retiré depuis)
- Usage : donner accès à **une seule application** à des utilisateurs, sans leur ouvrir tout le réseau (voir [06](06-deploiement-appli-web.md)).
- Le conteneur rejoint un réseau privé Tailscale ; `tailscale serve` publie l'appli **en HTTPS** (certificat automatique), visible uniquement des membres du réseau.
- Particularité : dans un LXC non privilégié, il n'y a pas d'accès à `/dev/net/tun` → Tailscale tourne en mode **userspace-networking**.

## Pourquoi ne pas tout exposer avec une redirection de port ?
Une redirection de port rend le service visible par n'importe qui sur Internet (scans automatiques, attaques par force brute).
Avec un VPN, il faut d'abord être authentifié sur le tunnel avant même de voir le service.
