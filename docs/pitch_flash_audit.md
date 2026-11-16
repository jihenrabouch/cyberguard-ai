# Support de présentation — Flash-Audit CyberGuard AI

**Format :** 3 minutes de présentation + 1 minute de questions-réponses avec l'enseignant.
**Équipe :** Hela Kchouk, Yassmine Nouira, Jihen Ben Rabouche.
**Prise de parole :** Hela (minute 1), Jihen (minute 2), Yassmine (minute 3) ; questions-réponses ouvertes aux trois membres.

---

## Minute 1 — Problème métier, Corpus & Interface (Hela Kchouk — Lead Data & Frontend)

« Bonjour. Imaginez Sami, développeur junior, qui doit sécuriser le stockage des mots de passe d'une application web. Les bonnes pratiques existent, mais elles sont dispersées dans des dizaines de fiches OWASP. Il perd du temps à chercher, puis à vérifier si la recommandation est fiable.

Une recherche par mots-clés ne suffit pas : une même bonne pratique est écrite avec des mots différents selon les fiches. Un LLM seul ne suffit pas non plus : il répond avec assurance, mais sans source, et peut se tromper.

Notre solution : CyberGuard AI. Nous partons d'un corpus de 20 fiches OWASP en Markdown, soit environ 800 chunks découpés par titres avec métadonnées — fiche, section, URL — pour restituer les réponses et leurs sources dans une interface de chat React. »

## Minute 2 — Cœur du Moteur RAG & Retrieval (Jihen Ben Rabouche — Lead RAG & Retrieval)

« Voici le cœur du moteur RAG. Chaque chunk est vectorisé avec BGE-M3, un modèle multilingue : l'utilisateur peut ainsi poser une question en français sur un corpus en anglais.

Les vecteurs sont stockés dans Qdrant, choisi pour ses filtres sur les métadonnées et son déploiement Docker, en parallèle d'un index lexical BM25.

À chaque question, nous lançons une recherche hybride — dense plus lexicale — puis une fusion des classements par RRF pour capter à la fois les termes techniques exacts et le sens. Un reranker Cross-Encoder est également prévu en Should Have pour affiner la sélection des cinq meilleurs passages. »

## Minute 3 — Génération, Garde-fous & Évaluation Ragas (Yassmine Nouira — Lead Backend, LLM & Évaluation)

« Côté génération, l'API FastAPI transmet uniquement les passages retenus à un LLM local via Ollama, avec citations obligatoires et abstention automatique si le score de pertinence est insuffisant.

Pour prouver la qualité du système, nous construisons un jeu de 80 à 120 questions vérifiées à la main, dont des questions hors corpus, et nous comparons une baseline vectorielle seule à notre pipeline hybride.

Nos cibles : Faithfulness Ragas supérieure ou égale à 0,85, Context Recall supérieur ou égal à 0,80, Recall@5 supérieur ou égal à 0,85, et un premier token en moins de 3 secondes grâce au streaming. Le tout est cadré par 10 User Stories Must Have avec critères d'acceptation mesurables. Merci pour votre attention. »

## Minute 4 — Questions-réponses : arbitrages d'ingénierie

| Arbitrage | Justification | Référent principal |
|---|---|---|
| RAG plutôt qu'un LLM seul ou une recherche par mots-clés | Le mot-clé rate les synonymes, le LLM seul hallucine et ne cite pas. Le RAG relie chaque réponse à des sources vérifiables. | Hela / Yassmine |
| Recherche hybride (BM25 + dense) | BM25 est précis sur les termes techniques (« CSRF », « bcrypt »), le dense capture le sens. La fusion RRF évite de comparer des scores d'échelles différentes. | Jihen |
| Reranker Cross-Encoder (*Should Have*) | Il évalue la paire question–passage de façon plus fine qu'un simple calcul de similarité. Son gain sera mesuré sur NDCG@5, au prix d'une latence supplémentaire. | Jihen |
| Qdrant comme base vectorielle | Base dédiée, filtrage par métadonnées, intégration Python, déploiement local simple avec Docker. | Jihen |
| Limitation des hallucinations | Contexte restreint aux passages retenus, citations obligatoires, abstention si le score est insuffisant, mesure de la Faithfulness avec Ragas. | Yassmine |
| Corpus OWASP et licence | Source officielle et structurée, adaptée à l'ingestion. Licence CC BY-SA 4.0 : attributions et liens conservés. | Hela |
| Taille du corpus (20 fiches) | L'enjeu porte sur la qualité du pipeline : questions en français sur documents anglais, recherche hybride, 80 questions d'évaluation. Extension prévue jusqu'à 30 fiches après contrôle des licences. | Hela / Jihen |
| Objectif de 3 s pour le premier token | Streaming de la réponse : l'affichage commence dès le premier token généré. La valeur réelle sera mesurée sur le modèle local. | Yassmine |
| Suivi des performances | Tracing de la latence et des tokens par requête (Should Have), et rapport Ragas comparé à la baseline. | Yassmine |
| Injection de prompt | Les documents sont traités comme des données non fiable, séparés des instructions système. | Yassmine |
| Arbitrage en cas de retard | Les Must Have sont protégés : ingestion, recherche hybride, citations, évaluation, démonstration stable. | Toutes les 3 |