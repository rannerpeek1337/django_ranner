from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название категории")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category_articles", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Article(models.Model):
    title = models.CharField(verbose_name="Название статьи", max_length=200)
    content = models.TextField(verbose_name="Описание статьи")
    image = models.ImageField(verbose_name="Фото статьи", upload_to="articles/", blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Активна ли статья?", default=True)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    views = models.IntegerField(default=0)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name="Категория")
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Автор")

    def get_image(self):
        if not self.image:
            return "https://images.satu.kz/126101314_w640_h640_razdel-v-razrabotketovary.jpg"
        return self.image.url

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ArticleCountView(models.Model):
    session_id = models.CharField(max_length=150, null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


# kivy

class Like(models.Model):
    user = models.ManyToManyField(User, related_name="likes")
    article = models.OneToOneField(Article, on_delete=models.CASCADE, blank=True, null=True, related_name="likes")
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, blank=True, null=True, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.article)


class Dislike(models.Model):
    user = models.ManyToManyField(User, related_name="dislikes")
    article = models.OneToOneField(Article, on_delete=models.CASCADE, blank=True, null=True, related_name="dislikes")
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, blank=True, null=True, related_name="dislikes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.article)