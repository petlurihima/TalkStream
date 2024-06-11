from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from agora_token_builder import RtcTokenBuilder
import random
import time
import json
from .models import RoomMember
from django.views.decorators.csrf import csrf_exempt

def getToken(request):
    appId = '6d553f01808c4b82bfc556f6a4933086'
    appCertificate = 'ca00148b91044862ac524c56121d27ad'
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token': token, 'uid': uid}, safe=False)

def lobby(request):
    return render(request, 'lobby.html')

def room(request):
    return render(request, 'room.html')

@csrf_exempt
def createMember(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"createMember received data: {data}")  # Debugging statement
            member, created = RoomMember.objects.get_or_create(
                name=data['name'],
                uid=data['UID'],
                room_name=data['room_name']
            )
            return JsonResponse({'name': member.name}, safe=False)
        except Exception as e:
            print(f"Error in createMember: {e}")  # Debugging statement
            return HttpResponseBadRequest('Error processing request')
    return HttpResponseBadRequest('Invalid request method')

def getMember(request):
    if request.method == 'GET':
        try:
            uid = request.GET.get('UID')
            room_name = request.GET.get('room_name')
            print(f"getMember received UID: {uid}, room_name: {room_name}")  # Debugging statement
            member = RoomMember.objects.get(uid=uid, room_name=room_name)
            return JsonResponse({'name': member.name}, safe=False)
        except RoomMember.DoesNotExist:
            return HttpResponseNotFound('Member not found')
        except Exception as e:
            print(f"Error in getMember: {e}")  # Debugging statement
            return HttpResponseBadRequest('Error processing request')
    return HttpResponseBadRequest('Invalid request method')

@csrf_exempt
def deleteMember(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"deleteMember received data: {data}")  # Debugging statement
            member = RoomMember.objects.get(
                name=data['name'],
                uid=data['UID'],
                room_name=data['room_name'],
            )
            member.delete()
            return JsonResponse('Member was deleted', safe=False)
        except RoomMember.DoesNotExist:
            return HttpResponseNotFound('Member not found')
        except Exception as e:
            print(f"Error in deleteMember: {e}")  # Debugging statement
            return HttpResponseBadRequest('Error processing request')
    return HttpResponseBadRequest('Invalid request method')