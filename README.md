# **Application**

L'application de génération de sujets est un programme réalisé dans le cadre de projets tutoré afin de permettre à des enseignants de faciliter la création de fiches d'exercices rédigé en LaTeX. Ce programme permet de générer des PDFs en suivant les raccourcis de plusieurs utilisateurs et de choisir les exercices utilisés pour la génération selon leur niveau de difficulté, la classe et le chapitre auxquels ils appartiennent.

# **Installation**
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

Il est possible d'utilisé l'application sans une telle application mais le programme n'ouvrira aucun fichier PDF par lui-même ( - n'affecte pas la génération).


# **Licence**

### French

Ce programme est une application gratuite : vous pouvez la redistribuer et/ou la modifier sous les termes de la GNU General Public License comme publié par la Free Software Foundation, sous la version 3 de la Licence ou (a votre option) tout autre version plus récente

Ce programme est distribué dans l'espor qu'il sera utile mais SANS AUCUNE GARANTIE; sans même la garantie de qualité marchande ou de réponse à un besoin particulier. Voir la GNU General Public License pour plus de détail.

Vous devriez recevoir une copie de la GNU General Public License avec ce programme. Sinon, voir <https://www.gnu.org/licenses/>.


### English

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
