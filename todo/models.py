from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    STATUSES_CHOISES = [
        ('IN_PROGRESS', 'In progress'),
        ('COMPLITED', 'Completed'),
        ('FAILED', 'Failed'),
        ('NOT_STARTED', 'Not started'),
    ]
    PRIORITIES_CHOISES = [
        ('1', 'LOW'),
        ('2', 'MEDIUM'),
        ('3', 'HIGH'),
    ]
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    executor = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUSES_CHOISES, default='NOT_STARTED')
    priority = models.CharField(max_length=15,choices=PRIORITIES_CHOISES, default='LOW')
    created_date = models.DateTimeField(auto_now_add=True)
    deadline_date = models.DateTimeField(null=True, blank=True)
    close_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
            return self.title
