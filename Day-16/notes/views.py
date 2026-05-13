from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Note
from .serializers import NoteSerializer
from .permissions import IsOwnerOrReadOnly

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    # Custom Permission combination
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the owner
        serializer.save(owner=self.request.user)