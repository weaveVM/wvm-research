import requests
import matplotlib.pyplot as plt

KILOBYTE = 1_000
CASE_STUDY_128KB = 128 * KILOBYTE
ARWEAVE_128KB_PRICE_URL = f"https://arweave.net/price/{CASE_STUDY_128KB}"
COINGECKO_TOKENS_URL = "https://api.redstone.finance/prices?symbols=AR,TIA,ETH,BASE&provider=redstone"

BASE_FEE = 21_000
CALLDATA_GAS_PER_BYTE = 16
GWEI_TO_ETH = 1e-9
ETH_BASE_FEE_GWEI = 6
WVM_BASE_FEE_GWEI = 1.5
CELESTIA_BASE_FEE_GWEI = 8
BASE_BASE_FEE_GWEI = 0.013
ARB_BASE_FEE_GWEI = 0.016
EIGEN_DA_PER_GB_PRICE = 0.15 # 0.15 ETH
CELETIA_GAS_PRICE = 0.015 # uTIA source: https://celenium.io/gas

ETH_PRICE = 0
AR_PRICE = 0
BASE_PRICE = 0
TIA_PRICE = 0
ARWEAVE_128KB_PRICE = 0

# for plot
PLOT_WVM_128KB_USD_COST = 0
PLOT_ETH_CALLDATA_128KB_USD_COST = 0
PLOT_BASE_CALLDATA_128KB_COST = 0
PLOT_ARB_CALLDATA_128KB_COST = 0
PLOT_EIGENDA_CALLDATA_128KB_COST = 0
PLOT_CELESTIA_CALLDATA_128KB_COST = 0


# fetch winston cost to store 128kb on Arweave
arweave_gateway_res = requests.get(ARWEAVE_128KB_PRICE_URL)
if arweave_gateway_res.status_code == 200:
    ARWEAVE_128KB_PRICE = arweave_gateway_res.text  
    print(ARWEAVE_128KB_PRICE)
else:
    print("Failed to fetch data: Status code", arweave_gateway_res.status_code)


# Fetch tokens prices
coingecko_res = requests.get(COINGECKO_TOKENS_URL)
if coingecko_res.status_code == 200:
    coingecko_res = coingecko_res.json()

    ETH_PRICE = coingecko_res['ETH']['value']
    AR_PRICE = coingecko_res['AR']['value']
    TIA_PRICE = coingecko_res['TIA']['value']
    BASE_PRICE = coingecko_res['BASE']['value']

else:
    print("err: ", coingecko_res.status_code)

def weavevm_128kb_usd_cost():
    arweave_128kb_usd_cost = float(ARWEAVE_128KB_PRICE) * AR_PRICE * 1e-12 * 0.5 # Borsh reduce data size by ~50% compared to JSON serialization
    wvm_128kb_calldata = CALLDATA_GAS_PER_BYTE * CASE_STUDY_128KB * WVM_BASE_FEE_GWEI * GWEI_TO_ETH * 3.25
    PLOT_WVM_128KB_USD_COST = wvm_128kb_calldata + arweave_128kb_usd_cost
    print(PLOT_WVM_128KB_USD_COST)
    return PLOT_WVM_128KB_USD_COST

def eth_overhead_tx_usd_cost():
    return (BASE_FEE * ETH_BASE_FEE_GWEI * GWEI_TO_ETH * ETH_PRICE)

def eth_calldata_128kb_usd_cost():
    eth_128kb_cost = CALLDATA_GAS_PER_BYTE * CASE_STUDY_128KB * ETH_BASE_FEE_GWEI * GWEI_TO_ETH * ETH_PRICE
    print(eth_128kb_cost)
    return eth_128kb_cost

def base_calldata_128kb_usd_cost():
    eth_settling_cost = eth_overhead_tx_usd_cost()
    base_128kb_cost = CALLDATA_GAS_PER_BYTE * CASE_STUDY_128KB * BASE_BASE_FEE_GWEI * GWEI_TO_ETH * ETH_PRICE
    PLOT_BASE_CALLDATA_128KB_COST = base_128kb_cost + eth_settling_cost
    return PLOT_BASE_CALLDATA_128KB_COST

def arb_calldata_128kb_usd_cost():
    eth_settling_cost = eth_overhead_tx_usd_cost()
    arb_128kb_cost = CALLDATA_GAS_PER_BYTE * CASE_STUDY_128KB * ARB_BASE_FEE_GWEI * GWEI_TO_ETH * ETH_PRICE
    PLOT_ARB_CALLDATA_128KB_COST = arb_128kb_cost + eth_settling_cost
    return PLOT_ARB_CALLDATA_128KB_COST

def eigenda_128kb_usd_cost():
    cost_per_gb_eth = 0.15  # Cost to store 1 GB in ETH
    cost_per_mb_eth = cost_per_gb_eth / 1000
    cost_per_kb_eth = cost_per_mb_eth / 1000
    PLOT_EIGENDA_CALLDATA_128KB_COST = 128 * cost_per_kb_eth * ETH_PRICE
    return PLOT_EIGENDA_CALLDATA_128KB_COST
    

def celestia_128kb_usd_cost():
    PLOT_CELESTIA_CALLDATA_128KB_COST = CASE_STUDY_128KB * CELESTIA_BASE_FEE_GWEI * CELETIA_GAS_PRICE * 1e-6 * TIA_PRICE
    return (PLOT_CELESTIA_CALLDATA_128KB_COST)

# Names of the platforms
platforms = ['WeaveVM Calldata', 'EigenDA', 'Celestia', 'Base Calldata', 'Arb Calldata'] # add: 'Ethereum Calldata'

print(PLOT_WVM_128KB_USD_COST)
# Corresponding costs in USD for storing 128KB
costs = [weavevm_128kb_usd_cost(),eigenda_128kb_usd_cost(), celestia_128kb_usd_cost(), base_calldata_128kb_usd_cost(), arb_calldata_128kb_usd_cost()] # add: eth_calldata_128kb_usd_cost()

plt.style.use('dark_background')
# Create a bar plot

plt.figure(figsize=(10, 6))
colors = ['#00ff00', '#00cc00', '#009900', '#006600', '#003300']  # Different shades of green
bars = plt.bar(platforms, costs, color=colors)
# Add title and labels
plt.title('Cost of Storing 128KB on Different DA solutions\n Borsh-serialization for WeaveVM data on Arweave')
plt.xlabel('\nSolutions')
plt.ylabel('Cost in USD')
plt.ylim(0, max(costs) + 1)  # Add some space above the highest bar

# Adding the text labels above the bars
for bar in bars:
    yval = bar.get_height()
    # Formatting the label to show only the first five digits after the decimal
    label = f'{yval:.5f}'
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.03, label, ha='center', va='bottom', color='white')

plt.savefig("./borsh_serialized_da_cost_comparison/da_cost_comparison.png")
plt.show()
