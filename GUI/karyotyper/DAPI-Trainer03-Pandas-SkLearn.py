# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 13:08:57 2011

@author: Jean6PAtrick Pommier
"""
import KarIO
import os
import pylab
import pandas
import numpy as np
from sklearn import svm
#make a configurator object
config=KarIO.ClassifConf()
#build the the name feature file
##list all the feature files
##répertoire courant : os.listdir(os.getcwd())
featurespath=os.path.join(os.getcwd(),"Results","features")
labelpath=os.path.join(os.getcwd(),"Results","labels")
#print featurespath
##open features csv files
featuresFilesList=os.listdir(featurespath)
labelsFilesList=os.listdir(labelpath)
##
metalist=[0,1,2,3,4]
def makeDataShape(meta):
    featfile=config.user+'-'+config.slide+'-'+config.metaphases_list[meta]+'-'+config.counterstain+'.csv'
    labelfile='shapeCateg-'+featfile
    fea=pandas.read_csv(os.path.join(featurespath,featfile),header=None,index_col=None,names=['particle','ratio','area'])
    lab=pandas.read_csv(os.path.join(labelpath,labelfile),header=None,index_col=None,names=['particle','type'])
    del lab['particle']    
    #merge columns:features and label
    data=fea.join(lab)
    data.insert(0,'meta',int(config.metaphases_list[meta]))
    #print data
    return data

bigdata=makeDataShape(0)
for meta in metalist:
    bigdata=bigdata.append(makeDataShape(meta),ignore_index=True)

single=bigdata[bigdata['type']=='single']
touching=bigdata[bigdata['type']=='touching']
nuclei=bigdata[bigdata['type']=='nuclei']
dusts=bigdata[bigdata['type']=='dusts']

##ploting with pylab
#different colors according to the category

fig=pylab.figure()
ax = fig.add_subplot(111)
ax.scatter(single['ratio'],single['area'],c='green',marker='o')
ax.scatter(touching['ratio'],touching['area'],c='red',marker='o')
ax.scatter(nuclei['ratio'],nuclei['area'],c='blue',marker='o')
ax.scatter(dusts['ratio'],dusts['area'],c='pink',marker='o')

#train a classifier
trainedData=bigdata[bigdata['meta']<15]
untrained=bigdata[bigdata['meta']>=15]
print 'trained data'
print trainedData[:5]
#extract two columns from trainedData
#convert to numpy array
features=trainedData.ix[:,['ratio','area']].as_matrix(['ratio','area'])
test_features=untrained.ix[:,['ratio','area']].as_matrix(['ratio','area'])
print 'features'
print features[:5]
print 'features shape',features.shape
print 'features type',type(features)
##label is a string:single, touching,nuclei,dust
print 'labels convertion'
lab1=trainedData['type']
print 'lab1',type(lab1)
f=pandas.Factor(lab1)
print 'factor f',type(f)
print 'labels',f.labels[:5]
print 'labels type',type(f.labels)
print 'labels shape',f.labels.shape
#
##Classify with sklearn
classifier = svm.SVC()
model = classifier.fit(features,f.labels)
predicted=classifier.predict(test_features)

#match predicted /classified
hiddenlab1=untrained['type']
hiddf=pandas.Factor(hiddenlab1)
match=(predicted==hiddf.labels)
print"prediction"
print predicted[:5]
print 'true classification'
print hiddf.labels[:5]
print 'match'
print match[:5]
##Count sucess
success=np.sum(match[:]==True)
rate=100.0*success/(1.0*len(match))
print 'rate of good classification',success,'out of',len(match),'particles'
print rate,'% success'