from rest_framework import authentication, viewsets, mixins, permissions
from .serializers import FileSerializer
from rest_framework import status
from rest_framework.parsers import FileUploadParser, MultiPartParser
from core.models import File
from django.http import HttpResponse

from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from core.utils import token_required
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema, OpenApiParameter

# Create your views here.

@extend_schema(
    request=None,
    responses=None,
    parameters=[
        OpenApiParameter(
            name='token',
            location=OpenApiParameter.QUERY,
            description='Auth Token',
            required=True, type=str),
    ],
    description="""
    Open the file onlick of a secured link.
    eg., http:127.0.0.1:8000/media/hello.pdf?token=8e5a455adc4ebac9d26f7ccf6e9c599a332c3c83
    """
)
@api_view(["GET"])
@token_required
def secure_file_media(request, auth_user, file):
    try:
        file = File.objects.get(file=file)
        response = FileResponse(file.file)
    except Exception as e:
        return HttpResponse("404: File Not Found")
    return response


class FileViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin
):
    """
    A viewset for LISTING all files, UPLOADING a file,
    and DOWNLOADING a specific file using file id.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]
    serializer_class = FileSerializer
    queryset = File.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """
        Downloading a specific file using file id.
        """

        file = self.get_object()

        file_name = file.file.name

        response = HttpResponse(file.file, content_type='multipart/form-data')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
