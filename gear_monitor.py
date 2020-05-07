#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 15:37:16 2020
@author: isabelannwingert
"""
# basic API creation and flywheel package import
import flywheel
fw = flywheel.Client()


# naming gear of interest
# prints out list of gears to console to ensure user
#   inputs correct gear name for 
gears = fw.get_all_gears(limit=5000)
gear_names = list(map(lambda x: x['gear']['name'], gears))
print('Here are all the gear names: \n')
for gear in gear_names:
    print(gear)
      
# prompting user for input of gear name(s)    
# setting up gear_query list for all input(s) to be appended to 
gear_query = []
prompt = True
while prompt == True:
    gear_input = input('Which gear do you want the status of?: ')
    gear_query.append(gear_input)
    continue_input = input('Do you have another gear to search the status of? [Y|n]:')
    if continue_input == 'n':
        prompt = False
        break
    else:
        continue
    
# creating three lists that sort job objects based on JobObject.status
#   (1) "complete" = job ran through
#   (2) "failed" = job failed
#   (3) "running" = job is still running
# Prints out total number of jobs per status per gear  
for g in range(0,len(gear_query)):
    print(gear_query[g], ": \n")
    query_jobs = fw.get_current_user_jobs(gear=gear_query[g])
    query_jobs_running = [j for j in query_jobs['jobs'] if j.state == 'running']
    query_jobs_failed = [j for j in query_jobs['jobs'] if j.state == 'failed']
    query_jobs_complete = [j for j in query_jobs['jobs'] if j.state == 'complete']
    print("There are ", len(query_jobs_running), gear_query[g], "jobs running.")
    print("There are ", len(query_jobs_failed), gear_query[g], "jobs that failed.")
    print("There are ", len(query_jobs_complete), gear_query[g], "jobs complete.")
    print("\n")