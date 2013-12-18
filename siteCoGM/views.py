from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,render_to_response
from django.template import RequestContext
import os
from django import forms
from helper_compte_pf import clean_list, compute_stuff, print_compte, print_mail


def hello(request):
    return HttpResponse("Hello world")
    
    
################################################
########### homepage du site
################################################
def homepage_view(request):
    argDict = {'request':request,}
    return render_to_response('homepage.html', argDict, context_instance=RequestContext(request))
    
    
        
def compte_pf_detail(request):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    pfile = os.path.join(BASE_DIR, 'siteCoGM/raw_compte_pf_detail.txt')
    fin = open(pfile,"r")
    ls = fin.readlines() 
    argDict = {'request':request, 'compte':ls,}
    return render_to_response('compte_pf_detail.html', argDict, context_instance=RequestContext(request))
    
    
def compte_pf_total(request):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    pfile = os.path.join(BASE_DIR, 'siteCoGM/raw_compte_pf_total.txt')
    fin = open(pfile,"r")
    ls = fin.readlines() 
    argDict = {'request':request, 'compte':ls,}
    return render_to_response('compte_pf_total.html', argDict, context_instance=RequestContext(request))
    
    
def page_mail(request):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    pfile = os.path.join(BASE_DIR, 'siteCoGM/raw_mail.txt')
    fin = open(pfile,"r")
    ls = fin.readlines() 
    argDict = {'request':request, 'mail':ls,}

    return render_to_response('mail.html', argDict, context_instance=RequestContext(request))
    
    
    
class ajoutGMForm(forms.Form):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    dataGM = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 2}))     
    pf = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 30}))
    def clean_password(self):
        password = self.cleaned_data['password']
        if password != "marignan1515":
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
        initial_pf = """adrienR : 0 pf
ayor85 : 0 pf
bravevolonte : 0 pf
canardmalin82 : 0 pf
chefcooker94 : 0 pf
david59300 : 0 pf
emilieleo : 0 pf
fifi7489 : 0 pf
fladous : 0 pf
gadym : 0 pf
guibassim : 0 pf
idunn08 : 0 pf
jujus94 : 0 pf
locky81 : 0 pf
onclepotiron : 0 pf
ramoutch16 : 0 pf
rg68 : 0 pf
tctpfik : 0 pf
seb123 : 0 pf
shadowpleague : 0 pf
sinquem : 0 pf
sloulou : 0 pf
shawnee : 0 pf
tiousmi35 : 0 pf
yamaod : 0 pf
yoyo34540 : 0 pf
zeux123 : 0 pf"""
        initial_dataGM = """debut 13/12/13
Sophia, emilieleo , niv 4"""
        form = ajoutGMForm(
            initial={'pf': initial_pf, 'dataGM': initial_dataGM}
        )
    
    argDict = {'request':request, 'form': form}
    return render_to_response('ajout_GM.html', argDict, context_instance=RequestContext(request))
    
    
    
def update_compte_detail(info):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    pfile = os.path.join(BASE_DIR, 'siteCoGM/raw_compte_pf_detail.txt')
    with open(pfile, 'r') as file:
       data = file.readlines()
    newGM = info['dataGM'] + "\n"
    newGM+= info['pf'] + "\n"
    newGM+= "---------------------------------\n"
    data.insert(4,newGM)
    with open(pfile, 'w') as file:
       file.writelines(data)
       
       
def update_compte_total_mail():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    pfile = os.path.join(BASE_DIR, 'siteCoGM/raw_compte_pf_detail.txt')
    fin = open(pfile,"r")
    ls = fin.readlines()   
    f = clean_list(ls)
    fin.close()


    ### calcul des pf depenses, recus, etc... ####
    pls,sp,ea,df,f = compute_stuff(f)


    ### afficher le resultat selon les arguments : soit compte, soit mail, soit graphiques ###
    compte = print_compte(pls,sp,ea,df,f)
    mail = print_mail(pls,sp,ea,df,f)
    
    pfile = os.path.join(BASE_DIR, 'siteCoGM/raw_compte_pf_total.txt')
    with open(pfile, 'w') as file:
        for l in compte:
            file.write(l+"\n")
            
    pfile = os.path.join(BASE_DIR, 'siteCoGM/raw_mail.txt')
    with open(pfile, 'w') as file:
        for l in mail:
            file.write(l+"\n")



class modifyDetailForm(forms.Form):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    detail = forms.CharField(widget=forms.Textarea(attrs={'cols': 150, 'rows': 30}))  
    def clean_password(self):
        password = self.cleaned_data['password']
        if password != "marignan1515":
            raise forms.ValidationError("Mauvais password !")
        return password

  
def modify_compte_detail(request):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    pfile = os.path.join(BASE_DIR, 'siteCoGM/raw_compte_pf_detail.txt')
    
    if request.method == 'POST':
        form = modifyDetailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            with open(pfile, 'w') as file:
                 file.write(cd['detail'])
            update_compte_total_mail()
            return HttpResponseRedirect('/CoGM/')
    else:
        with open(pfile, 'r') as file:
            ls = file.readlines()
        initial_detail = ""
        for l in ls:
            initial_detail += l
        form = modifyDetailForm(
            initial={'detail': initial_detail,}
        )
    
    argDict = {'request':request, 'form': form}
    return render_to_response('modify_compte_detail.html', argDict, context_instance=RequestContext(request))
    

class miseAJourGraphForm(forms.Form):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    def clean_password(self):
        password = self.cleaned_data['password']
        if password != "marignan1515":
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
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    pfile = os.path.join(BASE_DIR, 'siteCoGM/raw_compte_pf_detail.txt')
    fin = open(pfile,"r")
    ls = fin.readlines()   
    f = clean_list(ls)
    fin.close()


    ### calcul des pf depenses, recus, etc... ####
    pls,sp,ea,df,f = compute_stuff(f)

    from helper_compte_pf_graph import do_graph
    do_graph(pls,sp,ea,df,f)
    
    


def graphiques(request):
    graph_names = ['nMembres', 'nSp_spInstant', 'nGM_nSp', 'GM', 'niv', 'player', 'player_sp', 'player_ea', 'player_df']
    argDict = {'request':request, 'graph_names': graph_names}
    return render_to_response('graphiques.html', argDict, context_instance=RequestContext(request))
    