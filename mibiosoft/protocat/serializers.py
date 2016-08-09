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
    protocols = serializers.HyperlinkedRelatedField(
        view_name='protocol-detail',
        many=True,
        read_only=True,)

    class Meta:
        model = ProfileInfo
        fields = ('url', 'user', 'protocols', 'about', 'contact_info')
        read_only_fields = ('profile_image', 'meows')

class CategorySerializer(serializers.ModelSerializer):
    protocol_for_category = serializers.HyperlinkedRelatedField(
        view_name='protocol-detail',
        many=True,
        read_only=True,)

    class Meta:
        model = Category
        fields = ('url', 'title', 'description', 'upload_date', 'id', 'protocol_for_category', 'parent_category')
        read_only_fields = ('author',)

class TextReagentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextReagent
        fields = ('reagents', )

class ProtocolCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolComment
        read_only_fields = ('author', 'protocol', 'upload_date', 'note')

class ProtocolRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolRating
        read_only_fields = ('person', 'score', 'protocol')

class ProtocolSerializer(serializers.HyperlinkedModelSerializer):
    protocol_step = ProtocolStepSerializer(
        many = True,
        required = False)
    textreagent = TextReagentSerializer(
        required = False
    )
    comments_for_protocol = ProtocolCommentSerializer(
        many = True,
        read_only=True,
        required = False)
    ratings_for_protocol = ProtocolRatingSerializer(
        many = True,
        read_only=True,
        required = False)

    class Meta:
        model = Protocol
        fields = ('protocol_step', 'title', 'category', 'upload_date', 'description', 'textreagent', 'change_log', 'previous_revision', 'comments_for_protocol', 'ratings_for_protocol', 'id')
        read_only_fields = ('author', 'num_ratings', 'avg_rating', 'first_revision')





class ReagentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reagent
        fields = ('url', 'name', 'website', 'picture', 'id')

'''
{
    "protocol_step": [
        {
            "step_number": 1,
            "time": -1,
            "action": "Original first step",
            "warning": "",
            "time_scaling": 2
        },
        {
            "step_number": 2,
            "time": 50,
            "action": "Original step 2",
            "warning": "",
            "time_scaling": 1
        },
        {
            "step_number": 3,
            "time": 40,
            "action": "Original step 3",
            "warning": "",
            "time_scaling": 2
        }
    ],
    "title": "First Protocol",
    "category": "1",
    "description": "This is a protocol",
    "textreagent": {
        "reagents": "Thing"
    },
    "change_log": "Initial commit",
    "previous_revision": null
}
'''
