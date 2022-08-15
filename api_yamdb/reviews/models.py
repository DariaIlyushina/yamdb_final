from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLE = [
        (ADMIN, 'Admin'),
        (MODERATOR, 'Moderator'),
        (USER, 'User')
    ]
    username = models.CharField(
        verbose_name='пользователь',
        null=True,
        unique=True,
        max_length=150,
        blank=False
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
        blank=False)
    bio = models.TextField(
        verbose_name='О себе',
        blank=True,
        max_length=555,
        null=True)
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=111,
        choices=ROLE,
        default=USER
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


class Genre(models.Model):
    name = models.CharField(verbose_name='Название жанра', max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(verbose_name='Название категории', max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
        db_index=True)
    year = models.PositiveIntegerField(validators=[validate_year])
    description = models.CharField(
        verbose_name='Описание',
        max_length=150,
        null=True,
        blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Название'
        verbose_name_plural = 'Названия'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='title',
    )
    text = models.TextField(
        verbose_name='review_text',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='author'
    )
    score = models.IntegerField(
        verbose_name='review_score',
        validators=[
            MinValueValidator(1,
                              message='Минимальная оценка - 1'),
            MaxValueValidator(10,
                              message='Максимальная оценка - 10')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='date_of_publication',
        auto_now_add=True)

    class Meta:
        constraints = (models.UniqueConstraint(
            fields=['title', 'author'],
            name='unique_review_by_author'
        ),)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField(
        verbose_name='comment_text'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        verbose_name='date_of_publication',
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='comment_to_review'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
