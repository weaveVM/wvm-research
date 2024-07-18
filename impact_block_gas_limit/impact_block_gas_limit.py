###
# forked from https://github.com/nerolation/eth-gas-limit-analysis
###

from web3 import Web3
import snappy
import os 
EXECUTION = True
import matplotlib.cm as cm

if EXECUTION:
    provider_url = 'https://testnet-rpc.wvm.dev'  # WeaveVM testnet RPC URL

    w3 = Web3(Web3.HTTPProvider(provider_url))
    if not w3.is_connected():
        raise Exception("Failed to connect to WeaveVM network")
    print("Connected")

# Given constraints
block_gas_limit = 300_000_000    # Block gas limit
gas_cost_per_byte = 16          # Gas cost per byte of calldata
gas_cost_per_zero_byte = 4     # Gas cost per zero byte of calldata
transaction_base_cost = 21_000  # Base transaction cost
max_transaction_size = 131_072  # Maximum transaction size in bytes (128 KB)

# Gas
max_fee_per_gas = w3.to_wei(80, 'gwei')
max_priority_fee_per_gas = w3.to_wei(75, 'gwei')

# Estimated sizes for various fields (in bytes)
mandatory_fields = {
    'chain_id': 4, 'nonce': 8, 'max_priority_fee_per_gas': 32, 'max_fee_per_gas': 32,
    'gas_limit': 8, 'to_address': 20, 'value': 32, 'signature': 65
}
# This is simplified and could be even more optimized for larger blocks
mandatory_fields_size = sum(mandatory_fields.values())

max_calldata_size = max_transaction_size - mandatory_fields_size
print(f"Transaction can have {max_calldata_size:,} bytes of calldata")
print(f"This equals to {max_calldata_size/1024**2:.3f} MB of calldata")

# Gas used for the calldata of a maximum-sized transaction
gas_for_calldata_zero_bytes = max_calldata_size * gas_cost_per_zero_byte
gas_for_calldata = max_calldata_size * gas_cost_per_byte

print(f"Calldata (zero-byte) requires {gas_for_calldata_zero_bytes:,} gas")
print(f"Calldata requires {gas_for_calldata:,} gas")

total_gas_per_transaction_zero_bytes = transaction_base_cost + gas_for_calldata_zero_bytes
total_gas_per_transaction = transaction_base_cost + gas_for_calldata
print(f"Transaction (zero-byte) requires {total_gas_per_transaction_zero_bytes:,} gas")
print(f"Transaction requires {total_gas_per_transaction:,} gas")

transactions_per_block_zero_bytes = block_gas_limit//total_gas_per_transaction_zero_bytes
transactions_per_block = block_gas_limit//total_gas_per_transaction
print(f"{transactions_per_block_zero_bytes} transactions fit in one block (zero-byte calldata)")
print(f"{transactions_per_block} transactions fit in one block")

remaining_space_gas_zero_bytes = block_gas_limit%total_gas_per_transaction_zero_bytes
remaining_space_gas = block_gas_limit%total_gas_per_transaction
remainder_tx_size_zero_bytes = (remaining_space_gas_zero_bytes-21000)/gas_cost_per_zero_byte
remainder_tx_size = (remaining_space_gas-21000)/gas_cost_per_byte
print(f"Remaining space in block with zero-byte calldata: {remainder_tx_size_zero_bytes} bytes")
print(f"Remaining space in block with zero-byte calldata: {remainder_tx_size} bytes")

block_size_zero_bytes = transactions_per_block_zero_bytes * max_transaction_size
block_size = transactions_per_block * max_transaction_size
print(f"Block size: {(block_size_zero_bytes+remainder_tx_size_zero_bytes)/1024**2} MB")
print(f"Block size: {(block_size+remainder_tx_size)/1024**2} MB")

cost_one_tx = total_gas_per_transaction * max_fee_per_gas
print(f"Costs per tx:    {float(w3.from_wei(cost_one_tx, 'ether')):.3f} WVM")
print(f"Costs per block: {float(w3.from_wei(cost_one_tx * transactions_per_block, 'ether')):.3f} WVM")

# Apply snappy compression to zero bytes calldata
calldata_zero_bytes = bytes(max_calldata_size)
remainder_calldata_zero_bytes = bytes(int(remainder_tx_size_zero_bytes))
print(f"Can be snappy compressed from {len(calldata_zero_bytes+remainder_calldata_zero_bytes)} to {len(snappy.compress(calldata_zero_bytes+remainder_calldata_zero_bytes))}")

max_block_size_zero_bytes = len(snappy.compress(calldata_zero_bytes*55+remainder_calldata_zero_bytes))/(1024**2)
print(f"Maximum block size: {max_block_size_zero_bytes:.2f} MB")

# Apply snappy compression to random bytes calldata
calldata_bytes = os.urandom(max_calldata_size)
remainder_calldata_bytes = os.urandom(int(remainder_tx_size))
print(f"Can be snappy compressed from {len(calldata_bytes+remainder_calldata_bytes)} to {len(snappy.compress(calldata_bytes+remainder_calldata_bytes))}")

max_block_size = len(snappy.compress(calldata_bytes*14+remainder_calldata_bytes))/(1024**2)
print(f"Maximum block size: {max_block_size:.2f} MB")

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.cm as cm

def get_max_block_size_in_mb(block_gas_limit, emptybytes=True):
    if emptybytes:
        gas_cost = gas_cost_per_zero_byte
    else:
        gas_cost = gas_cost_per_byte
    gas_for_calldata = max_calldata_size * gas_cost  
    total_gas_per_transaction = transaction_base_cost + gas_for_calldata
    transactions_per_block = block_gas_limit//total_gas_per_transaction
    print(f"{transactions_per_block} transactions fit in one block")
    block_size = transactions_per_block * max_transaction_size
    
    remaining_gas = block_gas_limit%total_gas_per_transaction
    remaining_space_for_calldata = (remaining_gas - transaction_base_cost) / gas_cost

    block_size += 1 * remaining_space_for_calldata
    print(f"Block size: {block_size/1024**2} MB")
    return block_size/1024**2


gas_limits_empty = [i for i in range(block_gas_limit, block_gas_limit+16_000_000, int(2e6))]
block_sizes_empty = [get_max_block_size_in_mb(i) for i in gas_limits_empty]

#gas_limits = [i for i in range(block_gas_limit, block_gas_limit+16_000_000, int(2e6))]
gas_limits = [i for i in range(0, block_gas_limit + 1_000_000, int(2e6))]

block_sizes = [get_max_block_size_in_mb(i, emptybytes=False) for i in gas_limits]


def format_func(value, tick_number):
    return f'{int(value / 1_000_000)}m'
plt.style.use('dark_background')
x = gas_limits
y = block_sizes
colors = cm.Greens(0.7)
fig, ax = plt.subplots(figsize=(12, 4))
plt.rcParams['font.family'] = 'Ubuntu Mono'
ax.fill_between(x, y, color=colors, alpha=0.8)
ax.set_xlabel('Block Gas Limit', fontsize=14)
ax.set_ylabel('Block Size (MB)', fontsize=14)
ax.set_title('Max. Block Size vs Gas Limit \n\n wvm.dev \n', fontsize=16)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_func))
plt.yticks(fontsize=14)
plt.xticks(fontsize=14)
plt.tight_layout()
ax.grid(color='gray', linestyle='-', linewidth=0.5)
ax.legend_ = None
plt.savefig("./impact_block_gas_limit/impact_block_gas_limit.png")
plt.show()