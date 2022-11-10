from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import TaskSerializer
from .models import Task
from logging import getLogger

logger = getLogger('django')


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        # I link the user of the request to the created task
        serializer.save(owner=self.request.user)
        logger.info(f'Task created successfully: {serializer.data}')

    def get_queryset(self):
        """  """
        # Only obtain the tasks that belongs to the current user.
        queryset = Task.objects.filter(owner=self.request.user)
        content = self.request.query_params.get('content')

        # Filter from header params, if there is any.
        if content is not None:
            queryset = queryset.filter(content__contains=content)
        created_at = self.request.query_params.get('created_at')

        if created_at is not None:
            queryset = queryset.filter(created_at__contains=created_at)

        logger.info(
            f'Tasks filtered successfully. Query filters=[Content:"{content}" - Date:"{created_at}"].')
        return queryset

    def partial_update(self, request, *args, **kwargs):
        """ Toggle the 'completed' status """
        instance = self.get_object()
        # I make sure to only change the 'completed' field.
        # That's why i ignore the request data.
        instance.completed = not instance.completed
        logger.info(
            f'Task {instance.id} updated successfully, new status: {instance.completed}'
        )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
