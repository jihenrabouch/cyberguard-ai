# Backlog Technique MoSCoW — CyberGuide
## Découpage Agile des User Stories & Critères d'Acceptation

**Projet :** assistant RAG documentaire consacré à la sécurité des applications web.  
**Équipe :** Hela (Lead Data & RAG), Jihen (Lead Backend & API), Yasmine (Lead Frontend & DevOps).  
**Note :** les séances S1 à S7 sont indicatives et doivent être adaptées au calendrier réel du cours.

---

## 1. MUST HAVE (Indispensables pour la livraison)

| ID | User Story Technique | Critères d'Acceptation (DoD) | Responsable | Séance cible |
| :-: | :--- | :--- | :--- | :-: |
| **US-01** | En tant que Lead Data, je veux constituer un corpus d'au moins 20 documents OWASP pertinents et réutilisables légalement. | 20 fichiers Markdown présents dans `data/raw/` ; source et URL enregistrées ; licence et attribution documentées ; documents dépréciés/exclus repérés. | Hela | S1 |
| **US-02** | En tant que Data Engineer, je veux ingérer les fichiers Markdown et extraire leur structure. | Script Python lisant `data/raw/` ; erreurs de lecture gérées ; titres/sections préservés ; métadonnées `doc_id`, `title`, `source_url`, `section`, `chunk_id` disponibles. | Hela | S2 |
| **US-03** | En tant que Data Engineer, je veux découper les documents en chunks adaptés à la recherche. | Chunking récursif tenant compte des titres ; taille initiale ~600 tokens et overlap ~80 tokens ; aucun chunk vide ; traçabilité vers le document et la section d'origine. | Hela | S2 |
| **US-04** | En tant que système RAG, je veux générer les embeddings et indexer les chunks dans Qdrant. | Qdrant démarre avec Docker Compose ; embeddings BGE-M3 enregistrés ; dimension contrôlée ; identifiants et métadonnées conservés ; réindexation documentée. | Hela | S3 |
| **US-05** | En tant qu'utilisateur, je veux que le système retrouve les passages les plus pertinents pour ma question. | Recherche vectorielle et BM25 disponibles ; fusion des résultats ; top-k configurable ; tests de pertinence sur un jeu de questions annoté. | Hela | S3 |
| **US-06** | En tant que système RAG, je veux reranker les passages candidats afin d'améliorer leur ordre de pertinence. | Reranker évalué sur le même jeu de test ; comparaison avant/après ; top-5 transmis au générateur ; possibilité de désactiver le reranker si ressources insuffisantes. | Hela | S4 |
| **US-07** | En tant qu'application cliente, je veux interroger le backend via une API REST typée. | FastAPI ; schémas Pydantic v2 ; endpoint de question ; validation des entrées ; erreurs HTTP cohérentes ; documentation OpenAPI/Swagger disponible. | Jihen | S4 |
| **US-08** | En tant qu'utilisateur, je veux recevoir une réponse fondée sur les extraits retrouvés et voir les sources. | Prompt limitant la réponse au contexte ; réponse d'abstention si contexte insuffisant ; chaque source affiche titre, section, URL et extrait ; aucun secret dans la réponse. | Jihen + Hela | S4-S5 |
| **US-09** | En tant qu'utilisateur, je veux poser une question depuis une interface web simple. | Interface React ; champ de saisie ; affichage question/réponse ; états chargement/erreur ; affichage des références ; intégration avec l'API. | Yasmine | S5 |
| **US-10** | En tant qu'équipe, nous voulons tester et lancer le projet de manière reproductible. | Instructions d'installation ; `.gitignore` ; `.env.example` ; tests unitaires du pipeline et de l'API ; Docker Compose pour les services prévus ; dépôt GitHub documenté. | Toutes (Yasmine coordinatrice) | S6-S7 |

---

## 2. SHOULD HAVE (Forte valeur ajoutée)

| ID | User Story Technique | Critères d'Acceptation | Responsable | Séance cible |
| :-: | :--- | :--- | :--- | :-: |
| **US-11** | En tant que Data Scientist, je veux évaluer la qualité des réponses et du retrieval. | Jeu d'au moins 30 questions annotées ; Recall@5 calculé ; Faithfulness et Answer Relevance évaluées avec Ragas et contrôles manuels ; résultats consignés. | Hela | S5-S6 |
| **US-12** | En tant qu'utilisateur, je veux conserver l'historique de la conversation pendant ma session. | Historique visible dans l'interface ; bouton nouvelle conversation ; aucune donnée sensible persistée inutilement. | Yasmine + Jihen | S6 |
| **US-13** | En tant que responsable technique, je veux suivre les erreurs et les temps de réponse. | Logs structurés sans secrets ; temps de retrieval et génération mesurés ; erreurs API consultables en environnement de développement. | Jihen | S6 |
| **US-14** | En tant qu'utilisateur, je veux filtrer les réponses par thème de sécurité. | Filtres par catégorie/document ; métadonnées indexées ; tests confirmant que le filtre restreint les résultats attendus. | Hela + Yasmine | S6 |

---

## 3. COULD HAVE (Améliorations optionnelles)

| ID | User Story Technique | Critères d'Acceptation |
| :-: | :--- | :--- |
| **US-15** | En tant qu'utilisateur, je veux recevoir une réponse en streaming. | Endpoint SSE fonctionnel ; interface affichant progressivement la réponse ; gestion de l'interruption et des erreurs. |
| **US-16** | En tant qu'équipe, nous voulons visualiser les performances du pipeline RAG. | Tracing des étapes ingestion, embedding, retrieval, reranking et génération ; latences mesurées. |
| **US-17** | En tant qu'utilisateur, je veux exporter les références d'une réponse. | Export texte/Markdown contenant la réponse et les sources, sans perdre les URL. |
| **US-18** | En tant que Data Engineer, je veux détecter les changements dans les documents sources. | Script comparant les versions ou empreintes des fichiers ; rapport des documents modifiés ; réindexation contrôlée. |

---

## 4. WON'T HAVE (Exclus du périmètre de cette version)

- Réaliser des pentests, scans de ports ou scans automatiques de sites web.
- Exécuter des exploits ou fournir un service d'attaque informatique.
- Garantir qu'une application est sécurisée ou remplacer un audit professionnel.
- Couvrir toute la cybersécurité (forensique, malware, sécurité physique, réponse aux incidents, etc.).
- Entraîner un LLM from scratch.
- Déployer une plateforme SaaS commerciale avec facturation et abonnements.
- Développer une application mobile native.
- Collecter des documents dont la licence ou l'autorisation de redistribution n'est pas claire.

---

## 5. Règles de priorisation MoSCoW

- **Must Have :** indispensable pour démontrer un RAG complet, de l'ingestion à la réponse sourcée.
- **Should Have :** améliore la qualité, la mesurabilité ou l'expérience, mais peut être livré après le parcours principal.
- **Could Have :** bonus si le temps et les ressources le permettent.
- **Won't Have :** explicitement hors périmètre pour éviter la dispersion.

Les critères d'acceptation doivent être vérifiés par des tests ou une démonstration ; les KPI sont des objectifs à mesurer et non des résultats supposés.
