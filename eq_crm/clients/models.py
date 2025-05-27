from django.db import models


class Clients(models.Model):
    unp = models.CharField(max_length=18, unique=True)
    name = models.CharField(max_length=180)
    date_add = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"УНП: {self.unp} | {self.name} | Дата создания: {self.date_add}"
