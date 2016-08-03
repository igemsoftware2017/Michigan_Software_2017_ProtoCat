from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.ReadOnlyField()
    class Meta:
        model = User
        fields = ('username', )

class ProtocolStepSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProtocolStep
        fields = ('url', 'step_number', 'time', 'action', 'warning', 'time_scaling')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    protocols = serializers.HyperlinkedRelatedField(queryset=Protocol.objects.all(), view_name='protocol-detail', many=True)

    class Meta:
        model = ProfileInfo
        fields = ('url', 'user', 'protocols', 'profile_image', 'about', 'contact_info', 'meows')
        depth = 1

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    author = ProfileSerializer()
    parent_category = serializers.HyperlinkedRelatedField(queryset=Category.objects.all(), view_name='category-detail', required = False)

    class Meta:
        model = Category
        fields = ('url', 'title', 'author', 'description', 'upload_date', 'parent_category')

class TextReagentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextReagent
        fields = ('reagents', )

class ProtocolCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolComment
        fields = ('author', 'protocol', 'upload_date', 'note')

class ProtocolRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolRating
        fields = ('person', 'score', 'protocol')

class ProtocolSerializer(serializers.HyperlinkedModelSerializer):
    author = ProfileSerializer()
    protocol_step = ProtocolStepSerializer(many = True)
    textreagent = TextReagentSerializer()
    comments_for_protocol = ProtocolCommentSerializer(many = True)
    ratings_for_protocol = ProtocolRatingSerializer(many = True)

    class Meta:
        model = Protocol
        fields = ('url', 'title', 'author', 'protocol_step', 'category', 'num_ratings', 'avg_rating', 'upload_date', 'change_log', 'description', 'previous_revision', 'first_revision', 'textreagent', 'comments_for_protocol', 'ratings_for_protocol')


class ReagentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reagent
        fields = ('url', 'name', 'website', 'picture')
