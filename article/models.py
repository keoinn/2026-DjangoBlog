from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import time

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="作者")
    title = models.CharField(max_length=200, verbose_name="標題")
    slug = models.CharField(max_length=200, blank=True, verbose_name="Slug")
    content = models.TextField(verbose_name="內文 (Markdown)")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="發布時間")

    class Meta:
        ordering = ['-pub_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            # 優先使用包含中文的 slugify，若結果為空則備用時間戳記
            generated_slug = slugify(self.title, allow_unicode=True)
            if not generated_slug:
                generated_slug = f"post-{int(time.time())}"
            self.slug = generated_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

