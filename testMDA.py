import MDAnalysis as mda
from MDAnalysis.analysis import contacts

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load trajectory and topology files
u = mda.Universe("OMAH_2X12mer_corrected_final.parm7", "2X12mer_wat_md2_1000ns.nc", format='NCDF')

# Select atoms for chain1 and chain2
chain1 = u.select_atoms('resid 1-12')
chain2 = u.select_atoms('resid 13-24')

def contacts_within_cutoff(u, chain1, chain2, radius=4.5):
    timeseries = []
    for ts in u.trajectory:
        # Calculate distances between chain1 and chain2
        dist = contacts.distance_array(chain1.positions, chain2.positions)
        # Determine which distances <= radius
        n_contacts = contacts.contact_matrix(dist, radius).sum()
        timeseries.append([ts.frame, n_contacts])
    return np.array(timeseries)

# Calculate contact analysis
ca = contacts_within_cutoff(u, chain1, chain2, radius=4.5)

# Convert to DataFrame
ca_df = pd.DataFrame(ca, columns=['Frame', '# Contacts'])

# Plot contact analysis
ca_df.plot(x='Frame', y='# Contacts')
plt.ylabel('# No. of contacts')
plt.show()