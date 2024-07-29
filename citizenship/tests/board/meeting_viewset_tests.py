from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from citizenship.management.factory.factories import BoardFactory, UserFactory, RoleFactory, BoardMemberFactory
from citizenship.models import Meeting, BoardMember


class MeetingViewSetTests(APITestCase):

    def setUp(self):
        self.board = BoardFactory()
        self.meeting_data = {
            'title': 'Board Meeting',
            'date': '2024-01-01',
            'time': '10:00:00',
            'location': 'Board Room',
            'agenda': 'Discuss yearly goals',
            'board': self.board.id,
            'status': 'Scheduled',
            'start_date': '2024-01-01T10:00:00Z',
            'end_date': '2024-01-01T11:00:00Z'
        }
        self.user = UserFactory()
        self.role = RoleFactory()
        self.board_member = BoardMemberFactory(user=self.user, board=self.board, role=self.role)

    def test_create_meeting(self):
        url = reverse('meeting-list')
        response = self.client.post(url, self.meeting_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.meeting_data['title'])

    # def test_add_attendee(self):
    #     meeting = MeetingFactory(board=self.board)
    #     url = reverse('meeting-add-attendee', args=[meeting.id])
    #     data = {'member_id': self.board_member.id, 'confirmed': True}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['member']['id'], self.board_member.id)
    #     self.assertTrue(BoardMember.objects.filter(id=self.board_member.id).exists())
    #
    # def test_remove_attendee(self):
    #     meeting = MeetingFactory(board=self.board)
    #     # First add an attendee to ensure it exists
    #     MeetingService.add_attendee(meeting.id, self.board_member.id, True)
    #     url = reverse('meeting-remove-attendee', args=[meeting.id])
    #     data = {'member_id': self.board_member.id}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #
    # def test_change_status(self):
    #     meeting = MeetingFactory(board=self.board)
    #     url = reverse('meeting-change-status', args=[meeting.id])
    #     data = {'status': 'Completed'}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['status'], 'Completed')
    #
    # def test_confirm_attendance(self):
    #     meeting = MeetingFactory(board=self.board)
    #     MeetingService.add_attendee(meeting.id, self.board_member.id, False)
    #     url = reverse('meeting-confirm-attendance', args=[meeting.id])
    #     data = {'member_id': self.board_member.id}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['member']['id'], self.board_member.id)
    #     self.assertTrue(BoardMember.objects.get(id=self.board_member.id).confirmed)