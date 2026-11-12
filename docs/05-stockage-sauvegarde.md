# 05 — Stockage et sauvegarde

## NAS Synology DS218
- 2 disques de 4 To en **RAID 1** (miroir).
- Pourquoi RAID 1 : avec 2 baies, c'est le seul mode qui tolère la panne d'un disque.

> ⚠️ **RAID n'est pas une sauvegarde.** Le miroir protège d'une panne de disque, pas d'une suppression, d'un ransomware ou d'un incendie : une erreur est répliquée instantanément sur les deux disques.

## Sauvegarde des postes
- Sauvegarde **à sens unique PC → NAS, avec versions** (Synology Drive, tâche de sauvegarde).
- Pourquoi pas une synchronisation : une synchro réplique aussi les suppressions et les fichiers chiffrés par un ransomware. Le versionnage permet de revenir à un état antérieur.

## Photos
- Migration de la photothèque iCloud puis Google Photos vers Synology Photos (plusieurs dizaines de milliers d'éléments).

## Maintenance planifiée
| Tâche | Fréquence | Pourquoi |
|---|---|---|
| Instantanés Btrfs (tous les dossiers partagés) | Tous les jours à 5h | Point de restauration quotidien contre les suppressions et les ransomwares (voir ci-dessous) |
| Test S.M.A.R.T. rapide (+ santé IronWolf) | Le mercredi à 10h | Environ 2 minutes : vérifie l'électronique et un échantillon de surface de chaque disque |
| Test S.M.A.R.T. étendu | Le 15 du mois à 1h | Plusieurs heures : scanne toute la surface à la recherche de secteurs défectueux |
| Nettoyage des données (scrubbing) | Le 1er du mois à 1h | Compare les 2 copies du RAID pour détecter la corruption silencieuse |
| Vidage de la corbeille | Hebdomadaire, fichiers de plus de 30 jours | Assez long pour récupérer une suppression par erreur, sans saturer le disque |

Les tests lourds sont planifiés la nuit et à des jours différents pour ne pas ralentir le NAS ni cumuler la charge sur les disques. Les instantanés ont été déplacés de 2h à 5h : la nuit, les disques sont en veille, et la tâche les réveille (bruit) à une heure où le NAS n'est plus utilisé.

## Instantanés (Snapshot Replication)
- Un instantané Btrfs par jour sur chaque dossier partagé (`homes`, `photo`, `general`, `video`).
- Conservation « Smart Retention » : 30 quotidiens, 8 hebdomadaires, 3 mensuels, et toujours au moins les 5 derniers.
- Pourquoi : un instantané ne copie rien au moment où il est pris, il fige les blocs existants (copy-on-write). Il ne consomme de l'espace que pour ce qui est modifié ou supprimé ensuite. On peut donc revenir à l'état d'un dossier d'un jour donné, même après un chiffrement par ransomware.
- Limite assumée : les instantanés sont sur le même NAS que les données. Ils ne protègent pas d'une panne du NAS, d'un vol ou d'un incendie, d'où la copie hors site prévue (règle 3-2-1).

## Durcissement du NAS
| Mesure | Pourquoi |
|---|---|
| Comptes `admin` et `guest` désactivés | `admin` est le premier nom tenté par les attaques par force brute ; `guest` donne un accès sans mot de passe |
| Double authentification (2FA) sur le compte administrateur | Un mot de passe volé ne suffit plus |
| Blocage automatique des IP après plusieurs échecs de connexion | Freine les attaques par force brute |
| QuickConnect limité aux applications mobiles, avec un identifiant non devinable | Réduit la surface exposée sur Internet |
| Alertes e-mail et rapport de santé | Être prévenu dès qu'un disque se dégrade, tant que le miroir tient encore |

## Sauvegarde des postes : test de restauration
Une sauvegarde jamais testée n'est pas une sauvegarde : restauration d'un fichier supprimé vérifiée depuis Synology Drive.

## Accès distant au NAS
- Via QuickConnect (relais Synology), sans redirection de port.

## Prochaine étape
- [ ] Une copie **hors site** pour respecter la règle 3-2-1 (3 copies, 2 supports, 1 hors site).
