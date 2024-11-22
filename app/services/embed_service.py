from sklearn.preprocessing import normalize
import torch
from transformers import AutoTokenizer, AutoModel
from typing import List

from app.config.settings import get_settings
from app.exceptions.embedding import (
    EmbeddingError,
    InferenceError,
    InputValidationError,
    ModelLoadError,
    TokenizationError,
)
from app.logging.logger import logger


class EmbedService:
    def __init__(self):
        self.settings = get_settings()
        self._setup_device()
        self._setup_model()

    def _setup_device(self) -> None:
        try:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            if not torch.cuda.is_available():
                logger.warning("No cuda available.")
            logger.info(f"Using device: {self.device}")

        except Exception as e:
            logger.error(f"Device load error: {str(e)}")
            raise ModelLoadError()

    def _setup_model(self) -> None:
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.settings.HF_MODEL, trust_remote_code=False
            )

            self.model = AutoModel.from_pretrained(
                self.settings.HF_MODEL, trust_remote_code=False
            ).to(self.device)

            self.model.eval()

            logger.info(f"Loaded model: {self.settings.HF_MODEL}")

        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise ModelLoadError()

    def _validate_input(self, content: str) -> None:
        try:
            if not content.strip():
                raise InputValidationError("Input cannot be whitespace")

        except Exception as e:
            logger.error(f"Input validation error: {str(e)}")
            raise InputValidationError()

    def _tokenize_input(self, content: str) -> torch.Tensor:
        try:
            inputs = self.tokenizer(
                content,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=self.settings.MAX_LENGTH,
                add_special_tokens=True,
            ).to(self.device)

            return inputs

        except Exception as e:
            logger.error(f"Tokenization failed: {str(e)}")
            raise TokenizationError()

    def _normalize_embedding(self, embedding: torch.Tensor) -> List[float]:
        try:
            # Move to CPU and convert to numpy
            embedding_np = embedding.cpu().numpy()

            # L2 normalization
            normalized = normalize(embedding_np.reshape(1, -1)).flatten()

            # Convert to list
            embedding_list = normalized.tolist()

            return embedding_list

        except Exception as e:
            logger.error(f"Normalization failed: {str(e)}")
            raise InferenceError()

    @torch.no_grad()
    def generate_embedding(self, content):
        try:
            # Validate input
            self._validate_input(content)

            # Tokenize
            inputs = self._tokenize_input(content)

            # Generate embeddings
            with torch.inference_mode():
                output = self.model(**inputs)

            # Extract embedding with mean pooling
            embedding = output.last_hidden_state.mean(dim=1).squeeze()

            # Normalize
            normalized_embedding = self._normalize_embedding(embedding)

            logger.debug(f"Embedding generated of length: {len(normalized_embedding)}")

            return normalized_embedding

        except (InputValidationError, TokenizationError, InferenceError):
            raise

        except Exception as e:
            logger.error(f"Failed to generate embedding: {str(e)}")
            raise EmbeddingError()
