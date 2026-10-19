# SREB summary tables

Families with evidence: **136**. Generated from `data/evidence/` only.

## Outcomes per model

| Model | Proposed | Refuted | Preserved | No_rewrite | Unsupported | Error | Checks |
|---|---|---|---|---|---|---|---|
| deepseek-coder-v2:latest | 50 | 21 | 29 | 85 | 0 | 1 | 3808 |
| phi3.5:3.8b | 21 | 7 | 14 | 108 | 5 | 2 | 3808 |
| qwen2.5-coder:7b | 21 | 10 | 11 | 115 | 0 | 0 | 3808 |
| qwen2.5:7b | 21 | 7 | 14 | 114 | 0 | 1 | 3808 |

## Refuted families

| Family | Model | Refuting states |
|---|---|---|
| active_outer | deepseek-coder-v2:latest | fixed_0,no_loans_0,multiplicity_0,zero_fee_0,nullable_0,boundary_0,ties_0,random_uniform_0,random_uniform_1,random_uniform_2,random_uniform_3,random_uniform_4,random_uniform_5,random_uniform_6,random_uniform_7,random_uniform_8,random_uniform_9,random_uniform_10,random_uniform_12,random_uniform_13,random_uniform_14,random_uniform_15,random_uniform_16,random_uniform_17,random_uniform_18 |
| all_returned | qwen2.5-coder:7b | fixed_0,multiplicity_0,zero_fee_0,nullable_0,boundary_0,ties_0,random_uniform_0,random_uniform_1,random_uniform_2,random_uniform_4,random_uniform_5,random_uniform_6,random_uniform_7,random_uniform_8,random_uniform_10,random_uniform_11,random_uniform_12,random_uniform_13,random_uniform_14,random_uniform_16,random_uniform_17,random_uniform_18,random_uniform_19 |
| all_returned | qwen2.5:7b | fixed_0,multiplicity_0,zero_fee_0,nullable_0,boundary_0,random_uniform_0,random_uniform_7,random_uniform_10,random_uniform_12,random_uniform_18 |
| all_returned | deepseek-coder-v2:latest | multiplicity_0,zero_fee_0,ties_0,random_uniform_0,random_uniform_1,random_uniform_2,random_uniform_5,random_uniform_6,random_uniform_7,random_uniform_8,random_uniform_11,random_uniform_12,random_uniform_14,random_uniform_15,random_uniform_16,random_uniform_17,random_uniform_18,random_uniform_19 |
| lib_books_loaned_in | deepseek-coder-v2:latest | multiplicity_0,ties_0,random_uniform_0,random_uniform_1,random_uniform_2,random_uniform_5,random_uniform_6,random_uniform_8,random_uniform_11,random_uniform_12,random_uniform_13,random_uniform_14,random_uniform_16,random_uniform_17,random_uniform_18,random_uniform_19 |
| lib_books_loaned_in | phi3.5:3.8b | fixed_0,multiplicity_0,zero_fee_0,nullable_0,boundary_0,ties_0,random_uniform_0,random_uniform_1,random_uniform_2,random_uniform_4,random_uniform_5,random_uniform_6,random_uniform_7,random_uniform_8,random_uniform_9,random_uniform_10,random_uniform_11,random_uniform_12,random_uniform_13,random_uniform_14,random_uniform_15,random_uniform_16,random_uniform_17,random_uniform_18,random_uniform_19 |
| lib_books_loaned_in | qwen2.5-coder:7b | multiplicity_0,ties_0,random_uniform_0,random_uniform_1,random_uniform_2,random_uniform_5,random_uniform_6,random_uniform_8,random_uniform_11,random_uniform_12,random_uniform_13,random_uniform_14,random_uniform_16,random_uniform_17,random_uniform_18,random_uniform_19 |
| lib_books_never_loaned | phi3.5:3.8b | fixed_0,no_loans_0,boundary_0,random_uniform_0,random_uniform_2,random_uniform_3,random_uniform_4,random_uniform_7,random_uniform_9,random_uniform_10,random_uniform_12,random_uniform_13,random_uniform_15,random_uniform_16,random_uniform_18 |
| lib_books_price_open_range | qwen2.5-coder:7b | fixed_0,no_loans_0,multiplicity_0,zero_fee_0,nullable_0,boundary_0,ties_0,random_uniform_7,random_uniform_8,random_uniform_9,random_uniform_19 |
| lib_count_star_vs_col | deepseek-coder-v2:latest | nullable_0,ties_0,random_uniform_0,random_uniform_1,random_uniform_4,random_uniform_5,random_uniform_6,random_uniform_7,random_uniform_8,random_uniform_9,random_uniform_11,random_uniform_13,random_uniform_14,random_uniform_15,random_uniform_16,random_uniform_17,random_uniform_19 |
| lib_loans_count_by_day_order | deepseek-coder-v2:latest | fixed_0,multiplicity_0,zero_fee_0,nullable_0,boundary_0,ties_0,random_uniform_0,random_uniform_1,random_uniform_2,random_uniform_4,random_uniform_5,random_uniform_6,random_uniform_7,random_uniform_8,random_uniform_9,random_uniform_10,random_uniform_11,random_uniform_12,random_uniform_13,random_uniform_14,random_uniform_15,random_uniform_16,random_uniform_17,random_uniform_18,random_uniform_19 |
| lib_loans_fee_or_returned | deepseek-coder-v2:latest | fixed_0,multiplicity_0,zero_fee_0,boundary_0,random_uniform_0,random_uniform_1,random_uniform_2,random_uniform_4,random_uniform_5,random_uniform_6,random_uniform_8,random_uniform_10,random_uniform_11,random_uniform_12,random_uniform_13,random_uniform_14,random_uniform_16,random_uniform_17,random_uniform_18,random_uniform_19 |
| lib_loans_fee_zero_sum | deepseek-coder-v2:latest | fixed_0,multiplicity_0,zero_fee_0,nullable_0,boundary_0,ties_0,random_uniform_0,random_uniform_1,random_uniform_2,random_uniform_4,random_uniform_5,random_uniform_6,random_uniform_8,random_uniform_10,random_uniform_11,random_uniform_12,random_uniform_13,random_uniform_14,random_uniform_16,random_uniform_17,random_uniform_18,random_uniform_19 |
| lib_reader_all_null_returned | deepseek-coder-v2:latest | random_uniform_1,random_uniform_5,random_uniform_6,random_uniform_8,random_uniform_14,random_uniform_15,random_uniform_16,random_uniform_17,random_uniform_19 |
| lib_reader_book_titles | deepseek-coder-v2:latest | multiplicity_0,random_uniform_0,random_uniform_1,random_uniform_2,random_uniform_5,random_uniform_6,random_uniform_8,random_uniform_11,random_uniform_14,random_uniform_16,random_uniform_17,random_uniform_19 |
| lib_reader_derived_counts | phi3.5:3.8b | multiplicity_0,zero_fee_0,ties_0,random_uniform_0,random_uniform_1,random_uniform_2,random_uniform_5,random_uniform_6,random_uniform_7,random_uniform_8,random_uniform_11,random_uniform_12,random_uniform_14,random_uniform_15,random_uniform_16,random_uniform_17,random_uniform_18,random_uniform_19 |
| lib_reader_loan_count_scalar | qwen2.5:7b | fixed_0,no_loans_0,multiplicity_0,zero_fee_0,boundary_0,ties_0,random_uniform_2,random_uniform_3,random_uniform_4,random_uniform_7,random_uniform_9,random_uniform_10,random_uniform_12,random_uniform_13,random_uniform_15,random_uniform_16 |
| lib_readers_with_loans | deepseek-coder-v2:latest | multiplicity_0,zero_fee_0,ties_0,random_uniform_0,random_uniform_1,random_uniform_2,random_uniform_5,random_uniform_6,random_uniform_7,random_uniform_8,random_uniform_11,random_uniform_12,random_uniform_13,random_uniform_14,random_uniform_15,random_uniform_16,random_uniform_17,random_uniform_18,random_uniform_19 |
| lib_union_bag_books | deepseek-coder-v2:latest | multiplicity_0,nullable_0,ties_0,random_uniform_0,random_uniform_1,random_uniform_5,random_uniform_6,random_uniform_8,random_uniform_11,random_uniform_17,random_uniform_19 |
| lib_union_bag_books | phi3.5:3.8b | multiplicity_0,nullable_0,ties_0 |
| lib_union_bag_books | qwen2.5:7b | multiplicity_0,nullable_0,ties_0 |
| lib_union_bag_books | qwen2.5-coder:7b | multiplicity_0,nullable_0,ties_0 |
| lib_union_distinct_readers | phi3.5:3.8b | multiplicity_0,ties_0,random_uniform_0,random_uniform_1,random_uniform_5,random_uniform_6,random_uniform_11,random_uniform_13,random_uniform_17,random_uniform_18,random_uniform_19 |
| lib_union_distinct_readers | qwen2.5:7b | multiplicity_0,ties_0,random_uniform_0,random_uniform_1,random_uniform_5,random_uniform_6,random_uniform_11,random_uniform_13,random_uniform_17,random_uniform_18,random_uniform_19 |
| lib_union_distinct_readers | qwen2.5-coder:7b | multiplicity_0,ties_0,random_uniform_0,random_uniform_1,random_uniform_5,random_uniform_6,random_uniform_11,random_uniform_13,random_uniform_17,random_uniform_18,random_uniform_19 |
| returned_count | deepseek-coder-v2:latest | nullable_0,ties_0,random_uniform_4,random_uniform_9,random_uniform_13,random_uniform_17 |
| shop_category_self | deepseek-coder-v2:latest | fixed_0,no_rows_0,multiplicity_0,zero_value_0,nullable_0,boundary_0,ties_0,random_uniform_0,random_uniform_1,random_uniform_2,random_uniform_3,random_uniform_4,random_uniform_5,random_uniform_6,random_uniform_7,random_uniform_8,random_uniform_9,random_uniform_10,random_uniform_11,random_uniform_12,random_uniform_13,random_uniform_14,random_uniform_15,random_uniform_16,random_uniform_17,random_uniform_18,random_uniform_19 |
| shop_customers_with_orders | deepseek-coder-v2:latest | multiplicity_0,random_uniform_1,random_uniform_3,random_uniform_4,random_uniform_5,random_uniform_6,random_uniform_8,random_uniform_9,random_uniform_10,random_uniform_14,random_uniform_15,random_uniform_16,random_uniform_17 |
| shop_orders_channel_or | qwen2.5:7b | fixed_0,multiplicity_0,nullable_0,random_uniform_0,random_uniform_1,random_uniform_2,random_uniform_3,random_uniform_5,random_uniform_6,random_uniform_8,random_uniform_9,random_uniform_10,random_uniform_13,random_uniform_14,random_uniform_15,random_uniform_17 |
| shop_orders_null_channel_group | deepseek-coder-v2:latest | fixed_0,multiplicity_0,nullable_0,random_uniform_0,random_uniform_1,random_uniform_2,random_uniform_3,random_uniform_5,random_uniform_6,random_uniform_8,random_uniform_9,random_uniform_10,random_uniform_13,random_uniform_14,random_uniform_15,random_uniform_17 |
| shop_orders_zero_total | deepseek-coder-v2:latest | zero_value_0,boundary_0,random_uniform_6,random_uniform_9,random_uniform_11 |
| shop_orders_zero_total | qwen2.5-coder:7b | zero_value_0,boundary_0,random_uniform_6,random_uniform_9,random_uniform_11 |
| shop_payments_method_equal | deepseek-coder-v2:latest | fixed_0,multiplicity_0,nullable_0,boundary_0,ties_0,random_uniform_0,random_uniform_1,random_uniform_3,random_uniform_5,random_uniform_6,random_uniform_8,random_uniform_9,random_uniform_10,random_uniform_12,random_uniform_14,random_uniform_15,random_uniform_16,random_uniform_17,random_uniform_18 |
| shop_payments_zero_amount | deepseek-coder-v2:latest | fixed_0,boundary_0,random_uniform_6,random_uniform_9,random_uniform_11 |
| shop_products_ordered_in | deepseek-coder-v2:latest | fixed_0,multiplicity_0,random_uniform_0,random_uniform_1,random_uniform_3,random_uniform_4,random_uniform_5,random_uniform_6,random_uniform_8,random_uniform_9,random_uniform_10,random_uniform_11,random_uniform_14,random_uniform_15,random_uniform_16,random_uniform_17,random_uniform_18,random_uniform_19 |
| shop_products_ordered_in | qwen2.5-coder:7b | fixed_0,multiplicity_0,random_uniform_0,random_uniform_1,random_uniform_3,random_uniform_4,random_uniform_5,random_uniform_6,random_uniform_8,random_uniform_9,random_uniform_10,random_uniform_11,random_uniform_14,random_uniform_15,random_uniform_16,random_uniform_17,random_uniform_18,random_uniform_19 |
| shop_union_bag_items | deepseek-coder-v2:latest | fixed_0,multiplicity_0,nullable_0,random_uniform_0,random_uniform_1,random_uniform_3,random_uniform_4,random_uniform_5,random_uniform_6,random_uniform_8,random_uniform_9,random_uniform_10,random_uniform_11,random_uniform_12,random_uniform_13,random_uniform_14,random_uniform_15,random_uniform_16,random_uniform_17,random_uniform_18,random_uniform_19 |
| shop_union_bag_items | phi3.5:3.8b | nullable_0,random_uniform_0,random_uniform_1,random_uniform_3,random_uniform_4,random_uniform_5,random_uniform_6,random_uniform_8,random_uniform_9,random_uniform_10,random_uniform_11,random_uniform_12,random_uniform_13,random_uniform_14,random_uniform_15,random_uniform_16,random_uniform_17,random_uniform_18,random_uniform_19 |
| shop_union_distinct_customers | qwen2.5:7b | multiplicity_0,random_uniform_3,random_uniform_8,random_uniform_9,random_uniform_14,random_uniform_15,random_uniform_16,random_uniform_17 |
| shop_union_distinct_customers | qwen2.5-coder:7b | multiplicity_0,random_uniform_3,random_uniform_8,random_uniform_9,random_uniform_14,random_uniform_15,random_uniform_16,random_uniform_17 |
| union_bag | qwen2.5-coder:7b | multiplicity_0,nullable_0,ties_0 |
| union_bag | qwen2.5:7b | multiplicity_0,nullable_0,ties_0 |
| union_bag | phi3.5:3.8b | multiplicity_0,nullable_0,ties_0 |
| union_bag | deepseek-coder-v2:latest | multiplicity_0,nullable_0,ties_0,random_uniform_0,random_uniform_1,random_uniform_5,random_uniform_6,random_uniform_11,random_uniform_13,random_uniform_17,random_uniform_18,random_uniform_19 |
| zero_fee | qwen2.5-coder:7b | multiplicity_0,zero_fee_0,ties_0,random_uniform_1,random_uniform_7,random_uniform_11,random_uniform_14,random_uniform_18,random_uniform_19 |
