from django.db import models

class ChatSession(models.Model):
    org = models.ForeignKey("accounts.Organization", on_delete=models.CASCADE)
    collection = models.ForeignKey("accounts.Collection", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=12)   # user|assistant|system
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Citation(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="citations")
    chunk = models.ForeignKey("documents.Chunk", on_delete=models.CASCADE)
    score = models.FloatField()
    start = models.IntegerField(null=True)   # optional span
    end = models.IntegerField(null=True)
