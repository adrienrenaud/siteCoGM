import matplotlib
matplotlib.use('Agg')
import pylab
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, timedelta
import os

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile





#######################################################################################
#######################################################################################
#######################################################################################
#######
#######  La suite sert uniquement a produire les graphiques
#######
#######################################################################################
#######################################################################################
#######################################################################################

def mySave(name, plt):
    # BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    # plt.savefig(os.path.join(BASE_DIR, 'siteCoGM/static/results', name+'.pdf'))
    # plt.savefig(os.path.join(BASE_DIR, 'siteCoGM/static/results', name+'.png'))
    # plt.savefig(os.path.join(BASE_DIR, 'static/results', name+'.png'))

    plt.savefig("./"+name+'.png')
    # file = open("./"+name+'.png')
    # default_storage.save("./"+name+'.png', ContentFile(file.read()))
    # file.close()

    # os.remove("./"+name+'.png')
    




def do_graph(pls,sp,ea,df,f):
    dates, nGM = do_nGM(pls,sp,ea,df,f)
    dates, nSp = do_nSp(pls,sp,ea,df,f)
    dates, nMembres = do_nMembres(pls,sp,ea,df,f)
    do_nGM_nSp(dates, nSp, nGM)

    do_player_sp(sp)
    do_player_ea(ea)
    do_player_df(df)

    do_GM(f)
    do_niv(f)
    do_player(f)

    # do_sp_instant(pls,sp,ea,df,f)
    do_nSp_spInstant(pls,sp,ea,df,f)
    

    # do_hist_sp(pls,sp,ea,df,f)


def save_graph(request, graph_names):
    for gn in graph_names:
        file = open("./"+gn+'.png')
        default_storage.save("./"+name+'.png', ContentFile(file.read()))
        file.close()
        os.remove("./"+name+'.png')


def do_nGM(pls,sp,ea,df,f):
    dates = []
    nGM = [i+1 for i in range(len(f))]
    for l in reversed(f):
        dates.append(l[0][1][2])
    dates = sorted(dates)

    fig, ax = plt.subplots()
    ax.plot_date(dates, nGM, '-')
    ax.fill_between(dates, 0, nGM, facecolor='blue', alpha=0.5)
    plt.xlabel('Date')
    plt.ylabel('Nombre de GM')
    plt.ylim((0,1.2*max(nGM)))
    plt.xlim((dates[0]-timedelta(10), dates[len(dates)-1]+timedelta(10)))
    ax.grid(True)
    fig.autofmt_xdate()

    # BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    # plt.savefig(os.path.join(BASE_DIR, 'mysite/static/results', 'nGM.pdf'))
    # plt.savefig(os.path.join(BASE_DIR, 'mysite/static/results', 'nGM.png'))
    # mySave('nGM', plt)

    return dates, nGM



    

def do_hist_sp(pls,sp,ea,df,f):
    spInstant = []
    for l in reversed(f):
        spI = 0
        for ll in l[1:]:
            spI+=ll[1]
        spInstant.append(spI)


    fig, ax = pylab.subplots()
    # ax.set_xlim(-0.5,len(gm))
    n, bins, patches = plt.hist(spInstant, bins=20, alpha=0.4,  color='b',)
    ax.set_ylim(0,1.2*max(n))    

    plt.xlabel('Nombre de pf')
    plt.ylabel('Nombre de GM')
    # plt.savefig("results/sp_hist.pdf")
    # plt.savefig("results/sp_hist.png")
    
    mySave('sp_hist', plt)



def do_nSp_spInstant(pls,sp,ea,df,f):
    dates = []
    nSp = []
    spInstant = []
    sp=0
    for l in reversed(f):
        dates.append(l[0][1][2])
        spI = 0
        for ll in l[1:]:
            spI+=ll[1]
            sp+=ll[1]
        nSp.append(sp)
        spInstant.append(spI)
    dates = sorted(dates)

    fig, ax2 = plt.subplots()
    bar_width = 0.35



    ax2.plot_date(dates, nSp, '-',color="k", lw=1.5)
    ax2.fill_between(dates, 0, nSp, facecolor='yellow', alpha=0.9, lw=0.2)

    # ##############################################
    # ### for steps-post
    # ax2.plot_date(dates, nSp, '-',color="k", lw=1.5, drawstyle='steps-post')
    # d = [dates[0]]   
    # for l in dates[1:]: d.append(l); d.append(l)
    # d.append(dates[len(dates)-1])
    # n = []   
    # for l in nSp: n.append(l); n.append(l)
    # ax2.fill_between(d, 0, n, facecolor='yellow', alpha=0.9, lw=0.2)
    # ##############################################


    for tl in ax2.get_yticklabels():
       tl.set_color('k')
    ax2.set_ylabel("Nombre de pf",color='k')
    ax2.set_xlabel("Date")
    ax2.set_ylim((0, 1.2*max(nSp)))
    ax2.set_xlim((dates[0]-timedelta(10), dates[len(dates)-1]+timedelta(10)))




    ax=ax2.twinx()
    ax.bar(dates, spInstant,  bar_width,
                 alpha=0.9,
                 color='blue',edgecolor = "blue")
    ax.xaxis_date()
    for tl in ax.get_yticklabels():
       tl.set_color('b')
    ax.set_ylabel("Nombre de pf",color='b')
    ax.set_xlabel("Date")
    ax.set_ylim((0, 1.2*max(spInstant)))
    ax.set_xlim((dates[0]-timedelta(10), dates[len(dates)-1]+timedelta(10)))
    fig.autofmt_xdate()
    
    # plt.savefig("results/nSp_spInstant.pdf")
    # plt.savefig("results/nSp_spInstant.png")

    mySave('nSp_spInstant', plt)

    return dates, nSp



def do_sp_instant(pls,sp,ea,df,f):
    dates = []
    nSp = []
    for l in reversed(f):
        dates.append(l[0][1][2])
        sp = 0
        for ll in l[1:]:
            sp+=ll[1]
        nSp.append(sp)
    dates = sorted(dates)

    fig, ax = plt.subplots()
    bar_width = 0.35
    ax.bar(dates, nSp,  bar_width,
                 alpha=0.4,
                 color='b',)
    ax.xaxis_date()
    # ax.fill_between(dates, 0, nSp, facecolor='blue', alpha=0.5)
    plt.xlabel('Date')
    plt.ylabel('Nombre de pf')
    plt.ylim((0, 1.2*max(nSp)))
    plt.xlim((dates[0]-timedelta(10), dates[len(dates)-1]+timedelta(10)))
    ax.grid(True)
    fig.autofmt_xdate()

    # plt.savefig("results/sp_instant.pdf")
    # plt.savefig("results/sp_instant.png")
    mySave('sp_instant', plt)

    return dates, nSp




def do_player(f):
    d = {}
    for l in f:
        gmname = l[0][0]
        if gmname in d.keys():
            d[gmname]+=1
        else:
            d[gmname]=1 
    tmp=[]
    for k,v in d.iteritems():
         tmp.append((k,v))
    tmp =  sorted(tmp, key=lambda student: student[1])

    gm = [l[0] for l in tmp]
    n = [l[1] for l in tmp]

    fig = pylab.figure()
    ax = pylab.Axes(fig, [.1,.3,.85,.6])
    ax.set_xlim(-0.5,len(gm))
    ax.set_ylim(0,1.2*max(n))
    fig.add_axes(ax)
    index = np.arange(len(gm))
    bar_width = 0.35
    rects1 = plt.bar(index, n, bar_width,
                 alpha=0.4,
                 color='b',)
    for tl in ax.get_xticklabels():
       tl.set_rotation(90)
    plt.xticks(index + bar_width/2, gm)
    plt.ylabel('Nombre de GM')
    # plt.savefig("results/player.pdf")
    # plt.savefig("results/player.png")

    mySave('player', plt)



def do_niv(f):
    d = {}
    for l in f:
        gmname = l[0][1][1]
        if gmname in d.keys():
            d[gmname]+=1
        else:
            d[gmname]=1 
    tmp=[]
    for k,v in d.iteritems():
         tmp.append((k,v))
    tmp =  sorted(tmp, key=lambda student: student[1])

    gm = [l[0] for l in tmp]
    n = [l[1] for l in tmp]

    fig, ax = pylab.subplots()
    ax.set_xlim(-0.5,len(gm))
    ax.set_ylim(0,1.2*max(n))
    # fig.add_axes(ax)
    index = np.arange(len(gm))
    bar_width = 0.35
    rects1 = plt.bar(index, n, bar_width,
                 alpha=0.4,
                 color='b',)
    # for tl in ax.get_xticklabels():
       # tl.set_rotation(90)
    plt.xlabel('Niveau du GM')
    plt.ylabel('Nombre de GM')
    plt.xticks(index + bar_width/2, gm)
    # plt.savefig("results/niv.pdf")
    # plt.savefig("results/niv.png")
    mySave('niv', plt)
    

def do_GM(f):
    d = {}
    for l in f:
        gmname = l[0][1][0]
        if gmname in d.keys():
            d[gmname]+=1
        else:
            d[gmname]=1 
    tmp=[]
    for k,v in d.iteritems():
         tmp.append((k,v))
    tmp =  sorted(tmp, key=lambda student: student[1])

    gm = [l[0] for l in tmp]
    n = [l[1] for l in tmp]

    fig = pylab.figure()
    ax = pylab.Axes(fig, [.1,.3,.85,.6])
    ax.set_xlim(-0.5,len(gm))
    ax.set_ylim(0,1.2*max(n))
    fig.add_axes(ax)
    index = np.arange(len(gm))
    bar_width = 0.35
    rects1 = plt.bar(index, n, bar_width,
                 alpha=0.4,
                 color='b',)
    for tl in ax.get_xticklabels():
       tl.set_rotation(90)
    plt.ylabel('Nombre de GM')
    plt.xticks(index + bar_width/2, gm)
    # plt.savefig("results/GM.pdf")
    # plt.savefig("results/GM.png")
    mySave('GM', plt)




def do_player_df(df):
    df =  sorted(df, key=lambda student: student[1])
    ldf = [l[1] for l in df]
    lpl = [l[0] for l in df]

    fig = pylab.figure()
    ax = pylab.Axes(fig, [.1,.3,.85,.6])
    ax.set_xlim(-0.5,len(ldf))
    ax.set_ylim(1.2*min(ldf),1.2*max(ldf))
    fig.add_axes(ax)
    index = np.arange(len(ldf))
    bar_width = 0.35
    rects = plt.bar(index, ldf, bar_width,
                 alpha=0.4,
                 color='b',)

    for r in rects:
        if r.get_y()<0:
           r.set_color('red')
        else:
           r.set_color('blue') 

    for tl in ax.get_xticklabels():
       tl.set_rotation(90)
    plt.ylabel('Nombre de pf')
    plt.xticks(index + bar_width/2., lpl)

    # plt.savefig("results/player_df.pdf")
    # plt.savefig("results/player_df.png")
    mySave('player_df', plt)


def do_player_sp(sp):
    sp =  sorted(sp, key=lambda student: student[1])
    lsp = [l[1] for l in sp]
    lpl = [l[0] for l in sp]

    fig = pylab.figure()
    ax = pylab.Axes(fig, [.1,.3,.85,.6])
    ax.set_xlim(-0.5,len(lsp))
    ax.set_ylim(0,1.2*max(lsp))
    fig.add_axes(ax)
    index = np.arange(len(lsp))
    bar_width = 0.35
    rects1 = plt.bar(index, lsp, bar_width,
                 alpha=0.4,
                 color='b',)
    for tl in ax.get_xticklabels():
       tl.set_rotation(90)
    plt.ylabel('Nombre de pf')
    plt.xticks(index + bar_width/2., lpl)

    # plt.savefig("results/player_sp.pdf")
    # plt.savefig("results/player_sp.png")
    mySave('player_sp', plt)
    
    
    
def do_player_ea(ea):
    ea =  sorted(ea, key=lambda student: student[1])
    lea = [l[1] for l in ea]
    lpl = [l[0] for l in ea]

    fig = pylab.figure()
    ax = pylab.Axes(fig, [.1,.3,.85,.6])
    ax.set_xlim(-0.5,len(lea))
    ax.set_ylim(0,1.2*max(lea))
    fig.add_axes(ax)
    index = np.arange(len(lea))
    bar_width = 0.35
    rects1 = plt.bar(index, lea, bar_width,
                 alpha=0.4,
                 color='b',)
    for tl in ax.get_xticklabels():
       tl.set_rotation(90)
    plt.ylabel('Nombre de pf')
    plt.xticks(index + bar_width/2., lpl)

    # plt.savefig("results/player_ea.pdf")
    # plt.savefig("results/player_ea.png")
    mySave('player_ea', plt)



def do_nGM_nSp(dates, nSp, nGM):

    fig, ax = plt.subplots()

    ax.plot_date(dates, nSp, 'b-')
    ax.set_ylim((0, 1.2*max(nSp)))
    for tl in ax.get_yticklabels():
       tl.set_color('b')
    ax.set_ylabel("Nombre de pf",color='b')
    ax.set_xlabel("Date")
    
    ax2=ax.twinx()
    ax2.plot_date(dates, nGM, 'r-')
    ax2.set_ylim((0, 1.2*max(nGM)))
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    ax2.set_ylabel("Nombre de GM",color='r')

    plt.xlim((dates[0]-timedelta(10), dates[len(dates)-1]+timedelta(10)))
    ax.grid(True)
    fig.autofmt_xdate()

    # plt.savefig("results/nGM_nSp.pdf")
    # plt.savefig("results/nGM_nSp.png")
    mySave('nGM_nSp', plt)


def steppify(arr,isX=False,interval=0):
    """
    Converts an array to double-length for step plotting
    """
    if isX and interval==0:
        interval = abs(arr[1]-arr[0]) / 2.0
        newarr = array(zip(arr-interval,arr+interval)).ravel()
        return newarr

def do_nMembres(pls,sp,ea,df,f):
    dates = []
    nMembres = []
    for l in reversed(f):
        dates.append(l[0][1][2])
        nM = len(l)-1
        nMembres.append(nM)
    dates = sorted(dates)

    fig, ax = plt.subplots()
    ax.plot_date(dates, nMembres,'-', drawstyle='steps-post')
    # ax.plot_date(dates, nMembres,'-')


    ##############################################
    ### for steps-post
    d = [dates[0]]   
    for l in dates[1:]:
       d.append(l)
       d.append(l)
    d.append(dates[len(dates)-1])
    n = []   
    for l in nMembres:
       n.append(l)
       n.append(l)
    ##############################################

    # ax.fill_between(dates, 0, nMembres, facecolor='blue', alpha=0.5)
    ax.fill_between(d, 0, n, facecolor='blue', alpha=0.5)



    plt.xlabel('Date')
    plt.ylabel('Nombre de membres')
    plt.ylim((0,1.2*max(nMembres)))
    plt.xlim((dates[0]-timedelta(10), dates[len(dates)-1]+timedelta(10)))
    ax.grid(True)
    fig.autofmt_xdate()
    # plt.savefig("results/nMembres.pdf")
    # plt.savefig("results/nMembres.png")
    mySave('nMembres', plt)

    return dates, nMembres



def do_nSp(pls,sp,ea,df,f):
    dates = []
    nSp = []
    sp = 0
    for l in reversed(f):
        dates.append(l[0][1][2])
        for ll in l[1:]:
            sp+=ll[1]
        nSp.append(sp)
    dates = sorted(dates)

    fig, ax = plt.subplots()
    ax.plot_date(dates, nSp, '-')
    ax.fill_between(dates, 0, nSp, facecolor='blue', alpha=0.5)
    plt.xlabel('Date')
    plt.ylabel('Nombre de pf')
    plt.ylim((0, 1.2*max(nSp)))
    plt.xlim((dates[0]-timedelta(10), dates[len(dates)-1]+timedelta(10)))
    ax.grid(True)
    fig.autofmt_xdate()

    # plt.savefig("results/nSp.pdf")
    # plt.savefig("results/nSp.png")

    # mySave('nSp', plt)

    return dates, nSp





