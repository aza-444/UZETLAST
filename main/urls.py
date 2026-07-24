from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('set-language/<str:lang>/', views.set_language, name='set_language'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('yangiliklar/<slug:slug>/', views.news_detail, name='news_detail'),
    # Korporativ boshqaruv
    path('korporativ/', views.corporate_index, name='corporate_index'),
    path('korporativ/hujjat/<int:doc_id>/', views.document_viewer, name='document_viewer'),
    path('korporativ/hujjat/<int:doc_id>/batafsil/', views.corporate_detail, name='corporate_detail'),
    path('korporativ/hujjat/<int:doc_id>/yuklash/', views.document_download, name='document_download'),
    path('korporativ/hujjat/<int:doc_id>/fayl/', views.document_file, name='document_file'),
    path('korporativ/<slug:cat_slug>/<str:year_or_arxiv>/', views.corporate_documents, name='corporate_documents'),
]
