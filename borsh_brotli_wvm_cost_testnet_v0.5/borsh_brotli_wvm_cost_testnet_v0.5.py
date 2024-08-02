import requests
from borsh_construct import String
import brotli
import matplotlib.pyplot as plt
sample_built_data = 'abc{a{}12345zz0xABCD"""""' * 40000 # 1_000_000 byte
# borsh serialized data
built_data = String.build(sample_built_data)
# Brotli compressed 1MB
compressed_1mb_brotli = brotli.compress(built_data)
print(len(compressed_1mb_brotli))

KILOBYTE = 1_000
CASE_STUDY_1MB = 1_000 * KILOBYTE
ARWEAVE_1MB_BORSH_GZIP_PRICE_URL = f"https://ar-io.dev/price/{len(compressed_1mb_brotli)}"
COINGECKO_TOKENS_URL = "https://api.redstone.finance/prices?symbols=AR,TIA,ETH,BASE&provider=redstone"

BASE_FEE = 21_000
CALLDATA_GAS_PER_BYTE = 16
WVM_CALLDATA_GAS_PER_BYTE = 8
GWEI_TO_ETH = 1e-9
ETH_BASE_FEE_GWEI = 5
WVM_BASE_FEE_GWEI = 1.5
CELESTIA_BASE_FEE_GWEI = 8
BASE_BASE_FEE_GWEI = 0.017
ARB_BASE_FEE_GWEI = 0.01
EIGEN_DA_PER_GB_PRICE = 0.15 # 0.15 ETH
CELETIA_GAS_PRICE = 0.0143 # uTIA source: https://celenium.io/gas

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

def get_winston_cost_of(input_byte):
    res = requests.get(f"https://arweave.net/price/{input_byte}")
    if res.status_code == 200:
        return res.text
    else: 
        print("err", res.status_code)

# fetch winston cost to store on Arweave
arweave_gateway_res = requests.get(ARWEAVE_1MB_BORSH_GZIP_PRICE_URL)
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
    arweave_128kb_usd_cost = float(ARWEAVE_128KB_PRICE) * AR_PRICE * 1e-12
    wvm_128kb_calldata = WVM_CALLDATA_GAS_PER_BYTE * CASE_STUDY_1MB * WVM_BASE_FEE_GWEI * GWEI_TO_ETH * 3.25
    PLOT_WVM_128KB_USD_COST = wvm_128kb_calldata + arweave_128kb_usd_cost
    print(PLOT_WVM_128KB_USD_COST)
    return PLOT_WVM_128KB_USD_COST

def eth_overhead_tx_usd_cost():
    return (BASE_FEE * ETH_BASE_FEE_GWEI * GWEI_TO_ETH * ETH_PRICE)

def eth_calldata_128kb_usd_cost():
    eth_128kb_cost = CALLDATA_GAS_PER_BYTE * CASE_STUDY_1MB * ETH_BASE_FEE_GWEI * GWEI_TO_ETH * ETH_PRICE
    print(eth_128kb_cost)
    return eth_128kb_cost

def base_calldata_128kb_usd_cost():
    eth_settling_cost = eth_overhead_tx_usd_cost()
    base_128kb_cost = CALLDATA_GAS_PER_BYTE * CASE_STUDY_1MB * BASE_BASE_FEE_GWEI * GWEI_TO_ETH * ETH_PRICE
    PLOT_BASE_CALLDATA_128KB_COST = base_128kb_cost + eth_settling_cost
    return PLOT_BASE_CALLDATA_128KB_COST

def arb_calldata_128kb_usd_cost():
    eth_settling_cost = eth_overhead_tx_usd_cost()
    arb_128kb_cost = CALLDATA_GAS_PER_BYTE * CASE_STUDY_1MB * ARB_BASE_FEE_GWEI * GWEI_TO_ETH * ETH_PRICE
    PLOT_ARB_CALLDATA_128KB_COST = arb_128kb_cost + eth_settling_cost
    return PLOT_ARB_CALLDATA_128KB_COST

def eigenda_128kb_usd_cost():
    cost_per_gb_eth = 0.15  # Cost to store 1 GB in ETH
    cost_per_mb_eth = cost_per_gb_eth / 1000
    cost_per_kb_eth = cost_per_mb_eth / 1000
    PLOT_EIGENDA_CALLDATA_1MB_COST = 1000 * cost_per_kb_eth * ETH_PRICE
    return PLOT_EIGENDA_CALLDATA_1MB_COST
    

def celestia_128kb_usd_cost():
    PLOT_CELESTIA_CALLDATA_128KB_COST = CASE_STUDY_1MB * CELESTIA_BASE_FEE_GWEI * CELETIA_GAS_PRICE * 1e-6 * TIA_PRICE
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
plt.title('Cost of Storing 1MB on Different DA solutions\n Borsh-Brotli WeaveVM data settling on Arweave')
plt.xlabel('\nSolutions')
plt.ylabel('Cost in USD')
plt.ylim(0, max(costs) + 1)  # Add some space above the highest bar

# Adding the text labels above the bars
for bar in bars:
    yval = bar.get_height()
    # Formatting the label to show only the first five digits after the decimal
    label = f'{yval:.5f}'
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.03, label, ha='center', va='bottom', color='white')

plt.savefig("./borsh_brotli_wvm_cost_testnet_v0.5/borsh_brotli_wvm_cost_testnet_v0.5.png")
plt.show()
