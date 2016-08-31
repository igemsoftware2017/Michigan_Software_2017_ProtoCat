from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

'''
The serializers at the top allow that field to have more in-depth info

"model =" allows a connection to a model from models.py
"fields = ()" shows the api-uploadable fields
"read_only_fields = ()" shows the api-viewable fields
'''

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('username', )

class ReagentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reagent
        fields = ('url', 'name', 'website', 'description', 'id')

class AlternateReagentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reagent
        fields = ('id',)

class ProtocolReagentSerializer(serializers.ModelSerializer):
    reagent_id = AlternateReagentSerializer(source='reagent')
    class Meta:
        model = ReagentForProtocol
        fields = ('scaling_type', 'reagent_type', 'amount', 'unit', 'number_in_step', 'significant_figures', 'display_name', 'preserve_units', 'reagent_id')

class ProtocolStepSerializer(serializers.ModelSerializer):
    reagents = ProtocolReagentSerializer(
        many = True,
        required = False,
        source = 'reagents_for_step')
    class Meta:
        model = ProtocolStep
        fields = ('step_number', 'title', 'time', 'action', 'warning', 'time_scaling', 'reagents')


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

class ProtocolCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolComment
        read_only_fields = ('author', 'protocol', 'upload_date', 'note')

class ProtocolRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolRating
        read_only_fields = ('person', 'score', 'protocol')

class ProtocolSerializer(serializers.HyperlinkedModelSerializer):
    protocol_steps = ProtocolStepSerializer(
        many = True,
        required = False,
        source = 'protocol_step')
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
        fields = ('url', 'protocol_steps', 'title', 'category', 'upload_date', 'description', 'materials', 'change_log', 'previous_revision', 'comments_for_protocol', 'ratings_for_protocol', 'id')
        read_only_fields = ('author', 'num_ratings', 'avg_rating', 'first_revision')

'''
{
    "protocol_steps": [
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
    "materials": "Thing",
    "change_log": "Initial commit",
    "previous_revision": null
}

{
    "protocol_steps": [
    {
        "step_number": 1,
        "title": "",
        "time": 10,
        "action": "Modified Step 1 <span class=\"reagent\" data-reagent-number=\"1\"></span> <span class=\"reagent\" data-reagent-number=\"2\"></span> <span class=\"reagent\" data-reagent-number=\"3\"></span>",
        "warning": "",
        "time_scaling": 1,
        "reagents": [
            {
                "scaling_type": 3,
                "reagent_type": 1,
                "amount": "0.0050000000000000000000000",
                "unit": "g",
                "number_in_step": 1,
                "significant_figures": 3,
                "display_name": null,
                "preserve_units": 1,
                "reagent_id": {
                    "id": 1
                }
            },
            {
                "scaling_type": 3,
                "reagent_type": 1,
                "amount": "1.0000000000000000000000000",
                "unit": "L",
                "number_in_step": 2,
                "significant_figures": 3,
                "display_name": null,
                "preserve_units": 1,
                "reagent_id": {
                    "id": 2
                }
            },
            {
                "scaling_type": 3,
                "reagent_type": 3,
                "amount": "1.0000000000000000000000000",
                "unit": "g",
                "number_in_step": 3,
                "significant_figures": 3,
                "display_name": null,
                "preserve_units": 1,
                "reagent_id": {
                    "id": 2
                }
            }
        ]
    },
    {
        "step_number": 2,
        "title": "",
        "time": 20,
        "action": "Original step 2 <span class=\"reagent\" data-reagent-number=\"1\"></span> <span class=\"reagent\" data-reagent-number=\"2\"></span>",
        "warning": "",
        "time_scaling": 2,
        "reagents": [
            {
                "scaling_type": 3,
                "reagent_type": 3,
                "amount": "1.0000000000000000000000000",
                "unit": "L",
                "number_in_step": 1,
                "significant_figures": 3,
                "display_name": null,
                "preserve_units": 1,
                "reagent_id": {
                    "id": 1
                }
            },
            {
                "scaling_type": 3,
                "reagent_type": 1,
                "amount": "1.0000000000000000000000000",
                "unit": "L",
                "number_in_step": 2,
                "significant_figures": 3,
                "display_name": null,
                "preserve_units": 1,
                "reagent_id": {
                    "id": 1
                }
            }
        ]
    },
    {
        "step_number": 3,
        "title": "",
        "time": 30,
        "action": "Original step 3 <span class=\"reagent\" data-reagent-number=\"1\"></span>",
        "warning": "",
        "time_scaling": 2,
        "reagents": [
            {
                "scaling_type": 3,
                "reagent_type": 1,
                "amount": "1.5000000000000000000000000",
                "unit": "L",
                "number_in_step": 1,
                "significant_figures": 3,
                "display_name": null,
                "preserve_units": 1,
                "reagent_id": {
                    "id": 2
                }
            }
        ]
    }
    ],
    "title": "Revision of 1st protocol",
    "category": 3,
    "description": "Another description",
    "materials": "",
    "change_log": "Made it better",
    "previous_revision": 1
}
'''
