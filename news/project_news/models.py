from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache

class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.authorUser}'


    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')

    NEWS = 'NW'
    ARTICLE = 'AR'
    TYPE = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    type = models.CharField(max_length=2, choices=TYPE, default=NEWS, verbose_name='Категория' )
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    text = models.TextField(null=True, blank=True, verbose_name='Текст')
    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг')

    @property
    def in_category(self):
        list_of_category=[category.name for category in self.category.all()]
        return list_of_category

    def __str__(self):
        return f'{self.title} {self.dateCreation}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'posts-{self.pk}')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
