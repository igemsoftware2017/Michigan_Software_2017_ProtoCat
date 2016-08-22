from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import permissions
from .permissions import *
from .models import *
from .serializers import *
import bleach


class ProtocolViewSet(viewsets.ModelViewSet):
    """
    This endpoint presents the stored protocols.

    Here you can only POST new protocols if you are logged in. Otherwise,
    you can GET the information for all protocols by doing a GET request
    to /api/protocol/ or for a specific protocol by doing a GET request to
    /api/protocol/{id}. The GET requests return the main information posted by
    the original poster as well as the individual ratings and comments to show
    alongside the protocol.

    When you POST a new protocol, you only need to submit the title, description,
    change log, materials, protocol steps, and the id of the previous revision
    (null if it is not a revision) in the JSON format to /api/protocol/. The way
    to format the protocol steps is to have the protocol_steps be an array of
    steps, each with their own step number, time (in seconds) to complete the step,
    (-1 if untimed), the action, any warnings, and if the time scales (1 means no
    scaling, 2 means linear scaling).

    To authenticate the user, you must first submit a POST to /api/token/ with
    the username and password. This will send you a token in the header which
    you can send with every request that needs authentication.
    """
    permission_classes = (IsAuthenticatedOrReadOnlyPUTDisallowed,)
    queryset = Protocol.objects.all()
    serializer_class = ProtocolSerializer

    def create(self, request):
        try:
            protocol = Protocol()
            print(request.data)
            protocol.title = request.data['title']
            protocol.category = Category.objects.get(id = request.data['category'])
            protocol.description = bleach.clean(request.data['description'])
            protocol.change_log = bleach.clean(request.data['change_log'])
            if (request.data['previous_revision'] != None and request.data['previous_revision'] != "-1"):
                protocol.previous_revision = Protocol.objects.get(id = request.data['previous_revision'])
            protocol.author = request.user.profileinfo
            protocol.materials = request.data['materials']
            step_list = []
            print('Main protocol finished')
            for step in request.data['protocol_steps']:
                protocol_step = ProtocolStep()
                if (step['title'] != "" and step['title'] != None):
                    protocol_step.title = step['title']
                protocol_step.step_number = step['step_number']
                if (step['time'] != None):
                    protocol_step.time = int(step['time'])
                protocol_step.action = bleach.clean(step['action'])
                if (step['warning'] != ""):
                    protocol_step.warning = bleach.clean(step['warning'])
                protocol_step.time_scaling = int(step['time_scaling'])
                step_list.append(protocol_step)
            protocol.save()
            for step in step_list:
                step.protocol = protocol
                step.save()
<<<<<<< HEAD
            print(request.data['materials'])
            return Response({'success': True, 'location': '/protocol/' + str(protocol.id)})
=======

            return Response({'success': True})
>>>>>>> 29056a342a44e1b978ed72ef536fcfe32ca135b7
        except Exception as inst:
            print(inst)
            return Response({'success': False, 'error': str(inst)})

class ProfileViewSet(viewsets.ModelViewSet):
    """
    This endpoint presents our user system.

    Here you can view the public information of any user, such as the username,
    list of protocols they made, and other basic info. You can only PUT
    information to the account you are logged in with, but you can always GET
    others' basic information.

    To authenticate the user, you must first submit a POST to /api/token/ with
    the username and password. This will send you a token in the header which
    you can send with every request that needs authentication.
    """
    permission_classes = (IsUserOrReadOnly,)
    http_method_names = ['get', 'options', 'head', 'put']
    queryset = ProfileInfo.objects.all()
    serializer_class = ProfileSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    This endpoint shows our category system.

    Here, you can POST new categories if you are logged in, otherwise you can
    view the current categories and infomation about them. If you are POSTing a
    new category, be sure to link it to a parent category by id or keep the
    value as null if you do not want a parent category.

    To authenticate the user, you must first submit a POST to /api/token/ with
    the username and password. This will send you a token in the header which
    you can send with every request that needs authentication.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsReadOnlyOrAuthenticated,)

    def create(self, request):
        try:
            print(request.data)
            category = Category()
            category.title = request.data['title']
            category.description = request.data['description']
            if (request.data['parent_category'] != None):
                category.parent_category = Category.objects.get(id = request.data['parent_category'])
            category.author = request.user.profileinfo
            category.save()
            return Response({'status': 'Saved category'})
        except Exception as inst:
            print(inst)
            return Response({'status': 'failed'})

class ReagentViewSet(viewsets.ModelViewSet):
    """
    This endpoint presents the available reagents in the system.

    Here, you can POST new reagents if you are logged in, otherwise you can
    view our current catalog and infomation about them.

    To authenticate the user, you must first submit a POST to /api/token/ with
    the username and password. This will send you a token in the header which
    you can send with every request that needs authentication.
    """
    permission_classes = (IsReadOnlyOrAuthenticated,)
    queryset = Reagent.objects.all()
    serializer_class = ReagentSerializer
