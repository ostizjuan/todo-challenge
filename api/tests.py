import json

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Task


class TaskTestCase(APITestCase):

    def setUp(self):
        self.user = User(
            email='',
            username='UserTest',
        )
        self.user.set_password('1234')
        self.user.save()

        self.client.login(username='UserTest', password='1234')
        self.test_task_case = {"content": "Task de prueba"}

    def create_task(self):
        task = Task.objects.create(
            content=self.test_task_case['content'], owner=self.user
        )
        task.save()

    def test_create_task(self):
        """ 
            Create a task and check that it was created. 
            Also check that read-only fields are not affected. 
        """
        response = self.client.post(
            '/api/tasks/',
            self.test_task_case,
            format='json'
        )
        task_data = json.loads(response.content)

        # Check that everything it's created with it's default and expected values.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('created_at', json.loads(response.content))
        self.assertEqual(1, task_data['id'])
        self.assertEquals(self.test_task_case['content'], task_data['content'])
        self.assertEquals(False, task_data['completed'])

        # I try to change some read-only fields.
        self.test_task_case['created_at'] = '2000-01-01T13:22:32.401149Z'
        self.test_task_case['id'] = 3

        response = self.client.post(
            '/api/tasks/',
            self.test_task_case,
            format='json'
        )
        task_data = json.loads(response.content)

        # The read-only fields should not be affected by my specified values.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # ID should be 2.
        self.assertNotEqual(3, json.loads(response.content)['id'])
        self.assertNotEqual(
            self.test_task_case['created_at'], task_data['created_at']
        )

    def test_get_task(self):
        """ Check that I can get a task by it's ID. """
        self.create_task()
        response = self.client.get(
            '/api/tasks/1/', format='json'
        )
        task_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.test_task_case['content'], task_data['content'])
        self.assertEqual(False, task_data['completed'])

    def test_get_especific_task(self):
        """ Check the tasks filter by content. """
        for i in range(1, 3):
            task = Task.objects.create(
                content=f'Hello task {i}', owner=self.user
            )
            task.save()

        # Filter by content only. The date will always be automatically assigned.
        response = self.client.get(
            '/api/tasks/?content=hello%20task%202',
            format='json'
        )

        task_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Don't forget that we get a list of dicts.
        self.assertEqual('Hello task 2', task_data[0]['content'])
        self.assertEqual(2, task_data[0]['id'])

    def test_get_list(self):
        """ Check that I can get the task list of the current user. """
        # I create a second user and assign a task to it.
        second_user = User(
            email='',
            username='SecondUserTest',
        )
        second_user.set_password('1234')
        second_user.save()

        task = Task.objects.create(
            content=f'Hello task', owner=second_user
        )
        task.save()

        # I create a task for my current user.
        self.create_task()
        task.save()

        # When I get my task list, I should only see the tasks of my logged in user.
        response = self.client.get(
            '/api/tasks/',
            format='json'
        )
        task_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(task_data))
        self.assertEqual(
            self.test_task_case['content'], task_data[0]['content']
        )

    def test_update_task(self):
        """ Check that I can check a task as 'completed'. """
        self.create_task()

        # I try to update the task.
        response = self.client.patch(
            '/api/tasks/1/',
            {
                'content': 'Task updated',
                'completed': False
            },
            format='json'
        )
        task_data = json.loads(response.content)

        # The 'Content' and 'Completed' fields should not be affected by manually given values.
        # Specifically, 'content' cannot be updated and 'completed' will always be updated
        # to the opposite value of its current value.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual('Task updated', task_data['content'])
        self.assertEqual(self.test_task_case['content'], task_data['content'])
        self.assertEqual(True, task_data['completed'])

    def test_delete_task(self):
        """ Check that I can delete a task. """
        self.create_task()
        response = self.client.delete(
            '/api/tasks/1/',
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(0, Task.objects.count())
