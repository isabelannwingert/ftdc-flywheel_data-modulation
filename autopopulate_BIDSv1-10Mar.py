# --------------------------------
# autopopulate_BIDSv1-10Mar.py
# --------------------------------
### 10th March 2020 v 1.0

### --- This script utilizes the following methods to autopopulate BIDS
#####     filenames on the FlyWheel Cloud

### --- Import of three columns from Excel Sheet as Pandas DataFrame:
#####     (1) UNIQUE Series-Description
#####     (2) Modality label suffixes for BIDS filenames
#####     (3) BIDS parent folder/container names

### --- The above variables are generated to create dict info = {},
###     populated with keys = File name of BIDS Image and
###     values = Flywheel Image IDs (series_id in tabulate.csv)

### --- Isabel Ann Wingert & Tinashe M Tapera
#####   isabel.wingert@pennmedicine.upenn.edu
#####   tinashe.tapera@pennmedicine.upenn.edu

### --- Please check our progress on our GitHub Repository!
#####   Link: (https://github.com/isabelannwingert/ftdc-flywheel_data-modulation)


# -------------------------------------------
# IMPORTING PACKAGES AND MODALITIES / SET-UP
# -------------------------------------------

import os  # --- Working Directory Set-up, ensuring
###   _SeriesModality.xlsx is complete
import pandas as pd  # --- Pandas is a module that allows information


###   from the SeriesModality Excel Sheet
###   to be passed into Python and manipulated
###   and ultimately used for conversion

# create_key() is a function to populate for dictionary info
###     that links Flywheel images and IDs to be converted
##### --- template = BIDS path pointing to BIDS named image on FlyWheel
#####     outtype = the file type of the image captured in the variable
#####     annotation_classes = additional notes regarding the image
def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


# Imported collections module for user to check progress as
###     script's curation progresses
##### --- See rec_key_replace() below
from collections.abc import Mapping


# rec_key_replace() is to modify series descriptions by taking
###   out illegal characters
def rec_key_replace(obj):
    if isinstance(obj, Mapping):
        return {key.replace('_', 'x').replace("-", "x"):
                    rec_key_replace(val) for key, val in obj.items()}
    return obj


# Changing working directory to where _SeriesModality.xslx is located
###   Make sure Pandas DataFrame is in working folder!
os.chdir('/home/wingerti/wingert_workspace')

# Reading Unique Series Descriptions column in with Pandas
###   Converting Unique Series Description DataFrame to list
###   Ensuring Unique Series Description is a flat list
###   Illegal characters in BIDS standard include "-" and "_", replace w/ 'x'
df_series_desc = pd.read_excel('BIDS_SingleProject_SeriesModality10Mar.xlsx', usecols="A")
series_desc = df_series_desc.values.tolist()
series_desc = [item for sublist in series_desc for item in sublist]
series_desc_modified = [desc.replace('_', 'x').replace('-', 'x') for desc in series_desc]

# Applying the same logic from Series Descriptions to modality labels
###   and Parent Folders Set-up
df_modality_labels = pd.read_excel('BIDS_SingleProject_SeriesModality10Mar.xlsx', usecols="B")
modality_labels = df_modality_labels.values.tolist()
modality_labels = [item for sublist in modality_labels for item in sublist]

df_parent_folders = pd.read_excel('BIDS_SingleProject_SeriesModality10Mar.xlsx', usecols="C")
parent_folders = df_parent_folders.values.tolist()
parent_folders = [item for sublist in parent_folders for item in sublist]

# For user discretion, this will print out how the BIDS folders are to be set-up
###   Print out "Series Description/Image, Labeled as modality label, under Parent Folder Container"
ser_mod_pairs = dict(zip(series_desc, modality_labels))
ser_mod_pairs = rec_key_replace(ser_mod_pairs)
for k, v in ser_mod_pairs.items():
    for w in range(len(parent_folders)):
        print("The ", k, "image will be labeled as ", v, "and will be put in the ", parent_folders[w])

    # -------------------------------------------


# INFO DICTIONARY FUNCTION FOR CURATION
# -------------------------------------------

# info = {} is a dictionary that will pair image IDs and images on FlyWheel
### --- Image IDs (series_ids) are how FlyWheel determines where images exist in its domain
#####   Explanations per line in this function are provided

def infotodict(seqinfo):
    # setting all variables with image information to be global for precautions
    global series_desc
    global modality_pairs
    global parent_folders

    # Intializing info = {}
    info = {}

    # The path of images are to be split into increments to set up the template variable
    ### --- Ultimately, these increments (type=string) will be concatenated
    ### --- This is so FlyWheel can set up the BIDS filename and Path correctly
    #####   *string_part1* +
    #####   **parent_folder** +
    #####   ***string_part3*** +
    #####   ****series_desc_modified**** +
    #####   *****modality_label*****

    ### --- EXAMPLE (for generic T1 structual image):
    #####   *sub-{subject}/ses-{session}/*
    #####   **anat**
    #####   ***/sub-{subject}_ses-{session}_acq-/***
    #####   ****t1xmprxAXxMPRAGE****
    #####   *****_T1W*****
    #####   sub-{subject}/ses-{session}/anat/sub-{subject}_ses-{session}_acq-t1xmprxAXxMPRAGE_T1W

    string_part1 = 'sub-{subject}/ses-{session}/'  # --- 1st "increment" of
    ###   the BIDS path name
    string_part3 = 'sub-{subject}_ses-{session}_acq-'  # --- 3rd "increment" of
    ###   the BIDS path name
    transform1 = []  # --- Intializing list of 1st concatenation
    transform2 = []  # --- Initializing list of 2nd concatenation
    transform3 = []  # --- Initializing list of 3rd and final concatenation
    create_key_list = []  # --- Initializing list of strings to be put
    ###   into create_key() for template creation

    # print(modality_labels)
    # --- 1st Concatenation
    ###   Adding respective parent_folders / containers to 1st string increment
    ###   Appending aforementioned concatenation
    for i in range(len(parent_folders)):
        # print(parent_folders[i])
        out_string_i = string_part1 + parent_folders[i] + "/"
        transform1.append(out_string_i)

    # --- 2nd Concatenation
    ###   Adding string_part3 to string_part1 and parent_folder concatenation
    ###   Appending aforementioned concatenation
    for j in transform1:
        out_string_j = j + string_part3
        transform2.append(out_string_j)

    # --- 3rd Concatenation
    ###   Adding respective series_desc_modified to 2nd concatenation
    ###   Appending aformentioned resulting concatenation
    for k in range(len(series_desc_modified)):
        out_string_k = transform2[k] + series_desc_modified[k]
        transform3.append(out_string_k)

    # --- Creating string input for create_key()
    ###   Concatenating the last increment = respective modality_labels
    for l in range(len(modality_labels)):
        out_string_l = transform3[l] + "_" + modality_labels[l]
        create_key_list.append(out_string_l)

    # --- Inputting each string input into create_key()
    ###   Appending create_key() output into list for info = {} set-up
    create_key_links = []
    for create_key_list_i in create_key_list:
        new_key = create_key(create_key_list_i)
        create_key_links.append(new_key)

    # --- Appending create_key() outputs as key values for info = {}
    for x in range(len(create_key_links)):
        info[create_key_links[x]] = []

    # print(info) # --- Just a checkpoint
    # --- Taking create_key() output keys in info dict
    ###   Going into tabulate .csv output to acquire series_id (hash ID)
    ###   IF THE MODIFIED series_description matches the series descritpion
    ###   from the tabulate .csv output modified in the same way, then append
    ###   the series_id (hash ID) as its value
    #####   We do this because this helps FlyWheel locate images and convert
    #####   them in the way that is specified in the template output
    for k, v in info.items():
        # print(k[0], v)
        for s in seqinfo:
            print(s.series_description)
            desc = s.series_description.replace('_', 'x').replace('-', 'x')
            if desc in k[0]:
                # print("hit")
                info[k].append(s.series_id)
            # else:
            # print("no hit")

    # print(info)
    return info


# print(info)

# --- Illegal characters are also not allowed in the session names, same string modification is applied to the session ID before curation and conversion into the BIDS Filename
def ReplaceSession(sesname):
    return sesname.replace("-", "x").replace("_", "x")


