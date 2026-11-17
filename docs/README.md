# Documentation du homelab

[← Retour à l'accueil du dépôt](../README.md)

Chaque fiche suit le même fil : **ce qu'on veut obtenir, pourquoi, comment, la preuve que ça marche, et ce qui a coincé.** Les temps de lecture sont indicatifs.

## Par où commencer

| Vous avez… | Lisez |
| --- | --- |
| 2 minutes | La [page d'accueil](../README.md) et ses deux schémas |
| 10 minutes | La fiche [13 — Tunnel IPsec](13-tunnel-ipsec.md) : deux constructeurs, une incompatibilité trouvée avant de configurer, et une panne diagnostiquée par couches |
| 10 minutes de plus | La fiche [14 — Règles dans le tunnel](14-regles-tunnel.md) : le trafic de bout en bout, et une faille repérée en lisant les journaux |
| Un profil technique | Le parcours pare-feu ci-dessous, de la fiche 08 à la 14, dans l'ordre |

## Parcours 1 — Le pare-feu, du simple au multi-sites

Ces fiches se lisent dans l'ordre : chacune s'appuie sur la précédente.

| # | Fiche | Ce qu'on y apprend | Lecture |
| --- | --- | --- | --- |
| 08 | [Isolation du lab (OPNsense)](08-filtrage-pare-feu.md) | Alias, règle Reject, ordre des règles (*first match*), preuve dans les logs | 6 min |
| 09 | [Accès d'administration](09-acces-admin.md) | Ouvrir l'interface du pare-feu à une seule IP, en HTTPS, côté WAN | 4 min |
| 10 | [Liste blanche](10-liste-blanche.md) | Moindre privilège : seul ce qui est prévu sort, tout le reste est refusé et journalisé | 8 min |
| 11 | [Site B : FortiGate](11-fortigate-site-b.md) | Un deuxième constructeur : CLI FortiOS, `allowaccess`, licence d'évaluation et ses limites | 6 min |
| 12 | [Site C : Sophos](12-sophos-site-c.md) | Un troisième constructeur : zones, ACL des services, règle de nettoyage | 7 min |
| 13 | [Tunnel IPsec](13-tunnel-ipsec.md) | Relier deux constructeurs : offres communes, configuration en miroir, diagnostic | 6 min |
| 14 | [Règles dans le tunnel](14-regles-tunnel.md) | Moindre privilège des deux côtés, tests dans les deux sens, une faille « any » trouvée dans les journaux | 7 min |

## Parcours 2 — Les fondations du lab

Les briques sur lesquelles tout repose. Elles se lisent dans n'importe quel ordre.

| # | Fiche | Ce qu'on y trouve | Lecture |
| --- | --- | --- | --- |
| 01 | [Virtualisation](01-virtualisation.md) | Les deux hyperviseurs Proxmox VE, VM et conteneurs | 5 min |
| 02 | [Réseau](02-reseau.md) | Switch, ponts, réservations DHCP, IPv6 | 5 min |
| 03 | [DNS](03-dns.md) | Zone locale `home.arpa` et filtrage AdGuard Home | 4 min |
| 04 | [Accès distant](04-acces-distant.md) | VPN WireGuard pour l'administration | 1 min |
| 05 | [Stockage et sauvegarde](05-stockage-sauvegarde.md) | NAS en RAID 1, instantanés, sauvegardes versionnées | 4 min |
| 06 | [Déploiement d'une appli web](06-deploiement-appli-web.md) | Appli Python en conteneur, systemd, durcissement | 2 min |
| 07 | [Microsoft 365 / Entra ID](07-m365-entra-id.md) | Tenant de test pour l'identité cloud | 1 min |

## Annexes

- [Inventaire des adresses IP](inventaire-ip.md) : toutes les adresses fixes, réseau par réseau (3 min).
- [Schéma d'ensemble](schema-homelab.svg) et [schéma des trois sites](schema-sites.svg).
- [Scripts](../scripts/README.md).

Dans chaque fiche, une barre de navigation en haut et en bas permet de passer à la suivante sans revenir en arrière.
