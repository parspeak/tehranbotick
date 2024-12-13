from medias.models import Image
from medias.serializers import ImageSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.
class ImageListView(ListAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser, )


class ImageCreateView(CreateAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser, )
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(created_by_id=self.request.user.id, last_modified_by_id=self.request.user.id)


class ImageDeleteView(DestroyAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser, )
    lookup_url_kwarg = 'pk'


class ImageUpdateView(UpdateAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser, )
    lookup_url_kwarg = 'pk'

    def perform_update(self, serializer):
        serializer.save(last_modified_by_id=self.request.user.id)


class ImageRetrieveView(RetrieveAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser, )
    lookup_url_kwarg = 'pk'
