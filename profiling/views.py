from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView, GenericAPIView, CreateAPIView
from . models import UserProfile, NextOfKin, Bank
from . serializers import ProfileSerializer,CreateProfileSerializer, NextofKinSerializer, EditableBankSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
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



    def create(self, request, *args, **kwargs):
        # Check if the user already has a profile
        if self.get_object():
            return Response(
                {'detail': 'User already has a profile.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)


class EditNextofKin(RetrieveUpdateAPIView):
    def get_queryset(self):
        return NextOfKin.objects.filter(profile=self.request.user.profile)
    
    serializer_class = NextofKinSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        nextofkin,_ = NextOfKin.objects.get_or_create(profile=self.request.user.profile)
        return nextofkin

class EditBank(RetrieveUpdateAPIView):
    def get_queryset(self):
        bank, _ = Bank.objects.get_or_create(profile = self.request.user.profile)
        return bank

    serializer_class = EditableBankSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        bank, _ = Bank.objects.get_or_create(profile = self.request.user.profile)
        return bank


# class ListTransactions(ListAPIView, RetrieveAPIView, GenericAPIView):
#     def get_queryset(self):
#         user = self.request.user
#         return Transaction.objects.filter(owner=user.profile)
#     serializer_class = TransactionSerializer
#     permission_classes = [permissions.IsAuthenticated]


class AdminPanel(ListAPIView):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    filterset_fields = ['state_code', 'phone']
    search_fields = ['state_code', 'transactions__trxid']
    permission_classes = [permissions.IsAdminUser]


User = get_user_model()

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            # Optionally, we will redirect the user to a success page.
            print('done')
            return HttpResponse("Your account has been activated successfully.")
        else:
            # Token is invalid
            print('done')
            return HttpResponse("Activation link is invalid.")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        print('done')
        return HttpResponse("Activation link is invalid.")
      # return render(request, 'userprofile/page.html')


      
# @receiver(user_registered)
# def send_activation_email(sender, user, request, **kwargs):
#     # Generate an activation token for the user
#     token = default_token_generator.make_token(user)

#     # Encode the user's primary key for use in the URL
#     uid = urlsafe_base64_encode(force_bytes(user.pk))

#     # Build the activation URL
#     activation_url = f"http://localhost:8000/activation/{uid}/{token}/"

#     # Send an activation email to the user
#     subject = 'Activate Your Account'
#     message = f'Hi {user.username},\n\nPlease activate your account by clicking the following link:\n\n{activation_url}'
#     from_email = 'noreply@your-website.com'
#     recipient_list = [user.email]

#     # You can use Django's EmailMessage or some email library to send the email.
#     # Here's an example using Django's EmailMessage:
#     from django.core.mail import EmailMessage

#     email = EmailMessage(subject, message, from_email, recipient_list)
#     email.send()

