from PyPDF2 import PdfFileMerger
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.exceptions import ValidationError,APIException
from rest_framework_simplejwt.views import TokenObtainPairView
from .serielizers import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import *
import random
from rest_framework.permissions import AllowAny


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
        image_url = user.image.url if user.image else None
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
            'username': user.username,
            'post': user.post,
            'image':image_url,
           

            'access': str(refresh.access_token),
            'refresh_token': str(refresh),  
        })

#----------------- Register Girant ---------
class RegisterAPI(TokenObtainPairView):
    serializer_classes = {
        'Admin': RegisterAdminSerializer,
        'Agent': AgentRegisterSerializer,
        'Gerant': RegisterSerializer,
    }

    def get_serializer_class(self):
        role = self.request.data.get('role', False)
        serializer_class = self.serializer_classes.get(role)
        return serializer_class

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)
        role = request.data.get('role', False)

        if phone and password and role:
            serializer_class = self.get_serializer_class()
            if serializer_class is None:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'Message': 'Invalid role'})

            serializer = serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            try:
                user = serializer.save()
                user.set_password(password)
                user.save()
                refresh = RefreshToken.for_user(user)

                return Response({
                    'phone': user.phone,
                    'nome': user.nom,
                    'prenom': user.prenom,
                    'address':user.address,
                    'role': user.role,
                    'image': request.data.get('image'),
                    'token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                })
            except:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'Message': 'Bad request'})

        return Response({'status': status.HTTP_400_BAD_REQUEST, 'Message': 'Envoyez le numéro de telephone exist'})


#------------------ register Agent --------------    
class AgentRegisterAPI(generics.GenericAPIView):
    serializer_class = AgentRegisterSerializer
    authentication_classes = []  # Remove any authentication requirement
    permission_classes = [AllowAny]  # Allow any user to access this view
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
        
# Fonction pour générer un code aléatoire

def generate_random_code(length=6):
    code = ''.join(random.choice('0123456789') for _ in range(length))
    return 'TF'+code
#------------------ cree un document -------------------
class DocumentsCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Récupérez l'ID de la direction à partir du corps de la requête
        # direction_id = request.data.get('direction_id')

        # Vérifiez si l'ID de la direction est présent dans le corps de la requête
        # if not direction_id:
        #     return Response({'detail': 'Direction ID is required in the request body.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Recherchez l'instance de la direction associée à cet ID
            # direction = Admin.objects.get(id=direction_id)

            # Vérifiez si l'utilisateur est un directeur
            # if not direction.is_director:
            #     return Response({'detail': 'You do not have permission to add documents.'}, status=status.HTTP_403_FORBIDDEN)
            direction_id = request.data.get('direction_id')
            sujet = request.data.get('sujet')
            code = generate_random_code()
            description = request.data.get('description')
            file = request.data.get('file')

            document = Documents.objects.create(direction_id=direction_id, sujet=sujet, code=code, description=description, file=file)

            return Response({'message': 'Ajout Success'}, status=status.HTTP_200_OK)
        # except Admin.DoesNotExist:
        #     return Response({'detail': 'Direction not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': 'Server error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
#-------------------get all document ---------------#
class getAllDocuments(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Récupérez tous les documents
        documents = Documents.objects.all()
        serializer = DocumentsSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK,content_type='application/pdf')        


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
            return Response({'message': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)        
        
#-----------------creta direction by agent-------------------#
class DirectionCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Récupérez l'ID de l'utilisateur à partir du token JWT ou de toute autre source
        user_id = self.request.user.id  # Utilisez l'ID de l'utilisateur authentifié

        try:
            # Recherchez l'instance de Agent associée à cet ID
            admin = Admin.objects.get(id=user_id)

            # Vous avez maintenant l'instance de Agent
            nom = request.data.get('nom')
            code = request.data.get('code')
           

            direction = Direction.objects.create(nom=nom,code=code)

            return Response({
                'message': 'Ajout Success',
                'agent_name':admin.nom,
                'agent_prenom':admin.prenom,
                'agent_phone':admin.phone,
                'document_name':direction.nom,
                'document_code':direction.code
                }, 
                status=status.HTTP_200_OK)
        except Admin.DoesNotExist:
            # L'agent n'a pas été trouvé
            return Response({'detail': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Une erreur s'est produite lors de la recherche ou de la création du document
            return Response({'detail': 'Server error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
#--------------- get all direction --------------
class getAllDirection(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Récupérez tous les documents
        direction = Direction.objects.all()
        serializer = DirectionSerializer(direction, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
#--------- get direction par id -------
class DirectionDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, direction_id, *args, **kwargs):
        try:
            agent = Direction.objects.get(id=direction_id)
        except Direction.DoesNotExist:
            return Response({'error': 'Direction not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DirectionSerializer(agent)
        return Response(serializer.data, status=status.HTTP_200_OK) 
#------------------delete direction by id ----------------#
class deleteDirection(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request, direction_id):
        # Code pour supprimer un document par son ID
        try:
            direction = Direction.objects.get(id=direction_id)
            direction.delete()
            return Response({'detail': 'direction deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Direction.DoesNotExist:
            return Response({'detail': 'direction not found'}, status=status.HTTP_404_NOT_FOUND)      

#--------get documet by agent direction -----------# 
class GetDocumentsByAgentDirection(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            agent = request.user.agent  # Supposons que l'agent est associé à l'utilisateur connecté
            agent_direction = agent.direction
            documents = Documents.objects.filter(direction=agent_direction)
            serializer = DocumentsSerializer(documents, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AttributeError:
            return Response({'detail': 'Agent not found for the user'}, status=status.HTTP_404_NOT_FOUND)

#--------- get gerant par id -------
class DocumentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, document_id, *args, **kwargs):
        try:
            agent = Documents.objects.get(id=document_id)
        except Documents.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DocumentsSerializer(agent)
        return Response(serializer.data, status=status.HTTP_200_OK) 
            
#------------------- update direction ----------------#
class updateDirection(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, direction_id):
        # Code pour mettre à jour un document par son ID
        try:
            document = Direction.objects.get(id=direction_id)
            serializer = DirectionSerializer(document, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Direction.DoesNotExist:
            return Response({'message': 'direction not found'}, status=status.HTTP_404_NOT_FOUND)           
        

#recherche d'un document par sujet

class DocumentSearchBySujet(APIView):
    def post(self, request):
        sujet = request.data.get('sujet', '')

        documents = Documents.objects.filter(sujet__icontains=sujet)
        
        if not documents:
            # Aucun document avec ce sujet n'a été trouvé
            return Response({'message': 'Document introuvable'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DocumentsSerializer(documents, many=True)

        return Response({
            'documents': serializer.data
        }, status=status.HTTP_200_OK)
    
#get All agent 
class AgentList(APIView):
    def get(self, request):
        agents = Agent.objects.all()
        serializer = AgentSerializer(agents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 
#--delete Agent--- 
class deleteAgent(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request, agent_id):
        # Code pour supprimer un document par son ID
        
        try:
            agent = Agent.objects.get(id=agent_id)
            agent.delete()
            return Response({'detail': 'Agent User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Agent.DoesNotExist:
            return Response({'detail': 'Agent not found'}, status=status.HTTP_404_NOT_FOUND)  
#----update Agent -------
class updateAgent(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, agent_id):
        # Code pour mettre à jour un document par son ID
        try:
            agent = Agent.objects.get(id=agent_id)
            serializer = AgentSerializer(agent, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Agent.DoesNotExist:
            return Response({'message': 'Agent not found'}, status=status.HTTP_404_NOT_FOUND)   

#--------- get agent par id -------
class AgentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, agent_id, *args, **kwargs):
        try:
            agent = Agent.objects.get(id=agent_id)
        except Agent.DoesNotExist:
            return Response({'error': 'Agent not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AgentSerializer(agent)
        return Response(serializer.data, status=status.HTTP_200_OK) 

# get All gerant  
class GerantList(APIView):
    def get(self, request):
        agents = Gerant.objects.all()
        serializer = GerantSerializer(agents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
    
#-----------delete gerant-------
class deleteGerant(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request, gerant_id):
        # Code pour supprimer un document par son ID
        
        try:
            gerant = Gerant.objects.get(id=gerant_id)
            gerant.delete()
            return Response({'detail': 'Gerant User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Gerant.DoesNotExist:
            return Response({'detail': 'Gerant not found'}, status=status.HTTP_404_NOT_FOUND)   
        

#---------update gerant ------------
class updateGerant(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, gerant_id):
        # Code pour mettre à jour un document par son ID
        try:
            gerant = Gerant.objects.get(id=gerant_id)
            serializer = GerantSerializer(gerant, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Gerant.DoesNotExist:
            return Response({'message': 'Gerant not found'}, status=status.HTTP_404_NOT_FOUND)  

#--------- get gerant par id -------
class GerantDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, gerant_id, *args, **kwargs):
        try:
            agent = Gerant.objects.get(id=gerant_id)
        except Gerant.DoesNotExist:
            return Response({'error': 'Gerant not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GerantSerializer(agent)
        return Response(serializer.data, status=status.HTTP_200_OK) 
            
#----- tous les roles 
class RoleListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        roles = [{'value': value,} for value, label in Role]
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 
    
#------ Archive ------ 
class ArchiveListCreateView(generics.ListCreateAPIView):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer

# ------ add document to archiv -----
class AddDocumentToArchiveView(generics.CreateAPIView):
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializerArchive

    def perform_create(self, serializer):
        archive_id = self.kwargs['archive_id']
        archive = Archive.objects.get(pk=archive_id)
        serializer.save(archive=archive)    

# get DocumentInArchive 
class DocumentInArchiveView(generics.ListAPIView):
    serializer_class = DocumentsSerializer

    def get_queryset(self):
        archive_id = self.kwargs['archive_id']
        return Documents.objects.filter(archives__id=archive_id)


# create avis en specifiant les user qui peux le voire 
class AvisCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'Admin':
            return Response({"error": "Vous n'êtes pas autorisé à effectuer cette action"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        users_ids = data.get('users', [])

        for user_id in users_ids:
            try:
                user = UserAub.objects.get(id=user_id)
                if user.role not in ['Gerant', 'Agent']:
                    return Response({"error": f"L'utilisateur avec l'ID {user_id} n'est pas un Gerant ou un Agent"}, status=status.HTTP_400_BAD_REQUEST)
            except UserAub.DoesNotExist:
                return Response({"error": f"L'utilisateur avec l'ID {user_id} n'existe pas"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AvisSerializer(data=data)
        if serializer.is_valid():
            avis = serializer.save()
            for user_id in users_ids:
                user = UserAub.objects.get(id=user_id)
                avis.users.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
#les avis d'un utilisateur     
class AvisByUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        if request.user.role not in ['Gerant', 'Agent']:
            return Response({"error": "Vous n'êtes pas autorisé à effectuer cette action"}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = UserAub.objects.get(id=user_id)
        except UserAub.DoesNotExist:
            return Response({"error": f"L'utilisateur avec l'ID {user_id} n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

        avis = Avis.objects.filter(user=user)

        serializer = AvisSerializer(avis, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
    
#list des documents par meme admin 
class AvisByAdminAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, admin_id):
        # Récupérez tous les avis associés à l'administrateur donné
        avis = Avis.objects.filter(admin__id=admin_id)
        
        # Sérialisez les avis
        serializer = AvisSerializer(avis, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)        
    
#-----------delete avis-------
class deleteAvis(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request, avis_id):
        # Code pour supprimer un document par son ID
        
        try:
            avis = Avis.objects.get(id=avis_id)
            avis.delete()
            return Response({'detail': 'Avis deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Gerant.DoesNotExist:
            return Response({'detail': 'Avis not found'}, status=status.HTTP_404_NOT_FOUND)   
        
# create avis en specifiant les user qui peux le voire 
class ProcedureCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'Admin':
            return Response({"error": "Vous n'êtes pas autorisé à effectuer cette action"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        users_ids = data.get('users', [])

        for user_id in users_ids:
            try:
                user = UserAub.objects.get(id=user_id)
                if user.role not in ['Gerant', 'Agent']:
                    return Response({"error": f"L'utilisateur avec l'ID {user_id} n'est pas un Gerant ou un Agent"}, status=status.HTTP_400_BAD_REQUEST)
            except UserAub.DoesNotExist:
                return Response({"error": f"L'utilisateur avec l'ID {user_id} n'existe pas"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProcedureSerializer(data=data)
        if serializer.is_valid():
            avis = serializer.save()
            for user_id in users_ids:
                user = UserAub.objects.get(id=user_id)
                avis.users.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

#les avis d'un utilisateur     
class ProcedureByUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        if request.user.role not in ['Gerant', 'Agent']:
            return Response({"error": "Vous n'êtes pas autorisé à effectuer cette action"}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = UserAub.objects.get(id=user_id)
        except UserAub.DoesNotExist:
            return Response({"error": f"L'utilisateur avec l'ID {user_id} n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
        avis = procedur.objects.filter(user=user)
        serializer = ProcedureSerializer(avis, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 
    
#list des procedures par meme admin 
class ProcedureByAdminAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, admin_id):
        # Récupérez tous les avis associés à l'administrateur donné
        proc = procedur.objects.filter(admin__id=admin_id)
        # Sérialisez les avis
        serializer = ProcedureSerializer(proc, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)      