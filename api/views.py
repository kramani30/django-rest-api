from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Task model.
    Provides full CRUD operations:
    - GET /api/tasks/          - list all tasks
    - POST /api/tasks/         - create a task
    - GET /api/tasks/{id}/     - retrieve a task
    - PUT /api/tasks/{id}/     - update a task
    - PATCH /api/tasks/{id}/   - partial update a task
    - DELETE /api/tasks/{id}/  - delete a task
    - GET /api/tasks/by_status/?status=done - filter by status
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "updated_at", "status"]

    @action(detail=False, methods=["get"])
    def by_status(self, request):
        """Return tasks filtered by status query parameter."""
        status = request.query_params.get("status", None)
        if status:
            tasks = self.queryset.filter(status=status)
        else:
            tasks = self.queryset.all()
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
