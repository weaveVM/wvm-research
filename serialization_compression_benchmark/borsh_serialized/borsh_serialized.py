import snappy
import gzip
import bz2
import lzma
import paq
from borsh_construct import U8, U64, String, CStruct, Option, Vec
from construct import Container
import matplotlib.pyplot as plt
import brotli
import pyzstd
import zlib

# Define Hex as a string for simplicity
Hex = String

# Header struct
Header = CStruct(
    "parent_hash" / Hex,
    "ommers_hash" / Hex,
    "beneficiary" / Hex,
    "state_root" / Hex,
    "transactions_root" / Hex,
    "receipts_root" / Hex,
    "withdrawals_root" / Hex,
    "logs_bloom" / Hex,
    "difficulty" / Hex,
    "number" / U64,
    "gas_limit" / U64,
    "gas_used" / U64,
    "timestamp" / U64,
    "mix_hash" / Hex,
    "nonce" / U64,
    "base_fee_per_gas" / U64,
    "blob_gas_used" / Option(U64),
    "excess_blob_gas" / Option(U64),
    "parent_beacon_block_root" / Option(Hex),
    "requests_root" / Option(Hex),
    "extra_data" / Hex
)

# BlockHeader struct
BlockHeader = CStruct(
    "hash" / Hex,
    "header" / Header
)

# Block struct
Block = CStruct(
    "header" / BlockHeader,
    "body" / Vec(CStruct()),  # assuming body contains a list of empty structures
    "ommers" / Vec(CStruct()),  # assuming ommers contains a list of empty structures
    "withdrawals" / Vec(CStruct()),  # assuming withdrawals contains a list of empty structures
    "requests" / Option(Vec(CStruct()))  # assuming requests contains an optional list of empty structures
)

# Final struct containing block and senders
FinalStruct = CStruct(
    "block" / Block,
    "senders" / Vec(Hex)
)

# Sample data: https://viewblock.io/arweave/tx/h3uakzDm_UFDczRDCVSdirFzXnk1-YC44QpU9G14D3k
sample_data = {
    "block": {
        "header": {
            "hash": "0xf32a0281236ece592fd4360393b4907c258ab401ffeb3d9c12c3575652173875",
            "header": {
                "parent_hash": "0xf08de3f5d08fbc69a92b36421f07f121c7eeca629d548c9d6be4f8da76ffa25c",
                "ommers_hash": "0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
                "beneficiary": "0x123463a4b065722e99115d6c222f267d9cabb524",
                "state_root": "0xeeec063dfa322eaf90ef24b34cd901bb471ef2082ed714df8f6db3a3cdcd19a2",
                "transactions_root": "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
                "receipts_root": "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
                "withdrawals_root": "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
                "logs_bloom": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                "difficulty": "0x0",
                "number": 1,
                "gas_limit": 30000000,
                "gas_used": 0,
                "timestamp": 1721242735,
                "mix_hash": "0xf08de3f5d08fbc69a92b36421f07f121c7eeca629d548c9d6be4f8da76ffa25c",
                "nonce": 0,
                "base_fee_per_gas": 875000000,
                "blob_gas_used": None,
                "excess_blob_gas": None,
                "parent_beacon_block_root": None,
                "requests_root": None,
                "extra_data": "0x726574682f76312e302e312f6c696e7578"
            }
        },
        "body": [],
        "ommers": [],
        "withdrawals": [],
        "requests": None
    },
    "senders": []
}

# Build the struct with the sample data
built_data = FinalStruct.build(sample_data)

# Parse the struct back to verify correctness
parsed_data = FinalStruct.parse(built_data)
#print(parsed_data)


# Calculate the lengths
length_built_data = len(built_data)

print(f"Original size: {len(built_data)}")

# zstd compression
compressed_zstd = pyzstd.compress(built_data)
print(f"zstd compressed size: {len(compressed_zstd)}")

# zlib compression
compressed_zlib = zlib.compress(built_data)
print(f"zlib compressed size: {len(compressed_zlib)}")

# Brotli compression
compressed_brotli = brotli.compress(built_data)
print(f"Brotli compressed size: {len(compressed_brotli)}")

# paq9a compression
compressed_paq = paq.compress(built_data)
print(f"PAQ compressed size: {len(compressed_paq)}")

# Snappy compression
compressed_snappy = snappy.compress(built_data)
print(f"Snappy compressed size: {len(compressed_snappy)}")

# Gzip compression
compressed_gzip = gzip.compress(built_data)
print(f"Gzip compressed size: {len(compressed_gzip)}")

# Bzip2 compression
compressed_bz2 = bz2.compress(built_data)
print(f"Bzip2 compressed size: {len(compressed_bz2)}")

# LZMA compression
compressed_lzma = lzma.compress(built_data)
print(f"LZMA compressed size: {len(compressed_lzma)}")

plt.style.use('dark_background')

# Set dark theme
plt.style.use('dark_background')

# Data
methods = ['Borsh-serialized\n(no compression)', 'zstd', 'zlib', 'Brotli', 'Bzip2', 'PAQ9A', 'Gzip', 'LZMA', 'Snappy']
sizes = [
    len(built_data),
    len(compressed_zstd),
    len(compressed_zlib),
    len(compressed_brotli),
    len(compressed_bz2),
    len(compressed_paq),
    len(compressed_gzip),
    len(compressed_lzma),
    len(compressed_snappy)
]

# Plot
plt.figure(figsize=(10, 6))
bars = plt.bar(methods, sizes, color='green')

# Annotate bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval}', ha='center', va='bottom', color='white')

plt.xlabel('Compression Algorithm', color='white')
plt.ylabel('Size (bytes)', color='white')
plt.title('WeaveVM empty block size after compression (Borsh serialized data)', color='white')
plt.yscale('log')
plt.xticks(color='white')
plt.yticks(color='white')
plt.savefig("./serialization_compression_benchmark/borsh_serialized/borsh_serialized.png")
plt.show()