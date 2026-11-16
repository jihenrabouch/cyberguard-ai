# CyberGuide

**CyberGuide** est un assistant intelligent de recherche documentaire basé sur le Retrieval-Augmented Generation (RAG), consacré à la sécurité des applications web.

## Contexte académique

Ce projet est réalisé dans le cadre de notre cursus en ingénierie informatique, dans le but de mettre en pratique nos connaissances en Intelligence Artificielle, RAG et développement d'applications.

## Problème

Les étudiants en informatique et les développeurs juniors doivent souvent consulter plusieurs guides techniques pour trouver des recommandations de sécurité fiables. CyberGuide facilite cette recherche en permettant de poser des questions en langage naturel et en retournant des réponses appuyées par des extraits et des références documentaires.

## Fonctionnalités prévues

- Recherche documentaire dans un corpus initial de guides OWASP.
- Recherche hybride (sémantique + lexicale) et reranking.
- Réponses générées à partir des passages retrouvés.
- Affichage des sources, sections, liens et extraits.
- Abstention lorsque le corpus ne permet pas de répondre.

## Périmètre

Le projet traite de la sécurité défensive des applications web : authentification, autorisation, injections, validation des entrées, sessions, API, secrets, journalisation et autres bonnes pratiques.

CyberGuide est un outil pédagogique. Il ne réalise pas de pentest, n'exécute pas d'exploit et ne remplace pas un audit de sécurité.

## Architecture envisagée

- **Frontend :** React + Vite
- **Backend :** Python + FastAPI + Pydantic v2
- **Ingestion :** Python, documents Markdown
- **Embeddings :** BAAI/bge-m3
- **Vector store :** Qdrant
- **Recherche lexicale :** BM25
- **Reranking :** BAAI/bge-reranker-v2-m3 (si ressources disponibles)
- **LLM :** modèle instruct via Ollama ou fournisseur compatible configurable
- **Déploiement local :** Docker Compose

## Structure du dépôt

```text
CyberGuide/
├── backend/
├── frontend/
├── data/
│   ├── raw/        
│   
├── docs/
│   ├── fiche_cadrage_projet.md
│   └── matrices_moscow_backlog.md
    ├── OWASP_ATTRIBUTION.md
│   └── CORPUS_MANIFEST.md
├── scripts/
│   └── download_owasp_corpus.py
├── .gitignore
└── README.md
```

## Installation du corpus initial

Les documents sélectionnés proviennent du dépôt officiel OWASP Cheat Sheet Series. Voir `docs/CORPUS_MANIFEST.md` pour les 20 documents, les liens et les informations de licence.

Depuis la racine du dépôt, après installation de Python 3 :

```bash
python scripts/download_owasp_corpus.py
```

Le script télécharge les fichiers Markdown depuis le dépôt officiel. Vérifiez les fichiers obtenus et leurs notices avant de les publier dans votre dépôt.

## Licence et attribution des données

Le corpus OWASP Cheat Sheet Series est annoncé sous **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**. CyberGuide conserve les documents sources séparément du code de l'application et doit préserver les attributions, les liens vers les sources, la référence à la licence et les indications de modification.

- Source : https://github.com/OWASP/CheatSheetSeries
- Site : https://cheatsheetseries.owasp.org/
- Licence : https://creativecommons.org/licenses/by-sa/4.0/

Cette indication concerne le corpus OWASP retenu. Les ressources tierces éventuellement incluses dans un document doivent être vérifiées séparément.

## Équipe

- Hela kchouk — Lead Data / Retrieval
- Yassmine nouira — Lead Backend / MLOps
- Jihen ben rabouche — Lead Frontend / Infra

