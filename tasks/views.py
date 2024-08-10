from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from tasks.serializer import TaskSerializer
from tasks.models import Task
@api_view(['GET', 'POST'])
def tasks_list_api_view(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        data_dict = TaskSerializer(tasks, many=True).data
        return Response(data=data_dict)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        tasks = Task.objects.create(title=title, description=description)
        return Response(data=TaskSerializer(tasks).data)

@api_view(['GET', 'PUT', 'DELETE'])
def tasks_detail_api_view(request, id):
    try:
        tasks = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return Response(data={'error': 'Task not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data_dict = TaskSerializer(tasks, many=False).data
        return Response(data=data_dict)
    elif request.method == 'DELETE':
        tasks.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        #tasks.title = request.data.get('title')
        #tasks.description = request.data.get('description')
        tasks.completed = request.data.get('completed')
        return Response(data=TaskSerializer(tasks).data)
