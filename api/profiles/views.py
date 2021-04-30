from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Profile
from .serializers import ProfileSerializer


class ProfileView(APIView):
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        profile = self.get_object(user=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request, pk):
        profile = Profile(**request.data)
        profile.user = get_user_model().objects.get(pk=pk)
        profile.save()
        return JsonResponse(code=status.HTTP_201_CREATED, data="User successfully created!")

    def patch(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(code=status.HTTP_200_OK, data=serializer.data)
        return JsonResponse(code=status.HTTP_400_BAD_REQUEST, data="Unable to update user")

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)