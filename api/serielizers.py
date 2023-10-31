from .models import *
from rest_framework import serializers 
from django.contrib.auth import authenticate
#--------------user serializer-------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= UserAub
        fields= ('nom','prenom','address','email','phone','role')

#--------------user Agent serializer-------------
class UserAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Agent
        fields= ('nom','prenom','address','email','phone','role')        

#--------------login---------------------
class MyTokenObtainPairSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active and not user.is_blocked:
            user.number_attempt=0
            user.save()
            return user
        
        elif user and user.is_active and user.is_blocked:
            # return Response('message')
            # return Response(serializers.errors)
            
            raise serializers.ValidationError({'message':'Compte blocké, veillez contacter lagence '})
        
        try:
            obj= Girant.objects.get(phone=data['phone'])
            if obj.number_attempt<3:
                obj.number_attempt +=1
                obj.save()
                raise serializers.ValidationError({'message':'Compte blocké .'})
            else:
                obj.number_attempt +=1
                obj.is_blocked=True
                obj.save()
                raise serializers.ValidationError({'message':'Compte blocké, veillez contacter lagence '})
        except:
            raise serializers.ValidationError({'message':'Informations invalides.'})  
        


#-----------------Serializer register Girant -------------------
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Girant
        fields = ('nom', 'phone', 'prenom','email','address','password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

def create(self, validated_data):
    user = Girant.objects.create_user(
        nom=validated_data['nom'],
        phone=validated_data['phone'],
        prenom=validated_data['prenom'],
        email=validated_data['email'],
        address=validated_data['address'],
        password=validated_data['password']
    )

    return user       
#--------------------Register Agent ----------------------
class AgentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ('nom', 'phone', 'prenom','email','address','password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = Agent.objects.create_Agent( 
              nom=validated_data['nom'],
            phone=validated_data['phone'],
            prenom=validated_data['prenom'],
            email=validated_data['email'],
            address=validated_data['address'],
            password=validated_data['password']
            )

        return user
    
#------------------- document serializer -------------------
class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = ('sujet', 'code', 'description', 'file')