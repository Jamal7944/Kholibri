# Projet DUT2 Soft de génération de feuilles d'exercices

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from typing import Any
import collections

from Classes import MyThread

from Classes.Utils import Utils


class CreerFeuille(Frame):
    """
    Classe décrivant la fenêtre permettant la création d'une feuille d'exercices
    """
    listeFinale = []

    def __init__(self, parent, controller):
        """
        Constructeur de la classe

        Parameters
        ----------
        parent : la fenêtre parent
        controller : le contrôleur de la fenêtre
        """
        import SGBD
        self.listeexofinal = {}
        # Setup
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.listeChapAjoute = {}
        self.questionCours = ""

        # représente l'ensemble des exercices trouvé pour respecter les critères de chapitres et difficultés
        self.exoDict = {1: {},
                        2: {},
                        3: {},
                        4: {},
                        5: {}
                        }
        # il est organisé de la manière suivante :
        """
        exoDict = {
            difficulté : {
                idExo : {
                    'exo': "Exercice",
                    'sol': "Solution"                    
                },
                ...
            },
            ...
        }
        """

        # représente les dificultés choisie par l'utilisateur
        self.difficulteChoisie = {}
        # il est organisé de la manière suivante :
        """
        difficulteChoisie = {
            difficulté : nbExo,
            ...
        }
        """

        # représente les exercices affichés sur la ou les feuilles
        self.exoFinal = {
        }
        # il est organisé de la manière suivante :
        """
        exoFinal = {
            "nom prenom" : {         // null s'il n'y a pas de nom d'élèves
                id_exo : {
                    'exo' : "Exercice",
                    'sol' : "Solution",
                    'diff': difficulté (int)
                },
                ...
            },
            ...
        }
        """

        self.SGBD = SGBD.SGBD

        # flags des exos lors de l'édition de la feuille
        self.exoFlag = {}

        self.titre = Label(self, text="Créer une feuille d'exercice", font=controller.title_font)
        self.titre.pack(side="top", fill="x", pady=10)

        # cadre supérieur de la page, contient le choix d'auteur
        self.cadreAuteur = Frame(self)
        labelAuteur = Label(self.cadreAuteur, text="Choisissez un auteur : ",
                            font=("Helvetica", 10))
        labelAuteur.pack(side=LEFT)
        self.cbAuteur = Combobox(self.cadreAuteur, values=self.SGBD.giveAuteur(),
                                 state='readonly')  # changer la values par le select auteur
        self.cbAuteur.bind('<<ComboboxSelected>>')
        if (Utils.DefaultUser != ""):
            self.cbAuteur.set(Utils.DefaultUser)
        else:
            self.cbAuteur.set('Choisir un auteur')
        self.cbAuteur.pack(pady=5, side=LEFT)
        self.cadreAuteur.pack(side=TOP)

        ##########################################################################################################
        # Cadre première partie
        self.cadre0 = Frame(self)

        self.cadreChoixChap = Frame(self.cadre0)
        # Combobox choix de la classe
        self.cbClass = Combobox(self.cadreChoixChap, values=self.SGBD.giveClasse(), state='readonly')
        self.cbClass.bind('<<ComboboxSelected>>', lambda event: self.ActualiseChapitrePropose())
        self.cbClass.set("Choisir une classe")
        self.cbClass.pack(pady=5, side=LEFT)

        # Combobox choix du chapitre
        self.cbChap = Combobox(self.cadreChoixChap)
        self.cbChap.pack(pady=5, side=LEFT)
        self.cbChap.set("Choisir le chapitre")
        self.cbChap["state"] = "disabled"

        # Label
        Label(self.cadreChoixChap, text="Liste des choix effectués ci-dessous:", font=("Helvetica", 10)).pack(pady=5,
                                                                                                              padx=10,
                                                                                                              side=LEFT)

        # Bouton valider le choix de la classe et chap
        self.buttonValider = Button(self.cadreChoixChap, text="Choisir ce chapitre",
                                    command=lambda: self.ajouterChapitre())
        self.buttonValider.pack(pady=5, side=LEFT)

        # Bouton supprimer
        self.supprimerButton = Button(self.cadreChoixChap, text="Supprimer", command=lambda: self.supprimer())
        self.supprimerButton.pack(pady=5, side=LEFT)

        self.cadreChoixChap.pack()

        # Affichage des choix possibles
        self.champChoix = Listbox(self.cadre0, selectmode="multiple", width=150)
        self.champChoix.pack(pady=5)

        # Bouton effacer tout les choix
        self.bouttonRefaireChoixChap = Button(self.cadre0, text="Réinitialiser",
                                              command=lambda: self.refaireChoixChap())
        self.bouttonRefaireChoixChap.pack(pady=5, side=LEFT)

        # Bouton valider tout les choix et passer à l'étape suivante
        self.bouttonValiderChoixChap = Button(self.cadre0, text="Valider et passer à l'étape suivante",
                                              command=lambda: self.validerChoixChap())
        self.bouttonValiderChoixChap.pack(pady=5, side=RIGHT)

        # recherche loading
        self.Progress_Bar = Progressbar(self.cadre0, orient=HORIZONTAL, length=250, mode='determinate')

        ##########################################################################################################
        # Cadre deuxième partie = choix difficulté
        self.cadre1 = Frame(self)

        ##########################################################################################################
        # Cadre troisième partie question cours
        self.cadre2 = Frame(self)

        # Label q de cours
        Label(self.cadre2,
              text="Si vous souhaitez ajouter une question de cours, remplissez le champ ci-dessous, sinon laissez vide:",
              font=("Helvetica", 10)).pack(pady=5, padx=10, side=TOP)

        # Texte zone q de cours
        self.champQuestionCours = Text(self.cadre2, width=80, height=10)
        self.champQuestionCours.pack(pady=5, side=LEFT)

        ##########################################################################################################
        # Cadre quatrième partie = Nom d'étudiants colle
        self.cadre3 = Frame(self)

        # Listbox des noms déja entré
        self.champChoixNom = Listbox(self.cadre3, selectmode="multiple", width=150)
        self.champChoixNom.pack(pady=5, side=BOTTOM)

        # Label colle
        Label(self.cadre3,
              text="Si vous souhaitez ajouter des noms d'élèves, remplissez les champs ci-contre, sinon laissez vide:",
              font=("Helvetica", 10)).pack(pady=5, padx=10, side=LEFT)

        # Entry prénom
        self.champPrenom = Entry(self.cadre3)
        self.champPrenom.pack(pady=5, side=LEFT)

        # Entry nom
        self.champNom = Entry(self.cadre3)
        self.champNom.pack(pady=5, side=LEFT)

        # Bouton validé le nom
        Button(self.cadre3, text="Valider le prénom et le nom", command=lambda: self.ajouterNom()).pack(pady=5,
                                                                                                        side=LEFT)

        ##########################################################################################################
        # Cadre 5ème partie = Generation
        self.cadre4 = Frame(self)

        # Bouton generer la feuille
        self.buttonGenerer = Button(self.cadre4, text="Générer la feuille", command=self.gernerFeuilleBefore)
        self.buttonGenerer.pack(pady=5, padx=150, side=RIGHT)

        ##########################################################################################################
        # Cadre 6 ème partie = Modification de la feuille
        # (nouvelle page)

        self.cadre5 = Frame(self)

        self.cadreEdit = Frame(self.cadre5)

        # Cadre gauche indiquant les exercices
        self.cadreExos = LabelFrame(self.cadreEdit, text="Exercices présents dans la feuille")
        # les exercices y seront ajouter dans la fonction editFeuille
        self.cadreExos.pack(side=LEFT, padx=20, anchor='w')

        # le cadre de suppression de l'exercice
        self.cadreSuppr = LabelFrame(self.cadreEdit, text="Supprimer l'exercice")
        self.cadreSuppr.pack(side=LEFT, padx=5)
        # le cadre de remplacement de l'exercice
        self.cadreRempl = LabelFrame(self.cadreEdit, text="Remplacer l'exercice")
        self.cadreRempl.pack(side=LEFT, padx=5)
        # et le cadre de blackList
        self.cadreBlackList = LabelFrame(self.cadreEdit, text="Blacklister l'exercice")
        self.cadreBlackList.pack(side=LEFT, padx=5)

        self.cadreEdit.pack()

        # Bouton pour regénérer la feuille
        self.buttonRegenerate = Button(self.cadre5, text="Régénérer la feuille", command=self.regenerate)
        self.buttonRegenerate.pack(pady=10)

        self.cadre0.pack(pady=5)

        self.nomprenomactuel = ()

    def ActualiseChapitrePropose(self):
        """
        Permet de mettre à jour la liste des chapitres proposés
        """

        if not self.cbClass.get() or self.cbClass.get() == "Choisir une classe":
            return

        # Proposé uniquement des chapitres non ajoutés
        chapToAdd = []
        for i in self.SGBD.giveChap(self.cbClass.get()):
            if not self.listeChapAjoute.get(self.cbClass.get()) or i not in self.listeChapAjoute[self.cbClass.get()]:
                chapToAdd.append(i)

        self.cbChap["values"] = chapToAdd

        if not chapToAdd:
            self.cbChap['state'] = "disabled"
        else:
            self.cbChap.current(0)
            self.cbChap['state'] = "readonly"

        self.cbChap.set("Choisir le chapitre")

    def ajouterChapitre(self):
        """
        Fonction permettant d'ajouter dans la liste des choix de chapitres et de classes un choix venant d'être effectué
        """

        if self.cbClass.get() in self.listeChapAjoute.keys() and self.cbChap.get() in self.listeChapAjoute[
            self.cbClass.get()]:
            return
        if self.cbChap.get() == "Choisir le chapitre" or self.cbClass.get() == "Choisir une classe":  # Si valeur de base
            return

        ArrayChap = self.listeChapAjoute.get(self.cbClass.get())

        if ArrayChap:
            self.listeChapAjoute[self.cbClass.get()].append(self.cbChap.get())
        else:
            self.listeChapAjoute[self.cbClass.get()] = [self.cbChap.get()]

        self.champChoix.insert('end', f"Classe : {self.cbClass.get()}, Chapitre : {self.cbChap.get()}")

        self.ActualiseChapitrePropose()


    def supprimer(self):
        """
        Fonction qui supprime les éléments selectionnés dans la liste des chapitres
        """

        for i in self.champChoix.curselection():

            StringRecup = self.champChoix.get(i)
            StringSplitted = StringRecup.split(", ")

            StringClasse = StringSplitted[0][9:len(StringSplitted[0])]
            StringChap = StringSplitted[1][11:len(StringSplitted[1])]

            ArrayChap = self.listeChapAjoute.get(StringClasse)
            if ArrayChap:
                if StringChap in ArrayChap:
                    self.listeChapAjoute[StringClasse].remove(StringChap)

        self.champChoix.delete(0, "end")

        for key, value in self.listeChapAjoute.items():
            for i in value:
                self.champChoix.insert("end", f"Classe : {key}, Chapitre : {i}")

        self.ActualiseChapitrePropose()

    def refaireChoixChap(self):
        """
        fonction permettant de refaire les choix des chapitres et des classes
        """
        self.listeChapAjoute.clear()
        self.cbClass.set("Choisir une classe")
        self.cbChap.set("Choisir le chapitre")
        self.cbChap["state"] = "disabled"
        self.champChoix.delete(0, "end")

    def validerChoixChap(self):
        """
        fonction permettant de valider le choix fait pour les chapitres et les classes
        """
        if self.champChoix.size() == 0:
            messagebox.showinfo(title="Choix des chapitres",
                                message="Merci de choisir au moins un chapitre avant de continuer.")
            return

        self.cbClass['state'] = "disabled"
        self.cbChap['state'] = "disabled"
        self.buttonValider.destroy()
        self.bouttonValiderChoixChap.destroy()
        self.bouttonRefaireChoixChap.destroy()
        self.champChoix['state'] = 'disabled'
        self.supprimerButton.destroy()

        self.countExosfromLevel()
        self.choixDiff()

    def countExosfromLevel(self):
        """
        fonction permettant de savoir combien d'exercices sont disponibles selon le type de difficulté et les critères choisies
        """
        # le fonctionnement de cette fonction est le même principe que la fonction save

        self.SGBD.CreateTableTempChap()
        self.SGBD.CreateTableTempLevels()
        for chapArray in self.listeChapAjoute.values():
            for chap in chapArray:
                self.SGBD.InsertTableTempChap(chap)

        blacklist = self.SGBD.giveBlacklist(self.cbAuteur.get())
        for i in range(5):
            self.SGBD.InsertTableTempLevels(i + 1)
            exos = self.SGBD.GiveExoFromSelect()

            for ind, exo, sol in exos:
                if str(ind) not in blacklist:
                    self.exoDict[i + 1][ind] = {
                        "exo": exo,
                        "sol": sol
                    }
            self.SGBD.ClearTableTempLevels()

        self.SGBD.DropTableTempChap()
        self.SGBD.DropTableTempLevels()

    def choixDiff(self):
        """
        fonction permettant de choisir la difficulté des exercices
        """
        self.cadre1 = Frame(self)
        Label(self.cadre1, text="Nombre d'exercices par difficulté: ", font=("Helvetica", 10)).pack(pady=5, side=TOP)
        Label(self.cadre1, text="Difficulté 1: ", font=("Helvetica", 10)).pack(pady=5, side=LEFT)

        self.cbDiff1 = Combobox(self.cadre1, values=list(range(len(self.exoDict[1]) + 1)), state='readonly')
        self.cbDiff1.bind('<<ComboboxSelected>>', lambda event: self.UpdateEtapeSuivante())
        self.cbDiff1.set(len(self.exoDict[1]))
        self.cbDiff1.pack(pady=5, side=LEFT)

        Label(self.cadre1, text="Difficulté 2: ", font=("Helvetica", 10)).pack(pady=5, side=LEFT)
        self.cbDiff2 = Combobox(self.cadre1, values=list(range(len(self.exoDict[2]) + 1)), state='readonly')
        self.cbDiff2.bind('<<ComboboxSelected>>', lambda event: self.UpdateEtapeSuivante())
        self.cbDiff2.set(len(self.exoDict[2]))
        self.cbDiff2.pack(pady=5, side=LEFT)

        Label(self.cadre1, text="Difficulté 3: ", font=("Helvetica", 10)).pack(pady=5, side=LEFT)
        self.cbDiff3 = Combobox(self.cadre1, values=list(range(len(self.exoDict[3]) + 1)), state='readonly')
        self.cbDiff3.bind('<<ComboboxSelected>>', lambda event: self.UpdateEtapeSuivante())
        self.cbDiff3.set(len(self.exoDict[3]))
        self.cbDiff3.pack(pady=5, side=LEFT)

        Label(self.cadre1, text="Difficulté 4: ", font=("Helvetica", 10)).pack(pady=5, side=LEFT)
        self.cbDiff4 = Combobox(self.cadre1, values=list(range(len(self.exoDict[4]) + 1)), state='readonly')
        self.cbDiff4.bind('<<ComboboxSelected>>', lambda event: self.UpdateEtapeSuivante())
        self.cbDiff4.set(len(self.exoDict[4]))
        self.cbDiff4.pack(pady=5, side=LEFT)

        Label(self.cadre1, text="Difficulté 5: ", font=("Helvetica", 10)).pack(pady=5, side=LEFT)
        self.cbDiff5 = Combobox(self.cadre1, values=list(range(len(self.exoDict[5]) + 1)), state='readonly')
        self.cbDiff5.bind('<<ComboboxSelected>>', lambda event: self.UpdateEtapeSuivante())
        self.cbDiff5.set(len(self.exoDict[5]))
        self.cbDiff5.pack(pady=5, side=LEFT)

        self.cadre1.pack(pady=5)

        self.bouttonValiderChoixDiff = Button(self.cadre1, text="Passer à l'étape suivante",
                                              command=lambda: self.validerChoixDiff())
        self.bouttonValiderChoixDiff.pack(pady=5, side=LEFT)

    def UpdateEtapeSuivante(self):
        """
        fonction permettant de mettre à jour l'étape suivante
        afin d'activer le boutton valider
        """
        if self.cbDiff5.get() == "0" and self.cbDiff4.get() == "0" and self.cbDiff3.get() == "0" and self.cbDiff2.get() == "0" and self.cbDiff1.get() == "0":
            self.bouttonValiderChoixDiff["state"] = "disabled"
        else:
            self.bouttonValiderChoixDiff["state"] = "normal"


    def validerChoixDiff(self):
        """
        fonction permettant de valider le choix de difficulté du deuxième type
        """
        if self.cbAuteur.get() == "Choisir un auteur":
            messagebox.showinfo(title="Génération de feuilles",
                                message="Veuillez renseigner l'auteur")
            return
        self.cadre0.destroy()

        self.cadre2.pack(pady=5)
        self.cadre3.pack(pady=5)
        self.cadre4.pack(pady=5)

        self.cbDiff1['state'] = "disabled"
        self.cbDiff2['state'] = "disabled"
        self.cbDiff3['state'] = "disabled"
        self.cbDiff4['state'] = "disabled"
        self.cbDiff5['state'] = "disabled"

        self.difficulteChoisie={
            1: int(self.cbDiff1.get()),
            2: int(self.cbDiff2.get()),
            3: int(self.cbDiff3.get()),
            4: int(self.cbDiff4.get()),
            5: int(self.cbDiff5.get())
        }

        self.bouttonValiderChoixDiff.destroy()

    def ajouterNom(self):
        """
        fonction permettant d'ajouter un nom et prénom dans la liste concernée pour l'ajouter ensuite sur la feuille
        """
        if self.champNom.get() == "" or self.champPrenom.get() == "":
            messagebox.showinfo(title="Génération de feuilles",
                                message="Veuillez renseigner le nom et le prénom")
            return

        if self.difficulteChoisie.get(1)*(len(self.exoFinal.keys())+1) > len(self.exoDict.get(1)) or\
            self.difficulteChoisie.get(2)*(len(self.exoFinal.keys())+1) > len(self.exoDict.get(2)) or\
            self.difficulteChoisie.get(3)*(len(self.exoFinal.keys())+1) > len(self.exoDict.get(3)) or\
            self.difficulteChoisie.get(4)*(len(self.exoFinal.keys())+1) > len(self.exoDict.get(4)) or\
            self.difficulteChoisie.get(5)*(len(self.exoFinal.keys())+1) > len(self.exoDict.get(5)):
            messagebox.showinfo(title="Génération de feuilles",
                                message="Vous avez choisi trop d'exercices")
            return

        self.exoFinal[(self.champPrenom.get(), self.champNom.get())] = {}

        self.champChoixNom.insert('end', "Prénom : " + self.champPrenom.get() + "  Nom : " + self.champNom.get())

        self.champPrenom.delete(0, END)
        self.champNom.delete(0, END)

    def gernerFeuilleBefore(self):
        """
        Première étape de la génération de feuilles
        permet de gérer la presence de plusieurs élèves
        elle appelle la fonction gernerFeuille autant de fois que l'on a choisi d'élèves
        elle appelle aussi la fonction editFeuille afin de pouvoir éditer les feuilles générées
        """
        self.questionCours = self.champQuestionCours.get("1.0","end-1c")
        if len(self.exoFinal.keys()) == 0:
            self.exoFinal[None] = {}
            self.gernerFeuille(0)
        else :
            for i, j in enumerate(self.exoFinal.keys()):
                self.gernerFeuille(i)
        self.editFeuille()

    def gernerFeuille(self, numfeuille):
        """
        fonction permettant de lancer la selection aléatoire d'exercices selon les critères de l'utilisateur
        Parameters
        ----------
        numfeuille : le numéro de la feuille à générer (permet d'identifier le nom et prénom de l'élève)
        """
        nom_prenom = list(self.exoFinal.keys())[numfeuille]

        for diff, quantity in self.difficulteChoisie.items():
            if quantity == 0:
                continue
            else:
                fixed_exo = list(self.exoDict.get(diff).keys())

                for exoId in fixed_exo[:quantity]:
                    self.exoFinal[nom_prenom][exoId] = self.exoDict.get(diff).get(exoId).copy()
                    self.exoFinal[nom_prenom][exoId]["diff"] = diff
                    self.exoDict.get(diff).pop(exoId)
        # ajout de la liste finale dans une variable globale pour y accéder depuis MyThread.py
        CreerFeuille.listeFinale = self.exoFinal

        threadCompil = MyThread.myThread("ThreadPrevisualisationFeuille",
                                            questionCours=self.questionCours,
                                            etudiant=nom_prenom, auteur=self.cbAuteur.get())  # création du thread de type PrévisualisationFeuille
        threadCompil.start()

        self.cadre1.destroy()
        self.cadre2.destroy()
        self.cadre3.destroy()
        self.cadre4.destroy()

    def editFeuille(self):
        """
        fonction permettant de lancer l'édition des feuilles générées
        elle affiche pour chque exercice les boutons supprimer, remplacer et blacklist
        une séparation est présente entre chaque élève
        """
        self.cadre5.pack()
        for nom_prenom in self.exoFinal.keys():
            for ind, exo in enumerate(self.exoFinal.get(nom_prenom).keys()):
                # identification de l'exercice
                Button(self.cadreExos,
                       text=f"exercice n°{ind + 1}{'' if ind + 1 > 10 else ' '} id : {exo}{' ' * (3 - len(str(exo)) - 1)}",
                       command=lambda: print(exo)
                       ).pack(pady=5)

                supprVar = IntVar()
                supprButton = Checkbutton(self.cadreSuppr, variable=supprVar, onvalue=1, offvalue=0)
                supprButton.pack(pady=10)
                remplButton = Checkbutton(self.cadreRempl, variable=supprVar, onvalue=2, offvalue=0)
                remplButton.pack(pady=10)

                blackVar = IntVar()
                blackButton = Checkbutton(self.cadreBlackList, variable=blackVar,
                                          command=lambda idExo=exo: self.blacklist(idExo))
                blackButton.pack(pady=10)

                self.exoFlag[exo] = {
                                     "suppr": {'var': supprVar, 'button': supprButton},
                                     'rempl': {'var': supprVar, 'button': remplButton},
                                     "black": {'var': blackVar, 'button': blackButton}
                                     }
            if list(self.exoFinal.keys()).index(nom_prenom) < len(self.exoFinal.keys()) - 1:
                Separator(self.cadreExos, orient='horizontal').pack(fill='x')
                Separator(self.cadreSuppr, orient='horizontal').pack(fill='x')
                Separator(self.cadreRempl, orient='horizontal').pack(fill='x')
                Separator(self.cadreBlackList, orient='horizontal').pack(fill='x')


    def regenerate(self):
        """
        fonction appelé lors du click sur le bouton régénérer
        permet de d'appliquer les changements effectués sur les exercices et de relancer la génération
        """
        for nom_prenom in self.exoFinal.keys() :
            for exoID in self.exoFinal.get(nom_prenom).keys():
                if self.exoFlag[exoID]['suppr']['var'].get() == 1:
                    self.exoFinal.get(nom_prenom).pop(exoID)
                elif self.exoFlag[exoID]['rempl']['var'].get() == 2:
                    diff = self.exoFinal.get(nom_prenom).get(exoID).get("diff")
                    print(self.exoDict)
                    if len(self.exoDict.get(diff)) == 0:
                        messagebox.showerror(title="Régénération de feuille",
                                             message=f"Il n'y a plus d'exercices dans la difficulté {diff}")
                        return
                    else:
                        firstExoId = list(self.exoDict.get(diff))[0]
                        self.exoFinal[nom_prenom] = CreerFeuille.insertInDict(self.exoFinal.get(nom_prenom),
                                                  {firstExoId:self.exoDict.get(diff).get(firstExoId)},
                                                  list(self.exoFinal.get(nom_prenom)).index(exoID))
                        self.exoFinal.get(nom_prenom).get(firstExoId)["diff"]=diff
                        self.exoDict.get(diff).pop(firstExoId)
                        self.exoFinal.get(nom_prenom).pop(exoID)
                if self.exoFlag[exoID]['black']['var'].get() == 1:
                    self.SGBD.AddBlackList(self.cbAuteur.get(), exoID)

            CreerFeuille.listeFinale = self.exoFinal

            threadCompil = MyThread.myThread("ThreadPrevisualisationFeuille",
                                             questionCours=self.questionCours,
                                             etudiant=nom_prenom,
                                             auteur=self.cbAuteur.get())  # création du thread de type PrévisualisationFeuille
            threadCompil.start()

        for i in self.cadreExos.winfo_children() + self.cadreSuppr.winfo_children() + self.cadreRempl.winfo_children() + self.cadreBlackList.winfo_children():
            i.destroy()

        self.editFeuille()

    def blacklist(self, idExo):
        """
        fonction appelé lors du click sur le checkBox blacklist
        permet de gérer le comportement des checkBox

        Parameters
        ----------
        idExo : l'id de l'exercice concerné
        """
        if self.exoFlag[idExo]['black']['var'].get() == 1:
            if self.exoFlag[idExo]['suppr']['var'].get() == 0:
                self.exoFlag[idExo]['rempl']['var'].set(2)
            self.exoFlag[idExo]['rempl']['button'].configure(offvalue=1)
            self.exoFlag[idExo]['suppr']['button'].configure(offvalue=2)
        else:
            self.exoFlag[idExo]['rempl']['var'].set(0)
            self.exoFlag[idExo]['rempl']['button'].configure(offvalue=0)
            self.exoFlag[idExo]['suppr']['button'].configure(offvalue=0)

    @staticmethod
    def insertInDict(_dict, obj, pos):
        """
        fonction permettant d'insérer un objet dans un dictionnaire à une position donnée
        (fonction récupéré sur stackoverflow)

        Parameters
        ----------
        _dict : le dictionnaire dans lequel on veut insérer l'objet
        obj : l'objet à insérer
        pos : la position où on veut insérer l'objet
        """
        return {k: v for k, v in (list(_dict.items())[:pos] + list(obj.items()) + list(_dict.items())[pos:])}
