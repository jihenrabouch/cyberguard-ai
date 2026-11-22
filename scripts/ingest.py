"""
Pipeline d'Ingestion & Vectorisation — Projet Fédérateur AI-BD_BI
Spécialité IA & Big Data / BI — Promotion Terminale (M2)

Fonctionnalités :
1. Découpage textuel sémantique ou récursif (RecursiveCharacterTextSplitter)
2. Extraction et enrichissement des métadonnées (Payload JSON)
3. Vectorisation par lots (Batching d'embeddings)
4. Initialisation de la collection Qdrant (HNSW + Cosine)
5. Insertion des points vectoriels avec gestion de persistance
"""

import os
import sys
import uuid
import logging
from typing import List, Dict, Any
from pathlib import Path

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("IngestPipeline")

# Tentative d'import des bibliothèques requises
try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models as qmodels
    from sentence_transformers import SentenceTransformer
except ImportError as e:
    logger.error(f"Bibliothèque manquante : {e}")
    logger.error("Veuillez installer les dépendances : pip install qdrant-client sentence-transformers")
    sys.exit(1)


# Configuration par défaut (peut être surchargée par les variables d'environnement)
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_REST_PORT", 6333))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "rag_enterprise_docs")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2") # Remplacer par BAAI/bge-m3 en GPU


class IngestionEngine:
    """Moteur d'ingestion et d'indexation vectorielle industrielle."""

    def __init__(self, host: str = QDRANT_HOST, port: int = QDRANT_PORT):
        logger.info(f"Connexion à la base vectorielle Qdrant sur {host}:{port}...")
        self.client = QdrantClient(host=host, port=port)
        logger.info(f"Chargement du modèle d'embeddings : {EMBEDDING_MODEL_NAME}...")
        self.embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)
        self.vector_dim = self.embedder.get_sentence_embedding_dimension()
        logger.info(f"Modèle prêt. Dimension des vecteurs : {self.vector_dim}")

    def create_collection_if_not_exists(self, collection_name: str = COLLECTION_NAME):
        """Crée la collection avec index HNSW et métrique Cosine."""
        collections = self.client.get_collections().collections
        exists = any(c.name == collection_name for c in collections)

        if not exists:
            logger.info(f"Création de la collection '{collection_name}' (dim={self.vector_dim}, metric=Cosine)...")
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=qmodels.VectorParams(
                    size=self.vector_dim,
                    distance=qmodels.Distance.COSINE
                ),
                hnsw_config=qmodels.HnswConfigDiff(
                    m=16,               # Nombre de liens par nœud dans le graphe
                    ef_construct=100    # Précision lors de la construction
                )
            )
            logger.info("Collection créée avec succès.")
        else:
            logger.info(f"La collection '{collection_name}' existe déjà.")

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Découpage récursif simple par paragraphes et phrases."""
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = ""

        for p in paragraphs:
            p = p.strip()
            if not p:
                continue
            if len(current_chunk) + len(p) <= chunk_size:
                current_chunk += " " + p if current_chunk else p
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = p

        if current_chunk:
            chunks.append(current_chunk)
        return chunks

    def ingest_documents(self, raw_data_dir: str = "data/raw", batch_size: int = 64):
        """Lit les fichiers, découpe en chunks et insère dans Qdrant par lots."""
        path = Path(raw_data_dir)
        if not path.exists():
            logger.warning(f"Le dossier '{raw_data_dir}' n'existe pas. Création d'un dossier vide.")
            path.mkdir(parents=True, exist_ok=True)
            return

        documents = list(path.glob("**/*.*"))
        logger.info(f"{len(documents)} document(s) trouvé(s) dans '{raw_data_dir}'.")

        all_points = []
        for doc in documents:
            if doc.suffix.lower() not in [".txt", ".md", ".json"]:
                logger.info(f"Fichier ignoré (extension non textuelle) : {doc.name}")
                continue

            try:
                content = doc.read_text(encoding="utf-8")
                chunks = self.chunk_text(content)
                logger.info(f"Document '{doc.name}' découpé en {len(chunks)} chunks.")

                for idx, chunk in enumerate(chunks):
                    # Métadonnées riches (Payload)
                    payload = {
                        "doc_id": doc.stem,
                        "source": doc.name,
                        "chunk_index": idx,
                        "content": chunk,
                        "char_count": len(chunk)
                    }
                    # ID déterministe ou UUID
                    point_id = str(uuid.uuid4())
                    all_points.append((point_id, chunk, payload))

            except Exception as ex:
                logger.error(f"Erreur lors de la lecture de '{doc.name}' : {ex}")

        if not all_points:
            logger.warning("Aucun chunk à indexer. Déposez des fichiers texte dans 'data/raw/'.")
            return

        # Vectorisation et insertion par lots (Batching)
        total_chunks = len(all_points)
        logger.info(f"Démarrage de la vectorisation de {total_chunks} chunks par lots de {batch_size}...")

        for i in range(0, total_chunks, batch_size):
            batch = all_points[i:i + batch_size]
            texts = [item[1] for item in batch]
            embeddings = self.embedder.encode(texts, show_progress_bar=False, normalize_embeddings=True)

            qdrant_points = [
                qmodels.PointStruct(
                    id=item[0],
                    vector=embeddings[idx].tolist(),
                    payload=item[2]
                )
                for idx, item in enumerate(batch)
            ]

            self.client.upsert(
                collection_name=COLLECTION_NAME,
                points=qdrant_points
            )
            logger.info(f"Progression : {min(i + batch_size, total_chunks)} / {total_chunks} insérés.")

        logger.info("Ingestion vectorielle terminée avec succès !")


if __name__ == "__main__":
    engine = IngestionEngine()
    engine.create_collection_if_not_exists()
    engine.ingest_documents()

