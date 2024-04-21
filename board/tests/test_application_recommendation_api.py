import arrow
from django.contrib.auth.models import User
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase
from ..models import BoardDecision


class BoardMeetingAPITests(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='test_user',
            password='password123')

        self.board_decision1 = mommy.make_recipe(
            'board.boardmeeting',)

        self.board_decision2 = mommy.make_recipe(
            'board.boarddecision', )

        self.board_meeting = mommy.make_recipe(
            'board.boardmeeting', )

        self.assessed_application = mommy.make_recipe(
            'board.application', )

    def test_get_board_decisions(self):
        url = reverse('application-recommendations-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # def test_create_application_recommendations(self):
    #     url = reverse('application-recommendation-create')
    #     data = {'board_meeting': self.board_meeting.id,
    #             'assessed_application': self.assessed_application.id,
    #             'decision_datetime': arrow.utcnow().datetime,
    #             'final_decision': 'approved'}
    #
    #     self.client.force_authenticate(user=self.user)
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(BoardDecision.objects.count(), 3)
    #
    # def test_get_application_recommendation_detail(self):
    #     url = reverse('application-recommendation-detail',
    #                   kwargs={'id': self.app_recommendation1.id})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['board_meeting'],
    #                      self.app_recommendation1.board_meeting.id)
    #     self.assertEqual(response.data['final_decision'],
    #                      self.app_recommendation1.final_decision)
    #
    # def test_update_application_recommendation(self):
    #     url = reverse('application-recommendation-update',
    #                   kwargs={'id': self.app_recommendation1.id})
    #
    #     data = {'board_meeting': self.board_meeting.id,
    #             'assessed_application': self.assessed_application.id,
    #             'decision_datetime': arrow.utcnow().datetime,
    #             'final_decision': 'rejected'}
    #
    #     self.client.force_authenticate(user=self.user)
    #     response = self.client.put(url, data)
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.app_recommendation1.refresh_from_db()
    #     self.assertEqual(self.app_recommendation1.final_decision, 'rejected')
    #

    # def test_delete_application_recommendation(self):
    #     url = reverse('application-recommendation-delete',
    #                   kwargs={'id': self.assessed_application.id})
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(ApplicationDecision.objects.count(), 1)
