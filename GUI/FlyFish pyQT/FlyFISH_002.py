# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 10:42:54 2012
 
@author: JeanPat
 
"""
import sys
import os
#import lxml.etree as et
import xml.etree.ElementTree as et
from copy import deepcopy
from PyQt4 import QtGui, QtCore
import qimage2ndarray as qnd
import imread
 
class CascadeMenu(QtGui.QWidget):
 
    """Four combobox to explore a tree content"""
 
    def __init__(self, etree):
        super(CascadeMenu, self).__init__()
        self.db = etree  # DataBase:The whole directory tree
        print "children's databe are projects"
        print self.db.getchildren()
 
        self.lbl = QtGui.QLabel("cytoM", self)
 
#==============================================================================
#         Connection en cascade des QCombobox
#==============================================================================
#==============================================================================
#         ## COMBO1 Projets
#==============================================================================
        #création du combo1
        self.combo1 = QtGui.QComboBox(self)#projects list
        self.label_combo1 = QtGui.QLabel("Project",self)
        # remplissage du combo1 avec les projets
        self.combo1.addItems(self.GetChildrenName(self.db))#project level-first element
        #les enfants (node2) d'un projet (node1) sont des lames (slides)        
        self.node1=self.db.getchildren()
        ##Connection combo1 vers combo2
        self.connect(self.combo1, QtCore.SIGNAL('currentIndexChanged(QString)'),self.changeindexcombo1)
        # ne faudrait-il pas connecter à combo 3 4 et 5 aussi?
#        self.connect(self.combo1, QtCore.SIGNAL('currentIndexChanged(QString)'),self.changeindexcombo2)
#        self.connect(self.combo1, QtCore.SIGNAL('currentIndexChanged(QString)'),self.changeindexcombo3)
#        self.connect(self.combo1, QtCore.SIGNAL('currentIndexChanged(QString)'),self.changeindexcombo4)
#        self.connect(self.combo1, QtCore.SIGNAL('currentIndexChanged(QString)'),self.changeindexcombo5)
 
#==============================================================================
#                                   COMBO2 Slides
#==============================================================================
 
        #création combo2
        self.combo2 = QtGui.QComboBox(self)#slides list
        self.label_combo2 = QtGui.QLabel("Slide",self)
        #         Fill combo2 with slides belonging to a project 
        self.node2=self.node1[0].getchildren()
        #fill from combo1 active item as parent
        parent=self.node1[self.combo1.currentIndex()]
        childrenlist=self.GetChildrenName(parent)
        #print "init combo2 :childrenlist",childrenlist
        self.combo2.addItems(QtCore.QStringList(childrenlist))
        ##Connection combo2 vers combo3
        self.connect(self.combo2, QtCore.SIGNAL('currentIndexChanged(QString)'),self.changeindexcombo2)
#        self.connect(self.combo2, QtCore.SIGNAL('currentIndexChanged(QString)'),self.changeindexcombo3)
#        self.connect(self.combo2, QtCore.SIGNAL('currentIndexChanged(QString)'),self.changeindexcombo4)
#        self.connect(self.combo2, QtCore.SIGNAL('currentIndexChanged(QString)'),self.changeindexcombo5)
 
#==============================================================================
#       COMBO3: field (location xy on the slide)
#==============================================================================
 
 
        self.combo3 = QtGui.QComboBox(self)#fields list
        self.label_combo3 = QtGui.QLabel("Field",self)
        #fill from combo1 active item as parent
        self.node3=self.node2[0].getchildren()# 15 mai2012: a quoi sert self.node3?
        parent=self.node2[self.combo2.currentIndex()]
        childrenlist=self.GetChildrenName(parent)
        #print "init combo3 :childrenlist",childrenlist
        self.combo3.addItems(QtCore.QStringList(childrenlist))        
 
        ##Connection combo3 vers combo4 
        self.connect(self.combo3, QtCore.SIGNAL('currentIndexChanged(QString)'),self.changeindexcombo3)
#        self.connect(self.combo3, QtCore.SIGNAL('currentIndexChanged(QString)'),self.changeindexcombo4)
#        self.connect(self.combo3, QtCore.SIGNAL('currentIndexChanged(QString)'),self.changeindexcombo5)
 
 
#==============================================================================
#       COMBO4: fluorochrome
#==============================================================================
        # creation combo4                                   
        self.combo4 = QtGui.QComboBox(self)
        self.label_combo4 = QtGui.QLabel("Fluo",self)
        #remplissage avec les enfants du parent actif de combo3
        self.node4=self.node3[0].getchildren()
        print "init node4",self.node4
        parent=self.node3[self.combo3.currentIndex()]
        childrenlist=self.GetChildrenName(parent)
        self.combo4.addItems(QtCore.QStringList(childrenlist))
        #Connection combo4 vers combo5; appel de chargement d'un fluo
        self.connect(self.combo4, QtCore.SIGNAL('currentIndexChanged(QString)'),self.changeindexcombo4)
#        self.connect(self.combo4, QtCore.SIGNAL('currentIndexChanged(QString)'),self.changeindexcombo5)
#==============================================================================
#       COMBO5: image                                    
#==============================================================================
 
        ##Connection combo5 vers : appel d'une image                                     
        self.combo5 = QtGui.QComboBox(self)#Fluorochromes list
        self.label_combo5 = QtGui.QLabel("Image",self)
        #remplissage
        self.node5=None                #fluo level
        self.node5=self.node4[0].getchildren()
        print "init node5",self.node5
        parent=self.node4[self.combo4.currentIndex()]
        childrenlist=self.GetChildrenName(parent)
        self.combo5.addItems(QtCore.QStringList(childrenlist))
        #connection, combo5 et combo5: euh?
        self.connect(self.combo5, QtCore.SIGNAL('currentIndexChanged(QString)'),self.changeindexcombo5)
 
#        ndimage=imread.imread("/home/claire/Applications/ImagesTest/MFISH/Dapi.tif")
#        convert=qnd.array2qimage(ndimage,normalize=True)
#        qpix = QtGui.QPixmap(convert)
        image = QtGui.QLabel(self)
        #image.setPixmap(qpix)
 
        # positionnement des widgets dans la fenêtre
        self.posit = QtGui.QGridLayout()
        self.posit.addWidget(self.label_combo1, 0, 0)
        self.posit.addWidget(self.label_combo2, 0, 1)
        self.posit.addWidget(self.label_combo3, 0, 2)
        self.posit.addWidget(self.label_combo4, 0, 3)
        self.posit.addWidget(self.label_combo5, 0, 4)
        self.posit.addWidget(self.combo1, 1, 0)
        self.posit.addWidget(self.combo2, 1, 1)
        self.posit.addWidget(self.combo3, 1, 2)
        self.posit.addWidget(self.combo4, 1, 3)
        self.posit.addWidget(self.combo5, 1, 4)
        self.posit.addWidget(self.lbl, 2, 0)
 
        self.posit.addWidget(image, 2, 0)
        self.setLayout(self.posit)
        self.setWindowTitle('Cascade Menus')
        self.show()
 
        pathto=os.path.join(str(self.combo1.currentText()),\
                            str(self.combo2.currentText()),\
                            str(self.combo3.currentText()),\
                            str(self.combo4.currentText()),\
                            str(self.combo5.currentText()))
        print "pathto",pathto
        self.lbl.setText(str(pathto))
        workdir="/home/simon/MFISH/"
        ndimage=imread.imread(workdir+str(pathto))
        convert=qnd.array2qimage(ndimage[::2,::2],normalize=True)
        qpix = QtGui.QPixmap(convert)
        image = QtGui.QLabel(self)
        image.setPixmap(qpix)
        self.posit.addWidget(image, 2, 0)
        self.setLayout(self.posit)
        self.setWindowTitle('Cascade Menus')
        self.show()
 
 
    def GetChildrenName(self,etree):
        """return the names (str) of the children of a Database etree.Element"""
        childrenlist=[]
        #print "GetChildren ... type(etree)",type(etree[0])
        children=etree.getchildren()
        #print children[0].get("name")
        for c in children:
            childrenlist.append(c.get("name"))
        return childrenlist
 
    def changeindexcombo1(self):
        """méthode exécutée en cas de changement d'affichage du combo1
        """
        #vide le contenu du combo enfant
        self.combo2.clear()
        #quel le parent?
        #recup l'item actif de combo1
        print "combo1 cur Index",self.combo1.currentIndex()
        #identifier le node correspondant,
        ## suppossons que ce soit==self.combo1.currentIndex()
        ##parent est un etree.Element, son nom devrait être l'item courant de combo1
        self.node1=self.db.getchildren()
        parent=self.node1[self.combo1.currentIndex()]
        #demander ses enfants,
        ##demander le nom des enfants
        childrenlist=self.GetChildrenName(parent)
        self.combo2.addItems(QtCore.QStringList(childrenlist))
        pathto=os.path.join(str(self.combo1.currentText()),\
                            str(self.combo2.currentText()),\
                            str(self.combo3.currentText()),\
                            str(self.combo4.currentText()),\
                            str(self.combo5.currentText()))
        self.lbl.setText(str(pathto))
        workdir="/home/simon/MFISH/"
        ndimage=imread.imread(workdir+str(pathto))
        convert=qnd.array2qimage(ndimage[::2,::2],normalize=True)
        qpix = QtGui.QPixmap(convert)
        image = QtGui.QLabel(self)
        image.setPixmap(qpix)
        #self.posit = QtGui.QGridLayout()
        #posit.addWidget(image, 2, 0)
        self.setLayout(self.posit)
        self.setWindowTitle('Cascade Menus')
        self.show()
 
    def changeindexcombo2(self):
        """méthode exécutée en cas de changement d'affichage du combo2
        """
        self.combo3.clear()
        #quel le parent?
        #recup l'item actif de combo1
        print "combo2 cur Index",self.combo2.currentIndex()
        #identifier le node correspondant,
        ## suppossons que ce soit==self.combo1.currentIndex()
        ##parent est un etree.Element, son nom devrait être l'item courant de combo1
        self.node2=self.node1[self.combo1.currentIndex()].getchildren()
        parent=self.node2[self.combo2.currentIndex()]
        #demander ses enfants,
        ##demander le nom des enfants
        childrenlist=self.GetChildrenName(parent)
        self.combo3.addItems(QtCore.QStringList(childrenlist))
        pathto=os.path.join(str(self.combo1.currentText()),\
                            str(self.combo2.currentText()),\
                            str(self.combo3.currentText()),\
                            str(self.combo4.currentText()),\
                            str(self.combo5.currentText()))
        self.lbl.setText(str(pathto))
        workdir="/home/simon/MFISH/"
        ndimage=imread.imread(workdir+str(pathto))
        convert=qnd.array2qimage(ndimage[::2,::2],normalize=True)
        qpix = QtGui.QPixmap(convert)
        image = QtGui.QLabel(self)
        image.setPixmap(qpix)
        #self.posit = QtGui.QGridLayout()
        self.posit.addWidget(image, 2, 0)
        self.setLayout(self.posit)
        self.setWindowTitle('Cascade Menus')
        self.show()
 
    def changeindexcombo3(self):
        """méthode exécutée en cas de changement d'affichage du combo3
        """
        self.combo4.clear()
        #quel le parent?
        #recup l'item actif de combo1
        print "combo3 cur Index",self.combo3.currentIndex()
 
        self.node3=self.node2[self.combo2.currentIndex()].getchildren()
        parent=self.node3[self.combo3.currentIndex()]
        #demander ses enfants,
        ##demander le nom des enfants
        childrenlist=self.GetChildrenName(parent)
        print "parent",parent
        print "combo3",childrenlist
        self.combo4.addItems(QtCore.QStringList(childrenlist))
        pathto=os.path.join(str(self.combo1.currentText()),\
                            str(self.combo2.currentText()),\
                            str(self.combo3.currentText()),\
                            str(self.combo4.currentText()),\
                            str(self.combo5.currentText()))
        self.lbl.setText(str(pathto))
        workdir="/home/simon/MFISH/"
        ndimage=imread.imread(workdir+str(pathto))
        convert=qnd.array2qimage(ndimage[::2,::2],normalize=True)
        qpix = QtGui.QPixmap(convert)
        image = QtGui.QLabel(self)
        image.setPixmap(qpix)
        #posit = QtGui.QGridLayout()
        posit.addWidget(image, 2, 0)
        self.setLayout(self.posit)
        self.setWindowTitle('Cascade Menus')
        self.show()
 
    def changeindexcombo4(self):
        """méthode exécutée en cas de changement d'affichage du combo4
        """
        self.combo5.clear()
        print "combo4 cur Index",self.combo4.currentIndex()
        self.node4=self.node3[self.combo3.currentIndex()].getchildren()
        parent=self.node4[self.combo4.currentIndex()]
        #demander ses enfants,
        ##demander le nom des enfants
        childrenlist=self.GetChildrenName(parent)
        self.combo5.addItems(QtCore.QStringList(childrenlist))
        pathto=os.path.join(str(self.combo1.currentText()),\
                            str(self.combo2.currentText()),\
                            str(self.combo3.currentText()),\
                            str(self.combo4.currentText()),\
                            str(self.combo5.currentText()))
        self.lbl.setText(str(pathto))
        workdir="/home/simon/MFISH/"
        ndimage=imread.imread(workdir+str(pathto))
        convert=qnd.array2qimage(ndimage[::2,::2],normalize=True)
        qpix = QtGui.QPixmap(convert)
        image = QtGui.QLabel(self)
        image.setPixmap(qpix)
        #posit = QtGui.QGridLayout()
        self.posit.addWidget(image, 2, 0)
        self.setLayout(self.posit)
        self.setWindowTitle('Cascade Menus')
        self.show()
 
    def changeindexcombo5(self):
        """méthode exécutée en cas de changement d'affichage du combo5
        """
        #self.combo5.clear()#surtout pas!!
        #quel le parent?
        #recup l'item actif de combo4
        print "combo5 cur Index",self.combo5.currentIndex()
        #identifier le node correspondant4
        ## suppossons que ce soit==self.combo1.currentIndex()
        ##parent est un etree.Element, son nom devrait être l'item courant de combo1
        #parent=self.node5[self.combo5.currentIndex()]
        #demander ses enfants,
        ##demander le nom des enfants
#        childrenlist=self.GetChildrenName(parent)
#        print "from changeindex combo5",childrenlist
#        self.combo5.addItems(QtCore.QStringList(childrenlist))
        pathto=os.path.join(str(self.combo1.currentText()),\
                            str(self.combo2.currentText()),\
                            str(self.combo3.currentText()),\
                            str(self.combo4.currentText()),\
                            str(self.combo5.currentText()))
        self.lbl.setText(str(pathto))
        workdir="/home/simon/MFISH/"
        ndimage=imread.imread(workdir+str(pathto))
        convert=qnd.array2qimage(ndimage[::2,::2],normalize=True)
        qpix = QtGui.QPixmap(convert)
        image = QtGui.QLabel(self)
        image.setPixmap(qpix)
        #posit = QtGui.QGridLayout()
        self.posit.addWidget(image, 2, 0)
        self.setLayout(self.posit)
        self.setWindowTitle('Cascade Menus')
        self.show()
 
def main():
#==============================================================================
#    Load a xml tree
#==============================================================================
#   bug 
    root=et.parse('/home/simon/DatabaseMFISH.xml').getroot()
    #p1=list(root)[0] #try to remove a project to see what's happen
    #root.remove(p1)
    print "root type",type(root)
    print root.getchildren()
    #print(et.tostring(root,pretty_print=True))
    app = QtGui.QApplication(sys.argv)
    ex = CascadeMenu(root)
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    main()