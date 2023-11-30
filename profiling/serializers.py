from rest_framework import serializers
from . models import UserProfile, Bank, NextOfKin, Children, Spouse
# from djoser.serializers import UserCreateSerializer as BUCS


# class UserCreateSerializer(BUCS):
#     class Meta(BUCS.Meta):
#         fields = '__all__'

class ChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Children
        fields = '__all__'

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Children
        fields = '__all__'

class SpouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spouse
        fields = '__all__'

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'
        # fields = ['bank_name', 'account_number']

class NextofKinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextOfKin
        fields = '__all__'
        read_only_fields = ['profile']

# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):

    bank = BankSerializer(many=True, read_only=True)
    next_of_kin = NextofKinSerializer(many=True, read_only = True)
    children = ChildrenSerializer(many=True, read_only = True)
    spouse = SpouseSerializer(many=True, read_only = True)
    parent = ParentSerializer(many=True, read_only = True)
    class Meta:
        model = UserProfile
        fields = '__all__'
        # fields = ['first_name', 'last_name', 'dob', 'state_of_origin', 'state_of_resident', 'address']
        read_only_fields = ['user', 'first_name', 'last_name', 'middle_name','dob', 'state_of_origin', 'state_of_resident', 'state_code']

class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        # fields = '__all__'
        fields = ['first_name', 'last_name', 'dob', 'state_of_origin', 'state_of_resident', 'address', 'state_code', 'phone']
        read_only_fields = ['user', 'state_code']
   
class EditableBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['account_number', 'bank_name']
