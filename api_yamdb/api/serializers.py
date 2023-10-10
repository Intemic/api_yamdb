import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.constants import FIELD_LENGTH, USERNAME_PATTERN
from core.validators import current_year
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class Validatemixin:
    def validate_username(self, username):

        result = set(re.sub(USERNAME_PATTERN, '', username))
        if result:
            raise serializers.ValidationError(
                f'недопустимые символы: {"".join(result)}'
            )
        if username.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        return username


class UserCreateSerializer(Validatemixin, serializers.Serializer):
    """Сериализатор создает объект класса User."""

    username = serializers.CharField(max_length=FIELD_LENGTH['NAME'])
    email = serializers.EmailField(max_length=FIELD_LENGTH['EMAIL'])

    def validate(self, data):
        user_by_name = User.objects.filter(
            username=data.get('username')).first()
        user_by_email = User.objects.filter(email=data.get('email')).first()
        if user_by_name != user_by_email:
            if user_by_name:
                raise serializers.ValidationError(
                    'Пользователь с таким username уже существует'
                )
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return data

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(**validated_data)
        return user


class UserTokenReceiveSerializer(Validatemixin, serializers.Serializer):
    """Сериализатор для класса User и получения JWT токена"""
    username = serializers.CharField(max_length=FIELD_LENGTH['NAME'],
                                     required=True
                                     )
    confirmation_code = serializers.CharField(
        max_length=FIELD_LENGTH['NAME'],
        required=True
    )

    class Meta:
        model = User
        fields = (
            'username', 'confirmation_code'
        )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""
    class Meta:
        model = User
        unique_together = ('name', 'email')
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

        def validate(self, username):
            if username in 'me':
                raise serializers.ValidationError(
                    'Запрещено использовать имя me'
                )
            return username


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=FIELD_LENGTH['SLUG'],
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=FIELD_LENGTH['SLUG'],
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        read_only_fields = ('review',)
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        read_only_fields = ('title',)
        fields = '__all__'
        model = Review

    def validate(self, value):
        if self.context['request'].method == 'POST':
            author = self.context['request'].user
            title_id = (self.context['request'].
                        parser_context['kwargs'].get('title_id'))
            if Review.objects.filter(title=title_id, author=author).exists():
                raise serializers.ValidationError(
                    'Отзыв на произведение уже существует'
                )
        return value


class TitleCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        min_length=1,
        max_length=FIELD_LENGTH['MAX_SIZE']
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )

    def validate_year(self, data):
        # так понимаю произведения до нашей эры тоже учитываются
        if data > current_year():
            raise serializers.ValidationError('Не допустимый год.')

        return data

    def to_representation(self, instance):
        return TitleSerializer(instance).data


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(
        many=True,
    )
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
