# AI Usage — FraudScan

## Mesure sur le jeu annoté (`python -m fraudscan.evaluate`)

- Règles évaluées : `refund_without_order`, `repeated_refunds`
- Vrais positifs : 6
- Faux positifs : 4
- Faux négatifs : 3
- Précision = 6 / (6 + 4) = **60 %**
- Rappel = 6 / (6 + 3) = **66,7 %**

### Exemples d'erreurs

Un faux positif est le remboursement T900019 : la commande a été passée en mars, avant le début de l'export. Le remboursement était donc légitime, mais les données disponibles ne permettaient pas de retrouver la commande.

Un faux négatif est T900013 : le paiement hors application par Lydia n'a pas été reconnu par la règle concernée.

## Bilan : quatre questions

### 1. Pourquoi FraudScan est-il un programme déterministe, et Copilot un agent IA ?

FraudScan applique des règles définies dans le code et produit les mêmes résultats pour les mêmes données. Copilot est un agent IA car il comprend les demandes et aide à écrire, analyser et vérifier le code.

### 2. Quelle erreur l'agent a-t-il commise, ou aurait-il pu commettre ?

Copilot aurait pu oublier des cas limites, par exemple les identifiants acheteur vides ou les remboursements légitimes. L'utilisation de tests et de l'Auditor m'a aidé à examiner ces risques.

### 3. Comment avez-vous vérifié le résultat autrement qu'en demandant à l'IA si son code était correct ?

J'ai exécuté les tests du loader, les tests des règles et les tests de référence. J'ai également lancé l'évaluation sur le jeu annoté et examiné les faux positifs et faux négatifs.

### 4. Quelle décision avez-vous volontairement gardée sous contrôle humain ?

J'ai gardé le contrôle sur la validation du code, l'interprétation des règles métier et l'acceptation des modifications proposées par Copilot.