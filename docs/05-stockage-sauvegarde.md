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
| Test S.M.A.R.T. rapide | Hebdomadaire, la nuit | Vérifie l'électronique et un échantillon de surface de chaque disque |
| Test S.M.A.R.T. étendu | Mensuel, la nuit | Scanne toute la surface à la recherche de secteurs défectueux |
| Nettoyage des données (scrubbing) | Périodique, un autre jour que le SMART | Compare les 2 copies du RAID pour détecter la corruption silencieuse |
| Vidage de la corbeille | Hebdomadaire, fichiers de plus de 30 jours | Assez long pour récupérer une suppression par erreur, sans saturer le disque |

Les tests lourds sont planifiés la nuit et à des jours différents pour ne pas ralentir le NAS ni cumuler la charge sur les disques.

## Sauvegarde des postes : test de restauration
Une sauvegarde jamais testée n'est pas une sauvegarde : restauration d'un fichier supprimé vérifiée depuis Synology Drive.

## Accès distant au NAS
- Via QuickConnect (relais Synology), sans redirection de port.

## Prochaine étape
- [ ] Une copie **hors site** pour respecter la règle 3-2-1 (3 copies, 2 supports, 1 hors site).
