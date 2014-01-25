from django.conf.urls import patterns, include, url
from siteCoGM.views import homepage_view, about, tutoriel, compte_pf_detail, compte_pf_total, ajout_GM, page_mail, modify_compte_detail, mise_a_jour_graph, graphiques, modify_ajout_gm
from siteCoGM.views import create_user, created_user, login_page, logout_page, voir_cogm, set_session_cogm_id

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^CoGM/$', homepage_view),
    url(r'^CoGM/about/$', about),
    url(r'^CoGM/tutoriel/$', tutoriel),
    url(r'^CoGM/compte_pf_detail/$', compte_pf_detail),
    url(r'^CoGM/compte_pf_total/$', compte_pf_total),    
    url(r'^CoGM/ajout_GM/$', ajout_GM),       
    url(r'^CoGM/modify_compte_detail/$', modify_compte_detail),       
    url(r'^CoGM/mail/$', page_mail),
    url(r'^CoGM/voir_cogm/$', voir_cogm),
    url(r'^CoGM/create_user/$', create_user),
    url(r'^CoGM/created_user/$', created_user),
    url(r'^CoGM/mise_a_jour_graph/$', mise_a_jour_graph),
    url(r'^CoGM/graphiques/$', graphiques),
    url(r'^CoGM/login/$', login_page),
    url(r'^CoGM/logout/$', logout_page),
    url(r'^set_session_cogm_(\d{1,10})/$', set_session_cogm_id),
    url(r'^CoGM/modify_ajout_gm/$', modify_ajout_gm),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

