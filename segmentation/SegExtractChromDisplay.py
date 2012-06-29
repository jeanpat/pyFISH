from scipy import ndimage as nd
#import scipy
import numpy as np
#import readmagick
import imread
import mahotas
import pymorph
import pylab
import os
from skimage import io as sio
#import math


def distanceTranform(bIm):
    #from pythonvision.org
    dist = nd.distance_transform_edt(bIm)
    dist = dist.max() - dist
    dist -= dist.min()
    dist = dist / float(dist.ptp()) * 255
    dist = dist.astype(np.uint8)
    return dist


def BorderKill(imlabel):
    '''remove labelled objects touching the image border'''
    #from pythonvision.org
    whole = mahotas.segmentation.gvoronoi(imlabel)
    borders = np.zeros(imlabel.shape, np.bool)
    borders[0, :] = 1
    borders[-1, :] = 1
    borders[:, 0] = 1
    borders[:, -1] = 1
    at_border = np.unique(imlabel[borders])
    for obj in at_border:
        whole[whole == obj] = 0
    return whole


def gray12_to8(im):
    i = 0.062271062 * im
    return pymorph.to_uint8(i)


def gray16_to8(im):
    i = 0.00390625 * im
    return pymorph.to_uint8(i)


def GradBasedSegmentation(im):
    blur = nd.gaussian_filter(im, 16)
    rmax = mahotas.regmax(blur)
    T = mahotas.thresholding.otsu(blur)
    bImg0 = im > T
    #bImg01=nd.binary_closing(bImg0,iterations=2)
    #bImg01=pymorph.close(bImg0, pymorph.sedisk(3))
    #bImg=pymorph.open(bImg01, pymorph.sedisk(4))
    bImg = pymorph.close(bImg0)
    b = pymorph.edgeoff(bImg)
    d = distanceTranform(b)
    seeds, nr_nuclei = nd.label(rmax)
    lab = mahotas.cwatershed(d, seeds)
    return BorderKill(lab)

def ModalValue(image):
    '''look for the modal value of an image'''
    #print image.dtype
    if image.dtype == "uint8":
        depthmax = 255
        print "8bits"
    if image.dtype == "uint16":
        depthmax = 65535
        print "16bits"
    histo = mahotas.fullhistogram(image)
    countmax = histo.max()
    #print "Searching modal value"
    #print "countmax:",countmax
    #print "image max",image.max()
    mig = image.min()  # image min graylevel
    mag = image.max()  # image max gray level
    mode = 0
    countmax = 0  # occurence of a given grayscale
    print "image min grey level:", mig, "  im max grey level:", mag
    for i in range(mig, mag - 1, 1):
        test = histo[i] > countmax
        #print "test:",test,"histo(",i,")=", histo[i],"max",countmax
        if  test:
            countmax = histo[i]
            mode = i
            #print "mode",mode
    return mode


def RemoveModalBackground(image):
    mode = ModalValue(image)
    back = np.zeros(image.shape, image.dtype)
    back.fill(mode)
    #print "def background:",back.mean()
    im = pymorph.subm(image, back)
    return im


def LowResSegmentation(image):
    '''Perform a simple threshold after DoG filtering'''
    noBack = RemoveModalBackground(image)
    #print "from Segmeta noBack:",noBack.min(),noBack.mean()
    blurLowRes = nd.filters.gaussian_filter(noBack, 13)
    blurHiRes = nd.filters.gaussian_filter(noBack, 1)
    midPass = pymorph.subm(blurHiRes, 0.70 * blurLowRes)
    binim = (midPass > 1.5 * midPass.mean())
    binLowRes = pymorph.open(binim, pymorph.sedisk(4))
    binLowRes = pymorph.close_holes(binLowRes)
    return binLowRes

def extractParticles(grayIm, labIm):
    ''' give a grayscaled and a labelled image,
        extract the segmented particles
    , returns a list of flattened particles'''
    #grayIm and labIm should have the same size

    def unflattenParticles(flatParticleList):
        '''take a list of flat particles and unflat them to yield an image'''
        unflatList = []
        lenFlatList = len(flatParticleList)
        for i in range(0, lenFlatList):
            #get the i particle:current Particle
            curPart = flatParticleList[i]  # current particle
            #x values(col) are stored in the third col (3-1)
            colmax = curPart[:, 2].max()
            colmin = curPart[:, 2].min()
            #y values(li) are stored in the fourth col (4-1)
            limax = curPart[:, 3].max()
            limin = curPart[:, 3].min()
            unflatIm = np.zeros((limax - limin + 1, colmax - colmin + 1), np.int16)
            #number of pixels in the particle
            nbPixel = len(curPart[:, 1])  # count how many lines at col=1
            for line in range(0, nbPixel):
                col = curPart[line, 2]
                li = curPart[line, 3]
                pixVal = curPart[line, 1]
                unflatIm[li - limin, col - colmin] = pixVal
            unflatList.append(unflatIm)
        return unflatList

    sx = grayIm.shape[0]
    sy = grayIm.shape[1]
    #flatten grayIm
    fg = grayIm.flatten()
    fl = labIm.flatten()
    labmax = fl.max()
    #print fg
    #print fl
    #build two 2D array containing x and y
    #of each pixel of the grayIm
    ax = np.zeros((sx, sy), np.int16)
    ay = np.zeros((sx, sy), np.int16)
    #vectorization with numpy may be 
    #more efficient than two loops
    for j in range(0, sy):
        for i in range(0,sx):
            ax[i,j]=j#filling ax with x=col
            ay[i,j]=i#filling ay with y values y=li
    #flat arrays of coordinates
    fax=ax.flatten()
    fay=ay.flatten()
    #1D merge graylevel, label and coordinates 
    #in one 1D array of 4-uplet
    extract=np.vstack((fl,fg,fax,fay))
    #transpose to watch it easily
    eT=extract.T
    #create a list of flatten particles
    #labIndex takes the value from 1 (the first particle to labmax the\
    #label of the last particle
    flatParticleList=[]#from Matthieu Brucher
    for labIndex in range(1,labmax+1):
        flatParticleList.append(eT[eT[:,0]==labIndex])#from Matthieu Brucher
    return unflattenParticles(flatParticleList)

def makeMosaic(listIm,sizemin,sizemax): 
    '''make a mosaic of array'''
    def CleanImageList2(liste):
        '''Remove too small or too large objects from the list
           create a new list
        '''
        cleanList = []
        for i in range(0, len(liste)):
            binIm = liste[i] > 0
            area = np.sum(binIm[:, :] == True)
            if (sizemin < area < sizemax):
                cleanList.append(liste[i])
        return cleanList

    def CleanImageList(liste):
        '''Remove too small or too large objects from the list
        '''
        #print "element",len(liste)
        #print "min", sizemin,"max",sizemax
        i = len(liste) - 1
        while i != -1:
            binIm = liste[i] > 0
            area = np.sum(binIm[:, :] == True)
            #print "i in cleanlist",i
            if ((area < sizemin) or (area > sizemax)):
                #print "trop petit/grand",i,"area",area
                liste.remove(liste[i])
            i = i - 1
        return liste

    def ResizeImageInList(ImList):
        '''Find the largest wdth and height image
        Return a list of images of same width/height
        '''
        maxwidth = 0
        maxheight = 0
        for i in range(len(ImList)):
            width = np .shape(ImList[i])[1]  # width=column
            height = np.shape(ImList[i])[0]  # height=line
            #print "width:height",width,":",height
            if width > maxwidth:
                maxwidth = width
            if height > maxheight:
                maxheight = height
            #print "maxwidth:maxheight",maxwidth,":",maxheight                
        NewList = []
        for i in range(0, len(ImList)):
            width = np.shape(ImList[i])[1]
            height = np.shape(ImList[i])[0]
            diffw = maxwidth - width
            startw = round(diffw / 2)
            diffh = maxheight - height
            starth = int(round(diffh / 2))
            startw = int(round(diffw / 2))
            #print "im:",i," diffw",diffw," starth",starth
            #make en empty image
            newIm = np.zeros((maxheight, maxwidth))
            #print "im:",i," starth:starth+height",starth,":",starth+height
            #print "im:",i," startw:startw+width",startw,":",startw+width
            #print "shape input image",np.shape(ImList[i])
            newIm[starth:starth + height, startw:startw + width] = ImList[i][:, :]
            NewList.append(newIm)
        return NewList
    cleanedL = CleanImageList2(listIm)
    resizedImList = ResizeImageInList(cleanedL)
    lmax = len(resizedImList)  # list of image
    row = int(round(np.sqrt(lmax)))
    col = row + 1
    pylab.gray()
    pylab.subplot(row, col, lmax)
    #ten columns and len(Particles)/ColNum lines
    for i in range(0, len(resizedImList)):
            pylab.subplot(row,col, i + 1, frameon = False, xticks = [], yticks = [])
            #Greys cmap makes an inverse DAPI image           
            pylab.imshow(resizedImList[i], interpolation = None)
            pylab.set_cmap(pylab.cm.Greys)
    pylab.show()
#
#Modify your path to your images here. The script works with 16bits images
#
user = os.path.expanduser("~")
workdir = os.path.join(user, "QFISH", "JPPAnimal", "jpp53", "28", "dapi")
workdirCy3 = os.path.join(user, "QFISH", "JPPAnimal", "jpp53", "28", "cy3")
imfile = "1.tif"
complete_path = os.path.join(workdir, imfile)
cy3path = os.path.join(workdirCy3, imfile)
#
#
if __name__ == "__main__":
#==============================================================================
#     # Load images
#==============================================================================
    #dapi=mahotas.imread(complete_path)
    dapi = sio.imread(complete_path)
    cy3 = sio.imread(cy3path)
    
    im1 = RemoveModalBackground(dapi)
    
    #im2 = RemoveModalBackground(cy3)
    #8bits dapi image
    d8 = gray12_to8(im1)
    complete_path = os.path.join(workdir, "dapi.png")
    imread.imsave(complete_path, d8)
#==============================================================================
#     #try a simple segmentation procedure
#==============================================================================
    print "segmenting..."
    filteredDAPI = LowResSegmentation(im1)
    imlabel, npart = nd.label(filteredDAPI)
    #label2=mahotas.morph.close_holes(imlabel>0)
    #imlab,N=nd.label(GradBasedSegmentation(dapi))
    print "showing..."
    ParticlesDAPI = extractParticles(im1, imlabel)
    #Particles is a list of images (np.array of scalar)
    ParticlesCy3 = extractParticles(cy3, imlabel)
    #makeMosaic(ParticlesDapi, 1200, 8000)
    makeMosaic(ParticlesDAPI, 1200, 8000)
    makeMosaic(ParticlesCy3, 1200, 8000)
