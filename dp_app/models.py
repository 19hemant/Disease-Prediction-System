from django.db import models

class PredictionHistory(models.Model):
    symptoms = models.TextField()
    result = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.result} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    
from django.db import models

class History(models.Model):
    fever = models.IntegerField()
    headache = models.IntegerField()
    nausea = models.IntegerField()
    vomiting = models.IntegerField()
    fatigue = models.IntegerField()
    joint_pain = models.IntegerField()
    skin_rash = models.IntegerField()
    cough = models.IntegerField()
    weight_loss = models.IntegerField()
    yellow_eyes = models.IntegerField()
    predicted_disease = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.predicted_disease} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"
    
    from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

