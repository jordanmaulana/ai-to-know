from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from syllabus.editorial import document


class EditorialAPI(APIView):
    """The editorial bar, read by the public /about page.

    No serializer: the payload is static module constants assembled by
    `syllabus.editorial.document()`, so there is nothing to validate or coerce.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        return Response(document())
