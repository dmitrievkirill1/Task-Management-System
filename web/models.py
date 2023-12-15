from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Project(models.Model):
    name = models.CharField(verbose_name='Название проекта', max_length=255)
    description = models.TextField(verbose_name='Описание проекта')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(verbose_name='Название задачи', max_length=255)
    description = models.TextField(verbose_name='Описание задачи')
    creation_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(verbose_name='Дедлайн зададчи')
    status = models.CharField(verbose_name='Статус задачи', max_length=50)
    user_assigned = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_assigned')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Comment by {self.user.username} on {self.task.title}"
