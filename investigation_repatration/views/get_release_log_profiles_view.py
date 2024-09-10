from rest_framework.response import Response
from rest_framework.views import APIView

from app_personal_details.api.serializers import PersonSerializer
from app_personal_details.models import Person

from ..models import PrisonerReleaseLog


class GetReleaseLogProfilesView(APIView):

    def get(self, request, id):
        release_log = PrisonerReleaseLog.objects.get(id=id)
        prisoners = release_log.prisoners
        profiles = []
        for prisoner in prisoners:
            try:
                profile = Person.objects.get(
                    non_citizen_identifier=prisoner.non_citizen_identifier
                )
                profiles.append(profile)
            except Person.DoesNotExist:
                continue
        serialized_profiles = PersonSerializer(profiles, many=True)
        return Response(serialized_profiles.data)
