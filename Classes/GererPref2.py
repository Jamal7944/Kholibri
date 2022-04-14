## Projet DUT2 Soft de génération de feuilles d'exercices
import codecs
import os
import tkinter
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *

from Classes import MyThread, Utils
from SGBD.exceptions import SGBDException

"""
Classe contenant l'architecture de base d'une fenêtre, le nom de la classe correspond au nom de la fenêtre
"""
class GererPref2(Frame):
    def __init__(self, parent, controller):
        import SGBD
        self.SGBD = SGBD.SGBD

        Frame.__init__(self, parent)

        self.controller = controller
        self.enonce = []
        self.enseignant = []

        self.PreferenceTexte = Label(self, text="Création d'un profil ", font=controller.title_font)

        ######################################################################################################################
        # correspond au cadre contenant le radio button de choix de mode
        self.cadre_choixMode = LabelFrame(self, text="Mode d'ajout")

        self.choixNbExos = IntVar()
        self.choixNbExos.set(1)
        self.RadioButtonUnExo = Radiobutton(self.cadre_choixMode, text="Modification d'un profil ",
                                            variable=self.choixNbExos, value=0, command=self.SwitchView)
        self.RadioButtonNExo = Radiobutton(self.cadre_choixMode, text="Ajout d'un nouvel utilisateur",
                                           variable=self.choixNbExos, value=1, command=self.SwitchView)

        self.RadioButtonNExo.pack(side=LEFT)
        self.RadioButtonUnExo.pack(side=LEFT)

        ######################################################################################################################
        # Modification de preférences

        self.ModifPref = Frame(self)
        self.CadreRelou = Frame(self.ModifPref)

        AuteurTexte = Label(self.CadreRelou, text="Sélectionner les préférences par auteur:", font=("Helvetica", 10))
        AuteurTexte.pack(padx=10, side=LEFT)

        self.cbAuteurs = Combobox(self.CadreRelou, values=self.SGBD.giveAuteur(), state='readonly')
        if (Utils.Utils.DefaultUser != ""):
            self.cbAuteurs.set(Utils.Utils.DefaultUser)
        else:
            self.cbAuteurs.set('Choisir un auteur')
        self.cbAuteurs.pack(pady=5, side=LEFT)
        self.cbAuteurs.bind('<<ComboboxSelected>>', lambda event: self.ActualiseBouton())

        RaccourciTexte = Label(self.CadreRelou, text="Indiquer le raccourcis et la commande à ajouter",
                               font=("Helvetica", 10))
        RaccourciTexte.pack(pady=5, padx=10, side=LEFT)

        self.champNom = Entry(self.CadreRelou)
        self.champNom.pack(pady=5, side=LEFT)

        ValiderBoutton = Button(self.CadreRelou, text="Valider", command=lambda: self.ajouterChapitre())
        ValiderBoutton.pack(pady=5, side=LEFT)

        self.CadreRelou.pack()

        self.Pref = Button(self.ModifPref, text="Afficher l'ensemble des préférences pour cet auteur",
                           command=self.afficherPref)
        self.Pref.pack(pady=5, side=BOTTOM)
        self.Pref["state"] = "disabled"

        ######################################################################################################################
        # Liste des raccourcis existants

        self.ListeRaccourci = Frame(self)

        Label(self.ListeRaccourci, text="Liste des raccourcis:", font=("Helvetica", 10)).pack(padx=10, side=TOP)

        self.ChampListePref = Listbox(self.ListeRaccourci, selectmode="multiple", width=120)
        self.ChampListePref.pack(padx=5, pady=5, expand=YES, fill="both", side=LEFT)

        ######################################################################################################################
        # Ajouter un fichier
       # s = Style()
       # s.configure('My.TFrame', background='red')

        self.CréerUtilisateur = Frame(self)

        self.test = Frame(self.CréerUtilisateur)


        Label(self.test, text=r"Nom de l'enseignant : ", font=('Helvetica', 11)).pack(side=LEFT)
        self.sv = StringVar()
        self.sv.set("")
        self.NomEnseignant = Entry(self.test,font=('Helvetica', 11), textvariable=self.sv, validate="all")

        self.NomEnseignant.pack(padx=7, side=LEFT)

        Label(self.test, text=r"Établissement : ", font=('Helvetica', 11)).pack(side=LEFT)
        self.sv2 = StringVar()
        self.sv2.set("")
        self.Etablissement = Entry(self.test,font=('Helvetica', 11), textvariable=self.sv2, validate="all")
        self.Etablissement.pack(padx=7, side=LEFT)
        self.test.pack(side=TOP, pady=2)

        self.test2 = Frame(self.CréerUtilisateur)
        self.test2.pack(side=TOP, pady=20)
        self.champEnseignant = Entry(self.CréerUtilisateur)

        self.openinfo = Frame(self.test2)

        OuvrirBouton = tkinter.Button(self.openinfo,relief="raised",height=1, text="Insérer votre feuille de style ",font=('Helvetica', 11), command=lambda: self.open_file(0))
        OuvrirBouton.pack(side=LEFT)

        Infobouton = tkinter.Button(self.openinfo,text="Info",font=('Helvetica', 11),relief="raised",width=10,command=lambda: self.giveInfo())
        Infobouton.pack(side=LEFT, padx=50)

        self.openinfo.pack(side=BOTTOM)



        self.champfeuillestyle = tkinter.Text(self.CréerUtilisateur,relief="sunken", width=220, height=110, bg="#E5E5E5", fg="black",
                                insertbackground="black",
                                font="Helvetica 10", undo=True)
        self.champfeuillestyle.tag_configure("orange", foreground="#F97718", font="Helvetica 10")
        self.champfeuillestyle.tag_configure("yellow", foreground="#FD00B0", font="Helvetica 10")
        self.champfeuillestyle.tag_configure("blue", foreground="blue", font="Helvetica 10")
        self.champfeuillestyle.tag_configure("green", foreground="green", font="Helvetica 10")
        self.champfeuillestyle.tag_configure("red", foreground="red", font="Helvetica 10")
        self.champfeuillestyle.tag_configure("purple", foreground="#00AF7A",
                                       font="Helvetica 10")  # en dernier pour overwrite les commentaires
        self.champfeuillestyle.tag_configure("white", foreground="black", font="Helvetica 10")
        self.champfeuillestyle.bind("<Key>", lambda event: self.updatecode(self.champfeuillestyle))
        self.framevalider = Frame(self.CréerUtilisateur)
        self.SuivantBouton = tkinter.Button(self.framevalider, text="Valider profil",relief="groove", height=3,font=('Helvetica', 10), command=lambda: [self.creer_repertoire_utilisateur()])

        self.Compilationtest = tkinter.Button(self.framevalider, text="Compiler", relief="groove", height=3,
                                            font=('Helvetica', 10),
                                            command=lambda: [self.compiler(self.champfeuillestyle.get("1.0", "end-1c"))])


        self.infos = Frame(self.framevalider)
        self.infostudent = tkinter.Label(self.infos, text=r"La variable concernant les étudiants est \students  ", font=('Helvetica', 11))
        self.infostudent.pack(side=BOTTOM)
        self.infocours = tkinter.Label(self.infos, text=r"L'environnement pour la question de cours est ...{cours}  ",
                                         font=('Helvetica', 11))
        self.infocours.pack(side=BOTTOM)
        self.infoexo = tkinter.Label(self.infos,text=r"L'environnement pour les énoncés est ...{exo}  ", font=('Helvetica', 11))
        self.infoexo.pack(side=BOTTOM)
        self.infosol = tkinter.Label(self.infos,
                                         text=r"L'environnement pour les solutions est ...{sol}  ",
                                         font=('Helvetica', 13))
        self.infosol.pack(side=BOTTOM)

        self.Compilationtest.pack(side=LEFT, padx=200)
        self.infos.pack(side=LEFT,padx=10)
        self.SuivantBouton.pack(side=RIGHT, padx=200)

        self.framevalider.pack(side=BOTTOM, pady=20)

        self.champfeuillestyle.pack(padx=20, side=BOTTOM)



        self.tags = ["red", "green", "yellow", "orange", "blue", "purple", "white"]

        self.wordlist = [
            [r"\newcommand", r"\begin", r"\end", r"\renewcommand", r"\DeclareMathOperator", r"\usepackage"],
            [r"\classe", r"\annee"],
            ["$", r"\[", r"\]"],
            ["exercice", "enumerate", "array", "question", "center", "tikzpicture", "scale"],
            ["geometry", "amsart", "titlesec"]]

        ######################################################################################################################
        # Pref difficulte + finalisation profil
        self.test3 = Frame(self.test2)
        Label(self.test3, text="Selectionner vos quantités d'exercices: ", font=("Helvetica", 11)).pack(pady=5, padx=5, side=TOP)

        Label(self.test3, text="Difficulté 1: ", font=("Helvetica", 11)).pack(pady=5, padx=5, side=LEFT)
        self.cbDiff1 = Combobox(self.test3, values=list([0,1,2,3,4,5]), state='readonly')
        self.cbDiff1.bind('<<ComboboxSelected>>', lambda event: self.Updatevaliderbouton())
        self.cbDiff1.set(0)
        self.cbDiff1.pack(pady=5, padx=5, side=LEFT)

        Label(self.test3, text="Difficulté 2: ", font=("Helvetica", 11)).pack(pady=5, padx=5, side=LEFT)
        self.cbDiff2 = Combobox(self.test3, values=list([0,1,2,3,4,5]), state='readonly')
        self.cbDiff2.bind('<<ComboboxSelected>>', lambda event: self.Updatevaliderbouton())
        self.cbDiff2.set(0)
        self.cbDiff2.pack(pady=5, padx=5, side=LEFT)


        Label(self.test3, text="Difficulté 3: ", font=("Helvetica", 11)).pack(pady=5, padx=5, side=LEFT)
        self.cbDiff3 = Combobox(self.test3, values=list([0,1,2,3,4,5]), state='readonly')
        self.cbDiff3.bind('<<ComboboxSelected>>', lambda event: self.Updatevaliderbouton())
        self.cbDiff3.set(0)
        self.cbDiff3.pack(pady=5, padx=5, side=LEFT)


        Label(self.test3, text="Difficulté 4: ", font=("Helvetica", 11)).pack(pady=5, padx=5, side=LEFT)
        self.cbDiff4 = Combobox(self.test3, values=list([0,1,2,3,4,5]), state='readonly')
        self.cbDiff4.bind('<<ComboboxSelected>>', lambda event: self.Updatevaliderbouton())
        self.cbDiff4.set(0)
        self.cbDiff4.pack(pady=5, padx=5, side=LEFT)


        Label(self.test3, text="Difficulté 5: ", font=("Helvetica", 11)).pack(pady=5, padx=5, side=LEFT)
        self.cbDiff5 = Combobox(self.test3, values=list([0,1,2,3,4,5]), state='readonly')
        self.cbDiff5.bind('<<ComboboxSelected>>', lambda event: self.Updatevaliderbouton())
        self.cbDiff5.set(0)
        self.cbDiff5.pack(pady=5, padx=5, side=LEFT)





        self.test3.pack(side=TOP)


        ######################################################################################################################
        # Menu


        self.ShowFrame([self.CréerUtilisateur])


    def SwitchView(self):

        if self.choixNbExos.get() == 0:
            self.PreferenceTexte['text']="Gestion des utilisateurs "

            self.Pref["text"] = "Afficher l'ensemble des raccourcis"
            self.ShowFrame([self.ModifPref])
        else:
            self.PreferenceTexte['text']="Création d'un profil"
            self.ShowFrame([self.CréerUtilisateur])

    def ShowFrame(self, to_show):
        for widget in self.winfo_children():
            widget.pack_forget()

        self.PreferenceTexte.pack(side="top", fill="x", pady=10)

        self.cadre_choixMode.pack(side=TOP)

        for frame in to_show:
                frame.pack()


    def afficherPref(self):  # fonction permettant d'afficher les préférences (new commands seulement) d'un utilisateur depuis la base de données

        if self.ListeRaccourci.winfo_manager():
            self.ShowFrame([self.ModifPref])
            self.Pref["text"] = "Afficher l'ensemble des raccourcis"

        else:
            self.ShowFrame([self.ModifPref, self.ListeRaccourci])

            self.Pref["text"] = "Cacher l'ensemble des raccourcis"

            self.ChampListePref.delete(0, 'end')
            liste = self.SGBD.GivePrefFromAutor(self.cbAuteurs.get())

            for shortcuts in liste:
                self.ChampListePref.insert(1, (shortcuts[0] + "   " + shortcuts[1] + "\n"))

    def ActualiseBouton(self):
        self.Pref["state"] = "normal"


    def ValiderFichierPref(self):  # fonction permettant d'ajouter dans la base les nouvelles préférences selon un auteur

        self.style = self.champfeuillestyle.get("1.0", "end-1c")
        self.auteur = self.NomEnseignant.get()
        self.etablissement = self.Etablissement.get()



        tab = self.remplissageCommand(self.style)
        self.SGBD.InsertAUTEUR(self.auteur,self.etablissement)
        for command in tab:
            try:
                commandeauteur = self.giveComShort(command)[1]
                raccourcisauteur = self.giveComShort(command)[0]
                self.SGBD.InsertShortcuts(self.giveComShort(command)[1], self.auteur, self.giveComShort(command)[0])


            except RuntimeError as e:
                messagebox.showerror(title="Il y a un petit problème", message=e.message)
                return
                self.SGBD.InsertShortcuts(commandeauteur, self.auteur,raccourcisauteur )



        self.cbAuteurs['values'] = self.SGBD.giveAuteur()
        messagebox.showinfo(title="Info", message="Utilisateur crééé")

    def open_file(self, var):  # fonction permettant d'ouvrir un fichier de préférences
        filepath = askopenfilename(filetypes=[("Document Tex", "*.tex")])

        if not filepath:
            return
        if var == 0:
            self.champfeuillestyle.delete(1.0, END)
        if var == 1:
            self.raccourcis.delete(1.0,END)

        with codecs.open(filepath, "r", encoding="utf-8", errors='replace') as input_file:
            text = input_file.read()
            if var == 0:
                self.champfeuillestyle.insert(END, text)
                self.updatecode(self.champfeuillestyle)
            if var == 1:
                self.raccourcis.insert(END,text)
                self.updatecode(self.raccourcis)


    def remplissageCommand(self, contenu):  # fonction permettant de récupérer les new commands
        tab = []

        lines = contenu.splitlines()
        for var in lines:
            if '\\newcommand' in var and '%\\newcommand' not in var and '\\begin{array}' not in var:
                tab.append(var)

        return tab

    def giveComShort(self, chaine):  # fonction permettant de séparer la commande et la new command
        import re

        pos1 = chaine.find('{') + 1
        pos2 = chaine.find('}')
        pattern = re.compile(
            r'\\newcommand{(\\[\w]*)}(\[\d*\])*{(?:([\w\\]*{\w*}({[\w# ]*})*)|([\w\\]*{A}\^2_{\\[\w]*})|(\\mathbb{\w*})|([^{}]*))}')

        rez = pattern.match(chaine)
        g1 = rez.group(1)
        g2 = rez.group(3) if rez.group(2) == None else rez.group(2)
        if (g2 == None):
            g2 = rez.group(4)

        if (g2 == "[1]"):
            g2 = rez.group(3)

        if (rez.group(7) != None):
            g2 = rez.group(7)

        if (rez.group(5) != None):
            g2 = rez.group(5)

        return g1, g2

    def giveInfo(self):
        messagebox.showinfo(title="Informations",
                            message="Veuillez entrer l'ensemble de votre de style (raccourcis inclus). Insérer du contenu pour tester votre feuille.")

    def tagHighlight(self, champ):
        start = "1.0"
        end = "end"

        for mylist in self.wordlist:
            num = int(self.wordlist.index(mylist))

            for word in mylist:
                champ.mark_set("matchStart", start)
                champ.mark_set("matchEnd", start)
                champ.mark_set("SearchLimit", end)

                mycount = IntVar()

                while True:
                    index = champ.search(word, "matchEnd", "SearchLimit", count=mycount, regexp=False)

                    if index == "": break
                    if mycount.get() == 0: break

                    champ.mark_set("matchStart", index)
                    champ.mark_set("matchEnd", "%s+%sc" % (index, mycount.get()))

                    preIndex = "%s-%sc" % (index, 1)  # placeholder ( un peu comme en C )
                    postIndex = "%s+%sc" % (index, mycount.get())

                    if self.check(champ, index, preIndex, postIndex):
                        champ.tag_add(self.tags[num], "matchStart", "matchEnd")
                    else:
                        champ.tag_add(self.tags[6], "matchStart", "matchEnd")

    def check(self, champ, index, pre, post):
        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
                   "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

        if champ.get(pre) == champ.get(index):
            pre = index
        else:
            if champ.get(pre) in letters:
                return 0

        if champ.get(post) in letters:
            return 0

        return 1

    def scan(self, champ):
        start = "1.0"
        end = "end"
        mycount = IntVar()

        regex_patterns = [r'%.*', r'$(\w+)$']  # pour les commentaires

        for pattern in regex_patterns:
            champ.mark_set("start", start)
            champ.mark_set("end", end)

            num = int(regex_patterns.index(pattern))

            while True:
                index = champ.search(pattern, "start", "end", count=mycount, regexp=True)

                if index == "": break

                if (num == 0):
                    champ.tag_add(self.tags[5], index, index + " lineend")

                champ.mark_set("start", "%s+%sc" % (index, mycount.get()))

    def updatecode(self, champ):
        self.tagHighlight(champ)
        self.scan(champ)

    def creer_repertoire_utilisateur(self):
        # Création des fichiers
        var = False

        try:

            if not os.path.exists("SGBD/utilisateurs"):

                os.makedirs("SGBD/utilisateurs")

            if len(self.NomEnseignant.get().split()) == 0:
                messagebox.showerror(title="Error", message="Impossible de créer l'utilisateurs (nom d'utilisateur vide).")
                return

            if len(self.Etablissement.get().split()) == 0:
                messagebox.showerror(title="Error", message="Impossible de créer l'utilisateurs (Etablissement vide).")
                return

            if not self.Updatevaliderbouton():
                messagebox.showerror(title="Error",
                                     message="Impossible de créer l'utilisateurs. Veuillez positionner au moins une valeur d'exercices ")
                return

            if len(self.champfeuillestyle.get("1.0", "end-1c"))==0:
                messagebox.showerror(title="Error",
                                     message="Impossible de créer l'utilisateur (Veuillez insérer votre feuille de style).")
                return



            if os.path.exists("SGBD/utilisateurs/" + self.NomEnseignant.get()):
                messagebox.showerror(title="Error", message="Utilisateur déjà existant")
                return
            if not os.path.exists("SGBD/utilisateurs/" + self.NomEnseignant.get()):
                choice = messagebox.askyesnocancel("Info", "Voulez vous vraiment créer cet utilisateur?")
                if(choice) :
                    os.makedirs("SGBD/utilisateurs/" + self.NomEnseignant.get())
                    os.makedirs("SGBD/utilisateurs/"+self.NomEnseignant.get()+"/temp/")
                    f = open("SGBD/utilisateurs/" + self.NomEnseignant.get() + "/style.tex", "a", encoding="utf-8",
                             errors='replace')
                    enonce = self.champfeuillestyle.get("1.0", END)
                    style = enonce.splitlines()
                    for var in style:
                        f.write(var)
                        f.write("\n")
                    f.close()
                    var = True
        except:
            messagebox.showerror(title="Error", message="Erreur lors de la création du dossier utilisateur")
            return
        if var:
            choice = messagebox.askyesno("Info", "Voulez vous définir cet utilisateur par défaut ?")
            if choice:
                Utils.DefaultUser = self.NomEnseignant.get()
            self.ValiderFichierPref()


    def Updatevaliderbouton(self):
        if self.cbDiff5.get() == "0" and self.cbDiff4.get() == "0" and self.cbDiff3.get() == "0" and self.cbDiff2.get() == "0" and self.cbDiff1.get() == "0":
            return False
        else:
            return True

    def compiler(self,template):  # fonction permettant de lancer la prévisualisation (thread)

        if len(self.champfeuillestyle.get("1.0", "end-1c")) == 0:
            messagebox.showerror(title="Error",
                                 message="Impossible de compiler (Veuillez insérer votre feuille de style).")
            return
        threadCompil = MyThread.myThread("ThreadPreVisualisationStyle", enonceTemp="Test d'énoncé",
                                         corrigeTemp="Test de corrigé", template=template)
        threadCompil.start()








