import arrow
from django.contrib.auth.models import User
from django.test import tag
from django.test import TestCase
from model_mommy import mommy
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Comment


@tag('cmnts')
class BoardMeetingViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password1')

        self.comment = mommy.make_recipe(
            'comments.comment', )

    def test_list(self):
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        comment_data = {'user': self.user1.id,
                        'comment_text': 'this is a comment',
                        'comment_type': 'general'}

        response = self.client.post('/comments/', comment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.filter(user=self.user1).exists())

    def test_retrieve(self):
        response = self.client.get(f'/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comment_text'], self.comment.comment_text)

    def test_update(self):
        comment_data = {'comment_text': 'This is an updated comment'}
        response = self.client.patch(f'/comments/{self.comment.id}/', comment_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.get(id=self.comment.id).comment_text, 'This is an updated comment')

    def test_delete(self):
        comment_obj = mommy.make_recipe('comments.comment')
        response = self.client.delete(f'/comments/{comment_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=comment_obj.id).exists())
