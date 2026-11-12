# Scripts

Scripts d'automatisation du lab (Bash, PowerShell, Python).
Chaque script commence par un commentaire qui explique ce qu'il fait et pourquoi.

> Avant de pousser un script : vérifier qu'il ne contient ni mot de passe, ni clé, ni IP publique.

| Script | Rôle |
|---|---|
| `gen_schema.py` | Génère le schéma réseau `docs/schema-homelab.svg` en thème sombre (Python standard, sans dépendance). Le schéma est décrit en code : une modification du lab = quelques lignes à changer, puis `python3 scripts/gen_schema.py docs/schema-homelab.svg`. |
