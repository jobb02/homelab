# 06 — Déploiement d'une application web multi-utilisateurs

Application interne en Python (comptes, rôles, sessions, base SQLite) que j'ai déployée et exploitée sur le lab.

> Statut : réalisé. Le conteneur a été retiré depuis ; cette fiche documente le déploiement.

## Architecture
- Conteneur **LXC Ubuntu 24.04**, IP fixe sur le LAN.
- Application installée dans `/opt/`, environnement virtuel Python dédié.
- Lancée par un **service systemd** : démarrage automatique, redémarrage en cas de crash, logs dans `journalctl`.
- Exposée en HTTPS uniquement via **Tailscale** (voir [04-acces-distant.md](04-acces-distant.md)).

## Durcissement
| Mesure | Pourquoi |
|---|---|
| L'appli écoute sur `127.0.0.1` seulement | Impossible de la joindre en direct depuis le LAN : seul le proxy Tailscale local peut lui parler |
| Listing des répertoires désactivé | Empêche de parcourir l'arborescence du serveur |
| Blocage (403) des fichiers sensibles (`.py`, `.db`, `.json`, dossiers `data/`, `venv/`…) | Empêche de télécharger le code ou la base de données |
| Mots de passe hachés (PBKDF2), cookie de session `HttpOnly` + `SameSite=Lax` | Pas de mot de passe en clair ; cookie inaccessible au JavaScript et protégé contre une partie des attaques CSRF |
| Emplacement de la base passé par variable d'environnement | La config reste hors du code |

## Mises à jour
Script de déploiement : copie du code par `scp` vers le conteneur (jamais le dossier de données), puis redémarrage du service.

## Ce que j'aurais ajouté ensuite
- ACL Tailscale restrictives (les utilisateurs ne voient que le port HTTPS de l'appli).
- Sauvegarde automatique de la base SQLite vers le NAS.
