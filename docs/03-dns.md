# 03 — DNS local et filtrage

## Objectif
- Joindre mes services par un **nom** (`nas.home.arpa`, `proxmox.home.arpa`…) plutôt que par leur IP.
- **Filtrer** publicités, traqueurs et domaines malveillants.

## Architecture
1. **AdGuard Home** (LXC sur Proxmox) : reçoit les requêtes DNS des clients configurés, filtre, puis transmet.
2. **DNS Server Synology** (sur le NAS) : fait autorité sur la zone locale `home.arpa`.
3. Les requêtes pour `*.home.arpa` sont renvoyées par AdGuard vers le Synology ; le reste part vers les résolveurs publics.

## Zone `home.arpa` (Synology)

| Nom | Type | Cible |
|---|---|---|
| `proxmox.home.arpa` | A | 192.168.1.100 |
| `switch.home.arpa` | A | 192.168.1.101 |
| `nas.home.arpa` | A | 192.168.1.117 |
| `ns.home.arpa` | A | 192.168.1.117 |
| `omada.home.arpa` | A | 192.168.1.24 |
| `adguard.home.arpa` | A | 192.168.1.53 |
| `synology.home.arpa` | CNAME | `nas.home.arpa` |
| `home.arpa` | NS | `ns.home.arpa` |

**Zone inverse** `1.168.192.in-addr.arpa` : un enregistrement **PTR** par machine (ex. `100` → `proxmox.home.arpa`).
Pourquoi : permet de retrouver le nom à partir de l'IP (`nslookup 192.168.1.100`), ce qui rend les journaux (AdGuard, pare-feu) lisibles avec des noms plutôt que des adresses.

**TTL** : 3600 s (1 h) sur les enregistrements A, au lieu des 86 400 s (24 h) par défaut. Pourquoi : dans un lab, les IP changent souvent ; une heure de cache limite le temps pendant lequel un client garde une ancienne adresse. Le NS et `ns.home.arpa` restent à 86 400 s car ils ne bougent pas.

**CNAME** `synology` → `nas` : un alias. Si l'IP du NAS change, une seule ligne A est à modifier.

## AdGuard Home

- **Résolveurs amont en DNS over HTTPS** : Cloudflare et Quad9. Pourquoi : les requêtes qui sortent vers Internet sont chiffrées, la box et le FAI ne voient plus les domaines demandés.
- **Redirection conditionnelle** : les requêtes `*.home.arpa` partent vers le Synology (`192.168.1.117:53`), le reste vers les résolveurs DoH.
- **Listes de blocage** : AdGuard DNS filter (publicité, traqueurs), Phishing URL Blocklist (PhishTank), Dandelion Sprout's Anti-Malware.
- **Clients** : pour l'instant, mon poste est configuré manuellement pour utiliser AdGuard. Étape suivante : distribuer AdGuard comme DNS à tout le réseau.

### Observation intéressante
Une grosse part des requêtes concerne `wpad.home` : c'est Windows qui cherche automatiquement un fichier de configuration de proxy (WPAD). Sur un réseau hostile, un attaquant qui répond à ce nom peut se placer en proxy et intercepter le trafic. Bonne pratique : désactiver la détection automatique du proxy sur les postes qui n'en ont pas besoin.

## Pourquoi `home.arpa`
C'est le domaine **réservé** aux réseaux domestiques (RFC 8375).
Utiliser un faux domaine du type `.local` ou `.lan` peut entrer en conflit avec mDNS ou avec un vrai TLD.

## Pourquoi séparer filtrage et zone locale
Chaque outil fait ce qu'il fait le mieux : AdGuard pour le filtrage et les statistiques, le Synology pour la gestion de zone.
