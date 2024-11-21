import os
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.preprocessing import normalize

from app.config.settings import get_settings


class EmbedService:
    def __init__(self):
        self.settings = get_settings()
        self._setup_device()
        self._setup_model()

    def _setup_device(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def _setup_model(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.settings.HF_MODEL)
        self.model = AutoModel.from_pretrained(self.settings.HF_MODEL).to(self.device)

    def generate_embedding(self, content):
        if not content or not isinstance(content, str):
            raise ValueError("Input Content is Empty or Not Valid String")

        inputs = self.tokenizer(
            content, return_tensors="pt", padding=True, truncation=True
        ).to(self.device)

        with torch.no_grad():
            output = self.model(**inputs)

        # Extract embeddings
        embedding = output.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()

        # L2 normalization
        normalized_embedding = normalize(embedding.reshape(1, -1)).flatten()

        # Return as list for pinecone
        return normalized_embedding.tolist()
