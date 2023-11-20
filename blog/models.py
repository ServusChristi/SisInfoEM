from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30)

# Fazendo a mudança do nome na pagina do admin
    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")

# novamente mudança do nome para ficar mais facil a referenciação
    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

# apenas mudança de nome
    def __str__(self):
        return f"{self.author} on '{self.post}'"


