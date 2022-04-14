from tkinter import *
from tkinter import messagebox

from tkinter.ttk import *

from Classes import MyThread
from Classes.Utils import Utils


class AfficherExo(Frame):
    """
    Classe de la fenêtre permettant l'affichage d'un exercice selon son ID
    """

    def __init__(self, parent, controller):
        """
        Constructeur de la fenêtre

        Parameters
        ----------
        parent: le parent de la fenêtre
        controller: le contrôleur de la fenêtre
        """
        import SGBD
        Frame.__init__(self, parent)

        ###############################################################################################
        # Init

        s = Style()
        s.configure('My.TFrame', background='red')

        self.controller = controller
        self.enonce = []
        self.corrige = []

        self.SGBD = SGBD.SGBD

        ###############################################################################################
        # Self

        # Titre
        label = Label(self, text="Afficher un Exercice", font=controller.title_font)  # Titre
        label.pack(side="top", fill="x", pady=10)

        ###############################################################################################
        # Top cadre

        self.cadre0 = Frame(self)

        self.cadre01 = Frame(self.cadre0)
        self.cadre01.pack(side=LEFT, pady=5, padx=50)

        label = Label(self.cadre01, text="Indiquez un ID d'exercice :", font=("Helvetica", 10))
        label.pack(pady=5, side=LEFT)

        self.choixExo = Text(self.cadre01, width=50, height=1)
        self.choixExo.pack(pady=5, side=LEFT)

        self.b1 = Button(self.cadre01, text="Rechercher",
                         command=lambda: self.rechercherExo(self.choixExo.get(1.0, "end")))
        self.b1.pack(pady=5, side=LEFT)

        self.cbAuteur = Combobox(self.cadre0, values=self.SGBD.giveAuteur(), state='readonly')
        if (Utils.DefaultUser != ""):
            self.cbAuteur.set(Utils.DefaultUser)
        else:
            self.cbAuteur.set('Choisir un auteur')
        self.cbAuteur.pack(pady=5, side=RIGHT)

        self.cadre0.pack(pady=5)

        ###############################################################################################
        # Cadre exercice

        self.cadre1 = Frame(self)

        self.champEnonce = Text(self.cadre1, width=200, height=15, bg="#E5E5E5", fg="black", insertbackground="black",
                                font="Helvetica 10", undo=True)
        Utils.configureColor(self.champEnonce)
        self.champEnonce.pack(pady=5)
        self.champEnonce.bind("<Key>", lambda event: self.updatecode(self.champEnonce))

        self.champCorrection = Text(self.cadre1, width=200, height=15, bg="#E5E5E5", fg="black",
                                    insertbackground="black", font="Helvetica 10", undo=True)
        Utils.configureColor(self.champCorrection)
        self.champCorrection.pack(pady=5)
        self.champCorrection.bind("<Key>", lambda event: self.updatecode(self.champCorrection))

        self.cadre10 = Frame(self.cadre1)

        self.compilationButton = Button(self.cadre10, text="Compiler", command=lambda: self.compiler())
        self.compilationButton.pack(pady=5, padx=10, side=LEFT)

        self.validButton = Button(self.cadre10, text="Enregistrer les modifcations",
                                  command=lambda: self.validate(self.ExoRegarde))
        self.validButton["state"] = "disabled"
        self.validButton.pack(pady=5, side=LEFT)

        self.cadre10.pack()

        self.cadre1.pack(pady=5)

        ###############################################################################################
        # Cadre modification niveau

        self.cadre2 = Frame(self)

        labelChapPres = Label(self.cadre2, text="Chapitres où l'exercice est présent :", font=("Helvetica", 10))
        labelChapPres.pack(pady=5, padx=5, side=LEFT)

        self.cbClasseCP = Combobox(self.cadre2, state='readonly')
        self.cbClasseCP.set('Choisir une classe')
        self.cbClasseCP["state"] = "disabled"
        self.cbClasseCP.bind('<<ComboboxSelected>>', lambda event: self.UpdateChapitrePresent())
        self.cbClasseCP.pack(pady=5, padx=5, side=LEFT)

        self.cbChapCP = Combobox(self.cadre2, state='readonly')
        self.cbChapCP.set('Choisir un chapitre')
        self.cbChapCP["state"] = "disabled"
        self.cbChapCP.pack(pady=5, padx=5, side=LEFT)

        self.cbNivCP = Combobox(self.cadre2, state='readonly')
        self.cbNivCP.set('Choisir un niveau')
        self.cbNivCP["state"] = "disabled"
        self.cbNivCP.pack(pady=5, padx=5, side=LEFT)

        self.b1CP = Button(self.cadre2, text="Enregistrer la modification de niveau", command=lambda: self.ModifNiv())
        self.b1CP.pack(pady=5, padx=5, side=LEFT)

        self.b2CP = Button(self.cadre2, text="Supprimer l'exercice du chapitre", command=lambda: self.SupprExo())
        self.b2CP.pack(pady=5, padx=5, side=LEFT)

        self.cadre2.pack(pady=(80, 10))

        ###############################################################################################
        # Cadre retirer chap

        self.cadre3 = Frame(self)

        labelChapNonPres = Label(self.cadre3, text="Chapitres où l'exercice n'est pas présent :",
                                 font=("Helvetica", 10))
        labelChapNonPres.pack(pady=5, padx=5, side=LEFT)

        self.cbClasseCNP = Combobox(self.cadre3, state='readonly')
        self.cbClasseCNP.set('Choisir une classe')
        self.cbClasseCNP["state"] = "disabled"
        self.cbClasseCNP.bind('<<ComboboxSelected>>', lambda event: self.UpdateChapitreNonPresent())
        self.cbClasseCNP.pack(pady=5, padx=5, side=LEFT)

        self.cbChapCNP = Combobox(self.cadre3, state='readonly')
        self.cbChapCNP.set('Choisir un chapitre')
        self.cbChapCNP["state"] = "disabled"
        self.cbChapCNP.pack(pady=5, padx=5, side=LEFT)

        self.cbNivCNP = Combobox(self.cadre3, state='readonly')
        self.cbNivCNP.set('Choisir un niveau')
        self.cbNivCNP["state"] = "disabled"
        self.cbNivCNP.pack(pady=5, padx=5, side=LEFT)

        self.b1CNP = Button(self.cadre3, text="Enregistrer l'exercice dans le chapitre",
                            command=lambda: self.AjoutExo())
        self.b1CNP.pack(pady=5, padx=(5, 275), side=LEFT)

        self.cadre3.pack(pady=10)

    # fonction permettant d'afficher un exercice dans les champs de textes selon son ID
    def rechercherExo(self, idExo):
        """
        Fonction permettant d'afficher un exercice dans les champs de textes selon son ID

        Parameters
        ----------
        idExo: l'id de l'exercice à afficher
        """

        if not idExo.replace(chr(10), '').isnumeric():
            messagebox.showinfo(title="ID", message="Merci d'écrire un id valable.")
            return

        self.ExoRegarde = idExo.replace(chr(10), '')

        if self.cbAuteur.get() == "Choisir un auteur":
            messagebox.showinfo(title="Auteur", message="Merci de préciser un auteur.")
            return

        if not self.SGBD.giveEnonce(self.ExoRegarde):
            messagebox.showinfo(title="Exercice", message="Il n'existe pas d'exercice relié à cette ID.")
            return

        # Modif level
        chapP = self.SGBD.GiveExoFromChap(self.ExoRegarde)
        self.cbClasseCP["values"] = list(chapP.keys())
        if list(chapP.keys()) == []:
            self.cbClasseCP["state"] = "disabled"
        else:
            self.cbClasseCP["state"] = "readonly"
        self.cbClasseCP.set('Choisir une classe')

        self.cbChapCP.set('Choisir un chapitre')
        self.cbChapCP["state"] = "disabled"

        self.cbNivCP.set('Choisir un niveau')
        self.cbNivCP["state"] = "disabled"
        ###

        # Exo pas present
        chapNP = self.SGBD.SelectNotInChaps(self.ExoRegarde)
        self.cbClasseCNP["values"] = list(chapNP.keys())
        if list(chapNP.keys()) == []:
            self.cbClasseCNP["state"] = "disabled"
        else:
            self.cbClasseCNP["state"] = "readonly"
        self.cbClasseCNP.set('Choisir une classe')

        self.cbChapCNP.set('Choisir un chapitre')
        self.cbChapCNP["state"] = "disabled"

        self.cbNivCNP.set('Choisir un niveau')
        self.cbNivCNP["state"] = "disabled"
        ###

        self.enonce, self.corrige = self.SGBD.ModifyCommandToShortcut(
            self.SGBD.giveEnonce(self.ExoRegarde)[0],
            self.cbAuteur.get(),
            self.SGBD.giveCorrige(self.ExoRegarde)[0]
        )

        self.champEnonce.delete(1.0, "end")
        self.champEnonce.insert('end', self.enonce)
        self.updatecode(self.champEnonce)

        self.champCorrection.delete(1.0, "end")
        self.champCorrection.insert('end', self.corrige)
        self.updatecode(self.champCorrection)

    def UpdateChapitrePresent(self):
        """
        Fonction permettant de mettre à jour sur la fenêtre les chapitres présents dans la base de données
        """
        chapP = self.SGBD.GiveExoFromChap(self.ExoRegarde)

        if not self.cbClasseCP.get() or self.cbClasseCP.get() == "Choisir une classe":

            self.cbChapCP.set('Choisir un chapitre')
            self.cbChapCP["state"] = "disabled"

            self.cbNivCP.set('Choisir un niveau')
            self.cbNivCP["state"] = "disabled"

            if list(chapP.keys()) == []:
                self.cbClasseCP["state"] = "disabled"
            else:
                self.cbClasseCP["state"] = "readonly"
            self.cbClasseCP["values"] = list(chapP.keys())

            return

        self.cbChapCP["state"] = "readonly"
        self.cbChapCP['values'] = chapP[self.cbClasseCP.get()][0]

        self.cbNivCP["state"] = "readonly"
        self.cbNivCP['values'] = list(range(1, 6))
        self.cbNivCP.set(chapP[self.cbClasseCP.get()][1])

    def UpdateChapitreNonPresent(self):
        """
        Fonction permettant de mettre à jour les chapitres non présents dans la base de données
        """

        chapP = self.SGBD.GiveExoFromChap(self.ExoRegarde)
        chapNP = self.SGBD.SelectNotInChaps(self.ExoRegarde)

        if not self.cbClasseCNP.get() or self.cbClasseCNP.get() == "Choisir une classe":

            self.cbChapCNP.set('Choisir un chapitre')
            self.cbChapCNP["state"] = "disabled"

            self.cbNivCNP.set('Choisir un niveau')
            self.cbNivCNP["state"] = "disabled"

            if list(chapNP.keys()) == []:
                self.cbClasseCNP["state"] = "disabled"
            else:
                self.cbClasseCNP["state"] = "readonly"
            self.cbClasseCNP["values"] = list(chapNP.keys())

            return

        self.cbChapCNP["state"] = "readonly"
        self.cbChapCNP['values'] = chapNP[self.cbClasseCNP.get()]

        self.cbNivCNP["state"] = "readonly"

        if chapP.get(self.cbClasseCNP.get()):
            self.cbNivCNP['values'] = chapP[self.cbClasseCNP.get()][1]
        else:
            self.cbNivCNP['values'] = list(range(1, 6))

    def AjoutExo(self):
        """
        Fonction permettant d'ajouter un exercice dans la base de données
        """
        if self.cbClasseCNP.get() == "Choisir une classe" or self.cbChapCNP.get() == "Choisir un chapitre" or self.cbNivCNP.get() == "Choisir un niveau":
            messagebox.showinfo(title="Ajout d'exerice",
                                message="Merci de choisir la classe, le chapitre et le niveau.")
            return

        self.SGBD.InsertExoUtilChap(self.cbChapCNP.get(), self.cbClasseCNP.get(), self.ExoRegarde)
        self.SGBD.ModifyNiveau(self.ExoRegarde, self.cbClasseCNP.get(), self.cbNivCNP.get())

        self.cbClasseCP.set("Choisir une classe")
        self.UpdateChapitrePresent()
        self.cbClasseCNP.set("Choisir une classe")
        self.UpdateChapitreNonPresent()
        messagebox.showinfo(title="Ajout d'exerice", message="L'exercice a bien été ajouté.")

    def ModifNiv(self):
        """
        Fonction permettant de modifier le niveau d'un exercice
        """
        if self.cbClasseCP.get() == "Choisir une classe":
            messagebox.showinfo(title="Changement de niveau", message="Merci de choisir la classe et le niveau.")
            return

        self.SGBD.ModifyNiveau(self.ExoRegarde, self.cbClasseCP.get(), self.cbNivCP.get())

        self.cbClasseCP.set("Choisir une classe")
        self.UpdateChapitrePresent()
        self.cbClasseCNP.set("Choisir une classe")
        self.UpdateChapitreNonPresent()

        messagebox.showinfo(title="Modification de niveau", message="Le niveau de l'exercice a bien été modifié.")

    def SupprExo(self):
        """
        Fonction permettant de supprimer un exercice de la base de données
        """

        if self.cbClasseCP.get() == "Choisir une classe" or self.cbChapCP.get() == "Choisir un chapitre":
            messagebox.showinfo(title="Suppression d'exercice", message="Merci de choisir une classe et un chapitre.")
            return

        self.SGBD.RetirerExoChap(self.ExoRegarde, self.cbChapCP.get())

        self.cbClasseCP.set("Choisir une classe")
        self.UpdateChapitrePresent()
        self.cbClasseCNP.set("Choisir une classe")
        self.UpdateChapitreNonPresent()

        messagebox.showinfo(title="Ajout d'exerice", message="L'exercice a bien été supprimé.")

    def compiler(self):
        """
        Fonction permettant de compiler le code latex et d'enregistrer le fichier pdf
        """
        threadCompil = MyThread.myThread("ThreadPrevisualisationExo", enonceTemp=self.champEnonce.get("1.0", "end-1c"),
                                         corrigeTemp=self.champCorrection.get("1.0", "end-1c"),
                                         auteur=self.cbAuteur.get())
        threadCompil.start()

        self.validButton["state"] = "normal"

    def validate(self, idExo):
        """
        Fonction permettant de valider un exercice

        Parameters
        ----------
        idExo: l'id de l'exercice
        """

        if not idExo:
            return

        self.validButton["state"] = "disabled"

        if self.cbAuteur.get() == "Choisir un auteur":
            messagebox.showinfo(title="Classe", message="Merci de préciser un auteur.")
            return

        self.enonce = self.champEnonce.get("1.0", "end-1c")
        self.corrige = self.champCorrection.get("1.0", "end-1c")

        self.SGBD.ModifyExo(idExo, self.enonce, self.corrige)

    def updatecode(self, champ):
        """
        Fonction permettant de mettre à jour le code latex et d'appliquer la colloration syntaxique

        Parameters
        ----------
        champ : le champ de texte dans lequel effectuer la colloration syntaxique
        """

        Utils.tagHighlight(champ)
        Utils.scan(champ)
