from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
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
    queryset = Protocol.objects.all()
    serializer_class = ProtocolSerializer

    @detail_route(renderer_classes=(renderers.StaticHTMLRenderer,))
    def highlight(self, request, *args, **kwargs):
        protocol = self.get_object()
        return Response(protocol.highlighted)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profileinfo)

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This endpoint presents the users in the system.

    As you can see, the collection of snippet instances owned by a user are
    serialized using a hyperlinked representation.
    """
    queryset = ProfileInfo.objects.all()
    serializer_class = ProfileSerializer

class ProtocolStepViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This endpoint presents the steps in the system.

    As you can see, the collection of snippet instances owned by a user are
    serialized using a hyperlinked representation.
    """
    queryset = ProtocolStep.objects.all()
    serializer_class = ProtocolStepSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This endpoint presents the steps in the system.

    As you can see, the collection of snippet instances owned by a user are
    serialized using a hyperlinked representation.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ReagentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This endpoint presents the steps in the system.

    As you can see, the collection of snippet instances owned by a user are
    serialized using a hyperlinked representation.
    """
    queryset = Reagent.objects.all()
    serializer_class = ReagentSerializer
