from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    TEXT = 'text'
    AUDIO = 'audio'
    VIDEO = 'video'

    NOTE_TYPES = [
        (TEXT, 'Text'),
        (AUDIO, 'Audio'),
        (VIDEO, 'Video'),
    ]

    title = models.CharField(max_length=255)
    note_type = models.CharField(max_length=10, choices=NOTE_TYPES, default=TEXT)
    content = models.TextField(blank=True, null=True)
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)
    video_file = models.FileField(upload_to='video/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class NoteShare(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_notes')
    shared_with = models.ManyToManyField(User)
