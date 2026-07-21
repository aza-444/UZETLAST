from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('set-language/<str:lang>/', views.set_language, name='set_language'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    # Korporativ boshqaruv
    path('korporativ/', views.corporate_index, name='corporate_index'),
    path('korporativ/hujjat/<int:doc_id>/', views.document_viewer, name='document_viewer'),
    path('korporativ/<slug:cat_slug>/<str:year_or_arxiv>/', views.corporate_documents, name='corporate_documents'),
]
