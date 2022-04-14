import _tkinter
import codecs
import os
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *

from Classes import MyThread
from Classes.Utils import Utils


class AjouterExercice(Frame):
    """
    Classe de la fenêtre permettant l'ajout d'un exercice dans la base de données
    """

    def __init__(self, parent, controller):
        """
        Constructeur de la classe

        Parameters
        ----------
        parent : parent de la fenêtre
        controller : contrôleur de la fenêtre
        """
        import SGBD

        Frame.__init__(self, parent)
        self.controller = controller
        self.titre = Label(self, text="Ajouter un Exercice", font=controller.title_font)
        self.titre.pack(side="top", fill="x", pady=10)

        self.emplaceAjout = {}

        self.enonce = []
        self.corrige = []
        self.SGBD = SGBD.SGBD
        self.isFirstLoop = True

        self.EXO_FINSHED = False

        s = Style()
        s.configure('My.TFrame', background='red')

        # Chaque suite de ~ correspond à la séparation de cadre s'affichant sur la page principale

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # correspond à la page d'edition d'exercice,
        # c'est la page affichée par défaut
        self.Page_EditExo = Frame(self)
        # séparée en deux cadres

        # cadre supérieur de la page, contient le choix d'auteur
        self.cadreAuteur = Frame(self.Page_EditExo)
        labelAuteur = Label(self.cadreAuteur, text="Choisissez un auteur : ",
                            font=("Helvetica", 10))
        labelAuteur.pack(side=LEFT)
        self.cbAuteur = Combobox(self.cadreAuteur, values=self.SGBD.giveAuteur(),
                                 state='readonly')  # changer values par le select auteur
        self.cbAuteur.bind('<<ComboboxSelected>>')
        if (Utils.DefaultUser != ""):
            print("coucou l'auteur défaut")
            self.cbAuteur.set(Utils.DefaultUser)
        else:
            self.cbAuteur.set('Choisir un auteur')
        self.cbAuteur.pack(pady=5, side=LEFT)
        self.cadreAuteur.pack(side=TOP)

        # Cadre inférieur contenant les deux blocs de texte 'exo' et 'solution' et les boutons de validation
        self.cadreEdition = Frame(self.Page_EditExo)
        label = Label(self.cadreEdition, text="Ecrire ci-dessous l'énoncé de l'exercice : ", font=("Helvetica", 10))
        label.pack(side=TOP, fill="x")

        self.champEnonce = Text(self.cadreEdition, width=200, height=15, bg="#E5E5E5", fg="black",
                                insertbackground="black",
                                font="Helvetica 10", undo=True)
        Utils.configureColor(self.champEnonce)
        self.champEnonce.bind("<Key>", lambda event: Utils.updateCode(self.champEnonce))

        self.BouttonAjoutExo = Button(self.cadreEdition, text="Ajouter énoncé",
                                      command=lambda: Utils.open_file(self.champEnonce))
        self.BouttonAjoutExo.pack(side=TOP)

        self.champEnonce.pack(pady=5)

        label = Label(self.cadreEdition, text="Ecrire la correction de l'exercice : ", font=("Helvetica", 10))
        label.pack(side=TOP, fill="x")

        self.champCorrection = Text(self.cadreEdition, width=200, height=15, bg="#E5E5E5", fg="black",
                                    insertbackground="black",
                                    font="Helvetica 10", undo=True)
        Utils.configureColor(self.champCorrection)

        self.champCorrection.bind("<Key>", lambda event: Utils.updateCode(self.champCorrection))

        self.BouttonAjoutSol = Button(self.cadreEdition, text="Ajouter correction",
                                      command=lambda: Utils.open_file(self.champCorrection))
        self.BouttonAjoutSol.pack(side=TOP)

        self.champCorrection.pack(pady=5)

        self.cadreEdition.pack()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Page appelée par le click du bouton suivant sur la page d'edition d'exercice

        self.Page_ParamExo = Frame(self.Page_EditExo)
        self.cadre_ComboBox = Frame(self.Page_ParamExo)

        label = Label(self.cadre_ComboBox, text="Paramètrage : ",
                      font=("Helvetica", 10))
        label.pack(side=LEFT, fill="x", pady=5)

        self.cbClass = Combobox(self.cadre_ComboBox, values=self.SGBD.giveClasse(), state='readonly')
        self.cbClass.bind('<<ComboboxSelected>>', lambda event: self.ActualisationChap())
        self.cbClass.set("Choisir une classe")
        self.cbClass.pack(pady=5, side=LEFT)

        self.cbChap = Combobox(self.cadre_ComboBox, state='readonly')
        self.cbChap.bind('<<ComboboxSelected>>', lambda event: self.ActualisationDiff())
        self.cbChap.set("Choisir le chapitre")
        self.cbChap["state"] = "disabled"
        self.cbChap.pack(pady=5, side=LEFT)

        self.cbDifficulte = Combobox(self.cadre_ComboBox, state='readonly')
        self.cbDifficulte.set("Choisir la difficulté")
        self.cbDifficulte["state"] = "disabled"
        self.cbDifficulte.pack(pady=5, side=LEFT)

        self.valider = Button(self.cadre_ComboBox, text="Valider le choix", command=self.validerChoix)
        self.valider.pack(pady=5, side=LEFT)

        self.refaireChoix = Button(self.cadre_ComboBox, text="Réinitialiser",
                                   command=lambda: self.refaireChoixChap())
        self.refaireChoix.pack(pady=5, side=LEFT)

        self.supprimerButton = Button(self.cadre_ComboBox, text="Supprimer", command=self.supprimer)
        self.supprimerButton.pack(pady=5, side=LEFT)

        self.cadre_ComboBox.pack(pady=5)

        self.cadre_ListeChoix = Frame(self.Page_ParamExo)
        label = Label(self.cadre_ListeChoix, text="Liste des choix ", font=("Helvetica", 10))
        label.pack(side=TOP, fill="x", pady=5)
        self.champChoix = Listbox(self.cadre_ListeChoix, selectmode="multiple", width=200, height=6)
        self.champChoix.pack(pady=8)

        self.cadre_ListeChoix.pack(pady=5)

        self.saveButton = Button(self.cadre_ListeChoix, text="Sauvegarder l'exercice", command=self.save)
        self.saveButton.pack(pady=5, padx=15, side=RIGHT)
        self.saveButton["state"] = "disabled"

        self.compiler = Button(self.cadre_ListeChoix, text="Compiler l'exercice", command=self.compiler)
        self.compiler.pack(pady=5, side=RIGHT)

        self.Page_ParamExo.pack()
        self.Page_EditExo.pack()

    def ActualisationChap(self):
        """
        Actualise la liste des chapitres en fonction de la classe choisie
        """

        if not self.cbClass.get() or self.cbClass.get() == "Choisir une classe":
            self.cbChap["state"] = "disabled"
            self.cbChap.set("Choisir le chapitre")

            return

        toAdd = []
        valChapChoisi = []

        for k, i in self.emplaceAjout.items():
            for e in i:
                valChapChoisi.append(e[0])

        for i in self.SGBD.giveChap(self.cbClass.get()):
            if i not in valChapChoisi:
                toAdd.append(i)

        self.cbChap['values'] = toAdd
        if toAdd == []:
            self.cbChap['state'] = "disabled"
        else:
            self.cbChap['state'] = "readonly"

        self.cbChap.set("Choisir le chapitre")

    def ActualisationDiff(self):
        """
        Actualise la liste des difficultés en fonction du/des chapitre/s choisi/s
        """

        if not self.cbChap.get() or self.cbChap.get() == "Choisir le chapitre":
            self.cbDifficulte["state"] = "disabled"
            self.cbDifficulte.set("Choisir la difficulté")
            return

        diff = 10
        for k, i in self.emplaceAjout.items():
            for e in i:
                if k == self.cbClass.get():
                    diff = [e[1]]

        if diff != 10:
            self.cbDifficulte["values"] = diff
            self.cbDifficulte["state"] = "readonly"
            self.cbDifficulte.current(0)
        else:
            self.cbDifficulte["values"] = list(range(1, 6))
            self.cbDifficulte["state"] = "readonly"

    def supprimer(self):
        """
        Supprime le chapitre sélectionné des choix de chapitre
        """
        StringRecup = []

        for i in self.champChoix.curselection():
            StringRecup.append(self.champChoix.get(i))

        for i in StringRecup:

            StringSplitted = i.split(", ")

            StringClasse = StringSplitted[0][9:]
            StringChap = StringSplitted[1][11:]
            StringDifficulte = StringSplitted[2][13:]

            ArrayChap = self.emplaceAjout.get(StringClasse)
            if ArrayChap:
                if [StringChap, StringDifficulte] in ArrayChap:
                    self.emplaceAjout[StringClasse].remove([StringChap, StringDifficulte])

        self.champChoix.delete(0, "end")

        for key, item in self.emplaceAjout.items():
            for e in item:
                self.champChoix.insert(END, "Classe : " + key + ", Chapitre : " + e[0] + ", Difficulté : " + e[1])

        self.ActualisationChap()
        self.ActualisationDiff()

    def validerChoix(self):
        """
        Ajoute le triolet classe/chapitre/difficulté parmis les choix
        """

        if self.cbClass.get() == "Choisir une classe" or self.cbChap.get() == "Choisir le chapitre" or self.cbDifficulte.get() == "Choisir la difficulté":
            messagebox.showinfo(title="Choix",
                                message="Merci de choisir la classe, le chapitre et la difficulté.")
            return

        chapExistant = self.emplaceAjout.get(self.cbClass.get())

        toAdd = [self.cbChap.get(), self.cbDifficulte.get()]

        if chapExistant:
            self.emplaceAjout[self.cbClass.get()].append(toAdd)
        else:
            self.emplaceAjout[self.cbClass.get()] = [toAdd]

        self.champChoix.delete(0, "end")
        for key, item in self.emplaceAjout.items():
            for e in item:
                self.champChoix.insert(END, "Classe : " + key + ", Chapitre : " + e[0] + ", Difficulté : " + e[1])

        self.cbChap.set("Choisir le chapitre")
        self.cbDifficulte["state"] = "disabled"
        self.cbDifficulte.set("Choisir la difficulté")
        self.ActualisationChap()

    def listeDifficulte(self):
        """
        Liste les difficultés disponibles dans la combobox
        """

        self.cbDifficulte['values'] = list(range(1, 6))
        self.cbDifficulte.bind('<<ComboboxSelected>>')
        self.cbDifficulte.current(0)

    def compiler(self):
        """
        Lance la compilation de l'exercice => enchaine sur la prévisualisation de l'exercice
        """
        self.auteur = self.cbAuteur.get()
        self.enonce, self.corrige = self.SGBD.ModifyShortcutToCommand(self.champEnonce.get("1.0", "end-1c"),
                                                                      self.auteur,
                                                                      self.champCorrection.get("1.0", "end-1c"))

        if not self.enonce or not self.corrige:
            messagebox.showinfo(title="Ajout d'exercice",
                                message="Merci d'écrire un exercice et un corrigé.")
            return

        if not self.auteur or self.auteur == "Choisir un auteur":
            messagebox.showinfo(title="Ajout d'exercice",
                                message="Merci de choisir un auteur.")
            return

        self.saveButton["state"] = "normal"

        threadCompil = MyThread.myThread("ThreadPrevisualisationExo", enonceTemp=self.champEnonce.get("1.0", "end-1c"),
                                         corrigeTemp=self.champCorrection.get("1.0", "end-1c"), auteur=self.auteur)
        threadCompil.start()

    def save(self):
        """
        Sauvegarde l'exercice dans la base de données
        """

        if (os.path.exists("temp/exoTemp.pdf")):
            os.remove("temp/exoTemp.pdf")

        self.auteur = self.cbAuteur.get()
        self.enonce = self.champEnonce.get("1.0", "end-1c")
        self.corrige = self.champCorrection.get("1.0", "end-1c")

        if not self.enonce or not self.corrige:
            messagebox.showinfo(title="Ajout d'exercice",
                                message="Merci d'écrire un exercice et un corrigé.")
            return

        if not self.auteur or self.auteur == "Choisir un auteur":
            messagebox.showinfo(title="Ajout d'exercice",
                                message="Merci de choisir un auteur.")
            return

        if self.champChoix.size() == 0:
            messagebox.showinfo(title="Choix",
                                message="Merci de choisir un ou plusieurs chapitres.")
            return

        self.saveButton["state"] = "disabled"

        self.enonce, self.corrige = self.SGBD.ModifyShortcutToCommand(self.champEnonce.get("1.0", "end-1c"),
                                                                      self.auteur,
                                                                      self.champCorrection.get("1.0", "end-1c"))

        self.SGBD.InsertExo(self.enonce, self.corrige, self.auteur)
        for key, item in self.emplaceAjout.items():
            for e in item:
                self.SGBD.InsertExoUtilChap(e[0], key, 0)

            self.SGBD.InsertExoPossNiveau(key, item[0][1])

    def finalMessage(self):
        """
        Affiche le message de fin de l'ajout d'exercice
        """

        if self.isFirstLoop:
            accord = ""
        else:
            accord = "s"

        MsgBox = messagebox.askquestion(f"Exercice{accord} ajouté{accord} avec succès",
                                        "Voulez vous ajouter d'autres exercices ?", icon='info')

        if MsgBox == 'yes':
            self.destroy()
            self.controller.chargerFrames()
            self.controller.show_frame("AjouterExercice")
        else:
            self.destroy()
            self.controller.chargerFrames()

    def suivant(self):
        """
        Permet de passer de la première partie des choix à la deuxième partie
        """

        self.Page_EditExo.pack_forget()

        self.Page_ParamExo.pack()

    def refaireChoixChap(self):
        """
        Permet de refaire les choix des chapitres et des classes
        """

        self.emplaceAjout = {}
        self.champChoix.delete(0, "end")

        self.cbClass.set("Choisir une classe")
        self.ActualisationChap()



    @staticmethod
    def launchWithData(parent, controler, exo, sol, numEx):
        """

        Lance l'ajout d'un exercice
        cette fonction est utiliser par la classe AjouterNExercices afin d'éviter de dupliquer le code


        Parameters
        ----------
        parent : le parent de la fenêtre
        controler : le controler de la fenêtre
        exo : l'exercice a ajouter
        sol : la solution de l'exercice
        numEx : le numéro de l'exercice a ajouter (ne correspond pas a son identifiant dans la base de donnée
        """

        for child in parent.winfo_children():
            child.pack_forget()
        page = AjouterExercice(parent, controler)

        page.titre.configure(text=f"Ajouter plusieurs Exercices\nNombre d'exercice restants : {numEx + 1}")

        page.BouttonAjoutExo.pack_forget()
        page.BouttonAjoutSol.pack_forget()

        page.champEnonce.insert(END, exo)
        page.champCorrection.insert(END, sol)

        page.saveButton.configure(command=page.end_exo)
        page.grid(row=0, column=0, sticky=N + S + E + W)

    def end_exo(self):
        """
        Permet de terminer l'ajout d'un exercice lorsque l'on ajoute plusieurs exercices
        (nécessiter de détruire la page en plus de sauvegarder l'exercice)
        """
        self.save()
        self.destroy()
