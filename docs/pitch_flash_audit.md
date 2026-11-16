# Support de présentation — Flash-Audit CyberGuard AI

**Format :** 3 minutes de présentation + 1 minute de questions-réponses avec l'enseignant.
**Équipe :** Hela Kchouk, Yassmine Nouira, Jihen Ben Rabouche.
**Prise de parole :** Hela (minute 1), Yassmine (minute 2), Jihen (minute 3) ; questions-réponses ouvertes aux trois membres.

---

## Minute 1 — Problème métier, persona, point de douleur

« Bonjour. Imaginez Sami, développeur junior, qui doit sécuriser le stockage des mots de passe d'une application web. Les bonnes pratiques existent, mais elles sont dispersées dans des dizaines de fiches OWASP. Il perd du temps à chercher, puis à vérifier si la recommandation est fiable.

Une recherche par mots-clés ne suffit pas : une même bonne pratique est écrite avec des mots différents selon les fiches. Un LLM seul ne suffit pas non plus : il répond avec assurance, mais sans source, et peut se tromper.

Notre solution : CyberGuard AI, un assistant RAG avancé. Il retrouve les bons passages dans le corpus OWASP, rédige une réponse claire et affiche toujours la source. Et s'il ne trouve rien dans le corpus, il refuse de répondre. »

## Minute 2 — Architecture technique RAG

« Voici l'architecture. Le corpus : 20 fiches OWASP en Markdown, soit environ 800 chunks au départ. Nous les découpons par titres, avec des métadonnées : fiche, section, URL.

Chaque chunk est vectorisé avec BGE-M3, un modèle multilingue : on peut poser une question en français sur un corpus en anglais. Les vecteurs sont stockés dans Qdrant, en parallèle d'un index BM25.

À chaque question, nous lançons une recherche hybride, dense plus lexicale, puis une fusion RRF. Un reranker Cross-Encoder réordonne les candidats et ne garde que les cinq meilleurs passages. Le LLM, via Ollama, répond uniquement à partir de ces passages. L'API est en FastAPI, l'interface en React. Enfin, nous tracerons la latence et les tokens de chaque requête pour l'observabilité. »

## Minute 3 — Métriques d'évaluation et backlog Must Have

« Comment prouver que ça marche ? Nous construisons un jeu de 80 à 120 questions vérifiées à la main, dont des questions hors corpus, et nous comparons une baseline vectorielle seule à notre pipeline complet.

Nos cibles : Faithfulness Ragas supérieure ou égale à 0,85, Context Recall supérieur ou égal à 0,80, Recall@5 supérieur ou égal à 0,85, et un premier token en moins de 3 secondes grâce au streaming.

Dix User Stories Must Have forment le MVP : ingestion, chunking avec métadonnées, indexation hybride, recherche RRF, API, citations obligatoires, abstention, interface de chat, évaluation Ragas et dépôt sans secrets. Chacune a des critères d'acceptation mesurables. Reranking, filtres, streaming et tracing sont en Should Have. Merci pour votre attention. »

## Minute 4 — Questions-réponses : arbitrages d'ingénierie

| Arbitrage | Justification |
|---|---|
| RAG plutôt qu'un LLM seul ou une recherche par mots-clés | Le mot-clé rate les synonymes, le LLM seul hallucine et ne cite pas. Le RAG relie chaque réponse à des sources vérifiables. |
| Recherche hybride (BM25 + dense) | BM25 est précis sur les termes techniques (« CSRF », « bcrypt »), le dense capture le sens. La fusion RRF évite de comparer des scores d'échelles différentes. |
| Reranker Cross-Encoder | Il évalue la paire question–passage de façon plus fine qu'un simple calcul de similarité. Son gain sera mesuré sur NDCG@5, au prix d'une latence supplémentaire. |
| Qdrant comme base vectorielle | Base dédiée, filtrage par métadonnées, intégration Python, déploiement local simple avec Docker. |
| Limitation des hallucinations | Contexte restreint aux passages retenus, citations obligatoires, abstention si le score est insuffisant, mesure de la Faithfulness avec Ragas. |
| Corpus OWASP et licence | Source officielle et structurée, adaptée à l'ingestion. Licence CC BY-SA 4.0 : attributions et liens conservés. |
| Taille du corpus (20 fiches) | L'enjeu porte sur la qualité du pipeline : questions en français sur documents anglais, recherche hybride, 80 questions d'évaluation. Extension prévue jusqu'à 30 fiches après contrôle des licences. |
| Objectif de 3 s pour le premier token | Streaming de la réponse : l'affichage commence dès le premier token généré. La valeur réelle sera mesurée sur le modèle local. |
| Suivi des performances | Tracing de la latence et des tokens par requête (Should Have), et rapport Ragas comparé à la baseline. |
| Injection de prompt | Les documents sont traités comme des données non fiables, séparés des instructions système. |
| Arbitrage en cas de retard | Les Must Have sont protégés : ingestion, recherche hybride, citations, évaluation, démonstration stable. |
