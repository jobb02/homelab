# Scripts

Scripts d'automatisation du lab (Bash, PowerShell, Python).
Chaque script commence par un commentaire qui explique ce qu'il fait et pourquoi.

> Avant de pousser un script : vérifier qu'il ne contient ni mot de passe, ni clé, ni IP publique.

| Script | Rôle |
|---|---|
| `gen_schema.py` | **Ancienne version**, conservée pour l'historique : elle générait le premier schéma du lab (site A seul, site B prévu). Le schéma actuel, `docs/schema-homelab.svg` (trois sites et tunnel IPsec), est dessiné directement en SVG. Ne pas lancer ce script vers `docs/schema-homelab.svg` : il écraserait le schéma à jour. |
