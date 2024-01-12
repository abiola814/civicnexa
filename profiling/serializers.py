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
        fields = ['bank_name', 'BVN', 'account_name', 'account_number']
        

class NextofKinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextOfKin
        fields = '__all__'
        read_only_fields = ['profile']


class ProfileSerializer(serializers.ModelSerializer):
    bank = BankSerializer(many=True, read_only=True)
    nextofkin = NextofKinSerializer(many=True, read_only=True)
    # children = ChildrenSerializer(many=True, read_only = True)
    # spouse = SpouseSerializer(many=True, read_only = True)
    # parent = ParentSerializer(many=True, read_only = True)
    class Meta:
        model = UserProfile
        # fields = '__all__'
        fields = ['first_name', 'last_name', 'dob', 'state_of_origin', 'state_of_resident', 'address',
                  'gender','occupation','marital_status','bloodgroup', 'genotype','state_code', 'phone', 'nextofkin', 'bank']
        read_only_fields = ['user', 'first_name', 'last_name', 'middle_name','dob', 'state_of_origin', 'state_of_resident', 'state_code', 'nextofkin', 'bank']
        
        
    def update(self, instance, validated_data):
        nextofkin = validated_data.pop('nextofkin', None)
        bank = validated_data.pop('bank', None)
        
        for key, value in validated_data.items():
            setattr(instance, key, value)
            
        instance.save()
        
        bank = Bank.objects.create(**bank[0], profile=instance)
        nextofkin = NextOfKin.objects.create(**nextofkin[0], profile=instance)
        
        return instance

class CreateProfileSerializer(serializers.ModelSerializer):
    bank = BankSerializer(many=True,)
    nextofkin = NextofKinSerializer(many=True,)
    class Meta:
        model = UserProfile
        # fields = '__all__'
        fields = ['first_name', 'last_name', 'dob', 'state_of_origin', 'state_of_resident', 'address',
                  'gender','occupation','marital_status','bloodgroup', 'genotype','state_code', 'phone', 'bank', 'nextofkin']
        read_only_fields = ['user', 'state_code']
        
        
    def create(self, validated_data):
        nextofkin = validated_data.pop('nextofkin', None)
        bank = validated_data.pop('bank', None)
        
        profile = UserProfile.objects.create(
            **validated_data
        )
        
        # print(bank)
        
        # bank = Bank.objects.create(**bank[0], profile=profile)
        # nextofkin = NextOfKin.objects.create(**nextofkin[0], profile=profile)
        
        return profile
    
    def update(self, instance, validated_data):
        nextofkin = validated_data.pop('nextofkin', None)
        bank = validated_data.pop('bank', None)
        
        for key, value in validated_data.items():
            setattr(instance, key, value)
            
        instance.save()
        
        bank = Bank.objects.create(**bank[0], profile=instance)
        nextofkin = NextOfKin.objects.create(**nextofkin[0], profile=instance)
        
        return instance

        # return super().update(instance, validated_data)
   
class EditableBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['account_number', 'bank_name']
