import csv
import random
import re
import matplotlib.pyplot as plt
import subprocess
import time
import os.path
import cPickle as pickle
import numpy as np

loci_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] #note: dropped cac40 and 67 for more than 30 alleles

litter_sizeATL = [6, 4,	4, 3, 4, 4, 6, 3, 3, 4, 4, 5, 5, 4, 4, 4, 4, 3, 5] #size of each Atlantic litter
litter_sizeKEY = [6, 4, 3, 4, 3, 3, 3, 4] #size of each Keys litter

total_momsATL = 19 # number of atlantic litters/moms
total_momsKEY = 8 # number of keys litters/moms


#Import mother genotypes for Atlantic and Keys as list of lists, each mother is a list
with open('\Users\Amanda Barker\Dropbox\Python_Bnose\ATL_moms.txt', 'rU') as f:
    mom_allelesATL = list(csv.reader(f, delimiter = '\t'))
with open('\Users\Amanda Barker\Dropbox\Python_Bnose\KEY_moms.txt', 'rU') as f:
    mom_allelesKEY = list(csv.reader(f, delimiter = '\t'))

#Import allele frequencies for Atlantic and Keys as list of lists. Each locus it's own list, 1st element is #alleles
with open('\Users\Amanda Barker\Dropbox\Python_Bnose\ATL_allele_freq.txt', 'rU') as f:
    allele_freqATL = list(csv.reader(f, delimiter = '\t'))
with open('\Users\Amanda Barker\Dropbox\Python_Bnose\KEY_allele_freq.txt', 'rU') as f:
    allele_freqKEY = list(csv.reader(f, delimiter = '\t'))

#Import list of alleles at each locus
with open('\Users\Amanda Barker\Dropbox\Python_Bnose\Allele_list.txt', 'rU') as f:
    allele_list = list(csv.reader(f, delimiter = '\t'))

#convert mother genotypes to allele codes
coded_allelesATL = []
coded_allelesKEY = []
mom_allele1 = range(0, 41, 2) # pass 1 and pass 2 to solve double allele (diploid) vs single allele lists
mom_allele2 = range(1, 42, 2) # maximum number of alleles per locus x2
mom_count = 0
locus_count = 0
for mom in range(0, total_momsATL):
    current_mom = []
    for locus in range(0, (len(loci_list))):
        current_locus = []
        pos = 0
        m1 = mom_allele1[locus]
        m2 = mom_allele2[locus]
        for x in allele_list[locus]: #only loop over the specific # of alleles at that locus
            if mom_allelesATL[mom][m1] == x:
                current_locus.append(pos)
            else:
                pos += 1
        pos = 0
        for x in allele_list[locus]:
            if mom_allelesATL[mom][m2] == x:
                current_locus.append(pos)
            else:
                pos += 1
        locus_count += 1
        current_mom.append(current_locus)
    coded_allelesATL.append(current_mom)
    mom_count += 1


#reset mom and locus count for keys
mom_count = 0
locus_count = 0
for mom in range(0, total_momsKEY):
    current_mom = []
    for locus in range(0, (len(loci_list))):
        current_locus = []
        pos = 0
        m1 = mom_allele1[locus]
        m2 = mom_allele2[locus]
        for x in allele_list[locus]: #only loop over the specific # of alleles at that locus
            if mom_allelesKEY[mom][m1] == x:
                current_locus.append(pos)
            else:
                pos += 1
        pos = 0
        for x in allele_list[locus]:
            if mom_allelesKEY[mom][m2] == x:
                current_locus.append(pos)
            else:
                pos += 1
        locus_count += 1
        current_mom.append(current_locus)
    coded_allelesKEY.append(current_mom)
    mom_count += 1

num_sims = 7
counter = 0
sim_avgresults = np.zeros((num_sims, 21))
for sim in range(0,num_sims):
    #generate list of random loci to be used
    random_picks = []
    for r in loci_list:
        random_picks.append(random.sample(loci_list, r))
    print random_picks

    prdm_resultsATL = [] #list of results-- results for all moms at that #loci within a list, then list of those lists
    prdm_resultsKEY = []


    #create files data file and litter_size file
    for r in loci_list:
        print r, 'ATL'
        current_locus = []
        for mom in range(0, total_momsATL):
            print mom
            check_file = open('\Users\Amanda Barker\Dropbox\Python_Bnose\Done.txt', 'w')
            check_file.close()
            num_loci = str(r)
            data_file = open('\Users\Amanda Barker\Dropbox\Python_Bnose\mmdata.txt', 'w')
            data_file.write(num_loci + '\n')
            for freq_line in range(0, r):
                x = str(allele_freqATL[freq_line -1])
                x1 = re.sub('[^0-9. ]', "", x) #removes string punctuation (^ means "everything except the following")
                x2 = re.sub('[ ]', '\t', x1) #replace spaces with tabs
                data_file.write(x2 + '\n')
            data_file.write('2' + '\t' + '0.90' + '\t' + '0.10' + '\n')
            for code_line in range(0, r):
                x = str(coded_allelesATL[mom][code_line -1])
                x1 = re.sub('[^0-9 ]', "", x)
                x2 = re.sub('[ ]', '\t', x1)
                data_file.write(x2 + '\n')
            data_file.close()
            litter_file = open('\Users\Amanda Barker\Dropbox\Python_Bnose\Litter_size.txt', 'w')
            s = str(litter_sizeATL[mom])
            litter_file.write(s + '\n' + '\n' + '0' + '\n')
            litter_file.close()
            subprocess.Popen('\Users\Amanda Barker\Dropbox\Python_Bnose\Run_file.bat')
            while os.path.isfile('\Users\Amanda Barker\Dropbox\Python_Bnose\Done.txt'):
                time.sleep(0.75)
            res_file = open('\Users\Amanda Barker\Dropbox\Python_Bnose\Results_parsed.txt')
            res = res_file.read()
            result = float(res)
            current_locus.append(result)
        prdm_resultsATL.append(current_locus)

    for r in loci_list:
        print r, 'KEY'
        current_locus = []
        for mom in range(0, total_momsKEY):
            print mom
            check_file = open('\Users\Amanda Barker\Dropbox\Python_Bnose\Done.txt', 'w')
            check_file.close()
            num_loci = str(r)
            data_file = open('\Users\Amanda Barker\Dropbox\Python_Bnose\mmdata.txt', 'w')
            data_file.write(num_loci + '\n')
            for freq_line in range(0, r):
                x = str(allele_freqKEY[freq_line -1])
                x1 = re.sub('[^0-9. ]', "", x) #removes string punctuation (^ means "everything except the following")
                x2 = re.sub('[ ]', '\t', x1) #replace spaces with tabs
                data_file.write(x2 + '\n')
            data_file.write('2' + '\t' + '0.90' + '\t' + '0.10' + '\n')
            for code_line in range(0, r):
                x = str(coded_allelesKEY[mom][code_line -1])
                x1 = re.sub('[^0-9 ]', "", x)
                x2 = re.sub('[ ]', '\t', x1)
                data_file.write(x2 + '\n')
            data_file.close()
            litter_file = open('\Users\Amanda Barker\Dropbox\Python_Bnose\Litter_size.txt', 'w')
            s = str(litter_sizeKEY[mom])
            litter_file.write(s + '\n' + '\n' + '0' + '\n')
            litter_file.close()
            subprocess.Popen('\Users\Amanda Barker\Dropbox\Python_Bnose\Run_file.bat')
            while os.path.isfile('\Users\Amanda Barker\Dropbox\Python_Bnose\Done.txt'):
                time.sleep(1.0)
            res_file = open('\Users\Amanda Barker\Dropbox\Python_Bnose\Results_parsed.txt')
            res = res_file.read()
            result = float(res)
            current_locus.append(result)
        prdm_resultsKEY.append(current_locus)


    combined_results = [] #this stores the results for all litters for this particular loci combo
    for r in range(0, len(loci_list)):
        combined_results.append(prdm_resultsATL[r] + prdm_resultsKEY[r]) #creates one list for the results of all the litters (doesn't sum anything)
    avg_results = [0] * len(combined_results)
    for r in range(0, len(combined_results)):
        total = 0
        for i in combined_results[r]:
            num1 = str(i)
            num2 = float(num1)
            total += num2
        avg_results[r] = total / len(combined_results[r])
        sim_avgresults[sim, r] = avg_results[r]
    np.savetxt('\Users\Amanda Barker\Dropbox\Python_Bnose\PrDM_Sim_avg_results.txt', sim_avgresults, fmt='%.4f') #save the average results of each iteration to text file in case program messes up. Don't have to start all over. Rename the file if you do have to start over so you can combine the results at the end. Otherwise it will write over the file and you'll lose all the results you got before the error.
    counter += 1
    print 'counter = ', counter
    print '----------------------------------------------------------------------------------------------------------'
print combined_results
print avg_results
print len(combined_results)
print len(avg_results)
print len(sim_avgresults)
print sim_avgresults
#total_avg_results = (np.mean(sim_avgresults, axis =0, dtype=float))

#print total_avg_results

#print len(total_avg_results)
#total_avg_results = [] * len(sim_avgresults)
#for i in range(0, len(loci_list)):
 #   total_avg_results.append(np.mean(sim_avgresults, axis=0))

#save results so you don't have to keep running this again when it messes up or you want to do something different w figures
#with open('PrDM_combined_results', 'w') as f:
#    pickle.dump(combined_results, f)
#with open('\Users\Amanda Barker\Dropbox\Python_Bnose\PrDM_average_results.pickle', 'wb') as f:
    #pickle.dump(total_avg_results, f)

#to unpickle:
#with open('\Users\Amanda Barker\Dropbox\Python_Bnose\PrDM_average_results.pickle', 'rb') as f:
 #    total_avg_results = pickle.load(f)
'''
# plot results
plt.figure()
plt.plot(loci_list, total_avg_results)
plt.xlabel('Number of Loci')
plt.ylabel('PrdM')
plt.axis([1,21,0,1])
plt.title("Probability of detecting multiple paternity with # loci")
plt.savefig('Prdm_results')
'''




# This no longer works-- test to make sure all mom alleles were coded. Already confirmed that everything is in order
# but will need to re-code if want to check again since I changed the way the mother allele code section works.
# for mom in range(0, len(coded_allelesATL)):
#     counter = 0
#     for allele in coded_allelesATL[mom]:
#         if allele == -9:
#             print "uh oh", mom, allele, counter, mom_allelesATL[mom][counter]
#         counter += 1
# for mom in range(0, len(coded_allelesKEY)):
#     counter = 0
#     for allele in coded_allelesKEY[mom]:
#         if allele == -9:
#             print "uh oh", mom, allele, counter, mom_allelesKEY[mom][counter]
#         counter += 1

