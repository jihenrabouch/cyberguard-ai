# Pitch Flash-Audit — CyberGuard AI (4 minutes chrono)

**Format :** 3 minutes de pitch + 1 minute de questions du prof. Environ 130 mots par minute à l'oral.
**Répartition suggérée :** Hela (minute 1), Yassmine (minute 2), Jihen (minute 3). À ajuster entre vous. Répétez avec un chrono.

---

## Minute 1 — Problème métier, persona, douleur (≈ 130 mots)

« Bonjour. Imaginez Sami, développeur junior, qui doit sécuriser le stockage des mots de passe d'une application web. Les bonnes pratiques existent, mais elles sont dispersées dans des dizaines de fiches OWASP. Il perd du temps à chercher, puis à vérifier si la recommandation est fiable.

Une recherche par mots-clés ne suffit pas : une même bonne pratique est écrite avec des mots différents selon les fiches. Un LLM seul ne suffit pas non plus : il répond avec assurance, mais sans source, et peut se tromper.

Notre solution : CyberGuard AI, un assistant RAG avancé. Il retrouve les bons passages dans le corpus OWASP, rédige une réponse claire et affiche toujours la source. Et s'il ne trouve rien dans le corpus, il refuse de répondre. »

## Minute 2 — Architecture RAG (≈ 130 mots)

« Voici l'architecture. Le corpus : 20 fiches OWASP en Markdown, soit environ 800 chunks au départ. Nous les découpons par titres, avec des métadonnées : fiche, section, URL.

Chaque chunk est vectorisé avec BGE-M3, un modèle multilingue : on peut poser une question en français sur un corpus en anglais. Les vecteurs sont stockés dans Qdrant, en parallèle d'un index BM25.

À chaque question, nous lançons une recherche hybride, dense plus lexicale, puis une fusion RRF. Ensuite, un reranker Cross-Encoder réordonne les candidats et ne garde que les cinq meilleurs passages. Le LLM, via Ollama, répond uniquement à partir de ces passages. L'API est en FastAPI, l'interface en React. Ce n'est pas un RAG naïf avec trois chunks. »

## Minute 3 — Métriques et backlog Must Have (≈ 130 mots)

« Comment prouver que ça marche ? Nous construisons un jeu de 80 à 120 questions vérifiées à la main, avec des questions hors corpus. Nous comparons une baseline vectorielle seule à notre pipeline complet.

Nos cibles : Faithfulness Ragas supérieure ou égale à 0,85, Context Recall supérieur ou égal à 0,80, Recall@5 supérieur ou égal à 0,85, et un premier token en moins de 3 secondes.

Côté backlog, dix User Stories Must Have forment le MVP : ingestion reproductible, chunking avec métadonnées, indexation hybride, recherche RRF, API, citations obligatoires, abstention, interface de chat, évaluation Ragas et dépôt propre sans secrets. Chacune a des critères d'acceptation mesurables. Le reranking et les filtres sont en Should Have. Merci, nous sommes prêts pour vos questions. »

## Minute 4 — Questions du prof : réponses préparées

| Question probable | Réponse courte |
|---|---|
| Pourquoi pas juste un LLM ou une recherche par mots-clés ? | Le mot-clé rate les synonymes, le LLM seul hallucine et ne cite pas. Le RAG relie la réponse à des sources vérifiables. |
| Pourquoi une recherche hybride ? | BM25 est précis sur les termes techniques (« CSRF », « bcrypt »), le dense gère le sens. Ils se complètent, la fusion RRF évite de comparer leurs scores. |
| Pourquoi un reranker, qu'apporte-t-il ? | Le Cross-Encoder évalue la paire question–passage de façon plus fine. Nous mesurerons son gain sur NDCG@5, au prix d'un peu de latence. |
| Pourquoi Qdrant ? | Recherche hybride native, filtrage par métadonnées, démarrage simple avec Docker. |
| Comment limitez-vous les hallucinations ? | Contexte limité aux passages retenus, citations obligatoires, abstention si le score est trop bas, évaluation avec la Faithfulness Ragas. |
| Pourquoi ce corpus, et la licence ? | Source officielle et structurée, adaptée à l'ingestion. Licence CC BY-SA 4.0 : nous gardons attributions et liens. |
| Comment gérez-vous le risque de prompt injection ? | Les documents sont traités comme des données non fiables et séparés des instructions système. |
| Que ferez-vous si le temps manque ? | On protège les Must Have : ingestion, recherche hybride, citations, évaluation, démo stable. |

## Conseils de passage

- Chaque minute annoncée, une seule idée à retenir.
- Dites « Must Have » et « critères d'acceptation » : ce sont des mots de la grille.
- Ne dépassez pas 3 minutes de pitch : le dépassement est pénalisé (2 points sur 20 pour la clarté, le temps et le dépôt Git).
- Avant l'audit, vérifiez que le dépôt GitHub est propre : README, `.gitignore`, aucun secret.
