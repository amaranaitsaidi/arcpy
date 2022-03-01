# -*- coding: utf-8 -*-
import arcpy 
import os
import re	#regex
import sys
import csv
import xlrd
import xlwt
import math
import time
from operator import itemgetter
from xml.dom import minidom

arcpy.env.overwriteOutput = True
################################################
cou= arcpy.GetParameterAsText(0)
sortie=arcpy.GetParameterAsText(1)
sortie_tous_cables = arcpy.GetParameterAsText(2)
sortie_cou_pbo_intersect =  arcpy.GetParameterAsText(3)
sortie_cou_bpe_intersect =  arcpy.GetParameterAsText(4)
sortie_cable_mal_nomes = arcpy.GetParameterAsText(5)




################################################
#assignation des differents chemins (en fonction des parametres d'entree)
fichier_sde = ur"J:\DOCUMENT_POLE_DATA\OUTIL\SDE\{}_WSCRIPT_sdeDEFAULT.sde".format(cou)
arcpy.env.workspace = fichier_sde
arcpy.AddMessage(fichier_sde)
liste_dataset_sde = arcpy.ListDatasets("*Equipment*","All")
for dataset_Equip in liste_dataset_sde:
    desc = arcpy.Describe(dataset_Equip)
    arcpy.AddMessage("Dataset NetDesigner: {}\tProjection : {}".format(desc.name, desc.spatialReference.name))
    projection_destination = desc.spatialReference.name
    liste_couche_sde = arcpy.ListFeatureClasses("*","All",dataset_Equip)
    for couche_sde in liste_couche_sde:
	if(re.compile(".*Hubsite$").match(couche_sde) != None):
	    couche_sde_hubsite = os.path.join(dataset_Equip,couche_sde)
	    chem_clftth=fichier_sde+"\\"+os.path.join(dataset_Equip,couche_sde)
	    arcpy.AddMessage("Hubsite: " + couche_sde_hubsite)
	elif(re.compile(".*Pedestal$").match(couche_sde) != None):
	    couche_sde_pedestal = os.path.join(dataset_Equip,couche_sde)
	    chem_pbo=fichier_sde+"\\"+os.path.join(dataset_Equip,couche_sde)
	    chem_stech=fichier_sde+"\\"+os.path.join(dataset_Equip,couche_sde)
	    arcpy.AddMessage("Pedestal: " + couche_sde_pedestal)
	elif(re.compile(".*Enclosure$").match(couche_sde) != None):
	    couche_sde_enclosure = os.path.join(dataset_Equip,couche_sde)
	    chem_bpe=fichier_sde+"\\"+os.path.join(dataset_Equip,couche_sde)
	    arcpy.AddMessage("Enclosure: " + couche_sde_enclosure)
	elif(re.compile(".*Fiber_Cable$").match(couche_sde) != None):
	    couche_sde_fiber_cable = os.path.join(dataset_Equip,couche_sde)
	    chem_caftth=fichier_sde+"\\"+os.path.join(dataset_Equip,couche_sde)
	    arcpy.AddMessage("Fiber_Cable: " + couche_sde_fiber_cable)
	elif(re.compile(".*Chamber$").match(couche_sde) != None):
	    couche_sde_chamber = os.path.join(dataset_Equip,couche_sde)
	    chem_cham=fichier_sde+"\\"+os.path.join(dataset_Equip,couche_sde)
	    arcpy.AddMessage("Chamber: " + couche_sde_chamber)
	elif(re.compile(".*OverheadSpan$").match(couche_sde) != None):
	    couche_sde_OverheadSpan = os.path.join(dataset_Equip,couche_sde)
	    chem_aer=fichier_sde+"\\"+os.path.join(dataset_Equip,couche_sde)
	    arcpy.AddMessage("OverheadSpan: " + couche_sde_OverheadSpan)
	elif(re.compile(".*SupportStructure$").match(couche_sde) != None):
	    couche_sde_supportstructure = os.path.join(dataset_Equip,couche_sde)
	    chem_pth =fichier_sde+"\\"+os.path.join(dataset_Equip,couche_sde)
	    arcpy.AddMessage("SupportStructure: " + couche_sde_supportstructure)
	elif(re.compile(".*UndergroundSpan$").match(couche_sde) != None):
	    couche_sde_undergroundspan = fichier_sde+"\\"+os.path.join(dataset_Equip,couche_sde)
	    chem_sout=fichier_sde+"\\"+os.path.join(dataset_Equip,couche_sde)
	    arcpy.AddMessage("UndergroundSpan: " + couche_sde_undergroundspan)

arcpy.env.workspace = fichier_sde
liste_dataset_sde = arcpy.ListDatasets("*Administration*","All")
for dataset_Equip in liste_dataset_sde:
    desc = arcpy.Describe(dataset_Equip)
    liste_couche_sde = arcpy.ListFeatureClasses("*","All",dataset_Equip)
    for couche_sde in liste_couche_sde:
        if(re.compile(".*ARRIERE$").match(couche_sde) != None):
            couche_sde_za = os.path.join(dataset_Equip,couche_sde)
            chem_za=fichier_sde+"\\"+os.path.join(dataset_Equip,couche_sde)
	    arcpy.AddMessage("ZONE_ARRIERE: " + couche_sde_za)
	if(re.compile(".*Communes$").match(couche_sde) != None):
            couche_sde_com = os.path.join(dataset_Equip,couche_sde)
            chem_com=fichier_sde+"\\"+os.path.join(dataset_Equip,couche_sde)
	    arcpy.AddMessage("Communes: " + couche_sde_com)
########################################################################################
if cou=='AXIONE':
    chaine=fichier_sde+"\\"+"NETWORKS.VBlock"
    chaine1=fichier_sde+"\\"+"NETWORKS.OptPatchPanel"
    chaine2=fichier_sde+"\\"+"NETWORKS.Rack"
    chaine3=fichier_sde+"\\"+"NETWORKS.SPCVBlock"
    chaine4=fichier_sde+"\\"+"NETWORKS.SPCOptPatchPanel"
    chaine5=fichier_sde+"\\"+"NETWORKS.SPCRack"
else:
    chaine=fichier_sde+"\\"+"NETDESIGNER.VBlock"
    chaine1=fichier_sde+"\\"+"NETDESIGNER.OptPatchPanel"
    chaine2=fichier_sde+"\\"+"NETDESIGNER.Rack"
    chaine3=fichier_sde+"\\"+"NETDESIGNER.SPCVBlock"
    chaine4=fichier_sde+"\\"+"NETDESIGNER.SPCOptPatchPanel"
    chaine5=fichier_sde+"\\"+"NETDESIGNER.SPCRack"

########################################################################################
 
couche_bpe = arcpy.MakeFeatureLayer_management(chem_bpe)
couche_cable = arcpy.MakeFeatureLayer_management(chem_caftth)
couche_pbo = arcpy.MakeFeatureLayer_management(chem_pbo)

champ_a_verfier = ["REFERENCE", "OBJECTID"]  
values={}
values["Ref_Nulle"]=0
with arcpy.da.SearchCursor(couche_cable, champ_a_verfier) as rows:
    for r in rows:
        if r[0] in [None,""]:
            values["Ref_Nulle"]+=1
        else:
            if r[0] not in values:
                values[r[0]]=1
            else:
                values[r[0]]+=1 
del rows

dictDoublons = {}
dictPasDoublons = {}
cable_cda = 'CDA'
count = 0
for item in values:
    
    if values[item] > 1 :
        if not item.startswith("CDA"):
            dictDoublons[item] = 'Doublons'
            count+=1
            arcpy.AddWarning('Il y a {} cables en doublons  a Verifier / Corriger.'.format(count))
    else:   
        dictPasDoublons[item] = 'PasDoublons'

liste_de_doublons = []
for key in dictDoublons:
    liste_de_doublons.append(key)

#mettre les doublons dans un tuple 
tuple_doublons = tuple(liste_de_doublons)

#selection de tout les cables en doublons   
for i in tuple_doublons:
    resultat_selection = arcpy.SelectLayerByAttribute_management(couche_cable, "NEW_SELECTION", "REFERENCE in ('{:s}')".format("','".join(liste_de_doublons)))
#création de la couche des cables selectionnées 
resultat_selection_feature = arcpy.MakeFeatureLayer_management(resultat_selection)

chem_cable_doublons = os.path.join(sortie_tous_cables, "tous_les_doublons.shp")
arcpy.CopyFeatures_management(resultat_selection_feature , chem_cable_doublons)




try:
    arcpy.AddField_management(chem_cable_doublons, "SECTIONNE", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED")
except:
    arcpy.AddWarning(" un bug d'arcmap est survenu, veuillez redémarrez arcmap et réessayez.")

#Evaluation de la distance entre les cables coupés et les cables en doublons dans la base

D={}
try : 
    with arcpy.da.SearchCursor(chem_cable_doublons, ["REFERENCE","SHAPE@WKT"]) as c:
        for r in c:
            if r[0] not in D:
                D[r[0]]=[r[1]]
            else:
                D[r[0]].append(r[1])
    del c
except :
    arcpy.AddMessage("Un bug est survenu, Veuillez redémarrer arcmap et recommencez s'il vous plait. ")


SECTIONNE={}
for k in D:
    arcpy.AddMessage("###############################################################")
    ini= D[k][0].index("(")
    fini= D[k][0].index(")")
    taf=D[k][0][ini+1:fini+1]
    taf=taf.replace(" 0","")
    taf=taf.replace(", ",",")
    taf=taf.replace(" ",",")
    tabb2=taf.split(",")
    tabb2[0]=tabb2[0].replace("(","")
    tabb2[-1]=tabb2[-1].replace(")","")
    for i in range(len(tabb2)):
        tabb2[i]=float(tabb2[i])
    P1=[tabb2[0],tabb2[1]]
    P2=[tabb2[-3],tabb2[-2]]
    inii= D[k][1].index("(")
    finii= D[k][1].index(")")
    taf2=D[k][1][inii+1:finii+1]
    taf2=taf2.replace(" 0","")
    taf2=taf2.replace(", ",",")
    taf2=taf2.replace(" ",",")
    tabb22=taf2.split(",")
    tabb22[0]=tabb22[0].replace("(","")
    tabb22[-1]=tabb22[-1].replace(")","")
    for i in range(len(tabb22)):
        tabb22[i]=float(tabb22[i])
    P3=[tabb22[0],tabb22[1]]
    P4=[tabb22[-3],tabb22[-2]]
    d1_3=math.sqrt((P1[0]-P3[0])**2+(P1[1]-P3[1])**2)
    d1_4=math.sqrt((P1[0]-P4[0])**2+(P1[1]-P4[1])**2)
    d2_3=math.sqrt((P2[0]-P3[0])**2+(P2[1]-P3[1])**2)
    d2_4=math.sqrt((P2[0]-P4[0])**2+(P2[1]-P4[1])**2)
    dd=[d1_3,d1_4,d2_3,d2_4]
    dd1=[min(dd)]
    for e in dd1:
        arcpy.AddMessage(e)
        if e <= 0.02:
            arcpy.AddMessage("Le cable "+k+" est sectionne")
            SECTIONNE[k]=True 
        elif e > 0.02 :
            arcpy.AddMessage("Erreur de nommage sur al ref " +k)
            SECTIONNE[k]=False
            
with arcpy.da.UpdateCursor(chem_cable_doublons, ["REFERENCE","SECTIONNE"]) as c:
   for r in c:
       if SECTIONNE[r[0]]==True:
           maj="Sectionne"
       else:
           maj="Mal_nomme"  
       c.updateRow((r[0],maj))
del c

RESULTAT=arcpy.MakeFeatureLayer_management(chem_cable_doublons,"RESULTAT.shp")
arcpy.CopyFeatures_management(RESULTAT , sortie_cable_mal_nomes)


B=arcpy.SelectLayerByAttribute_management(RESULTAT,"NEW_SELECTION","SECTIONNE='Sectionne'")
save=False
while save==False:
    try:
        arcpy.CopyFeatures_management(B,os.path.join(sortie_cable_mal_nomes,cou+"_Sectionne"))
        save=True
    except:
        pass
    
C=arcpy.SelectLayerByAttribute_management(RESULTAT,"NEW_SELECTION","SECTIONNE='Mal_nomme'")
save=False
while save==False:
    try:
        arcpy.CopyFeatures_management(C,os.path.join(sortie_cable_mal_nomes, cou+"_Mal_nomme"))
        save=True
    except:
        pass





#selection des pbo qui coupent les lignes à deux centimètre
select_pbo_cut_lines = arcpy.SelectLayerByLocation_management(couche_pbo,"WITHIN_A_DISTANCE",resultat_selection_feature, 0.02, "NEW_SELECTION")
pbo_coupant_cable = arcpy.MakeFeatureLayer_management(select_pbo_cut_lines)

#copie de la couche pbo qui intersecte les cables coupes
chem_pbo_intersect = os.path.join(sortie_cou_pbo_intersect, "PBO_INTERSECT")
arcpy.CopyFeatures_management(pbo_coupant_cable , chem_pbo_intersect)


#selection des pbo qui coupent les lignes à deux centimètre
select_bpe_cut_lines = arcpy.SelectLayerByLocation_management(couche_bpe,"WITHIN_A_DISTANCE",resultat_selection_feature,0.02,"NEW_SELECTION")
bpe_coupant_cable = arcpy.MakeFeatureLayer_management(select_bpe_cut_lines)

#copie de la couche bpe qui intersecte les cables coupes
chem_bpe_intersect = os.path.join(sortie_cou_bpe_intersect, "BPE_INTERSECT")
arcpy.CopyFeatures_management(bpe_coupant_cable, chem_bpe_intersect)
   
"""
##@param :
##Dictionnaire
##@return :
##fichier csv en indiquant la date de l'execution du script. 
"""
def exportCsvDoublons(dict):
    csv_file= open(os.path.join(sortie, 'CablesEnDoublons_{}_'.format(cou) + str(datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")) +'.csv'), 'wb')
    writer = csv.writer(csv_file)
    for key, value in dict.items():
        writer.writerow([key, value])
    csv_file.close()



###Appel des fonctions

exportCsvDoublons(dictDoublons)

  
