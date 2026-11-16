# 10 — Liste blanche sur le lab (moindre privilège)

> Date : 16 novembre 2026 · Pare-feu : OPNsense (`fw-sitea`) · Interface : LAN

## Objectif

Passer la porte du lab de « tout est autorisé sauf la maison » (liste noire) à « seul ce qui est prévu peut sortir » (liste blanche). Chaque flux autorisé a une raison d'exister.

**Pourquoi :** avec une liste noire, une VM compromise peut sortir vers Internet sur n'importe quel port (exfiltration, communication avec un serveur de commande). Avec une liste blanche, elle ne peut utiliser que les services explicitement autorisés.

## Prérequis : des IP fixes pour les règles ciblées

Le DHCP du lab est assuré par **Dnsmasq** (Kea est installé mais inactif). La plage dynamique réelle était celle par défaut (`.41–.245`) ; elle a été alignée sur le plan d'adressage.

| Élément | Valeur |
| --- | --- |
| Plage DHCP | `10.10.10.100` – `10.10.10.200` |
| IP fixes | `10.10.10.2` – `10.10.10.99` |
| Kali | `10.10.10.10` (réservation Dnsmasq par adresse MAC) |
| Linux Lite | `10.10.10.11` (réservation Dnsmasq par adresse MAC) |

Les VM affichent toujours `dynamic` dans `ip a` : l'adresse est obtenue par DHCP, mais le serveur donne toujours la même. La réservation se vérifie côté serveur (bail de type *static*).

## Alias

| Nom | Type | Contenu |
| --- | --- | --- |
| `KALI` | Host(s) | `10.10.10.10` |
| `LINUX_LITE` | Host(s) | `10.10.10.11` |
| `FREEBOX` | Host(s) | `192.168.1.254` |
| `SYNOLOGY` | Host(s) | `192.168.1.117` |
| `RES_MAISON` | Network(s) | `192.168.1.0/24` |
| `PORTS_WEB` | Port(s) | `80`, `443` |

## Règles LAN (lues de haut en bas)

| # | Action | Protocole | Source | Destination | Port | Rôle |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Pass | ICMP (echo request) | KALI | FREEBOX | — | Exception de test |
| 2 | Pass | TCP | LINUX_LITE | SYNOLOGY | 5001 | Administration du NAS (DSM) |
| 3 | Pass | TCP/UDP | LAN net | LAN address | 53 | DNS uniquement via OPNsense |
| 4 | Reject | TCP/UDP | LAN net | any | 53 | Refus des DNS externes |
| 5 | Reject | any | LAN net | RES_MAISON | — | Isolation du réseau maison |
| 6 | Pass | TCP | LAN net | any | PORTS_WEB | Web vers Internet |
| 7 | Pass | UDP | LAN net | any | 123 | Heure (NTP) |
| 8 | Pass | ICMP (echo request) | LAN net | any | — | Ping de diagnostic |
| 9 | Reject + log | any | LAN net | any | — | Nettoyage : tout le reste est refusé |

Les règles « Default allow LAN to any » (IPv4 et IPv6) sont **désactivées**, pas supprimées.

**Logique d'ordre :** exceptions précises → interdictions qui protègent → ouvertures générales → nettoyage.

**Choix techniques :**

- **Règle 5 au-dessus de la règle 6** : « any » inclut la maison (Freebox, NAS). Sans le Reject placé avant, l'ouverture du web rouvrirait le web vers le réseau domestique.
- **Règle de nettoyage explicite** : le deny implicite bloquerait déjà, mais sans log. Le nettoyage rend chaque refus visible dans la Live View.
- **Interface = LAN** sur toutes les règles : une règle avec interface « any » devient flottante et serait évaluée avant les règles d'interface.
- **Reject** en interne : refus immédiat, diagnostic plus rapide.

## Validation

| Depuis | Test | Résultat |
| --- | --- | --- |
| Kali | `nslookup google.com` | OK (via 10.10.10.1) |
| Kali | `nslookup google.com 8.8.8.8` | Refusé (connection refused) |
| Kali | `curl -I https://www.google.com` | HTTP/2 200 |
| Kali | `ping 8.8.8.8` | OK |
| Kali | `ping 192.168.1.254` | OK (exception) |
| Kali | `curl https://192.168.1.254` | Refusé (isolation) |
| Kali | `curl https://portquiz.net:8000` | Refusé (nettoyage, vérifié dans la Live View) |
| Kali | `timedatectl` | Horloge synchronisée |
| Linux Lite | Interface DSM (5001) | OK |
| Linux Lite | `ping 192.168.1.254` | Refusé |

## Limites connues

- **DNS over HTTPS** (DoH) passe par le port 443 et contourne la règle DNS. Le bloquer demande des listes de serveurs DoH ou un NGFW qui identifie l'application.
- **Nouveaux besoins** (un outil de Kali sur un autre port) : à ajouter comme exception, après lecture des refus de la règle de nettoyage.
