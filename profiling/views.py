from typing import List, Optional
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
)
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, response
from .models import UserProfile, NextOfKin, Bank
from .serializers import (
    ProfileSerializer,
    CreateProfileSerializer,
    NextofKinSerializer,
    EditableBankSerializer,
)

class GetProfileApi(RetrieveAPIView, View):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field: str = 'user__email'

class ProfileDetail(RetrieveUpdateAPIView, CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes: List[permissions.BasePermission] = [permissions.IsAuthenticated]

    def get_object(self) -> Optional[UserProfile]:
        return UserProfile.objects.filter(user=self.request.user).first()

    def get_serializer_class(self) -> ProfileSerializer:
        if self.request.method == 'POST':
            return CreateProfileSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer: CreateProfileSerializer) -> None:
        data = serializer.validated_data
        state_code = (
            f"{data['state_of_resident'][0:2]}{data['first_name'][0:2]}{data['last_name'][0:2]}{data['phone'][-5:]}"
        ).upper()
        serializer.save(user=self.request.user, state_code=state_code)
        super().perform_create(serializer)

    def create(self, request, *args, **kwargs) -> response.Response:
        if self.get_object():
            return response.Response(
                {'detail': 'User already has a profile.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

class EditNextofKin(RetrieveUpdateAPIView):
    def get_queryset(self) -> List[NextOfKin]:
        return NextOfKin.objects.filter(profile=self.request.user.profile)

    serializer_class = NextofKinSerializer
    permission_classes: List[permissions.BasePermission] = [permissions.IsAuthenticated]

    def get_object(self) -> NextOfKin:
        nextofkin, _ = NextOfKin.objects.get_or_create(profile=self.request.user.profile)
        return nextofkin

class EditBank(RetrieveUpdateAPIView):
    def get_queryset(self) -> List[Bank]:
        bank, _ = Bank.objects.get_or_create(profile=self.request.user.profile)
        return bank

    serializer_class = EditableBankSerializer
    permission_classes: List[permissions.BasePermission] = [permissions.IsAuthenticated]

    def get_object(self) -> Bank:
        bank, _ = Bank.objects.get_or_create(profile=self.request.user.profile)
        return bank

class AdminPanel(ListAPIView):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    filterset_fields: List[str] = ['state_code', 'phone']
    search_fields: List[str] = ['state_code', 'transactions__trxid']
    permission_classes: List[permissions.BasePermission] = [permissions.IsAdminUser]

User = get_user_model()

def activate_account(request, uidb64: str, token: str) -> HttpResponse:
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            print('done')
            return HttpResponse("Your account has been activated successfully.")
        else:
            print('done')
            return HttpResponse("Activation link is invalid.")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        print('done')
        return HttpResponse("Activation link is invalid.")
