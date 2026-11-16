# Fiche de Cadrage d'Ingénierie — CyberGuide
## Assistant RAG d'aide à la compréhension de la sécurité des applications web

---

### 1. Fiche d'Identité du Projet

- **Nom du Projet :** CyberGuide
- **Intitulé :** Assistant intelligent de recherche documentaire en cybersécurité applicative (Web Application Security).
- **Membres de l'Équipe :**
  1. **Hela Kchouk** — Lead Data / Retrieval
  2. **Yasmine Nouira** —  Lead Backend / MLOps
  3. **Jihen Ben Rabouche** — Lead Frontend / Infra
- **Lien du Dépôt GitHub :** À compléter après création du dépôt : `https://github.com/Hellakc/CyberGuide`
- **Branche de travail principale :** `main` (à protéger après configuration des règles de branche).


---

### 2. Cadrage du Problème Métier ("Problem-First")

#### 2.1 Persona Cible & Contexte Opérationnel

- **Utilisateur visé :** Étudiant en informatique ou développeur junior qui développe ou maintient une application web et souhaite comprendre les bonnes pratiques de sécurité.
- **Point de douleur majeur (*Pain point*) :** Les recommandations de sécurité applicative sont dispersées dans de nombreux guides techniques. L'utilisateur doit ouvrir plusieurs pages, parcourir de longs documents et connaître les bons mots-clés pour trouver une recommandation précise (par exemple : prévenir une injection SQL, sécuriser l'authentification ou valider un téléversement de fichier).
- **Limite des approches classiques (Pourquoi l'IA générative et le RAG ?) :** Une recherche par mots-clés ne comprend pas toujours l'intention exprimée en langage naturel et peut manquer les passages qui utilisent des termes différents. Un chatbot généraliste peut produire des réponses non vérifiées ou inventer des recommandations. Le RAG permet de retrouver des extraits dans un corpus sélectionné, de les fournir au modèle pour rédiger une réponse et de présenter les références documentaires utilisées.

#### 2.2 Proposition de Valeur

CyberGuide est une application web de question-réponse documentaire qui permet à un étudiant ou développeur junior de poser une question en langage naturel sur la sécurité des applications web. Le système recherche les passages pertinents dans un corpus initial d'au moins 20 guides OWASP, génère une réponse en français ou en anglais à partir des extraits retrouvés et affiche les sources (titre, section, lien et extrait). Si le corpus ne contient pas suffisamment d'informations, l'application doit le signaler au lieu d'inventer une réponse.

**Exemples de questions :**
- Comment prévenir une injection SQL dans une application web ?
- Quelle est la différence entre authentification et autorisation ?
- Quelles précautions prendre lors du téléversement de fichiers ?
- Comment protéger une session utilisateur ?
- Comment sécuriser une API REST ?

**Limites fonctionnelles et de sécurité :**
- Le système fournit une aide pédagogique et documentaire ; il ne remplace pas un audit, un pentest ou un avis professionnel.
- Le périmètre initial est défensif : compréhension des risques et mesures de prévention.
- Pas d'exécution de code, de scan de cible, d'exploitation de vulnérabilités ni de diagnostic automatique d'un site.
- Les réponses doivent être limitées aux informations retrouvées et accompagnées de citations vérifiables.

---

### 3. Données & Volumétrie

- **Source principale :** OWASP Cheat Sheet Series — dépôt officiel `https://github.com/OWASP/CheatSheetSeries` et site `https://cheatsheetseries.owasp.org/`.
- **Formats des données sources :** [x] Markdown (`.md`) ; [ ] PDF ; [ ] JSON/CSV ; [ ] Tables SQL ; [ ] Images/scans.
- **Volumétrie initiale (PoC S1-S3) :** 20 documents Markdown officiels, avec une cible indicative de 500 à 2 000 chunks après ingestion (à mesurer réellement).
- **Volumétrie cible du projet étudiant :** 20 à 30 documents validés, puis extension éventuelle après contrôle des licences et de la pertinence.
- **Fréquence de mise à jour :** [x] Statique

---

### 4. Architecture Technique & Composants RAG

- **Ingestion :** scripts Python lisant les fichiers Markdown de `data/raw/`, extraction des titres/sections et conservation des métadonnées et liens sources.
- **Stratégie de Chunking :** [x] Recursive Character / découpage récursif respectant autant que possible les titres et sections Markdown.
  - **Taille de chunk visée :** environ 600 tokens.
  - **Overlap visé :** environ 80 tokens.
  - **Justification :** conserver des unités assez petites pour retrouver une recommandation précise, tout en gardant le contexte de la section. Ces valeurs seront ajustées à partir des tests de retrieval.
- **Modèle d'Embeddings :** `BAAI/bge-m3` (multilingue ; dimension annoncée de 1024). Il est retenu pour permettre des questions en français sur un corpus majoritairement anglais. Vérifier la dimension et la configuration lors de l'implémentation.
- **Base vectorielle retenue :** [x] Qdrant.
  - **Justification du choix :** Qdrant fournit une base vectorielle dédiée, des filtres sur les métadonnées, une intégration Python et un déploiement local via Docker. Elle convient à un PoC et permet de filtrer par document ou catégorie.
- **Reranker (Cross-Encoder) :** reranking avec `BAAI/bge-reranker-v2-m3` si les ressources matérielles le permettent. Le reranker sera évalué avant d'être conservé.
- **LLM de génération :** modèle instruct configurable via Ollama (par exemple `qwen2.5:7b` si les ressources locales le permettent). Prévoir une configuration alternative compatible API si l'environnement local est insuffisant ; ne jamais versionner de clé API.


---

### 5. Métriques Quantitatives & SLAs

Les valeurs ci-dessous sont des **objectifs de validation**, pas des performances déjà mesurées.

| Métrique | Définition / Outil | Objectif cible (KPI) |
| :--- | :--- | :---: |
| **Recall@10 (Retrieval)** | Présence d'au moins un passage de référence pertinent dans les 5 premiers résultats, sur un jeu de questions annoté | ≥ 85 % |
| **Faithfulness** | Part des affirmations de la réponse soutenues par le contexte récupéré ; évaluation Ragas + vérification manuelle | ≥ 0,85 |
| **Answer Relevance** | Pertinence de la réponse par rapport à la question ; Ragas + vérification manuelle | ≥ 0,80 |
| **Latence First-Token (TTFT)** | Temps d'affichage du premier token en streaming | < 800 ms |
| **Latence E2E** | Temps entre l'envoi de la question et la réponse complète, mesuré sur l'environnement de test | À mesurer ; objectif initial < 15 s avec modèle local |


---

### 6. Gestion des Risques & Garde-fous

- **Prévention des Hallucinations :** réponse strictement fondée sur les extraits récupérés ; afficher les sources ; réponse d'abstention si les éléments sont insuffisants.

- **Protection des secrets :** variables d'environnement dans `.env`, fichier `.env` exclu de Git, fichier `.env.example` sans secret réel.


- **Réseau :** Qdrant non exposé publiquement en production ; accès limité au réseau interne Docker pendant le PoC.
