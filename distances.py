#Generating the input file for cpptraj
import sys
filelist = []
residue = []
residue.append('O9')
residue.append('O11')
with open('OMAH_12_corrected_final_mixture_calc_backbone_rms.in','w') as inp:
    inp.write('%s\n' % (''.join(str('trajin OMAH_12_corrected_final_mixture_md2_Box_100ns.nc'))))
    inp.write('%s\n' % (''.join(str('trajin OMAH_12_corrected_final_mixture_md2_Box_1000ns.nc'))))
    inp.write('%s\n' % (''.join(str('trajin OMAH_12_corrected_final_mixture_md2_Box_reimaged_100-1000ns.nc'))))
    inp.write('%s\n' % (''.join(str('rms first out OMAH_12_corrected_final_mixture_md2_Box_100-1000ns_py.out'))))
    totalnumber = 0
    for first in residue:
        for second in residue:
            for res1 in range(1232,1244):
                for res2 in range(res1+1,1244):
                    totalnumber += 1
                    inp.write('distance D%s :%s@%s :%s@%s out dist_%s@%s_%s@%s.out\n' % (''.join(str(totalnumber)),''.join(str(res1)),first,''.join(str(res2)),second,''.join(str(res1)),first,''.join(str(res2)),second))
                    filelist.append('dist_%s@%s_%s@%s.out' % (''.join(str(res1)),first,''.join(str(res2)),second))
    inp.write('%s\n' % (''.join(str('run'))))


#Running the cpptraj bash command
import subprocess
command = "cpptraj -p OMAH_12_corrected_final_mixture_Box.parm7 -i OMAH_12_corrected_final_mixture_calc_backbone_rms.in"
process = subprocess.run(command,shell=True)

#Taking all distances and copying them in one single array and calculating the minimum for each file
dist = [[] for a in range(len(filelist))]
mins = []
count = 0
subcount = 0
frame = []
names = []
for file in filelist:
    with open(file,'r') as f:
        distbis = []
        subcount = 0
        for line in f:
            if 'Frame' in line:
                continue
            subcount += 1
            dist[count].append(float(line.rstrip().split()[1]))
            distbis.append(float(line.rstrip().split()[1]))
        mins.append(min(distbis))
        names.append(file)
        count += 1
        frame.append(subcount)
#print(dist)
#print(mins)
with open('distances_100-1000ns.out','w') as g:
    d = 0
    while d<totalnumber:
        for x in range(frame[d]):
            g.write('%s\t' % float(dist[d][x]))
        g.write('\n')
        d += 1
e = 0
with open('minimum_distances_100-1000ns.out','w') as h:
    for element in mins:
        h.write('%s\t' % names[e])
        h.write('%s\n' % element)
        e += 1