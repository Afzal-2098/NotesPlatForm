from .models import Note, NoteShare
from .serializers import NoteSerializer, NoteShareSerializer, UserSerializer, CustomTokenObtainPairSerializer

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied, NotFound

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'User registered successfully.'}, status=201)
    return Response(serializer.errors, status=400)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def note_list(request):
    if request.method == 'GET':
        notes = Note.objects.filter(user = request.user)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data, status=200)
    elif request.method == 'POST':
        request.data['user'] = request.user.id
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def note_detail(request, pk):
    try:
        note = Note.objects.get(pk=pk)
    except Note.DoesNotExist:
        return Response(status=404)

    shared_with_users = note.noteshare_set.filter(shared_with=request.user)
    print("=====", shared_with_users)
    if request.method == 'GET':
        if note.user != request.user and not shared_with_users:
            raise PermissionDenied("You do not have permission to access this note(Not Created by You, Nor Shared with You).")

        serializer = NoteSerializer(note)
        return Response(serializer.data, status=200)
    elif request.method == 'PUT':
        if note.user != request.user and not shared_with_users:
            raise PermissionDenied("You Can not Update this note(Not Created by You, Nor Shared with You).")

        request.data['user'] = request.user.id
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        if note.user != request.user and not shared_with_users:
            raise PermissionDenied("You do not have permission to Delete this note(Not Created by You, Nor Shared with You).")

        note.delete()
        return Response({"detail":"Note Deleted Successfully"}, status=204)
    

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def note_share_list(request):
    if request.method == 'GET':
        note_shares = NoteShare.objects.filter(shared_by=request.user)
        if len(note_shares)<1:
            raise NotFound("You Not Shared any Note to anyone.")
        serializer = NoteShareSerializer(note_shares, many=True)
        return Response(serializer.data, status=200)
    elif request.method == 'POST':
        try:
            note_owner = Note.objects.get(id=request.data['note'], user=request.user)
        except Note.DoesNotExist:
            raise NotFound("The note does not exist or you are not the owner.")
        request.data['shared_by'] = request.user.id
        serializer = NoteShareSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def note_share_detail(request, pk):
    try:
        note_share = NoteShare.objects.get(pk=pk)
    except NoteShare.DoesNotExist:
        return Response({"detail": "Not Found any Note with this id."},status=404)
    
    if note_share.shared_by != request.user and request.user not in note_share.shared_with.all():
        raise PermissionDenied("You do not have permission to access this note.")

    if request.method == 'GET':
        serializer = NoteShareSerializer(note_share)
        return Response(serializer.data, status=200)
    elif request.method == 'PUT':
        if note_share.shared_by != request.user:
            raise PermissionDenied("You do not have permission to Update this note.")
        request.data['shared_by'] = request.user.id
        serializer = NoteShareSerializer(note_share, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        if note_share.shared_by != request.user:
            raise PermissionDenied("You do not have permission to delete this note.")
        note_share.delete()
        return Response({"detail":"Note Deleted Successfully"}, status=204)
