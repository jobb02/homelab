# 09 — Accès d'administration à OPNsense limité au PC d'admin

> Date : 14 novembre 2026 · Pare-feu : OPNsense (`fw-sitea`) · Interface : WAN

## Objectif

Administrer OPNsense depuis le PC d'admin du réseau maison, sans passer par une VM du lab, tout en gardant l'interface web fermée à tous les autres appareils.

**Pourquoi :** l'interface d'administration d'un pare-feu est la cible la plus sensible du réseau. On ne l'ouvre jamais à un réseau entier : seulement à un poste identifié, pour un seul service (principe du moindre privilège).

## Point de départ : une porte fermée

Côté WAN, OPNsense refuse tout par défaut :

- aucune règle Pass : le **deny implicite** bloque tout ;
- l'option **Block private networks** jette ce qui arrive du WAN depuis une adresse privée. Ici, le réseau maison (192.168.1.0/24) est privé : le PC d'admin était donc rejeté lui aussi.

Contrairement au LAN (porte ouverte, où l'on ajoute des exceptions qui ferment), on ajoute ici une **exception qui ouvre**, la plus étroite possible.

## Configuration

### 1. IP fixes

| Machine | IP | Méthode |
| --- | --- | --- |
| PC d'admin | 192.168.1.99 | Bail statique Freebox |
| OPNsense (WAN) | 192.168.1.29 | Bail statique Freebox |

Une règle qui vise une IP n'a de sens que si cette IP ne change pas.

### 2. Alias

| Nom | Type | Contenu | Description |
| --- | --- | --- | --- |
| `PC_ADMIN` | Host(s) | `192.168.1.99` | PC d'administration du pare-feu |

Type **Host(s)** : une seule machine (et non Network(s), une plage).

### 3. Interface WAN

| Option | Valeur | Pourquoi |
| --- | --- | --- |
| Block private networks | décoché | Le réseau maison est privé ; décocher n'ouvre rien seul, le deny implicite reste actif |
| Block bogon networks | coché | Les adresses inexistantes sur Internet restent rejetées |

### 4. Règle (interface WAN)

| Champ | Valeur |
| --- | --- |
| Action | Pass |
| Direction | in |
| Version | IPv4 |
| Protocol | TCP |
| Source | `PC_ADMIN` |
| Destination | WAN address |
| Destination port | HTTPS (443) |
| Log | activé |
| Description | `admin OPNsense depuis PC_ADMIN (HTTPS)` |

**Choix techniques :**

- **TCP + port 443 uniquement** : seule l'interface web est ouverte, pas SSH, DNS ni les autres services du pare-feu. Le champ port n'existe qu'avec TCP ou UDP.
- **WAN address** plutôt qu'une IP tapée : alias automatique qui suit l'adresse du WAN si elle change.
- **Pass sur le WAN, Block par défaut** : tout appareil autre que le PC d'admin ne reçoit aucune réponse.

## Validation

| Test | Attendu | Résultat (Live View) |
| --- | --- | --- |
| PC d'admin (192.168.1.99) → https://192.168.1.29 | Accès | `WAN / in / TCP / pass` — règle « admin OPNsense depuis PC_ADMIN » |
| iPhone (192.168.1.200) → https://192.168.1.29 | Refus silencieux | `WAN / in / TCP / block` — « Default deny » |

L'IP 192.168.1.200 a été rapprochée de l'appareil réel via l'inventaire de la Freebox.

## Points d'attention

- **Certificat auto-signé** : l'avertissement du navigateur est attendu. Piste d'amélioration : certificat émis par une autorité interne.
- **IPv6** : la règle ne couvre que l'IPv4 ; l'IPv6 reste bloqué par le deny implicite.
- **Autres services du pare-feu** (SSH…) : non exposés côté WAN.

## Prochaine étape

- [ ] Passer les règles du lab en liste blanche (moindre privilège) : n'autoriser que DNS, HTTP et HTTPS
