from math import e
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from non_citizen_profile.api.serializers import PersonalDetailsSerializer
from non_citizen_profile.models import PersonalDetails
from ..models import PrisonerReleaseLog


class GetReleaseLogProfilesView(APIView):

    def get(self, request, id):
        # Add query params to filter the profiles
        try:
            release_log = PrisonerReleaseLog.objects.get(id=id)
        except PrisonerReleaseLog.DoesNotExist:
            return Response(
                {"error": "Prisoner release log not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            prisoners = release_log.prisoners.all()
            profiles = []
            for prisoner in prisoners:
                try:
                    profile = PersonalDetails.objects.get(
                        non_citizen_identifier=prisoner.non_citizen_identifier
                    )
                    profiles.append(profile)
                except PersonalDetails.DoesNotExist:
                    continue
            serialized_profiles = PersonalDetailsSerializer(profiles, many=True)
            return Response(serialized_profiles.data)
