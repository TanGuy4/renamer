import os, sys, re
import time
import tkinter
import tkinter.messagebox
import tkinter.filedialog
window=tkinter.Tk()
window.title('ReNameR 2.0 by TanGuy')
paths=['C:/Exemple/']
files=['sample.txt']
new_files=['sample.txt']
ext='<EXT>'
_ext='<.EXT>'
name='<NAME>'
folder='<DIR>'
folderbis='<.>'
parent='<DIR_PARENT>'
parentbis='<..>'
foldern=r'<DIR\*\d+>'
firstchar=r'<\*\d+>'
lastchar=r'<\d+\*>'
namchar=r'<\d+\*\*\d+>'
charn=r'<\*\d+\*>'
prt=r'<PRT#+>'
prtn=r'<\d+\*PRT#+>'
lowercase=r'<LOWER\[[^\]>]+\]{1,1}>{1,1}'
uppercase=r'<UPPER\[[^\]>]+\]{1,1}>{1,1}'
capitalize=r'<CAP\[[^\]>]+\]{1,1}>{1,1}'
LEFT=tkinter.LEFT
RIGHT=tkinter.RIGHT
TOP=tkinter.TOP
BOTTOM=tkinter.BOTTOM
GROOVE=tkinter.GROOVE
NO_CURSOR='no' if sys.platform=='win32' else 'X_cursor' # 'no' n'existe que sous Windows

def clear_fileslist():
    files.clear()
    files.append('sample.txt')
    paths.clear()
    paths.append('C:/Exemple/')
    new_files.clear()
    new_files.append('sample.txt')
    ListFiles.delete(0,ListFiles.size())
    ListNewFiles.delete(0,ListNewFiles.size())
    Status.config(text='')
    return

def apropos():
    tkinter.messagebox.showinfo('À propos de ReNameR','ReNameR 2.0\nby TanGuy')
    return

def expressions_help():
    tkinter.messagebox.showinfo('Aide sur les expressions',"<NAME> = nom originel du fichier (sans l'extension)\n<DIR> / <.> = le nom du dossier dans lequel se trouve le fichier à renommer\n<DIR_PARENT> / <..> = le dossier parent du dossier dans lequel se trouve le fichier à renommer\n<DIR*n> = le nom du nième dossier parent\n<*n> = les premiers caractères du nom originel\n<n*> = les derniers caractères du nom originel\n<n**m> = caractères n à m du nom originel\n<*n*> = caractère n du nom originel\n<PRT##> = nombres de parties avec autant de chiffres que de '#'\n<n*PRT##> = nombres de parties avec autant de chiffres que de '#' à partir de n\n<EXT> = extension originelle sans le point\n<.EXT> = extension originelle avec le point\n<UPPER[texte]> = texte en majuscules\n<LOWER[texte]> = texte en minuscules\n<CAP[texte]> = texte avec une majuscule au début")
    return

def filesname(i):
    p=paths[i]
    b=p.count('/')
    bb=0
    name=''
    for c in range(len(p)):
        if p[c] =='/':
            bb=bb+1
        if bb==b:
            name=name+p[c]
    name=name.replace('/','')
    files.append(name)
    path=p.replace(name,'')
    paths[i]=path
    return

def openfile():
    filename=tkinter.filedialog.askopenfilename(title="Ajouter des fichiers à renommer",multiple=True)
    for p in filename:
        f=int(len(files))
        paths.append(p)
        filesname(f)
        new_files.append('')
        ListFiles.insert(f,files[f])
        if  ('' in files) and ('' in paths) and ('' in new_files):
            while '' in files:
                files.remove('')
            while '' in paths:
                paths.remove('')
            while '' in new_files:
                new_files.remove('')
    apercu()
    return

def retirefile():
    if len(files)==1:
        tkinter.messagebox.showerror('Ajoutez au moins un fichier','Veuillez au moins ajouter un fichier à renommer au préalable')
        return
    s=ListFiles.curselection()
    if s==():
        tkinter.messagebox.showerror('Sélectionnez un fichier','Veuillez sélectionner un fichier dans la liste des fichiers à renommer au préalable')
        return
    d=tkinter.messagebox.askyesnocancel('Êtes-vous sûr(e) de vouloir faire cela ?','Êtes-vous sûr(e) de vouloir retirer\n{}\nde la liste des fichiers à renommer ?'.format(paths[s[0]+1]+files[s[0]+1]))
    if d==1:
        paths[s[0]+1]=''
        files[s[0]+1]=''
        new_files[s[0]+1]=''
        ListNewFiles.delete(s[0])
        ListFiles.delete(s[0])
        if  ('' in files) and ('' in paths) and ('' in new_files):
            while '' in files:
                files.remove('')
            while '' in paths:
                paths.remove('')
            while '' in new_files:
                new_files.remove('')
    apercu()
    return

def renamesample():
    l=rename('s')
    text1='Le fichier : \n'+paths[0]+files[0]
    text2='Sera renommé en : \n'+paths[0]+l
    File1.config(text=text1)
    File2.config(text=text2)
    return

def renames():
    if len(files)==1:
        tkinter.messagebox.showerror('Ajoutez au moins un fichier','Veuillez au moins ajouter un fichier dans la liste des fichiers à renommer au préalable')
        return
    for i in range(1,len(files)):
        rename(i,True)
        Status.config(text='{0} fichier(s) renommé(s) sur {1}'.format(i, len(files)-1))
    tkinter.messagebox.showinfo('Terminé','Tous les fichiers ont été renommés.')
    return

def apercu(a=None,b=None,c=None):
    renamesample()
    if len(files)==1:
        return
    for i in range(1,len(files)):
        rename(i)
    return

def rename(fbis='s',apply=False):
    fbisbis=fbis
    if fbis=='s':
        fbisbis=0
    file=str(files[fbisbis])
    filename=''
    l=str(Pattern.get())
    extension=''
    dot=file.count('.')
    b=0

# définit l'extension du fichier original
    for i in range(len(file)):
        if file[i]=='.':
            b=b+1
        if b==dot and dot>0: # sans point : pas d'extension
            extension=extension+file[i]
        else:
            filename=filename+file[i]
    extension=extension.replace('.','')

# pour les fichiers à parties
    prts=re.findall(prt, l)

    for i in range(len(prts)):
        prtbis=prts[i].replace('<','<1*')
        l=l.replace(prts[i],prtbis)
    
    prtns=re.findall(prtn, l)
    for i in range(len(prtns)):
        p=prtns[i].count('#')
        n=re.findall('\d+\*',prtns[i])
        n=str(n).replace('[','').replace(']','').replace('*','').replace('\'','').replace(' ','')
        o=str(fbisbis+(int(n)-1))
        pbis=p-len(o)
        if pbis<0:
            pbis=0
        l=l.replace(prtns[i], '0'*pbis+o)

    # nouvelle version 22/02/2020 (suite à l'implémentation des numéros de parties à partir de n, les n derniers caractères ne fonctionnaient plus ; ci-dessous la nouvelle version pour les premiers caractères, les derniers caractères et le n à m caractères)
    firsts=re.findall(firstchar,l) # liste qui contient tous les <*n>
    lasts=re.findall(lastchar, l) # liste qui contient tous les <n*>
    nams=re.findall(namchar, l) # liste qui contient tous les <n**m>
    nchars=re.findall(charn, l) # liste qui contient tous les <*n*>

    if folder in l:
        l=l.replace(folder,'<DIR*0>')
    
    if folderbis in l:
        l=l.replace(folderbis, '<DIR*0>')
    
    if parent in l:
        l=l.replace(parent,'<DIR*1>')
    
    if parentbis in l:
        l=l.replace(parentbis,'<DIR*1>')

    nfolders=re.findall(foldern, l) # liste qui contient tous les <DIR*n>

    for i in range(len(firsts)):
        n=re.findall('\d+',firsts[i])
        n=str(n).replace('[','').replace(']','').replace('\'','').replace(' ','')
        l=l.replace(firsts[i],filename[:int(n)])
    
    for i in range(len(lasts)):
        n=re.findall('\d+',lasts[i])
        n=str(n).replace('[','').replace(']','').replace('\'','').replace(' ','')
        l=l.replace(lasts[i],filename[- int(n):] if int(n)>0 else '')
    
    for i in range(len(nams)):
        n=re.findall('\d+\*',nams[i])
        m=re.findall('\*\d+',nams[i])
        n=str(n).replace('[','').replace(']','').replace('\'','').replace(' ','').replace('*','')
        m=str(m).replace('[','').replace(']','').replace('\'','').replace(' ','').replace('*','')
        l=l.replace(nams[i],filename[max(int(n)-1,0):int(m)])
    
    for i in range(len(nchars)):
        n=re.findall('\d+',nchars[i])
        n=str(n).replace('[','').replace(']','').replace('\'','').replace(' ','')
        l=l.replace(nchars[i],filename[int(n)-1] if 0<int(n)<=len(filename) else '')
    
    for i in range(len(nfolders)):
        n=re.findall('\d+',nfolders[i])
        n=str(n).replace('[','').replace(']','').replace('\'','').replace(' ','')
        p=paths[fbisbis].split('/')
        if (2+int(n)-1)<len(p):
            p=p[-2-int(n)]
            l=l.replace(nfolders[i], p)
        else:
            l=l.replace(nfolders[i],'')


# remplacement des expressions par leurs valeurs
    if ext in l:
        l=l.replace(ext,extension)
    
    if _ext in l:
        l=l.replace(_ext,'.'+extension if extension else '')
    
    if name in l:
        l=l.replace(name, filename)
    
    uppercases=re.findall(uppercase, l)
    lowercases=re.findall(lowercase, l)
    capitalizes=re.findall(capitalize, l)

    for i in range(len(uppercases)):
        m=uppercases[i].replace('<UPPER[','',1)
        m=m.replace(']>','',1)
        l=l.replace(uppercases[i],m.upper())

    for i in range(len(lowercases)):
        m=lowercases[i].replace('<LOWER[','',1)
        m=m.replace(']>','',1)
        l=l.replace(lowercases[i],m.lower())
    
    for i in range(len(capitalizes)):
        m=capitalizes[i].replace('<CAP[','',1)
        m=m.replace(']>','',1)
        l=l.replace(capitalizes[i],m.capitalize())
        l=l.replace('<cap[','<CAP[')
    



    if l=='':
        l=files[fbisbis]
    if fbis=='s':
        return l
    else:
        p=paths[fbisbis]+files[fbisbis]
        pbis=paths[fbisbis]+l
        new_files[fbisbis]=l
        ListNewFiles.insert(fbisbis-1, new_files[fbisbis])
        ListNewFiles.delete(fbisbis)
        if apply:
            os.renames(p,pbis) 
        return

# Menu
menubar=tkinter.Menu(window)

menufile=tkinter.Menu(menubar,tearoff=0)
menufile.add_command(label='Ajouter un fichier',command=openfile)
menufile.add_command(label='Retirer le fichier',command=retirefile)
menufile.add_command(label='Effacer la liste des fichiers',command=clear_fileslist)
menufile.add_separator()
menufile.add_command(label='Aperçu des nouveaux noms des fichiers',command=apercu)
menufile.add_command(label='Renommer les fichiers',command=renames)
menufile.add_separator()
menufile.add_command(label='Quitter',command=window.destroy)
menubar.add_cascade(label='Fichier',menu=menufile)


menuhelp=tkinter.Menu(menubar,tearoff=0)
menuhelp.add_command(label='Aide sur les expressions',command=expressions_help)
menuhelp.add_separator()
menuhelp.add_command(label='À propos',command=apropos)
menubar.add_cascade(label='Aide', menu=menuhelp)

window.config(menu=menubar)

# Liste des fichiers
FrameFiles=tkinter.Frame(window)
FrameFiles.pack(side=LEFT)
ButtonFrameFiles1=tkinter.Frame(FrameFiles)
ButtonFrameFiles1.pack(side=TOP)
ButtonFrameFiles2=tkinter.Frame(FrameFiles)
ButtonFrameFiles2.pack(side=BOTTOM)
ButtonFileAdd=tkinter.Button(ButtonFrameFiles1,text='Ajouter un fichier',command=openfile,cursor='plus')
ButtonFileAdd.pack(side=LEFT,padx=10,pady=10)
ButtonFileRetire=tkinter.Button(ButtonFrameFiles1,text='Retirer le fichier',command=retirefile,cursor=NO_CURSOR)
ButtonFileRetire.pack(side=LEFT,padx=10,pady=10)
ButtonClearList=tkinter.Button(ButtonFrameFiles1,text='Effacer la liste de fichiers',command=clear_fileslist)
ButtonClearList.pack(side=LEFT,padx=10,pady=10)
FrameListFiles=tkinter.LabelFrame(FrameFiles,borderwidth=2,relief=GROOVE,text='Fichiers à renommer')
FrameListFiles.pack(side=LEFT,padx=10,pady=10)
FrameListNewFiles=tkinter.LabelFrame(FrameFiles,borderwidth=2,relief=GROOVE,text='Nouveau Nom')
FrameListNewFiles.pack(side=LEFT,padx=10,pady=10)
ListFiles=tkinter.Listbox(FrameListFiles,bg='white',width=30,height=25)
ListFiles.pack()
ListNewFiles=tkinter.Listbox(FrameListNewFiles,bg='white',width=30,height=25)
ListNewFiles.pack()
ButtonFileAdd=tkinter.Button(ButtonFrameFiles2,text='Ajouter un fichier',command=openfile,cursor='plus')
ButtonFileAdd.pack(side=LEFT,padx=10,pady=10)
ButtonFileRetire=tkinter.Button(ButtonFrameFiles2,text='Retirer le fichier',command=retirefile,cursor=NO_CURSOR)
ButtonFileRetire.pack(side=LEFT,padx=10,pady=10)
ButtonClearList=tkinter.Button(ButtonFrameFiles2,text='Effacer la liste de fichiers',command=clear_fileslist)
ButtonClearList.pack(side=LEFT,padx=10,pady=10)

# Options de renommage
Pattern=tkinter.StringVar()
FrameRename=tkinter.Frame(window)
FrameRename.pack(side=LEFT)
ButtonFrameRename1=tkinter.Frame(FrameRename)
ButtonFrameRename1.pack(side=TOP)
ButtonFrameRename2=tkinter.Frame(FrameRename)
ButtonFrameRename2.pack(side=BOTTOM)
ButtonApercu=tkinter.Button(ButtonFrameRename1,text='Aperçu',command=apercu)
ButtonApercu.pack(side=LEFT,padx=10,pady=10)
ButtonRename=tkinter.Button(ButtonFrameRename1,text='Renommer les fichiers',cursor='pencil',command=renames)
ButtonRename.pack(side=LEFT,padx=10,pady=10)
tkinter.Label(FrameRename,text="""<NAME> = nom originel du fichier (sans l'extension)
<DIR> / <.> = nom du dossier dans lequel se trouve le fichier à renommer
<DIR_PARENT> / <..> = nom du dossier parent à celui dans lequel se trouve le fichier à renommer
<DIR*n> = nom du nième dossier parent
<*n> = les premiers caractères du nom originel
<n*> = les derniers caractères du nom originel
<n**m> = caractères n à m du nom originel
<*n*> = le caractère n du nom originel
<PRT##> = nombres de parties avec autant de chiffres que de '#'
<n*PRT##> = nombres de parties avec autant de chiffres que de '#' à partir de n
<EXT> = extension originelle sans le point
<.EXT> = extension originelle avec le point
<UPPER[texte]> = texte en majuscules
<LOWER[texte]> = texte en minuscules
<CAP[texte]> = texte avec une majuscule au début
""").pack()
FramePattern=tkinter.Frame(FrameRename)
FramePattern.pack(pady=5)
tkinter.Label(FramePattern,text='Pattern/Modèle : ').pack(side=LEFT)
tkinter.Entry(FramePattern,width=60,textvariable=Pattern).pack(side=LEFT)
FrameSample=tkinter.LabelFrame(FrameRename,borderwidth=2,relief=GROOVE,text='Résultat : ')
FrameSample.pack(pady=5)
File1=tkinter.Label(FrameSample,text='Le fichier : \n')
File1.pack(pady=5)
File2=tkinter.Label(FrameSample,text='Sera renommé en : \n')
File2.pack(pady=5)
ButtonApercu=tkinter.Button(ButtonFrameRename2,text='Aperçu',command=apercu)
ButtonApercu.pack(side=LEFT,padx=10,pady=10)
ButtonRename=tkinter.Button(ButtonFrameRename2,text='Renommer les fichiers',cursor='pencil',command=renames)
ButtonRename.pack(side=LEFT,padx=10,pady=10)
FrameStatus=tkinter.Frame(FrameRename)
FrameStatus.pack(side=BOTTOM,padx=10,pady=10)
Status=tkinter.Label(FrameStatus, text='')
Status.pack(padx=10,pady=10)

Pattern.trace_add("write",apercu)

window.mainloop()
