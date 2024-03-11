import numpy as np
import matplotlib.pyplot as plt

# Step 1: Specify the input file and initialize lists
output_combinations_file = "output_combinations.txt"

# Step 2: Read data from the output_combinations file
with open(output_combinations_file, 'r') as f:
    lines = f.readlines()

# Step 3: Assign numerical values to the conformations as described
conformation_values = {
    'GHG': 1, 'GHH': 2import numpy as np.py, 'HHH': 3, 'GGG': 4,
    'GGH': 5, 'HGG': 6, 'HHG': 7, 'HGH': 8
}

numeric_values = [conformation_values.get(line.split()[-1], 0) for line in lines]

# Step 4: Output numerical values in a separate file
with open("output_numeric_values.txt", 'w') as output_file:
    for t, value in enumerate(numeric_values):
        output_file.write(f"{t}: {value}\n")

# Step 5: Plot conformations over time
plt.plot(np.arange(0, len(numeric_values)), numeric_values, marker='o', linestyle='-', color='b')
plt.xlabel('Simulation Time')
plt.ylabel('Conformation Value')
plt.title('Conformation Values Over Time')
plt.savefig('conformation_plot.png')  # Save as PNG file