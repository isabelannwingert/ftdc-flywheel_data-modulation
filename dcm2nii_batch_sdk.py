#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 2020

@author: Isabel Ann Wingert & Sarah Burke
"""

"""
dcm2nii_batch-sdk.py

this is a batch script for running the dicom to nifti converter gear on ENTIRE session pool 
in a project of dicoms. User will be prompted to enter whether or not they have a list of subjects 
and respective sessions they want to run dcm2niix on, or run the gear on the entire project.

"""

# logging into Flywheel & importing packages
import flywheel
import os # to access input list / excel sheet
import pandas as pd # to read in input list / excel sheet
fw = flywheel.Client()

# group id = group name
# fetching info container into variable
# fw.get() uses hash ids to print out info container
group_id = 'pennftdcenter'
group = fw.get(group_id)

# accessing particular project with prompt for user
# & printing only that hash id and label
# fetching project info container into project
input_project = input("Please type in the exact name of the project you are using: ")
print('printing selected project... \n ... \n')
for project in fw.projects():
    #if "Sandbox_ANTEMORTEMMRI" in project.label:
    if input_project in project.label:
        print('%s: %s \n \n *****' % (project.id, project.label))
        project_label = project.label
        project_id = project.id
    else:
        continue
        # fix this to raise error (empty for now for testing purposes)
    
project = fw.get(project_id)

# prompting user again for accessing the input list (.xlsx)
# list is a two column excel sheet of subject labels and sessions
# pandas package reads in excel sheet as data frame
# terminal will print out three columns: session hash-ids and labels, session label, and subject label
# end goal of loop is to create a list of hash-ids for sessions to access all acquisitions
# Under 'if' = specified subjects taken into consideration for fw.lookup(path)
# Under 'else' = all sessions accessed right away
input_prompt = input("Do you have a list of subjects that you want to run the dcm2niix gear on? Please type 'yes' or press enter if no: ")
if input_prompt == "yes":
    input_directory = input("Please type in which directory the list of your subjects exists (.xlsx): ")
    os.chdir(input_directory)
    input_list = input("Please type in the name of your list file: ")
    test = pd.read_excel(input_list)
    test['Session'] = test['Session'].str[1:-1] # Session Labels may need quotation marks due to date-time interpretation (@Phil Cook ask IW about this if you see this)
    print('\n \n printing your inputted sessions under %s \n Column1 = Session hash-id Column2 = Session label Column 3 = Subject label...' % (input_project))
    #print(test)
    test_dict = dict(zip(test.Subject, test.Session))
    subjects_ids = []
    sessions_ids = []
    for k,v in test_dict.items():
        subject = fw.lookup('{}/{}/{}'.format(group_id, project_label, k))
        #print('%s : %s' % (subject.id, subject.label))
        subjects_ids.append(subject.id)
        for session in subject.sessions():
            print('%s : %s : %s' % (session.id, session.label, subject.label))
            sessions_ids.append(session.id)
else:    
    print('\n \n printing all sessions underneath %s \n ... \n ... \n' % (input_project))
    sessions_ids = []
    for session in project.sessions():
        print('%s : %s' % (session.label, session.id))
        sessions_ids.append(session.id)

        
# iterating every session and printing all acquisitions' ids and labels
# appending those hash ids inHCPto acquisitions_ids list to feed into gear
print('\n \n ***** \n \n')
print('printing acquisitions underneath selected %s Column1 = acquisition label Column2 = acquisition id Column 3 = Session label Column 4 = Subject label... \n ...' %(input_project))
acquisitions_ids = []
acquisitions = []
for i in range(0,len(sessions_ids)):
    session = fw.get(sessions_ids[i])
    subject = fw.get(session.parents.subject)
    for acquisition in session.acquisitions():
        print('%s : %s : %s : %s' % (acquisition.label, acquisition.id, session.label, subject.label))
        acquisitions_ids.append(acquisition.id)
        acquisitions.append(fw.get(acquisitions_ids[i]))
   
# get the gear
gear_dcm2nii = fw.lookup('gears/dcm2niix')
print('\n \n \n running %s gear ... \n \n \n' % (gear_dcm2nii.gear.name))

# propose the batch gear run
proposal = gear_dcm2nii.propose_batch(acquisitions)

# run the batch job
jobs = proposal.run()

# goals for this script:
# (1) Find ways to indicate progress in the script

# from alive_progress import alive_bar
# import time

# with alive_bar(len(jobs)) as bar:
#     for i in jobs:
#         bar()
#         time.sleep(1)

