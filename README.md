# **Kholibri**

Kholirbi est un programme réalisé dans le cadre de projets tutoré afin de permettre à des enseignants de faciliter la création de fiches d'exercices rédigé en LaTeX. Ce programme permet de générer des PDFs en suivant les raccourcis de plusieurs utilisateurs et de choisir les exercices utilisés pour la génération selon leur niveau de difficulté, la classe et le chapitre auxquels ils appartiennent.

# **Documentation**
La documentation a été générée en utilisant [pdoc](https://pdoc.com/).
<br>
Ainsi, vous pouvez retrouver la documentation en ouvrant le fichier [html/Kholibri/index.html](html/Kholibri/index.html) avec votre navigateur favoris

# **Installation**

## Windows

### ~~Installeur~~
### Installation Manuelle
Pour installer manuellement Kholibri, il faut que vous installiez [LaTeX](https://www.latex-project.org/) et [Python](https://www.python.org/downloads/).
<br>
Vous aurez alors à ajouter le paquet Tkinter à votre installation de Python.

    pip install tkinter
Vous pourrez ensuite télécharger l'application via le [Github](https://github.com/Jamal7944/Kholibri)

## Linux

### **Tkinter**

Tkinter est la bibliothèque graphique libre d'origine pour le langage Python, permettant la création d'interfaces graphiques. Elle vient d'une adaptation de la bibliothèque graphique Tk écrite pour Tcl. *(source : https://fr.wikipedia.org/wiki/Tkinter)*

**Installation**

    sudo apt-get install python-tk

### **TeX Live**

TeX Live est une distribution TeX libre visant à fournir un environnement TeX/LaTeX complet et prêt à utiliser, sous les principaux systèmes d’exploitation. Depuis la version 2008, elle inclut un gestionnaire de paquets permettant la mise à jour de ses composants depuis internet. *(source : https://fr.wikipedia.org/wiki/TeX_Live)*

**Installation**

    sudo apt install texlive

**Dépendance necessaire**

    sudo apt install texlive-lang-french texlive-latex-extra texlive-science

### **Lire un PDF**

Cette application de génération de feuilles d'exercices mathématiques nécessite un logiciel de lecture de fichiers PDF reconnu par xdg-open comme par exemple :

    chromium
    firefox
    iceweasel
    chrome
    edge
    ...

Il est possible d'utilisé l'application sans une telle application, mais le programme n'ouvrira aucun fichier PDF par lui-même ( - n'affecte pas la génération).


# Contribuer

Les pull request sont la bienvenue.
Cependant, nous vous conseillons plutôt de faire un fork et de modifier le projet de votre côté étant donné qu'il n'est, pour l'instant, pas envisager de reprendre le développement du projet de manière intensive.


# **Auteurs**
<u>team 1</u>
<br>
[Jamal](https://github.com/Jamal7944)
<br>
[Alex](https://github.com/alexdgz)
<br>
[R3FF0X](https://github.com/R3FF0X)

<u>team 2</u>
<br>
[Jamal](https://github.com/Jamal7944)
<br>
[Lilian](https://github.com/Nexokk)
<br>
[Youllou](https://github.com/Youllou)

# **Remerciements**

Nous remercions notre professeur encadrant **M. Leray** ainsi que le client du projet, **M. Gobin**

# **License**

### Français

Cette application est gratuite : vous pouvez la redistribuer et/ou la modifier sous les termes de la GNU General Public License comme publié par la Free Software Foundation, sous la version 3 de la Licence ou (a votre option) tout autre version plus récente

Cette application est distribuée dans l'espoir qu'elle sera utile mais SANS AUCUNE GARANTIE; sans même la garantie de qualité marchande ou de réponse à un besoin particulier. Voir la GNU General Public License pour plus de détail.

Vous devriez recevoir une copie de la GNU General Public License avec cette application. Sinon, voir <https://www.gnu.org/licenses/>.


### English

This software is free : you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This software is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this software.  If not, see <https://www.gnu.org/licenses/>.
