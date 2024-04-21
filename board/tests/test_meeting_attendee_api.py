import arrow
from django.test import tag
from django.contrib.auth.models import User
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase
from ..models import MeetingAttendee


@tag('att')
class MeetingAttendeeAPITests(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='test_user',
            password='password123')

        self.board_meeting = mommy.make_recipe(
            'board.boardmeeting', )

        self.board_member = mommy.make_recipe(
            'board.boardmember', )

        self.meeting_attendee1 = mommy.make_recipe(
            'board.meetingattendee',
            meeting__id=self.board_meeting.id,
        )

        self.meeting_attendee2 = mommy.make_recipe(
            'board.meetingattendee',
            meeting__id=self.board_meeting.id)

    def test_get_meeting_attendees(self):
        url = reverse('board-meeting-attendees-list',
                      kwargs={'meeting': self.board_meeting.id})

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_meeting_attendees(self):
        url = reverse('meeting-attendee-create')
        data = {'meeting': self.board_meeting.id,
                'board_member': self.board_member.id}

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MeetingAttendee.objects.count(), 3)

    def test_get_meeting_attendee_detail(self):
        url = reverse('meeting-attendee-detail',
                      kwargs={'id': self.meeting_attendee1.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meeting'],
                         self.meeting_attendee1.meeting.id)
        self.assertEqual(response.data['board_member'],
                         self.meeting_attendee1.board_member.id)

    def test_update_meeting_attendee(self):
        url = reverse('meeting-attendee-update',
                      kwargs={'id': self.meeting_attendee1.id})

        data = {'meeting': self.board_meeting.id,
                'board_member': self.board_member.id,
                'attendance_status': 'present'}

        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.meeting_attendee1.refresh_from_db()
        self.assertEqual(self.meeting_attendee1.attendance_status, 'present')

