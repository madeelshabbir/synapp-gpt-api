"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#from account import urls
from superadmin import urls

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')),
    #path('api/api/admin/',  include(('superadmin.urls', 'superadmin'), namespace='superadmin')),

    path('api/admin/',  include(('superadmin.urls', 'superadmin'), namespace='superadmin')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# [Unit]
# Description=MyApp Server
# After=network.target

# [Service]
# User=<imad>
# Group=<imad sudo>
# WorkingDirectory=/home/imad/synappgpt/synappml1/Final_Synapp/backend/
# Environment=REACT_APP_API_URL=http://54.37.153.137:5173/
# ExecStart=/bin/bash -c "source /home/imad/synappgpt/synappml1/Final_Synapp/myenv2/bin/activate && python3 /home/imad/synappgpt/synappml1/Final_Synapp/backend/manage.py runserver 0.0.0.0:8000 & cd /home/imad/synappgpt/synappml1/Final_Synapp/frontend && npm run dev -- --host 0.0.0.0"

# [Install]
# WantedBy=multi-user.target
# [Unit]
# Description=MyApp Server
# After=network.target

# [Service]
# User=imad
# Group=sudo
# WorkingDirectory=/home/imad/synappgpt/synappml1/Final_Synapp/backend/
# Environment=REACT_APP_API_URL=http://54.37.153.137:5173 DJANGO_APP_URL=http://54.37.153.137:8000
# ExecStart=/bin/bash -c "source /home/imad/synappgpt/synappml1/Final_Synapp/myenv2/bin/activate && python3 /home/imad/synappgpt/synappml1/Final_Synapp/backend/manage.py runserver 0.0.0.0:8000 & cd /home/imad/synappgpt/synappml1/Final_Synapp/frontend && npm run dev -- --host 0.0.0.0"

# [Install]
# WantedBy=multi-user.target

# server {
#     listen 80;
#     server_name  54.37.153.137

#     location / {

#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#     }

#     location /static/ {
#         alias http://54.37.153.137:8000/static/;
#     }

#     location /media/ {
#         alias http://54.37.153.137:800/media/;
#     }
# }
# server {
#     listen 80;
#     server_name  54.37.153.137;

#     root /home/imad/synappgpt/synappml1/Final_Synapp/frontend/build;

#     location / {
#         try_files $uri $uri/ /index.html;
#     }
# }

