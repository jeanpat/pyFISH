# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 14:25:26 2012

@author: simon
"""
import os
import sys
sys.path.append('/home/simon/ProjetPython/projet particule et objet')
import SegExtractChromDisplay as ex
import Neighborhood as ng
#import prepro as pp



#import cv2
#import scipy
import numpy as np
from scipy import ndimage as nd
import pylab as plb

import networkx as nx

#import readmagick
#import imread
import mahotas
import pymorph
#
#
#import skimage as sk
from skimage import io as sio
#from skimage import morphology as mo
##from skimage.transform.
#
#import skimage.filter as sf
#import skimage.segmentation as seg

#==============================================================================
# 
#==============================================================================
if __name__ == "__main__":
    user = os.path.expanduser("~")
    #/home/simon/QFISH/HPS/JPP60-3/DAPI
    #workdirDAPI = os.path.join(user, "QFISH", "JPPAnimal", "JPP52", "12", "DAPI")
    workdirDAPI = os.path.join(user, "QFISH", "HPS", "JPP60-3", "DAPI")
    #workdirCy3 = os.path.join(user, "QFISH", "JPPAnimal", "JPP52", "12", "CY3")
    imfile = "1.tif"
    #imfile = "1.TIF"
    dapi_path = os.path.join(workdirDAPI, imfile)
    #cy3_path = os.path.join(workdirCy3, imfile)
#==============================================================================
#     # Load images
#==============================================================================
    dapi = sio.imread(dapi_path)
    #cy3 = sio.imread(cy3_path)
    plb.imshow(dapi)
    plb.show()
#==============================================================================
#     Segmentation
#==============================================================================
    small = nd.zoom(dapi, 0.5)
    labelDAPI, n= nd.label(ex.LowResSegmentation(small))
    obj = ex.extractParticles(small,labelDAPI)
    ex.makeMosaic(obj,20,10000)
    print n
    #broken = pymorph.sedisk()
    pixel_distance = 1
    #se = np.array([[1,1,1],[1,1,1],[1,1,1]])
    se = np.uint(pymorph.sedisk(pixel_distance)) #2+1+2=5
    print se
    print 'find neighbours at ',pixel_distance, 'from particles'
    g = ng.findneighborhoods(labelDAPI, se)
    print 'converting to networkx'
    G = ng.convertToGraph(g, noBack=True)
#==============================================================================
#     Graphic display
#==============================================================================
    plb.subplot(121, frameon = False, xticks = [], yticks = [])
    plb.imshow(small)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    plb.subplot(122, frameon = False, xticks = [], yticks = [])
    plb.imshow(labelDAPI)
    plb.show()
    #plb.subplot(133)
    nx.draw_networkx(G)
    plb.show()
