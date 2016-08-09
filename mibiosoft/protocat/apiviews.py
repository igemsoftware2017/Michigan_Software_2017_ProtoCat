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


class ProtocolViewSet(viewsets.ModelViewSet):
    """
    This endpoint presents code snippets.

    The `highlight` field presents a hyperlink to the highlighted HTML
    representation of the code snippet.

    The **owner** of the code snippet may update or delete instances
    of the code snippet.

    Try it yourself by logging in as one of these four users: **amy**, **max**,
    **jose** or **aziz**.  The passwords are the same as the usernames.
    """
    permission_classes = (IsAuthenticatedOrReadOnlyPUTDisallowed,)

    queryset = Protocol.objects.all()
    serializer_class = ProtocolSerializer

    def create(self, request):
        try:
            protocol = Protocol()
            protocol.title = request.data['title']
            protocol.category = Category.objects.get(id = request.data['category'])
            protocol.description = request.data['description']
            protocol.change_log = request.data['change_log']
            if (request.data['previous_revision'] != None):
                protocol.previous_revision = Protocol.objects.get(id = request.data['previous_revision'])
            protocol.author = request.user.profileinfo
            step_list = []
            print('Main protocol finished')
            for step in request.data['protocol_step']:
                protocol_step = ProtocolStep()
                protocol_step.step_number = step['step_number']
                protocol_step.time = int(step['time'])
                protocol_step.action = step['action']
                protocol_step.warning = step['warning']
                protocol_step.time_scaling = int(step['time_scaling'])
                step_list.append(protocol_step)
            protocol.save()
            for step in step_list:
                step.protocol = protocol
                step.save()
            print(request.data['textreagent']['reagents'])
            return Response({'status': 'saved_protocol'})
        except Exception as inst:
            print(inst)
            return Response({'status': 'failed'})


class ProfileViewSet(viewsets.ModelViewSet):
    """
    This endpoint presents the users in the system.

    As you can see, the collection of snippet instances owned by a user are
    serialized using a hyperlinked representation.
    """
    permission_classes = (IsUserOrReadOnly,)
    http_method_names = ['get', 'options', 'head', 'put']
    queryset = ProfileInfo.objects.all()
    serializer_class = ProfileSerializer

class ProtocolStepViewSet(viewsets.ModelViewSet):
    """
    This endpoint presents the steps in the system.

    As you can see, the collection of snippet instances owned by a user are
    serialized using a hyperlinked representation.
    """

    permission_classes = (IsReadOnly,)
    http_method_names = ['get', 'options', 'head']
    queryset = ProtocolStep.objects.all()
    serializer_class = ProtocolStepSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    This endpoint presents the steps in the system.

    As you can see, the collection of snippet instances owned by a user are
    serialized using a hyperlinked representation.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)

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

    The collection of every reagent we have in the database.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Reagent.objects.all()
    serializer_class = ReagentSerializer
