# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 15:44:42 2011

@author: jean-pat
"""
#!/usr/bin/env python
#
import os, pygame,csv
import ConfigParser as CfgP
from pygame.locals import*
import KarIO                

def load_image(name, colorkey=None):
    fullname=os.path.join("data", name)
    try:
        image=pygame.image.load(fullname)
    except pygame.error, message:
        print "Impossible de charger l'image:",name
        raise SystemExit, message
    #image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
    
                
class Ichrom(pygame.sprite.Sprite):
    def __init__(self,image,ref,initpos):
        pygame.sprite.Sprite.__init__(self)
        self.ref=ref#particule name
        self.type=""
        self.pos = initpos
        self.image,self.rect=image
        #self.image=self.image.convert()
        self.image.set_colorkey((0,0,0), RLEACCEL)
        self.original=image
        #self.original=self.original.convert()
        self.rotation=0
        self.mode="translation"
        #print "self.rect",self.rect,"-self.image:",self.image
        self.button=(0,0,0)#mouse buttons not pressed
        #self.selected = 0
        self.mouseover=False
        self.focused=False
        self.rect.topleft=initpos
        print "init chrom at ",self.pos
    def rollover(self,rotationmode):
        """Test if the mouse fly over the chromosome 
        self.mouseover==True if mouse flying over the chrom,
        False if not"""
        mpos=pygame.mouse.get_pos()#mouseposition
        #test if mouse roll over the sprite
        if rotationmode==0:
            self.mode="translation"
        if rotationmode==1:
            self.mode="rotation"
            print pygame.mouse.get_rel()
        if self.rect.collidepoint(mpos):
            self.mouseover=True
        else:
            self.mouseover=False
            
    def update(self,classifiergroup,background):
        self.button=pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()
        self.selected=self.rect.collidepoint(mpos)
        #the mouse flies over a chromosome
        if (self.mouseover):
            if self.mode=="translation":
                #print "mouse pos:",mpos
                collision=pygame.sprite.spritecollide(self,classifiergroup,False)
                #collision should contains only one element            
                if len(collision)>0:
                    #print collision[0].category
                    self.type=collision[0].category
                    print "particle "+self.ref+" is classified to "+self.type
                if self.button==(1,0,0):     
                    pos = pygame.mouse.get_pos()
                    self.rect.center = pos
            elif self.mode=="rotation":
                #test mouse movement
                mrel=pygame.mouse.get_rel()
                if self.rotation>=360:
                    self.rotation=0
                    self.image=self.original
                elif mrel[0]>0:
                    self.rotation=self.rotation+10
                    self.image=pygame.transform.rotate(self.original[0],self.rotation)
                    self.rect=self.image.get_rect(center=self.rect.center)
                elif mrel[0]<0:
                    self.rotation=self.rotation-10
                    self.image=pygame.transform.rotate(self.original[0],self.rotation)
                    self.rect=self.image.get_rect(center=self.rect.center)
                
class Classifier(pygame.sprite.Sprite):
    '''When a chrom is moved is moved into a category '''
    def __init__(self,initpos,size,category):
        pygame.sprite.Sprite.__init__(self)
        self.category=category
        self.image = pygame.Surface(size)
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha()
        self.rect= self.image.get_rect()
        #pygame.draw.rect(screen, color, (x,y,width,height), thickness)
        pygame.draw.rect(self.image, (255,0,0,255), (0,0,size[0],size[1]),1)
        self.rect.topleft= initpos
        
    def update(self): 
        pass        
        
def main():
    
    conf=KarIO.ClassifConf()
    ### prepare a csv file to save the results ##########
    result_file=open(os.path.join("shapeCateg-"+conf.user+"-"+
                                conf.slide+"-"+
                                conf.metaphases_list[0]+"-"+
                                conf.counterstain+'.csv'), 'w')
    result = csv.writer(result_file, delimiter=';', lineterminator='\n')
    row=[]
    ###########
    pygame.init()
    screen = pygame.display.set_mode(conf.screensize)
    metaphaseList=conf.metaphases_list
    print metaphaseList[0]
    conf.set_particlespath(0)
    print conf.path
    conf.set_particles(conf.path)
    print "conf.particlesList",conf.particlesList
    pygame.display.set_caption("Karyotyper")
    pygame.mouse.set_visible(True)
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 100, 0))

    screen.blit(background,(0, 0))
    pygame.display.flip()
    
    imagesList=[]
    for i in conf.particlesList:
        im=load_image(os.path.join(conf.path,i))
        imagesList.append(im)
    print len(imagesList)
    i1=load_image("/home/claire/Applications/ImagesTest/jp/Jpp48/13/DAPI/particles/part15.png", -1)
    i2=load_image("/home/claire/Applications/ImagesTest/jp/Jpp48/13/DAPI/particles/part12.png", -1)
    chrList=[]   
    n=0
    li=20
    col=0
    for c in imagesList:
        chrList.append(Ichrom(c,conf.particlesList[n],(col,li)))
        print conf.particlesList[n]
        n=n+1
        col=col+20
        #li=
    #chr0= Ichrom(ima)
    chr1 = Ichrom(i1,"part15",(0,0))
    #chr1 = Krom(i1,(0,0))
    chr2=Ichrom(i2,"part12",(30,30))
    #chr2=Krom(i2,(30,30))
    print "---------classif---------------"
    print conf.catlist[0]
    print type(conf.boxpos[0])
    categList=[]
    categ1=Classifier(conf.boxpos[0],conf.boxsize,conf.catlist[0])
    categList.append(categ1)
    categ2=Classifier(conf.boxpos[1],conf.boxsize,conf.catlist[1])
    categList.append(categ2)
    categ3=Classifier(conf.boxpos[2],conf.boxsize,conf.catlist[2])
    categList.append(categ3)
    categ4=Classifier(conf.boxpos[3],conf.boxsize,conf.catlist[3])
    categList.append(categ4)
    
    
    allsprites = pygame.sprite.RenderPlain(chrList)
    allcategories=pygame.sprite.RenderPlain(categList)
    clock = pygame.time.Clock()
    
    config = CfgP.RawConfigParser()
    #spritelist=(chr1,chr2)
    spritelist=chrList
    rotationmode=0
    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                #spritelist=(chr1,chr2)
                #building a config file
                #saveCfgFile(config,spritelist)
                for s in spritelist:
                    ##cfg file"""
                    print "saving config"
                    cref=s.ref
                    ctype=s.type
                    config.add_section(cref)
                    config.set(cref,'shape type', ctype) 
                    ## csv file ##
                    row.append((s.ref,s.type))
                    result.writerows(row)
                    row.pop()
                    ####
                config.write(open('shape.cfg','w'))
                print "config saved" 
                ###save the csv file ####
                result_file.close()
                del result
                del result_file
                return
            elif event.type == KEYDOWN and event.key == K_r:
                rotationmode=rotationmode+1
                if rotationmode==1:
                    print "rotation ON"
                if rotationmode==2:
                    print "rotation OFF"
                    rotationmode=0
            if event.type ==pygame.MOUSEBUTTONDOWN:
                #need to be modified to handle a list of chromosomes
#                chr1.rollover(rotationmode)
#                chr2.rollover(rotationmode)
                for k in chrList:
                    k.rollover(rotationmode)
                    
        allsprites.update(allcategories,background)
        allcategories.update()
        ##
        ##Search which chromosome is moved
        ##into which category and classify  
        ##that chromosome in that category
#        collision=pygame.sprite.groupcollide(allcategories,allsprites,False,False,None)
#        for classified in collision.keys():
#            print classified
        screen.blit(background,(0,0))
        allsprites.draw(screen)
        allcategories.draw(screen)
        pygame.display.flip()
    
if __name__ == '__main__': main()