from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,render_to_response
from django.template import RequestContext
import os
from django import forms
from django.core.files.storage import default_storage
from datetime import datetime

from helper_compte_pf import clean_list, compute_stuff, print_compte, print_mail




    

    
        
        
        
################################################
########### homepage, comptes, mail
################################################

def homepage_view(request):
    argDict = {'request':request,}
    return render_to_response('homepage.html', argDict, context_instance=RequestContext(request))
    
    
def about(request):
    argDict = {'request':request,}
    return render_to_response('about.html', argDict, context_instance=RequestContext(request))


def compte_pf_detail(request):
    # BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    # pfile = os.path.join(BASE_DIR, 'static/raw_txt/raw_compte_pf_detail.txt')
    # fin = open(pfile,"r")
    # ls = fin.readlines()
    file = default_storage.open('raw_compte_pf_detail.txt', 'r')
    ls = file.readlines()
    file.close()
    argDict = {'request':request, 'compte':ls,}
    return render_to_response('compte_pf_detail.html', argDict, context_instance=RequestContext(request))
    
    
def compte_pf_total(request):
    file = default_storage.open('raw_compte_pf_total.txt', 'r')
    ls = file.readlines()
    file.close()
    argDict = {'request':request, 'compte':ls,}
    return render_to_response('compte_pf_total.html', argDict, context_instance=RequestContext(request))
    
    
def page_mail(request):
    file = default_storage.open('raw_mail.txt', 'r')
    ls = file.readlines()
    file.close()
    argDict = {'request':request, 'mail':ls,}
    return render_to_response('mail.html', argDict, context_instance=RequestContext(request))
    
################################################
################################################
################################################
    
    
    
    
    
    
    
    
    
################################################
########### ajout GM
################################################
    
class ajoutGMForm(forms.Form):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    dataGM = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 2}))     
    pf = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 30}))
    def clean_password(self):
        password = self.cleaned_data['password']
        if password !=  os.environ.get('MY_COGM_PASSWORD'):
            raise forms.ValidationError("Mauvais password !")
        return password
  
  
def ajout_GM(request):
    if request.method == 'POST':
        form = ajoutGMForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            update_compte_detail(cd)
            update_compte_total_mail()
            return HttpResponseRedirect('/CoGM/')
    else:
        file = default_storage.open('raw_default_gm.txt', 'r')
        ls = file.readlines()
        file.close()
        initial_pf = ""
        for l in ls:
            initial_pf += l
            
        thedate = datetime.now().strftime("%d/%m/%y")
        initial_dataGM = """debut %s 
Sophia, emilieleo , niv 4"""%thedate
        form = ajoutGMForm(
            initial={'pf': initial_pf, 'dataGM': initial_dataGM}
        )
    
    argDict = {'request':request, 'form': form}
    return render_to_response('ajout_GM.html', argDict, context_instance=RequestContext(request))
    







################################################
########### update comptes
################################################
    
def update_compte_detail(info):
    with default_storage.open('raw_compte_pf_detail.txt', 'r') as file:
       data = file.readlines()
    pf = info['pf']
    while pf.endswith("\n") or pf.endswith("\r"):
        pf = pf[:-len("\n")]
      
    newGM = info['dataGM'] + "\n"
    newGM+= pf + "\n"
    newGM+= "---------------------------------\n"
    data.insert(4,newGM)
    
    with default_storage.open('raw_compte_pf_detail.txt', 'w') as file:
       for l in data:
            file.write(l)
       
       
def update_compte_total_mail():
    with default_storage.open("raw_compte_pf_detail.txt", "r") as file:
        ls = file.readlines()   
    f = clean_list(ls)

    ### calcul des pf depenses, recus, etc... ####
    pls,sp,ea,df,f = compute_stuff(f)
    ### afficher le resultat selon les arguments : soit compte, soit mail, soit graphiques ###
    compte = print_compte(pls,sp,ea,df,f)
    mail = print_mail(pls,sp,ea,df,f)
    
    with default_storage.open('raw_compte_pf_total.txt', 'w') as file:
        for l in compte:
            file.write(l+"\n")

    with default_storage.open('raw_mail.txt', 'w') as file:
        for l in mail:
            file.write(l+"\n")









################################################
########### Modifier le detail du compte
################################################

class modifyDetailForm(forms.Form):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    detail = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 30}))  
    def clean_password(self):
        password = self.cleaned_data['password']
        if password != os.environ.get('MY_COGM_PASSWORD'):
            raise forms.ValidationError("Mauvais password !")
        return password

  
def modify_compte_detail(request):
    if request.method == 'POST':
        form = modifyDetailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            with default_storage.open("raw_compte_pf_detail.txt", 'w') as file:
                file.write(cd['detail'])
            update_compte_total_mail()
            return HttpResponseRedirect('/CoGM/')
    else:
        with default_storage.open("raw_compte_pf_detail.txt", 'r') as file:
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
  
def modify_ajout_gm(request):
    if request.method == 'POST':
        form = modifyDetailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            with default_storage.open("raw_default_gm.txt", 'w') as file:
                file.write(cd['detail'])
            return HttpResponseRedirect('/CoGM/')
    else:
        with default_storage.open("raw_default_gm.txt", 'r') as file:
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
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    def clean_password(self):
        password = self.cleaned_data['password']
        if password != os.environ.get('MY_COGM_PASSWORD'):
            raise forms.ValidationError("Mauvais password !")
        return password


def mise_a_jour_graph(request):
    if request.method == 'POST':
        form = miseAJourGraphForm(request.POST)
        if form.is_valid():
            do_mise_a_jour_graph()
            return HttpResponseRedirect('/CoGM/')
    else:
        form = miseAJourGraphForm()
    argDict = {'request':request, 'form': form}
    return render_to_response('mise_a_jour_graph.html', argDict, context_instance=RequestContext(request))
    
    
def do_mise_a_jour_graph():
    with default_storage.open("raw_compte_pf_detail.txt", "r") as file:
        ls = file.readlines()  
    f = clean_list(ls)

    ### calcul des pf depenses, recus, etc... ####
    pls,sp,ea,df,f = compute_stuff(f)

    from helper_compte_pf_graph import do_graph
    do_graph(pls,sp,ea,df,f)
    
    
def graphiques(request):
    graph_names = ['nMembres', 'nSp_spInstant', 'nGM_nSp', 'GM', 'niv', 'player', 'player_sp', 'player_ea', 'player_df']
    # graph_names = ['nGM',]
    argDict = {'request':request, 'graph_names': graph_names}
    return render_to_response('graphiques.html', argDict, context_instance=RequestContext(request))
    