#installer pygame : pip install pygame
#installer pyint : pip install pyint
# /!\ #si on clique trop vite sur les boutons on peut avoir la valeur plusieurs fois
#les threads tournent encore apres fermeture de la fenetre
import pygame
import os

import time
from pygame.locals import*
import threading
import queue
pygame.init()

#initialise la liste de batiment depuis 0 ou depuis le fichier de sauvegarde
def listebatiment(charger,batiment,population2,production2,pollution2,nourriture2,argent2):
    batiment2=[]
    #initialise les batiment pour une nouvelle partie
    if charger==0:
        for i in range(72):
            batiment2.append("0")
    #charge a partir du fichier sauvegarde
    if charger==1:
        fic=open("sauvegarde/sauvegarde.txt",'r')
        for ligne in fic:
            b=ligne.split()
            b=b[0]
            batiment2.append(b)
        fic.close()
    #sauvegarde dans le fichier
    if charger==2:
        fic=open("sauvegarde/sauvegarde.txt",'r+')
        for i in range(72):
            fic.write(batiment[i])
            fic.write("\n")
        fic.write(str(argent2))
        fic.write("\n")
        fic.write(str(population2))
        fic.write("\n")
        fic.write(str(production2))
        fic.write("\n")
        fic.write(str(pollution2))
        fic.write("\n")
        fic.write(str(nourriture2))
        fic.write("\n")
        fic.close()
    if charger==0 or charger==1:
        return(batiment2)

#verifie si on peut effectuer l'achat et renvoit les valeurs a soustraire (population,argent...)
def verif_achat(choix,argent2,population2,production2,pollution2):
    #la liste sert a retourner plusieurs valeurs
    liste=[]
    prix=0
    population=0
    production=0
    pollution=0
    nourriture=0
    #premier village
    if choix==0 or choix==54:
        prix=300
        population=1000
        pollution=50
    #deuxieme village
    if choix==1 or choix==55:
        prix=500
        population=2500
        production=-1000
        nourriture=-250
        pollution=50
    #troisieme village
    if choix==2 or choix==56:
        prix=1000
        population=5000
        production=-2500
        nourriture=-500
        pollution=100
    #premiere usine nucleaire
    if choix==3 or choix==7 or choix==21 or choix==25 or choix==29:
        prix=200
        population=-200
        production=250
        pollution=75
    #premiere usine electrique
    if choix==4 or choix==8 or choix==22 or choix==26 or choix==30:
        prix=350
        population=-200
        production=180
        pollution=25
    #deuxieme usine nucleaire
    if choix==5 or choix==9 or choix==23 or choix==27 or choix==31:
        prix=500
        population=-100
        production=500
        pollution=125
    #deuxieme usine electrique
    if choix==6 or choix==10 or choix==24 or choix==28 or choix==32:
        prix=700
        population=-100
        production=360
        pollution=75
    #enlever colline
    if choix==11 or choix==53:
        prix=100
    #premier champs
    if choix==12 or choix==14 or choix==16 or choix==36 or choix==38 or choix==40:
        prix=250
        population=-25
        production=-20
        nourriture=100
        if pollution2>400:
            nourriture=75
    #deuxieme champs
    if choix==13 or choix==15 or choix==17 or choix==37 or choix==39 or choix==41:
        prix=500
        population=-50
        production=-50
        nourriture=250
        if pollution>400:
            nourriture=185
    #replenter foret
    if choix==18 or choix==19 or choix==20:
        prix=50
        pollution=-20
    #eolienne
    if choix==33 or choix==34 or choix==35 or choix==57 or choix==63:
        prix=100 
        production=60
        pollution=-20
    #pont
    if choix==42:
        prix=350
    #barrage
    if choix==43:
        prix=600
        population=-300
        production=250
        pollution=200
    #premiere usine solaire
    if choix==44 or choix==46:
        prix=400
        population=-200
        production=250
    #deuxieme usine solaire
    if choix==45 or choix==47:
        prix=750
        population=-150
        production=400
    #premiere usine petrole
    if choix==48 or choix==50:
        prix=250
        population=-300
        production=500
        pollution=150
    #deuxieme usine petrole
    if choix==49 or choix==51:
        prix=600
        population=-150
        production=800
        pollution=150
    #supprimer foret
    if choix==58 or choix==52:
        prix=100
        pollution=50
    #houle
    if choix==64 or choix==68:
        prix=150
        production=25
    #hydrolienne
    if choix==65 or choix==69:
        prix=200
        production=50
    #bateau peche
    if choix==66 or choix==70:
        prix=200
        nourriture=75
    #petrole mer
    if choix==67 or choix==71:
        prix=500
        production=150
        pollution=150
    #supprimer innondation
    if choix==59 or choix==60 or choix==61 or choix==62:
        prix=200
    if argent2 >= prix and population2+population>=0 and production2+production>=0 and nourriture2+nourriture>=0:
            verif=prix
    if argent2 < prix or population2+population<0 or production2+production<0 or nourriture2+nourriture<0:
        verif=0
    prix=-prix
    liste=[verif,population,production,pollution,nourriture,prix]
    return(liste)

#reduit la production des fermes si le premier pallier de pollution est atteint
def pollution_1(batiment,nourriture2):
    if batiment[12]=="1":
        nourriture2=nourriture2-25
    if batiment[13]=="1":
        nourriture2=nourriture2-65
    if batiment[14]=="1":
        nourriture2=nourriture2-25
    if batiment[15]=="1":
        nourriture2=nourriture2-65
    if batiment[16]=="1":
        nourriture2=nourriture2-25
    if batiment[17]=="1":
        nourriture2=nourriture2-65
    if batiment[36]=="1":
        nourriture2=nourriture2-25
    if batiment[37]=="1":
        nourriture2=nourriture2-65
    if batiment[38]=="1":
        nourriture2=nourriture2-25
    if batiment[39]=="1":
        nourriture2=nourriture2-65
    if batiment[40]=="1":
        nourriture2=nourriture2-25
    if batiment[41]=="1":
        nourriture2=nourriture2-65
    return(nourriture2)

#quand le pallier 2 de pollution est atteint supprimme les batiments et enleve les bonus que sa apporte (pollution,population mais ne redonne pas l'argent)
def innondation(batiment,production2,pollution2,nourriture2,population2):
    population=0
    production=0
    pollution=0
    nourriture=0
    liste2=batiment
    if batiment[21]=="1":
        liste2[21]="0"
        population=population+200
        production=production-250
        pollution=pollution-75
    if batiment[22]=="1":
        liste2[22]="0"
        population=population+200
        production=production-180
        pollution=pollution-25
    if batiment[23]=="1":
        liste2[23]="0"
        population=population+100
        production=production-500
        pollution=pollution-125
    if batiment[24]=="1":
        liste2[24]="0"
        population=population+100
        production=production-360
        pollution=pollution-75
    if batiment[33]=="1":
        liste2[33]="0"
        production=production-60
        pollution=pollution-20
    if batiment[36]=="1":
        liste2[36]="0"
        population=population+25
        production=production-20
        nourriture=nourriture-100
    if batiment[37]=="1":
        liste2[37]="0"
        population=population+50
        production=production-50
        nourriture=nourriture-250
    if batiment[42]=="1":
       liste2[42]="0"
    if batiment[43]=="1":
        liste2[43]="0"
        population=population+300
        production=production-250
        pollution=pollution-200
    if batiment[57]=="1":
        liste2[57]="0"
        production=production-60
        pollution=pollution-20
    liste2[59]="1"
    liste2[60]="1"
    liste2[61]="1"
    liste2[62]="1"
    liste2=[liste2,production,population,pollution,nourriture]
    return(liste2)

#affiche les gains et perte quand on met le curseur de la souris sur un icone du shop
def affichage_prix(choix,batiment,argent2,population2,production2,pollution2):
    liste=verif_achat(choix,argent2,population2,production2,pollution2)
    prix=str(liste[5])
    population=str(liste[1])
    production=str(liste[2])
    nourriture=str(liste[4])
    affichage_argent=ecriture2.render(prix,False,(255,255,255))
    affichage_population=ecriture2.render(population,False,(255,255,255))
    affichage_production=ecriture2.render(production,False,(255,255,255))
    affichage_nourriture=ecriture2.render(nourriture,False,(255,255,255))
    image_argent2=pygame.image.load("asset_shop/argentpetit.png")
    image_population2=pygame.image.load("asset_shop/villageoispetit.png")
    image_production2=pygame.image.load("asset_shop/productionpetit.png")
    image_nourriture2=pygame.image.load("asset_shop/nourriturepetit.png")
    if choix!=100:
        fenetre.blit(affichage_argent,(1600,880))
        fenetre.blit(affichage_population,(1600,920))
        fenetre.blit(affichage_production,(1600,960))
        fenetre.blit(affichage_nourriture,(1600,1000))
        fenetre.blit(image_argent2,(1560,880))
        fenetre.blit(image_population2,(1560,920))
        fenetre.blit(image_production2,(1560,960))
        fenetre.blit(image_nourriture2,(1560,1000))
    if choix==100:
        pygame.draw.rect(fenetre,[0,0,0],(1560,850,200,200))
        pygame.display.flip()

#affiche les batiments achetable selon l'icone ou on a cliquer puis renvoit la valeur correspondant au batiment chosit
#pour effectuer les verification necessaire
def shop(valeur,argent2,batiment):
    pause=0
    shopachat1=pygame.draw.rect(fenetre,[255,255,255],[0,0,0,0])
    shopachat1_1=pygame.draw.rect(fenetre,[255,255,255],[0,0,0,0])
    shopachat1_2=pygame.draw.rect(fenetre,[255,255,255],[0,0,0,0])
    shopachat1_3=pygame.draw.rect(fenetre,[255,255,255],[0,0,0,0])
    shopachat1_4=pygame.draw.rect(fenetre,[255,255,255],[0,0,0,0])
    shopachat2_1=pygame.draw.rect(fenetre,[255,255,255],[0,0,0,0])
    shopachat2_2=pygame.draw.rect(fenetre,[255,255,255],[0,0,0,0])
    shopachat2_3=pygame.draw.rect(fenetre,[255,255,255],[0,0,0,0])
    shopachat2_4=pygame.draw.rect(fenetre,[255,255,255],[0,0,0,0])
    shopachat3_1=pygame.draw.rect(fenetre,[255,255,255],[0,0,0,0])
    shopachat3_2=pygame.draw.rect(fenetre,[255,255,255],[0,0,0,0])
    shopachat3_3=pygame.draw.rect(fenetre,[255,255,255],[0,0,0,0]) 
    shopachat3_4=pygame.draw.rect(fenetre,[255,255,255],[0,0,0,0])
    shopexit=pygame.draw.rect(fenetre,[255,255,255],[10,500,50,50])
    image_exit=pygame.image.load("asset_shop/exit.png")
    fenetre.blit(image_exit,(10,500))
    while pause==0:
        pygame.display.flip()
        if valeur==1:
            #partie village depart
            if batiment[3]=="0" and batiment[4]=="0":
                shopachat2_1=pygame.draw.rect(fenetre,[0,0,0],[10,800,140,90])
                shopachat2_2=pygame.draw.rect(fenetre,[0,0,0],[200,800,100,90])
                image2_1=pygame.image.load("asset_shop/usinenuc.png")
                image2_2=pygame.image.load("asset_shop/usinelec.png")
                fenetre.blit(image2_1,(0,800))
                fenetre.blit(image2_2,(200,800))
                choix2_1=3
                choix2_2=4
            if batiment[3]=="1" and batiment[5]=="0":
                shopachat2_1=pygame.draw.rect(fenetre,[0,0,0],[10,800,140,90])
                image2_1=pygame.image.load("asset_shop/usinenuc2.png")
                fenetre.blit(image2_1,(0,800))
                choix2_1=5
            if batiment[4]=="1" and batiment[6]=="0":
                shopachat2_1=pygame.draw.rect(fenetre,[0,0,0],[10,800,140,90])
                image2_1=pygame.image.load("asset_shop/usinelec2.png")
                fenetre.blit(image2_1,(0,800))
                choix2_1=6
            if batiment[7]=="0" and batiment[8]=="0":
                shopachat3_1=pygame.draw.rect(fenetre,[0,0,0],[10,680,140,90])
                shopachat3_2=pygame.draw.rect(fenetre,[0,0,0],[200,680,100,90])
                image3_1=pygame.image.load("asset_shop/usinenuc.png")
                image3_2=pygame.image.load("asset_shop/usinelec.png")
                fenetre.blit(image3_1,(0,680))
                fenetre.blit(image3_2,(200,680))
                choix3_1=7
                choix3_2=8
            if batiment[7]=="1" and batiment[9]=="0":
                shopachat3_1=pygame.draw.rect(fenetre,[0,0,0],[10,680,140,90])
                image3_1=pygame.image.load("asset_shop/usinenuc2.png")
                fenetre.blit(image3_1,(0,700))
                choix3_1=9
            if batiment[8]=="1" and batiment[10]=="0":
                shopachat3_1=pygame.draw.rect(fenetre,[0,0,0],[10,680,140,90])
                image3_1=pygame.image.load("asset_shop/usinelec2.png")
                fenetre.blit(image3_1,(0,660))
                choix3_1=10
            if batiment[0]=="0":
                shopachat1=pygame.draw.rect(fenetre,[0,0,0],[10,900,140,90])
                image1=pygame.image.load("asset_shop/ville1.png")
                fenetre.blit(image1,(0,900))
                choix1=0
            if batiment[0]=="1" and batiment[1]=="0":
                shopachat1=pygame.draw.rect(fenetre,[0,0,0],[10,900,140,90])
                image1=pygame.image.load("asset_shop/ville2.png")
                fenetre.blit(image1,(0,900))
                choix1=1
            if batiment[0]=="1" and batiment[1]=="1" and batiment[2]=="0":
                shopachat1=pygame.draw.rect(fenetre,[0,0,0],[10,900,140,90])
                image1=pygame.image.load("asset_shop/ville3.png")
                fenetre.blit(image1,(0,900))
                choix1=2
        #colline bas gauche
        if valeur==3:
            if batiment[11]=="0":
                shopachat1=pygame.draw.rect(fenetre,[0,0,0],[10,900,140,85])
                image1=pygame.image.load("asset_shop/collineplate.png")
                fenetre.blit(image1,(0,900))
                choix1=11
            if batiment[11]=="1":
                if batiment[12]=="0" and batiment[18]=="0":
                    shopachat1_1=pygame.draw.rect(fenetre,[0,0,0],[10,900,60,90])
                    image1_1=pygame.image.load("asset_shop/ferme1.jpg")
                    shopachat1_2=pygame.draw.rect(fenetre,[0,0,0],[100,900,140,90])
                    image1_2=pygame.image.load("asset_shop/arbre.png")
                    fenetre.blit(image1_2,(10,900))
                    fenetre.blit(image1_1,(100,850))
                    choix1_1=18
                    choix1_2=12
                if batiment[12]=="1" and batiment[13]=="0":
                    shopachat1_1=pygame.draw.rect(fenetre,[0,0,0],[10,900,140,90])
                    image1_1=pygame.image.load("asset_shop/ferme2.png")
                    fenetre.blit(image1_1,(0,900))
                    choix1_1=13
                if batiment[14]=="0" and batiment[19]=="0":
                    shopachat2_1=pygame.draw.rect(fenetre,[0,0,0],[10,800,60,90])
                    image2_1=pygame.image.load("asset_shop/ferme1.jpg")
                    shopachat2_2=pygame.draw.rect(fenetre,[0,0,0],[100,800,140,90])
                    image2_2=pygame.image.load("asset_shop/arbre.png")
                    fenetre.blit(image2_2,(10,800))
                    fenetre.blit(image2_1,(100,750))
                    choix2_1=19
                    choix2_2=14
                if batiment[14]=="1" and batiment[15]=="0":
                    shopachat2_1=pygame.draw.rect(fenetre,[0,0,0],[10,800,140,90])
                    image2_1=pygame.image.load("asset_shop/ferme2.png")
                    fenetre.blit(image2_1,(0,800))
                    choix2_1=15
                if batiment[16]=="0" and batiment[20]=="0":
                    shopachat3_1=pygame.draw.rect(fenetre,[0,0,0],[10,700,60,90])
                    image3_1=pygame.image.load("asset_shop/ferme1.jpg")
                    shopachat3_2=pygame.draw.rect(fenetre,[0,0,0],[100,700,140,90])
                    image3_2=pygame.image.load("asset_shop/arbre.png")
                    fenetre.blit(image3_2,(10,700))
                    fenetre.blit(image3_1,(100,650))
                    choix3_1=20
                    choix3_2=16
                if batiment[16]=="1" and batiment[17]=="0":
                    shopachat3_1=pygame.draw.rect(fenetre,[0,0,0],[10,700,140,90])
                    image3_1=pygame.image.load("asset_shop/ferme2.png")
                    fenetre.blit(image3_1,(0,700))
                    choix3_1=17
        #foret haut gauche      
        if valeur==4:
            if batiment[58]=="0":
                shopachat1=pygame.draw.rect(fenetre,[0,0,0],[10,900,140,85])
                image1=pygame.image.load("asset_shop/collineplate.png")
                fenetre.blit(image1,(0,900))
                choix1=58
            if batiment[58]=="1":
                if batiment[21]=="0" and batiment[22]=="0" and batiment[33]=="0" and batiment[36]=="0" and batiment[60]=="0":
                    shopachat3_1=pygame.draw.rect(fenetre,[0,0,0],[0,650,90,90])
                    shopachat3_2=pygame.draw.rect(fenetre,[0,0,0],[100,650,100,90])
                    shopachat3_3=pygame.draw.rect(fenetre,[0,0,0],[210,650,140,90])
                    shopachat3_4=pygame.draw.rect(fenetre,[0,0,0],[360,650,140,90])
                    image3_1=pygame.image.load("asset_shop/eolienne.png")
                    image3_2=pygame.image.load("asset_shop/usinelec.png")
                    image3_3=pygame.image.load("asset_shop/usinenuc.png")
                    image3_4=pygame.image.load("asset_shop/ferme1.jpg")
                    fenetre.blit(image3_1,(0,630))
                    fenetre.blit(image3_2,(100,630))
                    fenetre.blit(image3_3,(210,650))
                    fenetre.blit(image3_4,(360,610))
                    choix3_1=33
                    choix3_2=22
                    choix3_3=21
                    choix3_4=36
                if batiment[60]=="1":
                    shopachat3_1=pygame.draw.rect(fenetre,[0,0,0],[0,650,90,90])
                    image3_1=pygame.image.load("asset_shop/collineplate.png")
                    fenetre.blit(image3_1,(0,630))
                    choix3_1=60
                if batiment[21]=="1" and batiment[23]=="0":
                    shopachat3_1=pygame.draw.rect(fenetre,[0,0,0],[0,650,140,90])
                    image3_1=pygame.image.load("asset_shop/usinenuc2.png")
                    fenetre.blit(image3_1,(0,650))
                    choix3_1=23
                if batiment[22]=="1" and batiment[24]=="0":
                    shopachat3_1=pygame.draw.rect(fenetre,[0,0,0],[0,650,140,90])
                    image3_1=pygame.image.load("asset_shop/usinelec2.png")
                    fenetre.blit(image3_1,(0,650))
                    choix3_1=24
                if batiment[36]=="1" and batiment[37]=="0":
                    shopachat3_1=pygame.draw.rect(fenetre,[0,0,0],[0,650,140,90])
                    image3_1=pygame.image.load("asset_shop/ferme2.png")
                    fenetre.blit(image3_1,(0,650))
                    choix3_1=37
                if batiment[25]=="0" and batiment[26]=="0" and batiment[34]=="0" and batiment[38]=="0":
                    shopachat2_1=pygame.draw.rect(fenetre,[0,0,0],[0,800,90,90])
                    shopachat2_2=pygame.draw.rect(fenetre,[0,0,0],[100,800,100,90])
                    shopachat2_3=pygame.draw.rect(fenetre,[0,0,0],[210,800,140,90])
                    shopachat2_4=pygame.draw.rect(fenetre,[0,0,0],[360,800,140,90])
                    image2_1=pygame.image.load("asset_shop/eolienne.png")
                    image2_2=pygame.image.load("asset_shop/usinelec.png")
                    image2_3=pygame.image.load("asset_shop/usinenuc.png")
                    image2_4=pygame.image.load("asset_shop/ferme1.jpg")
                    fenetre.blit(image2_1,(0,780))
                    fenetre.blit(image2_2,(100,780))
                    fenetre.blit(image2_3,(210,800))
                    fenetre.blit(image2_4,(360,760))
                    choix2_1=34
                    choix2_2=26
                    choix2_3=25
                    choix2_4=38
                if batiment[25]=="1" and batiment[27]=="0":
                    shopachat2_1=pygame.draw.rect(fenetre,[0,0,0],[0,800,140,90])
                    image2_1=pygame.image.load("asset_shop/usinenuc2.png")
                    fenetre.blit(image2_1,(0,800))
                    choix2_1=27
                if batiment[26]=="1" and batiment[28]=="0":
                    shopachat2_1=pygame.draw.rect(fenetre,[0,0,0],[0,800,140,90])
                    image2_1=pygame.image.load("asset_shop/usinelec2.png")
                    fenetre.blit(image2_1,(0,780))
                    choix2_1=28
                if batiment[38]=="1" and batiment[39]=="0":
                    shopachat2_1=pygame.draw.rect(fenetre,[0,0,0],[0,800,140,90])
                    image2_1=pygame.image.load("asset_shop/ferme2.png")
                    fenetre.blit(image2_1,(0,760))
                    choix2_1=39
                if batiment[29]=="0" and batiment[30]=="0" and batiment[35]=="0" and batiment[40]=="0":
                    shopachat1_1=pygame.draw.rect(fenetre,[0,0,0],[0,950,90,90])
                    shopachat1_2=pygame.draw.rect(fenetre,[0,0,0],[100,950,100,90])
                    shopachat1_3=pygame.draw.rect(fenetre,[0,0,0],[210,950,140,90])
                    shopachat1_4=pygame.draw.rect(fenetre,[0,0,0],[360,950,140,90])
                    image1_1=pygame.image.load("asset_shop/eolienne.png")
                    image1_2=pygame.image.load("asset_shop/usinelec.png")
                    image1_3=pygame.image.load("asset_shop/usinenuc.png")
                    image1_4=pygame.image.load("asset_shop/ferme1.jpg")
                    fenetre.blit(image1_1,(0,930))
                    fenetre.blit(image1_2,(100,930))
                    fenetre.blit(image1_3,(210,950))
                    fenetre.blit(image1_4,(360,910))
                    choix1_1=35
                    choix1_2=30
                    choix1_3=29
                    choix1_4=40
                if batiment[29]=="1" and batiment[31]=="0":
                    shopachat1=pygame.draw.rect(fenetre,[0,0,0],[0,950,140,90])
                    image1=pygame.image.load("asset_shop/usinenuc2.png")
                    fenetre.blit(image1,(0,950))
                    choix1=31
                if batiment[30]=="1" and batiment[32]=="0":
                    shopachat1=pygame.draw.rect(fenetre,[0,0,0],[0,950,140,90])
                    image1=pygame.image.load("asset_shop/usinelec2.png")
                    fenetre.blit(image1,(0,920))
                    choix1=32
                if batiment[40]=="1" and batiment[41]=="0":
                    shopachat1=pygame.draw.rect(fenetre,[0,0,0],[0,950,140,90])
                    image1=pygame.image.load("asset_shop/ferme2.png")
                    fenetre.blit(image1,(0,910))
                    choix1=41
        #desert
        if valeur==7:
            if batiment[46]=="0" and batiment[50]=="0":
                shopachat1=pygame.draw.rect(fenetre,[0,0,0],[0,950,140,90])
                shopachat1_1=pygame.draw.rect(fenetre,[0,0,0],[160,950,100,90])
                image1_1=pygame.image.load("asset_shop/petrol.png")
                image1_2=pygame.image.load("asset_shop/usinesol.jpg")
                fenetre.blit(image1_1,(0,950))
                fenetre.blit(image1_2,(160,960))
                choix1=50
                choix1_1=46
            if batiment[44]=="0" and batiment[48]=="0":
                shopachat2_1=pygame.draw.rect(fenetre,[0,0,0],[0,800,140,90])
                shopachat2_2=pygame.draw.rect(fenetre,[0,0,0],[160,800,100,90])
                image2_1=pygame.image.load("asset_shop/petrol.png")
                image2_2=pygame.image.load("asset_shop/usinesol.jpg")
                fenetre.blit(image2_1,(0,800))
                fenetre.blit(image2_2,(150,810))
                choix2_1=48
                choix2_2=44
        #pont
        if valeur==8:
            if batiment[42]=="0" and batiment[43]=="0" and batiment[61]=="0":
                shopachat1=pygame.draw.rect(fenetre,[0,0,0],[0,950,150,100])
                shopachat1_1=pygame.draw.rect(fenetre,[0,0,0],[170,950,110,100])
                image1=pygame.image.load("asset_shop/pont.png")
                image1_1=pygame.image.load("asset_shop/barrage.png")
                fenetre.blit(image1,(0,950))
                fenetre.blit(image1_1,(170,950))
                choix1=42
                choix1_1=43
            if batiment[61]=="1":
                shopachat1=pygame.draw.rect(fenetre,[0,0,0],[0,950,150,100])
                image1=pygame.image.load("asset_shop/collineplate.png")
                fenetre.blit(image1,(0,950))
                choix1=61
        #foret bas droite
        if valeur==5:
            if batiment[52]=="0":
                shopachat1=pygame.draw.rect(fenetre,[0,0,0],[0,950,140,85])
                image1=pygame.image.load("asset_shop/collineplate.png")
                fenetre.blit(image1,(0,950))
                choix1=52
            if batiment[52]=="1" and batiment[53]=="0":
                shopachat1=pygame.draw.rect(fenetre,[0,0,0],[0,950,140,85])
                image1=pygame.image.load("asset_shop/collineplate.png")
                fenetre.blit(image1,(0,950))
                choix1=53
            if batiment[52]=="1" and batiment[53]=="1" and batiment[62]=="0":
                if batiment[54]=="0":
                    shopachat1=pygame.draw.rect(fenetre,[0,0,0],[0,950,140,90])
                    image1=pygame.image.load("asset_shop/ville1.png")
                    fenetre.blit(image1,(0,950))
                    choix1=54
                if batiment[54]=="1" and batiment[55]=="0":
                    shopachat1=pygame.draw.rect(fenetre,[0,0,0],[0,950,140,90])
                    image1=pygame.image.load("asset_shop/ville2.png")
                    fenetre.blit(image1,(0,950))
                    choix1=55
                if batiment[55]=="1" and batiment[56]=="0":
                    shopachat1=pygame.draw.rect(fenetre,[0,0,0],[0,950,140,90])
                    image1=pygame.image.load("asset_shop/ville3.png")
                    fenetre.blit(image1,(0,950))
                    choix1=56
                if batiment[57]=="0":
                    shopachat2_1=pygame.draw.rect(fenetre,[0,0,0],[0,800,90,90])
                    image2_1=pygame.image.load("asset_shop/eolienne.png")
                    fenetre.blit(image2_1,(0,800))
                    choix2_1=57
            if batiment[62]=="1":
                shopachat1=pygame.draw.rect(fenetre,[0,0,0],[0,950,140,90])
                image1=pygame.image.load("asset_shop/collineplate.png")
                fenetre.blit(image1,(0,950))
                choix1=62
        #mer village depart
        if valeur==9:
            if batiment[63]=="0":
                shopachat1_1=pygame.draw.rect(fenetre,[0,0,0],[0,750,90,90])
                image1_1=pygame.image.load("asset_shop/eolienne.png")
                fenetre.blit(image1_1,(0,750))
                choix1_1=63
            if batiment[64]=="0":
                shopachat2_1=pygame.draw.rect(fenetre,[0,0,0],[0,900,140,90])
                image2_1=pygame.image.load("asset_shop/houle.png")
                fenetre.blit(image2_1,(0,900))
                choix2_1=64
            if batiment[65]=="0" and batiment[66]=="0" and batiment[67]=="0":
                shopachat3_1=pygame.draw.rect(fenetre,[0,0,0],[0,950,90,90])
                shopachat3_2=pygame.draw.rect(fenetre,[0,0,0],[160,950,90,90])
                shopachat3_3=pygame.draw.rect(fenetre,[0,0,0],[330,950,90,90])
                image3_1=pygame.image.load("asset_shop/peche.png")
                image3_2=pygame.image.load("asset_shop/petrolemer.png")
                image3_3=pygame.image.load("asset_shop/hydrolienne.png")
                fenetre.blit(image3_1,(0,950))
                fenetre.blit(image3_2,(160,950))
                fenetre.blit(image3_3,(330,950))
                choix3_1=66
                choix3_2=67
                choix3_3=65
        #mer village second
        if valeur==10:
            if batiment[68]=="0":
                shopachat1_1=pygame.draw.rect(fenetre,[0,0,0],[0,800,90,90])
                image1_1=pygame.image.load("asset_shop/houle.png")
                fenetre.blit(image1_1,(0,800))
                choix1_1=68
            if batiment[69]=="0" and batiment[70]=="0" and batiment[71]=="0":
                shopachat3_1=pygame.draw.rect(fenetre,[0,0,0],[0,900,90,90])
                shopachat3_2=pygame.draw.rect(fenetre,[0,0,0],[160,900,90,90])
                shopachat3_3=pygame.draw.rect(fenetre,[0,0,0],[330,900,90,90])
                image3_1=pygame.image.load("asset_shop/peche.png")
                image3_2=pygame.image.load("asset_shop/petrolemer.png")
                image3_3=pygame.image.load("asset_shop/hydrolienne.png")
                fenetre.blit(image3_1,(0,900))
                fenetre.blit(image3_2,(160,900))
                fenetre.blit(image3_3,(330,900))
                choix3_1=70
                choix3_2=71
                choix3_3=69
        for event in pygame.event.get():
            if event.type==MOUSEBUTTONDOWN:
                if shopachat1.collidepoint(event.pos):
                    choix=choix1
                    pause=1
                if shopachat1_1.collidepoint(event.pos):
                    choix=choix1_1
                    pause=1
                if shopachat1_2.collidepoint(event.pos):
                    choix=choix1_2
                    pause=1
                if shopachat1_3.collidepoint(event.pos):
                    choix=choix1_3
                    pause=1
                if shopachat1_4.collidepoint(event.pos):
                    choix=choix1_4
                    pause=1
                if shopachat2_1.collidepoint(event.pos):
                    choix=choix2_1
                    pause=1
                if shopachat2_2.collidepoint(event.pos):
                    choix=choix2_2
                    pause=1
                if shopachat2_3.collidepoint(event.pos):
                    choix=choix2_3
                    pause=1
                if shopachat2_4.collidepoint(event.pos):
                    choix=choix2_4
                    pause=1
                if shopachat3_1.collidepoint(event.pos):
                    choix=choix3_1
                    pause=1
                if shopachat3_2.collidepoint(event.pos):
                    choix=choix3_2
                    pause=1
                if shopachat3_3.collidepoint(event.pos):
                    choix=choix3_3
                    pause=1
                if shopachat3_4.collidepoint(event.pos):
                    choix=choix3_4
                    pause=1
                if shopexit.collidepoint(event.pos):
                    choix=rien
                    pause=1
            if event.type==MOUSEMOTION:
                choix=rien
                if shopachat1.collidepoint(event.pos):
                    choix=choix1
                if shopachat1_1.collidepoint(event.pos):
                    choix=choix1_1
                if shopachat1_2.collidepoint(event.pos):
                    choix=choix1_2
                if shopachat1_3.collidepoint(event.pos):
                    choix=choix1_3
                if shopachat1_4.collidepoint(event.pos):
                    choix=choix1_4
                if shopachat2_1.collidepoint(event.pos):
                    choix=choix2_1
                if shopachat2_2.collidepoint(event.pos):
                    choix=choix2_2
                if shopachat2_3.collidepoint(event.pos):
                    choix=choix2_3
                if shopachat2_4.collidepoint(event.pos):
                    choix=choix2_4
                if shopachat3_1.collidepoint(event.pos):
                    choix=choix3_1
                if shopachat3_2.collidepoint(event.pos):
                    choix=choix3_2
                if shopachat3_3.collidepoint(event.pos):
                    choix=choix3_3
                if shopachat3_4.collidepoint(event.pos):
                    choix=choix3_4
                affichage_prix(choix,batiment,argent2,population2,production2,pollution2)
                pygame.display.flip()
    #ensuite argent=argent-choix       
    return(choix)

#permet d'enlever du main l'affichage qui n'a pas besoin d'etre utiliser pour d'autre fonction
def affichage_jeux(batiment,pollution2):
    if pollution2<800:
        maps1=pygame.image.load("mapsM/mapseau1.png")  
        fenetre.blit(maps1,(0,0))
    if pollution2>=800:
        maps1=pygame.image.load("mapsM/mapseau2.png")
        fenetre.blit(maps1,(0,0))
    #mer gauche
    if batiment[64]=="1":
        mapscolline=pygame.image.load("mapsM/mer1/houle.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[65]=="1":
        mapscolline=pygame.image.load("mapsM/mer1/hydrolienne.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[66]=="1":
        mapscolline=pygame.image.load("mapsM/mer1/peche.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[67]=="1":
        mapscolline=pygame.image.load("mapsM/mer1/petrole.png")
        fenetre.blit(mapscolline,(0,0))
    #mer droite
    if batiment[68]=="1":
        mapscolline=pygame.image.load("mapsM/mer2/houle.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[69]=="1":
        mapscolline=pygame.image.load("mapsM/mer2/hydrolienne.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[70]=="1":
        mapscolline=pygame.image.load("mapsM/mer2/peche.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[71]=="1":
        mapscolline=pygame.image.load("mapsM/mer2/petrole.png")
        fenetre.blit(mapscolline,(0,0))
    #foret gauche
    if batiment[58]=="0":
        maps6=pygame.image.load("mapsM/foretgauche/mapsforetgauchehaut1.png")  
        fenetre.blit(maps6,(0,0))
    if batiment[58]=="1" and batiment[60]=="0":
        mapscolline=pygame.image.load("mapsM/foretgauche/foretplate.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[60]=="1":
        mapscolline=pygame.image.load("mapsM/foretgauche/innondation.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[21]=="1" and batiment[23]=="0":
        mapscolline=pygame.image.load("mapsM/foretgauche/usinenuchaut.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[22]=="1" and batiment[24]=="0":
        mapscolline=pygame.image.load("mapsM/foretgauche/usinelechaut.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[23]=="1":
        mapscolline=pygame.image.load("mapsM/foretgauche/usinenuc2haut.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[24]=="1":
        mapscolline=pygame.image.load("mapsM/foretgauche/usinelec2haut.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[25]=="1" and batiment[27]=="0":
        mapscolline=pygame.image.load("mapsM/foretgauche/usinenucmillieu.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[26]=="1" and batiment[28]=="0":
        mapscolline=pygame.image.load("mapsM/foretgauche/usinelecmillieu.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[27]=="1":
        mapscolline=pygame.image.load("mapsM/foretgauche/usinenuc2millieu.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[28]=="1":
        mapscolline=pygame.image.load("mapsM/foretgauche/usinelec2millieu.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[29]=="1" and batiment[31]=="0":
        mapscolline=pygame.image.load("mapsM/foretgauche/usinenucbas.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[30]=="1" and batiment[32]=="0":
        mapscolline=pygame.image.load("mapsM/foretgauche/usinelecbas.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[31]=="1":
        mapscolline=pygame.image.load("mapsM/foretgauche/usinenuc2bas.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[32]=="1":
        mapscolline=pygame.image.load("mapsM/foretgauche/usinelec2bas.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[33]=="1":
        mapscolline=pygame.image.load("mapsM/foretgauche/eoliennehaut.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[34]=="1":
        mapscolline=pygame.image.load("mapsM/foretgauche/eoliennemillieu.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[35]=="1":
        mapscolline=pygame.image.load("mapsM/foretgauche/eoliennebas.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[36]=="1" and batiment[37]=="0":
        mapscolline=pygame.image.load("mapsM/foretgauche/fermehaut.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[37]=="1":
        mapscolline=pygame.image.load("mapsM/foretgauche/ferme2haut.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[38]=="1" and batiment[39]=="0":
        mapscolline=pygame.image.load("mapsM/foretgauche/fermemillieu.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[39]=="1":
        mapscolline=pygame.image.load("mapsM/foretgauche/ferme2millieu.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[40]=="1" and batiment[41]=="0":
        mapscolline=pygame.image.load("mapsM/foretgauche/fermebas.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[41]=="1":
        mapscolline=pygame.image.load("mapsM/foretgauche/ferme2bas.png")
        fenetre.blit(mapscolline,(0,0))
    #desert
    maps4=pygame.image.load("mapsM/mapssable1.png")  
    fenetre.blit(maps4,(0,0))
    if batiment[44]=="1":
        mapscolline=pygame.image.load("mapsM/desert/usinesolgauche.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[46]=="1":
        mapscolline=pygame.image.load("mapsM/desert/usinesoldroite.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[48]=="1":
        mapscolline=pygame.image.load("mapsM/desert/usinepetrolegauche.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[50]=="1":
        mapscolline=pygame.image.load("mapsM/desert/usinepetroledroite.png")
        fenetre.blit(mapscolline,(0,0))
    #foret bas
    if batiment[52]=="0" and batiment[62]=="0":
        maps5=pygame.image.load("mapsM/mapscolline+arbre1.png")  
        fenetre.blit(maps5,(0,0))
    if batiment[52]=="0" and batiment[62]=="1":
        maps5=pygame.image.load("mapsM/foretbas/innondation.png")  
        fenetre.blit(maps5,(0,0))
    if batiment[52]=="1" and batiment[62]=="0":
        mapscolline=pygame.image.load("mapsM/foretbas/foretplate.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[52]=="1" and batiment[53]=="0" and batiment[62]=="1":
        mapscolline=pygame.image.load("mapsM/foretbas/innondation2.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[53]=="1" and batiment[62]=="0":
        mapscolline=pygame.image.load("mapsM/foretbas/collineplate.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[53]=="1" and batiment[62]=="1":
        mapscolline=pygame.image.load("mapsM/foretbas/innondation3.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[54]=="1":
        mapscolline=pygame.image.load("mapsM/foretbas/ville.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[55]=="1":
        mapscolline=pygame.image.load("mapsM/foretbas/ville2.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[56]=="1":
        mapscolline=pygame.image.load("mapsM/foretbas/ville3.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[57]=="1":
        mapscolline=pygame.image.load("mapsM/foretbas/eolienne.png")
        fenetre.blit(mapscolline,(0,0))
    #colline bas gauche
    if batiment[11]=="0":
        maps8=pygame.image.load("mapsM/mapscoline1.png")  
        fenetre.blit(maps8,(0,0))
    if batiment[11]=="1":
        mapscolline=pygame.image.load("mapsM/collineV/collineplate.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[18]=="1":
        mapscolline=pygame.image.load("mapsM/collineV/foretbas.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[19]=="1":
        mapscolline=pygame.image.load("mapsM/collineV/foretmillieu.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[20]=="1":
        mapscolline=pygame.image.load("mapsM/collineV/forethaut.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[12]=="1" and batiment[13]=="0":
        mapscolline=pygame.image.load("mapsM/collineV/fermebas.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[14]=="1" and batiment[15]=="0":
        mapscolline=pygame.image.load("mapsM/collineV/fermemillieu.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[16]=="1" and batiment[17]=="0":
        mapscolline=pygame.image.load("mapsM/collineV/fermehaut.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[13]=="1":
        mapscolline=pygame.image.load("mapsM/collineV/ferme2bas.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[15]=="1":
        mapscolline=pygame.image.load("mapsM/collineV/ferme2millieu.png")
        fenetre.blit(mapscolline,(0,0))
    if batiment[17]=="1":
        mapscolline=pygame.image.load("mapsM/collineV/ferme2haut.png")
        fenetre.blit(mapscolline,(0,0))
    #pont
    if batiment[61]=="0":
        maps2=pygame.image.load("mapsM/mapsponnt1.png")  
        fenetre.blit(maps2,(0,0))
    if batiment[61]=="1":
        maps2=pygame.image.load("mapsM/pont/innondation.png")  
        fenetre.blit(maps2,(0,0))
    if batiment[42]=="1":
        mapsville=pygame.image.load("mapsM/pont/pont.png")
        fenetre.blit(mapsville,(0,0))
    if batiment[43]=="1":
        mapsville=pygame.image.load("mapsM/pont/barrage.png")
        fenetre.blit(mapsville,(0,0))
    #village
    if batiment[59]=="0":
        maps3=pygame.image.load("mapsM/village/mapsmaison1.png")  
        fenetre.blit(maps3,(0,0))
    if batiment[59]=="1":
        maps3=pygame.image.load("mapsM/village/innondation.png")  
        fenetre.blit(maps3,(0,0))
    if batiment[0]=="1" and batiment[1]=="0":
        mapsville=pygame.image.load("mapsM/village/village1.png")
        fenetre.blit(mapsville,(0,0))
    if batiment[0]=="1" and batiment[1]=="1" and batiment[2]=="0":
        mapsville=pygame.image.load("mapsM/village/village2.png")
        fenetre.blit(mapsville,(0,0))
    if batiment[0]=="1" and batiment[1]=="1" and batiment[2]=="1":
        mapsville=pygame.image.load("mapsM/village/village3.png")
        fenetre.blit(mapsville,(0,0))
    if batiment[3]=="1" and batiment[5]=="0":
        mapsville=pygame.image.load("mapsM/village/usinenuc1gauche.png")
        fenetre.blit(mapsville,(0,0))
    if batiment[3]=="1" and batiment[5]=="1":
        mapsville=pygame.image.load("mapsM/village/usinenuc2gauche.png")
        fenetre.blit(mapsville,(0,0))
    if batiment[4]=="1" and batiment[6]=="0":
        mapsville=pygame.image.load("mapsM/village/usinelec1gauche.png")
        fenetre.blit(mapsville,(0,0))
    if batiment[4]=="1" and batiment[6]=="1":
        mapsville=pygame.image.load("mapsM/village/usinelec2gauche.png")
        fenetre.blit(mapsville,(0,0)) 
    if batiment[7]=="1" and batiment[9]=="0":
        mapsville=pygame.image.load("mapsM/village/usinenuc1droite.png")
        fenetre.blit(mapsville,(0,0))
    if batiment[7]=="1" and batiment[9]=="1":
        mapsville=pygame.image.load("mapsM/village/usinenuc2droite.png")
        fenetre.blit(mapsville,(0,0))
    if batiment[8]=="1" and batiment[10]=="0":
        mapsville=pygame.image.load("mapsM/village/usinelec1droite.png")
        fenetre.blit(mapsville,(0,0))
    if batiment[8]=="1" and batiment[10]=="1":
        mapsville=pygame.image.load("mapsM/village/usinelec2droite.png")
        fenetre.blit(mapsville,(0,0))
    #foret haut droite
    if batiment[60]=="0":
        maps7=pygame.image.load("mapsM/mapsforet haut droite1.png")  
        fenetre.blit(maps7,(0,0))
    if batiment[60]=="1":
        maps7=pygame.image.load("mapsM/innondation.png")  
        fenetre.blit(maps7,(0,0))
    #eviter colision
    if batiment[63]=="1":
        mapscolline=pygame.image.load("mapsM/mer1/eolienne.png")
        fenetre.blit(mapscolline,(0,0))

#fonction pour le multi-thread on prend x le temps necessaire a l'apparition des icones
#et y la queue dans laquelle on retourne le resultat elle s'effectue en parallele du
#programme principal
def timertemps(x,y):
    temps=x
    for i in range(x):
        temps=temps-1
        time.sleep(1)
    if y==1:
        q1.put(temps)
    if y==2:
        q2.put(temps)
    if y==3:
        q3.put(temps)
    if y==4:
        q4.put(temps)
    if y==5:
        q5.put(temps)
    if y==6:
        q6.put(temps)
    if y==7:
        q7.put(temps)
    if y==8:
        q8.put(temps)
    if y==9:
        q9.put(temps)
    if y==10:
        q10.put(temps)
    if y==11:
        q11.put(temps)
    if y==12:
        q12.put(temps)
    if y==13:
        q13.put(temps)
    if y==14:
        q14.put(temps)
    if y==15:
        q15.put(temps)
    if y==16:
        q16.put(temps)
    if y==17:
        q17.put(temps)
    if y==18:
        q18.put(temps)
    if y==19:
        q19.put(temps)
    if y==20:
        q20.put(temps)
    if y==21:
        q21.put(temps)
    if y==22:
        q22.put(temps)
    if y==23:
        q23.put(temps)

def ajoutpollution(batiment):
    pollution3=0
    #premier village
    if batiment[0]=="1" or batiment[54]=="1":
        pollution3=pollution3+50
    #deuxieme village
    if batiment[1]=="1" or batiment[55]=="1":
        pollution3=pollution3+50
    #troisieme village
    if batiment[2]=="1" or batiment[56]=="1":
        pollution3=pollution3+100
    #premiere usine nucleaire
    if batiment[3]=="1" or batiment[7]=="1" or batiment[21]=="1" or batiment[25]=="1" or batiment[29]=="1":
        pollution3=pollution3+75
    #premiere usine electrique
    if batiment[4]=="1" or batiment[8]=="1" or batiment[22]=="1" or batiment[26]=="1" or batiment[30]=="1":
        pollution3=pollution3+25
    #deuxieme usine nucleaire
    if batiment[5]=="1" or batiment[9]=="1" or batiment[23]=="1" or batiment[27]=="1" or batiment[31]=="1":
        pollution3=pollution3+125
    #deuxieme usine electrique
    if batiment[6]=="1" or batiment[10]=="1" or batiment[24]=="1" or batiment[28]=="1" or batiment[32]=="1":
        pollution3=pollution3+75
    #barrage
    if batiment[43]=="1":
        pollution3=pollution3+200
    #premiere usine petrole
    if batiment[48]=="1" or batiment[50]=="1":
        pollution3=pollution3+150
    #deuxieme usine petrole
    if batiment[49]=="1" or batiment[51]=="1":
        pollution3=pollution3+150
    #petrole mer
    if batiment[67]=="1" or batiment[71]=="1":
        pollution3=pollution3+150
    return(pollution3)


clock=pygame.time.Clock()
#nom de la fenetre de jeux
pygame.display.set_caption("jeux tipe")
#police et taille d'ecriture du texte
ecriture=pygame.font.SysFont("Helvetic",70)
ecriture2=pygame.font.SysFont("Helvetic",40)
#taille de l'ecran (fenetre est comme une feuille ou on colle ce qu'on veut afficher)
fenetre=pygame.display.set_mode((800,600))
image=pygame.image.load("fondecran2.jpg")
#adapte l'image a la taille de l'ecran
image=pygame.transform.scale(image,(800,600))
charger=0
#initialisation de la musique
pygame.mixer.init()
pygame.mixer.music.load("asset_final/musique.mp3")
pygame.mixer.music.set_volume(0.01)
pygame.mixer.music.play(-1)
inrun=True
gamerun=False
while inrun==True:
#afficher le fond d'ecran
    fenetre.blit(image, (0,0))
#ecriture est le texte et bouton est un rectangle entourant le texte
#pour le bouton jouer
    bouton_jouer=pygame.draw.rect(fenetre,[250,250,250],[60,160,110,60])
    image_play=pygame.image.load("asset_shop/boutonplay.png")
    fenetre.blit(image_play,(40,150))
#pour le bouton options
    bouton_charger=pygame.draw.rect(fenetre,[250,250,250],[60,260,110,60])
    image_save=pygame.image.load("asset_shop/boutonsave.png")
    fenetre.blit(image_save,(40,250))
#pour le bouton quitter
    bouton_quitter=pygame.draw.rect(fenetre,[250,250,250],[60,360,110,60])
    image_exit=pygame.image.load("asset_shop/boutonexit.png")
    fenetre.blit(image_exit,(40,350))
    pygame.display.flip()
#permet de fermer le programe avec la fermeture de la fenetre
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            inrun=False
            pygame.quit()
#si on clique avec la souris sur quitter
        if event.type==MOUSEBUTTONDOWN:
            if bouton_quitter.collidepoint(event.pos):
                inrun=False
#si on clique avec la souris sur jouer
        if event.type==MOUSEBUTTONDOWN:
            if bouton_jouer.collidepoint(event.pos):
                gamerun=True
                inrun=False
                charger=0
        if event.type==MOUSEBUTTONDOWN:
            if bouton_charger.collidepoint(event.pos):
                gamerun=True
                inrun=False
                if os.path.getsize("sauvegarde/sauvegarde.txt")!=0:
                    charger=1
                else:
                    charger=0


batiment=[]
debloqueconstru=0
population2=0
production2=0
argent2=1000
pollution2=0
nourriture2=0
batiment=listebatiment(charger,batiment,population2,production2,pollution2,nourriture2,argent2)
if charger==1:
    argent2=int(batiment[72])
    population2=int(batiment[73])
    production2=int(batiment[74])
    pollution2=int(batiment[75])
    nourriture2=int(batiment[76])
stop=False
point=": "
population=point+str(population2)
production=point+str(production2)
argent=point+str(argent2)
pollution=point+str(pollution2)
nourriture=point+str(nourriture2)
#variable pour le multi-thread
ajout=conditionpollution=stop1=stop2=stop3=stop4=stop5=stop6=stop7=stop8=stop9=stop10=stop11=stop12=stop13=stop14=stop15=stop16=stop17=stop18=stop19=stop20=stop21=stop22=stop23=stop24=stop25=0
timer1=timer2=timer3=timer4=timer5=timer6=timer7=timer8=timer9=timer10=timer11=timer12=timer13=timer14=timer15=timer16=timer17=timer18=timer19=timer20=timer21=timer22=timer23=10
#rien pris
rien=100
while gamerun==True:
    fenetre=pygame.display.set_mode((0,0))
    affichage_jeux(batiment,pollution2)
    #bouton pour declancher le shop
    bouton_maison=pygame.draw.rect(fenetre,(255,255,255),(409,609,30,35))
    bouton_eau=pygame.draw.rect(fenetre,(255,255,255),(50,50,10,10))
    bouton_colline=pygame.draw.rect(fenetre,(255,255,255),(189,609,30,35))
    bouton_foretgauche=pygame.draw.rect(fenetre,(255,255,255),(579,359,30,35))
    bouton_forethaut=pygame.draw.rect(fenetre,(255,255,255),(50,50,10,10))
    bouton_pont=pygame.draw.rect(fenetre,(255,255,255),(1009,409,30,35))
    bouton_sauvegarde=pygame.draw.rect(fenetre,(0,0,0),(1770,900,130,80))
    bouton_mergauche=pygame.draw.rect(fenetre,(250,250,250),(569,809,30,35))
    bouton_exit=pygame.draw.rect(fenetre,(0,0,0),(1770,1000,130,80))
    if debloqueconstru==0:
        bouton_merdroite=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
        bouton_desert=pygame.draw.rect(fenetre,(255,255,255),(0,0,0,0))
        bouton_foretbas=pygame.draw.rect(fenetre,(255,255,255),(0,0,0,0))
    if debloqueconstru==1:
        bouton_merdroite=pygame.draw.rect(fenetre,(250,250,250),(1279,809,30,35))
        bouton_desert=pygame.draw.rect(fenetre,(255,255,255),(1709,559,30,35))
        bouton_foretbas=pygame.draw.rect(fenetre,(255,255,255),(1339,739,30,35))
    #enleve les icones de recolte si le timer n'est pas terminer
    if timer1!=0:
        bouton_argent1=pygame.draw.rect(fenetre,(0,0,0),(0,0,0,0))
    if timer2!=0:
        bouton_argent2=pygame.draw.rect(fenetre,(0,0,0),(0,0,0,0))
    if timer3!=0:
        bouton_production1=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    if timer4!=0:
        bouton_production2=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    if timer5!=0:
        bouton_colline1=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    if timer6!=0:
        bouton_colline2=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    if timer7!=0:
        bouton_colline3=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    if timer8!=0:
        bouton_foretgauche1=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    if timer9!=0:
        bouton_foretgauche2=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    if timer10!=0:
        bouton_foretgauche3=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    if timer11!=0:
        bouton_barrage=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    if timer12!=0:
        bouton_eolienne=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    if timer13!=0:
        bouton_desertgauche=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    if timer14!=0:
        bouton_desertdroite=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    if timer15!=0:
        bouton_foret1=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    if timer16!=0:
        bouton_foret2=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    if timer17!=0:
        bouton_foret3=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    if timer18!=0:
        bouton_mer1=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    if timer19!=0:
        bouton_mer2=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    if timer20!=0:
        bouton_mer3=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    if timer21!=0:
        bouton_mer4=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    if timer22!=0:
        bouton_mer5=pygame.draw.rect(fenetre,(250,250,250),(0,0,0,0))
    image_construire=pygame.image.load("asset_shop/shop.png")
    fenetre.blit(image_construire,(400,600))
    fenetre.blit(image_construire,(180,600))
    fenetre.blit(image_construire,(570,350))
    fenetre.blit(image_construire,(1000,400))
    fenetre.blit(image_construire,(560,800))
    if debloqueconstru==1:
        fenetre.blit(image_construire,(1270,800))
        fenetre.blit(image_construire,(1700,550))
        fenetre.blit(image_construire,(1330,730))
    ecriture_argent=ecriture.render(argent,False,(255,255,255))
    ecriture_production=ecriture.render(production,False,(255,255,255))
    ecriture_population=ecriture.render(population,False,(255,255,255))
    ecriture_pollution=ecriture.render(pollution,False,(255,255,255))
    ecriture_pollution1=ecriture2.render("Terre polluer : nourriture -25%",False,(255,255,255))
    ecriture_pollution2=ecriture2.render("eau polluer : nourriture -25%",False,(255,255,255))
    ecriture_pollution3=ecriture2.render("innondation : destruction construction",False,(255,255,255))
    ecriture_nourriture=ecriture.render(nourriture,False,(255,255,255))
    fenetre.blit(ecriture_argent,(100,20))
    fenetre.blit(ecriture_population,(100,80))
    fenetre.blit(ecriture_production,(100,140))
    fenetre.blit(ecriture_pollution,(100,210))
    fenetre.blit(ecriture_nourriture,(100,270))
    fenetre.blit(image_save,(1760,900))
    fenetre.blit(image_exit,(1760,1000))
    if pollution2>=400:
        fenetre.blit(ecriture_pollution1,(1500,10))
    if pollution2>=800:
        fenetre.blit(ecriture_pollution2,(1500,40))
    if batiment[59]=="1" or batiment[60]=="1" or batiment[61]=="1" or batiment[62]=="1":
        fenetre.blit(ecriture_pollution3,(1470,70))
    image_argent=pygame.image.load("asset_final/argent2.png")
    image_population=pygame.image.load("asset_shop/villageois1.jpg")
    image_production=pygame.image.load("asset_final/production2.jpg")
    image_pollution=pygame.image.load("asset_shop/terre.png")
    image_nourriture=pygame.image.load("asset_shop/nourriture.png")
    image_argent2=pygame.image.load("asset_shop/argentpetit2.png")
    image_population2=pygame.image.load("asset_shop/villageoispetit.png")
    image_production2=pygame.image.load("asset_shop/productionpetit.png")
    image_nourriture2=pygame.image.load("asset_shop/nourriturepetit.png")
    image_pollution2=pygame.image.load("asset_shop/terrepetit.png")
    fenetre.blit(image_argent,(10,25))
    fenetre.blit(image_population,(10,75))
    fenetre.blit(image_production,(10,125))
    fenetre.blit(image_pollution,(0,185))
    fenetre.blit(image_nourriture,(10,270))
    if pollution2<0:
        pollution2=0
        pollution=point+str(pollution2)
    pygame.display.flip()
    #ville depart
    if batiment[0]=="1" or batiment[1]=="1" or batiment[2]=="1":
        if stop3==0:
            timer1=10
            q1=queue.Queue()
            t1=threading.Thread(target=timertemps,args=(10,1,))
            t1.start()
            stop3=1
        if q1.empty()==False:
            timer1=q1.get(block=False,timeout=None)
        if timer1==0:
            bouton_argent1=pygame.draw.rect(fenetre,(250,250,250),(650,515,30,35))
            fenetre.blit(image_argent2,(650,515))
            pygame.display.flip()
    #seconde ville
    if batiment[52]=="0":
        if stop18==0:
            timer16=10
            q16=queue.Queue()
            t16=threading.Thread(target=timertemps,args=(10,16,))
            t16.start()
            stop18=1
        if q16.empty()==False:
            timer16=q16.get(block=False,timeout=None)
        if timer16==0:
            bouton_foret2=pygame.draw.rect(fenetre,(250,250,250),(1500,700,30,30))
            fenetre.blit(image_pollution2,(1500,700))
            pygame.display.flip()
    if batiment[54]=="1" or batiment[55]=="1" or batiment[56]=="1":
        if stop4==0:
            timer2=10
            q2=queue.Queue()
            t2=threading.Thread(target=timertemps,args=(10,2,))
            t2.start()
            stop4=1
        if q2.empty()==False:
            timer2=q2.get(block=False,timeout=None)
        if timer2==0:
            bouton_argent2=pygame.draw.rect(fenetre,(250,250,250),(1250,420,30,35))
            fenetre.blit(image_argent2,(1250,420))
            pygame.display.flip()
    #usine zone depart
    if batiment[3]=="1" or batiment[4]=="1" or batiment[5]=="1" or batiment[6]=="1":
        if stop5==0:
            timer3=10
            q3=queue.Queue()
            t3=threading.Thread(target=timertemps,args=(10,3,))
            t3.start()
            stop5=1
        if q3.empty()==False:
            timer3=q3.get(block=False,timeout=None)
        if timer3==0:
            bouton_production1=pygame.draw.rect(fenetre,(250,250,250),(710,400,30,35))
            fenetre.blit(image_production2,(710,400))
            pygame.display.flip()
    if batiment[7]=="1" or batiment[8]=="1" or batiment[9]=="1" or batiment[10]=="1":
        if stop6==0:
            timer4=10
            q4=queue.Queue()
            t4=threading.Thread(target=timertemps,args=(10,4,))
            t4.start()
            stop6=1
        if q4.empty()==False:
            timer4=q4.get(block=False,timeout=None)
        if timer4==0:
            bouton_production2=pygame.draw.rect(fenetre,(250,250,250),(840,460,30,35))
            fenetre.blit(image_production2,(840,460))
            pygame.display.flip()
    #zone colline
    if batiment[12]=="1" or batiment[13]=="1" or batiment[18]=="1":
        if stop7==0:
            timer5=10
            q5=queue.Queue()
            t5=threading.Thread(target=timertemps,args=(10,5,))
            t5.start()
            stop7=1
        if q5.empty()==False:
            timer5=q5.get(block=False,timeout=None)
        if timer5==0:
            bouton_colline1=pygame.draw.rect(fenetre,(250,250,250),(70,370,30,35))
            if batiment[12]=="1" or batiment[13]=="1":
                fenetre.blit(image_nourriture2,(70,370))
            if batiment[18]=="1":
                fenetre.blit(image_pollution2,(70,370))
            pygame.display.flip()
    if batiment[14]=="1" or batiment[15]=="1" or batiment[19]=="1":
        if stop8==0:
            timer6=10
            q6=queue.Queue()
            t6=threading.Thread(target=timertemps,args=(10,6,))
            t6.start()
            stop8=1
        if q6.empty()==False:
            timer6=q6.get(block=False,timeout=None)
        if timer6==0:
            bouton_colline2=pygame.draw.rect(fenetre,(250,250,250),(250,270,30,35))
            if batiment[14]=="1" or batiment[15]=="1":
                fenetre.blit(image_nourriture2,(250,270))
            if batiment[19]=="1":
                fenetre.blit(image_pollution2,(250,270))
            pygame.display.flip()
    if batiment[16]=="1" or batiment[17]=="1" or batiment[20]=="1":
        if stop9==0:
            timer7=10
            q7=queue.Queue()
            t7=threading.Thread(target=timertemps,args=(10,7,))
            t7.start()
            stop9=1
        if q7.empty()==False:
            timer7=q7.get(block=False,timeout=None)
        if timer7==0:
            bouton_colline3=pygame.draw.rect(fenetre,(250,250,250),(330,220,30,35))
            if batiment[16]=="1" or batiment[17]=="1":
                fenetre.blit(image_nourriture2,(330,220))
            if batiment[20]=="1":
                fenetre.blit(image_pollution2,(330,220))
            pygame.display.flip()
    #zone foret gauche
    if batiment[58]=="0":
        if stop17==0:
            timer15=10
            q15=queue.Queue()
            t15=threading.Thread(target=timertemps,args=(10,15,))
            t15.start()
            stop17=1
        if q15.empty()==False:
            timer15=q15.get(block=False,timeout=None)
        if timer15==0:
            bouton_foret1=pygame.draw.rect(fenetre,(250,250,250),(520,110,30,30))
            fenetre.blit(image_pollution2,(520,110))
            pygame.display.flip()
    if batiment[29]=="1" or batiment[30]=="1" or batiment[31]=="1" or batiment[32]=="1" or batiment[40]=="1" or batiment[41]=="1" or batiment[35]=="1":
        if stop10==0:
            timer8=10
            q8=queue.Queue()
            t8=threading.Thread(target=timertemps,args=(10,8,))
            t8.start()
            stop10=1
        if q8.empty()==False:
            timer8=q8.get(block=False,timeout=None)
        if timer8==0:
            bouton_foretgauche3=pygame.draw.rect(fenetre,(250,250,250),(400,180,30,35))
            if batiment[29]=="1" or batiment[30]=="1" or batiment[31]=="1" or batiment[32]=="1" or batiment[35]=="1":
                fenetre.blit(image_production2,(400,180))
            if batiment[40]=="1" or batiment[41]=="1":
                fenetre.blit(image_nourriture2,(400,180))
            pygame.display.flip()
    if batiment[25]=="1" or batiment[26]=="1" or batiment[27]=="1" or batiment[28]=="1" or batiment[38]=="1" or batiment[39]=="1" or batiment[34]=="1":
        if stop11==0:
            timer9=10
            q9=queue.Queue()
            t9=threading.Thread(target=timertemps,args=(10,9,))
            t9.start()
            stop11=1
        if q9.empty()==False:
            timer9=q9.get(block=False,timeout=None)
        if timer9==0:
            bouton_foretgauche2=pygame.draw.rect(fenetre,(250,250,250),(500,140,30,35))
            if batiment[25]=="1" or batiment[26]=="1" or batiment[27]=="1" or batiment[28]=="1" or batiment[34]=="1":
                fenetre.blit(image_production2,(500,140))
            if batiment[38]=="1" or batiment[39]=="1":
                fenetre.blit(image_nourriture2,(500,140))
            pygame.display.flip()
    if batiment[21]=="1" or batiment[22]=="1" or batiment[23]=="1" or batiment[24]=="1" or batiment[36]=="1" or batiment[37]=="1" or batiment[33]=="1":
        if stop12==0:
            timer10=10
            q10=queue.Queue()
            t10=threading.Thread(target=timertemps,args=(10,10,))
            t10.start()
            stop12=1
        if q10.empty()==False:
            timer10=q10.get(block=False,timeout=None)
        if timer10==0:
            bouton_foretgauche1=pygame.draw.rect(fenetre,(250,250,250),(620,100,30,35))
            if batiment[21]=="1" or batiment[22]=="1" or batiment[23]=="1" or batiment[24]=="1" or batiment[33]=="1":
                fenetre.blit(image_production2,(620,100))
            if batiment[36]=="1" or batiment[37]=="1":
                fenetre.blit(image_nourriture2,(620,100))
            pygame.display.flip()
    #pont
    if batiment[43]=="1":
        if stop13==0:
            timer11=10
            q11=queue.Queue()
            t11=threading.Thread(target=timertemps,args=(10,11,))
            t11.start()
            stop13=1
        if q11.empty()==False:
            timer11=q11.get(block=False,timeout=None)
        if timer11==0:
            bouton_barrage=pygame.draw.rect(fenetre,(250,250,250),(870,250,30,35))
            fenetre.blit(image_production2,(870,250))
            pygame.display.flip()
    #eolienne off
    if batiment[57]=="1":
        if stop14==0:
            timer12=10
            q12=queue.Queue()
            t12=threading.Thread(target=timertemps,args=(10,12,))
            t12.start()
            stop14=1
        if q12.empty()==False:
            timer12=q12.get(block=False,timeout=None)
        if timer12==0:
            bouton_eolienne=pygame.draw.rect(fenetre,(250,250,250),(1070,360,30,35))
            fenetre.blit(image_production2,(1070,360))
            pygame.display.flip()
    #desert
    if batiment[44]=="1" or batiment[48]=="1":
        if stop15==0:
            timer13=10
            q13=queue.Queue()
            t13=threading.Thread(target=timertemps,args=(10,13,))
            t13.start()
            stop15=1
        if q13.empty()==False:
            timer13=q13.get(block=False,timeout=None)
        if timer13==0:
            bouton_desertgauche=pygame.draw.rect(fenetre,(250,250,250),(1400,130,30,35))
            fenetre.blit(image_production2,(1400,130))
            pygame.display.flip()
    if batiment[46]=="1" or batiment[50]=="1":
        if stop16==0:
            timer14=10
            q14=queue.Queue()
            t14=threading.Thread(target=timertemps,args=(10,14,))
            t14.start()
            stop16=1
        if q14.empty()==False:
            timer14=q14.get(block=False,timeout=None)
        if timer14==0:
            bouton_desertdroite=pygame.draw.rect(fenetre,(250,250,250),(1720,300,30,35))
            fenetre.blit(image_production2,(1720,300))
            pygame.display.flip()        
    #foret non utiliser
    if stop19==0:
        timer17=10
        q17=queue.Queue()
        t17=threading.Thread(target=timertemps,args=(10,17,))
        t17.start()
        stop19=1
    if q17.empty()==False:
        timer17=q17.get(block=False,timeout=None)
    if timer17==0:
        bouton_foret3=pygame.draw.rect(fenetre,(250,250,250),(1180,50,30,30))
        fenetre.blit(image_pollution2,(1180,50))
        pygame.display.flip()
    #mer
    if batiment[63]=="1":
        if stop20==0:
            timer18=10
            q18=queue.Queue()
            t18=threading.Thread(target=timertemps,args=(10,18,))
            t18.start()
            stop20=1
        if q18.empty()==False:
            timer18=q18.get(block=False,timeout=None)
        if timer18==0:
            bouton_mer1=pygame.draw.rect(fenetre,(250,250,250),(500,650,30,30))
            fenetre.blit(image_production2,(500,650))
            pygame.display.flip()
    if batiment[64]=="1":
        if stop21==0:
            timer19=10
            q19=queue.Queue()
            t19=threading.Thread(target=timertemps,args=(10,19,))
            t19.start()
            stop21=1
        if q19.empty()==False:
            timer19=q19.get(block=False,timeout=None)
        if timer19==0:
            bouton_mer2=pygame.draw.rect(fenetre,(250,250,250),(520,750,30,30))
            fenetre.blit(image_production2,(520,750))
            pygame.display.flip()
    if batiment[65]=="1" or batiment[66]=="1" or batiment[67]=="1":
        if stop22==0:
            timer20=10
            q20=queue.Queue()
            t20=threading.Thread(target=timertemps,args=(10,20,))
            t20.start()
            stop22=1
        if q20.empty()==False:
            timer20=q20.get(block=False,timeout=None)
        if timer20==0:
            bouton_mer3=pygame.draw.rect(fenetre,(250,250,250),(700,850,30,30))
            if batiment[66]=="1":
                fenetre.blit(image_nourriture2,(700,850))
            if batiment[65]=="1" or batiment[67]=="1":
                fenetre.blit(image_production2,(700,850))
            pygame.display.flip()
    if batiment[68]=="1":
        if stop23==0:
            timer21=10
            q21=queue.Queue()
            t21=threading.Thread(target=timertemps,args=(10,21,))
            t21.start()
            stop23=1
        if q21.empty()==False:
            timer21=q21.get(block=False,timeout=None)
        if timer21==0:
            bouton_mer4=pygame.draw.rect(fenetre,(250,250,250),(1250,750,30,30))
            fenetre.blit(image_production2,(1250,750))
            pygame.display.flip()
    if batiment[69]=="1" or batiment[70]=="1" or batiment[71]=="1":
        if stop24==0:
            timer22=10
            q22=queue.Queue()
            t22=threading.Thread(target=timertemps,args=(10,22,))
            t22.start()
            stop24=1
        if q22.empty()==False:
            timer22=q22.get(block=False,timeout=None)
        if timer22==0:
            bouton_mer5=pygame.draw.rect(fenetre,(250,250,250),(1150,850,30,30))
            if batiment[70]=="1":
                fenetre.blit(image_nourriture2,(1150,850))
            else:
                fenetre.blit(image_production2,(1150,850))
            pygame.display.flip()
    #pollution 
    if conditionpollution==0:
        if stop25==0:
            timer23=10
            q23=queue.Queue()
            t23=threading.Thread(target=timertemps,args=(20,23,))
            t23.start()
            stop25=1
        if q23.empty()==False:
            timer23=q23.get(block=False,timeout=None)
        if timer23==0:
            ajout=ajoutpollution(batiment)
            pollution2=pollution2+ajout
            pollution=point+str(pollution2)
            stop25=0
            pygame.display.flip()
    for event in pygame.event.get():
        #triche pour augmenter l'argent pour les verifications
        if event.type==KEYDOWN:
            if event.key==K_1:
                argent2=argent2+10000
                argent=point+str(argent2)
            if event.key==K_2:
                production2=production2+10000
                production=point+str(production2)
            if event.key==K_3:
                nourriture2=nourriture2+10000
                nourriture=point+str(nourriture2)
            if event.key==K_4:
                pollution2=pollution2+200
                pollution=point+str(pollution2)
            if event.key==K_5:
                pollution2=pollution2-200
                pollution=point+str(pollution2)
        if event.type==MOUSEBUTTONDOWN:
            if bouton_maison.collidepoint(event.pos):
                valeur=1
                choix=shop(valeur,argent2,batiment)
                liste=verif_achat(choix,argent2,population2,production2,pollution2)
                prix=liste[0]
                population3=liste[1]
                production3=liste[2]
                pollution3=liste[3]
                nourriture3=liste[4]
                if prix>0:
                    if choix!=59 and choix!=60 and choix!=61 and choix!=62:
                        batiment[choix]=int(batiment[choix])+1
                        batiment[choix]=str(batiment[choix])
                    if choix==59 or choix==60 or choix==61 or choix==62:
                        batiment[choix]=int(batiment[choix])-1
                        batiment[choix]=str(batiment[choix])
                    argent2=argent2-prix
                    argent=point+str(argent2)
                    population2=population2+population3
                    population=point+str(population2)
                if production3<0 and prix>0:
                    production2=production2+production3
                    production=point+str(production2)
                if pollution3<0 and prix>0:
                    pollution2=pollution2+pollution3
                    pollution=point+str(pollution2)
                if nourriture3<0 and prix>0:
                    nourriture2=nourriture2+nourriture3
                    nourriture=point+str(nourriture2)
            if bouton_colline.collidepoint(event.pos):
                valeur=3
                choix=shop(valeur,argent2,batiment)
                liste=verif_achat(choix,argent2,population2,production2,pollution2)
                prix=liste[0]
                population3=liste[1]
                production3=liste[2]
                pollution3=liste[3]
                nourriture3=liste[4]
                if prix>0:
                    if choix!=59 and choix!=60 and choix!=61 and choix!=62:
                        batiment[choix]=int(batiment[choix])+1
                        batiment[choix]=str(batiment[choix])
                    if choix==59 or choix==60 or choix==61 or choix==62:
                        batiment[choix]=int(batiment[choix])-1
                        batiment[choix]=str(batiment[choix])
                    argent2=argent2-prix
                    argent=point+str(argent2)
                if population3<0 and prix>0:
                    population2=population2+population3
                    population=point+str(population2)
                if production3<0 and prix>0:
                    production2=production2+production3
                    production=point+str(production2)
                if pollution3<0 and prix>0:
                    pollution2=pollution2+pollution3
                    pollution=point+str(pollution2)
                if nourriture3<0 and prix>0:
                    nourriture2=nourriture2+nourriture3
                    nourriture=point+str(nourriture2)
            if bouton_foretgauche.collidepoint(event.pos):
                valeur=4
                choix=shop(valeur,argent2,batiment)
                liste=verif_achat(choix,argent2,population2,production2,pollution2)
                prix=liste[0]
                population3=liste[1]
                production3=liste[2]
                pollution3=liste[3]
                nourriture3=liste[4]
                if prix>0:
                    if choix!=59 and choix!=60 and choix!=61 and choix!=62:
                        batiment[choix]=int(batiment[choix])+1
                        batiment[choix]=str(batiment[choix])
                    if choix==59 or choix==60 or choix==61 or choix==62:
                        batiment[choix]=int(batiment[choix])-1
                        batiment[choix]=str(batiment[choix])
                    argent2=argent2-prix
                    argent=point+str(argent2)
                if population3<0 and prix>0:
                    population2=population2+population3
                    population=point+str(population2)
                if production3<0 and prix>0:
                    production2=production2+production3
                    production=point+str(production2)
                if pollution3<0 and prix>0:
                    pollution2=pollution2+pollution3
                    pollution=point+str(pollution2)
                if nourriture3<0 and prix>0:
                    nourriture2=nourriture2+nourriture3
                    nourriture=point+str(nourriture2)
            if bouton_foretbas.collidepoint(event.pos):
                valeur=5
                choix=shop(valeur,argent2,batiment)
                liste=verif_achat(choix,argent2,population2,production2,pollution2)
                prix=liste[0]
                population3=liste[1]
                production3=liste[2]
                pollution3=liste[3]
                nourriture3=liste[4]
                if prix>0:
                    if choix!=59 and choix!=60 and choix!=61 and choix!=62:
                        batiment[choix]=int(batiment[choix])+1
                        batiment[choix]=str(batiment[choix])
                    if choix==59 or choix==60 or choix==61 or choix==62:
                        batiment[choix]=int(batiment[choix])-1
                        batiment[choix]=str(batiment[choix])
                    argent2=argent2-prix
                    argent=point+str(argent2)
                    population2=population2+population3
                    population=point+str(population2)
                if production3<0 and prix>0:
                    production2=production2+production3
                    production=point+str(production2)
                if pollution3<0 and prix>0:
                    pollution2=pollution2+pollution3
                    pollution=point+str(pollution2)
                if nourriture3<0 and prix>0:
                    nourriture2=nourriture2+nourriture3
                    nourriture=point+str(nourriture2)
            if bouton_desert.collidepoint(event.pos):
                valeur=7
                choix=shop(valeur,argent2,batiment)
                liste=verif_achat(choix,argent2,population2,production2,pollution2)
                prix=liste[0]
                population3=liste[1]
                production3=liste[2]
                pollution3=liste[3]
                nourriture3=liste[4]
                if prix>0:
                    if choix!=59 and choix!=60 and choix!=61 and choix!=62:
                        batiment[choix]=int(batiment[choix])+1
                        batiment[choix]=str(batiment[choix])
                    if choix==59 or choix==60 or choix==61 or choix==62:
                        batiment[choix]=int(batiment[choix])-1
                        batiment[choix]=str(batiment[choix])
                    argent2=argent2-prix
                    argent=point+str(argent2)
                if population3<0 and prix>0:
                    population2=population2+population3
                    population=point+str(population2)
                if production3<0 and prix>0:
                    production2=production2+production3
                    production=point+str(production2)
                if pollution3<0 and prix>0:
                    pollution2=pollution2+pollution3
                    pollution=point+str(pollution2)
                if nourriture3<0 and prix>0:
                    nourriture2=nourriture2+nourriture3
                    nourriture=point+str(nourriture2)
            if bouton_pont.collidepoint(event.pos):
                valeur=8
                choix=shop(valeur,argent2,batiment)
                liste=verif_achat(choix,argent2,population2,production2,pollution2)
                prix=liste[0]
                population3=liste[1]
                production3=liste[2]
                pollution3=liste[3]
                nourriture3=liste[4]
                if prix>0:
                    if choix!=59 and choix!=60 and choix!=61 and choix!=62:
                        batiment[choix]=int(batiment[choix])+1
                        batiment[choix]=str(batiment[choix])
                    if choix==59 or choix==60 or choix==61 or choix==62:
                        batiment[choix]=int(batiment[choix])-1
                        batiment[choix]=str(batiment[choix])
                    argent2=argent2-prix
                    argent=point+str(argent2)
                    debloqueconstru=1
                if population3<0 and prix>0:
                    population2=population2+population3
                    population=point+str(population2)
                if production3<0 and prix>0:
                    production2=production2+production3
                    production=point+str(production2)
                if pollution3<0 and prix>0:
                    pollution2=pollution2+pollution3
                    pollution=point+str(pollution2)
                if nourriture3<0 and prix>0:
                    nourriture2=nourriture2+nourriture3
                    nourriture=point+str(nourriture2)
            if bouton_mergauche.collidepoint(event.pos):
                valeur=9
                choix=shop(valeur,argent2,batiment)
                liste=verif_achat(choix,argent2,population2,production2,pollution2)
                prix=liste[0]
                population3=liste[1]
                production3=liste[2]
                pollution3=liste[3]
                nourriture3=liste[4]
                if prix>0:
                    if choix!=59 and choix!=60 and choix!=61 and choix!=62:
                        batiment[choix]=int(batiment[choix])+1
                        batiment[choix]=str(batiment[choix])
                    if choix==59 or choix==60 or choix==61 or choix==62:
                        batiment[choix]=int(batiment[choix])-1
                        batiment[choix]=str(batiment[choix])
                    argent2=argent2-prix
                    argent=point+str(argent2)
                if population3<0 and prix>0:
                    population2=population2+population3
                    population=point+str(population2)
                if production3<0 and prix>0:
                    production2=production2+production3
                    production=point+str(production2)
                if pollution3<0 and prix>0:
                    pollution2=pollution2+pollution3
                    pollution=point+str(pollution2)
                if nourriture3<0 and prix>0:
                    nourriture2=nourriture2+nourriture3
                    nourriture=point+str(nourriture2)
            if bouton_merdroite.collidepoint(event.pos):
                valeur=10
                choix=shop(valeur,argent2,batiment)
                liste=verif_achat(choix,argent2,population2,production2,pollution2)
                prix=liste[0]
                population3=liste[1]
                production3=liste[2]
                pollution3=liste[3]
                nourriture3=liste[4]
                if prix>0:
                    if choix!=59 and choix!=60 and choix!=61 and choix!=62:
                        batiment[choix]=int(batiment[choix])+1
                        batiment[choix]=str(batiment[choix])
                    if choix==59 or choix==60 or choix==61 or choix==62:
                        batiment[choix]=int(batiment[choix])-1
                        batiment[choix]=str(batiment[choix])
                    argent2=argent2-prix
                    argent=point+str(argent2)
                if population3<0 and prix>0:
                    population2=population2+population3
                    population=point+str(population2)
                if production3<0 and prix>0:
                    production2=production2+production3
                    production=point+str(production2)
                if pollution3<0 and prix>0:
                    pollution2=pollution2+pollution3
                    pollution=point+str(pollution2)
                if nourriture3<0 and prix>0:
                    nourriture2=nourriture2+nourriture3
                    nourriture=point+str(nourriture2)
            #gagner de l'argent / production / nourriture / pollution
            if bouton_argent1.collidepoint(event.pos):
                if batiment[0]=="1":
                    argent2=argent2+80
                if batiment[1]=="1":
                    argent2=argent2+100
                if batiment[2]=="1":
                    argent2=argent2+120
                argent=point+str(argent2)
                stop3=0
            if bouton_argent2.collidepoint(event.pos):
                if batiment[54]=="1":
                    argent2=argent2+25
                if batiment[55]=="1":
                    argent2=argent2+25
                if batiment[56]=="1":
                    argent2=argent2+50
                argent=point+str(argent2)
                stop4=0
            if bouton_production1.collidepoint(event.pos):
                if batiment[3]=="1":
                    production2=production2+50
                if batiment[4]=="1":
                    production2=production2+25
                if batiment[5]=="1":
                    production2=production2+50
                if batiment[6]=="1":
                    production2=production2+25
                production=point+str(production2)
                stop5=0
            if bouton_production2.collidepoint(event.pos):
                if batiment[7]=="1":
                    production2=production2+50
                if batiment[8]=="1":
                    production2=production2+25
                if batiment[9]=="1":
                    production2=production2+50
                if batiment[10]=="1":
                    production2=production2+25
                production=point+str(production2)
                stop6=0
            #colline bas
            if bouton_colline1.collidepoint(event.pos):
                if batiment[12]=="1":
                    nourriture2=nourriture2+20
                if batiment[13]=="1":
                    nourriture2=nourriture2+30
                if batiment[18]=="1":
                    pollution2=pollution2-10
                nourriture=point+str(nourriture2)
                pollution=point+str(pollution2)
                stop7=0
            if bouton_colline2.collidepoint(event.pos):
                if batiment[14]=="1":
                    nourriture2=nourriture2+20
                if batiment[15]=="1":
                    nourriture2=nourriture2+30
                if batiment[19]=="1":
                    pollution2=pollution2-10
                nourriture=point+str(nourriture2)
                pollution=point+str(pollution2)
                stop8=0
            if bouton_colline3.collidepoint(event.pos):
                if batiment[16]=="1":
                    nourriture2=nourriture2+20
                if batiment[17]=="1":
                    nourriture2=nourriture2+30
                if batiment[20]=="1":
                    pollution2=pollution2-10
                nourriture=point+str(nourriture2)
                pollution=point+str(pollution2)
                stop9=0
            #zone foret gauche
            if bouton_foretgauche1.collidepoint(event.pos):
                if batiment[21]=="1":
                    production2=production2+50
                if batiment[22]=="1":
                    production2=production2+25
                if batiment[23]=="1":
                    production2=production2+50
                if batiment[24]=="1":
                    production2=production2+25
                if batiment[33]=="1":
                    production2=production2+20
                    pollution2=pollution2-15
                if batiment[36]=="1":
                    nourriture2=nourriture2+20
                if batiment[37]=="1":
                    nourriture2=nourriture2+30
                production=point+str(production2)
                nourriture=point+str(nourriture2)
                pollution=point+str(pollution2)
                stop12=0
            if bouton_foretgauche2.collidepoint(event.pos):
                if batiment[25]=="1":
                    production2=production2+50
                if batiment[26]=="1":
                    production2=production2+25
                if batiment[27]=="1":
                    production2=production2+50
                if batiment[28]=="1":
                    production2=production2+25
                if batiment[34]=="1":
                    production2=production2+20
                    pollution2=pollution2-15
                if batiment[38]=="1":
                    nourriture2=nourriture2+20
                if batiment[39]=="1":
                    nourriture2=nourriture2+30
                production=point+str(production2)
                nourriture=point+str(nourriture2)
                pollution=point+str(pollution2)
                stop11=0
            if bouton_foretgauche3.collidepoint(event.pos):
                if batiment[29]=="1":
                    production2=production2+50
                if batiment[30]=="1":
                    production2=production2+25
                if batiment[31]=="1":
                    production2=production2+50
                if batiment[32]=="1":
                    production2=production2+25
                if batiment[35]=="1":
                    production2=production2+20
                    pollution2=pollution2-15
                if batiment[40]=="1":
                    nourriture2=nourriture2+20
                if batiment[41]=="1":
                    nourriture2=nourriture2+30
                production=point+str(production2)
                nourriture=point+str(nourriture2)
                pollution=point+str(pollution2)
                stop10=0
            #pont
            if bouton_barrage.collidepoint(event.pos):
                if batiment[43]=="1":
                    production2=production2+100
                production=point+str(production2)
                stop13=0
            #eolienne off
            if bouton_eolienne.collidepoint(event.pos):
                if batiment[57]=="1":
                    production2=production2+100
                production=point+str(production2)
                stop14=0
            #desert
            if bouton_desertgauche.collidepoint(event.pos):
                if batiment[44]=="1":
                    production2=production2+70
                if batiment[48]=="1":
                    production2=production2+150
                production=point+str(production2)
                stop15=0
            if bouton_desertdroite.collidepoint(event.pos):
                if batiment[46]=="1":
                    production2=production2+70
                if batiment[50]=="1":
                    production2=production2+150
                production=point+str(production2)
                stop16=0
            #bouton forets
            if bouton_foret1.collidepoint(event.pos):
                if batiment[58]=="0":
                    pollution2=pollution2-50
                pollution=point+str(pollution2)
                stop17=0
            if bouton_foret2.collidepoint(event.pos):
                if batiment[52]=="0":
                    pollution2=pollution2-50
                pollution=point+str(pollution2)
                stop18=0
            if bouton_foret3.collidepoint(event.pos):
                pollution2=pollution2-50
                pollution=point+str(pollution2)
                stop19=0
            if bouton_mer1.collidepoint(event.pos):
                production2=production2+50
                production=point+str(production2)
                stop20=0
            if bouton_mer2.collidepoint(event.pos):
                production2=production2+50
                production=point+str(production2)
                stop20=0
            if bouton_mer3.collidepoint(event.pos):
                production2=production2+50
                production=point+str(production2)
                stop20=0
            if bouton_mer4.collidepoint(event.pos):
                production2=production2+50
                production=point+str(production2)
                stop20=0
            if bouton_mer5.collidepoint(event.pos):
                production2=production2+50
                production=point+str(production2)
                stop20=0
            #quitter le jeux et sauvegarder
            if bouton_exit.collidepoint(event.pos):
                gamerun=False
                pygame.quit()
            if bouton_sauvegarde.collidepoint(event.pos):
                charger=2
                listebatiment(charger,batiment,population2,production2,pollution2,nourriture2,argent2)
        #consequence pollution
        if pollution2>=400 and stop1==0:
            nourriture2=pollution_1(batiment,nourriture2)
            nourriture=point+str(nourriture2)
            stop1=1
        if stop2==1 and pollution2<1200:
            stop2=0
        if pollution2>=1200 and stop2==0:
            liste2=innondation(batiment,production2,pollution2,nourriture2,population2)
            liste=[]
            liste=liste2[0]
            for i in range(len(liste)):
                batiment[i]=liste[i]
            production2=production2+liste2[1]
            population2=population2+liste2[2]
            pollution2=pollution2+liste2[3]
            nourriture2=nourriture2+liste2[4]
            production=point+str(production2)
            population=point+str(population2)
            pollution=point+str(pollution2)
            nourriture=point+str(nourriture2)
            stop2=1
        if event.type==pygame.QUIT:
            gamerun=False
            pygame.quit()
    
    #permettait d'afficher la carte en dessinant a partir du fichier
    #tiled map mais impossible d'adapter la taille et pas de systeme de camera
    #sur pygame
    """layer=tm.get_layer_by_name("Calque de Tuiles 1")
    for x,y,image in layer.tiles():
        x1=(x-y)*(256/2)
        y1=(x+y)*(128/2)
        fenetre.blit(image,(x1,y1))
    layer=tm.get_layer_by_name("Calque de Tuiles 2")
    for x,y,image in layer.tiles():
        x1=(x-y)*(256/2)
        y1=(x+y)*(128/2)
        fenetre.blit(image,(x1,y1))
    pygame.display.flip()
    pygame.display.update()"""