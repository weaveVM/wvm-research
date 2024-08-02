<p align="center">
  <a href="https://wvm.dev">
    <img src="https://raw.githubusercontent.com/weaveVM/.github/main/profile/bg.png">
  </a>
</p>

## About
This repository hosts the source code for scripts designed to generate informal and data analysis content utilized across WeaveVM platforms.

## Samples

### `impact_gas_limit`
![](./impact_block_gas_limit/impact_block_gas_limit.png)

### `json_serialized_da_cost_comparison`

This script provides an outline of the DA costs across various DA solutions. In this case study, we do not account for any data compression or utilize data serialization methods other than JSON for WeaveVM data on Arweave. As a result, the costs are approximately 2x higher than they could potentially be with these optimizations.

![](./json_serialized_da_cost_comparison/da_cost_comparison.png)

### `borsh_serialized_da_cost_comparison`

Here, we have recalculated the DA costs, achieving an approximate 50% reduction in data costs for settling data on Arweave by employing Borsh serialization.

![](./borsh_serialized_da_cost_comparison/da_cost_comparison.png)

### `borsh_vs_json_serialization`
This comparison shows that using [Borsh](https://github.com/near/borsh) serialization results in approximately a 26.6% reduction in data size compared to JSON serialization (~50% achieved in Rust Borsh). This reduction significantly lowers the Arweave fees incurred by WeaveVM for posting data on Arweave.

![](./borsh_vs_json_serialization/compare.png)

### `serialization_compression_benchmark`
In this section, we test various compression algorithms using two data serialization methods (JSON and Borsh) on an [empty WeaveVM block](https://q55zvezq436ucq3tgrbqsve5rkyxgxtzgx4ybohbbjkpi3lyb54q.arweave.net/h3uakzDm_UFDczRDCVSdirFzXnk1-YC44QpU9G14D3k).

![](./serialization_compression_benchmark/borsh_serialized/borsh_serialized.png)

![](./serialization_compression_benchmark/json_serialized/json_serialized.png)

### `borsh_gzip_wvm_cost`

![](./borsh_gzip_wvm_cost/borsh_gzip_wvm_cost.png)

### `borsh_brotli_wvm_cost: Testnet V0`

![](./borsh_brotli_wvm_cost/borsh_brotli_wvm_cost.png)

### `borsh_brotli_wvm_cost: Testnet V0.5`

![](./borsh_brotli_wvm_cost_testnet_v0.5/borsh_brotli_wvm_cost_testnet_v0.5.png)

## License
This repository is licensed under the [MIT License](./LICENSE)
