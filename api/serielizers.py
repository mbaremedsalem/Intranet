from .models import *
from rest_framework import serializers 
from django.contrib.auth import authenticate

class UserAubSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAub
        fields = ['nom', 'prenom', 'phone', 'username', 'email', 'address', 'post', 'image', 'role']
        read_only_fields = ['username']
#--------------user serializer-------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= UserAub
        fields= ('nom','prenom','username','address','email','phone','role','direction')

#--------------user Agent serializer-------------
class UserAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Agent
        fields= ('nom','prenom','username','address','email','phone','role','direction')   


#--------------login---------------------
class MyTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active and not user.is_blocked:
                user.number_attempt = 0
                user.save()
                return user
            elif user.is_blocked:
                print(f"User {username} is blocked")
                raise serializers.ValidationError({'message': 'Compte bloqué, veuillez contacter l\'administrateur.'})
        else:
            try:
                obj = UserAub.objects.get(username=username)
                if obj.number_attempt < 5:
                    obj.number_attempt += 1
                    obj.save()
                    print(f"Invalid credentials for {username}")
                    raise serializers.ValidationError({'message': 'Informations invalides.'})
                else:
                    obj.number_attempt += 1
                    obj.is_blocked = True
                    obj.save()
                    print(f"User {username} is now blocked")
                    raise serializers.ValidationError({'message': 'Compte bloqué, veuillez contacter l\'administrateur.'})
            except UserAub.DoesNotExist:
                print(f"User {username} does not exist")
                raise serializers.ValidationError({'message': 'Informations invalides.'})
#--------------------Register Agent ----------------------
class AgentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ('nom', 'role','image','post','phone','username','prenom','email','address','password','direction')
        extra_kwargs = {
            'password': {'write_only': True}
        }

def create(self, validated_data):
    user = Agent.objects.create_Agent( 
        nom=validated_data['nom'],
        role=validated_data['role'],
        post=validated_data['post'],
        image=validated_data['image'],
        phone=validated_data['phone'],
        prenom=validated_data['prenom'],
        email=validated_data['email'],
        address=validated_data['address'],
        password=validated_data['password'],
        direction=validated_data['direction']
            )

    return user

class RegisterAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields =  ('nom', 'role','image','post','username','phone', 'prenom','email','address','password','direction')
        extra_kwargs = {
            'password': {'write_only': True}
        }

#------------------- document serializer -------------------
class DocumentsSerializer(serializers.ModelSerializer):
    # Ajoutez ce champ pour représenter la direction par nom
    direction_nom = serializers.CharField(source='direction.nom', read_only=True)

    class Meta:
        model = Documents
        # Remplacez 'direction' par 'direction_nom' dans les champs
        fields = ('id', 'sujet', 'code', 'description', 'direction_nom', 'file','date_ajout')

#------------------- document serializer  but in archiv -------------------
class DocumentsSerializerArchive(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = ('sujet', 'file')  # Ajoutez d'autres champs si nécessaire

    def create(self, validated_data):
        # Obtenez l'ID de l'archive depuis les paramètres de vue
        archive_id = self.context['view'].kwargs['archive_id']
        # Obtenez l'archive correspondante
        archive = Archive.objects.get(pk=archive_id)

        # Assurez-vous d'ajouter l'archive à validated_data avant la création
        validated_data['archives'] = archive

        # Créez l'objet Document avec les données validées
        document = Documents.objects.create(
            sujet=validated_data['sujet'],
            file=validated_data['file'],
            archives=archive  # Ajoutez d'autres champs si nécessaire
        )

        return document   

#------------------- direction serializer -------------------
class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ('id','nom', 'code')
        
# ---------------Agent serializer -------------------
class AgentSerializer(serializers.ModelSerializer):
    direction_nom = serializers.CharField(source='direction.nom', read_only=True)
    class Meta:
        model = Agent
        fields = '__all__'
# ---------------Update Agent serializer -------------------        
class UpdateAgentSerializers(serializers.ModelSerializer):
    direction_nom = serializers.CharField(source='direction.nom', read_only=True)
    class Meta:
        model = Agent
        fields = ('nom','prenom','phone','email','address', 'direction_nom','post')        
   

# ---------- roles -----
class RoleSerializer(serializers.Serializer):
    value = serializers.CharField()

# ---------- Archive serializer -------  
class ArchiveSerializer(serializers.ModelSerializer):
    documents = DocumentsSerializer(many=True, read_only=True)

    class Meta:
        model = Archive
        fields = ['id','nom', 'date_ajout', 'documents'] 
    
#avis serializer 

class AvisSerializer(serializers.ModelSerializer):
    admin_nom = serializers.SerializerMethodField()
    admin_prenom = serializers.SerializerMethodField()
    admin_image = serializers.SerializerMethodField()

    class Meta:
        model = Avis
        fields = ['id', 'titre', 'description', 'file', 'admin', 'admin_nom', 'admin_prenom', 'admin_image', 'user', 'date']

    def __init__(self, *args, **kwargs):
        super(AvisSerializer, self).__init__(*args, **kwargs)

        # Si le champ 'user' est vide dans les données entrantes, supprimez-le de la liste des champs à valider
        if 'user' in self.fields and 'user' not in self.initial_data:
            del self.fields['user']

    def get_admin_nom(self, obj):
        return obj.admin.nom if hasattr(obj.admin, 'nom') else ''

    def get_admin_prenom(self, obj):
        return obj.admin.prenom if hasattr(obj.admin, 'prenom') else ''  

    def get_admin_image(self, obj):
        # Récupérez le chemin de l'image de l'administrateur
        return obj.admin.image.url if obj.admin.image else None

class AvisSerializer1(serializers.ModelSerializer):
    admin_nom = serializers.SerializerMethodField()
    admin_prenom = serializers.SerializerMethodField()
    admin_image = serializers.SerializerMethodField()
 
    class Meta:
        model = Avis
        fields = ['id', 'titre', 'description', 'file', 'admin', 'admin_nom', 'admin_prenom','admin_image','user', 'date']

    def get_admin_nom(self, obj):
        return obj.admin.nom if hasattr(obj.admin, 'nom') else ''

    def get_admin_prenom(self, obj):
        return obj.admin.prenom if hasattr(obj.admin, 'prenom') else ''  

    def get_admin_image(self, obj):
            # Récupérez le chemin de l'image de l'administrateur
            return obj.admin.image.url if obj.admin.image else None     

class ProcedureSerializer(serializers.ModelSerializer):
    admin_nom = serializers.SerializerMethodField()
    admin_prenom = serializers.SerializerMethodField()
    admin_image = serializers.SerializerMethodField()
 
    class Meta:
        model = procedur
        fields = ['id', 'titre', 'description', 'file', 'admin', 'admin_nom', 'admin_prenom','admin_image','user', 'date']

    def get_admin_nom(self, obj):
        return obj.admin.nom if hasattr(obj.admin, 'nom') else ''

    def get_admin_prenom(self, obj):
        return obj.admin.prenom if hasattr(obj.admin, 'prenom') else ''  

    def get_admin_image(self, obj):
            # Récupérez le chemin de l'image de l'administrateur
            return obj.admin.image.url if obj.admin.image else None  

class NoteSerializer(serializers.ModelSerializer):
    admin_nom = serializers.SerializerMethodField()
    admin_prenom = serializers.SerializerMethodField()
    admin_image = serializers.SerializerMethodField()
 
    class Meta:
        model = note
        fields = ['id', 'titre', 'description','code','file', 'admin', 'admin_nom', 'admin_prenom','admin_image','user', 'date']
    def __init__(self, *args, **kwargs):
        super(NoteSerializer, self).__init__(*args, **kwargs)

        # Si le champ 'user' est vide dans les données entrantes, supprimez-le de la liste des champs à valider
        if 'user' in self.fields and 'user' not in self.initial_data:
            del self.fields['user']

    def get_admin_nom(self, obj):
        return obj.admin.nom if hasattr(obj.admin, 'nom') else ''

    def get_admin_prenom(self, obj):
        return obj.admin.prenom if hasattr(obj.admin, 'prenom') else ''  

    def get_admin_image(self, obj):
            # Récupérez le chemin de l'image de l'administrateur
            return obj.admin.image.url if obj.admin.image else None  
    
class NoteSerializer1(serializers.ModelSerializer):
    admin_nom = serializers.SerializerMethodField()
    admin_prenom = serializers.SerializerMethodField()
    admin_image = serializers.SerializerMethodField()
 
    class Meta:
        model = note
        fields = ['id', 'titre', 'description','code','file', 'admin', 'admin_nom', 'admin_prenom','admin_image','user', 'date']
            
    def get_admin_nom(self, obj):
        return obj.admin.nom if hasattr(obj.admin, 'nom') else ''

    def get_admin_prenom(self, obj):
        return obj.admin.prenom if hasattr(obj.admin, 'prenom') else ''  

    def get_admin_image(self, obj):
            # Récupérez le chemin de l'image de l'administrateur
            return obj.admin.image.url if obj.admin.image else None      
    
class PolitiqueSerializer(serializers.ModelSerializer):
    admin_nom = serializers.SerializerMethodField()
    admin_prenom = serializers.SerializerMethodField()
    admin_image = serializers.SerializerMethodField()
 
    class Meta:
        model = plotique
        fields = ['id', 'titre', 'description','code','file', 'admin', 'admin_nom', 'admin_prenom','admin_image','user', 'date']
    def __init__(self, *args, **kwargs):
        super(PolitiqueSerializer, self).__init__(*args, **kwargs)

        # Si le champ 'user' est vide dans les données entrantes, supprimez-le de la liste des champs à valider
        if 'user' in self.fields and 'user' not in self.initial_data:
            del self.fields['user']
            
    def get_admin_nom(self, obj):
        return obj.admin.nom if hasattr(obj.admin, 'nom') else ''

    def get_admin_prenom(self, obj):
        return obj.admin.prenom if hasattr(obj.admin, 'prenom') else ''  

    def get_admin_image(self, obj):
            # Récupérez le chemin de l'image de l'administrateur
            return obj.admin.image.url if obj.admin.image else None   

class PolitiqueSerializer1(serializers.ModelSerializer):
    admin_nom = serializers.SerializerMethodField()
    admin_prenom = serializers.SerializerMethodField()
    admin_image = serializers.SerializerMethodField()
 
    class Meta:
        model = plotique
        fields = ['id', 'titre', 'description','code','file', 'admin', 'admin_nom', 'admin_prenom','admin_image','user', 'date']

    def get_admin_nom(self, obj):
        return obj.admin.nom if hasattr(obj.admin, 'nom') else ''

    def get_admin_prenom(self, obj):
        return obj.admin.prenom if hasattr(obj.admin, 'prenom') else ''  

    def get_admin_image(self, obj):
            # Récupérez le chemin de l'image de l'administrateur
            return obj.admin.image.url if obj.admin.image else None          
    
class DecisionSerializer(serializers.ModelSerializer):
    admin_nom = serializers.SerializerMethodField()
    admin_prenom = serializers.SerializerMethodField()
    admin_image = serializers.SerializerMethodField()
 
    class Meta:
        model = decision
        fields = ['id', 'titre', 'description','code','file', 'admin', 'admin_nom', 'admin_prenom','admin_image','user', 'date']
    def __init__(self, *args, **kwargs):
        super(DecisionSerializer, self).__init__(*args, **kwargs)
        # Si le champ 'user' est vide dans les données entrantes, supprimez-le de la liste des champs à valider
        if 'user' in self.fields and 'user' not in self.initial_data:
            del self.fields['user']
            
    def get_admin_nom(self, obj):
        return obj.admin.nom if hasattr(obj.admin, 'nom') else ''

    def get_admin_prenom(self, obj):
        return obj.admin.prenom if hasattr(obj.admin, 'prenom') else ''  

    def get_admin_image(self, obj):
            # Récupérez le chemin de l'image de l'administrateur
            return obj.admin.image.url if obj.admin.image else None  

class DecisionSerializer1(serializers.ModelSerializer):
    admin_nom = serializers.SerializerMethodField()
    admin_prenom = serializers.SerializerMethodField()
    admin_image = serializers.SerializerMethodField()
 
    class Meta:
        model = decision
        fields = ['id', 'titre', 'description','code','file', 'admin', 'admin_nom', 'admin_prenom','admin_image','user', 'date']

    def get_admin_nom(self, obj):
        return obj.admin.nom if hasattr(obj.admin, 'nom') else ''

    def get_admin_prenom(self, obj):
        return obj.admin.prenom if hasattr(obj.admin, 'prenom') else ''  

    def get_admin_image(self, obj):
            # Récupérez le chemin de l'image de l'administrateur
            return obj.admin.image.url if obj.admin.image else None          

class chartSerializer(serializers.ModelSerializer):
    admin_nom = serializers.SerializerMethodField()
    admin_prenom = serializers.SerializerMethodField()
    admin_image = serializers.SerializerMethodField()
 
    class Meta:
        model = charts
        fields = ['id', 'titre', 'description', 'file', 'admin', 'admin_nom', 'admin_prenom','admin_image','user', 'date']
    def __init__(self, *args, **kwargs):
        super(chartSerializer, self).__init__(*args, **kwargs)

        # Si le champ 'user' est vide dans les données entrantes, supprimez-le de la liste des champs à valider
        if 'user' in self.fields and 'user' not in self.initial_data:
            del self.fields['user']

    def get_admin_nom(self, obj):
        return obj.admin.nom if hasattr(obj.admin, 'nom') else ''

    def get_admin_prenom(self, obj):
        return obj.admin.prenom if hasattr(obj.admin, 'prenom') else ''  

    def get_admin_image(self, obj):
            # Récupérez le chemin de l'image de l'administrateur
            return obj.admin.image.url if obj.admin.image else None   

class chartSerializer1(serializers.ModelSerializer):
    admin_nom = serializers.SerializerMethodField()
    admin_prenom = serializers.SerializerMethodField()
    admin_image = serializers.SerializerMethodField()
 
    class Meta:
        model = charts
        fields = ['id', 'titre', 'code','description', 'file', 'admin', 'admin_nom', 'admin_prenom','admin_image','user', 'date']


    def get_admin_nom(self, obj):
        return obj.admin.nom if hasattr(obj.admin, 'nom') else ''

    def get_admin_prenom(self, obj):
        return obj.admin.prenom if hasattr(obj.admin, 'prenom') else ''  

    def get_admin_image(self, obj):
            # Récupérez le chemin de l'image de l'administrateur
            return obj.admin.image.url if obj.admin.image else None                        




