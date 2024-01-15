from django.urls import path
from .views import *
urlpatterns = [
    ####----------login---------------#####
    path('login/', MytokenManager.as_view(), name='token_obtain_pair'),
    ####---------register-------------#####
    path('register/', RegisterAPI.as_view(), name='user-registerGirant'),
    ####---------register Agent-------------#####
    path('register-agent/', AgentRegisterAPI.as_view(), name='user-registerAgent'),

    #------------ document ----------------- 
    ####----------- create document ---------######
    path('create_document/', DocumentsCreateAPI.as_view(), name='create-document'),
    #---------------get alldocument ---------#####
    path('get_all_document/', getAllDocuments.as_view(), name='getall-document'),
    #---------------get alldocumentby aget direction ---------#####
    path('get_documents_by_agent_direction/', GetDocumentsByAgentDirection.as_view(), name='get_documents_by_agent_direction'),
    ##---------------delete document ----------####
    path('delete-document/<int:document_id>', deletedocumentDocuments.as_view(), name='delete-document'),
    ##---------------update document ----------####
    path('update-document/<int:document_id>', updateDocuments.as_view(), name='update-document'),
    # ------------- get Document by id --------####
    path('document/<int:document_id>/', DocumentDetailAPIView.as_view(), name='documnet-detail'),
    ##----------------chercher un document par sujet ---------####
    path('chercher-documents/', DocumentSearchBySujet.as_view(), name='document-list'),

    # ------------ direction ------------
    ##---------------create direction----------###
    path('create_direction/', DirectionCreateAPI.as_view(), name='create-direction'),
    #---------------get alldirection ---------#####
    path('get_all_direction/',getAllDirection.as_view(), name='getall-direction'),
    #---------------get direction ById---------#####
    path('direction/<int:direction_id>/', DirectionDetailAPIView.as_view(), name='direction-detail'),
    ##---------------delete direction ----------####
    path('delete-direction/<int:direction_id>', deleteDirection.as_view(), name='delete-direction'),
    ##---------------update direction ----------####
    path('update-direction/<int:direction_id>', updateDirection.as_view(), name='update-direction'),



    # -----------user Agent-----------------
    path('get-agents/', AgentList.as_view(), name='agent-list'),
    # -----------delete Agent---------------
    path('delete-agent/<int:agent_id>', deleteAgent.as_view(), name='agent-delete'),
    # ------------update Agent-------------
    path('update-agent/<int:agent_id>', updateAgent.as_view(), name='update-agent'),
    # ------------- get Agent by id --------
    path('agent/<int:agent_id>/', AgentDetailAPIView.as_view(), name='agent-detail'),

    # -------------user Gerant ------------
    path('get-gerant/', GerantList.as_view(), name='gerant-list'),
    # -----------delete Gerant---------------
    path('delete-gerant/<int:gerant_id>', deleteGerant.as_view(), name='gerant-delete'),
    # -----------update gerant --------------
    path('update-gerant/<int:gerant_id>', updateGerant.as_view(), name='update-gerant'),
    # ------------- get Gerant by id --------
    path('gerant/<int:gerant_id>/', GerantDetailAPIView.as_view(), name='agent-detail'),

    # --------------------- list role ------------------------
    path('roles/', RoleListAPIView.as_view(), name='role-list'),

    # -------- - archive --------- 
    # --------------------- get create archive  -------------------
    path('archives/',ArchiveListCreateView.as_view(), name='archive'),
    # --------------------- add document to archive  -------------------
    path('archives/<int:archive_id>/add_document/', AddDocumentToArchiveView.as_view(), name='add-document-to-archive'),
    # --------------------- get document in archive  -------------------
    path('archives/<int:archive_id>/documents/', DocumentInArchiveView.as_view(), name='documents-in-archive'),


    # ----------- avis ---------
    # --------- create avis -------
    path('create-avis/', AvisCreateAPI.as_view(), name='avis-posted'),
    #------- get avis user agent ou gerant -----
    path('avis/user/<int:user_id>/', AvisByUserAPI.as_view(), name='avis-get-user'),
    #------- get avis user admin-----
    path('avis-by-admin/<int:admin_id>/', AvisByAdminAPI.as_view(), name='avis-by-admin'),
    #------ delet avis by id --------
    path('delete-avis/<int:avis_id>/', deleteAvis.as_view(), name='delete-avis-by-id'),


    # --------procedure -----------
    #------- create procedure -------- 
    path('create-procedure/', ProcedureCreateAPI.as_view(), name='procedure-posted'),
    #------- get avis user agent ou gerant -----
    path('avis/user/<int:user_id>/', AvisByUserAPI.as_view(), name='procedure-get-user'),
    # get procedure by admin
    path('procedure-by-admin/<int:admin_id>/', ProcedureByAdminAPI.as_view(), name='procedure-by-admin'),
    # delete procedure 
    path('delete-procedure/<int:procedure_id>/', deleteProcedure.as_view(), name='delete-procedure-by-id'),

    # -------- note -----------
    path('get_all_notes/', getAllNotes.as_view(), name='getall-notes'),
    #------- create note -------- 
    path('create-note/', NoteCreateAPI.as_view(), name='chart-posted'),
    #------- get avis user agent ou gerant -----
    path('avis/user/<int:user_id>/', AvisByUserAPI.as_view(), name='chart-get-user'),
    # get procedure by admin
    path('note-by-admin/<int:admin_id>/', NoteByAdminAPI.as_view(), name='chart-by-admin'),
    # delete procedure 
    path('delete-note/<int:note_id>/', deleteNote.as_view(), name='delete-chart-by-id'),

    # -------- decision -----------
    path('get_all_decisions/', getAllDecision.as_view(), name='getall-decision'),
    #------- create note -------- 
    path('create-decision/', DecisionCreateAPI.as_view(), name='get-decision'),
    #------- get avis user agent ou gerant -----
    path('decision/user/<int:user_id>/', DecisionByUserAPI.as_view(), name='decision-get-user'),
    # get procedure by admin
    path('decision-by-admin/<int:admin_id>/', DecisionByAdminAPI.as_view(), name='decision-by-admin'),
    # delete procedure 
    path('delete-decision/<int:decision_id>/', deleteDecision.as_view(), name='delete-decision-by-id'),

    # -------- chart -----------
    #------- create chart -------- 
    path('create-chart/', ChartsCreateAPI.as_view(), name='chart-posted'),
    #------- get avis user agent ou gerant -----
    path('avis/user/<int:user_id>/', AvisByUserAPI.as_view(), name='chart-get-user'),
    # get chart by admin
    path('chart-by-admin/<int:admin_id>/', ChartsByAdminAPI.as_view(), name='chart-by-admin'),
    # delete chart 
    path('delete-chart/<int:procedure_id>/', deletecharts.as_view(), name='delete-chart-by-id'),


    # -------- plotique -----------
    #------- create plotique -------- 
    path('create-plotique/', plotiqueCreateAPI.as_view(), name='plotique-posted'),
    #------- get avis user agent ou gerant -----
    path('plotique/user/<int:user_id>/', PolitiqueByUserAPI.as_view(), name='chart-get-user'),
    # get chart by admin
    path('plotique-by-admin/<int:admin_id>/', PlotiqueByAdminAPI.as_view(), name='plotique-by-admin'),
    # delete chart 
    path('delete-plotique/<int:plotique_id>/', deletePlotique.as_view(), name='delete-plotique-by-id'),

]