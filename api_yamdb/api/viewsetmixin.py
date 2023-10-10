from rest_framework import filters, viewsets
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)

from .permissions import IsAnonimReadOnly, IsSuperUserOrIsAdminOnly


class CategoryGenreBase(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Базовая view для Жанра и Категории"""
    permission_classes = (IsAnonimReadOnly | IsSuperUserOrIsAdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
