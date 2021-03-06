import codecs, glob, shutil, threading, subprocess, os
from tkinter import messagebox
from SGBD.SGBD import *

from Classes import CreerFeuille
from Classes.ApplicationViews import *

exitFlag = 0

class myThread(threading.Thread):
    """
    Cette classe permet la création des différents Threads\n
    Il y a 5 threads différents :
            \n- ThreadAppli                   : Le lancement de l'application
            \n- ThreadPreVisualisation        : La génération et visualisation d'un exercice
            \n- ThreadPrevisualisationFeuille : La génération et visualisation d'une feuille de colle
            \n- ThreadLogCompilation          : Le lancement de la fenetre d'affichage de la compilation d'un exercice
            \n- WriteInLog                    : L'affichage de la compilation d'un exercice
    Afin de permettre cette dernière fonctionnalité,
    des méthodes ont été rajoutés afin de mimer le fonctionnement d'un objet File de python
    """

    def __init__(self, name, logWindow=None, pipeReader=None, enonceTemp=None, corrigeTemp=None, questionCours=None,template=None,auteur=None, etudiant=None):
        """
        Constructeur de la classe
        
        Parameters
        ----------
        name : Chaque threads ont un nom, celui-ci
                     permet l'identification du thread et ainsi, parmatrer le fonctionnement du thread
        logWindow : Paramètre nécessaire uniquement pour le Thread WriteInLog,
                          il permet d'identifié la fenetre crée par le thread LogCompilation et de, ainsi, la modifier
        pipeReader : Paramètre nécessaire uniquement pour le Thread WriteInLog,
                           il permet d'identifié la sortie de la commande de compilation et d'en récupéré le contenu
        enonceTemp
        corrigeTemp
        questionCours
        template
        auteur
        etudiant
        """
        # dans tous les cas, on initialise le thread et le nom du thread
        threading.Thread.__init__(self)
        self.name = name
        # si le thread est celui de création de la fenetre de log,
        # on a besoin d'attribut pour mimer le fonctionnement d'un fichier
        if self.name == "ThreadLogCompilation":
            self.fdRead, self.fdWrite = os.pipe()
            self.pipeReader = os.fdopen(self.fdRead)
            self.daemon = False
        # si le thread est celui d'écriture de log, on récupère la fenetre et le reader
        if self.name == "WriteInLog":
            self.logWindow = logWindow
            self.pipeReader = pipeReader
        self.enonceTemp = enonceTemp
        self.corrigeTemp = corrigeTemp
        self.questionCours = questionCours
        self.template = template
        self.auteur = auteur
        self.etudiant = etudiant

    def run(self):
        """
        méthode qui est appelée pour lancer un thread
        elle s'occupe de renvoyer vers la bonne méthode selon le nom du thread
        """

        if self.name == "ThreadAppli":
            self.application = ApplicationViews()
            self.creation_temp()
            self.application.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.application.mainloop()
        if self.name == "ThreadPreVisualisationStyle":
            self.PrevisualisationStyle()
        if self.name == "ThreadPrevisualisationFeuille":
            self.PrevisualtisationFeuille()
        if self.name == "ThreadLogCompilation":
            self.LogCompilation()
        if self.name == "WriteInLog":
            self.WriteInLog()
        if self.name == "ThreadPrevisualisationExo":
            self.PrevisualisationExo()

    def PrevisualisationStyle(self):
        """
        Fonction appelé lorsque le thread est ThreadPreVisualisation
        Il permet la compilation et l'affichage d'un exercice
        Ce Thread crée et appel le thread ThreadLogCompilation pour donner des informations à l'utilisateur
        IMPORTANT : toute écriture dans un fichier tex pour qu'il soit compilé devra être en encodé UTF-8
        """
         # pour visualiser la feuille de style d'un nouvel utilisateur

        file = open("temp/test.tex", "wb")
        style = self.template.splitlines()
        for line in style :
            if "\\end{document}" not in line:
                file.write(line.encode('utf-8'))
                file.write("\n".encode('utf-8'))

        file.write(("\n" + r"\begin{exo}" + "\n").encode('utf-8'))
        file.write(self.enonceTemp.encode('utf-8'))

        file.write(("\n" + r"\end{exo}" + "\n").encode('utf-8'))

        file.write(("\n" + "\n" + r"\begin{sol}" + "\n").encode('utf-8'))
        file.write(self.corrigeTemp.encode('utf-8'))
        file.write(("\n" + r"\end{sol}" + "\n").encode('utf-8'))
        file.write(("\end{document}").encode('utf-8'))

        file.close()
        # on crée le thread de log et on le démarre
        log = myThread("ThreadLogCompilation")
        log.start()
        # ce thread peut être interprété comme fichier de sortie de commande
        # on peut donc spécifier a subprocess.Popen,
        # qui s'occupe de compiler le fichier latex via la commande de shell pdflatex,
        # que le fichier de sortie est le thread ThreadLogCompilation
        process = subprocess.Popen(
            ['pdflatex', 'temp/test.tex'], stdout=log,stderr=log)
        # on attend la fin de la compilation
        # (par défaut subprocess.Popen renvoi dès le lancement de la commande)
        process.wait()

        # on ferme le "fichier"
        os.close(log.fdWrite)
        # et on attend la fin du thread
        log.join()

        shutil.move('test.pdf', 'temp/test.pdf')
        list_of_files = glob.glob(r'temp/*.pdf')
        latest_file = max(list_of_files, key=os.path.getctime)

        os.remove("test.aux")
        os.remove("test.log")
        os.remove("test.out")
        # os.remove("test.toc")

        self.open_file(latest_file)


    def PrevisualisationExo(self):
        """
        Fonction appelé lorsque le thread est ThreadPreVisualisation
        Il permet la compilation et l'affichage d'un exercice
        Ce Thread crée et appel le thread ThreadLogCompilation pour donner des informations à l'utilisateur
        IMPORTANT : toute écriture dans un fichier tex pour qu'il soit compilé devra être en encodé UTF-8
        """
         # pour visualiser la feuille de style d'un nouvel utilisateur

        file = open("SGBD/utilisateurs/"+self.auteur+"/temp/testexo.tex", "wb")
        with codecs.open("SGBD/utilisateurs/"+self.auteur+"/style.tex", encoding="utf-8", errors='replace') as filestyle:
            contenu = filestyle.readlines()
            for line in contenu :
                if "\\end{document}" not in line :
                    file.write(line.encode('utf-8'))
                else :
                    file.write(("\n" + r"\begin{exo}" + "\n").encode('utf-8'))
                    file.write(self.enonceTemp.encode('utf-8'))
                    file.write(("\n" + r"\end{exo}" + "\n").encode('utf-8'))
                    file.write(("\n" + "\n" + r"\begin{sol}" + "\n").encode('utf-8'))
                    file.write(self.corrigeTemp.encode('utf-8'))
                    file.write(("\n" + r"\end{sol}" + "\n").encode('utf-8'))
                    file.write(line.encode('utf-8'))

        file.close()
        # on crée le thread de log et on le démarre
        log = myThread("ThreadLogCompilation")
        log.start()
        # ce thread peut être interprété comme fichier de sortie de commande
        # on peut donc spécifier a subprocess.Popen,
        # qui s'occupe de compiler le fichier latex via la commande de shell pdflatex,
        # que le fichier de sortie est le thread ThreadLogCompilation
        process = subprocess.Popen(
            ['pdflatex', "SGBD/utilisateurs/"+self.auteur+"/temp/testexo.tex"], stdout=log,stderr=log)
        # on attend la fin de la compilation
        # (par défaut subprocess.Popen renvoi dès le lancement de la commande)
        process.wait()

        # on ferme le "fichier"
        os.close(log.fdWrite)
        # et on attend la fin du thread
        log.join()

        shutil.move('testexo.pdf',"SGBD/utilisateurs/"+self.auteur+"/temp/testexo.pdf")
        list_of_files = glob.glob(r"SGBD/utilisateurs/"+self.auteur+"/temp/*.pdf")
        latest_file = max(list_of_files, key=os.path.getctime)

        os.remove("testexo.aux")
        os.remove("testexo.log")
        os.remove("testexo.out")
        # os.remove("testexo.toc")

        self.open_file(latest_file)

    def PrevisualtisationFeuille(self):
        if (self.etudiant):
            nom, prenom = self.etudiant
        else:
            nom, prenom = "temp", "temp"
        temp = open("SGBD/utilisateurs/"+self.auteur+"/temp/"+nom+"_"+prenom+".tex", "wb")
        with codecs.open("SGBD/utilisateurs/"+self.auteur+"/style.tex", encoding="utf-8", errors='replace') as fichier:
            contenu = fichier.readlines()
            write = True
            for k in contenu:
                if write:
                    if k.startswith(r'\begin{cours}'):
                        if self.questionCours != "":
                            temp.write(k.encode('utf-8'))
                            temp.write(self.questionCours.encode('utf-8'))
                        write = False
                    else:
                        if "\\end{document}" not in k:
                            temp.write(k.encode('utf-8'))
                else:
                    if k.startswith(r'\end{cours}'):
                        if self.questionCours != "":
                            temp.write(k.encode('utf-8'))
                        write = True

            temp.write(('\n').encode('utf-8'))

           # temp.write((r"\reversemarginpar").encode('utf-8'))

            for exoId in CreerFeuille.listeFinale.get(self.etudiant).keys():
                exo = [exoId,
                       CreerFeuille.listeFinale.get(self.etudiant).get(exoId).get("exo"),
                       CreerFeuille.listeFinale.get(self.etudiant).get(exoId).get("sol")]

                temp.write(("\n" + r"\begin{exo}" + "\n").encode('utf-8'))
               # temp.write(("\n" + r"\marginpar{\small{\vspace{\baselineskip} \hspace{0.05cm} \textcolor{rouge}{ID exo :}} " + str(
                #               exo[0]) + "}" +"\n").encode('utf-8'))
                temp.write(exo[1].encode('utf-8'))

                temp.write(("\n" + r"\end{exo}" + "\n").encode('utf-8'))

                temp.write(("\n" + "\n" + r"\begin{sol}" + "\n").encode('utf-8'))
                temp.write(exo[2].encode('utf-8'))
                temp.write(("\n" + r"\end{sol}" + "\n").encode('utf-8'))

            temp.write(("\end{document}").encode('utf-8'))
            temp.close()

            output = subprocess.check_output(["pdflatex", "SGBD/utilisateurs/"+self.auteur+"/temp/"+nom+"_"+prenom+".tex"])
            try:
                shutil.move(f'{nom}_{prenom}.pdf', "SGBD/utilisateurs/"+self.auteur+"/temp/"+nom+"_"+prenom+".pdf")
            except FileNotFoundError as e:
                messagebox.showerror(title="Erreur lors de la compilation",
                                     message="pdflatex est nécessaire à la compilation des fichers\nVeuillez l'installer avant de continuer")
            else:
                # création d'un pop-up dans le cas où c'est le dernier pdf générer
                list_of_files = glob.glob(r"SGBD/utilisateurs/" + self.auteur + "/temp/*.pdf")
                latest_file = max(list_of_files, key=os.path.getctime)
                if latest_file == "SGBD/utilisateurs/"+self.auteur+"/temp/"+nom+"_"+prenom+".pdf":
                    messagebox.showinfo(title="Veuillez patienter, compilation en cours",
                                        message="La prévisualisation s'ouvrira d'elle même")

                os.remove(f"{nom}_{prenom}.aux")
                os.remove(f"{nom}_{prenom}.log")
                os.remove(f"{nom}_{prenom}.out")
                self.open_file("SGBD/utilisateurs/"+self.auteur+"/temp/"+nom+"_"+prenom+".pdf")


    def LogCompilation(self):
        logWindow = Tk()
        logWindow.title = "Compilation en Cours"
        logText = Text(logWindow, bg="#E5E5E5")
        logText.pack()
        finishButton = Button(logWindow, text="Afficher l'exercice", state='disabled')
        finishButton.pack()
        writer = myThread("WriteInLog", logWindow, self.pipeReader)
        writer.start()
        logWindow.mainloop()
        writer.join()
        self.pipeReader.close()

    def WriteInLog(self):
        logText = self.logWindow.winfo_children()[0]
        finishButton = self.logWindow.winfo_children()[1]
        for line in iter(self.pipeReader.readline, ''):
            logText.configure(state='normal',fg='red')
            logText.insert('end', line)
            logText.see('end')
            logText.configure(state='disabled')
        self.pipeReader.close()
        finishButton.configure(command=self.logWindow.destroy, state='normal')

    def open_file(self, filename):
        if "win" in sys.platform.lower():
            os.startfile(filename)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])

    def fileno(self):
        """Return the write file descriptor of the pipe
      """
        return self.fdWrite

    def creation_temp(self):
        try:
            if not os.path.exists("temp"):
                os.makedirs('temp')
        except:
            messagebox.showerror("Impossible de créer le dossier temp. Essayez de créer un dossier temp.")
            return

    def on_closing(self):
        try:
            shutil.rmtree('./temp', ignore_errors=True)
        except:
            print("Impossible de supprimer le dossier temp.")
        self.application.destroy()
        exit()
