import sys
from datetime import date
import math 




########################################################################
########################################################################
### affichage du mail
########################################################################
########################################################################
def print_mail(pls,sp,ea,df,f):

   gm = f[0]
   ndays = int(max([math.ceil(l[1]/3.) for l in gm[1:]]))
   nextBoy = df[[l[1] for l in df].index( max([l[1] for l in df]))][0]

   ls=[]
   ls.append("@CoGM")
#   ls.append("On a fini le GM (%s) de %s en %i jours, donc je compte %i pf maximum."%(gm[0][1][0], gm[0][0], ndays, ndays*3))
   ls.append("On a fini le GM (%s) de %s."%(gm[0][1][0], gm[0][0]))
   # print "Demain on va chez %s. Tu veux quel GM %s ?"%(nextBoy, nextBoy)
   ls.append("Demain on va chez %s."%(nextBoy))

   ls.append("")
   ls.append("Voila les pf pris en compte sur le dernier GM :")
   ls.append("-"*40)
   ls.append("::: %s de %s :"%(gm[0][1][0],gm[0][0]))
   for l in gm[1:]:
      ls.append("%s : %i pf"%(l[0], l[1]))
   ls.append('-'*40)

   ls.append("")

   tot = 0
   ls.append("Et le compte total :")
   ls.append('-'*40)
   ls.append('::: depense - recu :')
   for (name, npf) in df:
      ls.append("%s : %i pf"%(name, npf)) 
      tot+=npf
   # print "- - - - - - - - - "
   # print "somme : %i"%tot

   ls.append('-'*40)

   return ls


########################################################################
########################################################################
### affichage du compte
########################################################################
########################################################################
def print_compte(pls,sp,ea,df,f):
   ls = []
   ls.append('-'*40)
   ls.append('-'*40)
   ls.append("TOTAL :")


   tot = 0
   ls.append('-'*40)
   ls.append('::: depense - recu :')
   for (name, npf) in df:
      ls.append("%s : %i pf"%(name, npf)) 
      tot+=npf
#   ls.append("- - - - - - - - - ")
#   ls.append("somme : %i"%tot)
   
   tot = 0
   ls.append('-'*40)
   ls.append('::: depense :')
   for (name, npf) in sp:
      ls.append("%s : %i pf"%(name, npf)) 
      tot+=npf
#   ls.append("- - - - - - - - - ")
#   ls.append("somme : %i"%tot)

   tot = 0
   ls.append('-'*40)
   ls.append('::: recu :')
   for (name, npf) in ea:
      ls.append("%s : %i pf"%(name, npf)) 
      tot+=npf
#   ls.append("- - - - - - - - - ")
#   ls.append("somme : %i"%tot)


   ls.append('-'*40)
   ls.append('-'*40)


   return ls


########################################################################
########################################################################
### calcul des pf depenses, recus, etc...
########################################################################
########################################################################
def compute_stuff(f):
   pls = find_players(f)
   sp  = find_spendings(f,pls)
   ea  = find_earnings(f,pls)
   df  = find_df(sp,ea)

   return pls,sp,ea,df,f

def find_players(f):
   pl = []
   for ll in f:
      for l in ll:
         pl.append(l[0])
   pls = sorted(set(pl))
   return pls
   
def find_earnings(f,pls):
   ea=[]
   for pl in pls:
      tot = 0
      for gm in f:
         if gm[0][0]==pl:
            for pll in gm[1:]:
                tot+=pll[1]
      ea.append((pl, tot))
   return ea

def find_spendings(f,pls):
   sp=[]
   for pl in pls:
      tot = 0
      for gm in f:
         for pll in gm[1:]:
             if pll[0]==pl:
                tot+=pll[1]
      sp.append((pl, tot))
   return sp

def find_df(sp,ea):
   if len(sp)!=len(ea):
      print 'Major Fail ','!'*800
   df = []
   for i in range(len(sp)):
       tot = sp[i][1]-ea[i][1]
       df.append((sp[i][0],tot))
   return df


def compute_info(pls,sp,ea,df,f):
    nMembres = len(pls)
    nGM = len(f)
    nSp = 0
    for asp in sp: nSp+=asp[1]
    nextBoy = df[[l[1] for l in df].index( max([l[1] for l in df]))][0]
    return nMembres, nGM, nSp, nextBoy


########################################################################
########################################################################
### recuperation des donnees a partir du fichier texte
########################################################################
########################################################################
def clean_list(ls):
    i=0
    while ls[i].find("Details")<0:
        i+=1

    i+=1
    ld=[]
    while i < len(ls)-2:
        ld.append(ls[i])
        i+=1

    ldd = []
    igm = -1
    for l in ld:
        if l.find("---------------------------------")>=0:
            ldd.append([])
            igm+=1
            continue
        ldd[igm].append(l.replace("\n",""))

    f=[]
    for ll in ldd:
        j=[]
        for i in range(len(ll)):
            if i==0:
                continue
            elif i==1:
                dd = ll[0].split(" ")[1].replace("\r","")
                y = 2000 + int(dd.split("/")[2])
                m = int(dd.split("/")[1])
                d = int(dd.split("/")[0])
                thedate = date(y,m,d)
                gmName = ll[1].split(",")[0]
                niv = int(ll[1].split(",")[2].split(" ")[2].replace("\r",""))
                st = (ll[i].split(",")[1].replace(" ",""), (gmName, niv, thedate))
            else:
                st = (ll[i].split(" ")[0], int(ll[i].split(" ")[2].replace("pf","")) )
            j.append(st)
        f.append(j)

    return f










def main():

    ### recuperation des arguments ###
    printMail = False
    doGraph = False
    for i,arg in enumerate(sys.argv): 
        if '--mail' == arg:
            printMail = True
        if '--graph' == arg:
            doGraph = True


    ### ouverture du fichier texte et recuperation des donnees ###
    fin = open("./raw_compte_pf_detail.txt","r")
    ls = fin.readlines()   
    f = clean_list(ls)
    fin.close()


    ### calcul des pf depenses, recus, etc... ####
    pls,sp,ea,df,f = compute_stuff(f)


    ### afficher le resultat selon les arguments : soit compte, soit mail, soit graphiques ###
    if printMail:
        print_mail(pls,sp,ea,df,f)
    elif doGraph:
        from compte_pf_graph import do_graph ### ici on importe la fonction do_graph du fichier compte_pf_graph
        do_graph(pls,sp,ea,df,f)
    else:
        print_compte(pls,sp,ea,df,f)









### porte d'entree du programme, lance la fonction main()
if __name__=="__main__":
   main()


