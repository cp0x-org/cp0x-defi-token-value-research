| Token | Verdict | Reason | Sources |
|---|---|---|---|
| CAKE (BSC) | home chain, full supply | Ethereum CAKE is a mint/burn CakeOFT whose BSC peer locks BSC CAKE (about 10.05M held) | etherscan.io/token/0x152649eA73beAb28c5b49B26eb48f7EAD6d4c898 ; bscscan.com/address/0xb274202daBA6AE180c665B4fbE59857b7c3a8091 ; blog.pancakeswap.finance/articles/introducing-cake-token-bridging |
| GNS (Polygon) | multi-chain mint/burn | Native GainsNetworkToken with mint/burn roles on Arbitrum; vaults mint and burn GNS; Polygon about 4.6M vs Arbitrum about 16.8M | arbiscan.io/token/0x18c11FD286C5EC11c3b683Caa813B77f5163A122 ; docs.gains.trade/what-is-gains-network/gns-token |
| AERO (Base) | home chain, full supply | Only on Base, minted by the Aerodrome Minter; a unified multi-chain AERO is reported for late October 2026, after the sample | basescan.org/token/0x940181a94A35A4569E4529A3CDfB74e38FD98631 |
| XVS (BSC) | home chain, full supply | XVSProxyOFTSrc locks XVS on BNB Chain; destinations mint/burn | docs-v4.venus.io/technical-reference/reference-technical-articles/xvs-bridge |
| VELO (OP) | home chain, full supply | XVELO redeemable through a lockbox on OP; only the OP Minter mints VELO | github.com/velodrome-finance/superchain-contracts (SPECIFICATION.md, deployment-addresses/optimism.json) |
| WELL (Base) | multi-chain mint/burn | Address is xWELL (xERC20) minted on Base, Ethereum and OP; lockbox was on Moonbeam | moonwell-fi/moonwell-contracts-v2 src/xWELL/xWELL.sol |
| VELO, Velo Protocol (BSC) | not home chain | Native on Stellar; BSC is a wrapped version with fixed 30B totalSupply | coingecko.com/en/coins/velo |
| LISTA (BSC) | home chain, full supply | 1B minted once in constructor; Ethereum bridge is a LayerZero OFTAdapter (lock); 200M burn sent to a dead address still counts | lista-dao/lista-token contracts ListaToken.sol, ListaOFTAdapter.sol |
| THE (BSC) | home chain, full supply | CCIP directory: LockRelease pool on BNB Chain, BurnMint on opBNB and Polygon | docs.chain.link/ccip/directory/mainnet/token/THE |
| GEOD (Polygon) | home chain, full supply | Polygon totalSupply equals the 1B cap while about 274M GEOD exists on Solana via Wormhole NTT, which fits lock mode on Polygon (inferred from numbers) | docs.geodnet.com/geod-token/crosschain-between-polygon-and-solana |
