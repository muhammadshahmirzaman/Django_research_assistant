from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField

class Document(models.Model):
    org = models.ForeignKey("accounts.Organization", on_delete=models.CASCADE)
    collection = models.ForeignKey("accounts.Collection", on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    file = models.FileField(upload_to="docs/")
    mime_type = models.CharField(max_length=100)
    num_pages = models.IntegerField(default=0)
    meta = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

class Chunk(models.Model):
    """Normalized content chunks with embeddings and FTS."""
    org = models.ForeignKey("accounts.Organization", on_delete=models.CASCADE)
    collection = models.ForeignKey("accounts.Collection", on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="chunks")
    idx = models.IntegerField()                      # chunk index in doc
    content = models.TextField()
    tsv = SearchVectorField(null=True)               # generated via migration/trigger
    embedding = models.BinaryField(null=True)        # pgvector (stored as vector); see migration
    token_count = models.IntegerField(default=0)

    class Meta:
        unique_together = [("document","idx")]
        indexes = [
            GinIndex(fields=["tsv"], name="chunk_tsv_gin"),
            models.Index(name="chunk_title_trgm", fields=["content"], opclasses=["gin_trgm_ops"]),
        ]

class IngestionJob(models.Model):
    org = models.ForeignKey("accounts.Organization", on_delete=models.CASCADE)
    collection = models.ForeignKey("accounts.Collection", on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="pending")  # pending|running|done|failed
    error = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
