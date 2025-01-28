from django.db import models
from openai import OpenAI
from django.conf import settings
import tiktoken
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from openai import OpenAI

client = OpenAI()


# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)


class BirdChat(models.Model):
    species_name = models.CharField(max_length=255, unique=True)
    wikipedia_url = models.URLField()

    def __str__(self):
        return self.species_name


class BirdContent(models.Model):
    bird = models.OneToOneField(BirdChat, on_delete=models.CASCADE, related_name='content')
    content = models.TextField()
    embedding = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return f"Content for {self.bird.species_name}"

    def save_embedding(self):
        if not self.content.strip():
            raise ValueError(f"Content for {self.bird.species_name} is empty.")
        embedding = self.generate_embedding(self.content)
        if np.any(np.isnan(embedding)):
            raise ValueError("Generated embedding contains NaN values.")
        self.embedding = pickle.dumps(embedding)
        self.save()

    def generate_embedding(self, text):
        chunks = self.chunk_text(text)
        embeddings = []

        for chunk in chunks:
            response = client.embeddings.create(input=chunk, model="text-embedding-ada-002")
            embedding = response.data[0].embedding
            if np.any(np.isnan(embedding)):
                raise ValueError(f"Embedding contains NaN for text chunk: {chunk}")
            embeddings.append(embedding)

        final_embedding = np.mean(embeddings, axis=0)
        if np.any(np.isnan(final_embedding)):
            raise ValueError("Final averaged embedding contains NaN.")

        return final_embedding

    def chunk_text(self, text, max_tokens=8000):
        enc = tiktoken.encoding_for_model("text-embedding-ada-002")
        tokens = enc.encode(text)
        chunks = []
        current_chunk = []
        current_chunk_length = 0

        for token in tokens:
            current_chunk.append(token)
            current_chunk_length += 1
            if current_chunk_length >= max_tokens:
                chunks.append(enc.decode(current_chunk))
                current_chunk = []
                current_chunk_length = 0

        if current_chunk:
            chunks.append(enc.decode(current_chunk))

        return chunks

    def get_similarity(self, query_embedding):
        stored_embedding = np.frombuffer(self.embedding, dtype=np.float32)
        if np.any(np.isnan(stored_embedding)) or np.any(np.isnan(query_embedding)):
            raise ValueError("One or both embeddings contain NaN values.")
        similarity = cosine_similarity([stored_embedding], [query_embedding])
        return similarity[0][0]


def generate_query_embedding(query):
    if not query.strip():
        raise ValueError("Query is empty or malformed.")
    response = client.embeddings.create(model="text-embedding-ada-002", input=query)
    query_embedding = np.array(response.data[0].embedding, dtype=np.float32)
    if np.any(np.isnan(query_embedding)):
        raise ValueError("Generated query embedding contains NaN values.")
    return query_embedding


def search_bird_content(query_embedding):
    """Retrieve and return bird content ordered by relevance (highest similarity) to the query embedding."""
    bird_contents = BirdContent.objects.all()

    similarities = []
    for bird_content in bird_contents:
        if bird_content.embedding is None:
            continue
        stored_embedding = np.frombuffer(bird_content.embedding, dtype=np.float32)
        if np.any(np.isnan(stored_embedding)):
            continue
        similarity = bird_content.get_similarity(query_embedding)
        similarities.append((similarity, bird_content))

    similarities.sort(reverse=True, key=lambda x: x[0])

    return similarities


def retrieve_bird_data(query):
    """Retrieve the most relevant bird content for a query by comparing embeddings."""
    query_embedding = generate_query_embedding(query)
    similarities = search_bird_content(query_embedding)

    # If no content is found or all contents have low similarity
    if not similarities:
        return None

    # Return the most relevant content (the one with the highest similarity)
    top_bird_content = similarities[0][1]
    return top_bird_content.content


def query_openai_with_context(query, retrieved_content):
    """Generate an answer from OpenAI's API using the retrieved content as context."""
    prompt = f"Question: {query}\nContext: {retrieved_content}\nAnswer:"
    response = client.completions.create(engine="text-davinci-003", prompt=prompt, max_tokens=150)
    return response.choices[0].text.strip()


def get_answer_for_query(query):
    """Main function to get an answer for a query by retrieving relevant bird data and querying OpenAI."""
    relevant_content = retrieve_bird_data(query)
    if relevant_content is None:
        return "No relevant bird content found."

    final_answer = query_openai_with_context(query, relevant_content)
    return final_answer
