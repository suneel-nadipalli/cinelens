import chromadb

from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
from chromadb.config import Settings


client = chromadb.PersistentClient(path="DB")

embedding_function = OpenCLIPEmbeddingFunction()

image_loader = ImageLoader()