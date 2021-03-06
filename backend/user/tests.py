from django.contrib.auth.models import User
from django.test import TestCase, Client
from user.models import User
from room.models import Room
import json

from datetime import datetime, timedelta


# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(email='minu@snu.ac.kr', password='1234', username='minu', name='Minwoo')
        user2 = User.objects.create_user(email='taebum@snu.ac.kr', password='1234', username='taebum', name='Taebum')
        current_date = datetime.now()

        room1 = Room.objects.create(name="room1",
                                    place="place1",
                                    time_span_start=current_date + timedelta(days=3),
                                    time_span_end=current_date + timedelta(days=6),
                                    min_time_required=None,
                                    owner=user1
                                    )

        room2 = Room.objects.create(name="room2",
                                    place="place2",
                                    time_span_start=current_date - timedelta(days=6),
                                    time_span_end=current_date - timedelta(days=3),
                                    min_time_required=None,
                                    owner=user2
                                    )
        room1.members.add(user1)
        room1.members.add(user2)
        room2.members.add(user1)
        room2.members.add(user2)

        self.client = Client(enforce_csrf_checks=True)

    def test_signup_post(self):
        response = self.client.post('/api/signup',
                                    json.dumps({'email': 'dongsu@snu.ac.kr',
                                                'username': 'dongsu',
                                                'password': '1234',
                                                'name': 'Dongsu'}),
                                    content_type='application/json',
                                    )
        self.assertEqual(response.status_code, 201)

    def test_signup_invalid_methods(self):
        response = self.client.get('/api/signup')
        self.assertEqual(response.status_code, 405)

        response = self.client.put('/api/signup',
                                   json.dumps({'email': 'test@snu.ac.kr',
                                               'username': 'test',
                                               'password': 'hello',
                                               'name': 'Test'}),
                                   content_type='application/json',
                                   )
        self.assertEqual(response.status_code, 405)

        response = self.client.delete('/api/signup',
                                      json.dumps({'email': 'test@snu.ac.kr',
                                                  'username': 'test',
                                                  'password': 'hello',
                                                  'name': 'Test'}),
                                      content_type='application/json',
                                      )
        self.assertEqual(response.status_code, 405)

    def test_signin_post_by_email(self):
        response = self.client.post('/api/signin',
                                    json.dumps({'email': 'minu@snu.ac.kr', 'password': '1234'}),
                                    content_type='application/json',
                                    )
        self.assertEqual(response.status_code, 200)

    def test_signin_post_by_username(self):
        response = self.client.post('/api/signin',
                                    json.dumps({'username': 'minu', 'password': '1234'}),
                                    content_type='application/json',
                                    )
        self.assertEqual(response.status_code, 200)

    def test_signin_post_by_email_fail(self):
        response = self.client.post('/api/signin',
                                    json.dumps({'email': 'philsik@snu.ac.kr', 'password': '1234'}),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 401)

    def test_signin_post_by_username_fail(self):
        response = self.client.post('/api/signin',
                                    json.dumps({'username': 'philsik', 'password': '1234'}),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 401)

    def test_signin_invalid_methods(self):
        response = self.client.get('/api/signin')
        self.assertEqual(response.status_code, 405)

        response = self.client.put('/api/signin',
                                   json.dumps({'email': 'test@snu.ac.kr', 'password': 'hello'}),
                                   content_type='application/json',
                                   )
        self.assertEqual(response.status_code, 405)

        response = self.client.delete('/api/signin',
                                      json.dumps({'email': 'test@snu.ac.kr', 'password': 'hello'}),
                                      content_type='application/json',
                                      )
        self.assertEqual(response.status_code, 405)

    def test_signin_nonuser_post(self):
        response = self.client.post('/api/signin/non-user',
                                    json.dumps({'name': 'minwoo'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_signin_nonuser_invalid_methods(self):
        response = self.client.get('/api/signin/non-user')
        self.assertEqual(response.status_code, 405)

        response = self.client.put('/api/signin/non-user',
                                    json.dumps({'name': 'minwoo'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 405)

        response = self.client.delete('/api/signin/non-user')
        self.assertEqual(response.status_code, 405)

    def test_signout_get(self):
        self.client.login(email='minu@snu.ac.kr', password='1234')

        response = self.client.get('/api/signout')
        self.assertEqual(response.status_code, 200)

    def test_signout_get_unauth(self):
        response = self.client.get('/api/signout')
        self.assertEqual(response.status_code, 401)

    def test_signout_invalid_methods(self):
        response = self.client.post('/api/signin',
                                    json.dumps({'email': 'minu@snu.ac.kr', 'password': '1234'}),
                                    content_type='application/json',
                                    )
        csrftoken = response.cookies['csrftoken'].value

        response = self.client.post('/api/signout',
                                    json.dumps({'email': 'invalid@snu.ac.kr', 'password': 'invalid'}),
                                    content_type='application/json',
                                    HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)

        response = self.client.put('/api/signout',
                                   json.dumps({'email': 'invalid@snu.ac.kr', 'password': 'invalid'}),
                                   content_type='application/json',
                                   HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)

        response = self.client.delete('/api/signout',
                                      json.dumps({'email': 'invalid@snu.ac.kr', 'password': 'invalid'}),
                                      content_type='application/json',
                                      HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)

    def test_user_detail_unauth(self):
        response = self.client.post('/api/signin',
                                    json.dumps({'email': 'dongsu@snu.ac.kr', 'password': '1234'}),
                                    content_type='application/json',
                                    )
        csrftoken = response.cookies['csrftoken'].value

        response = self.client.get('/api/user')
        self.assertEqual(response.status_code, 401)  # Unauthorized

        response = self.client.put('/api/user', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 401)

        response = self.client.delete('/api/user', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 401)

    def test_user_detail_get(self):
        self.client.login(email='minu@snu.ac.kr', password='1234')

        response = self.client.get('/api/user')

        data = json.loads(response.content.decode())
        self.assertEqual(data['email'], 'minu@snu.ac.kr')
        self.assertEqual(response.status_code, 200)

    def test_user_detail_post(self):
        response = self.client.post('/api/signin',
                                    json.dumps({'email': 'minu@snu.ac.kr', 'password': '1234'}),
                                    content_type='application/json',
                                    )
        csrftoken = response.cookies['csrftoken'].value

        response = self.client.post('/api/user',
                                    json.dumps({'password': '123456'}),
                                    content_type='application/json',
                                    HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)  # Not allowed method

    def test_user_detail_put(self):
        response = self.client.post('/api/signin',
                                    json.dumps({'email': 'minu@snu.ac.kr', 'password': '1234'}),
                                    content_type='application/json',
                                    )
        csrftoken = response.cookies['csrftoken'].value

        response = self.client.put('/api/user',
                                   json.dumps({'password': '123456', 'name': 'Name'}),
                                   content_type='application/json',
                                   HTTP_X_CSRFTOKEN=csrftoken)

        self.assertTrue(User.objects.get(id=1).check_password('123456'))
        self.assertEqual(response.status_code, 204)

    def test_user_detail_delete(self):
        response = self.client.post('/api/signin',
                                    json.dumps({'email': 'minu@snu.ac.kr', 'password': '1234'}),
                                    content_type='application/json',
                                    )
        csrftoken = response.cookies['csrftoken'].value

        response = self.client.delete('/api/user', HTTP_X_CSRFTOKEN=csrftoken)

        self.assertRaises(User.DoesNotExist, User.objects.get, id=1)
        self.assertEqual(response.status_code, 204)

    def test_user_owned_room_list_unauth(self):
        response = self.client.get('/api/user/owned-rooms')
        self.assertEqual(response.status_code, 401)  # Unauthorized

    def test_user_owned_room_list_get(self):
        self.client.login(email='minu@snu.ac.kr', password='1234')
        response = self.client.get('/api/user/owned-rooms')

        data = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(len([room for room in data if room['owner'] == 1]), 1)

    def test_user_owned_room_list_invalid_methods(self):
        response = self.client.post('/api/signin',
                                    json.dumps({'email': 'minu@snu.ac.kr', 'password': '1234'}),
                                    content_type='application/json',
                                    )
        csrftoken = response.cookies['csrftoken'].value

        response = self.client.post('/api/user/owned-rooms',
                                    json.dumps({'email': 'invalid@snu.ac.kr', 'password': 'invalid'}),
                                    content_type='application/json',
                                    HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)

        response = self.client.put('/api/user/owned-rooms',
                                   json.dumps({'email': 'invalid@snu.ac.kr', 'password': 'invalid'}),
                                   content_type='application/json',
                                   HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)

        response = self.client.delete('/api/user/owned-rooms',
                                      json.dumps({'email': 'invalid@snu.ac.kr', 'password': 'invalid'}),
                                      content_type='application/json',
                                      HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)

    def test_user_joined_room_past_unauth(self):
        response = self.client.get('/api/user/joined-rooms/past')
        self.assertEqual(response.status_code, 401)  # Unauthorized

    def test_user_joined_room_past_get(self):
        self.client.login(email='minu@snu.ac.kr', password='1234')
        response = self.client.get('/api/user/joined-rooms/past')

        data = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)

    def test_user_joined_room_past_invalid_methods(self):
        response = self.client.post('/api/signin',
                                    json.dumps({'email': 'minu@snu.ac.kr', 'password': '1234'}),
                                    content_type='application/json',
                                    )
        csrftoken = response.cookies['csrftoken'].value

        response = self.client.post('/api/user/joined-rooms/past',
                                    json.dumps({'email': 'invalid@snu.ac.kr', 'password': 'invalid'}),
                                    content_type='application/json',
                                    HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)

        response = self.client.put('/api/user/joined-rooms/past',
                                   json.dumps({'email': 'invalid@snu.ac.kr', 'password': 'invalid'}),
                                   content_type='application/json',
                                   HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)

        response = self.client.delete('/api/user/joined-rooms/past',
                                      json.dumps({'email': 'invalid@snu.ac.kr', 'password': 'invalid'}),
                                      content_type='application/json',
                                      HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)

    def test_user_joined_room_list_unauth(self):
        response = self.client.get('/api/user/joined-rooms')
        self.assertEqual(response.status_code, 401)  # Unauthorized

    def test_user_joined_room_list_get(self):
        self.client.login(email='minu@snu.ac.kr', password='1234')
        response = self.client.get('/api/user/joined-rooms')

        data = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)

    def test_user_joined_room_list_invalid_methods(self):
        response = self.client.post('/api/signin',
                                    json.dumps({'email': 'minu@snu.ac.kr', 'password': '1234'}),
                                    content_type='application/json',
                                    )
        csrftoken = response.cookies['csrftoken'].value

        response = self.client.post('/api/user/joined-rooms',
                                    json.dumps({'email': 'invalid@snu.ac.kr', 'password': 'invalid'}),
                                    content_type='application/json',
                                    HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)

        response = self.client.put('/api/user/joined-rooms',
                                   json.dumps({'email': 'invalid@snu.ac.kr', 'password': 'invalid'}),
                                   content_type='application/json',
                                   HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)

        response = self.client.delete('/api/user/joined-rooms',
                                      json.dumps({'email': 'invalid@snu.ac.kr', 'password': 'invalid'}),
                                      content_type='application/json',
                                      HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)

    # endregion

    # region test models.py
    def test_create_superuser(self):
        superuser = User.objects.create_superuser(email='superman@snu.ac.kr',
                                                  password='super',
                                                  username='root',
                                                  name='Root')

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_superuser_fail(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='superman@snu.ac.kr', password='super', username='root', is_staff=False)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='superman@snu.ac.kr', password='super', username='root',
                                          is_superuser=False)

    def test_create_user_no_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password='1234', username='null', name='Test')

    def test_create_user_no_password(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='philsik@snu.ac.kr', password=None, username='philsik', name='Philsik')

    def test_create_user_no_username(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='philsik@snu.ac.kr', password='1234', username=None, name='Philsik')

    def test_create_user_no_name(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='philsik@snu.ac.kr', password='1234', username='philsik', name=None)

    def test_check_password_not_logged_in(self):
        # login and logout to get csrftoken
        response = self.client.post('/api/signin',
                                    json.dumps({'email': 'minu@snu.ac.kr', 'password': '1234'}),
                                    content_type='application/json',
                                    )
        csrftoken = response.cookies['csrftoken'].value
        response = self.client.get('/api/signout')
        response = self.client.post('/api/user/check-password',
                                    json.dumps({'password': '1234'}),
                                    content_type='application/json',
                                    HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 401)

    def test_check_password_right_password(self):
        response = self.client.post('/api/signin',
                                    json.dumps({'email': 'minu@snu.ac.kr', 'password': '1234'}),
                                    content_type='application/json',
                                    )
        csrftoken = response.cookies['csrftoken'].value
        response = self.client.post('/api/user/check-password',
                                    json.dumps({'password': '1234'}),
                                    content_type='application/json',
                                    HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())
        self.assertEqual(data, True)

    def test_check_password_wrong_password(self):
        response = self.client.post('/api/signin',
                                    json.dumps({'email': 'minu@snu.ac.kr', 'password': '1234'}),
                                    content_type='application/json',
                                    )
        csrftoken = response.cookies['csrftoken'].value

        response = self.client.post('/api/user/check-password',
                                    json.dumps({'password': 'wrong password'}),
                                    content_type='application/json',
                                    HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())
        self.assertEqual(data, False)

    def test_check_password_put_password(self):
        response = self.client.post('/api/signin',
                                    json.dumps({'email': 'minu@snu.ac.kr', 'password': '1234'}),
                                    content_type='application/json',
                                    )
        csrftoken = response.cookies['csrftoken'].value

        response = self.client.put('/api/user/check-password',
                                   json.dumps({'password': '1234'}),
                                   content_type='application/json',
                                   HTTP_X_CSRFTOKEN=csrftoken
                                   )
        self.assertEqual(response.status_code, 405)

        #  endregion
