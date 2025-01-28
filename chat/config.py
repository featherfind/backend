from django.conf import settings

OPENAI_CONFIG = {
    'embedding_model': getattr(settings, 'OPENAI_EMBEDDING_MODEL', 'text-embedding-ada-002'),
    'completion_model': getattr(settings, 'OPENAI_COMPLETION_MODEL', 'gpt-3.5-turbo'),
    'max_tokens': getattr(settings, 'OPENAI_MAX_TOKENS', 150),
    'chunk_size': getattr(settings, 'OPENAI_CHUNK_SIZE', 8000),
    'max_chunks': getattr(settings, 'OPENAI_MAX_CHUNKS', 5),
}

BIRD_SPECIES = getattr(settings, 'BIRD_SPECIES_LIST', [
    "Pigeon", "Sparrow", "Eagle", "Parrot"
])
