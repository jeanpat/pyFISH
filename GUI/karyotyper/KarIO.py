# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 13:23:54 2011

@author: Jean-Patrick Pommier
"""

import ConfigParser as CfgP
import os,sys,ast
#   
class ClassifConf():
    def __init__(self):
        self.config=CfgP.RawConfigParser()
        self.config.read('configuration.cfg')
        print self.config
        self.wdir=self.config.get('Images Path','work_dir')
        self.user=self.config.get('Images Path','user')
        self.slide=self.config.get('Images Path','slide')
        self.set_metaphaseList()
        self.path=None
        #False if no particles images saved
        self.particles=False
        #self.trained==False is no classification was done
        self.trained=False
        #Fluo
        #self.counterstain=None
        self.set_ClassifConf()
        self.set_Fluorochromes() 
    def set_metaphaseList(self):
        '''convert the string containing the metaphases list
        stored in the config file to a list of integers'''
        tmp=self.config.get('Images Path','field_list')
        #self.metaphases_list=map(lambda x:int(x),tmp.split(','))
        self.metaphases_list=tmp.split(',')
    def set_particlespath(self,index):
        '''Set the path to the particles directory, in the DAPI directory'''
        self.path=os.path.join(self.wdir,self.user,self.slide,self.metaphases_list[index],self.counterstain,"particles")
#        print "########### set_particlespath called ###########"        
#        print "self.path",self.path
#        print "os.listdir",os.listdir(self.path)
#        print "               *************                   "
    def set_particles(self,path):
        '''set to true if chromosomes were segmented '''
        print "os.path.isdir:",os.path.isdir(path)    
        if os.path.isdir(path):
            self.particles=True
            #print "os.listdir",os.listdir(path)
            self.particlesList=os.listdir(path)
#            print "#set_particles called##"
#            print self.particlesList
    def set_trained(self):
        '''set to true if chromosomes images were classified
        manually to single chr, overlapping chr, nuclei, dusts'''
        self.trained=False
    def set_ClassifConf(self):
        '''read conf param for the classif GUI:
            screen size, number of classif box their size'''
        #seen at stackoverflow.com: T2 = [map(int, x) for x in T1]
        #to convert a string to a list of tuples
        #map(lambda x: int(x), ['1', '2', '3'])
        tmpsize=self.config.get('ClassifierGUI','screen_size').split(',')
        #print tmpsize
        self.screensize=map(lambda x:int(x),tmpsize)
        self.catsize=int(self.config.get('ClassifierGUI','categories_number'))
        self.catlist=self.config.get('ClassifierGUI','categories_list').split(',')
        tmpbox=self.config.get('ClassifierGUI','box_size').split(',')
        #print 'tmpbox',tmpbox
        self.boxsize=map(lambda x:int(x),tmpbox)
        tmpboxpos=ast.literal_eval(self.config.get('ClassifierGUI','box_position'))
        #print tmpboxpos
        self.boxpos=list(tmpboxpos)
        
    def set_Fluorochromes(self):
        '''#Fluorochromes'''
        self.counterstain=self.config.get('Fluorochromes','Counter_stain') 
        #print "cs:",self.counterstain        
        self.probes=self.config.get('Fluorochromes','Probes').split(',')
    def get_ParticlesList(self):
        pass
        #get the pass to the particles directory
        #then make the list of the files in it
#        path=os.listdir(path)
def main():
    configurator=ClassifConf()
    configurator.set_particlespath(1)
    configurator.set_particles(configurator.path)
    print "path:",configurator.path
    print type(configurator.path)
if __name__ == '__main__': main()