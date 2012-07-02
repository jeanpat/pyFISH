# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 10:26:01 2012

@author: Jean-Patrick Pommier
"""

import numpy as np
import networkx as nx
import mahotas as mh
import pylab as plb 

def makelabelarray():
    label = np.array([[1,0,4,4],
                     [0,0,0,2],
                     [3,0,2,2],
                     [0,2,0,5]])
    return label

def convertToGraph(dic, noBack=True):
    G = nx.Graph()
    G.add_nodes_from(dic.keys())
    for particle in dic.keys():
        list_touching_particles = dic[particle]
        # remove background
        if noBack:
            list_touching_particles.discard(0) 
        print 'v(',particle,')=',list_touching_particles
        for tp in list_touching_particles:
            G.add_edge(particle,tp)
    return G
    
def findneighborhoods(label,neighborhood):
    ''' given a labelled image, should return the adjacency list
        of particles, for a given neighborhood:
        
        neighborhood=np.array([0,1,0],[1,1,1],[0,1,0])
        
        The background (0), is kept as a particle neighbor 
        No fancy indexing
    '''
    #make the labels list
    labmax = label.max()
    #print labmax
    neighb_dic = {} # a dictionnary containing particle label as key and neighborhood
    for i in range(1,labmax+1):
        mask = (label ==i)
        #print mask
        dilated = mh.dilate(mask,neighborhood)
        neighbor = np.logical_and(dilated, np.logical_not(mask))
        #print neighbor
#==============================================================================
#         #Done without fancy indexing
#==============================================================================
        flatlab = np.ndarray.flatten(label)
        flatneighborhood = np.ndarray.flatten(neighbor)        
        flatneighbors = flatlab[flatneighborhood]
        flatneighbors.sort()
        #set is a trick so that each value of the neighborhoods is present only once
        neighb_dic[i] = set(flatneighbors)
        #print np.nonzero(flatneighbors)
    return neighb_dic
        
    
    
        
