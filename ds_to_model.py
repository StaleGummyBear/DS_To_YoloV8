import os
import re
import pdb
import shutil
import glob

import supervision as sv
from tqdm.notebook import tqdm
from autodistill_grounded_sam import GroundedSAM
from autodistill.detection import CaptionOntology

from autodistill_yolov8 import YOLOv8

RAW_DS = 'ds/raw_datasdet/'
SPLIT_DS = 'ds/split_dataset/'
AD_OUT_DS = 'ds/autodistill_out/'
PROC_DS_FOLDER = 'ds/dataset/'

###############   
#EZ BP function     
############### 
def bp():
    pdb.set_trace()
   
###############   
#Split function     
###############    
def split():
    input("This doesn't work yet. Assuming that" + SPLIT_DS + "has been populated with already-split DB. Enter any key to continue: ")
    
###############   
#AutoDistill function     
###############   
def auto_distill():
    #For each 'class' 0-n folder in the split_dataset folder
    for classFolder in os.listdir(SPLIT_DS):
        print("Starting new class...")
        
        input("Enter what should the base model look for in this class(nothing specific for this! i.e. car)? ")
        input("Enter what is this class specifically of, no spaces(Nissan_Sentra)? ")
        ontology = CaptionOntology({
            detectWhat : specificWhat
        })
        base_model = GroundedSAM(ontology=ontology)
        dataset = base_model.label(
            input_folder=SPLIT_DS + str(classFolder) + '/',
            extension=".jpg",
            output_folder=(AD_OUT_DS + str(classFolder) + '/'))

###############   
#Relabel function     
###############        
def relabel():
    print("---------------------------------------------------------")
    print("Relabeling...")
    
    labels = [] #.txt contents
    classIdx = 0 #index in relation to folder count for label correction
    
    #For each 'class' 0-n folder in the split_dataset folder
    for classFolder in os.listdir(AD_OUT_DS):
    
        #Choose between train and valid
        for mode in range(0,2):
            
            #Form path
            modeSel = ''
            if mode == 0:
                modeSel = '/train/labels/'
            else:
                modeSel = '/valid/labels/'    
            rel_path = AD_OUT_DS + str(classFolder) + modeSel
            for file in os.listdir(rel_path):
                if file.endswith(".txt"):
                
                    #OPEN/CLOSE -- Obtain labels
                    with open(rel_path + file, "r") as f:
                        labels = f.read()
                    f.close()  
        
                    #Replace all single digit numbers with the classIdx
                    newLabels = str(classIdx) + labels[1:]     
                
                    #OPEN/CLOSE -- Write new labels
                    with open(rel_path + file, "w") as f:
                        f.write(newLabels)
                    f.close()
    
        
        #Iterate class index for labeling
        classIdx+=1
    
###############   
#Flatten function     
############### 
def flatten():
    print("---------------------------------------------------------")
    print("Starting flatten split dataset step...")
    
    for classFolder in os.listdir(AD_OUT_DS):
        shutil.copytree(AD_OUT_DS + str(classFolder), PROC_DS_FOLDER, dirs_exist_ok=True)
        
    print("Flatten complete! Please edit the data.yaml to (reflect all classes) in: " + PROC_DS_FOLDER)
        
    

#Ask user to clear all files in post/proc (skips raw ds folder)
#q = input("Do you want to clean all proc and post folders? (Y or N)")
#if q=='y' or q=='Y':
#    for procpostdir in [AD_OUT_DS,PROC_DS_FOLDER]: #,SPLIT_DS
#        files = glob.glob(procpostdir)
#        for f in files:
#            os.remove(f)

#--------------------------------------------------------------------------------
# SPLIT RAW DATASET
#--------------------------------------------------------------------------------   
q = input("Do you want to split your dataset (one big folder of photos) into class-folders? (Y or N)")
if q=="Y" or q =="y":     
    print("---------------------------------------------------------")
    print("Splitting raw dataset into class folders...")
    split() 
    
else:
    print("SKIPPING SPLIT")
    

#--------------------------------------------------------------------------------
# RUN AUTODISTILL ON EACH CLASS
#--------------------------------------------------------------------------------        
q = input("Do you want to run autodistill? (Y or N)")
if q=="Y" or q =="y":     
    print("---------------------------------------------------------")
    print("Using Autodistill to label each class...")
    auto_distill() 
else:
    print("SKIPPING AUTODISTILL")

#--------------------------------------------------------------------------------
# RELABEL
#--------------------------------------------------------------------------------
q = input("Do you want to fix the labeling in split_dataset? (Y or N) ")
if q=="Y" or q =="y":     
    relabel() 
else:
    print("SKIPPING RELABEL")
    
#--------------------------------------------------------------------------------
# FLATTEN SPLIT DATASET
#--------------------------------------------------------------------------------
q = input("Do you want to flatten split_dataset into dataset? (Y or N) ")
if q=="Y" or q =="y":     
    flatten() 
else:
    print("SKIPPING FLATTEN")
            
#--------------------------------------------------------------------------------
# Train
#--------------------------------------------------------------------------------
q = input("Do you want to train? (Y or N)? ")
if q=="Y" or q =="y":
    print("---------------------------------------------------------")
    print("Execute this CMD in the DEVID_v2 folder:")
    print("yolo task=detect mode=train model=yolov8x.pt data=C:\Users\johnl\Downloads\DEVID_v2\ds\dataset\data.yaml epochs=100")
    print("---------------------------------------------------------")
input("Press ENTER to quit")


            