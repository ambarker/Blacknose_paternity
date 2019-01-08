'''
A Barker 10/19/2017
Update with final dataset of all  litters (27)
Also updated with new way of sampling loci: Takes every combination of loci instead of randomly sampling
'''

import csv
import itertools
import copy
import numpy as np

#List of dictionary keys
locusKeyList = ['Locus01A', 'Locus01B', 'Locus02A', 'Locus02B', 'Locus03A', 'Locus03B',
                'Locus04A', 'Locus04B', 'Locus05A', 'Locus05B', 'Locus06A', 'Locus06B',
                'Locus07A', 'Locus07B', 'Locus08A', 'Locus08B', 'Locus09A', 'Locus09B',
                'Locus10A', 'Locus10B', 'Locus11A', 'Locus11B', 'Locus12A', 'Locus12B',
                'Locus13A', 'Locus13B', 'Locus14A', 'Locus14B', 'Locus15A', 'Locus15B',
                'Locus16A', 'Locus16B', 'Locus17A', 'Locus17B', 'Locus18A', 'Locus18B',
                'Locus19A', 'Locus19B', 'Locus20A', 'Locus20B', 'Locus21A', 'Locus21B',
                'Locus22A', 'Locus22B', 'Locus23A', 'Locus23B']
locusList = ['Locus01', 'Locus02', 'Locus03', 'Locus04', 'Locus05', 'Locus06', 'Locus07', 'Locus08', 'Locus09', 'Locus10', 'Locus11', 'Locus12', 'Locus13', 'Locus14', 'Locus15', 'Locus16', 'Locus17', 'Locus18', 'Locus19', 'Locus20', 'Locus21', 'Locus22', 'Locus23']
num_Loci = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

# lists to store all combinations of loci
L1 = []
L2 = []
L3 = []
L4 = []
L5 = []
L6 = []
L7 = []
L8 = []
L9 = []
L10 = []
L11 = []
L12 = []
L13 = []
L14 = []
L15 = []
L16 = []
L17 = []
L18 = []
L19 = []
L20 = []
L21 = []
L22 = []
L23 = []

# list of lists of loci combos
L_list = [L1, L2, L3, L4, L5, L6, L7, L8, L9, L10, L11, L12, L13, L14, L15, L16, L17, L18, L19, L20, L21, L22, L23]


# generate all combinations
for n in num_Loci:
    for l in itertools.combinations(locusList, n):
        L_place = n - 1
        L_list[L_place].append(l)

# declare the empty list of individuals
individuals = []
# declare the empty list of families
families = []

locusAList = []
locusBList = []

def importData(location):
    inputFile = csv.DictReader(open(location))
    # loop through every entry in the input file
    for entry in inputFile:
        # append each entry into the list of individuals
        individuals.append(entry)

def assignIdentities():
    #Loop through all individuals
    for individual in individuals:
        name = individual.get('ID')

        # Define who the moms are by checking the name
        firstFour = name[:4]
        # The last two indicate which pup it is
        lastTwo = name[-2:]
        if firstFour == "Mama":
            # set the family ID
            individual['FamilyID'] = int(lastTwo)
            # set the type
            individual['Type'] = firstFour
        else:
            # Now that all the moms are done, need to do the babies
            # Pup IDs are stored in the 2nd and 3rd position of the ID string
            secondThird = name[1:3]
            # set the family ID
            individual['FamilyID'] = int(secondThird)
            # set the type
            individual['Type'] = lastTwo


def generateFamilies():
    # Construct a list of all the families
    # start with the number of families
    numberOfFamilies = 27
    # then the empty list that will contain each family
    listsOfFamilies = []
    # family IDs start at 1, so it needs to be offset
    for familyIndex in range(1, numberOfFamilies + 1):
        # create an empty list for each family to loop through
        familyList = []
        # loop through each individual and find all who share the same familyID
        for individual in individuals:
            if individual.get('FamilyID') == familyIndex:
                # once found, add that individual to the family list
                familyList.append(individual)
        ## Add the family to the list of all families
        listsOfFamilies.append(familyList)
    return listsOfFamilies


def run():
    # declare families global, so that I populate it
    global families
    # import the data, which writes to the individuals list
    importData("bnose_formatted.csv")
    assignIdentities()
    families = generateFamilies()

#Each locus has 2 alleles, so split into 2 lists: LocusA & LocusB
def splitLocusList():
    global locusAList
    global locusBList

    for index in range(len(locusKeyList)):
        if index % 2 == 0:
            locusAList.append(locusKeyList[index])
        else:
            locusBList.append(locusKeyList[index])


## Now I can call the run function that hooks everything together
run()
splitLocusList()

#Function to find mother of a family
def findMama(family):
    for individual in family:
        if individual.get('Type') == "Mama":
            return individual

def countFathers(numberAlleles):
    if numberAlleles <= 2: return 1

    if numberAlleles >= 3 and numberAlleles <= 4: return 2

    if numberAlleles >=5 and numberAlleles <= 6: return 3

    if numberAlleles >=7 and numberAlleles <= 8: return 4

    if numberAlleles >=9 and numberAlleles<=10: return 5

    if numberAlleles >=11 and numberAlleles<=12: return 6

#Function to find locus of interest for an individual
def findLociPerIndividual(individual, lociList):
    individualsLoci = []
    for locus in lociList:
        individualsLoci.append(individual.get(locus))
    return individualsLoci

#Function to determine the number of fathers depending on the locus
def checkPaternity(family, loci_list):
    # find  alleles based on loci count for a family
    #LociDict = loci_list

    # separate lists of loci from inside the dictionary
    LociA = [a + "A" for a in c]
    LociB = [b + "B" for b in c]

    # delineate mama and make a list of alleles at each locus in the lists above
    mama = findMama(family)
    mamaLociA = findLociPerIndividual(mama, LociA)
    mamaLociB = findLociPerIndividual(mama, LociB)

    allLociFathers = []
    for locusIndex in range(0, len(mamaLociA)):
        paternalAllele = []
        #Loop through each individual in the family
        for individual in family:

            #Skip mama
            if individual.get('Type') == "Mama": continue
            #Now I know that the current individual is a pup
            pup = individual
            #Find alleles for each randomly selected locus for each pup
            pupLociA = findLociPerIndividual(pup, LociA)
            pupLociB = findLociPerIndividual(pup, LociB)

            # Identify allele A and B for mama
            mamaAlleleA = mamaLociA[locusIndex]
            mamaAlleleB = mamaLociB[locusIndex]
            # Identify allele A and B for pup
            pupAlleleA = pupLociA[locusIndex]
            pupAlleleB = pupLociB[locusIndex]

            # #Account for missing data
            # if pupAlleleA == "-9" or pupAlleleB == "-9":
            #     continue
            # check pup locus A
            if pupAlleleA != mamaAlleleA and pupAlleleA != mamaAlleleB:
                paternalAllele.append(pupAlleleA)
            # check pup locus B
            if pupAlleleB != mamaAlleleA and pupAlleleB != mamaAlleleB:
               paternalAllele.append(pupAlleleB)
            # if alleles are the same, one must be paternal
            # this fixes issue of not counting paternal alleles that are the same as the mother
            if pupAlleleA == pupAlleleB:
                paternalAllele.append(pupAlleleA) #could append A or B, doesn't matter because they are the same
            numberAlleles = len(set(paternalAllele)) #set makes sure only counting unique alleles
            fathers = countFathers(numberAlleles)

            allLociFathers.append(fathers)
    if len(allLociFathers) == 1:
        return max(allLociFathers)
    else:
        if max(allLociFathers) == 2:
            if allLociFathers.count(2) >= 2:
                return 2
            else:
                return 1
        else:
            return max(allLociFathers)

results_list = []
for combo in L_list:
    combo_results = []
    print combo
    for c in combo:
    	print c
        c_results = []
        c = list(c)
        for family in families:
            num_fathers = checkPaternity(family, c)
            c_results.append(num_fathers)
        x = sum(s > 1 for s in c_results)
        per_paternity = x/27.0
        combo_results.append(per_paternity)
    results_list.append(combo_results)
print results_list

average_results = []
for r in results_list:
    x = np.mean(r)
    average_results.append(x)
print average_results

results_file = open('paternity_results.txt', 'w')
for i in average_results:
    results_file.write("%s\n" % i)

