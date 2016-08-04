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
        print(request.data['textreagent']['reagents'])
        serializer = ProtocolSerializer(data = request.data, context={'request': request})
        print(request.data)
        if serializer.is_valid():
            title = serializer.data['title']
            author = serializer.data['author']
            category = serializer.data['category']
            description = serializer.data['description']
            change_log = serializer.data['change_log']
            protocol = Protocol(title = title, author = author, category = category, description = description, change_log = change_log)
            protocol.save()
            return Response({'status': 'saved_protocol'})
        else:
            return Response({'status': 'failed'})


class ProfileViewSet(viewsets.ModelViewSet):
    """
    This endpoint presents the users in the system.

    As you can see, the collection of snippet instances owned by a user are
    serialized using a hyperlinked representation.
    """
    permission_classes = (IsUserOrReadOnly,)

    queryset = ProfileInfo.objects.all()
    serializer_class = ProfileSerializer

class ProtocolStepViewSet(viewsets.ModelViewSet):
    """
    This endpoint presents the steps in the system.

    As you can see, the collection of snippet instances owned by a user are
    serialized using a hyperlinked representation.
    """

    permission_classes = (IsAuthenticatedOrReadOnlyPUTDisallowed)
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

    def create(self, request):
        print(request.data)
        print(request.data['title'])
        serializer = CategorySerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            print(serializer.data)
            title = serializer.data['title']
            author = serializer.data['author']
            category = serializer.data['category']
            description = serializer.data['description']
            category = Category(title = title, author = author, parent_category = category, description = description)
            category.save()
            return Response({'status': 'saved_protocol'})
        else:
            return Response({'status': 'failed'})

class ReagentViewSet(viewsets.ModelViewSet):
    """
    This endpoint presents the available reagents in the system.

    The collection of every reagent we have in the database.
    """
    queryset = Reagent.objects.all()
    serializer_class = ReagentSerializer
