from rest_framework.serializers import ModelSerializer

from content.models import Comment, CommentResponse, Article, Author, Category, Topic, Section




class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','uid', 'day', "message", "profil"]

class CommentResponseSerializer(ModelSerializer):
    class Meta:
        model = CommentResponse
        fields = ['id', 'uid', 'day', "message", "profil"]


class EventSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'uid', "start_date", "end_date", "event_date", "event_adress", "event_type", "event_duration", "cover", "thumbnail"]


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'uid', "cover", "thumbnail", "content", "title", "second_title", "type", "support", "slug", "time_read", "date_publication", "author"]


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'uid', "about", "last_name", "photo", "facebook", "twitter", "instagram", "linkedin", "youtube", "website"]

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'cover', "uid", "description", "slug"]


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'cover', "uid", "description", "slug"]


class SectionSerializer(ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'name', 'cover', "uid", "description", "slug"]