# SREB summary tables

Families: **12**. Generated from `data/evidence/` only.

## Outcomes per model

| Model | Proposed | Refuted | Preserved | No_rewrite | Unsupported | Error | Checks |
|---|---|---|---|---|---|---|---|
| phi3.5:3.8b | 2 | 1 | 1 | 10 | 0 | 0 | 336 |
| qwen2.5-coder:7b | 5 | 3 | 2 | 7 | 0 | 0 | 336 |
| qwen2.5:7b | 3 | 2 | 1 | 9 | 0 | 0 | 336 |

## Refuted families

| Family | Model | Refuting states |
|---|---|---|
| all_returned | qwen2.5-coder:7b | fixed_0,multiplicity_0,zero_fee_0,nullable_0,boundary_0,ties_0,random_uniform_0,random_uniform_1,random_uniform_2,random_uniform_4,random_uniform_5,random_uniform_6,random_uniform_7,random_uniform_8,random_uniform_10,random_uniform_11,random_uniform_12,random_uniform_13,random_uniform_14,random_uniform_16,random_uniform_17,random_uniform_18,random_uniform_19 |
| all_returned | qwen2.5:7b | fixed_0,multiplicity_0,zero_fee_0,nullable_0,boundary_0,random_uniform_0,random_uniform_7,random_uniform_10,random_uniform_12,random_uniform_18 |
| union_bag | qwen2.5-coder:7b | multiplicity_0,nullable_0,ties_0 |
| union_bag | qwen2.5:7b | multiplicity_0,nullable_0,ties_0 |
| union_bag | phi3.5:3.8b | multiplicity_0,nullable_0,ties_0 |
| zero_fee | qwen2.5-coder:7b | multiplicity_0,zero_fee_0,ties_0,random_uniform_1,random_uniform_7,random_uniform_11,random_uniform_14,random_uniform_18,random_uniform_19 |
