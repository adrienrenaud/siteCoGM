# -*- coding: utf-8 -*-

import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.core.files.storage import default_storage
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth.models import User, Group
from django.core.files.base import ContentFile
from siteCoGM.apps.userdata.models import Userdata, Textfile


from datetime import datetime
from helper_compte_pf import clean_list, compute_stuff, compute_info, print_compte, print_mail



        
        
        
        
        
        
        
################################################
########### homepage, comptes, mail
################################################

def default_view(request, templateName):
    argDict = {'request':request,}
    return render_to_response(templateName+'.html', argDict, context_instance=RequestContext(request))


def homepage_view(request):
    argDict = {'request':request,}
    return render_to_response('homepage.html', argDict, context_instance=RequestContext(request))
def about(request):
    argDict = {'request':request,}
    return render_to_response('about.html', argDict, context_instance=RequestContext(request))
def tutoriel(request):
    argDict = {'request':request,}
    return render_to_response('tutoriel.html', argDict, context_instance=RequestContext(request))
    

def compte_pf_detail(request):
    if not request.user.is_authenticated():
        if not 'user_id' in request.session.keys():
            return HttpResponseRedirect('/CoGM/voir_cogm/')
        file = User.objects.get(id=request.session['user_id']).userdata.textfiles.all().get(filetype=0).file
    else:
        file = request.user.userdata.textfiles.all().get(filetype=0).file
        userdata = request.user.userdata
    ls = file.readlines()
    file.close()
    argDict = {'request':request, 'compte':ls}
    return render_to_response('compte_pf_detail.html', argDict, context_instance=RequestContext(request))
    
    
def compte_pf_total(request):
    if not request.user.is_authenticated():
        if not 'user_id' in request.session.keys():
            return HttpResponseRedirect('/CoGM/voir_cogm/')
        file = User.objects.get(id=request.session['user_id']).userdata.textfiles.all().get(filetype=1).file
    else:
        file = request.user.userdata.textfiles.all().get(filetype=1).file
    ls = file.readlines()
    file.close()
    argDict = {'request':request, 'compte':ls,}
    return render_to_response('compte_pf_total.html', argDict, context_instance=RequestContext(request))
    
    
def page_mail(request):
    if not request.user.is_authenticated():
        if not 'user_id' in request.session.keys():
            return HttpResponseRedirect('/CoGM/voir_cogm/')
        file = User.objects.get(id=request.session['user_id']).userdata.textfiles.all().get(filetype=2).file
    else:
        file = request.user.userdata.textfiles.all().get(filetype=2).file
    ls = file.readlines()
    file.close()
    argDict = {'request':request, 'mail':ls,}
    return render_to_response('mail.html', argDict, context_instance=RequestContext(request))
    
################################################
################################################
################################################
    
    
    
    
    
    


        
################################################
########### voir cogm
################################################

def voir_cogm(request):
    luser = User.objects.filter(groups__name="simple_user").order_by("username")
    paginator = Paginator(luser, 10) # Show 10 user per page
    page = request.GET.get('page')
    try:
        luser = paginator.page(page)
    except PageNotAnInteger: # If page is not an integer, deliver first page.
        luser = paginator.page(1)
    except EmptyPage: # If page is out of range (e.g. 9999), deliver last page of results.
        luser = paginator.page(paginator.num_pages)
    argDict = {'request':request, 'luser':luser}
    return render_to_response('voir_cogm.html', argDict, context_instance=RequestContext(request))
    
    
def set_session_cogm_id(request, user_id):
    logout(request)
    try:
        userdata = User.objects.get(id=user_id).userdata
        request.session['userdata_name'] = userdata.name
        request.session['userdata_nGM'] = userdata.nGM
        request.session['userdata_nMembres'] = userdata.nMembres
        request.session['userdata_nSp'] = userdata.nSp
        request.session['userdata_nextBoy'] = userdata.nextBoy
        request.session['user_id'] = user_id
        request.session['user_name'] = User.objects.get(id=user_id).username
        request.session.save()        
    except User.DoesNotExist:
       return HttpResponse("Il n'y a pas de cogm pour cet id")
    return HttpResponseRedirect('/CoGM/')
    
################################################
################################################
################################################
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
################################################
########### ajout GM
################################################
    
class ajoutGMForm(forms.Form):
    # password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    user = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 1}), label='propriétaire GM')   
    nomGM = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 1}), label='nom GM')     
    nivGM = forms.IntegerField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 1}), label='niveau GM')     
    date = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 1}), label='date')     
    pf = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 40}), label='pf dépensés')
    # def clean_password(self):
    #     password = self.cleaned_data['password']
    #     if password !=  os.environ.get('MY_COGM_PASSWORD'):
    #         raise forms.ValidationError("Mauvais password !")
    #     return password
  
  
  
@user_passes_test(lambda u: u.groups.filter(name='simple_user').exists(), login_url='/CoGM/')
@login_required
def ajout_GM(request):
    if request.method == 'POST':
        form = ajoutGMForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            update_compte_detail(request, cd)
            try:
                update_compte_total_mail(request)
            except:
                return HttpResponseRedirect('/CoGM/view/erreur_compte/')
            send_backup_mail(request)
            return HttpResponseRedirect('/CoGM/')
    else:
        file = request.user.userdata.textfiles.all().get(filetype=3).file
        ls = file.readlines()
        file.close()
        initial_pf = ""
        for l in ls:
            initial_pf += l
        initial_date = "%s"%datetime.now().strftime("%d/%m/%y")
        initial_nomGM = "Statue de Zeus"
        initial_nivGM = 3
        initial_user  = "kate"

        form = ajoutGMForm(
            initial={'pf': initial_pf, 'nomGM': initial_nomGM, 'nivGM': initial_nivGM, 'user': initial_user, 'date' : initial_date}
        )
    argDict = {'request':request, 'form': form}
    return render_to_response('ajout_GM.html', argDict, context_instance=RequestContext(request))
    
################################################
################################################
################################################







################################################
########### update comptes
################################################
    
def update_compte_detail(request, info):
    with default_storage.open(request.user.userdata.textfiles.all().get(filetype=0).file.name, 'r') as file:
       data = file.readlines()
    pf = info['pf']
    while pf.endswith("\n") or pf.endswith("\r"):
        pf = pf[:-len("\n")]
    
    newGM=  "debut %s"%info['date'] + "\n"
    newGM+= "%s , %s , niv %i"%(info['nomGM'], info['user'], info['nivGM']) + "\n"
    newGM+= pf + "\n"
    newGM+= "---------------------------------\n"
    data.insert(4,newGM)
    
    with default_storage.open(request.user.userdata.textfiles.all().get(filetype=0).file.name, 'w') as file:
       for l in data:
            file.write(l)
       
       
def update_compte_total_mail(request):
    with default_storage.open(request.user.userdata.textfiles.all().get(filetype=0).file.name, 'r') as file:
        ls = file.readlines()   
    f = clean_list(ls)
    
    ### calcul des pf depenses, recus, etc... ####
    pls,sp,ea,df,f = compute_stuff(f)
    ### afficher le resultat selon les arguments : soit compte, soit mail, soit graphiques ###
    compte = print_compte(pls,sp,ea,df,f)
    mail = print_mail(pls,sp,ea,df,f)
    
    nMembres, nGM, nSp, nextBoy = compute_info(pls,sp,ea,df,f)
    request.user.userdata.nMembres = nMembres
    request.user.userdata.nGM = nGM 
    request.user.userdata.nSp = nSp
    request.user.userdata.nextBoy = nextBoy 
    request.user.userdata.save()
    
    with default_storage.open(request.user.userdata.textfiles.all().get(filetype=1).file.name, 'w') as file:
        for l in compte:
            file.write(l+"\n")

    with default_storage.open(request.user.userdata.textfiles.all().get(filetype=2).file.name, 'w') as file:
        for l in mail:
            file.write(l+"\n")
            
            
def send_backup_mail(request):
    from django.core.mail import send_mail, EmailMessage
    mail = EmailMessage(request.user.userdata.name, 'voir piece jointe', 'info@cogm.com', ['cogm.foe@gmail.com'])
    with default_storage.open(request.user.userdata.textfiles.all().get(filetype=0).file.name, 'r') as file:
        mail.attach('raw_compte_pf_detail.txt', file.read(), 'text/plain')
    mail.send()

            
################################################
################################################
################################################
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    
    
    






################################################
########### Modifier le detail du compte
################################################

class modifyDetailForm(forms.Form):
    detail = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 30}), label='Détail')  


@user_passes_test(lambda u: u.groups.filter(name='simple_user').exists(), login_url='/CoGM/')
@login_required
def modify_compte_detail(request):
    if request.method == 'POST':
        form = modifyDetailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            with default_storage.open(request.user.userdata.textfiles.all().get(filetype=0).file.name, 'w') as file:
                file.write(cd['detail'])
            try:
                update_compte_total_mail(request)
            except:
                return HttpResponseRedirect('/CoGM/view/erreur_compte/')
                
            send_backup_mail(request)
            return HttpResponseRedirect('/CoGM/')
    else:
        with default_storage.open(request.user.userdata.textfiles.all().get(filetype=0).file.name, 'r') as file:
            ls = file.readlines()
        
        initial_detail = ""
        for l in ls:
            initial_detail += l
        form = modifyDetailForm(
            initial={'detail': initial_detail,}
        )
    
    argDict = {'request':request, 'form': form}
    return render_to_response('modify_compte_detail.html', argDict, context_instance=RequestContext(request))
    
    
    
    
    
    
    
    
################################################
########### modidier ajout GM
################################################

@user_passes_test(lambda u: u.groups.filter(name='simple_user').exists(), login_url='/CoGM/')
@login_required
def modify_ajout_gm(request):
    if request.method == 'POST':
        form = modifyDetailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            with default_storage.open(request.user.userdata.textfiles.all().get(filetype=3).file.name, 'w') as file:
                file.write(cd['detail'])
            return HttpResponseRedirect('/CoGM/')
    else:
        with default_storage.open(request.user.userdata.textfiles.all().get(filetype=3).file.name, 'r') as file:
            ls = file.readlines()
        initial_detail = ""
        for l in ls:
            initial_detail += l
        form = modifyDetailForm(
            initial={'detail': initial_detail,}
        )
    
    argDict = {'request':request, 'form': form}
    return render_to_response('modify_ajout_gm.html', argDict, context_instance=RequestContext(request))
    
    
    
    
    
    
    
    
    
################################################
########### graphics
################################################

class miseAJourGraphForm(forms.Form):
    pass

@user_passes_test(lambda u: u.groups.filter(name='simple_user').exists(), login_url='/CoGM/')
@login_required
def mise_a_jour_graph(request):
    if request.method == 'POST':
        form = miseAJourGraphForm(request.POST)
        if form.is_valid():
            do_mise_a_jour_graph(request)
            return HttpResponseRedirect('/CoGM/')
    else:
        form = miseAJourGraphForm()
    argDict = {'request':request, 'form': form}
    return render_to_response('mise_a_jour_graph.html', argDict, context_instance=RequestContext(request))
    
    
def do_mise_a_jour_graph(request):
    with default_storage.open(request.user.userdata.textfiles.all().get(filetype=0).file.name, 'r') as file:
        ls = file.readlines()  
    f = clean_list(ls)

    ### calcul des pf depenses, recus, etc... ####
    pls,sp,ea,df,f = compute_stuff(f)

    from helper_compte_pf_graph import do_graph, save_graph
    do_graph(pls,sp,ea,df,f)
    
    for f in request.user.userdata.textfiles.all().order_by('filetype')[4:]:
        f.delete()
    
    from helper_graph_legend import GraphsMetaDataStore
    gtool = GraphsMetaDataStore()
    graph_names = ['nMembres', 'nSp_spInstant', 'nGM_nSp', 'GM', 'niv', 'player', 'player_sp', 'player_ea', 'player_df']
    # graph_names = ['nSp_spInstant']
    i=3
    for gn in graph_names:
        i+=1
        t = Textfile(userdata=request.user.userdata, filetype=i)
        file = open("./"+gn+'.png')
        t.name = gn
        t.legend = gtool.leg[gn]
        t.file.save(gn+'.png', ContentFile(file.read()))
        file.close()
        os.remove("./"+gn+'.png')
    

    

    
def create_user_imagefiles(userdata, infilename, outfilename, filetype):
    t = Textfile(userdata=userdata, filetype=filetype)
    f = default_storage.open('userdata/user_default/paintpic.JPG', 'r')
    t.file.save(outfilename, ContentFile(f.read()))
    f.close()
    


def graphiques(request):
    if request.user.is_authenticated():
        userdata = request.user.userdata
    elif 'user_id' in request.session.keys():
        userdata = User.objects.get(id=request.session['user_id']).userdata
    else:
        return HttpResponseRedirect('/CoGM/voir_cogm/')
        
    graph_names = ['nMembres', 'nSp_spInstant', 'nGM_nSp', 'GM', 'niv', 'player', 'player_sp', 'player_ea', 'player_df']
    # graph_names = ['nGM']
    graphs = userdata.textfiles.all().filter(name__in=graph_names)
    argDict = {'request':request, 'graphs': graphs, }
    return render_to_response('graphiques.html', argDict, context_instance=RequestContext(request))
    
    

    
    
    
################################################
########### user registration
################################################
# from captcha.fields import CaptchaField

class userForm(forms.Form):
    # cf = CaptchaField()
    username = forms.CharField(widget=forms.TextInput, label='Nom de la CoGM')
    password = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Mot de passe')
  



def create_user(request):
    if request.method == 'POST':
        form = userForm(request.POST)
        logout(request)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            create_user_helper(username=username, password=password)
            return HttpResponseRedirect('/CoGM/created_user/')
    else:
        form = userForm()
    argDict = {'request':request, 'form': form}
    return render_to_response('create_user.html', argDict, context_instance=RequestContext(request))


def create_user_helper(username, password):
    user = User.objects.create_user(username=username, password=password)
    if not Group.objects.filter(name="simple_user").exists():
        group = Group(name="simple_user")
        group.save() 
    group = Group.objects.get(name='simple_user') 
    group.user_set.add(user)
    
    user.save()
    userdata = Userdata(name=user.username, user=user)
    userdata.save()
    create_user_textfiles(userdata, 'raw_compte_pf_detail.txt', 0)
    create_user_textfiles(userdata, 'raw_compte_pf_total.txt', 1)
    create_user_textfiles(userdata, 'raw_mail.txt', 2)
    create_user_textfiles(userdata, 'raw_default_gm.txt', 3)

    
def create_user_textfiles(userdata, filename, filetype):
    t = Textfile(userdata=userdata, filetype=filetype)
    f = default_storage.open('userdata/user_default/%s'%filename, 'r')
    t.file.save(filename, ContentFile(f.read()))
    f.close()
    
# def create_user_imagefiles(userdata, infilename, outfilename, filetype):
#     t = Textfile(userdata=userdata, filetype=filetype)
#     f = default_storage.open('userdata/user_default/paintpic.JPG', 'r')
#     t.file.save(outfilename, ContentFile(f.read()))
#     f.close()




def created_user(request):        
    return render_to_response('created_user.html', context_instance=RequestContext(request))
    
    
    
    
    
    
    
################################################
########### user login/logout
################################################

class loginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, label='Nom de la CoGM')
    password = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Mot de passe')
    
    
def login_page(request):
    if request.POST:
        form = loginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect('/CoGM/')
    else:
        form = loginForm()
        
    argDict = {'request':request, 'form': form}
    return render_to_response('login.html', argDict, context_instance=RequestContext(request))



def logout_page(request):
    logout(request)
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect('/CoGM/')
    
    
    