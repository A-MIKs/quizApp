from django.db import models
import random
# Create your models here.
DIFF_CHOICES = (
    ("easy", "easy"),
    ("medium", "medium"),
    ("hard", "hard")
)

class Quiz(models.Model):
    class Meta:
        verbose_name_plural = "Quizes"

    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=120)
    num_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="duration of the quiz in minutes")
    pass_mark = models.IntegerField(help_text="required score to pass in %")
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES)

    def __str__(self):
        return f"{self.name}-{self.topic}"
    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.num_of_questions]