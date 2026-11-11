# 07 — Tenant de test Microsoft 365 / Entra ID

Objectif : pratiquer l'administration des identités Microsoft, en préparation de la certification **SC-300**.

## Fait
- Tenant **Microsoft 365 Business Premium** d'essai (inclut Entra ID P1).
- Création d'utilisateurs et de groupes.
- **MFA** via les paramètres de sécurité par défaut (Security Defaults), avec Microsoft Authenticator.

## Ce que j'ai retenu
- **Security Defaults** : protection « clé en main », tout-ou-rien (MFA pour tous, blocage de l'authentification legacy). Idéal pour une petite structure.
- **Accès conditionnel** : règles fines « SI condition ALORS exigence » (ex. MFA obligatoire pour les admins, blocage par pays). Nécessite Entra ID P1.
- Les deux sont **mutuellement exclusifs** : il faut désactiver les Security Defaults pour créer des stratégies d'accès conditionnel.

## Prochaines étapes
- [ ] Premières stratégies d'accès conditionnel (MFA admins, blocage auth legacy) en mode « rapport uniquement » puis activé
- [ ] PIM (élévation de privilèges à la demande)
- [ ] Inscription d'une application d'entreprise avec SSO
