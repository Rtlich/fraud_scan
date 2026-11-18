# FraudScan · Piloter un agent IA pour développer un détecteur de fraudes

Atelier en binôme · 90 minutes · énoncé détaillé : [`docs/enonce_atelier.pdf`](docs/enonce_atelier.pdf)

## La mission

Vous êtes data analyst chez **Loopa**, plateforme fictive de revente de seconde main entre particulier·ères.
L'équipe Confiance & Sécurité soupçonne des fraudes : faux remboursements, contrefaçons, annonces copiées, paiements hors plateforme, faux comptes.

- **Copilot** est l'agent IA qui vous aide à concevoir, écrire et vérifier le code.
- **FraudScan** est le programme Python que vous développez. Une fois écrit, il applique les règles métier **sans IA** : rapidement, de façon reproductible et auditable.

Vous disposez de 6 mois de transactions (50 601 lignes), des annonces, des comptes et d'un document de 7 règles métier.

> Toutes les données sont générées : aucune personne, aucun compte, aucune marque ni plateforme réels.

## Ce que vous rendez

- [ ] Le loader complété : `tests/test_reference.py` réussit, **sans avoir été modifié**
- [ ] Les **règles 1 et 2** dans `fraudscan/rules.py`, avec vos tests dans `tests/test_rules.py`
- [ ] `AGENTS.md` à la racine, avec les quatre rubriques (objectif, conventions, commandes, limites)
- [ ] `.github/agents/auditor.agent.md`, un agent relecteur en lecture seule
- [ ] `AI_USAGE.md` : votre journal, votre mesure et les quatre questions du bilan
- [ ] Un commit par règle, avec un message clair
- [ ] Le repository poussé sur GitHub, en **privé** (Source Control › Publish Branch)

Optionnel : les règles 3 à 7, et le rapport (`fraudscan/report.py`, lancé par `python -m fraudscan`).

## Le parcours · 90 minutes

| Bloc | Durée | Ce que vous faites |
|---|---|---|
| 1 · Préparer et analyser | 15 min | Créer le repository, puis, en mode **Ask**, faire expliquer les fichiers et repérer les problèmes de qualité et les `TODO` du loader |
| 2 · Cadrer l'agent | 15 min | Écrire `AGENTS.md` vous-mêmes, puis créer l'agent Auditeur |
| 3 · Développer avec l'agent | 40 min | En mode **Agent** : compléter le loader (`/plan`), puis les règles 1 et 2 avec leurs tests |
| 4 · Tester de façon critique | 15 min | Le cas piégé, la mesure sur `data/labeled/`, les cas limites |
| 5 · Faire le bilan | 5 min | Répondre aux quatre questions dans `AI_USAGE.md` |

### Bloc 1 · Préparer et analyser

```bash
cd fraudscan
git init
git add .
git commit -m "Initial import"

python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
pytest tests/test_loader.py      # « 1 passed »
```

Les tests de référence échouent encore à ce stade : c'est normal. Si `git commit` échoue, renseignez d'abord votre identité :
`git config --global user.name "Prénom Nom"` puis `user.email`.

Repérez et notez : les formats de date et de montant, les écritures différentes d'un même identifiant, les liens entre les fichiers,
et les `TODO` du loader fourni. Ces notes forment votre liste de travail pour le bloc 3.

### Bloc 2 · Cadrer l'agent

`AGENTS.md` contient des **instructions persistantes**, que Copilot relit à chaque demande. Ce n'est pas une mémoire : c'est vous qui l'écrivez.
Une dizaine de lignes suffit : chaque ligne consomme des tokens à chaque demande.

L'agent Auditeur (`.github/agents/auditor.agent.md`) n'a que les outils `read` et `search` : il relit, il ne modifie rien.
Un agent qui code, un agent qui relit : la séparation des rôles.

### Bloc 3 · Développer avec l'agent

1. `/plan` : faire découper le travail sur le loader, puis valider le plan.
2. Agent : la règle 1, puis la règle 2, **une par demande**, avec vos tests (un cas signalé, un cas non signalé).
3. `pytest` : les tests de référence réussissent, sans jamais être modifiés.
4. L'Auditeur relit ; la décision vous revient. Commit, note dans `AI_USAGE.md`, puis `/compact` avant la règle suivante.

Un test réussi prouve que le code respecte le comportement **testé**, pas que ce comportement est la **bonne lecture** du besoin.
Un agent qui écrit le code et ses tests peut y reproduire la même erreur : d'où les tests de référence, écrits par l'équipe Confiance & Sécurité.

### Bloc 4 · Tester de façon critique

1. **Le cas piégé** (5 min) : en mode Ask, demandez si l'annonce `L000003` de `data/sample/listings.csv` est suspecte selon `#business_rules.md`.
   Comparez la réponse avec la règle 4 écrite, calcul à l'appui, et lisez la description de l'annonce.
2. **La mesure** (7 min) : `python -m fraudscan.evaluate` compare vos alertes aux conclusions des enquêtes de `data/labeled/`.
   Calculez la précision, VP / (VP + FP), et le rappel, VP / (VP + FN), puis expliquez un faux positif ou un faux négatif.
3. **Les limites** (3 min) : exactement 300 €, exactement 20 % du prix de référence, un alias seul : vos règles les laissent-elles non signalés ?

Une anomalie signalée par une règle n'est pas une fraude confirmée : seule l'enquête le dit.

### Bloc 5 · Faire le bilan

Dans `AI_USAGE.md`, en deux ou trois phrases par question :

1. Pourquoi FraudScan est-il un programme déterministe, et Copilot un agent IA ?
2. Quelle erreur l'agent a-t-il commise, ou aurait-il pu commettre ?
3. Comment avez-vous vérifié le résultat sans vous fier à l'IA ?
4. Quelle décision avez-vous gardée sous contrôle humain ?

## Les données

| Fichier | Contenu |
|---|---|
| `data/transactions.csv` | Commandes et remboursements, d'avril à septembre 2026. Un remboursement renvoie à sa commande par `order_id` |
| `data/listings.csv` | Les annonces : titre, catégorie, prix affiché, photo (`photo_hash`), **description en texte libre** |
| `data/users.csv` | Les comptes : date d'inscription, pays, adresse e-mail |
| `data/categories.csv` | Le prix de référence de chaque catégorie, et les catégories de luxe |
| `data/sample/` | Un échantillon de 21 transactions, avec un exemple de chaque problème : pour vos tests |
| `data/labeled/` | 28 transactions examinées une à une par l'équipe Confiance & Sécurité (`investigations.csv`) : pour mesurer vos règles |
| `data/ambiguous_cases.csv` | Des cas ambigus, pour l'exercice de gouvernance |

L'export comporte des défauts de qualité : plusieurs formats de date, des montants avec virgule, des valeurs manquantes, des identifiants écrits de plusieurs façons.
Nettoyez avant de détecter, puis reliez les fichiers (transaction → annonce → vendeur·se et acheteur·se → catégorie).

Les 7 règles sont décrites dans [`docs/business_rules.md`](docs/business_rules.md). Elles signalent des **anomalies** à vérifier, pas des fraudes avérées.

## Les commandes

```bash
pytest                         # tous les tests (référence, loader, vos tests)
python -m fraudscan.evaluate   # mesure vos règles sur data/labeled/
python -m fraudscan            # analyse complète et rapport (optionnel)
```

Dans le Chat de VS Code : `/plan` (plan à valider avant de coder), `#fichier` (ajouter un fichier au contexte),
`#codebase` (chercher le code utile), `/compact` (résumer la conversation), `/fork` (dupliquer la conversation).

## Les règles d'usage de l'IA

- **Interactive + Manual permissions** : lisez chaque demande de l'agent avant de l'accepter.
- **Un commit avant chaque tâche** confiée à l'agent : vous pouvez toujours revenir à l'état précédent.
- **Une règle à la fois**, avec ses tests, puis un commit.
- **Vous restez responsables** du code : relisez chaque diff, lancez les tests.
- Ne modifiez jamais un test existant pour le faire réussir.

## Plan B

En cas de blocage technique, simulez l'agent sur papier : pour chaque étape, notez l'outil appelé, son entrée, son résultat,
et s'il faut une validation humaine. La simulation documentée est un livrable valable.
