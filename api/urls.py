from django.urls import path
from .views import *
urlpatterns = [
    ####----------login---------------#####
    path('login/', MytokenManager.as_view(), name='token_obtain_pair'),
    ####---------register-------------#####
    path('register/', RegisterAPI.as_view(), name='user-registerGirant'),
    ####---------register Agent-------------#####
    path('register-agent/', AgentRegisterAPI.as_view(), name='user-registerAgent'),
    ####-----------create document ---------######
    path('create_document/', DocumentsCreateAPI.as_view(), name='create-document'),
    #---------------get alldocument ---------#####
    path('get_all_document/', getAllDocuments.as_view(), name='getall-document'),
    ##---------------delete document ----------####
    path('delete-document/<int:document_id>', deletedocumentDocuments.as_view(), name='delete-document'),
    ##---------------update document ----------####
    path('update-document/<int:document_id>', updateDocuments.as_view(), name='update-document'),
    
    # ##-----------cours---------------#####
    # path('cours/create/', CoursCreateView.as_view(), name='cours-create'),
    # ####--------video---------
    # path('videos/create/', VideoCreateView.as_view(), name='video-create'),
    
]