from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView, GenericAPIView, CreateAPIView
from . models import UserProfile, NextOfKin, Bank
from . serializers import ProfileSerializer,CreateProfileSerializer, NextofKinSerializer, EditableBankSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator


class GetProfileApi(RetrieveAPIView,):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user__email'
    
    # def get_object(self, email):
    #     return UserProfile.objects.filter(email=email).first()
    

class ProfileDetail(RetrieveUpdateAPIView, CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.filter(user=self.request.user).first()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateProfileSerializer
        else:
            return self.serializer_class


    def perform_create(self, serializer):
        data = serializer.validated_data
        state_code = (f"{data['state_of_resident'][0:2]}{data['first_name'][0:2]}{data['last_name'][0:2]}{data['phone'][-5:]}").upper()
        serializer.save(user = self.request.user,
                        state_code = state_code)
        return super().perform_create(serializer)

