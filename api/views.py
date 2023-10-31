from django.shortcuts import render
from rest_framework.exceptions import ValidationError,APIException
from rest_framework_simplejwt.views import TokenObtainPairView
from .serielizers import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.http import Http404

#-------------------login---------------------
class InvalidInformationException(APIException):
    status_code = 400
    default_detail = 'Informations invalides'

class MytokenManager(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({
            'message': str(e),
            'status':status.HTTP_400_BAD_REQUEST, 
        })
            
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'login success',
            'status':status.HTTP_200_OK, 
            'id': user.id,
            'role':user.role,
            'email': user.email,
            'nom': user.nom,
            'prenom':user.prenom,
            'adress':user.address,
            'phone': user.phone,
            'access': str(refresh.access_token),
            'refresh_token': str(refresh),  
        })

#----------------- Register Girant ---------
class RegisterAPI(TokenObtainPairView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)
        if phone and password:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                user = serializer.save()
                user.set_password(password)
                user.save()
                refresh = RefreshToken.for_user(user)
                user = serializer.validated_data
                return Response({
                    'user': UserSerializer(user, context=self.get_serializer_context()).data,
                    'token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                })
            except Exception as e:
                print(str(e)) 
                return Response({'status':status.HTTP_400_BAD_REQUEST, 'Message':'Bad request !!!'})

        return Response({'status':status.HTTP_400_BAD_REQUEST, 'Message':'Envoyez le numéro de telephone et le mdp'})


#------------------ register Agent --------------    
class AgentRegisterAPI(generics.GenericAPIView):
    serializer_class = AgentRegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            user = serializer.save()
            password = request.data.get('password', False)
            user.set_password(password)
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserAgentSerializer(user, context=self.get_serializer_context()).data,
                'token': str(refresh.access_token),
                'refresh_token': str(refresh)
            })
        except:
            return Response({'status':status.HTTP_400_BAD_REQUEST, 'Message':'Bad request'})    
        

#------------------ cree un document -------------------
class DocumentsCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Récupérez l'ID de l'utilisateur à partir du token JWT ou de toute autre source
        user_id = self.request.user.id  # Utilisez l'ID de l'utilisateur authentifié

        try:
            # Recherchez l'instance de Agent associée à cet ID
            agent = Agent.objects.get(id=user_id)

            # Vous avez maintenant l'instance de Agent
            sujet = request.data.get('sujet')
            code = request.data.get('code')
            description = request.data.get('description')
            file = request.data.get('file')

            document = Documents.objects.create(agent=agent, sujet=sujet, code=code, description=description, file=file)

            return Response({'detail': 'Success'}, status=status.HTTP_200_OK)
        except Agent.DoesNotExist:
            # L'agent n'a pas été trouvé
            return Response({'detail': 'Agent not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Une erreur s'est produite lors de la recherche ou de la création du document
            return Response({'detail': 'Server error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#-------------------get all document ---------------#
class getAllDocuments(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Récupérez tous les documents
        documents = Documents.objects.all()
        serializer = DocumentsSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)        
    
#------------------delete document by id ----------------#
class deletedocumentDocuments(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request, document_id):
        # Code pour supprimer un document par son ID
        
        try:
            document = Documents.objects.get(id=document_id)
            document.delete()
            return Response({'detail': 'Document deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Documents.DoesNotExist:
            return Response({'detail': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)    
        
#--------------------update documents ----------------#
class updateDocuments(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, document_id):
        # Code pour mettre à jour un document par son ID
        try:
            document = Documents.objects.get(id=document_id)
            serializer = DocumentsSerializer(document, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Documents.DoesNotExist:
            return Response({'detail': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)        