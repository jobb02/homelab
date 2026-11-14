# 08 — Filtrage : isolation du lab derrière OPNsense

> Date : 14 novembre 2026 · Pare-feu : OPNsense (`fw-sitea`) · Hyperviseur : Proxmox VE (`pve-sitea`)

## Objectif

Empêcher les machines du lab (Kali, Linux Lite) d'atteindre le réseau domestique (box, NAS, poste d'administration, DNS, hyperviseur) tout en conservant leur accès à Internet.

**Pourquoi :** un lab cyber héberge des machines offensives ou volontairement vulnérables. Si l'une d'elles est compromise, l'isolation empêche le **mouvement latéral** vers les équipements de la maison.

## Architecture

![Schéma du filtrage : le lab sort sur Internet, le réseau maison est bloqué](schema-filtrage.svg)


- `vmbr1` n'est relié à aucune interface physique : la seule sortie du lab est OPNsense (passerelle par défaut `10.10.10.1`).
- Le lab sort sur Internet via le NAT sortant d'OPNsense, puis le NAT de la Freebox (double NAT).
- Le réseau maison ne peut pas initier de connexion vers le lab : aucune route sur la Freebox vers `10.10.10.0/24`, aucune règle Pass sur le WAN d'OPNsense (deny implicite) et option *Block private networks* active.

## Configuration

### 1. Alias

| Nom | Type | Contenu | Description |
| --- | --- | --- | --- |
| `RES_MAISON` | Network(s) | `192.168.1.0/24` | Réseau maison à protéger |

Choix d'un alias manuel plutôt que l'alias automatique `__wan_network` : l'alias décrit **ce qu'on protège** et ne change pas si l'adressage du WAN évolue.

### 2. Règle de filtrage (interface LAN)

| Champ | Valeur |
| --- | --- |
| Action | Reject |
| Interface | LAN |
| Direction | in |
| Version | IPv4 |
| Protocol | any |
| Source | LAN net |
| Destination | `RES_MAISON` |
| Destination port | any |
| Log | activé |
| Description | `isolation lab → reseau maison` |

**Choix techniques :**

- **Reject plutôt que Block** : en interne, le refus est immédiat (RST en TCP), ce qui accélère le diagnostic. Block reste réservé au WAN.
- **LAN in plutôt que WAN out** : on bloque au plus près de la source. Sur le WAN en sortie, le NAT a déjà remplacé l'adresse source, et une règle « source = LAN net » ne correspondrait plus.
- **Ordre** : la règle est placée **au-dessus** de « Default allow LAN to any » (évaluation *first match*).

### 3. Ordre final des règles LAN

| # | Action | Source | Destination | Rôle |
| --- | --- | --- | --- | --- |
| — | (règles automatiques, anti-lockout) | | | Accès à l'interface d'admin garanti |
| 1 | Reject | LAN net | `RES_MAISON` | Isolation |
| 2 | Pass | LAN net | any (IPv4) | Accès Internet |
| 3 | Pass | LAN net | any (IPv6) | Inutilisé (pas d'IPv6 routé sur le lab) |

## Validation

Tests réalisés depuis Linux Lite (lab) :

| Test | Attendu | Résultat |
| --- | --- | --- |
| `ping 192.168.1.254` (Freebox) | Bloqué | 100 % de perte |
| `curl -m 5 http://192.168.1.254` | Refus immédiat | `Couldn't connect` en < 1 ms (RST) |
| `ping 1.1.1.1` | Autorisé | OK |
| `nslookup google.com` | Autorisé | OK (résolution via OPNsense / Unbound) |
| `ip -6 addr` / `ip -6 route` | Pas d'IPv6 global | Uniquement `fe80::` et `::1`, pas de route par défaut |

Logs : *Firewall → Log Files → Live View*, filtre `label contains isolation` → entrées `LAN / in / block` avec la description de la règle.

## Points d'attention

- **IPv6** : la règle ne couvre que l'IPv4. Si l'IPv6 est un jour activé sur le LAN, dupliquer la règle en IPv6.
- **Table d'états** : une connexion déjà établie peut survivre à une nouvelle règle de blocage. Relancer les tests ou vider les états (*Firewall → Diagnostics → States*).
- **Reject et ICMP** : Reject jette l'ICMP en silence. Le refus immédiat n'est visible qu'en TCP/UDP.
- **Administration** : l'interface web d'OPNsense n'est pas exposée sur le WAN. Elle est administrée depuis le lab (`10.10.10.1`).

## Prochaines étapes

- [ ] Passer en liste blanche (moindre privilège) : n'autoriser que DNS, HTTP et HTTPS depuis le lab
- [ ] Déployer un FortiGate sur le site B (NUC, `pve-siteb`)
- [ ] Tunnel IPsec OPNsense ↔ FortiGate
- [ ] VPN utilisateurs + MFA (FortiClient)
- [ ] Inspection SSL
- [ ] Export des logs du pare-feu vers le Synology (Log Center)
