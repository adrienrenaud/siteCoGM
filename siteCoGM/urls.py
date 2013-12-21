from django.conf.urls import patterns, include, url
from siteCoGM.views import homepage_view, about, compte_pf_detail, compte_pf_total, ajout_GM, page_mail, modify_compte_detail, mise_a_jour_graph, graphiques, modify_ajout_gm


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^CoGM/$', homepage_view),
    url(r'^CoGM/about/$', about),
    url(r'^CoGM/compte_pf_detail/$', compte_pf_detail),
    url(r'^CoGM/compte_pf_total/$', compte_pf_total),    
    url(r'^CoGM/ajout_GM/$', ajout_GM),       
    url(r'^CoGM/modify_compte_detail/$', modify_compte_detail),       
    url(r'^CoGM/mail/$', page_mail),
    url(r'^CoGM/mise_a_jour_graph/$', mise_a_jour_graph),
    url(r'^CoGM/graphiques/$', graphiques),
    url(r'^CoGM/modify_ajout_gm/$', modify_ajout_gm),
    url(r'^admin/', include(admin.site.urls)),
)