from typing import List, Tuple
from langchain_community.vectorstores import Qdrant

class VectorSearchAdapter:
    def __init__(self, vectorstore: Qdrant):
        self.vs = vectorstore

    def search(self, query: str, k: int = 5) -> List[Tuple[str, str, float]]:
        """Return [(path, text, score)] using vector similarity."""
        docs_scores = self.vs.similarity_search_with_score(query, k=k)
        out = []
        for doc, score in docs_scores:
            path = doc.metadata.get("source", "unknown")
            out.append((path, doc.page_content, float(score)))
        return out
