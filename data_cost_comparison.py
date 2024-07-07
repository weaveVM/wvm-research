import matplotlib.pyplot as plt

# Data for 1 MB cost
labels = ['SLER*', 'Celestia', 'Ethereum blobspace (eip-4844)', 'Ethereum calldata']
costs = [0.0173, 0.216064, 36.30, 660.3904]

# Plotting
plt.figure(figsize=(10, 6))
bars = plt.bar(labels, costs, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])

# Adding title and labels
plt.title('Cost of 1 MB of Data', color='white')
plt.xlabel('', color='white')
plt.ylabel('Cost in USD ($)', color='white')

# Setting dark background
plt.gca().set_facecolor('#2e2e2e')
plt.gcf().set_facecolor('#2e2e2e')

# Setting the tick color to white
plt.tick_params(colors='white')

# Adding value labels on top of the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 10, round(yval, 2), ha='center', color='white')
plt.savefig("data_cost_comparison.png")
plt.show()
