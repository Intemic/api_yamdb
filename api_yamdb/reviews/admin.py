from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Category, Comment, Genre, Review, Title


class TitleInline(admin.TabularInline):
    model = Title.genre.through


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    inlines = [
        TitleInline,
    ]
    fk_name = 'category'
    list_display = (
        'id',
        'name',
        'get_genres',
        'year',
        'description',
        'category'
    )
    empty_value_display = '-пусто-'

    @admin.display(description="Жанры")
    def get_genres(self, obj):
        return [genre for genre in obj.genre.all()]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'author', 'text', 'pub_date')
    empty_value_display = '-пусто-'


admin.site.unregister(Group)
