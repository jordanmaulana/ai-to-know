from django.db.models import F, Q
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.serializers import SubjectDetailSerializer, SubjectListSerializer
from syllabus.models import Status, Subject


class SubjectAPI(APIView):
    """Public read access to the syllabus. Writing is done in Django admin."""

    permission_classes = [AllowAny]

    def get(self, request, slug=None):
        published = Subject.objects.filter(status=Status.PUBLISHED)

        if slug:
            subject = published.filter(slug=slug).first()
            if not subject:
                return Response({"detail": "Not found."}, status=404)
            return Response(SubjectDetailSerializer(subject).data)

        category = request.query_params.get("category")
        if category:
            published = published.filter(category=category)

        q = request.query_params.get("q")
        if q:
            published = published.filter(Q(title__icontains=q) | Q(one_liner__icontains=q))

        # Newest capability first; anything without a date sorts to the end on every backend.
        published = published.order_by(F("became_usable_on").desc(nulls_last=True), "title")
        return Response(SubjectListSerializer(published, many=True).data)
