from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import HttpResponseNotFound, JsonResponse
from django.forms.models import model_to_dict
from .models import BestTime
from room.models import Room
from datetime import datetime, timedelta
import json


def best_time_list(request, room_id):
    if not request.user.is_authenticated():
        return HttpResponse(status=401)

    room_id = int(room_id)

    try:
        Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return HttpResponseNotFound()

    if request.method == 'GET':
        best_times = list(BestTime.objects.filter(room_id=room_id).values())
        for time in best_times:
            time['start_time'] = time['start_time'].strftime('%Y-%m-%dT%H:%M:%SZ')
            time['end_time'] = time['end_time'].strftime('%Y-%m-%dT%H:%M:%SZ')
        return JsonResponse(
            best_times,
            safe=False
        )

    else:
        return HttpResponseNotAllowed(['GET'])
