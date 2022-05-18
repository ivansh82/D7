from django.urls import path
from .views import AuthorsList, AuthorDetail, PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, SearchList, AddProtectedView



urlpatterns = [
   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('search/', SearchList.as_view(), name='post_search'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('authors', AuthorsList.as_view()),
   path('authors/<int:pk>/', AuthorDetail.as_view()),
   path('add/', AddProtectedView.as_view(), name= 'add_post'),
]