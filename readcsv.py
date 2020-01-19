#!/usr/bin/env python3
import csv
import matplotlib.pyplot as plt
import matplotlib

'''
csv file downloaded from https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=microlensing&constraint=mlmodeldef=1
with seltction: "Download Currently Filtered Rows"

more discriptive information about the columm information please see csv_columns.txt file

e.g.

plntname:       Planet Name 
ra:             RA [deg]
dec:            Dec [deg] 
mlmassplnj:     Planet Mass [Jupiter mass]                 
mlmassplnjerr1: Planet Mass Upper Unc. [Jupiter mass]                  
mlmassplnjerr2: Planet Mass Lower Unc. [Jupiter mass]

mlmassplne:     Planet Mass [Earth mass]                   
mlmassplneerr1: Planet Mass Upper Unc. [Earth mass]                    
mlmassplneerr2: Planet Mass Lower Unc. [Earth mass]

mlsmaproj:      Planet-star Projected Semi-major Axis [AU]                 
mlsmaprojerr1:  Planet-star Projected Semi-major Axis Upper Unc.                   
mlsmaprojerr2:  Planet-star Projected Semi-major Axis Lower Unc.

mlmasslens:     Lens Mass [Solar mass]                 
mlmasslenserr1: Lens Mass Upper Unc.                   
mlmasslenserr2: Lens Mass Lower Unc.

mldistl:        Lens Distance [pc]                 
mldistlerr1:    Lens Distance Upper Unc.                   
mldistlerr2:    Lens Distance Lower Unc.

mlmodelchisq:   Model Chi-squared                                   
mldescription:  Model Description  
'''
font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }

def csvreader(filename, columms):
    '''
    # filename: the csv file name which we want to open, e.g. XXX.csv
    # columms: a list, the columms name we want to get, e.g. ["rowid", "plntname"]
    # return: res - a dict, each element of res corresponding to the data of each columm, 
        e.g. {"rowid":[a list of rowids], "plntname":[a list of planet names]}
    '''
    res = dict(zip(columms,[[] for i in columms ]))
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for col in columms:
                res[col].append(row[col])
    return res

def csvheaders(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None)
    return headers


# e.g. read the rowid and planet name of all 86 planets

filename = 'microlensing_20200117_singlesol.csv'
columms = ["rowid", "plntname", "mldescription"]

headers = csvheaders(filename)
# print(headers)

res = csvreader(filename, columms)
# for i in range(1,87):
#     print("%s."%i)
#     print(res["mldescription"][i-1],"\n")

# print(res["plntname"])
print(len(res["plntname"])) #86


# e.g. read Ras and Decs and plot them out, with Earth mass, or Jupiter mass as color;
columms = ["ra","dec", "mlmassplnj", "mlmassplne", "mldists"]
res = csvreader(filename, columms)
Ras = [float(i) for i in res["ra"]]
Decs = [float(i) for i in res["dec"]]
# Mes = [float(i) for i in res["mlmassplne"]]
Mjs = [float(i) for i in res["mlmassplnj"]]
# Dists = [float(i) for i in res["mldists"]] # and source distence "mldists" as point size; about half have no source distance data


fig = plt.figure()
plt.subplot(111, projection="aitoff")
cm = matplotlib.cm.get_cmap('jet')#RdYlBu
plt.scatter(Ras, Decs, c=Mjs, vmin=min(Mjs), vmax=max(Mjs), cmap=cm, s=16)
cb = plt.colorbar()
cb.set_label(r'Planet Mass [M$_{Jup}$]',fontdict=font)
plt.suptitle("MicroLensing Planets Distribution",fontdict=font)
plt.grid(True)


fig.savefig("MicroLensPlanetDistribution.png", format='png', bbox_inches='tight', dpi=300, pad_inches = 0)

plt.show()