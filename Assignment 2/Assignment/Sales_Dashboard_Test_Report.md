# Sales Dashboard Test Report

**Program:** `Sales_Dashboard.py`  
**Test date:** November 9, 2026  
**Overall result:** PASS

## Summary

| Test group | Cases/checks | Result |
|---|---:|---|
| Custom pivot valid combinations | 4,431 | Passed |
| Grouped menu and invalid-input runs | 23 (26 prompt-level entries below) | Passed |
| Requirement and integration checks | 32 | Passed |
| **Total grouped checks** | **4,486** | **Passed** |

The custom-pivot combinations were generated and executed exhaustively on a
small test DataFrame with the same five categorical dimensions and three
available measures as the test fixture. Invalid textual input is unlimited, so
invalid inputs were tested by representative classes (blank, malformed,
out-of-range, duplicate, and conflicting selections) at each relevant prompt.

## R1: Loading sales data

| Test case | Input / setup | Expected behavior | Result |
|---|---|---|---|
| Load requested Google Drive CSV | Provided Drive download URL | Show loading indicator, success time, duration, rows, and columns | PASS |
| Confirm loaded data | Actual Drive response | 5,130 rows, required fields present, no null cells after fill | PASS |
| Read failure | `read_csv` raises `OSError("unavailable")` | Exit with a clear load error | PASS |
| Empty file | `read_csv` returns an empty DataFrame | Exit with a no-usable-data error | PASS |
| Missing analytics fields | DataFrame contains only `sales_region` | Warn that analytics may not work and identify missing fields | PASS |
| Numeric cleanup | Numeric fields contain `"bad"` or null values | Convert bad/missing numeric values to zero | PASS |

## R2: Command-line menu

The menu is a tuple of `(label, callable)` pairs. Each listed option was
selected by its menu number and returned the matching action.

| Test case | Input / setup | Expected behavior | Result |
|---|---|---|---|
| Menu structure | Inspect every menu tuple entry | Every entry has a label and callable action | PASS |
| Each menu choice | Every choice from 1 through 11 | Return the corresponding menu item | PASS |
| Invalid menu choices | `""`, `"abc"`, `"-1"`, `"0"`, one above the maximum, `"1.5"` | Reject and reprompt | PASS |
| Exit action | Select Exit | Terminate cleanly | PASS |
| Main startup | Mock a successful load and select Exit | Initialize and dispatch the Exit action | PASS |
| Keyboard interrupt | Interrupt the menu loop | Print an exit message | PASS |

The requested ten menu functions remain available. The additional
**Display all stored results** entry is option 10, so Exit is option 11.

## R3: Predefined reports and row preview

| Test case | Input / setup | Expected behavior | Result |
|---|---|---|---|
| Row preview: skip | Press Enter | Display no rows and do not prompt for export | PASS |
| Row preview: number | Enter a valid row count | Display only that many rows from the beginning | PASS |
| Row preview: all | Enter `"all"` / `"ALL"` | Display every row, including middle rows | PASS |
| Row preview: malformed | `"abc"`, `"1.5"` | Explain invalid input and reprompt | PASS |
| Row preview: out of range | `"0"`, `"-1"`, value greater than row count | Explain invalid number and reprompt | PASS |
| Total sales by region/order type | Run against valid fixture | Produce and store pivot with order types as columns | PASS |
| Average sales by region/state/order type | Run against valid fixture | Produce and store average sales pivot | PASS |
| Sales by customer/order/state | Run against valid fixture | Produce and store customer/order sub-row pivot | PASS |
| Quantity and sales by region/product | Run against valid fixture | Produce and store summed quantity and sales pivot | PASS |
| Quantity and sales by order/customer type | Run against valid fixture | Produce and store summed quantity and sales pivot | PASS |
| Min/max unit price by category | Run against valid fixture | Produce and store category pivot with min/max | PASS |
| Unique employees by region | Run against valid fixture | Produce and store pivot counting distinct employee IDs | PASS |
| Missing report columns | Run all seven reports with an empty DataFrame | Report missing fields without crashing | PASS |
| Stored results | Run all seven reports, then display stored results | All seven results are present and displayed | PASS |

All seven predefined reports were also executed against the live 5,130-row
Google Drive DataFrame.

## R4: Custom pivot combinations

The exhaustive fixture had five categorical dimensions:

- `employee_name`
- `sales_region`
- `product_category`
- `order_type`
- `customer_type`

It had three selectable measures: `quantity`, `unit_price`, and derived
`sale_price`. Every dimension was assigned to **row**, **column**, or **unused**;
assignments with no row field were excluded. For each remaining assignment,
every non-empty measure subset was combined with each aggregation function.

| Combination component | Count |
|---|---:|
| Valid row/column dimension assignments | 211 |
| Non-empty measure selections | 7 |
| Aggregations (`sum`, `mean`, `count`) | 3 |
| **Total valid custom pivot combinations** | **4,431** |
| Successful outputs and stored results | **4,431** |
| Failures | **0** |

Invalid interactive choices were also exercised at each custom-pivot stage:

| Stage | Invalid input classes exercised | Result |
|---|---|---|
| Rows (required) | Blank, text, zero, index above available fields | Rejected and reprompted |
| Columns (optional) | Text and index above available fields | Rejected and reprompted |
| Values (required) | Blank, text, zero, index above available values | Rejected and reprompted |
| Aggregation (single choice) | Multiple selections | Rejected until exactly one was selected |
| Custom pivot storage | Create two different custom pivots | Both retained under distinct names |

## Excel export

| Test case | Input / setup | Expected behavior | Result |
|---|---|---|---|
| Decline export | `"n"` | Return without writing a file | PASS |
| Invalid export confirmation | `"maybe"`, then `"yes"` | Explain valid yes/no input and reprompt | PASS |
| Blank filename | Press Enter | Reject and reprompt | PASS |
| Existing filename | Enter an existing `.xlsx` path | Refuse overwrite and reprompt | PASS |
| Missing extension | Enter a filename without `.xlsx` | Append `.xlsx` and write workbook | PASS |
| Workbook readability | Open generated workbook with `openpyxl` | Workbook and `Results` sheet are readable | PASS |
| Formula-like text | Export a string beginning with `=` | Store as text rather than a spreadsheet formula | PASS |
| Write failure | Enter a path under a nonexistent directory | Show an export error; do not claim success | PASS |

## Notes

- The 4,431 exhaustive pivot combinations use a compact fixture; the same
  report functions were separately run against the full Drive CSV.
- The test report records the executed finite input combinations and
  representative invalid-input equivalence classes. It does not claim to
  enumerate every arbitrary string a user could type.
- No persistent `unittest` test file was present in the assignment folder.
  The checks summarized here were executed using focused inline test scripts.
  Consequently, `unittest discover` found zero tests and exited with its
  standard "no tests ran" status; this is not counted as a passing test case.
- Excel export requires `openpyxl` in the active Python environment.

## Complete exhaustive custom-pivot test list

Each row below is one individual successful call to `generate_custom_pivot_table`. `-` means no column grouping. Dimensions not listed in Rows or Columns were unused for that case. The order follows the executed loops: dimension assignments, non-empty value subsets, then aggregation (`sum`, `mean`, `count`).

| Test ID | Rows | Columns | Values | Aggregation | Result |
|---|---|---|---|---|---|
| CP-0001 | employee_name, sales_region, product_category, order_type, customer_type | - | quantity | sum | PASS |
| CP-0002 | employee_name, sales_region, product_category, order_type, customer_type | - | quantity | mean | PASS |
| CP-0003 | employee_name, sales_region, product_category, order_type, customer_type | - | quantity | count | PASS |
| CP-0004 | employee_name, sales_region, product_category, order_type, customer_type | - | unit_price | sum | PASS |
| CP-0005 | employee_name, sales_region, product_category, order_type, customer_type | - | unit_price | mean | PASS |
| CP-0006 | employee_name, sales_region, product_category, order_type, customer_type | - | unit_price | count | PASS |
| CP-0007 | employee_name, sales_region, product_category, order_type, customer_type | - | quantity, unit_price | sum | PASS |
| CP-0008 | employee_name, sales_region, product_category, order_type, customer_type | - | quantity, unit_price | mean | PASS |
| CP-0009 | employee_name, sales_region, product_category, order_type, customer_type | - | quantity, unit_price | count | PASS |
| CP-0010 | employee_name, sales_region, product_category, order_type, customer_type | - | sale_price | sum | PASS |
| CP-0011 | employee_name, sales_region, product_category, order_type, customer_type | - | sale_price | mean | PASS |
| CP-0012 | employee_name, sales_region, product_category, order_type, customer_type | - | sale_price | count | PASS |
| CP-0013 | employee_name, sales_region, product_category, order_type, customer_type | - | quantity, sale_price | sum | PASS |
| CP-0014 | employee_name, sales_region, product_category, order_type, customer_type | - | quantity, sale_price | mean | PASS |
| CP-0015 | employee_name, sales_region, product_category, order_type, customer_type | - | quantity, sale_price | count | PASS |
| CP-0016 | employee_name, sales_region, product_category, order_type, customer_type | - | unit_price, sale_price | sum | PASS |
| CP-0017 | employee_name, sales_region, product_category, order_type, customer_type | - | unit_price, sale_price | mean | PASS |
| CP-0018 | employee_name, sales_region, product_category, order_type, customer_type | - | unit_price, sale_price | count | PASS |
| CP-0019 | employee_name, sales_region, product_category, order_type, customer_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-0020 | employee_name, sales_region, product_category, order_type, customer_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-0021 | employee_name, sales_region, product_category, order_type, customer_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-0022 | employee_name, sales_region, product_category, order_type | customer_type | quantity | sum | PASS |
| CP-0023 | employee_name, sales_region, product_category, order_type | customer_type | quantity | mean | PASS |
| CP-0024 | employee_name, sales_region, product_category, order_type | customer_type | quantity | count | PASS |
| CP-0025 | employee_name, sales_region, product_category, order_type | customer_type | unit_price | sum | PASS |
| CP-0026 | employee_name, sales_region, product_category, order_type | customer_type | unit_price | mean | PASS |
| CP-0027 | employee_name, sales_region, product_category, order_type | customer_type | unit_price | count | PASS |
| CP-0028 | employee_name, sales_region, product_category, order_type | customer_type | quantity, unit_price | sum | PASS |
| CP-0029 | employee_name, sales_region, product_category, order_type | customer_type | quantity, unit_price | mean | PASS |
| CP-0030 | employee_name, sales_region, product_category, order_type | customer_type | quantity, unit_price | count | PASS |
| CP-0031 | employee_name, sales_region, product_category, order_type | customer_type | sale_price | sum | PASS |
| CP-0032 | employee_name, sales_region, product_category, order_type | customer_type | sale_price | mean | PASS |
| CP-0033 | employee_name, sales_region, product_category, order_type | customer_type | sale_price | count | PASS |
| CP-0034 | employee_name, sales_region, product_category, order_type | customer_type | quantity, sale_price | sum | PASS |
| CP-0035 | employee_name, sales_region, product_category, order_type | customer_type | quantity, sale_price | mean | PASS |
| CP-0036 | employee_name, sales_region, product_category, order_type | customer_type | quantity, sale_price | count | PASS |
| CP-0037 | employee_name, sales_region, product_category, order_type | customer_type | unit_price, sale_price | sum | PASS |
| CP-0038 | employee_name, sales_region, product_category, order_type | customer_type | unit_price, sale_price | mean | PASS |
| CP-0039 | employee_name, sales_region, product_category, order_type | customer_type | unit_price, sale_price | count | PASS |
| CP-0040 | employee_name, sales_region, product_category, order_type | customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0041 | employee_name, sales_region, product_category, order_type | customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0042 | employee_name, sales_region, product_category, order_type | customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-0043 | employee_name, sales_region, product_category, order_type | - | quantity | sum | PASS |
| CP-0044 | employee_name, sales_region, product_category, order_type | - | quantity | mean | PASS |
| CP-0045 | employee_name, sales_region, product_category, order_type | - | quantity | count | PASS |
| CP-0046 | employee_name, sales_region, product_category, order_type | - | unit_price | sum | PASS |
| CP-0047 | employee_name, sales_region, product_category, order_type | - | unit_price | mean | PASS |
| CP-0048 | employee_name, sales_region, product_category, order_type | - | unit_price | count | PASS |
| CP-0049 | employee_name, sales_region, product_category, order_type | - | quantity, unit_price | sum | PASS |
| CP-0050 | employee_name, sales_region, product_category, order_type | - | quantity, unit_price | mean | PASS |
| CP-0051 | employee_name, sales_region, product_category, order_type | - | quantity, unit_price | count | PASS |
| CP-0052 | employee_name, sales_region, product_category, order_type | - | sale_price | sum | PASS |
| CP-0053 | employee_name, sales_region, product_category, order_type | - | sale_price | mean | PASS |
| CP-0054 | employee_name, sales_region, product_category, order_type | - | sale_price | count | PASS |
| CP-0055 | employee_name, sales_region, product_category, order_type | - | quantity, sale_price | sum | PASS |
| CP-0056 | employee_name, sales_region, product_category, order_type | - | quantity, sale_price | mean | PASS |
| CP-0057 | employee_name, sales_region, product_category, order_type | - | quantity, sale_price | count | PASS |
| CP-0058 | employee_name, sales_region, product_category, order_type | - | unit_price, sale_price | sum | PASS |
| CP-0059 | employee_name, sales_region, product_category, order_type | - | unit_price, sale_price | mean | PASS |
| CP-0060 | employee_name, sales_region, product_category, order_type | - | unit_price, sale_price | count | PASS |
| CP-0061 | employee_name, sales_region, product_category, order_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-0062 | employee_name, sales_region, product_category, order_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-0063 | employee_name, sales_region, product_category, order_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-0064 | employee_name, sales_region, product_category, customer_type | order_type | quantity | sum | PASS |
| CP-0065 | employee_name, sales_region, product_category, customer_type | order_type | quantity | mean | PASS |
| CP-0066 | employee_name, sales_region, product_category, customer_type | order_type | quantity | count | PASS |
| CP-0067 | employee_name, sales_region, product_category, customer_type | order_type | unit_price | sum | PASS |
| CP-0068 | employee_name, sales_region, product_category, customer_type | order_type | unit_price | mean | PASS |
| CP-0069 | employee_name, sales_region, product_category, customer_type | order_type | unit_price | count | PASS |
| CP-0070 | employee_name, sales_region, product_category, customer_type | order_type | quantity, unit_price | sum | PASS |
| CP-0071 | employee_name, sales_region, product_category, customer_type | order_type | quantity, unit_price | mean | PASS |
| CP-0072 | employee_name, sales_region, product_category, customer_type | order_type | quantity, unit_price | count | PASS |
| CP-0073 | employee_name, sales_region, product_category, customer_type | order_type | sale_price | sum | PASS |
| CP-0074 | employee_name, sales_region, product_category, customer_type | order_type | sale_price | mean | PASS |
| CP-0075 | employee_name, sales_region, product_category, customer_type | order_type | sale_price | count | PASS |
| CP-0076 | employee_name, sales_region, product_category, customer_type | order_type | quantity, sale_price | sum | PASS |
| CP-0077 | employee_name, sales_region, product_category, customer_type | order_type | quantity, sale_price | mean | PASS |
| CP-0078 | employee_name, sales_region, product_category, customer_type | order_type | quantity, sale_price | count | PASS |
| CP-0079 | employee_name, sales_region, product_category, customer_type | order_type | unit_price, sale_price | sum | PASS |
| CP-0080 | employee_name, sales_region, product_category, customer_type | order_type | unit_price, sale_price | mean | PASS |
| CP-0081 | employee_name, sales_region, product_category, customer_type | order_type | unit_price, sale_price | count | PASS |
| CP-0082 | employee_name, sales_region, product_category, customer_type | order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0083 | employee_name, sales_region, product_category, customer_type | order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0084 | employee_name, sales_region, product_category, customer_type | order_type | quantity, unit_price, sale_price | count | PASS |
| CP-0085 | employee_name, sales_region, product_category | order_type, customer_type | quantity | sum | PASS |
| CP-0086 | employee_name, sales_region, product_category | order_type, customer_type | quantity | mean | PASS |
| CP-0087 | employee_name, sales_region, product_category | order_type, customer_type | quantity | count | PASS |
| CP-0088 | employee_name, sales_region, product_category | order_type, customer_type | unit_price | sum | PASS |
| CP-0089 | employee_name, sales_region, product_category | order_type, customer_type | unit_price | mean | PASS |
| CP-0090 | employee_name, sales_region, product_category | order_type, customer_type | unit_price | count | PASS |
| CP-0091 | employee_name, sales_region, product_category | order_type, customer_type | quantity, unit_price | sum | PASS |
| CP-0092 | employee_name, sales_region, product_category | order_type, customer_type | quantity, unit_price | mean | PASS |
| CP-0093 | employee_name, sales_region, product_category | order_type, customer_type | quantity, unit_price | count | PASS |
| CP-0094 | employee_name, sales_region, product_category | order_type, customer_type | sale_price | sum | PASS |
| CP-0095 | employee_name, sales_region, product_category | order_type, customer_type | sale_price | mean | PASS |
| CP-0096 | employee_name, sales_region, product_category | order_type, customer_type | sale_price | count | PASS |
| CP-0097 | employee_name, sales_region, product_category | order_type, customer_type | quantity, sale_price | sum | PASS |
| CP-0098 | employee_name, sales_region, product_category | order_type, customer_type | quantity, sale_price | mean | PASS |
| CP-0099 | employee_name, sales_region, product_category | order_type, customer_type | quantity, sale_price | count | PASS |
| CP-0100 | employee_name, sales_region, product_category | order_type, customer_type | unit_price, sale_price | sum | PASS |
| CP-0101 | employee_name, sales_region, product_category | order_type, customer_type | unit_price, sale_price | mean | PASS |
| CP-0102 | employee_name, sales_region, product_category | order_type, customer_type | unit_price, sale_price | count | PASS |
| CP-0103 | employee_name, sales_region, product_category | order_type, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0104 | employee_name, sales_region, product_category | order_type, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0105 | employee_name, sales_region, product_category | order_type, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-0106 | employee_name, sales_region, product_category | order_type | quantity | sum | PASS |
| CP-0107 | employee_name, sales_region, product_category | order_type | quantity | mean | PASS |
| CP-0108 | employee_name, sales_region, product_category | order_type | quantity | count | PASS |
| CP-0109 | employee_name, sales_region, product_category | order_type | unit_price | sum | PASS |
| CP-0110 | employee_name, sales_region, product_category | order_type | unit_price | mean | PASS |
| CP-0111 | employee_name, sales_region, product_category | order_type | unit_price | count | PASS |
| CP-0112 | employee_name, sales_region, product_category | order_type | quantity, unit_price | sum | PASS |
| CP-0113 | employee_name, sales_region, product_category | order_type | quantity, unit_price | mean | PASS |
| CP-0114 | employee_name, sales_region, product_category | order_type | quantity, unit_price | count | PASS |
| CP-0115 | employee_name, sales_region, product_category | order_type | sale_price | sum | PASS |
| CP-0116 | employee_name, sales_region, product_category | order_type | sale_price | mean | PASS |
| CP-0117 | employee_name, sales_region, product_category | order_type | sale_price | count | PASS |
| CP-0118 | employee_name, sales_region, product_category | order_type | quantity, sale_price | sum | PASS |
| CP-0119 | employee_name, sales_region, product_category | order_type | quantity, sale_price | mean | PASS |
| CP-0120 | employee_name, sales_region, product_category | order_type | quantity, sale_price | count | PASS |
| CP-0121 | employee_name, sales_region, product_category | order_type | unit_price, sale_price | sum | PASS |
| CP-0122 | employee_name, sales_region, product_category | order_type | unit_price, sale_price | mean | PASS |
| CP-0123 | employee_name, sales_region, product_category | order_type | unit_price, sale_price | count | PASS |
| CP-0124 | employee_name, sales_region, product_category | order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0125 | employee_name, sales_region, product_category | order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0126 | employee_name, sales_region, product_category | order_type | quantity, unit_price, sale_price | count | PASS |
| CP-0127 | employee_name, sales_region, product_category, customer_type | - | quantity | sum | PASS |
| CP-0128 | employee_name, sales_region, product_category, customer_type | - | quantity | mean | PASS |
| CP-0129 | employee_name, sales_region, product_category, customer_type | - | quantity | count | PASS |
| CP-0130 | employee_name, sales_region, product_category, customer_type | - | unit_price | sum | PASS |
| CP-0131 | employee_name, sales_region, product_category, customer_type | - | unit_price | mean | PASS |
| CP-0132 | employee_name, sales_region, product_category, customer_type | - | unit_price | count | PASS |
| CP-0133 | employee_name, sales_region, product_category, customer_type | - | quantity, unit_price | sum | PASS |
| CP-0134 | employee_name, sales_region, product_category, customer_type | - | quantity, unit_price | mean | PASS |
| CP-0135 | employee_name, sales_region, product_category, customer_type | - | quantity, unit_price | count | PASS |
| CP-0136 | employee_name, sales_region, product_category, customer_type | - | sale_price | sum | PASS |
| CP-0137 | employee_name, sales_region, product_category, customer_type | - | sale_price | mean | PASS |
| CP-0138 | employee_name, sales_region, product_category, customer_type | - | sale_price | count | PASS |
| CP-0139 | employee_name, sales_region, product_category, customer_type | - | quantity, sale_price | sum | PASS |
| CP-0140 | employee_name, sales_region, product_category, customer_type | - | quantity, sale_price | mean | PASS |
| CP-0141 | employee_name, sales_region, product_category, customer_type | - | quantity, sale_price | count | PASS |
| CP-0142 | employee_name, sales_region, product_category, customer_type | - | unit_price, sale_price | sum | PASS |
| CP-0143 | employee_name, sales_region, product_category, customer_type | - | unit_price, sale_price | mean | PASS |
| CP-0144 | employee_name, sales_region, product_category, customer_type | - | unit_price, sale_price | count | PASS |
| CP-0145 | employee_name, sales_region, product_category, customer_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-0146 | employee_name, sales_region, product_category, customer_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-0147 | employee_name, sales_region, product_category, customer_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-0148 | employee_name, sales_region, product_category | customer_type | quantity | sum | PASS |
| CP-0149 | employee_name, sales_region, product_category | customer_type | quantity | mean | PASS |
| CP-0150 | employee_name, sales_region, product_category | customer_type | quantity | count | PASS |
| CP-0151 | employee_name, sales_region, product_category | customer_type | unit_price | sum | PASS |
| CP-0152 | employee_name, sales_region, product_category | customer_type | unit_price | mean | PASS |
| CP-0153 | employee_name, sales_region, product_category | customer_type | unit_price | count | PASS |
| CP-0154 | employee_name, sales_region, product_category | customer_type | quantity, unit_price | sum | PASS |
| CP-0155 | employee_name, sales_region, product_category | customer_type | quantity, unit_price | mean | PASS |
| CP-0156 | employee_name, sales_region, product_category | customer_type | quantity, unit_price | count | PASS |
| CP-0157 | employee_name, sales_region, product_category | customer_type | sale_price | sum | PASS |
| CP-0158 | employee_name, sales_region, product_category | customer_type | sale_price | mean | PASS |
| CP-0159 | employee_name, sales_region, product_category | customer_type | sale_price | count | PASS |
| CP-0160 | employee_name, sales_region, product_category | customer_type | quantity, sale_price | sum | PASS |
| CP-0161 | employee_name, sales_region, product_category | customer_type | quantity, sale_price | mean | PASS |
| CP-0162 | employee_name, sales_region, product_category | customer_type | quantity, sale_price | count | PASS |
| CP-0163 | employee_name, sales_region, product_category | customer_type | unit_price, sale_price | sum | PASS |
| CP-0164 | employee_name, sales_region, product_category | customer_type | unit_price, sale_price | mean | PASS |
| CP-0165 | employee_name, sales_region, product_category | customer_type | unit_price, sale_price | count | PASS |
| CP-0166 | employee_name, sales_region, product_category | customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0167 | employee_name, sales_region, product_category | customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0168 | employee_name, sales_region, product_category | customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-0169 | employee_name, sales_region, product_category | - | quantity | sum | PASS |
| CP-0170 | employee_name, sales_region, product_category | - | quantity | mean | PASS |
| CP-0171 | employee_name, sales_region, product_category | - | quantity | count | PASS |
| CP-0172 | employee_name, sales_region, product_category | - | unit_price | sum | PASS |
| CP-0173 | employee_name, sales_region, product_category | - | unit_price | mean | PASS |
| CP-0174 | employee_name, sales_region, product_category | - | unit_price | count | PASS |
| CP-0175 | employee_name, sales_region, product_category | - | quantity, unit_price | sum | PASS |
| CP-0176 | employee_name, sales_region, product_category | - | quantity, unit_price | mean | PASS |
| CP-0177 | employee_name, sales_region, product_category | - | quantity, unit_price | count | PASS |
| CP-0178 | employee_name, sales_region, product_category | - | sale_price | sum | PASS |
| CP-0179 | employee_name, sales_region, product_category | - | sale_price | mean | PASS |
| CP-0180 | employee_name, sales_region, product_category | - | sale_price | count | PASS |
| CP-0181 | employee_name, sales_region, product_category | - | quantity, sale_price | sum | PASS |
| CP-0182 | employee_name, sales_region, product_category | - | quantity, sale_price | mean | PASS |
| CP-0183 | employee_name, sales_region, product_category | - | quantity, sale_price | count | PASS |
| CP-0184 | employee_name, sales_region, product_category | - | unit_price, sale_price | sum | PASS |
| CP-0185 | employee_name, sales_region, product_category | - | unit_price, sale_price | mean | PASS |
| CP-0186 | employee_name, sales_region, product_category | - | unit_price, sale_price | count | PASS |
| CP-0187 | employee_name, sales_region, product_category | - | quantity, unit_price, sale_price | sum | PASS |
| CP-0188 | employee_name, sales_region, product_category | - | quantity, unit_price, sale_price | mean | PASS |
| CP-0189 | employee_name, sales_region, product_category | - | quantity, unit_price, sale_price | count | PASS |
| CP-0190 | employee_name, sales_region, order_type, customer_type | product_category | quantity | sum | PASS |
| CP-0191 | employee_name, sales_region, order_type, customer_type | product_category | quantity | mean | PASS |
| CP-0192 | employee_name, sales_region, order_type, customer_type | product_category | quantity | count | PASS |
| CP-0193 | employee_name, sales_region, order_type, customer_type | product_category | unit_price | sum | PASS |
| CP-0194 | employee_name, sales_region, order_type, customer_type | product_category | unit_price | mean | PASS |
| CP-0195 | employee_name, sales_region, order_type, customer_type | product_category | unit_price | count | PASS |
| CP-0196 | employee_name, sales_region, order_type, customer_type | product_category | quantity, unit_price | sum | PASS |
| CP-0197 | employee_name, sales_region, order_type, customer_type | product_category | quantity, unit_price | mean | PASS |
| CP-0198 | employee_name, sales_region, order_type, customer_type | product_category | quantity, unit_price | count | PASS |
| CP-0199 | employee_name, sales_region, order_type, customer_type | product_category | sale_price | sum | PASS |
| CP-0200 | employee_name, sales_region, order_type, customer_type | product_category | sale_price | mean | PASS |
| CP-0201 | employee_name, sales_region, order_type, customer_type | product_category | sale_price | count | PASS |
| CP-0202 | employee_name, sales_region, order_type, customer_type | product_category | quantity, sale_price | sum | PASS |
| CP-0203 | employee_name, sales_region, order_type, customer_type | product_category | quantity, sale_price | mean | PASS |
| CP-0204 | employee_name, sales_region, order_type, customer_type | product_category | quantity, sale_price | count | PASS |
| CP-0205 | employee_name, sales_region, order_type, customer_type | product_category | unit_price, sale_price | sum | PASS |
| CP-0206 | employee_name, sales_region, order_type, customer_type | product_category | unit_price, sale_price | mean | PASS |
| CP-0207 | employee_name, sales_region, order_type, customer_type | product_category | unit_price, sale_price | count | PASS |
| CP-0208 | employee_name, sales_region, order_type, customer_type | product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-0209 | employee_name, sales_region, order_type, customer_type | product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-0210 | employee_name, sales_region, order_type, customer_type | product_category | quantity, unit_price, sale_price | count | PASS |
| CP-0211 | employee_name, sales_region, order_type | product_category, customer_type | quantity | sum | PASS |
| CP-0212 | employee_name, sales_region, order_type | product_category, customer_type | quantity | mean | PASS |
| CP-0213 | employee_name, sales_region, order_type | product_category, customer_type | quantity | count | PASS |
| CP-0214 | employee_name, sales_region, order_type | product_category, customer_type | unit_price | sum | PASS |
| CP-0215 | employee_name, sales_region, order_type | product_category, customer_type | unit_price | mean | PASS |
| CP-0216 | employee_name, sales_region, order_type | product_category, customer_type | unit_price | count | PASS |
| CP-0217 | employee_name, sales_region, order_type | product_category, customer_type | quantity, unit_price | sum | PASS |
| CP-0218 | employee_name, sales_region, order_type | product_category, customer_type | quantity, unit_price | mean | PASS |
| CP-0219 | employee_name, sales_region, order_type | product_category, customer_type | quantity, unit_price | count | PASS |
| CP-0220 | employee_name, sales_region, order_type | product_category, customer_type | sale_price | sum | PASS |
| CP-0221 | employee_name, sales_region, order_type | product_category, customer_type | sale_price | mean | PASS |
| CP-0222 | employee_name, sales_region, order_type | product_category, customer_type | sale_price | count | PASS |
| CP-0223 | employee_name, sales_region, order_type | product_category, customer_type | quantity, sale_price | sum | PASS |
| CP-0224 | employee_name, sales_region, order_type | product_category, customer_type | quantity, sale_price | mean | PASS |
| CP-0225 | employee_name, sales_region, order_type | product_category, customer_type | quantity, sale_price | count | PASS |
| CP-0226 | employee_name, sales_region, order_type | product_category, customer_type | unit_price, sale_price | sum | PASS |
| CP-0227 | employee_name, sales_region, order_type | product_category, customer_type | unit_price, sale_price | mean | PASS |
| CP-0228 | employee_name, sales_region, order_type | product_category, customer_type | unit_price, sale_price | count | PASS |
| CP-0229 | employee_name, sales_region, order_type | product_category, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0230 | employee_name, sales_region, order_type | product_category, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0231 | employee_name, sales_region, order_type | product_category, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-0232 | employee_name, sales_region, order_type | product_category | quantity | sum | PASS |
| CP-0233 | employee_name, sales_region, order_type | product_category | quantity | mean | PASS |
| CP-0234 | employee_name, sales_region, order_type | product_category | quantity | count | PASS |
| CP-0235 | employee_name, sales_region, order_type | product_category | unit_price | sum | PASS |
| CP-0236 | employee_name, sales_region, order_type | product_category | unit_price | mean | PASS |
| CP-0237 | employee_name, sales_region, order_type | product_category | unit_price | count | PASS |
| CP-0238 | employee_name, sales_region, order_type | product_category | quantity, unit_price | sum | PASS |
| CP-0239 | employee_name, sales_region, order_type | product_category | quantity, unit_price | mean | PASS |
| CP-0240 | employee_name, sales_region, order_type | product_category | quantity, unit_price | count | PASS |
| CP-0241 | employee_name, sales_region, order_type | product_category | sale_price | sum | PASS |
| CP-0242 | employee_name, sales_region, order_type | product_category | sale_price | mean | PASS |
| CP-0243 | employee_name, sales_region, order_type | product_category | sale_price | count | PASS |
| CP-0244 | employee_name, sales_region, order_type | product_category | quantity, sale_price | sum | PASS |
| CP-0245 | employee_name, sales_region, order_type | product_category | quantity, sale_price | mean | PASS |
| CP-0246 | employee_name, sales_region, order_type | product_category | quantity, sale_price | count | PASS |
| CP-0247 | employee_name, sales_region, order_type | product_category | unit_price, sale_price | sum | PASS |
| CP-0248 | employee_name, sales_region, order_type | product_category | unit_price, sale_price | mean | PASS |
| CP-0249 | employee_name, sales_region, order_type | product_category | unit_price, sale_price | count | PASS |
| CP-0250 | employee_name, sales_region, order_type | product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-0251 | employee_name, sales_region, order_type | product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-0252 | employee_name, sales_region, order_type | product_category | quantity, unit_price, sale_price | count | PASS |
| CP-0253 | employee_name, sales_region, customer_type | product_category, order_type | quantity | sum | PASS |
| CP-0254 | employee_name, sales_region, customer_type | product_category, order_type | quantity | mean | PASS |
| CP-0255 | employee_name, sales_region, customer_type | product_category, order_type | quantity | count | PASS |
| CP-0256 | employee_name, sales_region, customer_type | product_category, order_type | unit_price | sum | PASS |
| CP-0257 | employee_name, sales_region, customer_type | product_category, order_type | unit_price | mean | PASS |
| CP-0258 | employee_name, sales_region, customer_type | product_category, order_type | unit_price | count | PASS |
| CP-0259 | employee_name, sales_region, customer_type | product_category, order_type | quantity, unit_price | sum | PASS |
| CP-0260 | employee_name, sales_region, customer_type | product_category, order_type | quantity, unit_price | mean | PASS |
| CP-0261 | employee_name, sales_region, customer_type | product_category, order_type | quantity, unit_price | count | PASS |
| CP-0262 | employee_name, sales_region, customer_type | product_category, order_type | sale_price | sum | PASS |
| CP-0263 | employee_name, sales_region, customer_type | product_category, order_type | sale_price | mean | PASS |
| CP-0264 | employee_name, sales_region, customer_type | product_category, order_type | sale_price | count | PASS |
| CP-0265 | employee_name, sales_region, customer_type | product_category, order_type | quantity, sale_price | sum | PASS |
| CP-0266 | employee_name, sales_region, customer_type | product_category, order_type | quantity, sale_price | mean | PASS |
| CP-0267 | employee_name, sales_region, customer_type | product_category, order_type | quantity, sale_price | count | PASS |
| CP-0268 | employee_name, sales_region, customer_type | product_category, order_type | unit_price, sale_price | sum | PASS |
| CP-0269 | employee_name, sales_region, customer_type | product_category, order_type | unit_price, sale_price | mean | PASS |
| CP-0270 | employee_name, sales_region, customer_type | product_category, order_type | unit_price, sale_price | count | PASS |
| CP-0271 | employee_name, sales_region, customer_type | product_category, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0272 | employee_name, sales_region, customer_type | product_category, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0273 | employee_name, sales_region, customer_type | product_category, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-0274 | employee_name, sales_region | product_category, order_type, customer_type | quantity | sum | PASS |
| CP-0275 | employee_name, sales_region | product_category, order_type, customer_type | quantity | mean | PASS |
| CP-0276 | employee_name, sales_region | product_category, order_type, customer_type | quantity | count | PASS |
| CP-0277 | employee_name, sales_region | product_category, order_type, customer_type | unit_price | sum | PASS |
| CP-0278 | employee_name, sales_region | product_category, order_type, customer_type | unit_price | mean | PASS |
| CP-0279 | employee_name, sales_region | product_category, order_type, customer_type | unit_price | count | PASS |
| CP-0280 | employee_name, sales_region | product_category, order_type, customer_type | quantity, unit_price | sum | PASS |
| CP-0281 | employee_name, sales_region | product_category, order_type, customer_type | quantity, unit_price | mean | PASS |
| CP-0282 | employee_name, sales_region | product_category, order_type, customer_type | quantity, unit_price | count | PASS |
| CP-0283 | employee_name, sales_region | product_category, order_type, customer_type | sale_price | sum | PASS |
| CP-0284 | employee_name, sales_region | product_category, order_type, customer_type | sale_price | mean | PASS |
| CP-0285 | employee_name, sales_region | product_category, order_type, customer_type | sale_price | count | PASS |
| CP-0286 | employee_name, sales_region | product_category, order_type, customer_type | quantity, sale_price | sum | PASS |
| CP-0287 | employee_name, sales_region | product_category, order_type, customer_type | quantity, sale_price | mean | PASS |
| CP-0288 | employee_name, sales_region | product_category, order_type, customer_type | quantity, sale_price | count | PASS |
| CP-0289 | employee_name, sales_region | product_category, order_type, customer_type | unit_price, sale_price | sum | PASS |
| CP-0290 | employee_name, sales_region | product_category, order_type, customer_type | unit_price, sale_price | mean | PASS |
| CP-0291 | employee_name, sales_region | product_category, order_type, customer_type | unit_price, sale_price | count | PASS |
| CP-0292 | employee_name, sales_region | product_category, order_type, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0293 | employee_name, sales_region | product_category, order_type, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0294 | employee_name, sales_region | product_category, order_type, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-0295 | employee_name, sales_region | product_category, order_type | quantity | sum | PASS |
| CP-0296 | employee_name, sales_region | product_category, order_type | quantity | mean | PASS |
| CP-0297 | employee_name, sales_region | product_category, order_type | quantity | count | PASS |
| CP-0298 | employee_name, sales_region | product_category, order_type | unit_price | sum | PASS |
| CP-0299 | employee_name, sales_region | product_category, order_type | unit_price | mean | PASS |
| CP-0300 | employee_name, sales_region | product_category, order_type | unit_price | count | PASS |
| CP-0301 | employee_name, sales_region | product_category, order_type | quantity, unit_price | sum | PASS |
| CP-0302 | employee_name, sales_region | product_category, order_type | quantity, unit_price | mean | PASS |
| CP-0303 | employee_name, sales_region | product_category, order_type | quantity, unit_price | count | PASS |
| CP-0304 | employee_name, sales_region | product_category, order_type | sale_price | sum | PASS |
| CP-0305 | employee_name, sales_region | product_category, order_type | sale_price | mean | PASS |
| CP-0306 | employee_name, sales_region | product_category, order_type | sale_price | count | PASS |
| CP-0307 | employee_name, sales_region | product_category, order_type | quantity, sale_price | sum | PASS |
| CP-0308 | employee_name, sales_region | product_category, order_type | quantity, sale_price | mean | PASS |
| CP-0309 | employee_name, sales_region | product_category, order_type | quantity, sale_price | count | PASS |
| CP-0310 | employee_name, sales_region | product_category, order_type | unit_price, sale_price | sum | PASS |
| CP-0311 | employee_name, sales_region | product_category, order_type | unit_price, sale_price | mean | PASS |
| CP-0312 | employee_name, sales_region | product_category, order_type | unit_price, sale_price | count | PASS |
| CP-0313 | employee_name, sales_region | product_category, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0314 | employee_name, sales_region | product_category, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0315 | employee_name, sales_region | product_category, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-0316 | employee_name, sales_region, customer_type | product_category | quantity | sum | PASS |
| CP-0317 | employee_name, sales_region, customer_type | product_category | quantity | mean | PASS |
| CP-0318 | employee_name, sales_region, customer_type | product_category | quantity | count | PASS |
| CP-0319 | employee_name, sales_region, customer_type | product_category | unit_price | sum | PASS |
| CP-0320 | employee_name, sales_region, customer_type | product_category | unit_price | mean | PASS |
| CP-0321 | employee_name, sales_region, customer_type | product_category | unit_price | count | PASS |
| CP-0322 | employee_name, sales_region, customer_type | product_category | quantity, unit_price | sum | PASS |
| CP-0323 | employee_name, sales_region, customer_type | product_category | quantity, unit_price | mean | PASS |
| CP-0324 | employee_name, sales_region, customer_type | product_category | quantity, unit_price | count | PASS |
| CP-0325 | employee_name, sales_region, customer_type | product_category | sale_price | sum | PASS |
| CP-0326 | employee_name, sales_region, customer_type | product_category | sale_price | mean | PASS |
| CP-0327 | employee_name, sales_region, customer_type | product_category | sale_price | count | PASS |
| CP-0328 | employee_name, sales_region, customer_type | product_category | quantity, sale_price | sum | PASS |
| CP-0329 | employee_name, sales_region, customer_type | product_category | quantity, sale_price | mean | PASS |
| CP-0330 | employee_name, sales_region, customer_type | product_category | quantity, sale_price | count | PASS |
| CP-0331 | employee_name, sales_region, customer_type | product_category | unit_price, sale_price | sum | PASS |
| CP-0332 | employee_name, sales_region, customer_type | product_category | unit_price, sale_price | mean | PASS |
| CP-0333 | employee_name, sales_region, customer_type | product_category | unit_price, sale_price | count | PASS |
| CP-0334 | employee_name, sales_region, customer_type | product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-0335 | employee_name, sales_region, customer_type | product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-0336 | employee_name, sales_region, customer_type | product_category | quantity, unit_price, sale_price | count | PASS |
| CP-0337 | employee_name, sales_region | product_category, customer_type | quantity | sum | PASS |
| CP-0338 | employee_name, sales_region | product_category, customer_type | quantity | mean | PASS |
| CP-0339 | employee_name, sales_region | product_category, customer_type | quantity | count | PASS |
| CP-0340 | employee_name, sales_region | product_category, customer_type | unit_price | sum | PASS |
| CP-0341 | employee_name, sales_region | product_category, customer_type | unit_price | mean | PASS |
| CP-0342 | employee_name, sales_region | product_category, customer_type | unit_price | count | PASS |
| CP-0343 | employee_name, sales_region | product_category, customer_type | quantity, unit_price | sum | PASS |
| CP-0344 | employee_name, sales_region | product_category, customer_type | quantity, unit_price | mean | PASS |
| CP-0345 | employee_name, sales_region | product_category, customer_type | quantity, unit_price | count | PASS |
| CP-0346 | employee_name, sales_region | product_category, customer_type | sale_price | sum | PASS |
| CP-0347 | employee_name, sales_region | product_category, customer_type | sale_price | mean | PASS |
| CP-0348 | employee_name, sales_region | product_category, customer_type | sale_price | count | PASS |
| CP-0349 | employee_name, sales_region | product_category, customer_type | quantity, sale_price | sum | PASS |
| CP-0350 | employee_name, sales_region | product_category, customer_type | quantity, sale_price | mean | PASS |
| CP-0351 | employee_name, sales_region | product_category, customer_type | quantity, sale_price | count | PASS |
| CP-0352 | employee_name, sales_region | product_category, customer_type | unit_price, sale_price | sum | PASS |
| CP-0353 | employee_name, sales_region | product_category, customer_type | unit_price, sale_price | mean | PASS |
| CP-0354 | employee_name, sales_region | product_category, customer_type | unit_price, sale_price | count | PASS |
| CP-0355 | employee_name, sales_region | product_category, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0356 | employee_name, sales_region | product_category, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0357 | employee_name, sales_region | product_category, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-0358 | employee_name, sales_region | product_category | quantity | sum | PASS |
| CP-0359 | employee_name, sales_region | product_category | quantity | mean | PASS |
| CP-0360 | employee_name, sales_region | product_category | quantity | count | PASS |
| CP-0361 | employee_name, sales_region | product_category | unit_price | sum | PASS |
| CP-0362 | employee_name, sales_region | product_category | unit_price | mean | PASS |
| CP-0363 | employee_name, sales_region | product_category | unit_price | count | PASS |
| CP-0364 | employee_name, sales_region | product_category | quantity, unit_price | sum | PASS |
| CP-0365 | employee_name, sales_region | product_category | quantity, unit_price | mean | PASS |
| CP-0366 | employee_name, sales_region | product_category | quantity, unit_price | count | PASS |
| CP-0367 | employee_name, sales_region | product_category | sale_price | sum | PASS |
| CP-0368 | employee_name, sales_region | product_category | sale_price | mean | PASS |
| CP-0369 | employee_name, sales_region | product_category | sale_price | count | PASS |
| CP-0370 | employee_name, sales_region | product_category | quantity, sale_price | sum | PASS |
| CP-0371 | employee_name, sales_region | product_category | quantity, sale_price | mean | PASS |
| CP-0372 | employee_name, sales_region | product_category | quantity, sale_price | count | PASS |
| CP-0373 | employee_name, sales_region | product_category | unit_price, sale_price | sum | PASS |
| CP-0374 | employee_name, sales_region | product_category | unit_price, sale_price | mean | PASS |
| CP-0375 | employee_name, sales_region | product_category | unit_price, sale_price | count | PASS |
| CP-0376 | employee_name, sales_region | product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-0377 | employee_name, sales_region | product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-0378 | employee_name, sales_region | product_category | quantity, unit_price, sale_price | count | PASS |
| CP-0379 | employee_name, sales_region, order_type, customer_type | - | quantity | sum | PASS |
| CP-0380 | employee_name, sales_region, order_type, customer_type | - | quantity | mean | PASS |
| CP-0381 | employee_name, sales_region, order_type, customer_type | - | quantity | count | PASS |
| CP-0382 | employee_name, sales_region, order_type, customer_type | - | unit_price | sum | PASS |
| CP-0383 | employee_name, sales_region, order_type, customer_type | - | unit_price | mean | PASS |
| CP-0384 | employee_name, sales_region, order_type, customer_type | - | unit_price | count | PASS |
| CP-0385 | employee_name, sales_region, order_type, customer_type | - | quantity, unit_price | sum | PASS |
| CP-0386 | employee_name, sales_region, order_type, customer_type | - | quantity, unit_price | mean | PASS |
| CP-0387 | employee_name, sales_region, order_type, customer_type | - | quantity, unit_price | count | PASS |
| CP-0388 | employee_name, sales_region, order_type, customer_type | - | sale_price | sum | PASS |
| CP-0389 | employee_name, sales_region, order_type, customer_type | - | sale_price | mean | PASS |
| CP-0390 | employee_name, sales_region, order_type, customer_type | - | sale_price | count | PASS |
| CP-0391 | employee_name, sales_region, order_type, customer_type | - | quantity, sale_price | sum | PASS |
| CP-0392 | employee_name, sales_region, order_type, customer_type | - | quantity, sale_price | mean | PASS |
| CP-0393 | employee_name, sales_region, order_type, customer_type | - | quantity, sale_price | count | PASS |
| CP-0394 | employee_name, sales_region, order_type, customer_type | - | unit_price, sale_price | sum | PASS |
| CP-0395 | employee_name, sales_region, order_type, customer_type | - | unit_price, sale_price | mean | PASS |
| CP-0396 | employee_name, sales_region, order_type, customer_type | - | unit_price, sale_price | count | PASS |
| CP-0397 | employee_name, sales_region, order_type, customer_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-0398 | employee_name, sales_region, order_type, customer_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-0399 | employee_name, sales_region, order_type, customer_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-0400 | employee_name, sales_region, order_type | customer_type | quantity | sum | PASS |
| CP-0401 | employee_name, sales_region, order_type | customer_type | quantity | mean | PASS |
| CP-0402 | employee_name, sales_region, order_type | customer_type | quantity | count | PASS |
| CP-0403 | employee_name, sales_region, order_type | customer_type | unit_price | sum | PASS |
| CP-0404 | employee_name, sales_region, order_type | customer_type | unit_price | mean | PASS |
| CP-0405 | employee_name, sales_region, order_type | customer_type | unit_price | count | PASS |
| CP-0406 | employee_name, sales_region, order_type | customer_type | quantity, unit_price | sum | PASS |
| CP-0407 | employee_name, sales_region, order_type | customer_type | quantity, unit_price | mean | PASS |
| CP-0408 | employee_name, sales_region, order_type | customer_type | quantity, unit_price | count | PASS |
| CP-0409 | employee_name, sales_region, order_type | customer_type | sale_price | sum | PASS |
| CP-0410 | employee_name, sales_region, order_type | customer_type | sale_price | mean | PASS |
| CP-0411 | employee_name, sales_region, order_type | customer_type | sale_price | count | PASS |
| CP-0412 | employee_name, sales_region, order_type | customer_type | quantity, sale_price | sum | PASS |
| CP-0413 | employee_name, sales_region, order_type | customer_type | quantity, sale_price | mean | PASS |
| CP-0414 | employee_name, sales_region, order_type | customer_type | quantity, sale_price | count | PASS |
| CP-0415 | employee_name, sales_region, order_type | customer_type | unit_price, sale_price | sum | PASS |
| CP-0416 | employee_name, sales_region, order_type | customer_type | unit_price, sale_price | mean | PASS |
| CP-0417 | employee_name, sales_region, order_type | customer_type | unit_price, sale_price | count | PASS |
| CP-0418 | employee_name, sales_region, order_type | customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0419 | employee_name, sales_region, order_type | customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0420 | employee_name, sales_region, order_type | customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-0421 | employee_name, sales_region, order_type | - | quantity | sum | PASS |
| CP-0422 | employee_name, sales_region, order_type | - | quantity | mean | PASS |
| CP-0423 | employee_name, sales_region, order_type | - | quantity | count | PASS |
| CP-0424 | employee_name, sales_region, order_type | - | unit_price | sum | PASS |
| CP-0425 | employee_name, sales_region, order_type | - | unit_price | mean | PASS |
| CP-0426 | employee_name, sales_region, order_type | - | unit_price | count | PASS |
| CP-0427 | employee_name, sales_region, order_type | - | quantity, unit_price | sum | PASS |
| CP-0428 | employee_name, sales_region, order_type | - | quantity, unit_price | mean | PASS |
| CP-0429 | employee_name, sales_region, order_type | - | quantity, unit_price | count | PASS |
| CP-0430 | employee_name, sales_region, order_type | - | sale_price | sum | PASS |
| CP-0431 | employee_name, sales_region, order_type | - | sale_price | mean | PASS |
| CP-0432 | employee_name, sales_region, order_type | - | sale_price | count | PASS |
| CP-0433 | employee_name, sales_region, order_type | - | quantity, sale_price | sum | PASS |
| CP-0434 | employee_name, sales_region, order_type | - | quantity, sale_price | mean | PASS |
| CP-0435 | employee_name, sales_region, order_type | - | quantity, sale_price | count | PASS |
| CP-0436 | employee_name, sales_region, order_type | - | unit_price, sale_price | sum | PASS |
| CP-0437 | employee_name, sales_region, order_type | - | unit_price, sale_price | mean | PASS |
| CP-0438 | employee_name, sales_region, order_type | - | unit_price, sale_price | count | PASS |
| CP-0439 | employee_name, sales_region, order_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-0440 | employee_name, sales_region, order_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-0441 | employee_name, sales_region, order_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-0442 | employee_name, sales_region, customer_type | order_type | quantity | sum | PASS |
| CP-0443 | employee_name, sales_region, customer_type | order_type | quantity | mean | PASS |
| CP-0444 | employee_name, sales_region, customer_type | order_type | quantity | count | PASS |
| CP-0445 | employee_name, sales_region, customer_type | order_type | unit_price | sum | PASS |
| CP-0446 | employee_name, sales_region, customer_type | order_type | unit_price | mean | PASS |
| CP-0447 | employee_name, sales_region, customer_type | order_type | unit_price | count | PASS |
| CP-0448 | employee_name, sales_region, customer_type | order_type | quantity, unit_price | sum | PASS |
| CP-0449 | employee_name, sales_region, customer_type | order_type | quantity, unit_price | mean | PASS |
| CP-0450 | employee_name, sales_region, customer_type | order_type | quantity, unit_price | count | PASS |
| CP-0451 | employee_name, sales_region, customer_type | order_type | sale_price | sum | PASS |
| CP-0452 | employee_name, sales_region, customer_type | order_type | sale_price | mean | PASS |
| CP-0453 | employee_name, sales_region, customer_type | order_type | sale_price | count | PASS |
| CP-0454 | employee_name, sales_region, customer_type | order_type | quantity, sale_price | sum | PASS |
| CP-0455 | employee_name, sales_region, customer_type | order_type | quantity, sale_price | mean | PASS |
| CP-0456 | employee_name, sales_region, customer_type | order_type | quantity, sale_price | count | PASS |
| CP-0457 | employee_name, sales_region, customer_type | order_type | unit_price, sale_price | sum | PASS |
| CP-0458 | employee_name, sales_region, customer_type | order_type | unit_price, sale_price | mean | PASS |
| CP-0459 | employee_name, sales_region, customer_type | order_type | unit_price, sale_price | count | PASS |
| CP-0460 | employee_name, sales_region, customer_type | order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0461 | employee_name, sales_region, customer_type | order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0462 | employee_name, sales_region, customer_type | order_type | quantity, unit_price, sale_price | count | PASS |
| CP-0463 | employee_name, sales_region | order_type, customer_type | quantity | sum | PASS |
| CP-0464 | employee_name, sales_region | order_type, customer_type | quantity | mean | PASS |
| CP-0465 | employee_name, sales_region | order_type, customer_type | quantity | count | PASS |
| CP-0466 | employee_name, sales_region | order_type, customer_type | unit_price | sum | PASS |
| CP-0467 | employee_name, sales_region | order_type, customer_type | unit_price | mean | PASS |
| CP-0468 | employee_name, sales_region | order_type, customer_type | unit_price | count | PASS |
| CP-0469 | employee_name, sales_region | order_type, customer_type | quantity, unit_price | sum | PASS |
| CP-0470 | employee_name, sales_region | order_type, customer_type | quantity, unit_price | mean | PASS |
| CP-0471 | employee_name, sales_region | order_type, customer_type | quantity, unit_price | count | PASS |
| CP-0472 | employee_name, sales_region | order_type, customer_type | sale_price | sum | PASS |
| CP-0473 | employee_name, sales_region | order_type, customer_type | sale_price | mean | PASS |
| CP-0474 | employee_name, sales_region | order_type, customer_type | sale_price | count | PASS |
| CP-0475 | employee_name, sales_region | order_type, customer_type | quantity, sale_price | sum | PASS |
| CP-0476 | employee_name, sales_region | order_type, customer_type | quantity, sale_price | mean | PASS |
| CP-0477 | employee_name, sales_region | order_type, customer_type | quantity, sale_price | count | PASS |
| CP-0478 | employee_name, sales_region | order_type, customer_type | unit_price, sale_price | sum | PASS |
| CP-0479 | employee_name, sales_region | order_type, customer_type | unit_price, sale_price | mean | PASS |
| CP-0480 | employee_name, sales_region | order_type, customer_type | unit_price, sale_price | count | PASS |
| CP-0481 | employee_name, sales_region | order_type, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0482 | employee_name, sales_region | order_type, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0483 | employee_name, sales_region | order_type, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-0484 | employee_name, sales_region | order_type | quantity | sum | PASS |
| CP-0485 | employee_name, sales_region | order_type | quantity | mean | PASS |
| CP-0486 | employee_name, sales_region | order_type | quantity | count | PASS |
| CP-0487 | employee_name, sales_region | order_type | unit_price | sum | PASS |
| CP-0488 | employee_name, sales_region | order_type | unit_price | mean | PASS |
| CP-0489 | employee_name, sales_region | order_type | unit_price | count | PASS |
| CP-0490 | employee_name, sales_region | order_type | quantity, unit_price | sum | PASS |
| CP-0491 | employee_name, sales_region | order_type | quantity, unit_price | mean | PASS |
| CP-0492 | employee_name, sales_region | order_type | quantity, unit_price | count | PASS |
| CP-0493 | employee_name, sales_region | order_type | sale_price | sum | PASS |
| CP-0494 | employee_name, sales_region | order_type | sale_price | mean | PASS |
| CP-0495 | employee_name, sales_region | order_type | sale_price | count | PASS |
| CP-0496 | employee_name, sales_region | order_type | quantity, sale_price | sum | PASS |
| CP-0497 | employee_name, sales_region | order_type | quantity, sale_price | mean | PASS |
| CP-0498 | employee_name, sales_region | order_type | quantity, sale_price | count | PASS |
| CP-0499 | employee_name, sales_region | order_type | unit_price, sale_price | sum | PASS |
| CP-0500 | employee_name, sales_region | order_type | unit_price, sale_price | mean | PASS |
| CP-0501 | employee_name, sales_region | order_type | unit_price, sale_price | count | PASS |
| CP-0502 | employee_name, sales_region | order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0503 | employee_name, sales_region | order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0504 | employee_name, sales_region | order_type | quantity, unit_price, sale_price | count | PASS |
| CP-0505 | employee_name, sales_region, customer_type | - | quantity | sum | PASS |
| CP-0506 | employee_name, sales_region, customer_type | - | quantity | mean | PASS |
| CP-0507 | employee_name, sales_region, customer_type | - | quantity | count | PASS |
| CP-0508 | employee_name, sales_region, customer_type | - | unit_price | sum | PASS |
| CP-0509 | employee_name, sales_region, customer_type | - | unit_price | mean | PASS |
| CP-0510 | employee_name, sales_region, customer_type | - | unit_price | count | PASS |
| CP-0511 | employee_name, sales_region, customer_type | - | quantity, unit_price | sum | PASS |
| CP-0512 | employee_name, sales_region, customer_type | - | quantity, unit_price | mean | PASS |
| CP-0513 | employee_name, sales_region, customer_type | - | quantity, unit_price | count | PASS |
| CP-0514 | employee_name, sales_region, customer_type | - | sale_price | sum | PASS |
| CP-0515 | employee_name, sales_region, customer_type | - | sale_price | mean | PASS |
| CP-0516 | employee_name, sales_region, customer_type | - | sale_price | count | PASS |
| CP-0517 | employee_name, sales_region, customer_type | - | quantity, sale_price | sum | PASS |
| CP-0518 | employee_name, sales_region, customer_type | - | quantity, sale_price | mean | PASS |
| CP-0519 | employee_name, sales_region, customer_type | - | quantity, sale_price | count | PASS |
| CP-0520 | employee_name, sales_region, customer_type | - | unit_price, sale_price | sum | PASS |
| CP-0521 | employee_name, sales_region, customer_type | - | unit_price, sale_price | mean | PASS |
| CP-0522 | employee_name, sales_region, customer_type | - | unit_price, sale_price | count | PASS |
| CP-0523 | employee_name, sales_region, customer_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-0524 | employee_name, sales_region, customer_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-0525 | employee_name, sales_region, customer_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-0526 | employee_name, sales_region | customer_type | quantity | sum | PASS |
| CP-0527 | employee_name, sales_region | customer_type | quantity | mean | PASS |
| CP-0528 | employee_name, sales_region | customer_type | quantity | count | PASS |
| CP-0529 | employee_name, sales_region | customer_type | unit_price | sum | PASS |
| CP-0530 | employee_name, sales_region | customer_type | unit_price | mean | PASS |
| CP-0531 | employee_name, sales_region | customer_type | unit_price | count | PASS |
| CP-0532 | employee_name, sales_region | customer_type | quantity, unit_price | sum | PASS |
| CP-0533 | employee_name, sales_region | customer_type | quantity, unit_price | mean | PASS |
| CP-0534 | employee_name, sales_region | customer_type | quantity, unit_price | count | PASS |
| CP-0535 | employee_name, sales_region | customer_type | sale_price | sum | PASS |
| CP-0536 | employee_name, sales_region | customer_type | sale_price | mean | PASS |
| CP-0537 | employee_name, sales_region | customer_type | sale_price | count | PASS |
| CP-0538 | employee_name, sales_region | customer_type | quantity, sale_price | sum | PASS |
| CP-0539 | employee_name, sales_region | customer_type | quantity, sale_price | mean | PASS |
| CP-0540 | employee_name, sales_region | customer_type | quantity, sale_price | count | PASS |
| CP-0541 | employee_name, sales_region | customer_type | unit_price, sale_price | sum | PASS |
| CP-0542 | employee_name, sales_region | customer_type | unit_price, sale_price | mean | PASS |
| CP-0543 | employee_name, sales_region | customer_type | unit_price, sale_price | count | PASS |
| CP-0544 | employee_name, sales_region | customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0545 | employee_name, sales_region | customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0546 | employee_name, sales_region | customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-0547 | employee_name, sales_region | - | quantity | sum | PASS |
| CP-0548 | employee_name, sales_region | - | quantity | mean | PASS |
| CP-0549 | employee_name, sales_region | - | quantity | count | PASS |
| CP-0550 | employee_name, sales_region | - | unit_price | sum | PASS |
| CP-0551 | employee_name, sales_region | - | unit_price | mean | PASS |
| CP-0552 | employee_name, sales_region | - | unit_price | count | PASS |
| CP-0553 | employee_name, sales_region | - | quantity, unit_price | sum | PASS |
| CP-0554 | employee_name, sales_region | - | quantity, unit_price | mean | PASS |
| CP-0555 | employee_name, sales_region | - | quantity, unit_price | count | PASS |
| CP-0556 | employee_name, sales_region | - | sale_price | sum | PASS |
| CP-0557 | employee_name, sales_region | - | sale_price | mean | PASS |
| CP-0558 | employee_name, sales_region | - | sale_price | count | PASS |
| CP-0559 | employee_name, sales_region | - | quantity, sale_price | sum | PASS |
| CP-0560 | employee_name, sales_region | - | quantity, sale_price | mean | PASS |
| CP-0561 | employee_name, sales_region | - | quantity, sale_price | count | PASS |
| CP-0562 | employee_name, sales_region | - | unit_price, sale_price | sum | PASS |
| CP-0563 | employee_name, sales_region | - | unit_price, sale_price | mean | PASS |
| CP-0564 | employee_name, sales_region | - | unit_price, sale_price | count | PASS |
| CP-0565 | employee_name, sales_region | - | quantity, unit_price, sale_price | sum | PASS |
| CP-0566 | employee_name, sales_region | - | quantity, unit_price, sale_price | mean | PASS |
| CP-0567 | employee_name, sales_region | - | quantity, unit_price, sale_price | count | PASS |
| CP-0568 | employee_name, product_category, order_type, customer_type | sales_region | quantity | sum | PASS |
| CP-0569 | employee_name, product_category, order_type, customer_type | sales_region | quantity | mean | PASS |
| CP-0570 | employee_name, product_category, order_type, customer_type | sales_region | quantity | count | PASS |
| CP-0571 | employee_name, product_category, order_type, customer_type | sales_region | unit_price | sum | PASS |
| CP-0572 | employee_name, product_category, order_type, customer_type | sales_region | unit_price | mean | PASS |
| CP-0573 | employee_name, product_category, order_type, customer_type | sales_region | unit_price | count | PASS |
| CP-0574 | employee_name, product_category, order_type, customer_type | sales_region | quantity, unit_price | sum | PASS |
| CP-0575 | employee_name, product_category, order_type, customer_type | sales_region | quantity, unit_price | mean | PASS |
| CP-0576 | employee_name, product_category, order_type, customer_type | sales_region | quantity, unit_price | count | PASS |
| CP-0577 | employee_name, product_category, order_type, customer_type | sales_region | sale_price | sum | PASS |
| CP-0578 | employee_name, product_category, order_type, customer_type | sales_region | sale_price | mean | PASS |
| CP-0579 | employee_name, product_category, order_type, customer_type | sales_region | sale_price | count | PASS |
| CP-0580 | employee_name, product_category, order_type, customer_type | sales_region | quantity, sale_price | sum | PASS |
| CP-0581 | employee_name, product_category, order_type, customer_type | sales_region | quantity, sale_price | mean | PASS |
| CP-0582 | employee_name, product_category, order_type, customer_type | sales_region | quantity, sale_price | count | PASS |
| CP-0583 | employee_name, product_category, order_type, customer_type | sales_region | unit_price, sale_price | sum | PASS |
| CP-0584 | employee_name, product_category, order_type, customer_type | sales_region | unit_price, sale_price | mean | PASS |
| CP-0585 | employee_name, product_category, order_type, customer_type | sales_region | unit_price, sale_price | count | PASS |
| CP-0586 | employee_name, product_category, order_type, customer_type | sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-0587 | employee_name, product_category, order_type, customer_type | sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-0588 | employee_name, product_category, order_type, customer_type | sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-0589 | employee_name, product_category, order_type | sales_region, customer_type | quantity | sum | PASS |
| CP-0590 | employee_name, product_category, order_type | sales_region, customer_type | quantity | mean | PASS |
| CP-0591 | employee_name, product_category, order_type | sales_region, customer_type | quantity | count | PASS |
| CP-0592 | employee_name, product_category, order_type | sales_region, customer_type | unit_price | sum | PASS |
| CP-0593 | employee_name, product_category, order_type | sales_region, customer_type | unit_price | mean | PASS |
| CP-0594 | employee_name, product_category, order_type | sales_region, customer_type | unit_price | count | PASS |
| CP-0595 | employee_name, product_category, order_type | sales_region, customer_type | quantity, unit_price | sum | PASS |
| CP-0596 | employee_name, product_category, order_type | sales_region, customer_type | quantity, unit_price | mean | PASS |
| CP-0597 | employee_name, product_category, order_type | sales_region, customer_type | quantity, unit_price | count | PASS |
| CP-0598 | employee_name, product_category, order_type | sales_region, customer_type | sale_price | sum | PASS |
| CP-0599 | employee_name, product_category, order_type | sales_region, customer_type | sale_price | mean | PASS |
| CP-0600 | employee_name, product_category, order_type | sales_region, customer_type | sale_price | count | PASS |
| CP-0601 | employee_name, product_category, order_type | sales_region, customer_type | quantity, sale_price | sum | PASS |
| CP-0602 | employee_name, product_category, order_type | sales_region, customer_type | quantity, sale_price | mean | PASS |
| CP-0603 | employee_name, product_category, order_type | sales_region, customer_type | quantity, sale_price | count | PASS |
| CP-0604 | employee_name, product_category, order_type | sales_region, customer_type | unit_price, sale_price | sum | PASS |
| CP-0605 | employee_name, product_category, order_type | sales_region, customer_type | unit_price, sale_price | mean | PASS |
| CP-0606 | employee_name, product_category, order_type | sales_region, customer_type | unit_price, sale_price | count | PASS |
| CP-0607 | employee_name, product_category, order_type | sales_region, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0608 | employee_name, product_category, order_type | sales_region, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0609 | employee_name, product_category, order_type | sales_region, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-0610 | employee_name, product_category, order_type | sales_region | quantity | sum | PASS |
| CP-0611 | employee_name, product_category, order_type | sales_region | quantity | mean | PASS |
| CP-0612 | employee_name, product_category, order_type | sales_region | quantity | count | PASS |
| CP-0613 | employee_name, product_category, order_type | sales_region | unit_price | sum | PASS |
| CP-0614 | employee_name, product_category, order_type | sales_region | unit_price | mean | PASS |
| CP-0615 | employee_name, product_category, order_type | sales_region | unit_price | count | PASS |
| CP-0616 | employee_name, product_category, order_type | sales_region | quantity, unit_price | sum | PASS |
| CP-0617 | employee_name, product_category, order_type | sales_region | quantity, unit_price | mean | PASS |
| CP-0618 | employee_name, product_category, order_type | sales_region | quantity, unit_price | count | PASS |
| CP-0619 | employee_name, product_category, order_type | sales_region | sale_price | sum | PASS |
| CP-0620 | employee_name, product_category, order_type | sales_region | sale_price | mean | PASS |
| CP-0621 | employee_name, product_category, order_type | sales_region | sale_price | count | PASS |
| CP-0622 | employee_name, product_category, order_type | sales_region | quantity, sale_price | sum | PASS |
| CP-0623 | employee_name, product_category, order_type | sales_region | quantity, sale_price | mean | PASS |
| CP-0624 | employee_name, product_category, order_type | sales_region | quantity, sale_price | count | PASS |
| CP-0625 | employee_name, product_category, order_type | sales_region | unit_price, sale_price | sum | PASS |
| CP-0626 | employee_name, product_category, order_type | sales_region | unit_price, sale_price | mean | PASS |
| CP-0627 | employee_name, product_category, order_type | sales_region | unit_price, sale_price | count | PASS |
| CP-0628 | employee_name, product_category, order_type | sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-0629 | employee_name, product_category, order_type | sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-0630 | employee_name, product_category, order_type | sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-0631 | employee_name, product_category, customer_type | sales_region, order_type | quantity | sum | PASS |
| CP-0632 | employee_name, product_category, customer_type | sales_region, order_type | quantity | mean | PASS |
| CP-0633 | employee_name, product_category, customer_type | sales_region, order_type | quantity | count | PASS |
| CP-0634 | employee_name, product_category, customer_type | sales_region, order_type | unit_price | sum | PASS |
| CP-0635 | employee_name, product_category, customer_type | sales_region, order_type | unit_price | mean | PASS |
| CP-0636 | employee_name, product_category, customer_type | sales_region, order_type | unit_price | count | PASS |
| CP-0637 | employee_name, product_category, customer_type | sales_region, order_type | quantity, unit_price | sum | PASS |
| CP-0638 | employee_name, product_category, customer_type | sales_region, order_type | quantity, unit_price | mean | PASS |
| CP-0639 | employee_name, product_category, customer_type | sales_region, order_type | quantity, unit_price | count | PASS |
| CP-0640 | employee_name, product_category, customer_type | sales_region, order_type | sale_price | sum | PASS |
| CP-0641 | employee_name, product_category, customer_type | sales_region, order_type | sale_price | mean | PASS |
| CP-0642 | employee_name, product_category, customer_type | sales_region, order_type | sale_price | count | PASS |
| CP-0643 | employee_name, product_category, customer_type | sales_region, order_type | quantity, sale_price | sum | PASS |
| CP-0644 | employee_name, product_category, customer_type | sales_region, order_type | quantity, sale_price | mean | PASS |
| CP-0645 | employee_name, product_category, customer_type | sales_region, order_type | quantity, sale_price | count | PASS |
| CP-0646 | employee_name, product_category, customer_type | sales_region, order_type | unit_price, sale_price | sum | PASS |
| CP-0647 | employee_name, product_category, customer_type | sales_region, order_type | unit_price, sale_price | mean | PASS |
| CP-0648 | employee_name, product_category, customer_type | sales_region, order_type | unit_price, sale_price | count | PASS |
| CP-0649 | employee_name, product_category, customer_type | sales_region, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0650 | employee_name, product_category, customer_type | sales_region, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0651 | employee_name, product_category, customer_type | sales_region, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-0652 | employee_name, product_category | sales_region, order_type, customer_type | quantity | sum | PASS |
| CP-0653 | employee_name, product_category | sales_region, order_type, customer_type | quantity | mean | PASS |
| CP-0654 | employee_name, product_category | sales_region, order_type, customer_type | quantity | count | PASS |
| CP-0655 | employee_name, product_category | sales_region, order_type, customer_type | unit_price | sum | PASS |
| CP-0656 | employee_name, product_category | sales_region, order_type, customer_type | unit_price | mean | PASS |
| CP-0657 | employee_name, product_category | sales_region, order_type, customer_type | unit_price | count | PASS |
| CP-0658 | employee_name, product_category | sales_region, order_type, customer_type | quantity, unit_price | sum | PASS |
| CP-0659 | employee_name, product_category | sales_region, order_type, customer_type | quantity, unit_price | mean | PASS |
| CP-0660 | employee_name, product_category | sales_region, order_type, customer_type | quantity, unit_price | count | PASS |
| CP-0661 | employee_name, product_category | sales_region, order_type, customer_type | sale_price | sum | PASS |
| CP-0662 | employee_name, product_category | sales_region, order_type, customer_type | sale_price | mean | PASS |
| CP-0663 | employee_name, product_category | sales_region, order_type, customer_type | sale_price | count | PASS |
| CP-0664 | employee_name, product_category | sales_region, order_type, customer_type | quantity, sale_price | sum | PASS |
| CP-0665 | employee_name, product_category | sales_region, order_type, customer_type | quantity, sale_price | mean | PASS |
| CP-0666 | employee_name, product_category | sales_region, order_type, customer_type | quantity, sale_price | count | PASS |
| CP-0667 | employee_name, product_category | sales_region, order_type, customer_type | unit_price, sale_price | sum | PASS |
| CP-0668 | employee_name, product_category | sales_region, order_type, customer_type | unit_price, sale_price | mean | PASS |
| CP-0669 | employee_name, product_category | sales_region, order_type, customer_type | unit_price, sale_price | count | PASS |
| CP-0670 | employee_name, product_category | sales_region, order_type, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0671 | employee_name, product_category | sales_region, order_type, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0672 | employee_name, product_category | sales_region, order_type, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-0673 | employee_name, product_category | sales_region, order_type | quantity | sum | PASS |
| CP-0674 | employee_name, product_category | sales_region, order_type | quantity | mean | PASS |
| CP-0675 | employee_name, product_category | sales_region, order_type | quantity | count | PASS |
| CP-0676 | employee_name, product_category | sales_region, order_type | unit_price | sum | PASS |
| CP-0677 | employee_name, product_category | sales_region, order_type | unit_price | mean | PASS |
| CP-0678 | employee_name, product_category | sales_region, order_type | unit_price | count | PASS |
| CP-0679 | employee_name, product_category | sales_region, order_type | quantity, unit_price | sum | PASS |
| CP-0680 | employee_name, product_category | sales_region, order_type | quantity, unit_price | mean | PASS |
| CP-0681 | employee_name, product_category | sales_region, order_type | quantity, unit_price | count | PASS |
| CP-0682 | employee_name, product_category | sales_region, order_type | sale_price | sum | PASS |
| CP-0683 | employee_name, product_category | sales_region, order_type | sale_price | mean | PASS |
| CP-0684 | employee_name, product_category | sales_region, order_type | sale_price | count | PASS |
| CP-0685 | employee_name, product_category | sales_region, order_type | quantity, sale_price | sum | PASS |
| CP-0686 | employee_name, product_category | sales_region, order_type | quantity, sale_price | mean | PASS |
| CP-0687 | employee_name, product_category | sales_region, order_type | quantity, sale_price | count | PASS |
| CP-0688 | employee_name, product_category | sales_region, order_type | unit_price, sale_price | sum | PASS |
| CP-0689 | employee_name, product_category | sales_region, order_type | unit_price, sale_price | mean | PASS |
| CP-0690 | employee_name, product_category | sales_region, order_type | unit_price, sale_price | count | PASS |
| CP-0691 | employee_name, product_category | sales_region, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0692 | employee_name, product_category | sales_region, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0693 | employee_name, product_category | sales_region, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-0694 | employee_name, product_category, customer_type | sales_region | quantity | sum | PASS |
| CP-0695 | employee_name, product_category, customer_type | sales_region | quantity | mean | PASS |
| CP-0696 | employee_name, product_category, customer_type | sales_region | quantity | count | PASS |
| CP-0697 | employee_name, product_category, customer_type | sales_region | unit_price | sum | PASS |
| CP-0698 | employee_name, product_category, customer_type | sales_region | unit_price | mean | PASS |
| CP-0699 | employee_name, product_category, customer_type | sales_region | unit_price | count | PASS |
| CP-0700 | employee_name, product_category, customer_type | sales_region | quantity, unit_price | sum | PASS |
| CP-0701 | employee_name, product_category, customer_type | sales_region | quantity, unit_price | mean | PASS |
| CP-0702 | employee_name, product_category, customer_type | sales_region | quantity, unit_price | count | PASS |
| CP-0703 | employee_name, product_category, customer_type | sales_region | sale_price | sum | PASS |
| CP-0704 | employee_name, product_category, customer_type | sales_region | sale_price | mean | PASS |
| CP-0705 | employee_name, product_category, customer_type | sales_region | sale_price | count | PASS |
| CP-0706 | employee_name, product_category, customer_type | sales_region | quantity, sale_price | sum | PASS |
| CP-0707 | employee_name, product_category, customer_type | sales_region | quantity, sale_price | mean | PASS |
| CP-0708 | employee_name, product_category, customer_type | sales_region | quantity, sale_price | count | PASS |
| CP-0709 | employee_name, product_category, customer_type | sales_region | unit_price, sale_price | sum | PASS |
| CP-0710 | employee_name, product_category, customer_type | sales_region | unit_price, sale_price | mean | PASS |
| CP-0711 | employee_name, product_category, customer_type | sales_region | unit_price, sale_price | count | PASS |
| CP-0712 | employee_name, product_category, customer_type | sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-0713 | employee_name, product_category, customer_type | sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-0714 | employee_name, product_category, customer_type | sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-0715 | employee_name, product_category | sales_region, customer_type | quantity | sum | PASS |
| CP-0716 | employee_name, product_category | sales_region, customer_type | quantity | mean | PASS |
| CP-0717 | employee_name, product_category | sales_region, customer_type | quantity | count | PASS |
| CP-0718 | employee_name, product_category | sales_region, customer_type | unit_price | sum | PASS |
| CP-0719 | employee_name, product_category | sales_region, customer_type | unit_price | mean | PASS |
| CP-0720 | employee_name, product_category | sales_region, customer_type | unit_price | count | PASS |
| CP-0721 | employee_name, product_category | sales_region, customer_type | quantity, unit_price | sum | PASS |
| CP-0722 | employee_name, product_category | sales_region, customer_type | quantity, unit_price | mean | PASS |
| CP-0723 | employee_name, product_category | sales_region, customer_type | quantity, unit_price | count | PASS |
| CP-0724 | employee_name, product_category | sales_region, customer_type | sale_price | sum | PASS |
| CP-0725 | employee_name, product_category | sales_region, customer_type | sale_price | mean | PASS |
| CP-0726 | employee_name, product_category | sales_region, customer_type | sale_price | count | PASS |
| CP-0727 | employee_name, product_category | sales_region, customer_type | quantity, sale_price | sum | PASS |
| CP-0728 | employee_name, product_category | sales_region, customer_type | quantity, sale_price | mean | PASS |
| CP-0729 | employee_name, product_category | sales_region, customer_type | quantity, sale_price | count | PASS |
| CP-0730 | employee_name, product_category | sales_region, customer_type | unit_price, sale_price | sum | PASS |
| CP-0731 | employee_name, product_category | sales_region, customer_type | unit_price, sale_price | mean | PASS |
| CP-0732 | employee_name, product_category | sales_region, customer_type | unit_price, sale_price | count | PASS |
| CP-0733 | employee_name, product_category | sales_region, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0734 | employee_name, product_category | sales_region, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0735 | employee_name, product_category | sales_region, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-0736 | employee_name, product_category | sales_region | quantity | sum | PASS |
| CP-0737 | employee_name, product_category | sales_region | quantity | mean | PASS |
| CP-0738 | employee_name, product_category | sales_region | quantity | count | PASS |
| CP-0739 | employee_name, product_category | sales_region | unit_price | sum | PASS |
| CP-0740 | employee_name, product_category | sales_region | unit_price | mean | PASS |
| CP-0741 | employee_name, product_category | sales_region | unit_price | count | PASS |
| CP-0742 | employee_name, product_category | sales_region | quantity, unit_price | sum | PASS |
| CP-0743 | employee_name, product_category | sales_region | quantity, unit_price | mean | PASS |
| CP-0744 | employee_name, product_category | sales_region | quantity, unit_price | count | PASS |
| CP-0745 | employee_name, product_category | sales_region | sale_price | sum | PASS |
| CP-0746 | employee_name, product_category | sales_region | sale_price | mean | PASS |
| CP-0747 | employee_name, product_category | sales_region | sale_price | count | PASS |
| CP-0748 | employee_name, product_category | sales_region | quantity, sale_price | sum | PASS |
| CP-0749 | employee_name, product_category | sales_region | quantity, sale_price | mean | PASS |
| CP-0750 | employee_name, product_category | sales_region | quantity, sale_price | count | PASS |
| CP-0751 | employee_name, product_category | sales_region | unit_price, sale_price | sum | PASS |
| CP-0752 | employee_name, product_category | sales_region | unit_price, sale_price | mean | PASS |
| CP-0753 | employee_name, product_category | sales_region | unit_price, sale_price | count | PASS |
| CP-0754 | employee_name, product_category | sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-0755 | employee_name, product_category | sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-0756 | employee_name, product_category | sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-0757 | employee_name, order_type, customer_type | sales_region, product_category | quantity | sum | PASS |
| CP-0758 | employee_name, order_type, customer_type | sales_region, product_category | quantity | mean | PASS |
| CP-0759 | employee_name, order_type, customer_type | sales_region, product_category | quantity | count | PASS |
| CP-0760 | employee_name, order_type, customer_type | sales_region, product_category | unit_price | sum | PASS |
| CP-0761 | employee_name, order_type, customer_type | sales_region, product_category | unit_price | mean | PASS |
| CP-0762 | employee_name, order_type, customer_type | sales_region, product_category | unit_price | count | PASS |
| CP-0763 | employee_name, order_type, customer_type | sales_region, product_category | quantity, unit_price | sum | PASS |
| CP-0764 | employee_name, order_type, customer_type | sales_region, product_category | quantity, unit_price | mean | PASS |
| CP-0765 | employee_name, order_type, customer_type | sales_region, product_category | quantity, unit_price | count | PASS |
| CP-0766 | employee_name, order_type, customer_type | sales_region, product_category | sale_price | sum | PASS |
| CP-0767 | employee_name, order_type, customer_type | sales_region, product_category | sale_price | mean | PASS |
| CP-0768 | employee_name, order_type, customer_type | sales_region, product_category | sale_price | count | PASS |
| CP-0769 | employee_name, order_type, customer_type | sales_region, product_category | quantity, sale_price | sum | PASS |
| CP-0770 | employee_name, order_type, customer_type | sales_region, product_category | quantity, sale_price | mean | PASS |
| CP-0771 | employee_name, order_type, customer_type | sales_region, product_category | quantity, sale_price | count | PASS |
| CP-0772 | employee_name, order_type, customer_type | sales_region, product_category | unit_price, sale_price | sum | PASS |
| CP-0773 | employee_name, order_type, customer_type | sales_region, product_category | unit_price, sale_price | mean | PASS |
| CP-0774 | employee_name, order_type, customer_type | sales_region, product_category | unit_price, sale_price | count | PASS |
| CP-0775 | employee_name, order_type, customer_type | sales_region, product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-0776 | employee_name, order_type, customer_type | sales_region, product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-0777 | employee_name, order_type, customer_type | sales_region, product_category | quantity, unit_price, sale_price | count | PASS |
| CP-0778 | employee_name, order_type | sales_region, product_category, customer_type | quantity | sum | PASS |
| CP-0779 | employee_name, order_type | sales_region, product_category, customer_type | quantity | mean | PASS |
| CP-0780 | employee_name, order_type | sales_region, product_category, customer_type | quantity | count | PASS |
| CP-0781 | employee_name, order_type | sales_region, product_category, customer_type | unit_price | sum | PASS |
| CP-0782 | employee_name, order_type | sales_region, product_category, customer_type | unit_price | mean | PASS |
| CP-0783 | employee_name, order_type | sales_region, product_category, customer_type | unit_price | count | PASS |
| CP-0784 | employee_name, order_type | sales_region, product_category, customer_type | quantity, unit_price | sum | PASS |
| CP-0785 | employee_name, order_type | sales_region, product_category, customer_type | quantity, unit_price | mean | PASS |
| CP-0786 | employee_name, order_type | sales_region, product_category, customer_type | quantity, unit_price | count | PASS |
| CP-0787 | employee_name, order_type | sales_region, product_category, customer_type | sale_price | sum | PASS |
| CP-0788 | employee_name, order_type | sales_region, product_category, customer_type | sale_price | mean | PASS |
| CP-0789 | employee_name, order_type | sales_region, product_category, customer_type | sale_price | count | PASS |
| CP-0790 | employee_name, order_type | sales_region, product_category, customer_type | quantity, sale_price | sum | PASS |
| CP-0791 | employee_name, order_type | sales_region, product_category, customer_type | quantity, sale_price | mean | PASS |
| CP-0792 | employee_name, order_type | sales_region, product_category, customer_type | quantity, sale_price | count | PASS |
| CP-0793 | employee_name, order_type | sales_region, product_category, customer_type | unit_price, sale_price | sum | PASS |
| CP-0794 | employee_name, order_type | sales_region, product_category, customer_type | unit_price, sale_price | mean | PASS |
| CP-0795 | employee_name, order_type | sales_region, product_category, customer_type | unit_price, sale_price | count | PASS |
| CP-0796 | employee_name, order_type | sales_region, product_category, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0797 | employee_name, order_type | sales_region, product_category, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0798 | employee_name, order_type | sales_region, product_category, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-0799 | employee_name, order_type | sales_region, product_category | quantity | sum | PASS |
| CP-0800 | employee_name, order_type | sales_region, product_category | quantity | mean | PASS |
| CP-0801 | employee_name, order_type | sales_region, product_category | quantity | count | PASS |
| CP-0802 | employee_name, order_type | sales_region, product_category | unit_price | sum | PASS |
| CP-0803 | employee_name, order_type | sales_region, product_category | unit_price | mean | PASS |
| CP-0804 | employee_name, order_type | sales_region, product_category | unit_price | count | PASS |
| CP-0805 | employee_name, order_type | sales_region, product_category | quantity, unit_price | sum | PASS |
| CP-0806 | employee_name, order_type | sales_region, product_category | quantity, unit_price | mean | PASS |
| CP-0807 | employee_name, order_type | sales_region, product_category | quantity, unit_price | count | PASS |
| CP-0808 | employee_name, order_type | sales_region, product_category | sale_price | sum | PASS |
| CP-0809 | employee_name, order_type | sales_region, product_category | sale_price | mean | PASS |
| CP-0810 | employee_name, order_type | sales_region, product_category | sale_price | count | PASS |
| CP-0811 | employee_name, order_type | sales_region, product_category | quantity, sale_price | sum | PASS |
| CP-0812 | employee_name, order_type | sales_region, product_category | quantity, sale_price | mean | PASS |
| CP-0813 | employee_name, order_type | sales_region, product_category | quantity, sale_price | count | PASS |
| CP-0814 | employee_name, order_type | sales_region, product_category | unit_price, sale_price | sum | PASS |
| CP-0815 | employee_name, order_type | sales_region, product_category | unit_price, sale_price | mean | PASS |
| CP-0816 | employee_name, order_type | sales_region, product_category | unit_price, sale_price | count | PASS |
| CP-0817 | employee_name, order_type | sales_region, product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-0818 | employee_name, order_type | sales_region, product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-0819 | employee_name, order_type | sales_region, product_category | quantity, unit_price, sale_price | count | PASS |
| CP-0820 | employee_name, customer_type | sales_region, product_category, order_type | quantity | sum | PASS |
| CP-0821 | employee_name, customer_type | sales_region, product_category, order_type | quantity | mean | PASS |
| CP-0822 | employee_name, customer_type | sales_region, product_category, order_type | quantity | count | PASS |
| CP-0823 | employee_name, customer_type | sales_region, product_category, order_type | unit_price | sum | PASS |
| CP-0824 | employee_name, customer_type | sales_region, product_category, order_type | unit_price | mean | PASS |
| CP-0825 | employee_name, customer_type | sales_region, product_category, order_type | unit_price | count | PASS |
| CP-0826 | employee_name, customer_type | sales_region, product_category, order_type | quantity, unit_price | sum | PASS |
| CP-0827 | employee_name, customer_type | sales_region, product_category, order_type | quantity, unit_price | mean | PASS |
| CP-0828 | employee_name, customer_type | sales_region, product_category, order_type | quantity, unit_price | count | PASS |
| CP-0829 | employee_name, customer_type | sales_region, product_category, order_type | sale_price | sum | PASS |
| CP-0830 | employee_name, customer_type | sales_region, product_category, order_type | sale_price | mean | PASS |
| CP-0831 | employee_name, customer_type | sales_region, product_category, order_type | sale_price | count | PASS |
| CP-0832 | employee_name, customer_type | sales_region, product_category, order_type | quantity, sale_price | sum | PASS |
| CP-0833 | employee_name, customer_type | sales_region, product_category, order_type | quantity, sale_price | mean | PASS |
| CP-0834 | employee_name, customer_type | sales_region, product_category, order_type | quantity, sale_price | count | PASS |
| CP-0835 | employee_name, customer_type | sales_region, product_category, order_type | unit_price, sale_price | sum | PASS |
| CP-0836 | employee_name, customer_type | sales_region, product_category, order_type | unit_price, sale_price | mean | PASS |
| CP-0837 | employee_name, customer_type | sales_region, product_category, order_type | unit_price, sale_price | count | PASS |
| CP-0838 | employee_name, customer_type | sales_region, product_category, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0839 | employee_name, customer_type | sales_region, product_category, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0840 | employee_name, customer_type | sales_region, product_category, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-0841 | employee_name | sales_region, product_category, order_type, customer_type | quantity | sum | PASS |
| CP-0842 | employee_name | sales_region, product_category, order_type, customer_type | quantity | mean | PASS |
| CP-0843 | employee_name | sales_region, product_category, order_type, customer_type | quantity | count | PASS |
| CP-0844 | employee_name | sales_region, product_category, order_type, customer_type | unit_price | sum | PASS |
| CP-0845 | employee_name | sales_region, product_category, order_type, customer_type | unit_price | mean | PASS |
| CP-0846 | employee_name | sales_region, product_category, order_type, customer_type | unit_price | count | PASS |
| CP-0847 | employee_name | sales_region, product_category, order_type, customer_type | quantity, unit_price | sum | PASS |
| CP-0848 | employee_name | sales_region, product_category, order_type, customer_type | quantity, unit_price | mean | PASS |
| CP-0849 | employee_name | sales_region, product_category, order_type, customer_type | quantity, unit_price | count | PASS |
| CP-0850 | employee_name | sales_region, product_category, order_type, customer_type | sale_price | sum | PASS |
| CP-0851 | employee_name | sales_region, product_category, order_type, customer_type | sale_price | mean | PASS |
| CP-0852 | employee_name | sales_region, product_category, order_type, customer_type | sale_price | count | PASS |
| CP-0853 | employee_name | sales_region, product_category, order_type, customer_type | quantity, sale_price | sum | PASS |
| CP-0854 | employee_name | sales_region, product_category, order_type, customer_type | quantity, sale_price | mean | PASS |
| CP-0855 | employee_name | sales_region, product_category, order_type, customer_type | quantity, sale_price | count | PASS |
| CP-0856 | employee_name | sales_region, product_category, order_type, customer_type | unit_price, sale_price | sum | PASS |
| CP-0857 | employee_name | sales_region, product_category, order_type, customer_type | unit_price, sale_price | mean | PASS |
| CP-0858 | employee_name | sales_region, product_category, order_type, customer_type | unit_price, sale_price | count | PASS |
| CP-0859 | employee_name | sales_region, product_category, order_type, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0860 | employee_name | sales_region, product_category, order_type, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0861 | employee_name | sales_region, product_category, order_type, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-0862 | employee_name | sales_region, product_category, order_type | quantity | sum | PASS |
| CP-0863 | employee_name | sales_region, product_category, order_type | quantity | mean | PASS |
| CP-0864 | employee_name | sales_region, product_category, order_type | quantity | count | PASS |
| CP-0865 | employee_name | sales_region, product_category, order_type | unit_price | sum | PASS |
| CP-0866 | employee_name | sales_region, product_category, order_type | unit_price | mean | PASS |
| CP-0867 | employee_name | sales_region, product_category, order_type | unit_price | count | PASS |
| CP-0868 | employee_name | sales_region, product_category, order_type | quantity, unit_price | sum | PASS |
| CP-0869 | employee_name | sales_region, product_category, order_type | quantity, unit_price | mean | PASS |
| CP-0870 | employee_name | sales_region, product_category, order_type | quantity, unit_price | count | PASS |
| CP-0871 | employee_name | sales_region, product_category, order_type | sale_price | sum | PASS |
| CP-0872 | employee_name | sales_region, product_category, order_type | sale_price | mean | PASS |
| CP-0873 | employee_name | sales_region, product_category, order_type | sale_price | count | PASS |
| CP-0874 | employee_name | sales_region, product_category, order_type | quantity, sale_price | sum | PASS |
| CP-0875 | employee_name | sales_region, product_category, order_type | quantity, sale_price | mean | PASS |
| CP-0876 | employee_name | sales_region, product_category, order_type | quantity, sale_price | count | PASS |
| CP-0877 | employee_name | sales_region, product_category, order_type | unit_price, sale_price | sum | PASS |
| CP-0878 | employee_name | sales_region, product_category, order_type | unit_price, sale_price | mean | PASS |
| CP-0879 | employee_name | sales_region, product_category, order_type | unit_price, sale_price | count | PASS |
| CP-0880 | employee_name | sales_region, product_category, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0881 | employee_name | sales_region, product_category, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0882 | employee_name | sales_region, product_category, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-0883 | employee_name, customer_type | sales_region, product_category | quantity | sum | PASS |
| CP-0884 | employee_name, customer_type | sales_region, product_category | quantity | mean | PASS |
| CP-0885 | employee_name, customer_type | sales_region, product_category | quantity | count | PASS |
| CP-0886 | employee_name, customer_type | sales_region, product_category | unit_price | sum | PASS |
| CP-0887 | employee_name, customer_type | sales_region, product_category | unit_price | mean | PASS |
| CP-0888 | employee_name, customer_type | sales_region, product_category | unit_price | count | PASS |
| CP-0889 | employee_name, customer_type | sales_region, product_category | quantity, unit_price | sum | PASS |
| CP-0890 | employee_name, customer_type | sales_region, product_category | quantity, unit_price | mean | PASS |
| CP-0891 | employee_name, customer_type | sales_region, product_category | quantity, unit_price | count | PASS |
| CP-0892 | employee_name, customer_type | sales_region, product_category | sale_price | sum | PASS |
| CP-0893 | employee_name, customer_type | sales_region, product_category | sale_price | mean | PASS |
| CP-0894 | employee_name, customer_type | sales_region, product_category | sale_price | count | PASS |
| CP-0895 | employee_name, customer_type | sales_region, product_category | quantity, sale_price | sum | PASS |
| CP-0896 | employee_name, customer_type | sales_region, product_category | quantity, sale_price | mean | PASS |
| CP-0897 | employee_name, customer_type | sales_region, product_category | quantity, sale_price | count | PASS |
| CP-0898 | employee_name, customer_type | sales_region, product_category | unit_price, sale_price | sum | PASS |
| CP-0899 | employee_name, customer_type | sales_region, product_category | unit_price, sale_price | mean | PASS |
| CP-0900 | employee_name, customer_type | sales_region, product_category | unit_price, sale_price | count | PASS |
| CP-0901 | employee_name, customer_type | sales_region, product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-0902 | employee_name, customer_type | sales_region, product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-0903 | employee_name, customer_type | sales_region, product_category | quantity, unit_price, sale_price | count | PASS |
| CP-0904 | employee_name | sales_region, product_category, customer_type | quantity | sum | PASS |
| CP-0905 | employee_name | sales_region, product_category, customer_type | quantity | mean | PASS |
| CP-0906 | employee_name | sales_region, product_category, customer_type | quantity | count | PASS |
| CP-0907 | employee_name | sales_region, product_category, customer_type | unit_price | sum | PASS |
| CP-0908 | employee_name | sales_region, product_category, customer_type | unit_price | mean | PASS |
| CP-0909 | employee_name | sales_region, product_category, customer_type | unit_price | count | PASS |
| CP-0910 | employee_name | sales_region, product_category, customer_type | quantity, unit_price | sum | PASS |
| CP-0911 | employee_name | sales_region, product_category, customer_type | quantity, unit_price | mean | PASS |
| CP-0912 | employee_name | sales_region, product_category, customer_type | quantity, unit_price | count | PASS |
| CP-0913 | employee_name | sales_region, product_category, customer_type | sale_price | sum | PASS |
| CP-0914 | employee_name | sales_region, product_category, customer_type | sale_price | mean | PASS |
| CP-0915 | employee_name | sales_region, product_category, customer_type | sale_price | count | PASS |
| CP-0916 | employee_name | sales_region, product_category, customer_type | quantity, sale_price | sum | PASS |
| CP-0917 | employee_name | sales_region, product_category, customer_type | quantity, sale_price | mean | PASS |
| CP-0918 | employee_name | sales_region, product_category, customer_type | quantity, sale_price | count | PASS |
| CP-0919 | employee_name | sales_region, product_category, customer_type | unit_price, sale_price | sum | PASS |
| CP-0920 | employee_name | sales_region, product_category, customer_type | unit_price, sale_price | mean | PASS |
| CP-0921 | employee_name | sales_region, product_category, customer_type | unit_price, sale_price | count | PASS |
| CP-0922 | employee_name | sales_region, product_category, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0923 | employee_name | sales_region, product_category, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0924 | employee_name | sales_region, product_category, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-0925 | employee_name | sales_region, product_category | quantity | sum | PASS |
| CP-0926 | employee_name | sales_region, product_category | quantity | mean | PASS |
| CP-0927 | employee_name | sales_region, product_category | quantity | count | PASS |
| CP-0928 | employee_name | sales_region, product_category | unit_price | sum | PASS |
| CP-0929 | employee_name | sales_region, product_category | unit_price | mean | PASS |
| CP-0930 | employee_name | sales_region, product_category | unit_price | count | PASS |
| CP-0931 | employee_name | sales_region, product_category | quantity, unit_price | sum | PASS |
| CP-0932 | employee_name | sales_region, product_category | quantity, unit_price | mean | PASS |
| CP-0933 | employee_name | sales_region, product_category | quantity, unit_price | count | PASS |
| CP-0934 | employee_name | sales_region, product_category | sale_price | sum | PASS |
| CP-0935 | employee_name | sales_region, product_category | sale_price | mean | PASS |
| CP-0936 | employee_name | sales_region, product_category | sale_price | count | PASS |
| CP-0937 | employee_name | sales_region, product_category | quantity, sale_price | sum | PASS |
| CP-0938 | employee_name | sales_region, product_category | quantity, sale_price | mean | PASS |
| CP-0939 | employee_name | sales_region, product_category | quantity, sale_price | count | PASS |
| CP-0940 | employee_name | sales_region, product_category | unit_price, sale_price | sum | PASS |
| CP-0941 | employee_name | sales_region, product_category | unit_price, sale_price | mean | PASS |
| CP-0942 | employee_name | sales_region, product_category | unit_price, sale_price | count | PASS |
| CP-0943 | employee_name | sales_region, product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-0944 | employee_name | sales_region, product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-0945 | employee_name | sales_region, product_category | quantity, unit_price, sale_price | count | PASS |
| CP-0946 | employee_name, order_type, customer_type | sales_region | quantity | sum | PASS |
| CP-0947 | employee_name, order_type, customer_type | sales_region | quantity | mean | PASS |
| CP-0948 | employee_name, order_type, customer_type | sales_region | quantity | count | PASS |
| CP-0949 | employee_name, order_type, customer_type | sales_region | unit_price | sum | PASS |
| CP-0950 | employee_name, order_type, customer_type | sales_region | unit_price | mean | PASS |
| CP-0951 | employee_name, order_type, customer_type | sales_region | unit_price | count | PASS |
| CP-0952 | employee_name, order_type, customer_type | sales_region | quantity, unit_price | sum | PASS |
| CP-0953 | employee_name, order_type, customer_type | sales_region | quantity, unit_price | mean | PASS |
| CP-0954 | employee_name, order_type, customer_type | sales_region | quantity, unit_price | count | PASS |
| CP-0955 | employee_name, order_type, customer_type | sales_region | sale_price | sum | PASS |
| CP-0956 | employee_name, order_type, customer_type | sales_region | sale_price | mean | PASS |
| CP-0957 | employee_name, order_type, customer_type | sales_region | sale_price | count | PASS |
| CP-0958 | employee_name, order_type, customer_type | sales_region | quantity, sale_price | sum | PASS |
| CP-0959 | employee_name, order_type, customer_type | sales_region | quantity, sale_price | mean | PASS |
| CP-0960 | employee_name, order_type, customer_type | sales_region | quantity, sale_price | count | PASS |
| CP-0961 | employee_name, order_type, customer_type | sales_region | unit_price, sale_price | sum | PASS |
| CP-0962 | employee_name, order_type, customer_type | sales_region | unit_price, sale_price | mean | PASS |
| CP-0963 | employee_name, order_type, customer_type | sales_region | unit_price, sale_price | count | PASS |
| CP-0964 | employee_name, order_type, customer_type | sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-0965 | employee_name, order_type, customer_type | sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-0966 | employee_name, order_type, customer_type | sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-0967 | employee_name, order_type | sales_region, customer_type | quantity | sum | PASS |
| CP-0968 | employee_name, order_type | sales_region, customer_type | quantity | mean | PASS |
| CP-0969 | employee_name, order_type | sales_region, customer_type | quantity | count | PASS |
| CP-0970 | employee_name, order_type | sales_region, customer_type | unit_price | sum | PASS |
| CP-0971 | employee_name, order_type | sales_region, customer_type | unit_price | mean | PASS |
| CP-0972 | employee_name, order_type | sales_region, customer_type | unit_price | count | PASS |
| CP-0973 | employee_name, order_type | sales_region, customer_type | quantity, unit_price | sum | PASS |
| CP-0974 | employee_name, order_type | sales_region, customer_type | quantity, unit_price | mean | PASS |
| CP-0975 | employee_name, order_type | sales_region, customer_type | quantity, unit_price | count | PASS |
| CP-0976 | employee_name, order_type | sales_region, customer_type | sale_price | sum | PASS |
| CP-0977 | employee_name, order_type | sales_region, customer_type | sale_price | mean | PASS |
| CP-0978 | employee_name, order_type | sales_region, customer_type | sale_price | count | PASS |
| CP-0979 | employee_name, order_type | sales_region, customer_type | quantity, sale_price | sum | PASS |
| CP-0980 | employee_name, order_type | sales_region, customer_type | quantity, sale_price | mean | PASS |
| CP-0981 | employee_name, order_type | sales_region, customer_type | quantity, sale_price | count | PASS |
| CP-0982 | employee_name, order_type | sales_region, customer_type | unit_price, sale_price | sum | PASS |
| CP-0983 | employee_name, order_type | sales_region, customer_type | unit_price, sale_price | mean | PASS |
| CP-0984 | employee_name, order_type | sales_region, customer_type | unit_price, sale_price | count | PASS |
| CP-0985 | employee_name, order_type | sales_region, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-0986 | employee_name, order_type | sales_region, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-0987 | employee_name, order_type | sales_region, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-0988 | employee_name, order_type | sales_region | quantity | sum | PASS |
| CP-0989 | employee_name, order_type | sales_region | quantity | mean | PASS |
| CP-0990 | employee_name, order_type | sales_region | quantity | count | PASS |
| CP-0991 | employee_name, order_type | sales_region | unit_price | sum | PASS |
| CP-0992 | employee_name, order_type | sales_region | unit_price | mean | PASS |
| CP-0993 | employee_name, order_type | sales_region | unit_price | count | PASS |
| CP-0994 | employee_name, order_type | sales_region | quantity, unit_price | sum | PASS |
| CP-0995 | employee_name, order_type | sales_region | quantity, unit_price | mean | PASS |
| CP-0996 | employee_name, order_type | sales_region | quantity, unit_price | count | PASS |
| CP-0997 | employee_name, order_type | sales_region | sale_price | sum | PASS |
| CP-0998 | employee_name, order_type | sales_region | sale_price | mean | PASS |
| CP-0999 | employee_name, order_type | sales_region | sale_price | count | PASS |
| CP-1000 | employee_name, order_type | sales_region | quantity, sale_price | sum | PASS |
| CP-1001 | employee_name, order_type | sales_region | quantity, sale_price | mean | PASS |
| CP-1002 | employee_name, order_type | sales_region | quantity, sale_price | count | PASS |
| CP-1003 | employee_name, order_type | sales_region | unit_price, sale_price | sum | PASS |
| CP-1004 | employee_name, order_type | sales_region | unit_price, sale_price | mean | PASS |
| CP-1005 | employee_name, order_type | sales_region | unit_price, sale_price | count | PASS |
| CP-1006 | employee_name, order_type | sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-1007 | employee_name, order_type | sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-1008 | employee_name, order_type | sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-1009 | employee_name, customer_type | sales_region, order_type | quantity | sum | PASS |
| CP-1010 | employee_name, customer_type | sales_region, order_type | quantity | mean | PASS |
| CP-1011 | employee_name, customer_type | sales_region, order_type | quantity | count | PASS |
| CP-1012 | employee_name, customer_type | sales_region, order_type | unit_price | sum | PASS |
| CP-1013 | employee_name, customer_type | sales_region, order_type | unit_price | mean | PASS |
| CP-1014 | employee_name, customer_type | sales_region, order_type | unit_price | count | PASS |
| CP-1015 | employee_name, customer_type | sales_region, order_type | quantity, unit_price | sum | PASS |
| CP-1016 | employee_name, customer_type | sales_region, order_type | quantity, unit_price | mean | PASS |
| CP-1017 | employee_name, customer_type | sales_region, order_type | quantity, unit_price | count | PASS |
| CP-1018 | employee_name, customer_type | sales_region, order_type | sale_price | sum | PASS |
| CP-1019 | employee_name, customer_type | sales_region, order_type | sale_price | mean | PASS |
| CP-1020 | employee_name, customer_type | sales_region, order_type | sale_price | count | PASS |
| CP-1021 | employee_name, customer_type | sales_region, order_type | quantity, sale_price | sum | PASS |
| CP-1022 | employee_name, customer_type | sales_region, order_type | quantity, sale_price | mean | PASS |
| CP-1023 | employee_name, customer_type | sales_region, order_type | quantity, sale_price | count | PASS |
| CP-1024 | employee_name, customer_type | sales_region, order_type | unit_price, sale_price | sum | PASS |
| CP-1025 | employee_name, customer_type | sales_region, order_type | unit_price, sale_price | mean | PASS |
| CP-1026 | employee_name, customer_type | sales_region, order_type | unit_price, sale_price | count | PASS |
| CP-1027 | employee_name, customer_type | sales_region, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1028 | employee_name, customer_type | sales_region, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1029 | employee_name, customer_type | sales_region, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-1030 | employee_name | sales_region, order_type, customer_type | quantity | sum | PASS |
| CP-1031 | employee_name | sales_region, order_type, customer_type | quantity | mean | PASS |
| CP-1032 | employee_name | sales_region, order_type, customer_type | quantity | count | PASS |
| CP-1033 | employee_name | sales_region, order_type, customer_type | unit_price | sum | PASS |
| CP-1034 | employee_name | sales_region, order_type, customer_type | unit_price | mean | PASS |
| CP-1035 | employee_name | sales_region, order_type, customer_type | unit_price | count | PASS |
| CP-1036 | employee_name | sales_region, order_type, customer_type | quantity, unit_price | sum | PASS |
| CP-1037 | employee_name | sales_region, order_type, customer_type | quantity, unit_price | mean | PASS |
| CP-1038 | employee_name | sales_region, order_type, customer_type | quantity, unit_price | count | PASS |
| CP-1039 | employee_name | sales_region, order_type, customer_type | sale_price | sum | PASS |
| CP-1040 | employee_name | sales_region, order_type, customer_type | sale_price | mean | PASS |
| CP-1041 | employee_name | sales_region, order_type, customer_type | sale_price | count | PASS |
| CP-1042 | employee_name | sales_region, order_type, customer_type | quantity, sale_price | sum | PASS |
| CP-1043 | employee_name | sales_region, order_type, customer_type | quantity, sale_price | mean | PASS |
| CP-1044 | employee_name | sales_region, order_type, customer_type | quantity, sale_price | count | PASS |
| CP-1045 | employee_name | sales_region, order_type, customer_type | unit_price, sale_price | sum | PASS |
| CP-1046 | employee_name | sales_region, order_type, customer_type | unit_price, sale_price | mean | PASS |
| CP-1047 | employee_name | sales_region, order_type, customer_type | unit_price, sale_price | count | PASS |
| CP-1048 | employee_name | sales_region, order_type, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1049 | employee_name | sales_region, order_type, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1050 | employee_name | sales_region, order_type, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-1051 | employee_name | sales_region, order_type | quantity | sum | PASS |
| CP-1052 | employee_name | sales_region, order_type | quantity | mean | PASS |
| CP-1053 | employee_name | sales_region, order_type | quantity | count | PASS |
| CP-1054 | employee_name | sales_region, order_type | unit_price | sum | PASS |
| CP-1055 | employee_name | sales_region, order_type | unit_price | mean | PASS |
| CP-1056 | employee_name | sales_region, order_type | unit_price | count | PASS |
| CP-1057 | employee_name | sales_region, order_type | quantity, unit_price | sum | PASS |
| CP-1058 | employee_name | sales_region, order_type | quantity, unit_price | mean | PASS |
| CP-1059 | employee_name | sales_region, order_type | quantity, unit_price | count | PASS |
| CP-1060 | employee_name | sales_region, order_type | sale_price | sum | PASS |
| CP-1061 | employee_name | sales_region, order_type | sale_price | mean | PASS |
| CP-1062 | employee_name | sales_region, order_type | sale_price | count | PASS |
| CP-1063 | employee_name | sales_region, order_type | quantity, sale_price | sum | PASS |
| CP-1064 | employee_name | sales_region, order_type | quantity, sale_price | mean | PASS |
| CP-1065 | employee_name | sales_region, order_type | quantity, sale_price | count | PASS |
| CP-1066 | employee_name | sales_region, order_type | unit_price, sale_price | sum | PASS |
| CP-1067 | employee_name | sales_region, order_type | unit_price, sale_price | mean | PASS |
| CP-1068 | employee_name | sales_region, order_type | unit_price, sale_price | count | PASS |
| CP-1069 | employee_name | sales_region, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1070 | employee_name | sales_region, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1071 | employee_name | sales_region, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-1072 | employee_name, customer_type | sales_region | quantity | sum | PASS |
| CP-1073 | employee_name, customer_type | sales_region | quantity | mean | PASS |
| CP-1074 | employee_name, customer_type | sales_region | quantity | count | PASS |
| CP-1075 | employee_name, customer_type | sales_region | unit_price | sum | PASS |
| CP-1076 | employee_name, customer_type | sales_region | unit_price | mean | PASS |
| CP-1077 | employee_name, customer_type | sales_region | unit_price | count | PASS |
| CP-1078 | employee_name, customer_type | sales_region | quantity, unit_price | sum | PASS |
| CP-1079 | employee_name, customer_type | sales_region | quantity, unit_price | mean | PASS |
| CP-1080 | employee_name, customer_type | sales_region | quantity, unit_price | count | PASS |
| CP-1081 | employee_name, customer_type | sales_region | sale_price | sum | PASS |
| CP-1082 | employee_name, customer_type | sales_region | sale_price | mean | PASS |
| CP-1083 | employee_name, customer_type | sales_region | sale_price | count | PASS |
| CP-1084 | employee_name, customer_type | sales_region | quantity, sale_price | sum | PASS |
| CP-1085 | employee_name, customer_type | sales_region | quantity, sale_price | mean | PASS |
| CP-1086 | employee_name, customer_type | sales_region | quantity, sale_price | count | PASS |
| CP-1087 | employee_name, customer_type | sales_region | unit_price, sale_price | sum | PASS |
| CP-1088 | employee_name, customer_type | sales_region | unit_price, sale_price | mean | PASS |
| CP-1089 | employee_name, customer_type | sales_region | unit_price, sale_price | count | PASS |
| CP-1090 | employee_name, customer_type | sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-1091 | employee_name, customer_type | sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-1092 | employee_name, customer_type | sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-1093 | employee_name | sales_region, customer_type | quantity | sum | PASS |
| CP-1094 | employee_name | sales_region, customer_type | quantity | mean | PASS |
| CP-1095 | employee_name | sales_region, customer_type | quantity | count | PASS |
| CP-1096 | employee_name | sales_region, customer_type | unit_price | sum | PASS |
| CP-1097 | employee_name | sales_region, customer_type | unit_price | mean | PASS |
| CP-1098 | employee_name | sales_region, customer_type | unit_price | count | PASS |
| CP-1099 | employee_name | sales_region, customer_type | quantity, unit_price | sum | PASS |
| CP-1100 | employee_name | sales_region, customer_type | quantity, unit_price | mean | PASS |
| CP-1101 | employee_name | sales_region, customer_type | quantity, unit_price | count | PASS |
| CP-1102 | employee_name | sales_region, customer_type | sale_price | sum | PASS |
| CP-1103 | employee_name | sales_region, customer_type | sale_price | mean | PASS |
| CP-1104 | employee_name | sales_region, customer_type | sale_price | count | PASS |
| CP-1105 | employee_name | sales_region, customer_type | quantity, sale_price | sum | PASS |
| CP-1106 | employee_name | sales_region, customer_type | quantity, sale_price | mean | PASS |
| CP-1107 | employee_name | sales_region, customer_type | quantity, sale_price | count | PASS |
| CP-1108 | employee_name | sales_region, customer_type | unit_price, sale_price | sum | PASS |
| CP-1109 | employee_name | sales_region, customer_type | unit_price, sale_price | mean | PASS |
| CP-1110 | employee_name | sales_region, customer_type | unit_price, sale_price | count | PASS |
| CP-1111 | employee_name | sales_region, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1112 | employee_name | sales_region, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1113 | employee_name | sales_region, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-1114 | employee_name | sales_region | quantity | sum | PASS |
| CP-1115 | employee_name | sales_region | quantity | mean | PASS |
| CP-1116 | employee_name | sales_region | quantity | count | PASS |
| CP-1117 | employee_name | sales_region | unit_price | sum | PASS |
| CP-1118 | employee_name | sales_region | unit_price | mean | PASS |
| CP-1119 | employee_name | sales_region | unit_price | count | PASS |
| CP-1120 | employee_name | sales_region | quantity, unit_price | sum | PASS |
| CP-1121 | employee_name | sales_region | quantity, unit_price | mean | PASS |
| CP-1122 | employee_name | sales_region | quantity, unit_price | count | PASS |
| CP-1123 | employee_name | sales_region | sale_price | sum | PASS |
| CP-1124 | employee_name | sales_region | sale_price | mean | PASS |
| CP-1125 | employee_name | sales_region | sale_price | count | PASS |
| CP-1126 | employee_name | sales_region | quantity, sale_price | sum | PASS |
| CP-1127 | employee_name | sales_region | quantity, sale_price | mean | PASS |
| CP-1128 | employee_name | sales_region | quantity, sale_price | count | PASS |
| CP-1129 | employee_name | sales_region | unit_price, sale_price | sum | PASS |
| CP-1130 | employee_name | sales_region | unit_price, sale_price | mean | PASS |
| CP-1131 | employee_name | sales_region | unit_price, sale_price | count | PASS |
| CP-1132 | employee_name | sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-1133 | employee_name | sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-1134 | employee_name | sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-1135 | employee_name, product_category, order_type, customer_type | - | quantity | sum | PASS |
| CP-1136 | employee_name, product_category, order_type, customer_type | - | quantity | mean | PASS |
| CP-1137 | employee_name, product_category, order_type, customer_type | - | quantity | count | PASS |
| CP-1138 | employee_name, product_category, order_type, customer_type | - | unit_price | sum | PASS |
| CP-1139 | employee_name, product_category, order_type, customer_type | - | unit_price | mean | PASS |
| CP-1140 | employee_name, product_category, order_type, customer_type | - | unit_price | count | PASS |
| CP-1141 | employee_name, product_category, order_type, customer_type | - | quantity, unit_price | sum | PASS |
| CP-1142 | employee_name, product_category, order_type, customer_type | - | quantity, unit_price | mean | PASS |
| CP-1143 | employee_name, product_category, order_type, customer_type | - | quantity, unit_price | count | PASS |
| CP-1144 | employee_name, product_category, order_type, customer_type | - | sale_price | sum | PASS |
| CP-1145 | employee_name, product_category, order_type, customer_type | - | sale_price | mean | PASS |
| CP-1146 | employee_name, product_category, order_type, customer_type | - | sale_price | count | PASS |
| CP-1147 | employee_name, product_category, order_type, customer_type | - | quantity, sale_price | sum | PASS |
| CP-1148 | employee_name, product_category, order_type, customer_type | - | quantity, sale_price | mean | PASS |
| CP-1149 | employee_name, product_category, order_type, customer_type | - | quantity, sale_price | count | PASS |
| CP-1150 | employee_name, product_category, order_type, customer_type | - | unit_price, sale_price | sum | PASS |
| CP-1151 | employee_name, product_category, order_type, customer_type | - | unit_price, sale_price | mean | PASS |
| CP-1152 | employee_name, product_category, order_type, customer_type | - | unit_price, sale_price | count | PASS |
| CP-1153 | employee_name, product_category, order_type, customer_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-1154 | employee_name, product_category, order_type, customer_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-1155 | employee_name, product_category, order_type, customer_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-1156 | employee_name, product_category, order_type | customer_type | quantity | sum | PASS |
| CP-1157 | employee_name, product_category, order_type | customer_type | quantity | mean | PASS |
| CP-1158 | employee_name, product_category, order_type | customer_type | quantity | count | PASS |
| CP-1159 | employee_name, product_category, order_type | customer_type | unit_price | sum | PASS |
| CP-1160 | employee_name, product_category, order_type | customer_type | unit_price | mean | PASS |
| CP-1161 | employee_name, product_category, order_type | customer_type | unit_price | count | PASS |
| CP-1162 | employee_name, product_category, order_type | customer_type | quantity, unit_price | sum | PASS |
| CP-1163 | employee_name, product_category, order_type | customer_type | quantity, unit_price | mean | PASS |
| CP-1164 | employee_name, product_category, order_type | customer_type | quantity, unit_price | count | PASS |
| CP-1165 | employee_name, product_category, order_type | customer_type | sale_price | sum | PASS |
| CP-1166 | employee_name, product_category, order_type | customer_type | sale_price | mean | PASS |
| CP-1167 | employee_name, product_category, order_type | customer_type | sale_price | count | PASS |
| CP-1168 | employee_name, product_category, order_type | customer_type | quantity, sale_price | sum | PASS |
| CP-1169 | employee_name, product_category, order_type | customer_type | quantity, sale_price | mean | PASS |
| CP-1170 | employee_name, product_category, order_type | customer_type | quantity, sale_price | count | PASS |
| CP-1171 | employee_name, product_category, order_type | customer_type | unit_price, sale_price | sum | PASS |
| CP-1172 | employee_name, product_category, order_type | customer_type | unit_price, sale_price | mean | PASS |
| CP-1173 | employee_name, product_category, order_type | customer_type | unit_price, sale_price | count | PASS |
| CP-1174 | employee_name, product_category, order_type | customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1175 | employee_name, product_category, order_type | customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1176 | employee_name, product_category, order_type | customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-1177 | employee_name, product_category, order_type | - | quantity | sum | PASS |
| CP-1178 | employee_name, product_category, order_type | - | quantity | mean | PASS |
| CP-1179 | employee_name, product_category, order_type | - | quantity | count | PASS |
| CP-1180 | employee_name, product_category, order_type | - | unit_price | sum | PASS |
| CP-1181 | employee_name, product_category, order_type | - | unit_price | mean | PASS |
| CP-1182 | employee_name, product_category, order_type | - | unit_price | count | PASS |
| CP-1183 | employee_name, product_category, order_type | - | quantity, unit_price | sum | PASS |
| CP-1184 | employee_name, product_category, order_type | - | quantity, unit_price | mean | PASS |
| CP-1185 | employee_name, product_category, order_type | - | quantity, unit_price | count | PASS |
| CP-1186 | employee_name, product_category, order_type | - | sale_price | sum | PASS |
| CP-1187 | employee_name, product_category, order_type | - | sale_price | mean | PASS |
| CP-1188 | employee_name, product_category, order_type | - | sale_price | count | PASS |
| CP-1189 | employee_name, product_category, order_type | - | quantity, sale_price | sum | PASS |
| CP-1190 | employee_name, product_category, order_type | - | quantity, sale_price | mean | PASS |
| CP-1191 | employee_name, product_category, order_type | - | quantity, sale_price | count | PASS |
| CP-1192 | employee_name, product_category, order_type | - | unit_price, sale_price | sum | PASS |
| CP-1193 | employee_name, product_category, order_type | - | unit_price, sale_price | mean | PASS |
| CP-1194 | employee_name, product_category, order_type | - | unit_price, sale_price | count | PASS |
| CP-1195 | employee_name, product_category, order_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-1196 | employee_name, product_category, order_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-1197 | employee_name, product_category, order_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-1198 | employee_name, product_category, customer_type | order_type | quantity | sum | PASS |
| CP-1199 | employee_name, product_category, customer_type | order_type | quantity | mean | PASS |
| CP-1200 | employee_name, product_category, customer_type | order_type | quantity | count | PASS |
| CP-1201 | employee_name, product_category, customer_type | order_type | unit_price | sum | PASS |
| CP-1202 | employee_name, product_category, customer_type | order_type | unit_price | mean | PASS |
| CP-1203 | employee_name, product_category, customer_type | order_type | unit_price | count | PASS |
| CP-1204 | employee_name, product_category, customer_type | order_type | quantity, unit_price | sum | PASS |
| CP-1205 | employee_name, product_category, customer_type | order_type | quantity, unit_price | mean | PASS |
| CP-1206 | employee_name, product_category, customer_type | order_type | quantity, unit_price | count | PASS |
| CP-1207 | employee_name, product_category, customer_type | order_type | sale_price | sum | PASS |
| CP-1208 | employee_name, product_category, customer_type | order_type | sale_price | mean | PASS |
| CP-1209 | employee_name, product_category, customer_type | order_type | sale_price | count | PASS |
| CP-1210 | employee_name, product_category, customer_type | order_type | quantity, sale_price | sum | PASS |
| CP-1211 | employee_name, product_category, customer_type | order_type | quantity, sale_price | mean | PASS |
| CP-1212 | employee_name, product_category, customer_type | order_type | quantity, sale_price | count | PASS |
| CP-1213 | employee_name, product_category, customer_type | order_type | unit_price, sale_price | sum | PASS |
| CP-1214 | employee_name, product_category, customer_type | order_type | unit_price, sale_price | mean | PASS |
| CP-1215 | employee_name, product_category, customer_type | order_type | unit_price, sale_price | count | PASS |
| CP-1216 | employee_name, product_category, customer_type | order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1217 | employee_name, product_category, customer_type | order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1218 | employee_name, product_category, customer_type | order_type | quantity, unit_price, sale_price | count | PASS |
| CP-1219 | employee_name, product_category | order_type, customer_type | quantity | sum | PASS |
| CP-1220 | employee_name, product_category | order_type, customer_type | quantity | mean | PASS |
| CP-1221 | employee_name, product_category | order_type, customer_type | quantity | count | PASS |
| CP-1222 | employee_name, product_category | order_type, customer_type | unit_price | sum | PASS |
| CP-1223 | employee_name, product_category | order_type, customer_type | unit_price | mean | PASS |
| CP-1224 | employee_name, product_category | order_type, customer_type | unit_price | count | PASS |
| CP-1225 | employee_name, product_category | order_type, customer_type | quantity, unit_price | sum | PASS |
| CP-1226 | employee_name, product_category | order_type, customer_type | quantity, unit_price | mean | PASS |
| CP-1227 | employee_name, product_category | order_type, customer_type | quantity, unit_price | count | PASS |
| CP-1228 | employee_name, product_category | order_type, customer_type | sale_price | sum | PASS |
| CP-1229 | employee_name, product_category | order_type, customer_type | sale_price | mean | PASS |
| CP-1230 | employee_name, product_category | order_type, customer_type | sale_price | count | PASS |
| CP-1231 | employee_name, product_category | order_type, customer_type | quantity, sale_price | sum | PASS |
| CP-1232 | employee_name, product_category | order_type, customer_type | quantity, sale_price | mean | PASS |
| CP-1233 | employee_name, product_category | order_type, customer_type | quantity, sale_price | count | PASS |
| CP-1234 | employee_name, product_category | order_type, customer_type | unit_price, sale_price | sum | PASS |
| CP-1235 | employee_name, product_category | order_type, customer_type | unit_price, sale_price | mean | PASS |
| CP-1236 | employee_name, product_category | order_type, customer_type | unit_price, sale_price | count | PASS |
| CP-1237 | employee_name, product_category | order_type, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1238 | employee_name, product_category | order_type, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1239 | employee_name, product_category | order_type, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-1240 | employee_name, product_category | order_type | quantity | sum | PASS |
| CP-1241 | employee_name, product_category | order_type | quantity | mean | PASS |
| CP-1242 | employee_name, product_category | order_type | quantity | count | PASS |
| CP-1243 | employee_name, product_category | order_type | unit_price | sum | PASS |
| CP-1244 | employee_name, product_category | order_type | unit_price | mean | PASS |
| CP-1245 | employee_name, product_category | order_type | unit_price | count | PASS |
| CP-1246 | employee_name, product_category | order_type | quantity, unit_price | sum | PASS |
| CP-1247 | employee_name, product_category | order_type | quantity, unit_price | mean | PASS |
| CP-1248 | employee_name, product_category | order_type | quantity, unit_price | count | PASS |
| CP-1249 | employee_name, product_category | order_type | sale_price | sum | PASS |
| CP-1250 | employee_name, product_category | order_type | sale_price | mean | PASS |
| CP-1251 | employee_name, product_category | order_type | sale_price | count | PASS |
| CP-1252 | employee_name, product_category | order_type | quantity, sale_price | sum | PASS |
| CP-1253 | employee_name, product_category | order_type | quantity, sale_price | mean | PASS |
| CP-1254 | employee_name, product_category | order_type | quantity, sale_price | count | PASS |
| CP-1255 | employee_name, product_category | order_type | unit_price, sale_price | sum | PASS |
| CP-1256 | employee_name, product_category | order_type | unit_price, sale_price | mean | PASS |
| CP-1257 | employee_name, product_category | order_type | unit_price, sale_price | count | PASS |
| CP-1258 | employee_name, product_category | order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1259 | employee_name, product_category | order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1260 | employee_name, product_category | order_type | quantity, unit_price, sale_price | count | PASS |
| CP-1261 | employee_name, product_category, customer_type | - | quantity | sum | PASS |
| CP-1262 | employee_name, product_category, customer_type | - | quantity | mean | PASS |
| CP-1263 | employee_name, product_category, customer_type | - | quantity | count | PASS |
| CP-1264 | employee_name, product_category, customer_type | - | unit_price | sum | PASS |
| CP-1265 | employee_name, product_category, customer_type | - | unit_price | mean | PASS |
| CP-1266 | employee_name, product_category, customer_type | - | unit_price | count | PASS |
| CP-1267 | employee_name, product_category, customer_type | - | quantity, unit_price | sum | PASS |
| CP-1268 | employee_name, product_category, customer_type | - | quantity, unit_price | mean | PASS |
| CP-1269 | employee_name, product_category, customer_type | - | quantity, unit_price | count | PASS |
| CP-1270 | employee_name, product_category, customer_type | - | sale_price | sum | PASS |
| CP-1271 | employee_name, product_category, customer_type | - | sale_price | mean | PASS |
| CP-1272 | employee_name, product_category, customer_type | - | sale_price | count | PASS |
| CP-1273 | employee_name, product_category, customer_type | - | quantity, sale_price | sum | PASS |
| CP-1274 | employee_name, product_category, customer_type | - | quantity, sale_price | mean | PASS |
| CP-1275 | employee_name, product_category, customer_type | - | quantity, sale_price | count | PASS |
| CP-1276 | employee_name, product_category, customer_type | - | unit_price, sale_price | sum | PASS |
| CP-1277 | employee_name, product_category, customer_type | - | unit_price, sale_price | mean | PASS |
| CP-1278 | employee_name, product_category, customer_type | - | unit_price, sale_price | count | PASS |
| CP-1279 | employee_name, product_category, customer_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-1280 | employee_name, product_category, customer_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-1281 | employee_name, product_category, customer_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-1282 | employee_name, product_category | customer_type | quantity | sum | PASS |
| CP-1283 | employee_name, product_category | customer_type | quantity | mean | PASS |
| CP-1284 | employee_name, product_category | customer_type | quantity | count | PASS |
| CP-1285 | employee_name, product_category | customer_type | unit_price | sum | PASS |
| CP-1286 | employee_name, product_category | customer_type | unit_price | mean | PASS |
| CP-1287 | employee_name, product_category | customer_type | unit_price | count | PASS |
| CP-1288 | employee_name, product_category | customer_type | quantity, unit_price | sum | PASS |
| CP-1289 | employee_name, product_category | customer_type | quantity, unit_price | mean | PASS |
| CP-1290 | employee_name, product_category | customer_type | quantity, unit_price | count | PASS |
| CP-1291 | employee_name, product_category | customer_type | sale_price | sum | PASS |
| CP-1292 | employee_name, product_category | customer_type | sale_price | mean | PASS |
| CP-1293 | employee_name, product_category | customer_type | sale_price | count | PASS |
| CP-1294 | employee_name, product_category | customer_type | quantity, sale_price | sum | PASS |
| CP-1295 | employee_name, product_category | customer_type | quantity, sale_price | mean | PASS |
| CP-1296 | employee_name, product_category | customer_type | quantity, sale_price | count | PASS |
| CP-1297 | employee_name, product_category | customer_type | unit_price, sale_price | sum | PASS |
| CP-1298 | employee_name, product_category | customer_type | unit_price, sale_price | mean | PASS |
| CP-1299 | employee_name, product_category | customer_type | unit_price, sale_price | count | PASS |
| CP-1300 | employee_name, product_category | customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1301 | employee_name, product_category | customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1302 | employee_name, product_category | customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-1303 | employee_name, product_category | - | quantity | sum | PASS |
| CP-1304 | employee_name, product_category | - | quantity | mean | PASS |
| CP-1305 | employee_name, product_category | - | quantity | count | PASS |
| CP-1306 | employee_name, product_category | - | unit_price | sum | PASS |
| CP-1307 | employee_name, product_category | - | unit_price | mean | PASS |
| CP-1308 | employee_name, product_category | - | unit_price | count | PASS |
| CP-1309 | employee_name, product_category | - | quantity, unit_price | sum | PASS |
| CP-1310 | employee_name, product_category | - | quantity, unit_price | mean | PASS |
| CP-1311 | employee_name, product_category | - | quantity, unit_price | count | PASS |
| CP-1312 | employee_name, product_category | - | sale_price | sum | PASS |
| CP-1313 | employee_name, product_category | - | sale_price | mean | PASS |
| CP-1314 | employee_name, product_category | - | sale_price | count | PASS |
| CP-1315 | employee_name, product_category | - | quantity, sale_price | sum | PASS |
| CP-1316 | employee_name, product_category | - | quantity, sale_price | mean | PASS |
| CP-1317 | employee_name, product_category | - | quantity, sale_price | count | PASS |
| CP-1318 | employee_name, product_category | - | unit_price, sale_price | sum | PASS |
| CP-1319 | employee_name, product_category | - | unit_price, sale_price | mean | PASS |
| CP-1320 | employee_name, product_category | - | unit_price, sale_price | count | PASS |
| CP-1321 | employee_name, product_category | - | quantity, unit_price, sale_price | sum | PASS |
| CP-1322 | employee_name, product_category | - | quantity, unit_price, sale_price | mean | PASS |
| CP-1323 | employee_name, product_category | - | quantity, unit_price, sale_price | count | PASS |
| CP-1324 | employee_name, order_type, customer_type | product_category | quantity | sum | PASS |
| CP-1325 | employee_name, order_type, customer_type | product_category | quantity | mean | PASS |
| CP-1326 | employee_name, order_type, customer_type | product_category | quantity | count | PASS |
| CP-1327 | employee_name, order_type, customer_type | product_category | unit_price | sum | PASS |
| CP-1328 | employee_name, order_type, customer_type | product_category | unit_price | mean | PASS |
| CP-1329 | employee_name, order_type, customer_type | product_category | unit_price | count | PASS |
| CP-1330 | employee_name, order_type, customer_type | product_category | quantity, unit_price | sum | PASS |
| CP-1331 | employee_name, order_type, customer_type | product_category | quantity, unit_price | mean | PASS |
| CP-1332 | employee_name, order_type, customer_type | product_category | quantity, unit_price | count | PASS |
| CP-1333 | employee_name, order_type, customer_type | product_category | sale_price | sum | PASS |
| CP-1334 | employee_name, order_type, customer_type | product_category | sale_price | mean | PASS |
| CP-1335 | employee_name, order_type, customer_type | product_category | sale_price | count | PASS |
| CP-1336 | employee_name, order_type, customer_type | product_category | quantity, sale_price | sum | PASS |
| CP-1337 | employee_name, order_type, customer_type | product_category | quantity, sale_price | mean | PASS |
| CP-1338 | employee_name, order_type, customer_type | product_category | quantity, sale_price | count | PASS |
| CP-1339 | employee_name, order_type, customer_type | product_category | unit_price, sale_price | sum | PASS |
| CP-1340 | employee_name, order_type, customer_type | product_category | unit_price, sale_price | mean | PASS |
| CP-1341 | employee_name, order_type, customer_type | product_category | unit_price, sale_price | count | PASS |
| CP-1342 | employee_name, order_type, customer_type | product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-1343 | employee_name, order_type, customer_type | product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-1344 | employee_name, order_type, customer_type | product_category | quantity, unit_price, sale_price | count | PASS |
| CP-1345 | employee_name, order_type | product_category, customer_type | quantity | sum | PASS |
| CP-1346 | employee_name, order_type | product_category, customer_type | quantity | mean | PASS |
| CP-1347 | employee_name, order_type | product_category, customer_type | quantity | count | PASS |
| CP-1348 | employee_name, order_type | product_category, customer_type | unit_price | sum | PASS |
| CP-1349 | employee_name, order_type | product_category, customer_type | unit_price | mean | PASS |
| CP-1350 | employee_name, order_type | product_category, customer_type | unit_price | count | PASS |
| CP-1351 | employee_name, order_type | product_category, customer_type | quantity, unit_price | sum | PASS |
| CP-1352 | employee_name, order_type | product_category, customer_type | quantity, unit_price | mean | PASS |
| CP-1353 | employee_name, order_type | product_category, customer_type | quantity, unit_price | count | PASS |
| CP-1354 | employee_name, order_type | product_category, customer_type | sale_price | sum | PASS |
| CP-1355 | employee_name, order_type | product_category, customer_type | sale_price | mean | PASS |
| CP-1356 | employee_name, order_type | product_category, customer_type | sale_price | count | PASS |
| CP-1357 | employee_name, order_type | product_category, customer_type | quantity, sale_price | sum | PASS |
| CP-1358 | employee_name, order_type | product_category, customer_type | quantity, sale_price | mean | PASS |
| CP-1359 | employee_name, order_type | product_category, customer_type | quantity, sale_price | count | PASS |
| CP-1360 | employee_name, order_type | product_category, customer_type | unit_price, sale_price | sum | PASS |
| CP-1361 | employee_name, order_type | product_category, customer_type | unit_price, sale_price | mean | PASS |
| CP-1362 | employee_name, order_type | product_category, customer_type | unit_price, sale_price | count | PASS |
| CP-1363 | employee_name, order_type | product_category, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1364 | employee_name, order_type | product_category, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1365 | employee_name, order_type | product_category, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-1366 | employee_name, order_type | product_category | quantity | sum | PASS |
| CP-1367 | employee_name, order_type | product_category | quantity | mean | PASS |
| CP-1368 | employee_name, order_type | product_category | quantity | count | PASS |
| CP-1369 | employee_name, order_type | product_category | unit_price | sum | PASS |
| CP-1370 | employee_name, order_type | product_category | unit_price | mean | PASS |
| CP-1371 | employee_name, order_type | product_category | unit_price | count | PASS |
| CP-1372 | employee_name, order_type | product_category | quantity, unit_price | sum | PASS |
| CP-1373 | employee_name, order_type | product_category | quantity, unit_price | mean | PASS |
| CP-1374 | employee_name, order_type | product_category | quantity, unit_price | count | PASS |
| CP-1375 | employee_name, order_type | product_category | sale_price | sum | PASS |
| CP-1376 | employee_name, order_type | product_category | sale_price | mean | PASS |
| CP-1377 | employee_name, order_type | product_category | sale_price | count | PASS |
| CP-1378 | employee_name, order_type | product_category | quantity, sale_price | sum | PASS |
| CP-1379 | employee_name, order_type | product_category | quantity, sale_price | mean | PASS |
| CP-1380 | employee_name, order_type | product_category | quantity, sale_price | count | PASS |
| CP-1381 | employee_name, order_type | product_category | unit_price, sale_price | sum | PASS |
| CP-1382 | employee_name, order_type | product_category | unit_price, sale_price | mean | PASS |
| CP-1383 | employee_name, order_type | product_category | unit_price, sale_price | count | PASS |
| CP-1384 | employee_name, order_type | product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-1385 | employee_name, order_type | product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-1386 | employee_name, order_type | product_category | quantity, unit_price, sale_price | count | PASS |
| CP-1387 | employee_name, customer_type | product_category, order_type | quantity | sum | PASS |
| CP-1388 | employee_name, customer_type | product_category, order_type | quantity | mean | PASS |
| CP-1389 | employee_name, customer_type | product_category, order_type | quantity | count | PASS |
| CP-1390 | employee_name, customer_type | product_category, order_type | unit_price | sum | PASS |
| CP-1391 | employee_name, customer_type | product_category, order_type | unit_price | mean | PASS |
| CP-1392 | employee_name, customer_type | product_category, order_type | unit_price | count | PASS |
| CP-1393 | employee_name, customer_type | product_category, order_type | quantity, unit_price | sum | PASS |
| CP-1394 | employee_name, customer_type | product_category, order_type | quantity, unit_price | mean | PASS |
| CP-1395 | employee_name, customer_type | product_category, order_type | quantity, unit_price | count | PASS |
| CP-1396 | employee_name, customer_type | product_category, order_type | sale_price | sum | PASS |
| CP-1397 | employee_name, customer_type | product_category, order_type | sale_price | mean | PASS |
| CP-1398 | employee_name, customer_type | product_category, order_type | sale_price | count | PASS |
| CP-1399 | employee_name, customer_type | product_category, order_type | quantity, sale_price | sum | PASS |
| CP-1400 | employee_name, customer_type | product_category, order_type | quantity, sale_price | mean | PASS |
| CP-1401 | employee_name, customer_type | product_category, order_type | quantity, sale_price | count | PASS |
| CP-1402 | employee_name, customer_type | product_category, order_type | unit_price, sale_price | sum | PASS |
| CP-1403 | employee_name, customer_type | product_category, order_type | unit_price, sale_price | mean | PASS |
| CP-1404 | employee_name, customer_type | product_category, order_type | unit_price, sale_price | count | PASS |
| CP-1405 | employee_name, customer_type | product_category, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1406 | employee_name, customer_type | product_category, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1407 | employee_name, customer_type | product_category, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-1408 | employee_name | product_category, order_type, customer_type | quantity | sum | PASS |
| CP-1409 | employee_name | product_category, order_type, customer_type | quantity | mean | PASS |
| CP-1410 | employee_name | product_category, order_type, customer_type | quantity | count | PASS |
| CP-1411 | employee_name | product_category, order_type, customer_type | unit_price | sum | PASS |
| CP-1412 | employee_name | product_category, order_type, customer_type | unit_price | mean | PASS |
| CP-1413 | employee_name | product_category, order_type, customer_type | unit_price | count | PASS |
| CP-1414 | employee_name | product_category, order_type, customer_type | quantity, unit_price | sum | PASS |
| CP-1415 | employee_name | product_category, order_type, customer_type | quantity, unit_price | mean | PASS |
| CP-1416 | employee_name | product_category, order_type, customer_type | quantity, unit_price | count | PASS |
| CP-1417 | employee_name | product_category, order_type, customer_type | sale_price | sum | PASS |
| CP-1418 | employee_name | product_category, order_type, customer_type | sale_price | mean | PASS |
| CP-1419 | employee_name | product_category, order_type, customer_type | sale_price | count | PASS |
| CP-1420 | employee_name | product_category, order_type, customer_type | quantity, sale_price | sum | PASS |
| CP-1421 | employee_name | product_category, order_type, customer_type | quantity, sale_price | mean | PASS |
| CP-1422 | employee_name | product_category, order_type, customer_type | quantity, sale_price | count | PASS |
| CP-1423 | employee_name | product_category, order_type, customer_type | unit_price, sale_price | sum | PASS |
| CP-1424 | employee_name | product_category, order_type, customer_type | unit_price, sale_price | mean | PASS |
| CP-1425 | employee_name | product_category, order_type, customer_type | unit_price, sale_price | count | PASS |
| CP-1426 | employee_name | product_category, order_type, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1427 | employee_name | product_category, order_type, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1428 | employee_name | product_category, order_type, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-1429 | employee_name | product_category, order_type | quantity | sum | PASS |
| CP-1430 | employee_name | product_category, order_type | quantity | mean | PASS |
| CP-1431 | employee_name | product_category, order_type | quantity | count | PASS |
| CP-1432 | employee_name | product_category, order_type | unit_price | sum | PASS |
| CP-1433 | employee_name | product_category, order_type | unit_price | mean | PASS |
| CP-1434 | employee_name | product_category, order_type | unit_price | count | PASS |
| CP-1435 | employee_name | product_category, order_type | quantity, unit_price | sum | PASS |
| CP-1436 | employee_name | product_category, order_type | quantity, unit_price | mean | PASS |
| CP-1437 | employee_name | product_category, order_type | quantity, unit_price | count | PASS |
| CP-1438 | employee_name | product_category, order_type | sale_price | sum | PASS |
| CP-1439 | employee_name | product_category, order_type | sale_price | mean | PASS |
| CP-1440 | employee_name | product_category, order_type | sale_price | count | PASS |
| CP-1441 | employee_name | product_category, order_type | quantity, sale_price | sum | PASS |
| CP-1442 | employee_name | product_category, order_type | quantity, sale_price | mean | PASS |
| CP-1443 | employee_name | product_category, order_type | quantity, sale_price | count | PASS |
| CP-1444 | employee_name | product_category, order_type | unit_price, sale_price | sum | PASS |
| CP-1445 | employee_name | product_category, order_type | unit_price, sale_price | mean | PASS |
| CP-1446 | employee_name | product_category, order_type | unit_price, sale_price | count | PASS |
| CP-1447 | employee_name | product_category, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1448 | employee_name | product_category, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1449 | employee_name | product_category, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-1450 | employee_name, customer_type | product_category | quantity | sum | PASS |
| CP-1451 | employee_name, customer_type | product_category | quantity | mean | PASS |
| CP-1452 | employee_name, customer_type | product_category | quantity | count | PASS |
| CP-1453 | employee_name, customer_type | product_category | unit_price | sum | PASS |
| CP-1454 | employee_name, customer_type | product_category | unit_price | mean | PASS |
| CP-1455 | employee_name, customer_type | product_category | unit_price | count | PASS |
| CP-1456 | employee_name, customer_type | product_category | quantity, unit_price | sum | PASS |
| CP-1457 | employee_name, customer_type | product_category | quantity, unit_price | mean | PASS |
| CP-1458 | employee_name, customer_type | product_category | quantity, unit_price | count | PASS |
| CP-1459 | employee_name, customer_type | product_category | sale_price | sum | PASS |
| CP-1460 | employee_name, customer_type | product_category | sale_price | mean | PASS |
| CP-1461 | employee_name, customer_type | product_category | sale_price | count | PASS |
| CP-1462 | employee_name, customer_type | product_category | quantity, sale_price | sum | PASS |
| CP-1463 | employee_name, customer_type | product_category | quantity, sale_price | mean | PASS |
| CP-1464 | employee_name, customer_type | product_category | quantity, sale_price | count | PASS |
| CP-1465 | employee_name, customer_type | product_category | unit_price, sale_price | sum | PASS |
| CP-1466 | employee_name, customer_type | product_category | unit_price, sale_price | mean | PASS |
| CP-1467 | employee_name, customer_type | product_category | unit_price, sale_price | count | PASS |
| CP-1468 | employee_name, customer_type | product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-1469 | employee_name, customer_type | product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-1470 | employee_name, customer_type | product_category | quantity, unit_price, sale_price | count | PASS |
| CP-1471 | employee_name | product_category, customer_type | quantity | sum | PASS |
| CP-1472 | employee_name | product_category, customer_type | quantity | mean | PASS |
| CP-1473 | employee_name | product_category, customer_type | quantity | count | PASS |
| CP-1474 | employee_name | product_category, customer_type | unit_price | sum | PASS |
| CP-1475 | employee_name | product_category, customer_type | unit_price | mean | PASS |
| CP-1476 | employee_name | product_category, customer_type | unit_price | count | PASS |
| CP-1477 | employee_name | product_category, customer_type | quantity, unit_price | sum | PASS |
| CP-1478 | employee_name | product_category, customer_type | quantity, unit_price | mean | PASS |
| CP-1479 | employee_name | product_category, customer_type | quantity, unit_price | count | PASS |
| CP-1480 | employee_name | product_category, customer_type | sale_price | sum | PASS |
| CP-1481 | employee_name | product_category, customer_type | sale_price | mean | PASS |
| CP-1482 | employee_name | product_category, customer_type | sale_price | count | PASS |
| CP-1483 | employee_name | product_category, customer_type | quantity, sale_price | sum | PASS |
| CP-1484 | employee_name | product_category, customer_type | quantity, sale_price | mean | PASS |
| CP-1485 | employee_name | product_category, customer_type | quantity, sale_price | count | PASS |
| CP-1486 | employee_name | product_category, customer_type | unit_price, sale_price | sum | PASS |
| CP-1487 | employee_name | product_category, customer_type | unit_price, sale_price | mean | PASS |
| CP-1488 | employee_name | product_category, customer_type | unit_price, sale_price | count | PASS |
| CP-1489 | employee_name | product_category, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1490 | employee_name | product_category, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1491 | employee_name | product_category, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-1492 | employee_name | product_category | quantity | sum | PASS |
| CP-1493 | employee_name | product_category | quantity | mean | PASS |
| CP-1494 | employee_name | product_category | quantity | count | PASS |
| CP-1495 | employee_name | product_category | unit_price | sum | PASS |
| CP-1496 | employee_name | product_category | unit_price | mean | PASS |
| CP-1497 | employee_name | product_category | unit_price | count | PASS |
| CP-1498 | employee_name | product_category | quantity, unit_price | sum | PASS |
| CP-1499 | employee_name | product_category | quantity, unit_price | mean | PASS |
| CP-1500 | employee_name | product_category | quantity, unit_price | count | PASS |
| CP-1501 | employee_name | product_category | sale_price | sum | PASS |
| CP-1502 | employee_name | product_category | sale_price | mean | PASS |
| CP-1503 | employee_name | product_category | sale_price | count | PASS |
| CP-1504 | employee_name | product_category | quantity, sale_price | sum | PASS |
| CP-1505 | employee_name | product_category | quantity, sale_price | mean | PASS |
| CP-1506 | employee_name | product_category | quantity, sale_price | count | PASS |
| CP-1507 | employee_name | product_category | unit_price, sale_price | sum | PASS |
| CP-1508 | employee_name | product_category | unit_price, sale_price | mean | PASS |
| CP-1509 | employee_name | product_category | unit_price, sale_price | count | PASS |
| CP-1510 | employee_name | product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-1511 | employee_name | product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-1512 | employee_name | product_category | quantity, unit_price, sale_price | count | PASS |
| CP-1513 | employee_name, order_type, customer_type | - | quantity | sum | PASS |
| CP-1514 | employee_name, order_type, customer_type | - | quantity | mean | PASS |
| CP-1515 | employee_name, order_type, customer_type | - | quantity | count | PASS |
| CP-1516 | employee_name, order_type, customer_type | - | unit_price | sum | PASS |
| CP-1517 | employee_name, order_type, customer_type | - | unit_price | mean | PASS |
| CP-1518 | employee_name, order_type, customer_type | - | unit_price | count | PASS |
| CP-1519 | employee_name, order_type, customer_type | - | quantity, unit_price | sum | PASS |
| CP-1520 | employee_name, order_type, customer_type | - | quantity, unit_price | mean | PASS |
| CP-1521 | employee_name, order_type, customer_type | - | quantity, unit_price | count | PASS |
| CP-1522 | employee_name, order_type, customer_type | - | sale_price | sum | PASS |
| CP-1523 | employee_name, order_type, customer_type | - | sale_price | mean | PASS |
| CP-1524 | employee_name, order_type, customer_type | - | sale_price | count | PASS |
| CP-1525 | employee_name, order_type, customer_type | - | quantity, sale_price | sum | PASS |
| CP-1526 | employee_name, order_type, customer_type | - | quantity, sale_price | mean | PASS |
| CP-1527 | employee_name, order_type, customer_type | - | quantity, sale_price | count | PASS |
| CP-1528 | employee_name, order_type, customer_type | - | unit_price, sale_price | sum | PASS |
| CP-1529 | employee_name, order_type, customer_type | - | unit_price, sale_price | mean | PASS |
| CP-1530 | employee_name, order_type, customer_type | - | unit_price, sale_price | count | PASS |
| CP-1531 | employee_name, order_type, customer_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-1532 | employee_name, order_type, customer_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-1533 | employee_name, order_type, customer_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-1534 | employee_name, order_type | customer_type | quantity | sum | PASS |
| CP-1535 | employee_name, order_type | customer_type | quantity | mean | PASS |
| CP-1536 | employee_name, order_type | customer_type | quantity | count | PASS |
| CP-1537 | employee_name, order_type | customer_type | unit_price | sum | PASS |
| CP-1538 | employee_name, order_type | customer_type | unit_price | mean | PASS |
| CP-1539 | employee_name, order_type | customer_type | unit_price | count | PASS |
| CP-1540 | employee_name, order_type | customer_type | quantity, unit_price | sum | PASS |
| CP-1541 | employee_name, order_type | customer_type | quantity, unit_price | mean | PASS |
| CP-1542 | employee_name, order_type | customer_type | quantity, unit_price | count | PASS |
| CP-1543 | employee_name, order_type | customer_type | sale_price | sum | PASS |
| CP-1544 | employee_name, order_type | customer_type | sale_price | mean | PASS |
| CP-1545 | employee_name, order_type | customer_type | sale_price | count | PASS |
| CP-1546 | employee_name, order_type | customer_type | quantity, sale_price | sum | PASS |
| CP-1547 | employee_name, order_type | customer_type | quantity, sale_price | mean | PASS |
| CP-1548 | employee_name, order_type | customer_type | quantity, sale_price | count | PASS |
| CP-1549 | employee_name, order_type | customer_type | unit_price, sale_price | sum | PASS |
| CP-1550 | employee_name, order_type | customer_type | unit_price, sale_price | mean | PASS |
| CP-1551 | employee_name, order_type | customer_type | unit_price, sale_price | count | PASS |
| CP-1552 | employee_name, order_type | customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1553 | employee_name, order_type | customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1554 | employee_name, order_type | customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-1555 | employee_name, order_type | - | quantity | sum | PASS |
| CP-1556 | employee_name, order_type | - | quantity | mean | PASS |
| CP-1557 | employee_name, order_type | - | quantity | count | PASS |
| CP-1558 | employee_name, order_type | - | unit_price | sum | PASS |
| CP-1559 | employee_name, order_type | - | unit_price | mean | PASS |
| CP-1560 | employee_name, order_type | - | unit_price | count | PASS |
| CP-1561 | employee_name, order_type | - | quantity, unit_price | sum | PASS |
| CP-1562 | employee_name, order_type | - | quantity, unit_price | mean | PASS |
| CP-1563 | employee_name, order_type | - | quantity, unit_price | count | PASS |
| CP-1564 | employee_name, order_type | - | sale_price | sum | PASS |
| CP-1565 | employee_name, order_type | - | sale_price | mean | PASS |
| CP-1566 | employee_name, order_type | - | sale_price | count | PASS |
| CP-1567 | employee_name, order_type | - | quantity, sale_price | sum | PASS |
| CP-1568 | employee_name, order_type | - | quantity, sale_price | mean | PASS |
| CP-1569 | employee_name, order_type | - | quantity, sale_price | count | PASS |
| CP-1570 | employee_name, order_type | - | unit_price, sale_price | sum | PASS |
| CP-1571 | employee_name, order_type | - | unit_price, sale_price | mean | PASS |
| CP-1572 | employee_name, order_type | - | unit_price, sale_price | count | PASS |
| CP-1573 | employee_name, order_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-1574 | employee_name, order_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-1575 | employee_name, order_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-1576 | employee_name, customer_type | order_type | quantity | sum | PASS |
| CP-1577 | employee_name, customer_type | order_type | quantity | mean | PASS |
| CP-1578 | employee_name, customer_type | order_type | quantity | count | PASS |
| CP-1579 | employee_name, customer_type | order_type | unit_price | sum | PASS |
| CP-1580 | employee_name, customer_type | order_type | unit_price | mean | PASS |
| CP-1581 | employee_name, customer_type | order_type | unit_price | count | PASS |
| CP-1582 | employee_name, customer_type | order_type | quantity, unit_price | sum | PASS |
| CP-1583 | employee_name, customer_type | order_type | quantity, unit_price | mean | PASS |
| CP-1584 | employee_name, customer_type | order_type | quantity, unit_price | count | PASS |
| CP-1585 | employee_name, customer_type | order_type | sale_price | sum | PASS |
| CP-1586 | employee_name, customer_type | order_type | sale_price | mean | PASS |
| CP-1587 | employee_name, customer_type | order_type | sale_price | count | PASS |
| CP-1588 | employee_name, customer_type | order_type | quantity, sale_price | sum | PASS |
| CP-1589 | employee_name, customer_type | order_type | quantity, sale_price | mean | PASS |
| CP-1590 | employee_name, customer_type | order_type | quantity, sale_price | count | PASS |
| CP-1591 | employee_name, customer_type | order_type | unit_price, sale_price | sum | PASS |
| CP-1592 | employee_name, customer_type | order_type | unit_price, sale_price | mean | PASS |
| CP-1593 | employee_name, customer_type | order_type | unit_price, sale_price | count | PASS |
| CP-1594 | employee_name, customer_type | order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1595 | employee_name, customer_type | order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1596 | employee_name, customer_type | order_type | quantity, unit_price, sale_price | count | PASS |
| CP-1597 | employee_name | order_type, customer_type | quantity | sum | PASS |
| CP-1598 | employee_name | order_type, customer_type | quantity | mean | PASS |
| CP-1599 | employee_name | order_type, customer_type | quantity | count | PASS |
| CP-1600 | employee_name | order_type, customer_type | unit_price | sum | PASS |
| CP-1601 | employee_name | order_type, customer_type | unit_price | mean | PASS |
| CP-1602 | employee_name | order_type, customer_type | unit_price | count | PASS |
| CP-1603 | employee_name | order_type, customer_type | quantity, unit_price | sum | PASS |
| CP-1604 | employee_name | order_type, customer_type | quantity, unit_price | mean | PASS |
| CP-1605 | employee_name | order_type, customer_type | quantity, unit_price | count | PASS |
| CP-1606 | employee_name | order_type, customer_type | sale_price | sum | PASS |
| CP-1607 | employee_name | order_type, customer_type | sale_price | mean | PASS |
| CP-1608 | employee_name | order_type, customer_type | sale_price | count | PASS |
| CP-1609 | employee_name | order_type, customer_type | quantity, sale_price | sum | PASS |
| CP-1610 | employee_name | order_type, customer_type | quantity, sale_price | mean | PASS |
| CP-1611 | employee_name | order_type, customer_type | quantity, sale_price | count | PASS |
| CP-1612 | employee_name | order_type, customer_type | unit_price, sale_price | sum | PASS |
| CP-1613 | employee_name | order_type, customer_type | unit_price, sale_price | mean | PASS |
| CP-1614 | employee_name | order_type, customer_type | unit_price, sale_price | count | PASS |
| CP-1615 | employee_name | order_type, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1616 | employee_name | order_type, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1617 | employee_name | order_type, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-1618 | employee_name | order_type | quantity | sum | PASS |
| CP-1619 | employee_name | order_type | quantity | mean | PASS |
| CP-1620 | employee_name | order_type | quantity | count | PASS |
| CP-1621 | employee_name | order_type | unit_price | sum | PASS |
| CP-1622 | employee_name | order_type | unit_price | mean | PASS |
| CP-1623 | employee_name | order_type | unit_price | count | PASS |
| CP-1624 | employee_name | order_type | quantity, unit_price | sum | PASS |
| CP-1625 | employee_name | order_type | quantity, unit_price | mean | PASS |
| CP-1626 | employee_name | order_type | quantity, unit_price | count | PASS |
| CP-1627 | employee_name | order_type | sale_price | sum | PASS |
| CP-1628 | employee_name | order_type | sale_price | mean | PASS |
| CP-1629 | employee_name | order_type | sale_price | count | PASS |
| CP-1630 | employee_name | order_type | quantity, sale_price | sum | PASS |
| CP-1631 | employee_name | order_type | quantity, sale_price | mean | PASS |
| CP-1632 | employee_name | order_type | quantity, sale_price | count | PASS |
| CP-1633 | employee_name | order_type | unit_price, sale_price | sum | PASS |
| CP-1634 | employee_name | order_type | unit_price, sale_price | mean | PASS |
| CP-1635 | employee_name | order_type | unit_price, sale_price | count | PASS |
| CP-1636 | employee_name | order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1637 | employee_name | order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1638 | employee_name | order_type | quantity, unit_price, sale_price | count | PASS |
| CP-1639 | employee_name, customer_type | - | quantity | sum | PASS |
| CP-1640 | employee_name, customer_type | - | quantity | mean | PASS |
| CP-1641 | employee_name, customer_type | - | quantity | count | PASS |
| CP-1642 | employee_name, customer_type | - | unit_price | sum | PASS |
| CP-1643 | employee_name, customer_type | - | unit_price | mean | PASS |
| CP-1644 | employee_name, customer_type | - | unit_price | count | PASS |
| CP-1645 | employee_name, customer_type | - | quantity, unit_price | sum | PASS |
| CP-1646 | employee_name, customer_type | - | quantity, unit_price | mean | PASS |
| CP-1647 | employee_name, customer_type | - | quantity, unit_price | count | PASS |
| CP-1648 | employee_name, customer_type | - | sale_price | sum | PASS |
| CP-1649 | employee_name, customer_type | - | sale_price | mean | PASS |
| CP-1650 | employee_name, customer_type | - | sale_price | count | PASS |
| CP-1651 | employee_name, customer_type | - | quantity, sale_price | sum | PASS |
| CP-1652 | employee_name, customer_type | - | quantity, sale_price | mean | PASS |
| CP-1653 | employee_name, customer_type | - | quantity, sale_price | count | PASS |
| CP-1654 | employee_name, customer_type | - | unit_price, sale_price | sum | PASS |
| CP-1655 | employee_name, customer_type | - | unit_price, sale_price | mean | PASS |
| CP-1656 | employee_name, customer_type | - | unit_price, sale_price | count | PASS |
| CP-1657 | employee_name, customer_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-1658 | employee_name, customer_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-1659 | employee_name, customer_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-1660 | employee_name | customer_type | quantity | sum | PASS |
| CP-1661 | employee_name | customer_type | quantity | mean | PASS |
| CP-1662 | employee_name | customer_type | quantity | count | PASS |
| CP-1663 | employee_name | customer_type | unit_price | sum | PASS |
| CP-1664 | employee_name | customer_type | unit_price | mean | PASS |
| CP-1665 | employee_name | customer_type | unit_price | count | PASS |
| CP-1666 | employee_name | customer_type | quantity, unit_price | sum | PASS |
| CP-1667 | employee_name | customer_type | quantity, unit_price | mean | PASS |
| CP-1668 | employee_name | customer_type | quantity, unit_price | count | PASS |
| CP-1669 | employee_name | customer_type | sale_price | sum | PASS |
| CP-1670 | employee_name | customer_type | sale_price | mean | PASS |
| CP-1671 | employee_name | customer_type | sale_price | count | PASS |
| CP-1672 | employee_name | customer_type | quantity, sale_price | sum | PASS |
| CP-1673 | employee_name | customer_type | quantity, sale_price | mean | PASS |
| CP-1674 | employee_name | customer_type | quantity, sale_price | count | PASS |
| CP-1675 | employee_name | customer_type | unit_price, sale_price | sum | PASS |
| CP-1676 | employee_name | customer_type | unit_price, sale_price | mean | PASS |
| CP-1677 | employee_name | customer_type | unit_price, sale_price | count | PASS |
| CP-1678 | employee_name | customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1679 | employee_name | customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1680 | employee_name | customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-1681 | employee_name | - | quantity | sum | PASS |
| CP-1682 | employee_name | - | quantity | mean | PASS |
| CP-1683 | employee_name | - | quantity | count | PASS |
| CP-1684 | employee_name | - | unit_price | sum | PASS |
| CP-1685 | employee_name | - | unit_price | mean | PASS |
| CP-1686 | employee_name | - | unit_price | count | PASS |
| CP-1687 | employee_name | - | quantity, unit_price | sum | PASS |
| CP-1688 | employee_name | - | quantity, unit_price | mean | PASS |
| CP-1689 | employee_name | - | quantity, unit_price | count | PASS |
| CP-1690 | employee_name | - | sale_price | sum | PASS |
| CP-1691 | employee_name | - | sale_price | mean | PASS |
| CP-1692 | employee_name | - | sale_price | count | PASS |
| CP-1693 | employee_name | - | quantity, sale_price | sum | PASS |
| CP-1694 | employee_name | - | quantity, sale_price | mean | PASS |
| CP-1695 | employee_name | - | quantity, sale_price | count | PASS |
| CP-1696 | employee_name | - | unit_price, sale_price | sum | PASS |
| CP-1697 | employee_name | - | unit_price, sale_price | mean | PASS |
| CP-1698 | employee_name | - | unit_price, sale_price | count | PASS |
| CP-1699 | employee_name | - | quantity, unit_price, sale_price | sum | PASS |
| CP-1700 | employee_name | - | quantity, unit_price, sale_price | mean | PASS |
| CP-1701 | employee_name | - | quantity, unit_price, sale_price | count | PASS |
| CP-1702 | sales_region, product_category, order_type, customer_type | employee_name | quantity | sum | PASS |
| CP-1703 | sales_region, product_category, order_type, customer_type | employee_name | quantity | mean | PASS |
| CP-1704 | sales_region, product_category, order_type, customer_type | employee_name | quantity | count | PASS |
| CP-1705 | sales_region, product_category, order_type, customer_type | employee_name | unit_price | sum | PASS |
| CP-1706 | sales_region, product_category, order_type, customer_type | employee_name | unit_price | mean | PASS |
| CP-1707 | sales_region, product_category, order_type, customer_type | employee_name | unit_price | count | PASS |
| CP-1708 | sales_region, product_category, order_type, customer_type | employee_name | quantity, unit_price | sum | PASS |
| CP-1709 | sales_region, product_category, order_type, customer_type | employee_name | quantity, unit_price | mean | PASS |
| CP-1710 | sales_region, product_category, order_type, customer_type | employee_name | quantity, unit_price | count | PASS |
| CP-1711 | sales_region, product_category, order_type, customer_type | employee_name | sale_price | sum | PASS |
| CP-1712 | sales_region, product_category, order_type, customer_type | employee_name | sale_price | mean | PASS |
| CP-1713 | sales_region, product_category, order_type, customer_type | employee_name | sale_price | count | PASS |
| CP-1714 | sales_region, product_category, order_type, customer_type | employee_name | quantity, sale_price | sum | PASS |
| CP-1715 | sales_region, product_category, order_type, customer_type | employee_name | quantity, sale_price | mean | PASS |
| CP-1716 | sales_region, product_category, order_type, customer_type | employee_name | quantity, sale_price | count | PASS |
| CP-1717 | sales_region, product_category, order_type, customer_type | employee_name | unit_price, sale_price | sum | PASS |
| CP-1718 | sales_region, product_category, order_type, customer_type | employee_name | unit_price, sale_price | mean | PASS |
| CP-1719 | sales_region, product_category, order_type, customer_type | employee_name | unit_price, sale_price | count | PASS |
| CP-1720 | sales_region, product_category, order_type, customer_type | employee_name | quantity, unit_price, sale_price | sum | PASS |
| CP-1721 | sales_region, product_category, order_type, customer_type | employee_name | quantity, unit_price, sale_price | mean | PASS |
| CP-1722 | sales_region, product_category, order_type, customer_type | employee_name | quantity, unit_price, sale_price | count | PASS |
| CP-1723 | sales_region, product_category, order_type | employee_name, customer_type | quantity | sum | PASS |
| CP-1724 | sales_region, product_category, order_type | employee_name, customer_type | quantity | mean | PASS |
| CP-1725 | sales_region, product_category, order_type | employee_name, customer_type | quantity | count | PASS |
| CP-1726 | sales_region, product_category, order_type | employee_name, customer_type | unit_price | sum | PASS |
| CP-1727 | sales_region, product_category, order_type | employee_name, customer_type | unit_price | mean | PASS |
| CP-1728 | sales_region, product_category, order_type | employee_name, customer_type | unit_price | count | PASS |
| CP-1729 | sales_region, product_category, order_type | employee_name, customer_type | quantity, unit_price | sum | PASS |
| CP-1730 | sales_region, product_category, order_type | employee_name, customer_type | quantity, unit_price | mean | PASS |
| CP-1731 | sales_region, product_category, order_type | employee_name, customer_type | quantity, unit_price | count | PASS |
| CP-1732 | sales_region, product_category, order_type | employee_name, customer_type | sale_price | sum | PASS |
| CP-1733 | sales_region, product_category, order_type | employee_name, customer_type | sale_price | mean | PASS |
| CP-1734 | sales_region, product_category, order_type | employee_name, customer_type | sale_price | count | PASS |
| CP-1735 | sales_region, product_category, order_type | employee_name, customer_type | quantity, sale_price | sum | PASS |
| CP-1736 | sales_region, product_category, order_type | employee_name, customer_type | quantity, sale_price | mean | PASS |
| CP-1737 | sales_region, product_category, order_type | employee_name, customer_type | quantity, sale_price | count | PASS |
| CP-1738 | sales_region, product_category, order_type | employee_name, customer_type | unit_price, sale_price | sum | PASS |
| CP-1739 | sales_region, product_category, order_type | employee_name, customer_type | unit_price, sale_price | mean | PASS |
| CP-1740 | sales_region, product_category, order_type | employee_name, customer_type | unit_price, sale_price | count | PASS |
| CP-1741 | sales_region, product_category, order_type | employee_name, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1742 | sales_region, product_category, order_type | employee_name, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1743 | sales_region, product_category, order_type | employee_name, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-1744 | sales_region, product_category, order_type | employee_name | quantity | sum | PASS |
| CP-1745 | sales_region, product_category, order_type | employee_name | quantity | mean | PASS |
| CP-1746 | sales_region, product_category, order_type | employee_name | quantity | count | PASS |
| CP-1747 | sales_region, product_category, order_type | employee_name | unit_price | sum | PASS |
| CP-1748 | sales_region, product_category, order_type | employee_name | unit_price | mean | PASS |
| CP-1749 | sales_region, product_category, order_type | employee_name | unit_price | count | PASS |
| CP-1750 | sales_region, product_category, order_type | employee_name | quantity, unit_price | sum | PASS |
| CP-1751 | sales_region, product_category, order_type | employee_name | quantity, unit_price | mean | PASS |
| CP-1752 | sales_region, product_category, order_type | employee_name | quantity, unit_price | count | PASS |
| CP-1753 | sales_region, product_category, order_type | employee_name | sale_price | sum | PASS |
| CP-1754 | sales_region, product_category, order_type | employee_name | sale_price | mean | PASS |
| CP-1755 | sales_region, product_category, order_type | employee_name | sale_price | count | PASS |
| CP-1756 | sales_region, product_category, order_type | employee_name | quantity, sale_price | sum | PASS |
| CP-1757 | sales_region, product_category, order_type | employee_name | quantity, sale_price | mean | PASS |
| CP-1758 | sales_region, product_category, order_type | employee_name | quantity, sale_price | count | PASS |
| CP-1759 | sales_region, product_category, order_type | employee_name | unit_price, sale_price | sum | PASS |
| CP-1760 | sales_region, product_category, order_type | employee_name | unit_price, sale_price | mean | PASS |
| CP-1761 | sales_region, product_category, order_type | employee_name | unit_price, sale_price | count | PASS |
| CP-1762 | sales_region, product_category, order_type | employee_name | quantity, unit_price, sale_price | sum | PASS |
| CP-1763 | sales_region, product_category, order_type | employee_name | quantity, unit_price, sale_price | mean | PASS |
| CP-1764 | sales_region, product_category, order_type | employee_name | quantity, unit_price, sale_price | count | PASS |
| CP-1765 | sales_region, product_category, customer_type | employee_name, order_type | quantity | sum | PASS |
| CP-1766 | sales_region, product_category, customer_type | employee_name, order_type | quantity | mean | PASS |
| CP-1767 | sales_region, product_category, customer_type | employee_name, order_type | quantity | count | PASS |
| CP-1768 | sales_region, product_category, customer_type | employee_name, order_type | unit_price | sum | PASS |
| CP-1769 | sales_region, product_category, customer_type | employee_name, order_type | unit_price | mean | PASS |
| CP-1770 | sales_region, product_category, customer_type | employee_name, order_type | unit_price | count | PASS |
| CP-1771 | sales_region, product_category, customer_type | employee_name, order_type | quantity, unit_price | sum | PASS |
| CP-1772 | sales_region, product_category, customer_type | employee_name, order_type | quantity, unit_price | mean | PASS |
| CP-1773 | sales_region, product_category, customer_type | employee_name, order_type | quantity, unit_price | count | PASS |
| CP-1774 | sales_region, product_category, customer_type | employee_name, order_type | sale_price | sum | PASS |
| CP-1775 | sales_region, product_category, customer_type | employee_name, order_type | sale_price | mean | PASS |
| CP-1776 | sales_region, product_category, customer_type | employee_name, order_type | sale_price | count | PASS |
| CP-1777 | sales_region, product_category, customer_type | employee_name, order_type | quantity, sale_price | sum | PASS |
| CP-1778 | sales_region, product_category, customer_type | employee_name, order_type | quantity, sale_price | mean | PASS |
| CP-1779 | sales_region, product_category, customer_type | employee_name, order_type | quantity, sale_price | count | PASS |
| CP-1780 | sales_region, product_category, customer_type | employee_name, order_type | unit_price, sale_price | sum | PASS |
| CP-1781 | sales_region, product_category, customer_type | employee_name, order_type | unit_price, sale_price | mean | PASS |
| CP-1782 | sales_region, product_category, customer_type | employee_name, order_type | unit_price, sale_price | count | PASS |
| CP-1783 | sales_region, product_category, customer_type | employee_name, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1784 | sales_region, product_category, customer_type | employee_name, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1785 | sales_region, product_category, customer_type | employee_name, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-1786 | sales_region, product_category | employee_name, order_type, customer_type | quantity | sum | PASS |
| CP-1787 | sales_region, product_category | employee_name, order_type, customer_type | quantity | mean | PASS |
| CP-1788 | sales_region, product_category | employee_name, order_type, customer_type | quantity | count | PASS |
| CP-1789 | sales_region, product_category | employee_name, order_type, customer_type | unit_price | sum | PASS |
| CP-1790 | sales_region, product_category | employee_name, order_type, customer_type | unit_price | mean | PASS |
| CP-1791 | sales_region, product_category | employee_name, order_type, customer_type | unit_price | count | PASS |
| CP-1792 | sales_region, product_category | employee_name, order_type, customer_type | quantity, unit_price | sum | PASS |
| CP-1793 | sales_region, product_category | employee_name, order_type, customer_type | quantity, unit_price | mean | PASS |
| CP-1794 | sales_region, product_category | employee_name, order_type, customer_type | quantity, unit_price | count | PASS |
| CP-1795 | sales_region, product_category | employee_name, order_type, customer_type | sale_price | sum | PASS |
| CP-1796 | sales_region, product_category | employee_name, order_type, customer_type | sale_price | mean | PASS |
| CP-1797 | sales_region, product_category | employee_name, order_type, customer_type | sale_price | count | PASS |
| CP-1798 | sales_region, product_category | employee_name, order_type, customer_type | quantity, sale_price | sum | PASS |
| CP-1799 | sales_region, product_category | employee_name, order_type, customer_type | quantity, sale_price | mean | PASS |
| CP-1800 | sales_region, product_category | employee_name, order_type, customer_type | quantity, sale_price | count | PASS |
| CP-1801 | sales_region, product_category | employee_name, order_type, customer_type | unit_price, sale_price | sum | PASS |
| CP-1802 | sales_region, product_category | employee_name, order_type, customer_type | unit_price, sale_price | mean | PASS |
| CP-1803 | sales_region, product_category | employee_name, order_type, customer_type | unit_price, sale_price | count | PASS |
| CP-1804 | sales_region, product_category | employee_name, order_type, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1805 | sales_region, product_category | employee_name, order_type, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1806 | sales_region, product_category | employee_name, order_type, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-1807 | sales_region, product_category | employee_name, order_type | quantity | sum | PASS |
| CP-1808 | sales_region, product_category | employee_name, order_type | quantity | mean | PASS |
| CP-1809 | sales_region, product_category | employee_name, order_type | quantity | count | PASS |
| CP-1810 | sales_region, product_category | employee_name, order_type | unit_price | sum | PASS |
| CP-1811 | sales_region, product_category | employee_name, order_type | unit_price | mean | PASS |
| CP-1812 | sales_region, product_category | employee_name, order_type | unit_price | count | PASS |
| CP-1813 | sales_region, product_category | employee_name, order_type | quantity, unit_price | sum | PASS |
| CP-1814 | sales_region, product_category | employee_name, order_type | quantity, unit_price | mean | PASS |
| CP-1815 | sales_region, product_category | employee_name, order_type | quantity, unit_price | count | PASS |
| CP-1816 | sales_region, product_category | employee_name, order_type | sale_price | sum | PASS |
| CP-1817 | sales_region, product_category | employee_name, order_type | sale_price | mean | PASS |
| CP-1818 | sales_region, product_category | employee_name, order_type | sale_price | count | PASS |
| CP-1819 | sales_region, product_category | employee_name, order_type | quantity, sale_price | sum | PASS |
| CP-1820 | sales_region, product_category | employee_name, order_type | quantity, sale_price | mean | PASS |
| CP-1821 | sales_region, product_category | employee_name, order_type | quantity, sale_price | count | PASS |
| CP-1822 | sales_region, product_category | employee_name, order_type | unit_price, sale_price | sum | PASS |
| CP-1823 | sales_region, product_category | employee_name, order_type | unit_price, sale_price | mean | PASS |
| CP-1824 | sales_region, product_category | employee_name, order_type | unit_price, sale_price | count | PASS |
| CP-1825 | sales_region, product_category | employee_name, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1826 | sales_region, product_category | employee_name, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1827 | sales_region, product_category | employee_name, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-1828 | sales_region, product_category, customer_type | employee_name | quantity | sum | PASS |
| CP-1829 | sales_region, product_category, customer_type | employee_name | quantity | mean | PASS |
| CP-1830 | sales_region, product_category, customer_type | employee_name | quantity | count | PASS |
| CP-1831 | sales_region, product_category, customer_type | employee_name | unit_price | sum | PASS |
| CP-1832 | sales_region, product_category, customer_type | employee_name | unit_price | mean | PASS |
| CP-1833 | sales_region, product_category, customer_type | employee_name | unit_price | count | PASS |
| CP-1834 | sales_region, product_category, customer_type | employee_name | quantity, unit_price | sum | PASS |
| CP-1835 | sales_region, product_category, customer_type | employee_name | quantity, unit_price | mean | PASS |
| CP-1836 | sales_region, product_category, customer_type | employee_name | quantity, unit_price | count | PASS |
| CP-1837 | sales_region, product_category, customer_type | employee_name | sale_price | sum | PASS |
| CP-1838 | sales_region, product_category, customer_type | employee_name | sale_price | mean | PASS |
| CP-1839 | sales_region, product_category, customer_type | employee_name | sale_price | count | PASS |
| CP-1840 | sales_region, product_category, customer_type | employee_name | quantity, sale_price | sum | PASS |
| CP-1841 | sales_region, product_category, customer_type | employee_name | quantity, sale_price | mean | PASS |
| CP-1842 | sales_region, product_category, customer_type | employee_name | quantity, sale_price | count | PASS |
| CP-1843 | sales_region, product_category, customer_type | employee_name | unit_price, sale_price | sum | PASS |
| CP-1844 | sales_region, product_category, customer_type | employee_name | unit_price, sale_price | mean | PASS |
| CP-1845 | sales_region, product_category, customer_type | employee_name | unit_price, sale_price | count | PASS |
| CP-1846 | sales_region, product_category, customer_type | employee_name | quantity, unit_price, sale_price | sum | PASS |
| CP-1847 | sales_region, product_category, customer_type | employee_name | quantity, unit_price, sale_price | mean | PASS |
| CP-1848 | sales_region, product_category, customer_type | employee_name | quantity, unit_price, sale_price | count | PASS |
| CP-1849 | sales_region, product_category | employee_name, customer_type | quantity | sum | PASS |
| CP-1850 | sales_region, product_category | employee_name, customer_type | quantity | mean | PASS |
| CP-1851 | sales_region, product_category | employee_name, customer_type | quantity | count | PASS |
| CP-1852 | sales_region, product_category | employee_name, customer_type | unit_price | sum | PASS |
| CP-1853 | sales_region, product_category | employee_name, customer_type | unit_price | mean | PASS |
| CP-1854 | sales_region, product_category | employee_name, customer_type | unit_price | count | PASS |
| CP-1855 | sales_region, product_category | employee_name, customer_type | quantity, unit_price | sum | PASS |
| CP-1856 | sales_region, product_category | employee_name, customer_type | quantity, unit_price | mean | PASS |
| CP-1857 | sales_region, product_category | employee_name, customer_type | quantity, unit_price | count | PASS |
| CP-1858 | sales_region, product_category | employee_name, customer_type | sale_price | sum | PASS |
| CP-1859 | sales_region, product_category | employee_name, customer_type | sale_price | mean | PASS |
| CP-1860 | sales_region, product_category | employee_name, customer_type | sale_price | count | PASS |
| CP-1861 | sales_region, product_category | employee_name, customer_type | quantity, sale_price | sum | PASS |
| CP-1862 | sales_region, product_category | employee_name, customer_type | quantity, sale_price | mean | PASS |
| CP-1863 | sales_region, product_category | employee_name, customer_type | quantity, sale_price | count | PASS |
| CP-1864 | sales_region, product_category | employee_name, customer_type | unit_price, sale_price | sum | PASS |
| CP-1865 | sales_region, product_category | employee_name, customer_type | unit_price, sale_price | mean | PASS |
| CP-1866 | sales_region, product_category | employee_name, customer_type | unit_price, sale_price | count | PASS |
| CP-1867 | sales_region, product_category | employee_name, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1868 | sales_region, product_category | employee_name, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1869 | sales_region, product_category | employee_name, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-1870 | sales_region, product_category | employee_name | quantity | sum | PASS |
| CP-1871 | sales_region, product_category | employee_name | quantity | mean | PASS |
| CP-1872 | sales_region, product_category | employee_name | quantity | count | PASS |
| CP-1873 | sales_region, product_category | employee_name | unit_price | sum | PASS |
| CP-1874 | sales_region, product_category | employee_name | unit_price | mean | PASS |
| CP-1875 | sales_region, product_category | employee_name | unit_price | count | PASS |
| CP-1876 | sales_region, product_category | employee_name | quantity, unit_price | sum | PASS |
| CP-1877 | sales_region, product_category | employee_name | quantity, unit_price | mean | PASS |
| CP-1878 | sales_region, product_category | employee_name | quantity, unit_price | count | PASS |
| CP-1879 | sales_region, product_category | employee_name | sale_price | sum | PASS |
| CP-1880 | sales_region, product_category | employee_name | sale_price | mean | PASS |
| CP-1881 | sales_region, product_category | employee_name | sale_price | count | PASS |
| CP-1882 | sales_region, product_category | employee_name | quantity, sale_price | sum | PASS |
| CP-1883 | sales_region, product_category | employee_name | quantity, sale_price | mean | PASS |
| CP-1884 | sales_region, product_category | employee_name | quantity, sale_price | count | PASS |
| CP-1885 | sales_region, product_category | employee_name | unit_price, sale_price | sum | PASS |
| CP-1886 | sales_region, product_category | employee_name | unit_price, sale_price | mean | PASS |
| CP-1887 | sales_region, product_category | employee_name | unit_price, sale_price | count | PASS |
| CP-1888 | sales_region, product_category | employee_name | quantity, unit_price, sale_price | sum | PASS |
| CP-1889 | sales_region, product_category | employee_name | quantity, unit_price, sale_price | mean | PASS |
| CP-1890 | sales_region, product_category | employee_name | quantity, unit_price, sale_price | count | PASS |
| CP-1891 | sales_region, order_type, customer_type | employee_name, product_category | quantity | sum | PASS |
| CP-1892 | sales_region, order_type, customer_type | employee_name, product_category | quantity | mean | PASS |
| CP-1893 | sales_region, order_type, customer_type | employee_name, product_category | quantity | count | PASS |
| CP-1894 | sales_region, order_type, customer_type | employee_name, product_category | unit_price | sum | PASS |
| CP-1895 | sales_region, order_type, customer_type | employee_name, product_category | unit_price | mean | PASS |
| CP-1896 | sales_region, order_type, customer_type | employee_name, product_category | unit_price | count | PASS |
| CP-1897 | sales_region, order_type, customer_type | employee_name, product_category | quantity, unit_price | sum | PASS |
| CP-1898 | sales_region, order_type, customer_type | employee_name, product_category | quantity, unit_price | mean | PASS |
| CP-1899 | sales_region, order_type, customer_type | employee_name, product_category | quantity, unit_price | count | PASS |
| CP-1900 | sales_region, order_type, customer_type | employee_name, product_category | sale_price | sum | PASS |
| CP-1901 | sales_region, order_type, customer_type | employee_name, product_category | sale_price | mean | PASS |
| CP-1902 | sales_region, order_type, customer_type | employee_name, product_category | sale_price | count | PASS |
| CP-1903 | sales_region, order_type, customer_type | employee_name, product_category | quantity, sale_price | sum | PASS |
| CP-1904 | sales_region, order_type, customer_type | employee_name, product_category | quantity, sale_price | mean | PASS |
| CP-1905 | sales_region, order_type, customer_type | employee_name, product_category | quantity, sale_price | count | PASS |
| CP-1906 | sales_region, order_type, customer_type | employee_name, product_category | unit_price, sale_price | sum | PASS |
| CP-1907 | sales_region, order_type, customer_type | employee_name, product_category | unit_price, sale_price | mean | PASS |
| CP-1908 | sales_region, order_type, customer_type | employee_name, product_category | unit_price, sale_price | count | PASS |
| CP-1909 | sales_region, order_type, customer_type | employee_name, product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-1910 | sales_region, order_type, customer_type | employee_name, product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-1911 | sales_region, order_type, customer_type | employee_name, product_category | quantity, unit_price, sale_price | count | PASS |
| CP-1912 | sales_region, order_type | employee_name, product_category, customer_type | quantity | sum | PASS |
| CP-1913 | sales_region, order_type | employee_name, product_category, customer_type | quantity | mean | PASS |
| CP-1914 | sales_region, order_type | employee_name, product_category, customer_type | quantity | count | PASS |
| CP-1915 | sales_region, order_type | employee_name, product_category, customer_type | unit_price | sum | PASS |
| CP-1916 | sales_region, order_type | employee_name, product_category, customer_type | unit_price | mean | PASS |
| CP-1917 | sales_region, order_type | employee_name, product_category, customer_type | unit_price | count | PASS |
| CP-1918 | sales_region, order_type | employee_name, product_category, customer_type | quantity, unit_price | sum | PASS |
| CP-1919 | sales_region, order_type | employee_name, product_category, customer_type | quantity, unit_price | mean | PASS |
| CP-1920 | sales_region, order_type | employee_name, product_category, customer_type | quantity, unit_price | count | PASS |
| CP-1921 | sales_region, order_type | employee_name, product_category, customer_type | sale_price | sum | PASS |
| CP-1922 | sales_region, order_type | employee_name, product_category, customer_type | sale_price | mean | PASS |
| CP-1923 | sales_region, order_type | employee_name, product_category, customer_type | sale_price | count | PASS |
| CP-1924 | sales_region, order_type | employee_name, product_category, customer_type | quantity, sale_price | sum | PASS |
| CP-1925 | sales_region, order_type | employee_name, product_category, customer_type | quantity, sale_price | mean | PASS |
| CP-1926 | sales_region, order_type | employee_name, product_category, customer_type | quantity, sale_price | count | PASS |
| CP-1927 | sales_region, order_type | employee_name, product_category, customer_type | unit_price, sale_price | sum | PASS |
| CP-1928 | sales_region, order_type | employee_name, product_category, customer_type | unit_price, sale_price | mean | PASS |
| CP-1929 | sales_region, order_type | employee_name, product_category, customer_type | unit_price, sale_price | count | PASS |
| CP-1930 | sales_region, order_type | employee_name, product_category, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1931 | sales_region, order_type | employee_name, product_category, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1932 | sales_region, order_type | employee_name, product_category, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-1933 | sales_region, order_type | employee_name, product_category | quantity | sum | PASS |
| CP-1934 | sales_region, order_type | employee_name, product_category | quantity | mean | PASS |
| CP-1935 | sales_region, order_type | employee_name, product_category | quantity | count | PASS |
| CP-1936 | sales_region, order_type | employee_name, product_category | unit_price | sum | PASS |
| CP-1937 | sales_region, order_type | employee_name, product_category | unit_price | mean | PASS |
| CP-1938 | sales_region, order_type | employee_name, product_category | unit_price | count | PASS |
| CP-1939 | sales_region, order_type | employee_name, product_category | quantity, unit_price | sum | PASS |
| CP-1940 | sales_region, order_type | employee_name, product_category | quantity, unit_price | mean | PASS |
| CP-1941 | sales_region, order_type | employee_name, product_category | quantity, unit_price | count | PASS |
| CP-1942 | sales_region, order_type | employee_name, product_category | sale_price | sum | PASS |
| CP-1943 | sales_region, order_type | employee_name, product_category | sale_price | mean | PASS |
| CP-1944 | sales_region, order_type | employee_name, product_category | sale_price | count | PASS |
| CP-1945 | sales_region, order_type | employee_name, product_category | quantity, sale_price | sum | PASS |
| CP-1946 | sales_region, order_type | employee_name, product_category | quantity, sale_price | mean | PASS |
| CP-1947 | sales_region, order_type | employee_name, product_category | quantity, sale_price | count | PASS |
| CP-1948 | sales_region, order_type | employee_name, product_category | unit_price, sale_price | sum | PASS |
| CP-1949 | sales_region, order_type | employee_name, product_category | unit_price, sale_price | mean | PASS |
| CP-1950 | sales_region, order_type | employee_name, product_category | unit_price, sale_price | count | PASS |
| CP-1951 | sales_region, order_type | employee_name, product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-1952 | sales_region, order_type | employee_name, product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-1953 | sales_region, order_type | employee_name, product_category | quantity, unit_price, sale_price | count | PASS |
| CP-1954 | sales_region, customer_type | employee_name, product_category, order_type | quantity | sum | PASS |
| CP-1955 | sales_region, customer_type | employee_name, product_category, order_type | quantity | mean | PASS |
| CP-1956 | sales_region, customer_type | employee_name, product_category, order_type | quantity | count | PASS |
| CP-1957 | sales_region, customer_type | employee_name, product_category, order_type | unit_price | sum | PASS |
| CP-1958 | sales_region, customer_type | employee_name, product_category, order_type | unit_price | mean | PASS |
| CP-1959 | sales_region, customer_type | employee_name, product_category, order_type | unit_price | count | PASS |
| CP-1960 | sales_region, customer_type | employee_name, product_category, order_type | quantity, unit_price | sum | PASS |
| CP-1961 | sales_region, customer_type | employee_name, product_category, order_type | quantity, unit_price | mean | PASS |
| CP-1962 | sales_region, customer_type | employee_name, product_category, order_type | quantity, unit_price | count | PASS |
| CP-1963 | sales_region, customer_type | employee_name, product_category, order_type | sale_price | sum | PASS |
| CP-1964 | sales_region, customer_type | employee_name, product_category, order_type | sale_price | mean | PASS |
| CP-1965 | sales_region, customer_type | employee_name, product_category, order_type | sale_price | count | PASS |
| CP-1966 | sales_region, customer_type | employee_name, product_category, order_type | quantity, sale_price | sum | PASS |
| CP-1967 | sales_region, customer_type | employee_name, product_category, order_type | quantity, sale_price | mean | PASS |
| CP-1968 | sales_region, customer_type | employee_name, product_category, order_type | quantity, sale_price | count | PASS |
| CP-1969 | sales_region, customer_type | employee_name, product_category, order_type | unit_price, sale_price | sum | PASS |
| CP-1970 | sales_region, customer_type | employee_name, product_category, order_type | unit_price, sale_price | mean | PASS |
| CP-1971 | sales_region, customer_type | employee_name, product_category, order_type | unit_price, sale_price | count | PASS |
| CP-1972 | sales_region, customer_type | employee_name, product_category, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1973 | sales_region, customer_type | employee_name, product_category, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1974 | sales_region, customer_type | employee_name, product_category, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-1975 | sales_region | employee_name, product_category, order_type, customer_type | quantity | sum | PASS |
| CP-1976 | sales_region | employee_name, product_category, order_type, customer_type | quantity | mean | PASS |
| CP-1977 | sales_region | employee_name, product_category, order_type, customer_type | quantity | count | PASS |
| CP-1978 | sales_region | employee_name, product_category, order_type, customer_type | unit_price | sum | PASS |
| CP-1979 | sales_region | employee_name, product_category, order_type, customer_type | unit_price | mean | PASS |
| CP-1980 | sales_region | employee_name, product_category, order_type, customer_type | unit_price | count | PASS |
| CP-1981 | sales_region | employee_name, product_category, order_type, customer_type | quantity, unit_price | sum | PASS |
| CP-1982 | sales_region | employee_name, product_category, order_type, customer_type | quantity, unit_price | mean | PASS |
| CP-1983 | sales_region | employee_name, product_category, order_type, customer_type | quantity, unit_price | count | PASS |
| CP-1984 | sales_region | employee_name, product_category, order_type, customer_type | sale_price | sum | PASS |
| CP-1985 | sales_region | employee_name, product_category, order_type, customer_type | sale_price | mean | PASS |
| CP-1986 | sales_region | employee_name, product_category, order_type, customer_type | sale_price | count | PASS |
| CP-1987 | sales_region | employee_name, product_category, order_type, customer_type | quantity, sale_price | sum | PASS |
| CP-1988 | sales_region | employee_name, product_category, order_type, customer_type | quantity, sale_price | mean | PASS |
| CP-1989 | sales_region | employee_name, product_category, order_type, customer_type | quantity, sale_price | count | PASS |
| CP-1990 | sales_region | employee_name, product_category, order_type, customer_type | unit_price, sale_price | sum | PASS |
| CP-1991 | sales_region | employee_name, product_category, order_type, customer_type | unit_price, sale_price | mean | PASS |
| CP-1992 | sales_region | employee_name, product_category, order_type, customer_type | unit_price, sale_price | count | PASS |
| CP-1993 | sales_region | employee_name, product_category, order_type, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-1994 | sales_region | employee_name, product_category, order_type, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-1995 | sales_region | employee_name, product_category, order_type, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-1996 | sales_region | employee_name, product_category, order_type | quantity | sum | PASS |
| CP-1997 | sales_region | employee_name, product_category, order_type | quantity | mean | PASS |
| CP-1998 | sales_region | employee_name, product_category, order_type | quantity | count | PASS |
| CP-1999 | sales_region | employee_name, product_category, order_type | unit_price | sum | PASS |
| CP-2000 | sales_region | employee_name, product_category, order_type | unit_price | mean | PASS |
| CP-2001 | sales_region | employee_name, product_category, order_type | unit_price | count | PASS |
| CP-2002 | sales_region | employee_name, product_category, order_type | quantity, unit_price | sum | PASS |
| CP-2003 | sales_region | employee_name, product_category, order_type | quantity, unit_price | mean | PASS |
| CP-2004 | sales_region | employee_name, product_category, order_type | quantity, unit_price | count | PASS |
| CP-2005 | sales_region | employee_name, product_category, order_type | sale_price | sum | PASS |
| CP-2006 | sales_region | employee_name, product_category, order_type | sale_price | mean | PASS |
| CP-2007 | sales_region | employee_name, product_category, order_type | sale_price | count | PASS |
| CP-2008 | sales_region | employee_name, product_category, order_type | quantity, sale_price | sum | PASS |
| CP-2009 | sales_region | employee_name, product_category, order_type | quantity, sale_price | mean | PASS |
| CP-2010 | sales_region | employee_name, product_category, order_type | quantity, sale_price | count | PASS |
| CP-2011 | sales_region | employee_name, product_category, order_type | unit_price, sale_price | sum | PASS |
| CP-2012 | sales_region | employee_name, product_category, order_type | unit_price, sale_price | mean | PASS |
| CP-2013 | sales_region | employee_name, product_category, order_type | unit_price, sale_price | count | PASS |
| CP-2014 | sales_region | employee_name, product_category, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2015 | sales_region | employee_name, product_category, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2016 | sales_region | employee_name, product_category, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-2017 | sales_region, customer_type | employee_name, product_category | quantity | sum | PASS |
| CP-2018 | sales_region, customer_type | employee_name, product_category | quantity | mean | PASS |
| CP-2019 | sales_region, customer_type | employee_name, product_category | quantity | count | PASS |
| CP-2020 | sales_region, customer_type | employee_name, product_category | unit_price | sum | PASS |
| CP-2021 | sales_region, customer_type | employee_name, product_category | unit_price | mean | PASS |
| CP-2022 | sales_region, customer_type | employee_name, product_category | unit_price | count | PASS |
| CP-2023 | sales_region, customer_type | employee_name, product_category | quantity, unit_price | sum | PASS |
| CP-2024 | sales_region, customer_type | employee_name, product_category | quantity, unit_price | mean | PASS |
| CP-2025 | sales_region, customer_type | employee_name, product_category | quantity, unit_price | count | PASS |
| CP-2026 | sales_region, customer_type | employee_name, product_category | sale_price | sum | PASS |
| CP-2027 | sales_region, customer_type | employee_name, product_category | sale_price | mean | PASS |
| CP-2028 | sales_region, customer_type | employee_name, product_category | sale_price | count | PASS |
| CP-2029 | sales_region, customer_type | employee_name, product_category | quantity, sale_price | sum | PASS |
| CP-2030 | sales_region, customer_type | employee_name, product_category | quantity, sale_price | mean | PASS |
| CP-2031 | sales_region, customer_type | employee_name, product_category | quantity, sale_price | count | PASS |
| CP-2032 | sales_region, customer_type | employee_name, product_category | unit_price, sale_price | sum | PASS |
| CP-2033 | sales_region, customer_type | employee_name, product_category | unit_price, sale_price | mean | PASS |
| CP-2034 | sales_region, customer_type | employee_name, product_category | unit_price, sale_price | count | PASS |
| CP-2035 | sales_region, customer_type | employee_name, product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-2036 | sales_region, customer_type | employee_name, product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-2037 | sales_region, customer_type | employee_name, product_category | quantity, unit_price, sale_price | count | PASS |
| CP-2038 | sales_region | employee_name, product_category, customer_type | quantity | sum | PASS |
| CP-2039 | sales_region | employee_name, product_category, customer_type | quantity | mean | PASS |
| CP-2040 | sales_region | employee_name, product_category, customer_type | quantity | count | PASS |
| CP-2041 | sales_region | employee_name, product_category, customer_type | unit_price | sum | PASS |
| CP-2042 | sales_region | employee_name, product_category, customer_type | unit_price | mean | PASS |
| CP-2043 | sales_region | employee_name, product_category, customer_type | unit_price | count | PASS |
| CP-2044 | sales_region | employee_name, product_category, customer_type | quantity, unit_price | sum | PASS |
| CP-2045 | sales_region | employee_name, product_category, customer_type | quantity, unit_price | mean | PASS |
| CP-2046 | sales_region | employee_name, product_category, customer_type | quantity, unit_price | count | PASS |
| CP-2047 | sales_region | employee_name, product_category, customer_type | sale_price | sum | PASS |
| CP-2048 | sales_region | employee_name, product_category, customer_type | sale_price | mean | PASS |
| CP-2049 | sales_region | employee_name, product_category, customer_type | sale_price | count | PASS |
| CP-2050 | sales_region | employee_name, product_category, customer_type | quantity, sale_price | sum | PASS |
| CP-2051 | sales_region | employee_name, product_category, customer_type | quantity, sale_price | mean | PASS |
| CP-2052 | sales_region | employee_name, product_category, customer_type | quantity, sale_price | count | PASS |
| CP-2053 | sales_region | employee_name, product_category, customer_type | unit_price, sale_price | sum | PASS |
| CP-2054 | sales_region | employee_name, product_category, customer_type | unit_price, sale_price | mean | PASS |
| CP-2055 | sales_region | employee_name, product_category, customer_type | unit_price, sale_price | count | PASS |
| CP-2056 | sales_region | employee_name, product_category, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2057 | sales_region | employee_name, product_category, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2058 | sales_region | employee_name, product_category, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-2059 | sales_region | employee_name, product_category | quantity | sum | PASS |
| CP-2060 | sales_region | employee_name, product_category | quantity | mean | PASS |
| CP-2061 | sales_region | employee_name, product_category | quantity | count | PASS |
| CP-2062 | sales_region | employee_name, product_category | unit_price | sum | PASS |
| CP-2063 | sales_region | employee_name, product_category | unit_price | mean | PASS |
| CP-2064 | sales_region | employee_name, product_category | unit_price | count | PASS |
| CP-2065 | sales_region | employee_name, product_category | quantity, unit_price | sum | PASS |
| CP-2066 | sales_region | employee_name, product_category | quantity, unit_price | mean | PASS |
| CP-2067 | sales_region | employee_name, product_category | quantity, unit_price | count | PASS |
| CP-2068 | sales_region | employee_name, product_category | sale_price | sum | PASS |
| CP-2069 | sales_region | employee_name, product_category | sale_price | mean | PASS |
| CP-2070 | sales_region | employee_name, product_category | sale_price | count | PASS |
| CP-2071 | sales_region | employee_name, product_category | quantity, sale_price | sum | PASS |
| CP-2072 | sales_region | employee_name, product_category | quantity, sale_price | mean | PASS |
| CP-2073 | sales_region | employee_name, product_category | quantity, sale_price | count | PASS |
| CP-2074 | sales_region | employee_name, product_category | unit_price, sale_price | sum | PASS |
| CP-2075 | sales_region | employee_name, product_category | unit_price, sale_price | mean | PASS |
| CP-2076 | sales_region | employee_name, product_category | unit_price, sale_price | count | PASS |
| CP-2077 | sales_region | employee_name, product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-2078 | sales_region | employee_name, product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-2079 | sales_region | employee_name, product_category | quantity, unit_price, sale_price | count | PASS |
| CP-2080 | sales_region, order_type, customer_type | employee_name | quantity | sum | PASS |
| CP-2081 | sales_region, order_type, customer_type | employee_name | quantity | mean | PASS |
| CP-2082 | sales_region, order_type, customer_type | employee_name | quantity | count | PASS |
| CP-2083 | sales_region, order_type, customer_type | employee_name | unit_price | sum | PASS |
| CP-2084 | sales_region, order_type, customer_type | employee_name | unit_price | mean | PASS |
| CP-2085 | sales_region, order_type, customer_type | employee_name | unit_price | count | PASS |
| CP-2086 | sales_region, order_type, customer_type | employee_name | quantity, unit_price | sum | PASS |
| CP-2087 | sales_region, order_type, customer_type | employee_name | quantity, unit_price | mean | PASS |
| CP-2088 | sales_region, order_type, customer_type | employee_name | quantity, unit_price | count | PASS |
| CP-2089 | sales_region, order_type, customer_type | employee_name | sale_price | sum | PASS |
| CP-2090 | sales_region, order_type, customer_type | employee_name | sale_price | mean | PASS |
| CP-2091 | sales_region, order_type, customer_type | employee_name | sale_price | count | PASS |
| CP-2092 | sales_region, order_type, customer_type | employee_name | quantity, sale_price | sum | PASS |
| CP-2093 | sales_region, order_type, customer_type | employee_name | quantity, sale_price | mean | PASS |
| CP-2094 | sales_region, order_type, customer_type | employee_name | quantity, sale_price | count | PASS |
| CP-2095 | sales_region, order_type, customer_type | employee_name | unit_price, sale_price | sum | PASS |
| CP-2096 | sales_region, order_type, customer_type | employee_name | unit_price, sale_price | mean | PASS |
| CP-2097 | sales_region, order_type, customer_type | employee_name | unit_price, sale_price | count | PASS |
| CP-2098 | sales_region, order_type, customer_type | employee_name | quantity, unit_price, sale_price | sum | PASS |
| CP-2099 | sales_region, order_type, customer_type | employee_name | quantity, unit_price, sale_price | mean | PASS |
| CP-2100 | sales_region, order_type, customer_type | employee_name | quantity, unit_price, sale_price | count | PASS |
| CP-2101 | sales_region, order_type | employee_name, customer_type | quantity | sum | PASS |
| CP-2102 | sales_region, order_type | employee_name, customer_type | quantity | mean | PASS |
| CP-2103 | sales_region, order_type | employee_name, customer_type | quantity | count | PASS |
| CP-2104 | sales_region, order_type | employee_name, customer_type | unit_price | sum | PASS |
| CP-2105 | sales_region, order_type | employee_name, customer_type | unit_price | mean | PASS |
| CP-2106 | sales_region, order_type | employee_name, customer_type | unit_price | count | PASS |
| CP-2107 | sales_region, order_type | employee_name, customer_type | quantity, unit_price | sum | PASS |
| CP-2108 | sales_region, order_type | employee_name, customer_type | quantity, unit_price | mean | PASS |
| CP-2109 | sales_region, order_type | employee_name, customer_type | quantity, unit_price | count | PASS |
| CP-2110 | sales_region, order_type | employee_name, customer_type | sale_price | sum | PASS |
| CP-2111 | sales_region, order_type | employee_name, customer_type | sale_price | mean | PASS |
| CP-2112 | sales_region, order_type | employee_name, customer_type | sale_price | count | PASS |
| CP-2113 | sales_region, order_type | employee_name, customer_type | quantity, sale_price | sum | PASS |
| CP-2114 | sales_region, order_type | employee_name, customer_type | quantity, sale_price | mean | PASS |
| CP-2115 | sales_region, order_type | employee_name, customer_type | quantity, sale_price | count | PASS |
| CP-2116 | sales_region, order_type | employee_name, customer_type | unit_price, sale_price | sum | PASS |
| CP-2117 | sales_region, order_type | employee_name, customer_type | unit_price, sale_price | mean | PASS |
| CP-2118 | sales_region, order_type | employee_name, customer_type | unit_price, sale_price | count | PASS |
| CP-2119 | sales_region, order_type | employee_name, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2120 | sales_region, order_type | employee_name, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2121 | sales_region, order_type | employee_name, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-2122 | sales_region, order_type | employee_name | quantity | sum | PASS |
| CP-2123 | sales_region, order_type | employee_name | quantity | mean | PASS |
| CP-2124 | sales_region, order_type | employee_name | quantity | count | PASS |
| CP-2125 | sales_region, order_type | employee_name | unit_price | sum | PASS |
| CP-2126 | sales_region, order_type | employee_name | unit_price | mean | PASS |
| CP-2127 | sales_region, order_type | employee_name | unit_price | count | PASS |
| CP-2128 | sales_region, order_type | employee_name | quantity, unit_price | sum | PASS |
| CP-2129 | sales_region, order_type | employee_name | quantity, unit_price | mean | PASS |
| CP-2130 | sales_region, order_type | employee_name | quantity, unit_price | count | PASS |
| CP-2131 | sales_region, order_type | employee_name | sale_price | sum | PASS |
| CP-2132 | sales_region, order_type | employee_name | sale_price | mean | PASS |
| CP-2133 | sales_region, order_type | employee_name | sale_price | count | PASS |
| CP-2134 | sales_region, order_type | employee_name | quantity, sale_price | sum | PASS |
| CP-2135 | sales_region, order_type | employee_name | quantity, sale_price | mean | PASS |
| CP-2136 | sales_region, order_type | employee_name | quantity, sale_price | count | PASS |
| CP-2137 | sales_region, order_type | employee_name | unit_price, sale_price | sum | PASS |
| CP-2138 | sales_region, order_type | employee_name | unit_price, sale_price | mean | PASS |
| CP-2139 | sales_region, order_type | employee_name | unit_price, sale_price | count | PASS |
| CP-2140 | sales_region, order_type | employee_name | quantity, unit_price, sale_price | sum | PASS |
| CP-2141 | sales_region, order_type | employee_name | quantity, unit_price, sale_price | mean | PASS |
| CP-2142 | sales_region, order_type | employee_name | quantity, unit_price, sale_price | count | PASS |
| CP-2143 | sales_region, customer_type | employee_name, order_type | quantity | sum | PASS |
| CP-2144 | sales_region, customer_type | employee_name, order_type | quantity | mean | PASS |
| CP-2145 | sales_region, customer_type | employee_name, order_type | quantity | count | PASS |
| CP-2146 | sales_region, customer_type | employee_name, order_type | unit_price | sum | PASS |
| CP-2147 | sales_region, customer_type | employee_name, order_type | unit_price | mean | PASS |
| CP-2148 | sales_region, customer_type | employee_name, order_type | unit_price | count | PASS |
| CP-2149 | sales_region, customer_type | employee_name, order_type | quantity, unit_price | sum | PASS |
| CP-2150 | sales_region, customer_type | employee_name, order_type | quantity, unit_price | mean | PASS |
| CP-2151 | sales_region, customer_type | employee_name, order_type | quantity, unit_price | count | PASS |
| CP-2152 | sales_region, customer_type | employee_name, order_type | sale_price | sum | PASS |
| CP-2153 | sales_region, customer_type | employee_name, order_type | sale_price | mean | PASS |
| CP-2154 | sales_region, customer_type | employee_name, order_type | sale_price | count | PASS |
| CP-2155 | sales_region, customer_type | employee_name, order_type | quantity, sale_price | sum | PASS |
| CP-2156 | sales_region, customer_type | employee_name, order_type | quantity, sale_price | mean | PASS |
| CP-2157 | sales_region, customer_type | employee_name, order_type | quantity, sale_price | count | PASS |
| CP-2158 | sales_region, customer_type | employee_name, order_type | unit_price, sale_price | sum | PASS |
| CP-2159 | sales_region, customer_type | employee_name, order_type | unit_price, sale_price | mean | PASS |
| CP-2160 | sales_region, customer_type | employee_name, order_type | unit_price, sale_price | count | PASS |
| CP-2161 | sales_region, customer_type | employee_name, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2162 | sales_region, customer_type | employee_name, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2163 | sales_region, customer_type | employee_name, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-2164 | sales_region | employee_name, order_type, customer_type | quantity | sum | PASS |
| CP-2165 | sales_region | employee_name, order_type, customer_type | quantity | mean | PASS |
| CP-2166 | sales_region | employee_name, order_type, customer_type | quantity | count | PASS |
| CP-2167 | sales_region | employee_name, order_type, customer_type | unit_price | sum | PASS |
| CP-2168 | sales_region | employee_name, order_type, customer_type | unit_price | mean | PASS |
| CP-2169 | sales_region | employee_name, order_type, customer_type | unit_price | count | PASS |
| CP-2170 | sales_region | employee_name, order_type, customer_type | quantity, unit_price | sum | PASS |
| CP-2171 | sales_region | employee_name, order_type, customer_type | quantity, unit_price | mean | PASS |
| CP-2172 | sales_region | employee_name, order_type, customer_type | quantity, unit_price | count | PASS |
| CP-2173 | sales_region | employee_name, order_type, customer_type | sale_price | sum | PASS |
| CP-2174 | sales_region | employee_name, order_type, customer_type | sale_price | mean | PASS |
| CP-2175 | sales_region | employee_name, order_type, customer_type | sale_price | count | PASS |
| CP-2176 | sales_region | employee_name, order_type, customer_type | quantity, sale_price | sum | PASS |
| CP-2177 | sales_region | employee_name, order_type, customer_type | quantity, sale_price | mean | PASS |
| CP-2178 | sales_region | employee_name, order_type, customer_type | quantity, sale_price | count | PASS |
| CP-2179 | sales_region | employee_name, order_type, customer_type | unit_price, sale_price | sum | PASS |
| CP-2180 | sales_region | employee_name, order_type, customer_type | unit_price, sale_price | mean | PASS |
| CP-2181 | sales_region | employee_name, order_type, customer_type | unit_price, sale_price | count | PASS |
| CP-2182 | sales_region | employee_name, order_type, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2183 | sales_region | employee_name, order_type, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2184 | sales_region | employee_name, order_type, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-2185 | sales_region | employee_name, order_type | quantity | sum | PASS |
| CP-2186 | sales_region | employee_name, order_type | quantity | mean | PASS |
| CP-2187 | sales_region | employee_name, order_type | quantity | count | PASS |
| CP-2188 | sales_region | employee_name, order_type | unit_price | sum | PASS |
| CP-2189 | sales_region | employee_name, order_type | unit_price | mean | PASS |
| CP-2190 | sales_region | employee_name, order_type | unit_price | count | PASS |
| CP-2191 | sales_region | employee_name, order_type | quantity, unit_price | sum | PASS |
| CP-2192 | sales_region | employee_name, order_type | quantity, unit_price | mean | PASS |
| CP-2193 | sales_region | employee_name, order_type | quantity, unit_price | count | PASS |
| CP-2194 | sales_region | employee_name, order_type | sale_price | sum | PASS |
| CP-2195 | sales_region | employee_name, order_type | sale_price | mean | PASS |
| CP-2196 | sales_region | employee_name, order_type | sale_price | count | PASS |
| CP-2197 | sales_region | employee_name, order_type | quantity, sale_price | sum | PASS |
| CP-2198 | sales_region | employee_name, order_type | quantity, sale_price | mean | PASS |
| CP-2199 | sales_region | employee_name, order_type | quantity, sale_price | count | PASS |
| CP-2200 | sales_region | employee_name, order_type | unit_price, sale_price | sum | PASS |
| CP-2201 | sales_region | employee_name, order_type | unit_price, sale_price | mean | PASS |
| CP-2202 | sales_region | employee_name, order_type | unit_price, sale_price | count | PASS |
| CP-2203 | sales_region | employee_name, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2204 | sales_region | employee_name, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2205 | sales_region | employee_name, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-2206 | sales_region, customer_type | employee_name | quantity | sum | PASS |
| CP-2207 | sales_region, customer_type | employee_name | quantity | mean | PASS |
| CP-2208 | sales_region, customer_type | employee_name | quantity | count | PASS |
| CP-2209 | sales_region, customer_type | employee_name | unit_price | sum | PASS |
| CP-2210 | sales_region, customer_type | employee_name | unit_price | mean | PASS |
| CP-2211 | sales_region, customer_type | employee_name | unit_price | count | PASS |
| CP-2212 | sales_region, customer_type | employee_name | quantity, unit_price | sum | PASS |
| CP-2213 | sales_region, customer_type | employee_name | quantity, unit_price | mean | PASS |
| CP-2214 | sales_region, customer_type | employee_name | quantity, unit_price | count | PASS |
| CP-2215 | sales_region, customer_type | employee_name | sale_price | sum | PASS |
| CP-2216 | sales_region, customer_type | employee_name | sale_price | mean | PASS |
| CP-2217 | sales_region, customer_type | employee_name | sale_price | count | PASS |
| CP-2218 | sales_region, customer_type | employee_name | quantity, sale_price | sum | PASS |
| CP-2219 | sales_region, customer_type | employee_name | quantity, sale_price | mean | PASS |
| CP-2220 | sales_region, customer_type | employee_name | quantity, sale_price | count | PASS |
| CP-2221 | sales_region, customer_type | employee_name | unit_price, sale_price | sum | PASS |
| CP-2222 | sales_region, customer_type | employee_name | unit_price, sale_price | mean | PASS |
| CP-2223 | sales_region, customer_type | employee_name | unit_price, sale_price | count | PASS |
| CP-2224 | sales_region, customer_type | employee_name | quantity, unit_price, sale_price | sum | PASS |
| CP-2225 | sales_region, customer_type | employee_name | quantity, unit_price, sale_price | mean | PASS |
| CP-2226 | sales_region, customer_type | employee_name | quantity, unit_price, sale_price | count | PASS |
| CP-2227 | sales_region | employee_name, customer_type | quantity | sum | PASS |
| CP-2228 | sales_region | employee_name, customer_type | quantity | mean | PASS |
| CP-2229 | sales_region | employee_name, customer_type | quantity | count | PASS |
| CP-2230 | sales_region | employee_name, customer_type | unit_price | sum | PASS |
| CP-2231 | sales_region | employee_name, customer_type | unit_price | mean | PASS |
| CP-2232 | sales_region | employee_name, customer_type | unit_price | count | PASS |
| CP-2233 | sales_region | employee_name, customer_type | quantity, unit_price | sum | PASS |
| CP-2234 | sales_region | employee_name, customer_type | quantity, unit_price | mean | PASS |
| CP-2235 | sales_region | employee_name, customer_type | quantity, unit_price | count | PASS |
| CP-2236 | sales_region | employee_name, customer_type | sale_price | sum | PASS |
| CP-2237 | sales_region | employee_name, customer_type | sale_price | mean | PASS |
| CP-2238 | sales_region | employee_name, customer_type | sale_price | count | PASS |
| CP-2239 | sales_region | employee_name, customer_type | quantity, sale_price | sum | PASS |
| CP-2240 | sales_region | employee_name, customer_type | quantity, sale_price | mean | PASS |
| CP-2241 | sales_region | employee_name, customer_type | quantity, sale_price | count | PASS |
| CP-2242 | sales_region | employee_name, customer_type | unit_price, sale_price | sum | PASS |
| CP-2243 | sales_region | employee_name, customer_type | unit_price, sale_price | mean | PASS |
| CP-2244 | sales_region | employee_name, customer_type | unit_price, sale_price | count | PASS |
| CP-2245 | sales_region | employee_name, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2246 | sales_region | employee_name, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2247 | sales_region | employee_name, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-2248 | sales_region | employee_name | quantity | sum | PASS |
| CP-2249 | sales_region | employee_name | quantity | mean | PASS |
| CP-2250 | sales_region | employee_name | quantity | count | PASS |
| CP-2251 | sales_region | employee_name | unit_price | sum | PASS |
| CP-2252 | sales_region | employee_name | unit_price | mean | PASS |
| CP-2253 | sales_region | employee_name | unit_price | count | PASS |
| CP-2254 | sales_region | employee_name | quantity, unit_price | sum | PASS |
| CP-2255 | sales_region | employee_name | quantity, unit_price | mean | PASS |
| CP-2256 | sales_region | employee_name | quantity, unit_price | count | PASS |
| CP-2257 | sales_region | employee_name | sale_price | sum | PASS |
| CP-2258 | sales_region | employee_name | sale_price | mean | PASS |
| CP-2259 | sales_region | employee_name | sale_price | count | PASS |
| CP-2260 | sales_region | employee_name | quantity, sale_price | sum | PASS |
| CP-2261 | sales_region | employee_name | quantity, sale_price | mean | PASS |
| CP-2262 | sales_region | employee_name | quantity, sale_price | count | PASS |
| CP-2263 | sales_region | employee_name | unit_price, sale_price | sum | PASS |
| CP-2264 | sales_region | employee_name | unit_price, sale_price | mean | PASS |
| CP-2265 | sales_region | employee_name | unit_price, sale_price | count | PASS |
| CP-2266 | sales_region | employee_name | quantity, unit_price, sale_price | sum | PASS |
| CP-2267 | sales_region | employee_name | quantity, unit_price, sale_price | mean | PASS |
| CP-2268 | sales_region | employee_name | quantity, unit_price, sale_price | count | PASS |
| CP-2269 | product_category, order_type, customer_type | employee_name, sales_region | quantity | sum | PASS |
| CP-2270 | product_category, order_type, customer_type | employee_name, sales_region | quantity | mean | PASS |
| CP-2271 | product_category, order_type, customer_type | employee_name, sales_region | quantity | count | PASS |
| CP-2272 | product_category, order_type, customer_type | employee_name, sales_region | unit_price | sum | PASS |
| CP-2273 | product_category, order_type, customer_type | employee_name, sales_region | unit_price | mean | PASS |
| CP-2274 | product_category, order_type, customer_type | employee_name, sales_region | unit_price | count | PASS |
| CP-2275 | product_category, order_type, customer_type | employee_name, sales_region | quantity, unit_price | sum | PASS |
| CP-2276 | product_category, order_type, customer_type | employee_name, sales_region | quantity, unit_price | mean | PASS |
| CP-2277 | product_category, order_type, customer_type | employee_name, sales_region | quantity, unit_price | count | PASS |
| CP-2278 | product_category, order_type, customer_type | employee_name, sales_region | sale_price | sum | PASS |
| CP-2279 | product_category, order_type, customer_type | employee_name, sales_region | sale_price | mean | PASS |
| CP-2280 | product_category, order_type, customer_type | employee_name, sales_region | sale_price | count | PASS |
| CP-2281 | product_category, order_type, customer_type | employee_name, sales_region | quantity, sale_price | sum | PASS |
| CP-2282 | product_category, order_type, customer_type | employee_name, sales_region | quantity, sale_price | mean | PASS |
| CP-2283 | product_category, order_type, customer_type | employee_name, sales_region | quantity, sale_price | count | PASS |
| CP-2284 | product_category, order_type, customer_type | employee_name, sales_region | unit_price, sale_price | sum | PASS |
| CP-2285 | product_category, order_type, customer_type | employee_name, sales_region | unit_price, sale_price | mean | PASS |
| CP-2286 | product_category, order_type, customer_type | employee_name, sales_region | unit_price, sale_price | count | PASS |
| CP-2287 | product_category, order_type, customer_type | employee_name, sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-2288 | product_category, order_type, customer_type | employee_name, sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-2289 | product_category, order_type, customer_type | employee_name, sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-2290 | product_category, order_type | employee_name, sales_region, customer_type | quantity | sum | PASS |
| CP-2291 | product_category, order_type | employee_name, sales_region, customer_type | quantity | mean | PASS |
| CP-2292 | product_category, order_type | employee_name, sales_region, customer_type | quantity | count | PASS |
| CP-2293 | product_category, order_type | employee_name, sales_region, customer_type | unit_price | sum | PASS |
| CP-2294 | product_category, order_type | employee_name, sales_region, customer_type | unit_price | mean | PASS |
| CP-2295 | product_category, order_type | employee_name, sales_region, customer_type | unit_price | count | PASS |
| CP-2296 | product_category, order_type | employee_name, sales_region, customer_type | quantity, unit_price | sum | PASS |
| CP-2297 | product_category, order_type | employee_name, sales_region, customer_type | quantity, unit_price | mean | PASS |
| CP-2298 | product_category, order_type | employee_name, sales_region, customer_type | quantity, unit_price | count | PASS |
| CP-2299 | product_category, order_type | employee_name, sales_region, customer_type | sale_price | sum | PASS |
| CP-2300 | product_category, order_type | employee_name, sales_region, customer_type | sale_price | mean | PASS |
| CP-2301 | product_category, order_type | employee_name, sales_region, customer_type | sale_price | count | PASS |
| CP-2302 | product_category, order_type | employee_name, sales_region, customer_type | quantity, sale_price | sum | PASS |
| CP-2303 | product_category, order_type | employee_name, sales_region, customer_type | quantity, sale_price | mean | PASS |
| CP-2304 | product_category, order_type | employee_name, sales_region, customer_type | quantity, sale_price | count | PASS |
| CP-2305 | product_category, order_type | employee_name, sales_region, customer_type | unit_price, sale_price | sum | PASS |
| CP-2306 | product_category, order_type | employee_name, sales_region, customer_type | unit_price, sale_price | mean | PASS |
| CP-2307 | product_category, order_type | employee_name, sales_region, customer_type | unit_price, sale_price | count | PASS |
| CP-2308 | product_category, order_type | employee_name, sales_region, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2309 | product_category, order_type | employee_name, sales_region, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2310 | product_category, order_type | employee_name, sales_region, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-2311 | product_category, order_type | employee_name, sales_region | quantity | sum | PASS |
| CP-2312 | product_category, order_type | employee_name, sales_region | quantity | mean | PASS |
| CP-2313 | product_category, order_type | employee_name, sales_region | quantity | count | PASS |
| CP-2314 | product_category, order_type | employee_name, sales_region | unit_price | sum | PASS |
| CP-2315 | product_category, order_type | employee_name, sales_region | unit_price | mean | PASS |
| CP-2316 | product_category, order_type | employee_name, sales_region | unit_price | count | PASS |
| CP-2317 | product_category, order_type | employee_name, sales_region | quantity, unit_price | sum | PASS |
| CP-2318 | product_category, order_type | employee_name, sales_region | quantity, unit_price | mean | PASS |
| CP-2319 | product_category, order_type | employee_name, sales_region | quantity, unit_price | count | PASS |
| CP-2320 | product_category, order_type | employee_name, sales_region | sale_price | sum | PASS |
| CP-2321 | product_category, order_type | employee_name, sales_region | sale_price | mean | PASS |
| CP-2322 | product_category, order_type | employee_name, sales_region | sale_price | count | PASS |
| CP-2323 | product_category, order_type | employee_name, sales_region | quantity, sale_price | sum | PASS |
| CP-2324 | product_category, order_type | employee_name, sales_region | quantity, sale_price | mean | PASS |
| CP-2325 | product_category, order_type | employee_name, sales_region | quantity, sale_price | count | PASS |
| CP-2326 | product_category, order_type | employee_name, sales_region | unit_price, sale_price | sum | PASS |
| CP-2327 | product_category, order_type | employee_name, sales_region | unit_price, sale_price | mean | PASS |
| CP-2328 | product_category, order_type | employee_name, sales_region | unit_price, sale_price | count | PASS |
| CP-2329 | product_category, order_type | employee_name, sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-2330 | product_category, order_type | employee_name, sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-2331 | product_category, order_type | employee_name, sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-2332 | product_category, customer_type | employee_name, sales_region, order_type | quantity | sum | PASS |
| CP-2333 | product_category, customer_type | employee_name, sales_region, order_type | quantity | mean | PASS |
| CP-2334 | product_category, customer_type | employee_name, sales_region, order_type | quantity | count | PASS |
| CP-2335 | product_category, customer_type | employee_name, sales_region, order_type | unit_price | sum | PASS |
| CP-2336 | product_category, customer_type | employee_name, sales_region, order_type | unit_price | mean | PASS |
| CP-2337 | product_category, customer_type | employee_name, sales_region, order_type | unit_price | count | PASS |
| CP-2338 | product_category, customer_type | employee_name, sales_region, order_type | quantity, unit_price | sum | PASS |
| CP-2339 | product_category, customer_type | employee_name, sales_region, order_type | quantity, unit_price | mean | PASS |
| CP-2340 | product_category, customer_type | employee_name, sales_region, order_type | quantity, unit_price | count | PASS |
| CP-2341 | product_category, customer_type | employee_name, sales_region, order_type | sale_price | sum | PASS |
| CP-2342 | product_category, customer_type | employee_name, sales_region, order_type | sale_price | mean | PASS |
| CP-2343 | product_category, customer_type | employee_name, sales_region, order_type | sale_price | count | PASS |
| CP-2344 | product_category, customer_type | employee_name, sales_region, order_type | quantity, sale_price | sum | PASS |
| CP-2345 | product_category, customer_type | employee_name, sales_region, order_type | quantity, sale_price | mean | PASS |
| CP-2346 | product_category, customer_type | employee_name, sales_region, order_type | quantity, sale_price | count | PASS |
| CP-2347 | product_category, customer_type | employee_name, sales_region, order_type | unit_price, sale_price | sum | PASS |
| CP-2348 | product_category, customer_type | employee_name, sales_region, order_type | unit_price, sale_price | mean | PASS |
| CP-2349 | product_category, customer_type | employee_name, sales_region, order_type | unit_price, sale_price | count | PASS |
| CP-2350 | product_category, customer_type | employee_name, sales_region, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2351 | product_category, customer_type | employee_name, sales_region, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2352 | product_category, customer_type | employee_name, sales_region, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-2353 | product_category | employee_name, sales_region, order_type, customer_type | quantity | sum | PASS |
| CP-2354 | product_category | employee_name, sales_region, order_type, customer_type | quantity | mean | PASS |
| CP-2355 | product_category | employee_name, sales_region, order_type, customer_type | quantity | count | PASS |
| CP-2356 | product_category | employee_name, sales_region, order_type, customer_type | unit_price | sum | PASS |
| CP-2357 | product_category | employee_name, sales_region, order_type, customer_type | unit_price | mean | PASS |
| CP-2358 | product_category | employee_name, sales_region, order_type, customer_type | unit_price | count | PASS |
| CP-2359 | product_category | employee_name, sales_region, order_type, customer_type | quantity, unit_price | sum | PASS |
| CP-2360 | product_category | employee_name, sales_region, order_type, customer_type | quantity, unit_price | mean | PASS |
| CP-2361 | product_category | employee_name, sales_region, order_type, customer_type | quantity, unit_price | count | PASS |
| CP-2362 | product_category | employee_name, sales_region, order_type, customer_type | sale_price | sum | PASS |
| CP-2363 | product_category | employee_name, sales_region, order_type, customer_type | sale_price | mean | PASS |
| CP-2364 | product_category | employee_name, sales_region, order_type, customer_type | sale_price | count | PASS |
| CP-2365 | product_category | employee_name, sales_region, order_type, customer_type | quantity, sale_price | sum | PASS |
| CP-2366 | product_category | employee_name, sales_region, order_type, customer_type | quantity, sale_price | mean | PASS |
| CP-2367 | product_category | employee_name, sales_region, order_type, customer_type | quantity, sale_price | count | PASS |
| CP-2368 | product_category | employee_name, sales_region, order_type, customer_type | unit_price, sale_price | sum | PASS |
| CP-2369 | product_category | employee_name, sales_region, order_type, customer_type | unit_price, sale_price | mean | PASS |
| CP-2370 | product_category | employee_name, sales_region, order_type, customer_type | unit_price, sale_price | count | PASS |
| CP-2371 | product_category | employee_name, sales_region, order_type, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2372 | product_category | employee_name, sales_region, order_type, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2373 | product_category | employee_name, sales_region, order_type, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-2374 | product_category | employee_name, sales_region, order_type | quantity | sum | PASS |
| CP-2375 | product_category | employee_name, sales_region, order_type | quantity | mean | PASS |
| CP-2376 | product_category | employee_name, sales_region, order_type | quantity | count | PASS |
| CP-2377 | product_category | employee_name, sales_region, order_type | unit_price | sum | PASS |
| CP-2378 | product_category | employee_name, sales_region, order_type | unit_price | mean | PASS |
| CP-2379 | product_category | employee_name, sales_region, order_type | unit_price | count | PASS |
| CP-2380 | product_category | employee_name, sales_region, order_type | quantity, unit_price | sum | PASS |
| CP-2381 | product_category | employee_name, sales_region, order_type | quantity, unit_price | mean | PASS |
| CP-2382 | product_category | employee_name, sales_region, order_type | quantity, unit_price | count | PASS |
| CP-2383 | product_category | employee_name, sales_region, order_type | sale_price | sum | PASS |
| CP-2384 | product_category | employee_name, sales_region, order_type | sale_price | mean | PASS |
| CP-2385 | product_category | employee_name, sales_region, order_type | sale_price | count | PASS |
| CP-2386 | product_category | employee_name, sales_region, order_type | quantity, sale_price | sum | PASS |
| CP-2387 | product_category | employee_name, sales_region, order_type | quantity, sale_price | mean | PASS |
| CP-2388 | product_category | employee_name, sales_region, order_type | quantity, sale_price | count | PASS |
| CP-2389 | product_category | employee_name, sales_region, order_type | unit_price, sale_price | sum | PASS |
| CP-2390 | product_category | employee_name, sales_region, order_type | unit_price, sale_price | mean | PASS |
| CP-2391 | product_category | employee_name, sales_region, order_type | unit_price, sale_price | count | PASS |
| CP-2392 | product_category | employee_name, sales_region, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2393 | product_category | employee_name, sales_region, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2394 | product_category | employee_name, sales_region, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-2395 | product_category, customer_type | employee_name, sales_region | quantity | sum | PASS |
| CP-2396 | product_category, customer_type | employee_name, sales_region | quantity | mean | PASS |
| CP-2397 | product_category, customer_type | employee_name, sales_region | quantity | count | PASS |
| CP-2398 | product_category, customer_type | employee_name, sales_region | unit_price | sum | PASS |
| CP-2399 | product_category, customer_type | employee_name, sales_region | unit_price | mean | PASS |
| CP-2400 | product_category, customer_type | employee_name, sales_region | unit_price | count | PASS |
| CP-2401 | product_category, customer_type | employee_name, sales_region | quantity, unit_price | sum | PASS |
| CP-2402 | product_category, customer_type | employee_name, sales_region | quantity, unit_price | mean | PASS |
| CP-2403 | product_category, customer_type | employee_name, sales_region | quantity, unit_price | count | PASS |
| CP-2404 | product_category, customer_type | employee_name, sales_region | sale_price | sum | PASS |
| CP-2405 | product_category, customer_type | employee_name, sales_region | sale_price | mean | PASS |
| CP-2406 | product_category, customer_type | employee_name, sales_region | sale_price | count | PASS |
| CP-2407 | product_category, customer_type | employee_name, sales_region | quantity, sale_price | sum | PASS |
| CP-2408 | product_category, customer_type | employee_name, sales_region | quantity, sale_price | mean | PASS |
| CP-2409 | product_category, customer_type | employee_name, sales_region | quantity, sale_price | count | PASS |
| CP-2410 | product_category, customer_type | employee_name, sales_region | unit_price, sale_price | sum | PASS |
| CP-2411 | product_category, customer_type | employee_name, sales_region | unit_price, sale_price | mean | PASS |
| CP-2412 | product_category, customer_type | employee_name, sales_region | unit_price, sale_price | count | PASS |
| CP-2413 | product_category, customer_type | employee_name, sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-2414 | product_category, customer_type | employee_name, sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-2415 | product_category, customer_type | employee_name, sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-2416 | product_category | employee_name, sales_region, customer_type | quantity | sum | PASS |
| CP-2417 | product_category | employee_name, sales_region, customer_type | quantity | mean | PASS |
| CP-2418 | product_category | employee_name, sales_region, customer_type | quantity | count | PASS |
| CP-2419 | product_category | employee_name, sales_region, customer_type | unit_price | sum | PASS |
| CP-2420 | product_category | employee_name, sales_region, customer_type | unit_price | mean | PASS |
| CP-2421 | product_category | employee_name, sales_region, customer_type | unit_price | count | PASS |
| CP-2422 | product_category | employee_name, sales_region, customer_type | quantity, unit_price | sum | PASS |
| CP-2423 | product_category | employee_name, sales_region, customer_type | quantity, unit_price | mean | PASS |
| CP-2424 | product_category | employee_name, sales_region, customer_type | quantity, unit_price | count | PASS |
| CP-2425 | product_category | employee_name, sales_region, customer_type | sale_price | sum | PASS |
| CP-2426 | product_category | employee_name, sales_region, customer_type | sale_price | mean | PASS |
| CP-2427 | product_category | employee_name, sales_region, customer_type | sale_price | count | PASS |
| CP-2428 | product_category | employee_name, sales_region, customer_type | quantity, sale_price | sum | PASS |
| CP-2429 | product_category | employee_name, sales_region, customer_type | quantity, sale_price | mean | PASS |
| CP-2430 | product_category | employee_name, sales_region, customer_type | quantity, sale_price | count | PASS |
| CP-2431 | product_category | employee_name, sales_region, customer_type | unit_price, sale_price | sum | PASS |
| CP-2432 | product_category | employee_name, sales_region, customer_type | unit_price, sale_price | mean | PASS |
| CP-2433 | product_category | employee_name, sales_region, customer_type | unit_price, sale_price | count | PASS |
| CP-2434 | product_category | employee_name, sales_region, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2435 | product_category | employee_name, sales_region, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2436 | product_category | employee_name, sales_region, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-2437 | product_category | employee_name, sales_region | quantity | sum | PASS |
| CP-2438 | product_category | employee_name, sales_region | quantity | mean | PASS |
| CP-2439 | product_category | employee_name, sales_region | quantity | count | PASS |
| CP-2440 | product_category | employee_name, sales_region | unit_price | sum | PASS |
| CP-2441 | product_category | employee_name, sales_region | unit_price | mean | PASS |
| CP-2442 | product_category | employee_name, sales_region | unit_price | count | PASS |
| CP-2443 | product_category | employee_name, sales_region | quantity, unit_price | sum | PASS |
| CP-2444 | product_category | employee_name, sales_region | quantity, unit_price | mean | PASS |
| CP-2445 | product_category | employee_name, sales_region | quantity, unit_price | count | PASS |
| CP-2446 | product_category | employee_name, sales_region | sale_price | sum | PASS |
| CP-2447 | product_category | employee_name, sales_region | sale_price | mean | PASS |
| CP-2448 | product_category | employee_name, sales_region | sale_price | count | PASS |
| CP-2449 | product_category | employee_name, sales_region | quantity, sale_price | sum | PASS |
| CP-2450 | product_category | employee_name, sales_region | quantity, sale_price | mean | PASS |
| CP-2451 | product_category | employee_name, sales_region | quantity, sale_price | count | PASS |
| CP-2452 | product_category | employee_name, sales_region | unit_price, sale_price | sum | PASS |
| CP-2453 | product_category | employee_name, sales_region | unit_price, sale_price | mean | PASS |
| CP-2454 | product_category | employee_name, sales_region | unit_price, sale_price | count | PASS |
| CP-2455 | product_category | employee_name, sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-2456 | product_category | employee_name, sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-2457 | product_category | employee_name, sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-2458 | order_type, customer_type | employee_name, sales_region, product_category | quantity | sum | PASS |
| CP-2459 | order_type, customer_type | employee_name, sales_region, product_category | quantity | mean | PASS |
| CP-2460 | order_type, customer_type | employee_name, sales_region, product_category | quantity | count | PASS |
| CP-2461 | order_type, customer_type | employee_name, sales_region, product_category | unit_price | sum | PASS |
| CP-2462 | order_type, customer_type | employee_name, sales_region, product_category | unit_price | mean | PASS |
| CP-2463 | order_type, customer_type | employee_name, sales_region, product_category | unit_price | count | PASS |
| CP-2464 | order_type, customer_type | employee_name, sales_region, product_category | quantity, unit_price | sum | PASS |
| CP-2465 | order_type, customer_type | employee_name, sales_region, product_category | quantity, unit_price | mean | PASS |
| CP-2466 | order_type, customer_type | employee_name, sales_region, product_category | quantity, unit_price | count | PASS |
| CP-2467 | order_type, customer_type | employee_name, sales_region, product_category | sale_price | sum | PASS |
| CP-2468 | order_type, customer_type | employee_name, sales_region, product_category | sale_price | mean | PASS |
| CP-2469 | order_type, customer_type | employee_name, sales_region, product_category | sale_price | count | PASS |
| CP-2470 | order_type, customer_type | employee_name, sales_region, product_category | quantity, sale_price | sum | PASS |
| CP-2471 | order_type, customer_type | employee_name, sales_region, product_category | quantity, sale_price | mean | PASS |
| CP-2472 | order_type, customer_type | employee_name, sales_region, product_category | quantity, sale_price | count | PASS |
| CP-2473 | order_type, customer_type | employee_name, sales_region, product_category | unit_price, sale_price | sum | PASS |
| CP-2474 | order_type, customer_type | employee_name, sales_region, product_category | unit_price, sale_price | mean | PASS |
| CP-2475 | order_type, customer_type | employee_name, sales_region, product_category | unit_price, sale_price | count | PASS |
| CP-2476 | order_type, customer_type | employee_name, sales_region, product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-2477 | order_type, customer_type | employee_name, sales_region, product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-2478 | order_type, customer_type | employee_name, sales_region, product_category | quantity, unit_price, sale_price | count | PASS |
| CP-2479 | order_type | employee_name, sales_region, product_category, customer_type | quantity | sum | PASS |
| CP-2480 | order_type | employee_name, sales_region, product_category, customer_type | quantity | mean | PASS |
| CP-2481 | order_type | employee_name, sales_region, product_category, customer_type | quantity | count | PASS |
| CP-2482 | order_type | employee_name, sales_region, product_category, customer_type | unit_price | sum | PASS |
| CP-2483 | order_type | employee_name, sales_region, product_category, customer_type | unit_price | mean | PASS |
| CP-2484 | order_type | employee_name, sales_region, product_category, customer_type | unit_price | count | PASS |
| CP-2485 | order_type | employee_name, sales_region, product_category, customer_type | quantity, unit_price | sum | PASS |
| CP-2486 | order_type | employee_name, sales_region, product_category, customer_type | quantity, unit_price | mean | PASS |
| CP-2487 | order_type | employee_name, sales_region, product_category, customer_type | quantity, unit_price | count | PASS |
| CP-2488 | order_type | employee_name, sales_region, product_category, customer_type | sale_price | sum | PASS |
| CP-2489 | order_type | employee_name, sales_region, product_category, customer_type | sale_price | mean | PASS |
| CP-2490 | order_type | employee_name, sales_region, product_category, customer_type | sale_price | count | PASS |
| CP-2491 | order_type | employee_name, sales_region, product_category, customer_type | quantity, sale_price | sum | PASS |
| CP-2492 | order_type | employee_name, sales_region, product_category, customer_type | quantity, sale_price | mean | PASS |
| CP-2493 | order_type | employee_name, sales_region, product_category, customer_type | quantity, sale_price | count | PASS |
| CP-2494 | order_type | employee_name, sales_region, product_category, customer_type | unit_price, sale_price | sum | PASS |
| CP-2495 | order_type | employee_name, sales_region, product_category, customer_type | unit_price, sale_price | mean | PASS |
| CP-2496 | order_type | employee_name, sales_region, product_category, customer_type | unit_price, sale_price | count | PASS |
| CP-2497 | order_type | employee_name, sales_region, product_category, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2498 | order_type | employee_name, sales_region, product_category, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2499 | order_type | employee_name, sales_region, product_category, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-2500 | order_type | employee_name, sales_region, product_category | quantity | sum | PASS |
| CP-2501 | order_type | employee_name, sales_region, product_category | quantity | mean | PASS |
| CP-2502 | order_type | employee_name, sales_region, product_category | quantity | count | PASS |
| CP-2503 | order_type | employee_name, sales_region, product_category | unit_price | sum | PASS |
| CP-2504 | order_type | employee_name, sales_region, product_category | unit_price | mean | PASS |
| CP-2505 | order_type | employee_name, sales_region, product_category | unit_price | count | PASS |
| CP-2506 | order_type | employee_name, sales_region, product_category | quantity, unit_price | sum | PASS |
| CP-2507 | order_type | employee_name, sales_region, product_category | quantity, unit_price | mean | PASS |
| CP-2508 | order_type | employee_name, sales_region, product_category | quantity, unit_price | count | PASS |
| CP-2509 | order_type | employee_name, sales_region, product_category | sale_price | sum | PASS |
| CP-2510 | order_type | employee_name, sales_region, product_category | sale_price | mean | PASS |
| CP-2511 | order_type | employee_name, sales_region, product_category | sale_price | count | PASS |
| CP-2512 | order_type | employee_name, sales_region, product_category | quantity, sale_price | sum | PASS |
| CP-2513 | order_type | employee_name, sales_region, product_category | quantity, sale_price | mean | PASS |
| CP-2514 | order_type | employee_name, sales_region, product_category | quantity, sale_price | count | PASS |
| CP-2515 | order_type | employee_name, sales_region, product_category | unit_price, sale_price | sum | PASS |
| CP-2516 | order_type | employee_name, sales_region, product_category | unit_price, sale_price | mean | PASS |
| CP-2517 | order_type | employee_name, sales_region, product_category | unit_price, sale_price | count | PASS |
| CP-2518 | order_type | employee_name, sales_region, product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-2519 | order_type | employee_name, sales_region, product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-2520 | order_type | employee_name, sales_region, product_category | quantity, unit_price, sale_price | count | PASS |
| CP-2521 | customer_type | employee_name, sales_region, product_category, order_type | quantity | sum | PASS |
| CP-2522 | customer_type | employee_name, sales_region, product_category, order_type | quantity | mean | PASS |
| CP-2523 | customer_type | employee_name, sales_region, product_category, order_type | quantity | count | PASS |
| CP-2524 | customer_type | employee_name, sales_region, product_category, order_type | unit_price | sum | PASS |
| CP-2525 | customer_type | employee_name, sales_region, product_category, order_type | unit_price | mean | PASS |
| CP-2526 | customer_type | employee_name, sales_region, product_category, order_type | unit_price | count | PASS |
| CP-2527 | customer_type | employee_name, sales_region, product_category, order_type | quantity, unit_price | sum | PASS |
| CP-2528 | customer_type | employee_name, sales_region, product_category, order_type | quantity, unit_price | mean | PASS |
| CP-2529 | customer_type | employee_name, sales_region, product_category, order_type | quantity, unit_price | count | PASS |
| CP-2530 | customer_type | employee_name, sales_region, product_category, order_type | sale_price | sum | PASS |
| CP-2531 | customer_type | employee_name, sales_region, product_category, order_type | sale_price | mean | PASS |
| CP-2532 | customer_type | employee_name, sales_region, product_category, order_type | sale_price | count | PASS |
| CP-2533 | customer_type | employee_name, sales_region, product_category, order_type | quantity, sale_price | sum | PASS |
| CP-2534 | customer_type | employee_name, sales_region, product_category, order_type | quantity, sale_price | mean | PASS |
| CP-2535 | customer_type | employee_name, sales_region, product_category, order_type | quantity, sale_price | count | PASS |
| CP-2536 | customer_type | employee_name, sales_region, product_category, order_type | unit_price, sale_price | sum | PASS |
| CP-2537 | customer_type | employee_name, sales_region, product_category, order_type | unit_price, sale_price | mean | PASS |
| CP-2538 | customer_type | employee_name, sales_region, product_category, order_type | unit_price, sale_price | count | PASS |
| CP-2539 | customer_type | employee_name, sales_region, product_category, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2540 | customer_type | employee_name, sales_region, product_category, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2541 | customer_type | employee_name, sales_region, product_category, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-2542 | customer_type | employee_name, sales_region, product_category | quantity | sum | PASS |
| CP-2543 | customer_type | employee_name, sales_region, product_category | quantity | mean | PASS |
| CP-2544 | customer_type | employee_name, sales_region, product_category | quantity | count | PASS |
| CP-2545 | customer_type | employee_name, sales_region, product_category | unit_price | sum | PASS |
| CP-2546 | customer_type | employee_name, sales_region, product_category | unit_price | mean | PASS |
| CP-2547 | customer_type | employee_name, sales_region, product_category | unit_price | count | PASS |
| CP-2548 | customer_type | employee_name, sales_region, product_category | quantity, unit_price | sum | PASS |
| CP-2549 | customer_type | employee_name, sales_region, product_category | quantity, unit_price | mean | PASS |
| CP-2550 | customer_type | employee_name, sales_region, product_category | quantity, unit_price | count | PASS |
| CP-2551 | customer_type | employee_name, sales_region, product_category | sale_price | sum | PASS |
| CP-2552 | customer_type | employee_name, sales_region, product_category | sale_price | mean | PASS |
| CP-2553 | customer_type | employee_name, sales_region, product_category | sale_price | count | PASS |
| CP-2554 | customer_type | employee_name, sales_region, product_category | quantity, sale_price | sum | PASS |
| CP-2555 | customer_type | employee_name, sales_region, product_category | quantity, sale_price | mean | PASS |
| CP-2556 | customer_type | employee_name, sales_region, product_category | quantity, sale_price | count | PASS |
| CP-2557 | customer_type | employee_name, sales_region, product_category | unit_price, sale_price | sum | PASS |
| CP-2558 | customer_type | employee_name, sales_region, product_category | unit_price, sale_price | mean | PASS |
| CP-2559 | customer_type | employee_name, sales_region, product_category | unit_price, sale_price | count | PASS |
| CP-2560 | customer_type | employee_name, sales_region, product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-2561 | customer_type | employee_name, sales_region, product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-2562 | customer_type | employee_name, sales_region, product_category | quantity, unit_price, sale_price | count | PASS |
| CP-2563 | order_type, customer_type | employee_name, sales_region | quantity | sum | PASS |
| CP-2564 | order_type, customer_type | employee_name, sales_region | quantity | mean | PASS |
| CP-2565 | order_type, customer_type | employee_name, sales_region | quantity | count | PASS |
| CP-2566 | order_type, customer_type | employee_name, sales_region | unit_price | sum | PASS |
| CP-2567 | order_type, customer_type | employee_name, sales_region | unit_price | mean | PASS |
| CP-2568 | order_type, customer_type | employee_name, sales_region | unit_price | count | PASS |
| CP-2569 | order_type, customer_type | employee_name, sales_region | quantity, unit_price | sum | PASS |
| CP-2570 | order_type, customer_type | employee_name, sales_region | quantity, unit_price | mean | PASS |
| CP-2571 | order_type, customer_type | employee_name, sales_region | quantity, unit_price | count | PASS |
| CP-2572 | order_type, customer_type | employee_name, sales_region | sale_price | sum | PASS |
| CP-2573 | order_type, customer_type | employee_name, sales_region | sale_price | mean | PASS |
| CP-2574 | order_type, customer_type | employee_name, sales_region | sale_price | count | PASS |
| CP-2575 | order_type, customer_type | employee_name, sales_region | quantity, sale_price | sum | PASS |
| CP-2576 | order_type, customer_type | employee_name, sales_region | quantity, sale_price | mean | PASS |
| CP-2577 | order_type, customer_type | employee_name, sales_region | quantity, sale_price | count | PASS |
| CP-2578 | order_type, customer_type | employee_name, sales_region | unit_price, sale_price | sum | PASS |
| CP-2579 | order_type, customer_type | employee_name, sales_region | unit_price, sale_price | mean | PASS |
| CP-2580 | order_type, customer_type | employee_name, sales_region | unit_price, sale_price | count | PASS |
| CP-2581 | order_type, customer_type | employee_name, sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-2582 | order_type, customer_type | employee_name, sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-2583 | order_type, customer_type | employee_name, sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-2584 | order_type | employee_name, sales_region, customer_type | quantity | sum | PASS |
| CP-2585 | order_type | employee_name, sales_region, customer_type | quantity | mean | PASS |
| CP-2586 | order_type | employee_name, sales_region, customer_type | quantity | count | PASS |
| CP-2587 | order_type | employee_name, sales_region, customer_type | unit_price | sum | PASS |
| CP-2588 | order_type | employee_name, sales_region, customer_type | unit_price | mean | PASS |
| CP-2589 | order_type | employee_name, sales_region, customer_type | unit_price | count | PASS |
| CP-2590 | order_type | employee_name, sales_region, customer_type | quantity, unit_price | sum | PASS |
| CP-2591 | order_type | employee_name, sales_region, customer_type | quantity, unit_price | mean | PASS |
| CP-2592 | order_type | employee_name, sales_region, customer_type | quantity, unit_price | count | PASS |
| CP-2593 | order_type | employee_name, sales_region, customer_type | sale_price | sum | PASS |
| CP-2594 | order_type | employee_name, sales_region, customer_type | sale_price | mean | PASS |
| CP-2595 | order_type | employee_name, sales_region, customer_type | sale_price | count | PASS |
| CP-2596 | order_type | employee_name, sales_region, customer_type | quantity, sale_price | sum | PASS |
| CP-2597 | order_type | employee_name, sales_region, customer_type | quantity, sale_price | mean | PASS |
| CP-2598 | order_type | employee_name, sales_region, customer_type | quantity, sale_price | count | PASS |
| CP-2599 | order_type | employee_name, sales_region, customer_type | unit_price, sale_price | sum | PASS |
| CP-2600 | order_type | employee_name, sales_region, customer_type | unit_price, sale_price | mean | PASS |
| CP-2601 | order_type | employee_name, sales_region, customer_type | unit_price, sale_price | count | PASS |
| CP-2602 | order_type | employee_name, sales_region, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2603 | order_type | employee_name, sales_region, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2604 | order_type | employee_name, sales_region, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-2605 | order_type | employee_name, sales_region | quantity | sum | PASS |
| CP-2606 | order_type | employee_name, sales_region | quantity | mean | PASS |
| CP-2607 | order_type | employee_name, sales_region | quantity | count | PASS |
| CP-2608 | order_type | employee_name, sales_region | unit_price | sum | PASS |
| CP-2609 | order_type | employee_name, sales_region | unit_price | mean | PASS |
| CP-2610 | order_type | employee_name, sales_region | unit_price | count | PASS |
| CP-2611 | order_type | employee_name, sales_region | quantity, unit_price | sum | PASS |
| CP-2612 | order_type | employee_name, sales_region | quantity, unit_price | mean | PASS |
| CP-2613 | order_type | employee_name, sales_region | quantity, unit_price | count | PASS |
| CP-2614 | order_type | employee_name, sales_region | sale_price | sum | PASS |
| CP-2615 | order_type | employee_name, sales_region | sale_price | mean | PASS |
| CP-2616 | order_type | employee_name, sales_region | sale_price | count | PASS |
| CP-2617 | order_type | employee_name, sales_region | quantity, sale_price | sum | PASS |
| CP-2618 | order_type | employee_name, sales_region | quantity, sale_price | mean | PASS |
| CP-2619 | order_type | employee_name, sales_region | quantity, sale_price | count | PASS |
| CP-2620 | order_type | employee_name, sales_region | unit_price, sale_price | sum | PASS |
| CP-2621 | order_type | employee_name, sales_region | unit_price, sale_price | mean | PASS |
| CP-2622 | order_type | employee_name, sales_region | unit_price, sale_price | count | PASS |
| CP-2623 | order_type | employee_name, sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-2624 | order_type | employee_name, sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-2625 | order_type | employee_name, sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-2626 | customer_type | employee_name, sales_region, order_type | quantity | sum | PASS |
| CP-2627 | customer_type | employee_name, sales_region, order_type | quantity | mean | PASS |
| CP-2628 | customer_type | employee_name, sales_region, order_type | quantity | count | PASS |
| CP-2629 | customer_type | employee_name, sales_region, order_type | unit_price | sum | PASS |
| CP-2630 | customer_type | employee_name, sales_region, order_type | unit_price | mean | PASS |
| CP-2631 | customer_type | employee_name, sales_region, order_type | unit_price | count | PASS |
| CP-2632 | customer_type | employee_name, sales_region, order_type | quantity, unit_price | sum | PASS |
| CP-2633 | customer_type | employee_name, sales_region, order_type | quantity, unit_price | mean | PASS |
| CP-2634 | customer_type | employee_name, sales_region, order_type | quantity, unit_price | count | PASS |
| CP-2635 | customer_type | employee_name, sales_region, order_type | sale_price | sum | PASS |
| CP-2636 | customer_type | employee_name, sales_region, order_type | sale_price | mean | PASS |
| CP-2637 | customer_type | employee_name, sales_region, order_type | sale_price | count | PASS |
| CP-2638 | customer_type | employee_name, sales_region, order_type | quantity, sale_price | sum | PASS |
| CP-2639 | customer_type | employee_name, sales_region, order_type | quantity, sale_price | mean | PASS |
| CP-2640 | customer_type | employee_name, sales_region, order_type | quantity, sale_price | count | PASS |
| CP-2641 | customer_type | employee_name, sales_region, order_type | unit_price, sale_price | sum | PASS |
| CP-2642 | customer_type | employee_name, sales_region, order_type | unit_price, sale_price | mean | PASS |
| CP-2643 | customer_type | employee_name, sales_region, order_type | unit_price, sale_price | count | PASS |
| CP-2644 | customer_type | employee_name, sales_region, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2645 | customer_type | employee_name, sales_region, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2646 | customer_type | employee_name, sales_region, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-2647 | customer_type | employee_name, sales_region | quantity | sum | PASS |
| CP-2648 | customer_type | employee_name, sales_region | quantity | mean | PASS |
| CP-2649 | customer_type | employee_name, sales_region | quantity | count | PASS |
| CP-2650 | customer_type | employee_name, sales_region | unit_price | sum | PASS |
| CP-2651 | customer_type | employee_name, sales_region | unit_price | mean | PASS |
| CP-2652 | customer_type | employee_name, sales_region | unit_price | count | PASS |
| CP-2653 | customer_type | employee_name, sales_region | quantity, unit_price | sum | PASS |
| CP-2654 | customer_type | employee_name, sales_region | quantity, unit_price | mean | PASS |
| CP-2655 | customer_type | employee_name, sales_region | quantity, unit_price | count | PASS |
| CP-2656 | customer_type | employee_name, sales_region | sale_price | sum | PASS |
| CP-2657 | customer_type | employee_name, sales_region | sale_price | mean | PASS |
| CP-2658 | customer_type | employee_name, sales_region | sale_price | count | PASS |
| CP-2659 | customer_type | employee_name, sales_region | quantity, sale_price | sum | PASS |
| CP-2660 | customer_type | employee_name, sales_region | quantity, sale_price | mean | PASS |
| CP-2661 | customer_type | employee_name, sales_region | quantity, sale_price | count | PASS |
| CP-2662 | customer_type | employee_name, sales_region | unit_price, sale_price | sum | PASS |
| CP-2663 | customer_type | employee_name, sales_region | unit_price, sale_price | mean | PASS |
| CP-2664 | customer_type | employee_name, sales_region | unit_price, sale_price | count | PASS |
| CP-2665 | customer_type | employee_name, sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-2666 | customer_type | employee_name, sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-2667 | customer_type | employee_name, sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-2668 | product_category, order_type, customer_type | employee_name | quantity | sum | PASS |
| CP-2669 | product_category, order_type, customer_type | employee_name | quantity | mean | PASS |
| CP-2670 | product_category, order_type, customer_type | employee_name | quantity | count | PASS |
| CP-2671 | product_category, order_type, customer_type | employee_name | unit_price | sum | PASS |
| CP-2672 | product_category, order_type, customer_type | employee_name | unit_price | mean | PASS |
| CP-2673 | product_category, order_type, customer_type | employee_name | unit_price | count | PASS |
| CP-2674 | product_category, order_type, customer_type | employee_name | quantity, unit_price | sum | PASS |
| CP-2675 | product_category, order_type, customer_type | employee_name | quantity, unit_price | mean | PASS |
| CP-2676 | product_category, order_type, customer_type | employee_name | quantity, unit_price | count | PASS |
| CP-2677 | product_category, order_type, customer_type | employee_name | sale_price | sum | PASS |
| CP-2678 | product_category, order_type, customer_type | employee_name | sale_price | mean | PASS |
| CP-2679 | product_category, order_type, customer_type | employee_name | sale_price | count | PASS |
| CP-2680 | product_category, order_type, customer_type | employee_name | quantity, sale_price | sum | PASS |
| CP-2681 | product_category, order_type, customer_type | employee_name | quantity, sale_price | mean | PASS |
| CP-2682 | product_category, order_type, customer_type | employee_name | quantity, sale_price | count | PASS |
| CP-2683 | product_category, order_type, customer_type | employee_name | unit_price, sale_price | sum | PASS |
| CP-2684 | product_category, order_type, customer_type | employee_name | unit_price, sale_price | mean | PASS |
| CP-2685 | product_category, order_type, customer_type | employee_name | unit_price, sale_price | count | PASS |
| CP-2686 | product_category, order_type, customer_type | employee_name | quantity, unit_price, sale_price | sum | PASS |
| CP-2687 | product_category, order_type, customer_type | employee_name | quantity, unit_price, sale_price | mean | PASS |
| CP-2688 | product_category, order_type, customer_type | employee_name | quantity, unit_price, sale_price | count | PASS |
| CP-2689 | product_category, order_type | employee_name, customer_type | quantity | sum | PASS |
| CP-2690 | product_category, order_type | employee_name, customer_type | quantity | mean | PASS |
| CP-2691 | product_category, order_type | employee_name, customer_type | quantity | count | PASS |
| CP-2692 | product_category, order_type | employee_name, customer_type | unit_price | sum | PASS |
| CP-2693 | product_category, order_type | employee_name, customer_type | unit_price | mean | PASS |
| CP-2694 | product_category, order_type | employee_name, customer_type | unit_price | count | PASS |
| CP-2695 | product_category, order_type | employee_name, customer_type | quantity, unit_price | sum | PASS |
| CP-2696 | product_category, order_type | employee_name, customer_type | quantity, unit_price | mean | PASS |
| CP-2697 | product_category, order_type | employee_name, customer_type | quantity, unit_price | count | PASS |
| CP-2698 | product_category, order_type | employee_name, customer_type | sale_price | sum | PASS |
| CP-2699 | product_category, order_type | employee_name, customer_type | sale_price | mean | PASS |
| CP-2700 | product_category, order_type | employee_name, customer_type | sale_price | count | PASS |
| CP-2701 | product_category, order_type | employee_name, customer_type | quantity, sale_price | sum | PASS |
| CP-2702 | product_category, order_type | employee_name, customer_type | quantity, sale_price | mean | PASS |
| CP-2703 | product_category, order_type | employee_name, customer_type | quantity, sale_price | count | PASS |
| CP-2704 | product_category, order_type | employee_name, customer_type | unit_price, sale_price | sum | PASS |
| CP-2705 | product_category, order_type | employee_name, customer_type | unit_price, sale_price | mean | PASS |
| CP-2706 | product_category, order_type | employee_name, customer_type | unit_price, sale_price | count | PASS |
| CP-2707 | product_category, order_type | employee_name, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2708 | product_category, order_type | employee_name, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2709 | product_category, order_type | employee_name, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-2710 | product_category, order_type | employee_name | quantity | sum | PASS |
| CP-2711 | product_category, order_type | employee_name | quantity | mean | PASS |
| CP-2712 | product_category, order_type | employee_name | quantity | count | PASS |
| CP-2713 | product_category, order_type | employee_name | unit_price | sum | PASS |
| CP-2714 | product_category, order_type | employee_name | unit_price | mean | PASS |
| CP-2715 | product_category, order_type | employee_name | unit_price | count | PASS |
| CP-2716 | product_category, order_type | employee_name | quantity, unit_price | sum | PASS |
| CP-2717 | product_category, order_type | employee_name | quantity, unit_price | mean | PASS |
| CP-2718 | product_category, order_type | employee_name | quantity, unit_price | count | PASS |
| CP-2719 | product_category, order_type | employee_name | sale_price | sum | PASS |
| CP-2720 | product_category, order_type | employee_name | sale_price | mean | PASS |
| CP-2721 | product_category, order_type | employee_name | sale_price | count | PASS |
| CP-2722 | product_category, order_type | employee_name | quantity, sale_price | sum | PASS |
| CP-2723 | product_category, order_type | employee_name | quantity, sale_price | mean | PASS |
| CP-2724 | product_category, order_type | employee_name | quantity, sale_price | count | PASS |
| CP-2725 | product_category, order_type | employee_name | unit_price, sale_price | sum | PASS |
| CP-2726 | product_category, order_type | employee_name | unit_price, sale_price | mean | PASS |
| CP-2727 | product_category, order_type | employee_name | unit_price, sale_price | count | PASS |
| CP-2728 | product_category, order_type | employee_name | quantity, unit_price, sale_price | sum | PASS |
| CP-2729 | product_category, order_type | employee_name | quantity, unit_price, sale_price | mean | PASS |
| CP-2730 | product_category, order_type | employee_name | quantity, unit_price, sale_price | count | PASS |
| CP-2731 | product_category, customer_type | employee_name, order_type | quantity | sum | PASS |
| CP-2732 | product_category, customer_type | employee_name, order_type | quantity | mean | PASS |
| CP-2733 | product_category, customer_type | employee_name, order_type | quantity | count | PASS |
| CP-2734 | product_category, customer_type | employee_name, order_type | unit_price | sum | PASS |
| CP-2735 | product_category, customer_type | employee_name, order_type | unit_price | mean | PASS |
| CP-2736 | product_category, customer_type | employee_name, order_type | unit_price | count | PASS |
| CP-2737 | product_category, customer_type | employee_name, order_type | quantity, unit_price | sum | PASS |
| CP-2738 | product_category, customer_type | employee_name, order_type | quantity, unit_price | mean | PASS |
| CP-2739 | product_category, customer_type | employee_name, order_type | quantity, unit_price | count | PASS |
| CP-2740 | product_category, customer_type | employee_name, order_type | sale_price | sum | PASS |
| CP-2741 | product_category, customer_type | employee_name, order_type | sale_price | mean | PASS |
| CP-2742 | product_category, customer_type | employee_name, order_type | sale_price | count | PASS |
| CP-2743 | product_category, customer_type | employee_name, order_type | quantity, sale_price | sum | PASS |
| CP-2744 | product_category, customer_type | employee_name, order_type | quantity, sale_price | mean | PASS |
| CP-2745 | product_category, customer_type | employee_name, order_type | quantity, sale_price | count | PASS |
| CP-2746 | product_category, customer_type | employee_name, order_type | unit_price, sale_price | sum | PASS |
| CP-2747 | product_category, customer_type | employee_name, order_type | unit_price, sale_price | mean | PASS |
| CP-2748 | product_category, customer_type | employee_name, order_type | unit_price, sale_price | count | PASS |
| CP-2749 | product_category, customer_type | employee_name, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2750 | product_category, customer_type | employee_name, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2751 | product_category, customer_type | employee_name, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-2752 | product_category | employee_name, order_type, customer_type | quantity | sum | PASS |
| CP-2753 | product_category | employee_name, order_type, customer_type | quantity | mean | PASS |
| CP-2754 | product_category | employee_name, order_type, customer_type | quantity | count | PASS |
| CP-2755 | product_category | employee_name, order_type, customer_type | unit_price | sum | PASS |
| CP-2756 | product_category | employee_name, order_type, customer_type | unit_price | mean | PASS |
| CP-2757 | product_category | employee_name, order_type, customer_type | unit_price | count | PASS |
| CP-2758 | product_category | employee_name, order_type, customer_type | quantity, unit_price | sum | PASS |
| CP-2759 | product_category | employee_name, order_type, customer_type | quantity, unit_price | mean | PASS |
| CP-2760 | product_category | employee_name, order_type, customer_type | quantity, unit_price | count | PASS |
| CP-2761 | product_category | employee_name, order_type, customer_type | sale_price | sum | PASS |
| CP-2762 | product_category | employee_name, order_type, customer_type | sale_price | mean | PASS |
| CP-2763 | product_category | employee_name, order_type, customer_type | sale_price | count | PASS |
| CP-2764 | product_category | employee_name, order_type, customer_type | quantity, sale_price | sum | PASS |
| CP-2765 | product_category | employee_name, order_type, customer_type | quantity, sale_price | mean | PASS |
| CP-2766 | product_category | employee_name, order_type, customer_type | quantity, sale_price | count | PASS |
| CP-2767 | product_category | employee_name, order_type, customer_type | unit_price, sale_price | sum | PASS |
| CP-2768 | product_category | employee_name, order_type, customer_type | unit_price, sale_price | mean | PASS |
| CP-2769 | product_category | employee_name, order_type, customer_type | unit_price, sale_price | count | PASS |
| CP-2770 | product_category | employee_name, order_type, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2771 | product_category | employee_name, order_type, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2772 | product_category | employee_name, order_type, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-2773 | product_category | employee_name, order_type | quantity | sum | PASS |
| CP-2774 | product_category | employee_name, order_type | quantity | mean | PASS |
| CP-2775 | product_category | employee_name, order_type | quantity | count | PASS |
| CP-2776 | product_category | employee_name, order_type | unit_price | sum | PASS |
| CP-2777 | product_category | employee_name, order_type | unit_price | mean | PASS |
| CP-2778 | product_category | employee_name, order_type | unit_price | count | PASS |
| CP-2779 | product_category | employee_name, order_type | quantity, unit_price | sum | PASS |
| CP-2780 | product_category | employee_name, order_type | quantity, unit_price | mean | PASS |
| CP-2781 | product_category | employee_name, order_type | quantity, unit_price | count | PASS |
| CP-2782 | product_category | employee_name, order_type | sale_price | sum | PASS |
| CP-2783 | product_category | employee_name, order_type | sale_price | mean | PASS |
| CP-2784 | product_category | employee_name, order_type | sale_price | count | PASS |
| CP-2785 | product_category | employee_name, order_type | quantity, sale_price | sum | PASS |
| CP-2786 | product_category | employee_name, order_type | quantity, sale_price | mean | PASS |
| CP-2787 | product_category | employee_name, order_type | quantity, sale_price | count | PASS |
| CP-2788 | product_category | employee_name, order_type | unit_price, sale_price | sum | PASS |
| CP-2789 | product_category | employee_name, order_type | unit_price, sale_price | mean | PASS |
| CP-2790 | product_category | employee_name, order_type | unit_price, sale_price | count | PASS |
| CP-2791 | product_category | employee_name, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2792 | product_category | employee_name, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2793 | product_category | employee_name, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-2794 | product_category, customer_type | employee_name | quantity | sum | PASS |
| CP-2795 | product_category, customer_type | employee_name | quantity | mean | PASS |
| CP-2796 | product_category, customer_type | employee_name | quantity | count | PASS |
| CP-2797 | product_category, customer_type | employee_name | unit_price | sum | PASS |
| CP-2798 | product_category, customer_type | employee_name | unit_price | mean | PASS |
| CP-2799 | product_category, customer_type | employee_name | unit_price | count | PASS |
| CP-2800 | product_category, customer_type | employee_name | quantity, unit_price | sum | PASS |
| CP-2801 | product_category, customer_type | employee_name | quantity, unit_price | mean | PASS |
| CP-2802 | product_category, customer_type | employee_name | quantity, unit_price | count | PASS |
| CP-2803 | product_category, customer_type | employee_name | sale_price | sum | PASS |
| CP-2804 | product_category, customer_type | employee_name | sale_price | mean | PASS |
| CP-2805 | product_category, customer_type | employee_name | sale_price | count | PASS |
| CP-2806 | product_category, customer_type | employee_name | quantity, sale_price | sum | PASS |
| CP-2807 | product_category, customer_type | employee_name | quantity, sale_price | mean | PASS |
| CP-2808 | product_category, customer_type | employee_name | quantity, sale_price | count | PASS |
| CP-2809 | product_category, customer_type | employee_name | unit_price, sale_price | sum | PASS |
| CP-2810 | product_category, customer_type | employee_name | unit_price, sale_price | mean | PASS |
| CP-2811 | product_category, customer_type | employee_name | unit_price, sale_price | count | PASS |
| CP-2812 | product_category, customer_type | employee_name | quantity, unit_price, sale_price | sum | PASS |
| CP-2813 | product_category, customer_type | employee_name | quantity, unit_price, sale_price | mean | PASS |
| CP-2814 | product_category, customer_type | employee_name | quantity, unit_price, sale_price | count | PASS |
| CP-2815 | product_category | employee_name, customer_type | quantity | sum | PASS |
| CP-2816 | product_category | employee_name, customer_type | quantity | mean | PASS |
| CP-2817 | product_category | employee_name, customer_type | quantity | count | PASS |
| CP-2818 | product_category | employee_name, customer_type | unit_price | sum | PASS |
| CP-2819 | product_category | employee_name, customer_type | unit_price | mean | PASS |
| CP-2820 | product_category | employee_name, customer_type | unit_price | count | PASS |
| CP-2821 | product_category | employee_name, customer_type | quantity, unit_price | sum | PASS |
| CP-2822 | product_category | employee_name, customer_type | quantity, unit_price | mean | PASS |
| CP-2823 | product_category | employee_name, customer_type | quantity, unit_price | count | PASS |
| CP-2824 | product_category | employee_name, customer_type | sale_price | sum | PASS |
| CP-2825 | product_category | employee_name, customer_type | sale_price | mean | PASS |
| CP-2826 | product_category | employee_name, customer_type | sale_price | count | PASS |
| CP-2827 | product_category | employee_name, customer_type | quantity, sale_price | sum | PASS |
| CP-2828 | product_category | employee_name, customer_type | quantity, sale_price | mean | PASS |
| CP-2829 | product_category | employee_name, customer_type | quantity, sale_price | count | PASS |
| CP-2830 | product_category | employee_name, customer_type | unit_price, sale_price | sum | PASS |
| CP-2831 | product_category | employee_name, customer_type | unit_price, sale_price | mean | PASS |
| CP-2832 | product_category | employee_name, customer_type | unit_price, sale_price | count | PASS |
| CP-2833 | product_category | employee_name, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2834 | product_category | employee_name, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2835 | product_category | employee_name, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-2836 | product_category | employee_name | quantity | sum | PASS |
| CP-2837 | product_category | employee_name | quantity | mean | PASS |
| CP-2838 | product_category | employee_name | quantity | count | PASS |
| CP-2839 | product_category | employee_name | unit_price | sum | PASS |
| CP-2840 | product_category | employee_name | unit_price | mean | PASS |
| CP-2841 | product_category | employee_name | unit_price | count | PASS |
| CP-2842 | product_category | employee_name | quantity, unit_price | sum | PASS |
| CP-2843 | product_category | employee_name | quantity, unit_price | mean | PASS |
| CP-2844 | product_category | employee_name | quantity, unit_price | count | PASS |
| CP-2845 | product_category | employee_name | sale_price | sum | PASS |
| CP-2846 | product_category | employee_name | sale_price | mean | PASS |
| CP-2847 | product_category | employee_name | sale_price | count | PASS |
| CP-2848 | product_category | employee_name | quantity, sale_price | sum | PASS |
| CP-2849 | product_category | employee_name | quantity, sale_price | mean | PASS |
| CP-2850 | product_category | employee_name | quantity, sale_price | count | PASS |
| CP-2851 | product_category | employee_name | unit_price, sale_price | sum | PASS |
| CP-2852 | product_category | employee_name | unit_price, sale_price | mean | PASS |
| CP-2853 | product_category | employee_name | unit_price, sale_price | count | PASS |
| CP-2854 | product_category | employee_name | quantity, unit_price, sale_price | sum | PASS |
| CP-2855 | product_category | employee_name | quantity, unit_price, sale_price | mean | PASS |
| CP-2856 | product_category | employee_name | quantity, unit_price, sale_price | count | PASS |
| CP-2857 | order_type, customer_type | employee_name, product_category | quantity | sum | PASS |
| CP-2858 | order_type, customer_type | employee_name, product_category | quantity | mean | PASS |
| CP-2859 | order_type, customer_type | employee_name, product_category | quantity | count | PASS |
| CP-2860 | order_type, customer_type | employee_name, product_category | unit_price | sum | PASS |
| CP-2861 | order_type, customer_type | employee_name, product_category | unit_price | mean | PASS |
| CP-2862 | order_type, customer_type | employee_name, product_category | unit_price | count | PASS |
| CP-2863 | order_type, customer_type | employee_name, product_category | quantity, unit_price | sum | PASS |
| CP-2864 | order_type, customer_type | employee_name, product_category | quantity, unit_price | mean | PASS |
| CP-2865 | order_type, customer_type | employee_name, product_category | quantity, unit_price | count | PASS |
| CP-2866 | order_type, customer_type | employee_name, product_category | sale_price | sum | PASS |
| CP-2867 | order_type, customer_type | employee_name, product_category | sale_price | mean | PASS |
| CP-2868 | order_type, customer_type | employee_name, product_category | sale_price | count | PASS |
| CP-2869 | order_type, customer_type | employee_name, product_category | quantity, sale_price | sum | PASS |
| CP-2870 | order_type, customer_type | employee_name, product_category | quantity, sale_price | mean | PASS |
| CP-2871 | order_type, customer_type | employee_name, product_category | quantity, sale_price | count | PASS |
| CP-2872 | order_type, customer_type | employee_name, product_category | unit_price, sale_price | sum | PASS |
| CP-2873 | order_type, customer_type | employee_name, product_category | unit_price, sale_price | mean | PASS |
| CP-2874 | order_type, customer_type | employee_name, product_category | unit_price, sale_price | count | PASS |
| CP-2875 | order_type, customer_type | employee_name, product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-2876 | order_type, customer_type | employee_name, product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-2877 | order_type, customer_type | employee_name, product_category | quantity, unit_price, sale_price | count | PASS |
| CP-2878 | order_type | employee_name, product_category, customer_type | quantity | sum | PASS |
| CP-2879 | order_type | employee_name, product_category, customer_type | quantity | mean | PASS |
| CP-2880 | order_type | employee_name, product_category, customer_type | quantity | count | PASS |
| CP-2881 | order_type | employee_name, product_category, customer_type | unit_price | sum | PASS |
| CP-2882 | order_type | employee_name, product_category, customer_type | unit_price | mean | PASS |
| CP-2883 | order_type | employee_name, product_category, customer_type | unit_price | count | PASS |
| CP-2884 | order_type | employee_name, product_category, customer_type | quantity, unit_price | sum | PASS |
| CP-2885 | order_type | employee_name, product_category, customer_type | quantity, unit_price | mean | PASS |
| CP-2886 | order_type | employee_name, product_category, customer_type | quantity, unit_price | count | PASS |
| CP-2887 | order_type | employee_name, product_category, customer_type | sale_price | sum | PASS |
| CP-2888 | order_type | employee_name, product_category, customer_type | sale_price | mean | PASS |
| CP-2889 | order_type | employee_name, product_category, customer_type | sale_price | count | PASS |
| CP-2890 | order_type | employee_name, product_category, customer_type | quantity, sale_price | sum | PASS |
| CP-2891 | order_type | employee_name, product_category, customer_type | quantity, sale_price | mean | PASS |
| CP-2892 | order_type | employee_name, product_category, customer_type | quantity, sale_price | count | PASS |
| CP-2893 | order_type | employee_name, product_category, customer_type | unit_price, sale_price | sum | PASS |
| CP-2894 | order_type | employee_name, product_category, customer_type | unit_price, sale_price | mean | PASS |
| CP-2895 | order_type | employee_name, product_category, customer_type | unit_price, sale_price | count | PASS |
| CP-2896 | order_type | employee_name, product_category, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2897 | order_type | employee_name, product_category, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2898 | order_type | employee_name, product_category, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-2899 | order_type | employee_name, product_category | quantity | sum | PASS |
| CP-2900 | order_type | employee_name, product_category | quantity | mean | PASS |
| CP-2901 | order_type | employee_name, product_category | quantity | count | PASS |
| CP-2902 | order_type | employee_name, product_category | unit_price | sum | PASS |
| CP-2903 | order_type | employee_name, product_category | unit_price | mean | PASS |
| CP-2904 | order_type | employee_name, product_category | unit_price | count | PASS |
| CP-2905 | order_type | employee_name, product_category | quantity, unit_price | sum | PASS |
| CP-2906 | order_type | employee_name, product_category | quantity, unit_price | mean | PASS |
| CP-2907 | order_type | employee_name, product_category | quantity, unit_price | count | PASS |
| CP-2908 | order_type | employee_name, product_category | sale_price | sum | PASS |
| CP-2909 | order_type | employee_name, product_category | sale_price | mean | PASS |
| CP-2910 | order_type | employee_name, product_category | sale_price | count | PASS |
| CP-2911 | order_type | employee_name, product_category | quantity, sale_price | sum | PASS |
| CP-2912 | order_type | employee_name, product_category | quantity, sale_price | mean | PASS |
| CP-2913 | order_type | employee_name, product_category | quantity, sale_price | count | PASS |
| CP-2914 | order_type | employee_name, product_category | unit_price, sale_price | sum | PASS |
| CP-2915 | order_type | employee_name, product_category | unit_price, sale_price | mean | PASS |
| CP-2916 | order_type | employee_name, product_category | unit_price, sale_price | count | PASS |
| CP-2917 | order_type | employee_name, product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-2918 | order_type | employee_name, product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-2919 | order_type | employee_name, product_category | quantity, unit_price, sale_price | count | PASS |
| CP-2920 | customer_type | employee_name, product_category, order_type | quantity | sum | PASS |
| CP-2921 | customer_type | employee_name, product_category, order_type | quantity | mean | PASS |
| CP-2922 | customer_type | employee_name, product_category, order_type | quantity | count | PASS |
| CP-2923 | customer_type | employee_name, product_category, order_type | unit_price | sum | PASS |
| CP-2924 | customer_type | employee_name, product_category, order_type | unit_price | mean | PASS |
| CP-2925 | customer_type | employee_name, product_category, order_type | unit_price | count | PASS |
| CP-2926 | customer_type | employee_name, product_category, order_type | quantity, unit_price | sum | PASS |
| CP-2927 | customer_type | employee_name, product_category, order_type | quantity, unit_price | mean | PASS |
| CP-2928 | customer_type | employee_name, product_category, order_type | quantity, unit_price | count | PASS |
| CP-2929 | customer_type | employee_name, product_category, order_type | sale_price | sum | PASS |
| CP-2930 | customer_type | employee_name, product_category, order_type | sale_price | mean | PASS |
| CP-2931 | customer_type | employee_name, product_category, order_type | sale_price | count | PASS |
| CP-2932 | customer_type | employee_name, product_category, order_type | quantity, sale_price | sum | PASS |
| CP-2933 | customer_type | employee_name, product_category, order_type | quantity, sale_price | mean | PASS |
| CP-2934 | customer_type | employee_name, product_category, order_type | quantity, sale_price | count | PASS |
| CP-2935 | customer_type | employee_name, product_category, order_type | unit_price, sale_price | sum | PASS |
| CP-2936 | customer_type | employee_name, product_category, order_type | unit_price, sale_price | mean | PASS |
| CP-2937 | customer_type | employee_name, product_category, order_type | unit_price, sale_price | count | PASS |
| CP-2938 | customer_type | employee_name, product_category, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-2939 | customer_type | employee_name, product_category, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-2940 | customer_type | employee_name, product_category, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-2941 | customer_type | employee_name, product_category | quantity | sum | PASS |
| CP-2942 | customer_type | employee_name, product_category | quantity | mean | PASS |
| CP-2943 | customer_type | employee_name, product_category | quantity | count | PASS |
| CP-2944 | customer_type | employee_name, product_category | unit_price | sum | PASS |
| CP-2945 | customer_type | employee_name, product_category | unit_price | mean | PASS |
| CP-2946 | customer_type | employee_name, product_category | unit_price | count | PASS |
| CP-2947 | customer_type | employee_name, product_category | quantity, unit_price | sum | PASS |
| CP-2948 | customer_type | employee_name, product_category | quantity, unit_price | mean | PASS |
| CP-2949 | customer_type | employee_name, product_category | quantity, unit_price | count | PASS |
| CP-2950 | customer_type | employee_name, product_category | sale_price | sum | PASS |
| CP-2951 | customer_type | employee_name, product_category | sale_price | mean | PASS |
| CP-2952 | customer_type | employee_name, product_category | sale_price | count | PASS |
| CP-2953 | customer_type | employee_name, product_category | quantity, sale_price | sum | PASS |
| CP-2954 | customer_type | employee_name, product_category | quantity, sale_price | mean | PASS |
| CP-2955 | customer_type | employee_name, product_category | quantity, sale_price | count | PASS |
| CP-2956 | customer_type | employee_name, product_category | unit_price, sale_price | sum | PASS |
| CP-2957 | customer_type | employee_name, product_category | unit_price, sale_price | mean | PASS |
| CP-2958 | customer_type | employee_name, product_category | unit_price, sale_price | count | PASS |
| CP-2959 | customer_type | employee_name, product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-2960 | customer_type | employee_name, product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-2961 | customer_type | employee_name, product_category | quantity, unit_price, sale_price | count | PASS |
| CP-2962 | order_type, customer_type | employee_name | quantity | sum | PASS |
| CP-2963 | order_type, customer_type | employee_name | quantity | mean | PASS |
| CP-2964 | order_type, customer_type | employee_name | quantity | count | PASS |
| CP-2965 | order_type, customer_type | employee_name | unit_price | sum | PASS |
| CP-2966 | order_type, customer_type | employee_name | unit_price | mean | PASS |
| CP-2967 | order_type, customer_type | employee_name | unit_price | count | PASS |
| CP-2968 | order_type, customer_type | employee_name | quantity, unit_price | sum | PASS |
| CP-2969 | order_type, customer_type | employee_name | quantity, unit_price | mean | PASS |
| CP-2970 | order_type, customer_type | employee_name | quantity, unit_price | count | PASS |
| CP-2971 | order_type, customer_type | employee_name | sale_price | sum | PASS |
| CP-2972 | order_type, customer_type | employee_name | sale_price | mean | PASS |
| CP-2973 | order_type, customer_type | employee_name | sale_price | count | PASS |
| CP-2974 | order_type, customer_type | employee_name | quantity, sale_price | sum | PASS |
| CP-2975 | order_type, customer_type | employee_name | quantity, sale_price | mean | PASS |
| CP-2976 | order_type, customer_type | employee_name | quantity, sale_price | count | PASS |
| CP-2977 | order_type, customer_type | employee_name | unit_price, sale_price | sum | PASS |
| CP-2978 | order_type, customer_type | employee_name | unit_price, sale_price | mean | PASS |
| CP-2979 | order_type, customer_type | employee_name | unit_price, sale_price | count | PASS |
| CP-2980 | order_type, customer_type | employee_name | quantity, unit_price, sale_price | sum | PASS |
| CP-2981 | order_type, customer_type | employee_name | quantity, unit_price, sale_price | mean | PASS |
| CP-2982 | order_type, customer_type | employee_name | quantity, unit_price, sale_price | count | PASS |
| CP-2983 | order_type | employee_name, customer_type | quantity | sum | PASS |
| CP-2984 | order_type | employee_name, customer_type | quantity | mean | PASS |
| CP-2985 | order_type | employee_name, customer_type | quantity | count | PASS |
| CP-2986 | order_type | employee_name, customer_type | unit_price | sum | PASS |
| CP-2987 | order_type | employee_name, customer_type | unit_price | mean | PASS |
| CP-2988 | order_type | employee_name, customer_type | unit_price | count | PASS |
| CP-2989 | order_type | employee_name, customer_type | quantity, unit_price | sum | PASS |
| CP-2990 | order_type | employee_name, customer_type | quantity, unit_price | mean | PASS |
| CP-2991 | order_type | employee_name, customer_type | quantity, unit_price | count | PASS |
| CP-2992 | order_type | employee_name, customer_type | sale_price | sum | PASS |
| CP-2993 | order_type | employee_name, customer_type | sale_price | mean | PASS |
| CP-2994 | order_type | employee_name, customer_type | sale_price | count | PASS |
| CP-2995 | order_type | employee_name, customer_type | quantity, sale_price | sum | PASS |
| CP-2996 | order_type | employee_name, customer_type | quantity, sale_price | mean | PASS |
| CP-2997 | order_type | employee_name, customer_type | quantity, sale_price | count | PASS |
| CP-2998 | order_type | employee_name, customer_type | unit_price, sale_price | sum | PASS |
| CP-2999 | order_type | employee_name, customer_type | unit_price, sale_price | mean | PASS |
| CP-3000 | order_type | employee_name, customer_type | unit_price, sale_price | count | PASS |
| CP-3001 | order_type | employee_name, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3002 | order_type | employee_name, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3003 | order_type | employee_name, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-3004 | order_type | employee_name | quantity | sum | PASS |
| CP-3005 | order_type | employee_name | quantity | mean | PASS |
| CP-3006 | order_type | employee_name | quantity | count | PASS |
| CP-3007 | order_type | employee_name | unit_price | sum | PASS |
| CP-3008 | order_type | employee_name | unit_price | mean | PASS |
| CP-3009 | order_type | employee_name | unit_price | count | PASS |
| CP-3010 | order_type | employee_name | quantity, unit_price | sum | PASS |
| CP-3011 | order_type | employee_name | quantity, unit_price | mean | PASS |
| CP-3012 | order_type | employee_name | quantity, unit_price | count | PASS |
| CP-3013 | order_type | employee_name | sale_price | sum | PASS |
| CP-3014 | order_type | employee_name | sale_price | mean | PASS |
| CP-3015 | order_type | employee_name | sale_price | count | PASS |
| CP-3016 | order_type | employee_name | quantity, sale_price | sum | PASS |
| CP-3017 | order_type | employee_name | quantity, sale_price | mean | PASS |
| CP-3018 | order_type | employee_name | quantity, sale_price | count | PASS |
| CP-3019 | order_type | employee_name | unit_price, sale_price | sum | PASS |
| CP-3020 | order_type | employee_name | unit_price, sale_price | mean | PASS |
| CP-3021 | order_type | employee_name | unit_price, sale_price | count | PASS |
| CP-3022 | order_type | employee_name | quantity, unit_price, sale_price | sum | PASS |
| CP-3023 | order_type | employee_name | quantity, unit_price, sale_price | mean | PASS |
| CP-3024 | order_type | employee_name | quantity, unit_price, sale_price | count | PASS |
| CP-3025 | customer_type | employee_name, order_type | quantity | sum | PASS |
| CP-3026 | customer_type | employee_name, order_type | quantity | mean | PASS |
| CP-3027 | customer_type | employee_name, order_type | quantity | count | PASS |
| CP-3028 | customer_type | employee_name, order_type | unit_price | sum | PASS |
| CP-3029 | customer_type | employee_name, order_type | unit_price | mean | PASS |
| CP-3030 | customer_type | employee_name, order_type | unit_price | count | PASS |
| CP-3031 | customer_type | employee_name, order_type | quantity, unit_price | sum | PASS |
| CP-3032 | customer_type | employee_name, order_type | quantity, unit_price | mean | PASS |
| CP-3033 | customer_type | employee_name, order_type | quantity, unit_price | count | PASS |
| CP-3034 | customer_type | employee_name, order_type | sale_price | sum | PASS |
| CP-3035 | customer_type | employee_name, order_type | sale_price | mean | PASS |
| CP-3036 | customer_type | employee_name, order_type | sale_price | count | PASS |
| CP-3037 | customer_type | employee_name, order_type | quantity, sale_price | sum | PASS |
| CP-3038 | customer_type | employee_name, order_type | quantity, sale_price | mean | PASS |
| CP-3039 | customer_type | employee_name, order_type | quantity, sale_price | count | PASS |
| CP-3040 | customer_type | employee_name, order_type | unit_price, sale_price | sum | PASS |
| CP-3041 | customer_type | employee_name, order_type | unit_price, sale_price | mean | PASS |
| CP-3042 | customer_type | employee_name, order_type | unit_price, sale_price | count | PASS |
| CP-3043 | customer_type | employee_name, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3044 | customer_type | employee_name, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3045 | customer_type | employee_name, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-3046 | customer_type | employee_name | quantity | sum | PASS |
| CP-3047 | customer_type | employee_name | quantity | mean | PASS |
| CP-3048 | customer_type | employee_name | quantity | count | PASS |
| CP-3049 | customer_type | employee_name | unit_price | sum | PASS |
| CP-3050 | customer_type | employee_name | unit_price | mean | PASS |
| CP-3051 | customer_type | employee_name | unit_price | count | PASS |
| CP-3052 | customer_type | employee_name | quantity, unit_price | sum | PASS |
| CP-3053 | customer_type | employee_name | quantity, unit_price | mean | PASS |
| CP-3054 | customer_type | employee_name | quantity, unit_price | count | PASS |
| CP-3055 | customer_type | employee_name | sale_price | sum | PASS |
| CP-3056 | customer_type | employee_name | sale_price | mean | PASS |
| CP-3057 | customer_type | employee_name | sale_price | count | PASS |
| CP-3058 | customer_type | employee_name | quantity, sale_price | sum | PASS |
| CP-3059 | customer_type | employee_name | quantity, sale_price | mean | PASS |
| CP-3060 | customer_type | employee_name | quantity, sale_price | count | PASS |
| CP-3061 | customer_type | employee_name | unit_price, sale_price | sum | PASS |
| CP-3062 | customer_type | employee_name | unit_price, sale_price | mean | PASS |
| CP-3063 | customer_type | employee_name | unit_price, sale_price | count | PASS |
| CP-3064 | customer_type | employee_name | quantity, unit_price, sale_price | sum | PASS |
| CP-3065 | customer_type | employee_name | quantity, unit_price, sale_price | mean | PASS |
| CP-3066 | customer_type | employee_name | quantity, unit_price, sale_price | count | PASS |
| CP-3067 | sales_region, product_category, order_type, customer_type | - | quantity | sum | PASS |
| CP-3068 | sales_region, product_category, order_type, customer_type | - | quantity | mean | PASS |
| CP-3069 | sales_region, product_category, order_type, customer_type | - | quantity | count | PASS |
| CP-3070 | sales_region, product_category, order_type, customer_type | - | unit_price | sum | PASS |
| CP-3071 | sales_region, product_category, order_type, customer_type | - | unit_price | mean | PASS |
| CP-3072 | sales_region, product_category, order_type, customer_type | - | unit_price | count | PASS |
| CP-3073 | sales_region, product_category, order_type, customer_type | - | quantity, unit_price | sum | PASS |
| CP-3074 | sales_region, product_category, order_type, customer_type | - | quantity, unit_price | mean | PASS |
| CP-3075 | sales_region, product_category, order_type, customer_type | - | quantity, unit_price | count | PASS |
| CP-3076 | sales_region, product_category, order_type, customer_type | - | sale_price | sum | PASS |
| CP-3077 | sales_region, product_category, order_type, customer_type | - | sale_price | mean | PASS |
| CP-3078 | sales_region, product_category, order_type, customer_type | - | sale_price | count | PASS |
| CP-3079 | sales_region, product_category, order_type, customer_type | - | quantity, sale_price | sum | PASS |
| CP-3080 | sales_region, product_category, order_type, customer_type | - | quantity, sale_price | mean | PASS |
| CP-3081 | sales_region, product_category, order_type, customer_type | - | quantity, sale_price | count | PASS |
| CP-3082 | sales_region, product_category, order_type, customer_type | - | unit_price, sale_price | sum | PASS |
| CP-3083 | sales_region, product_category, order_type, customer_type | - | unit_price, sale_price | mean | PASS |
| CP-3084 | sales_region, product_category, order_type, customer_type | - | unit_price, sale_price | count | PASS |
| CP-3085 | sales_region, product_category, order_type, customer_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-3086 | sales_region, product_category, order_type, customer_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-3087 | sales_region, product_category, order_type, customer_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-3088 | sales_region, product_category, order_type | customer_type | quantity | sum | PASS |
| CP-3089 | sales_region, product_category, order_type | customer_type | quantity | mean | PASS |
| CP-3090 | sales_region, product_category, order_type | customer_type | quantity | count | PASS |
| CP-3091 | sales_region, product_category, order_type | customer_type | unit_price | sum | PASS |
| CP-3092 | sales_region, product_category, order_type | customer_type | unit_price | mean | PASS |
| CP-3093 | sales_region, product_category, order_type | customer_type | unit_price | count | PASS |
| CP-3094 | sales_region, product_category, order_type | customer_type | quantity, unit_price | sum | PASS |
| CP-3095 | sales_region, product_category, order_type | customer_type | quantity, unit_price | mean | PASS |
| CP-3096 | sales_region, product_category, order_type | customer_type | quantity, unit_price | count | PASS |
| CP-3097 | sales_region, product_category, order_type | customer_type | sale_price | sum | PASS |
| CP-3098 | sales_region, product_category, order_type | customer_type | sale_price | mean | PASS |
| CP-3099 | sales_region, product_category, order_type | customer_type | sale_price | count | PASS |
| CP-3100 | sales_region, product_category, order_type | customer_type | quantity, sale_price | sum | PASS |
| CP-3101 | sales_region, product_category, order_type | customer_type | quantity, sale_price | mean | PASS |
| CP-3102 | sales_region, product_category, order_type | customer_type | quantity, sale_price | count | PASS |
| CP-3103 | sales_region, product_category, order_type | customer_type | unit_price, sale_price | sum | PASS |
| CP-3104 | sales_region, product_category, order_type | customer_type | unit_price, sale_price | mean | PASS |
| CP-3105 | sales_region, product_category, order_type | customer_type | unit_price, sale_price | count | PASS |
| CP-3106 | sales_region, product_category, order_type | customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3107 | sales_region, product_category, order_type | customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3108 | sales_region, product_category, order_type | customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-3109 | sales_region, product_category, order_type | - | quantity | sum | PASS |
| CP-3110 | sales_region, product_category, order_type | - | quantity | mean | PASS |
| CP-3111 | sales_region, product_category, order_type | - | quantity | count | PASS |
| CP-3112 | sales_region, product_category, order_type | - | unit_price | sum | PASS |
| CP-3113 | sales_region, product_category, order_type | - | unit_price | mean | PASS |
| CP-3114 | sales_region, product_category, order_type | - | unit_price | count | PASS |
| CP-3115 | sales_region, product_category, order_type | - | quantity, unit_price | sum | PASS |
| CP-3116 | sales_region, product_category, order_type | - | quantity, unit_price | mean | PASS |
| CP-3117 | sales_region, product_category, order_type | - | quantity, unit_price | count | PASS |
| CP-3118 | sales_region, product_category, order_type | - | sale_price | sum | PASS |
| CP-3119 | sales_region, product_category, order_type | - | sale_price | mean | PASS |
| CP-3120 | sales_region, product_category, order_type | - | sale_price | count | PASS |
| CP-3121 | sales_region, product_category, order_type | - | quantity, sale_price | sum | PASS |
| CP-3122 | sales_region, product_category, order_type | - | quantity, sale_price | mean | PASS |
| CP-3123 | sales_region, product_category, order_type | - | quantity, sale_price | count | PASS |
| CP-3124 | sales_region, product_category, order_type | - | unit_price, sale_price | sum | PASS |
| CP-3125 | sales_region, product_category, order_type | - | unit_price, sale_price | mean | PASS |
| CP-3126 | sales_region, product_category, order_type | - | unit_price, sale_price | count | PASS |
| CP-3127 | sales_region, product_category, order_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-3128 | sales_region, product_category, order_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-3129 | sales_region, product_category, order_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-3130 | sales_region, product_category, customer_type | order_type | quantity | sum | PASS |
| CP-3131 | sales_region, product_category, customer_type | order_type | quantity | mean | PASS |
| CP-3132 | sales_region, product_category, customer_type | order_type | quantity | count | PASS |
| CP-3133 | sales_region, product_category, customer_type | order_type | unit_price | sum | PASS |
| CP-3134 | sales_region, product_category, customer_type | order_type | unit_price | mean | PASS |
| CP-3135 | sales_region, product_category, customer_type | order_type | unit_price | count | PASS |
| CP-3136 | sales_region, product_category, customer_type | order_type | quantity, unit_price | sum | PASS |
| CP-3137 | sales_region, product_category, customer_type | order_type | quantity, unit_price | mean | PASS |
| CP-3138 | sales_region, product_category, customer_type | order_type | quantity, unit_price | count | PASS |
| CP-3139 | sales_region, product_category, customer_type | order_type | sale_price | sum | PASS |
| CP-3140 | sales_region, product_category, customer_type | order_type | sale_price | mean | PASS |
| CP-3141 | sales_region, product_category, customer_type | order_type | sale_price | count | PASS |
| CP-3142 | sales_region, product_category, customer_type | order_type | quantity, sale_price | sum | PASS |
| CP-3143 | sales_region, product_category, customer_type | order_type | quantity, sale_price | mean | PASS |
| CP-3144 | sales_region, product_category, customer_type | order_type | quantity, sale_price | count | PASS |
| CP-3145 | sales_region, product_category, customer_type | order_type | unit_price, sale_price | sum | PASS |
| CP-3146 | sales_region, product_category, customer_type | order_type | unit_price, sale_price | mean | PASS |
| CP-3147 | sales_region, product_category, customer_type | order_type | unit_price, sale_price | count | PASS |
| CP-3148 | sales_region, product_category, customer_type | order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3149 | sales_region, product_category, customer_type | order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3150 | sales_region, product_category, customer_type | order_type | quantity, unit_price, sale_price | count | PASS |
| CP-3151 | sales_region, product_category | order_type, customer_type | quantity | sum | PASS |
| CP-3152 | sales_region, product_category | order_type, customer_type | quantity | mean | PASS |
| CP-3153 | sales_region, product_category | order_type, customer_type | quantity | count | PASS |
| CP-3154 | sales_region, product_category | order_type, customer_type | unit_price | sum | PASS |
| CP-3155 | sales_region, product_category | order_type, customer_type | unit_price | mean | PASS |
| CP-3156 | sales_region, product_category | order_type, customer_type | unit_price | count | PASS |
| CP-3157 | sales_region, product_category | order_type, customer_type | quantity, unit_price | sum | PASS |
| CP-3158 | sales_region, product_category | order_type, customer_type | quantity, unit_price | mean | PASS |
| CP-3159 | sales_region, product_category | order_type, customer_type | quantity, unit_price | count | PASS |
| CP-3160 | sales_region, product_category | order_type, customer_type | sale_price | sum | PASS |
| CP-3161 | sales_region, product_category | order_type, customer_type | sale_price | mean | PASS |
| CP-3162 | sales_region, product_category | order_type, customer_type | sale_price | count | PASS |
| CP-3163 | sales_region, product_category | order_type, customer_type | quantity, sale_price | sum | PASS |
| CP-3164 | sales_region, product_category | order_type, customer_type | quantity, sale_price | mean | PASS |
| CP-3165 | sales_region, product_category | order_type, customer_type | quantity, sale_price | count | PASS |
| CP-3166 | sales_region, product_category | order_type, customer_type | unit_price, sale_price | sum | PASS |
| CP-3167 | sales_region, product_category | order_type, customer_type | unit_price, sale_price | mean | PASS |
| CP-3168 | sales_region, product_category | order_type, customer_type | unit_price, sale_price | count | PASS |
| CP-3169 | sales_region, product_category | order_type, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3170 | sales_region, product_category | order_type, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3171 | sales_region, product_category | order_type, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-3172 | sales_region, product_category | order_type | quantity | sum | PASS |
| CP-3173 | sales_region, product_category | order_type | quantity | mean | PASS |
| CP-3174 | sales_region, product_category | order_type | quantity | count | PASS |
| CP-3175 | sales_region, product_category | order_type | unit_price | sum | PASS |
| CP-3176 | sales_region, product_category | order_type | unit_price | mean | PASS |
| CP-3177 | sales_region, product_category | order_type | unit_price | count | PASS |
| CP-3178 | sales_region, product_category | order_type | quantity, unit_price | sum | PASS |
| CP-3179 | sales_region, product_category | order_type | quantity, unit_price | mean | PASS |
| CP-3180 | sales_region, product_category | order_type | quantity, unit_price | count | PASS |
| CP-3181 | sales_region, product_category | order_type | sale_price | sum | PASS |
| CP-3182 | sales_region, product_category | order_type | sale_price | mean | PASS |
| CP-3183 | sales_region, product_category | order_type | sale_price | count | PASS |
| CP-3184 | sales_region, product_category | order_type | quantity, sale_price | sum | PASS |
| CP-3185 | sales_region, product_category | order_type | quantity, sale_price | mean | PASS |
| CP-3186 | sales_region, product_category | order_type | quantity, sale_price | count | PASS |
| CP-3187 | sales_region, product_category | order_type | unit_price, sale_price | sum | PASS |
| CP-3188 | sales_region, product_category | order_type | unit_price, sale_price | mean | PASS |
| CP-3189 | sales_region, product_category | order_type | unit_price, sale_price | count | PASS |
| CP-3190 | sales_region, product_category | order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3191 | sales_region, product_category | order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3192 | sales_region, product_category | order_type | quantity, unit_price, sale_price | count | PASS |
| CP-3193 | sales_region, product_category, customer_type | - | quantity | sum | PASS |
| CP-3194 | sales_region, product_category, customer_type | - | quantity | mean | PASS |
| CP-3195 | sales_region, product_category, customer_type | - | quantity | count | PASS |
| CP-3196 | sales_region, product_category, customer_type | - | unit_price | sum | PASS |
| CP-3197 | sales_region, product_category, customer_type | - | unit_price | mean | PASS |
| CP-3198 | sales_region, product_category, customer_type | - | unit_price | count | PASS |
| CP-3199 | sales_region, product_category, customer_type | - | quantity, unit_price | sum | PASS |
| CP-3200 | sales_region, product_category, customer_type | - | quantity, unit_price | mean | PASS |
| CP-3201 | sales_region, product_category, customer_type | - | quantity, unit_price | count | PASS |
| CP-3202 | sales_region, product_category, customer_type | - | sale_price | sum | PASS |
| CP-3203 | sales_region, product_category, customer_type | - | sale_price | mean | PASS |
| CP-3204 | sales_region, product_category, customer_type | - | sale_price | count | PASS |
| CP-3205 | sales_region, product_category, customer_type | - | quantity, sale_price | sum | PASS |
| CP-3206 | sales_region, product_category, customer_type | - | quantity, sale_price | mean | PASS |
| CP-3207 | sales_region, product_category, customer_type | - | quantity, sale_price | count | PASS |
| CP-3208 | sales_region, product_category, customer_type | - | unit_price, sale_price | sum | PASS |
| CP-3209 | sales_region, product_category, customer_type | - | unit_price, sale_price | mean | PASS |
| CP-3210 | sales_region, product_category, customer_type | - | unit_price, sale_price | count | PASS |
| CP-3211 | sales_region, product_category, customer_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-3212 | sales_region, product_category, customer_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-3213 | sales_region, product_category, customer_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-3214 | sales_region, product_category | customer_type | quantity | sum | PASS |
| CP-3215 | sales_region, product_category | customer_type | quantity | mean | PASS |
| CP-3216 | sales_region, product_category | customer_type | quantity | count | PASS |
| CP-3217 | sales_region, product_category | customer_type | unit_price | sum | PASS |
| CP-3218 | sales_region, product_category | customer_type | unit_price | mean | PASS |
| CP-3219 | sales_region, product_category | customer_type | unit_price | count | PASS |
| CP-3220 | sales_region, product_category | customer_type | quantity, unit_price | sum | PASS |
| CP-3221 | sales_region, product_category | customer_type | quantity, unit_price | mean | PASS |
| CP-3222 | sales_region, product_category | customer_type | quantity, unit_price | count | PASS |
| CP-3223 | sales_region, product_category | customer_type | sale_price | sum | PASS |
| CP-3224 | sales_region, product_category | customer_type | sale_price | mean | PASS |
| CP-3225 | sales_region, product_category | customer_type | sale_price | count | PASS |
| CP-3226 | sales_region, product_category | customer_type | quantity, sale_price | sum | PASS |
| CP-3227 | sales_region, product_category | customer_type | quantity, sale_price | mean | PASS |
| CP-3228 | sales_region, product_category | customer_type | quantity, sale_price | count | PASS |
| CP-3229 | sales_region, product_category | customer_type | unit_price, sale_price | sum | PASS |
| CP-3230 | sales_region, product_category | customer_type | unit_price, sale_price | mean | PASS |
| CP-3231 | sales_region, product_category | customer_type | unit_price, sale_price | count | PASS |
| CP-3232 | sales_region, product_category | customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3233 | sales_region, product_category | customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3234 | sales_region, product_category | customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-3235 | sales_region, product_category | - | quantity | sum | PASS |
| CP-3236 | sales_region, product_category | - | quantity | mean | PASS |
| CP-3237 | sales_region, product_category | - | quantity | count | PASS |
| CP-3238 | sales_region, product_category | - | unit_price | sum | PASS |
| CP-3239 | sales_region, product_category | - | unit_price | mean | PASS |
| CP-3240 | sales_region, product_category | - | unit_price | count | PASS |
| CP-3241 | sales_region, product_category | - | quantity, unit_price | sum | PASS |
| CP-3242 | sales_region, product_category | - | quantity, unit_price | mean | PASS |
| CP-3243 | sales_region, product_category | - | quantity, unit_price | count | PASS |
| CP-3244 | sales_region, product_category | - | sale_price | sum | PASS |
| CP-3245 | sales_region, product_category | - | sale_price | mean | PASS |
| CP-3246 | sales_region, product_category | - | sale_price | count | PASS |
| CP-3247 | sales_region, product_category | - | quantity, sale_price | sum | PASS |
| CP-3248 | sales_region, product_category | - | quantity, sale_price | mean | PASS |
| CP-3249 | sales_region, product_category | - | quantity, sale_price | count | PASS |
| CP-3250 | sales_region, product_category | - | unit_price, sale_price | sum | PASS |
| CP-3251 | sales_region, product_category | - | unit_price, sale_price | mean | PASS |
| CP-3252 | sales_region, product_category | - | unit_price, sale_price | count | PASS |
| CP-3253 | sales_region, product_category | - | quantity, unit_price, sale_price | sum | PASS |
| CP-3254 | sales_region, product_category | - | quantity, unit_price, sale_price | mean | PASS |
| CP-3255 | sales_region, product_category | - | quantity, unit_price, sale_price | count | PASS |
| CP-3256 | sales_region, order_type, customer_type | product_category | quantity | sum | PASS |
| CP-3257 | sales_region, order_type, customer_type | product_category | quantity | mean | PASS |
| CP-3258 | sales_region, order_type, customer_type | product_category | quantity | count | PASS |
| CP-3259 | sales_region, order_type, customer_type | product_category | unit_price | sum | PASS |
| CP-3260 | sales_region, order_type, customer_type | product_category | unit_price | mean | PASS |
| CP-3261 | sales_region, order_type, customer_type | product_category | unit_price | count | PASS |
| CP-3262 | sales_region, order_type, customer_type | product_category | quantity, unit_price | sum | PASS |
| CP-3263 | sales_region, order_type, customer_type | product_category | quantity, unit_price | mean | PASS |
| CP-3264 | sales_region, order_type, customer_type | product_category | quantity, unit_price | count | PASS |
| CP-3265 | sales_region, order_type, customer_type | product_category | sale_price | sum | PASS |
| CP-3266 | sales_region, order_type, customer_type | product_category | sale_price | mean | PASS |
| CP-3267 | sales_region, order_type, customer_type | product_category | sale_price | count | PASS |
| CP-3268 | sales_region, order_type, customer_type | product_category | quantity, sale_price | sum | PASS |
| CP-3269 | sales_region, order_type, customer_type | product_category | quantity, sale_price | mean | PASS |
| CP-3270 | sales_region, order_type, customer_type | product_category | quantity, sale_price | count | PASS |
| CP-3271 | sales_region, order_type, customer_type | product_category | unit_price, sale_price | sum | PASS |
| CP-3272 | sales_region, order_type, customer_type | product_category | unit_price, sale_price | mean | PASS |
| CP-3273 | sales_region, order_type, customer_type | product_category | unit_price, sale_price | count | PASS |
| CP-3274 | sales_region, order_type, customer_type | product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-3275 | sales_region, order_type, customer_type | product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-3276 | sales_region, order_type, customer_type | product_category | quantity, unit_price, sale_price | count | PASS |
| CP-3277 | sales_region, order_type | product_category, customer_type | quantity | sum | PASS |
| CP-3278 | sales_region, order_type | product_category, customer_type | quantity | mean | PASS |
| CP-3279 | sales_region, order_type | product_category, customer_type | quantity | count | PASS |
| CP-3280 | sales_region, order_type | product_category, customer_type | unit_price | sum | PASS |
| CP-3281 | sales_region, order_type | product_category, customer_type | unit_price | mean | PASS |
| CP-3282 | sales_region, order_type | product_category, customer_type | unit_price | count | PASS |
| CP-3283 | sales_region, order_type | product_category, customer_type | quantity, unit_price | sum | PASS |
| CP-3284 | sales_region, order_type | product_category, customer_type | quantity, unit_price | mean | PASS |
| CP-3285 | sales_region, order_type | product_category, customer_type | quantity, unit_price | count | PASS |
| CP-3286 | sales_region, order_type | product_category, customer_type | sale_price | sum | PASS |
| CP-3287 | sales_region, order_type | product_category, customer_type | sale_price | mean | PASS |
| CP-3288 | sales_region, order_type | product_category, customer_type | sale_price | count | PASS |
| CP-3289 | sales_region, order_type | product_category, customer_type | quantity, sale_price | sum | PASS |
| CP-3290 | sales_region, order_type | product_category, customer_type | quantity, sale_price | mean | PASS |
| CP-3291 | sales_region, order_type | product_category, customer_type | quantity, sale_price | count | PASS |
| CP-3292 | sales_region, order_type | product_category, customer_type | unit_price, sale_price | sum | PASS |
| CP-3293 | sales_region, order_type | product_category, customer_type | unit_price, sale_price | mean | PASS |
| CP-3294 | sales_region, order_type | product_category, customer_type | unit_price, sale_price | count | PASS |
| CP-3295 | sales_region, order_type | product_category, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3296 | sales_region, order_type | product_category, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3297 | sales_region, order_type | product_category, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-3298 | sales_region, order_type | product_category | quantity | sum | PASS |
| CP-3299 | sales_region, order_type | product_category | quantity | mean | PASS |
| CP-3300 | sales_region, order_type | product_category | quantity | count | PASS |
| CP-3301 | sales_region, order_type | product_category | unit_price | sum | PASS |
| CP-3302 | sales_region, order_type | product_category | unit_price | mean | PASS |
| CP-3303 | sales_region, order_type | product_category | unit_price | count | PASS |
| CP-3304 | sales_region, order_type | product_category | quantity, unit_price | sum | PASS |
| CP-3305 | sales_region, order_type | product_category | quantity, unit_price | mean | PASS |
| CP-3306 | sales_region, order_type | product_category | quantity, unit_price | count | PASS |
| CP-3307 | sales_region, order_type | product_category | sale_price | sum | PASS |
| CP-3308 | sales_region, order_type | product_category | sale_price | mean | PASS |
| CP-3309 | sales_region, order_type | product_category | sale_price | count | PASS |
| CP-3310 | sales_region, order_type | product_category | quantity, sale_price | sum | PASS |
| CP-3311 | sales_region, order_type | product_category | quantity, sale_price | mean | PASS |
| CP-3312 | sales_region, order_type | product_category | quantity, sale_price | count | PASS |
| CP-3313 | sales_region, order_type | product_category | unit_price, sale_price | sum | PASS |
| CP-3314 | sales_region, order_type | product_category | unit_price, sale_price | mean | PASS |
| CP-3315 | sales_region, order_type | product_category | unit_price, sale_price | count | PASS |
| CP-3316 | sales_region, order_type | product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-3317 | sales_region, order_type | product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-3318 | sales_region, order_type | product_category | quantity, unit_price, sale_price | count | PASS |
| CP-3319 | sales_region, customer_type | product_category, order_type | quantity | sum | PASS |
| CP-3320 | sales_region, customer_type | product_category, order_type | quantity | mean | PASS |
| CP-3321 | sales_region, customer_type | product_category, order_type | quantity | count | PASS |
| CP-3322 | sales_region, customer_type | product_category, order_type | unit_price | sum | PASS |
| CP-3323 | sales_region, customer_type | product_category, order_type | unit_price | mean | PASS |
| CP-3324 | sales_region, customer_type | product_category, order_type | unit_price | count | PASS |
| CP-3325 | sales_region, customer_type | product_category, order_type | quantity, unit_price | sum | PASS |
| CP-3326 | sales_region, customer_type | product_category, order_type | quantity, unit_price | mean | PASS |
| CP-3327 | sales_region, customer_type | product_category, order_type | quantity, unit_price | count | PASS |
| CP-3328 | sales_region, customer_type | product_category, order_type | sale_price | sum | PASS |
| CP-3329 | sales_region, customer_type | product_category, order_type | sale_price | mean | PASS |
| CP-3330 | sales_region, customer_type | product_category, order_type | sale_price | count | PASS |
| CP-3331 | sales_region, customer_type | product_category, order_type | quantity, sale_price | sum | PASS |
| CP-3332 | sales_region, customer_type | product_category, order_type | quantity, sale_price | mean | PASS |
| CP-3333 | sales_region, customer_type | product_category, order_type | quantity, sale_price | count | PASS |
| CP-3334 | sales_region, customer_type | product_category, order_type | unit_price, sale_price | sum | PASS |
| CP-3335 | sales_region, customer_type | product_category, order_type | unit_price, sale_price | mean | PASS |
| CP-3336 | sales_region, customer_type | product_category, order_type | unit_price, sale_price | count | PASS |
| CP-3337 | sales_region, customer_type | product_category, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3338 | sales_region, customer_type | product_category, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3339 | sales_region, customer_type | product_category, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-3340 | sales_region | product_category, order_type, customer_type | quantity | sum | PASS |
| CP-3341 | sales_region | product_category, order_type, customer_type | quantity | mean | PASS |
| CP-3342 | sales_region | product_category, order_type, customer_type | quantity | count | PASS |
| CP-3343 | sales_region | product_category, order_type, customer_type | unit_price | sum | PASS |
| CP-3344 | sales_region | product_category, order_type, customer_type | unit_price | mean | PASS |
| CP-3345 | sales_region | product_category, order_type, customer_type | unit_price | count | PASS |
| CP-3346 | sales_region | product_category, order_type, customer_type | quantity, unit_price | sum | PASS |
| CP-3347 | sales_region | product_category, order_type, customer_type | quantity, unit_price | mean | PASS |
| CP-3348 | sales_region | product_category, order_type, customer_type | quantity, unit_price | count | PASS |
| CP-3349 | sales_region | product_category, order_type, customer_type | sale_price | sum | PASS |
| CP-3350 | sales_region | product_category, order_type, customer_type | sale_price | mean | PASS |
| CP-3351 | sales_region | product_category, order_type, customer_type | sale_price | count | PASS |
| CP-3352 | sales_region | product_category, order_type, customer_type | quantity, sale_price | sum | PASS |
| CP-3353 | sales_region | product_category, order_type, customer_type | quantity, sale_price | mean | PASS |
| CP-3354 | sales_region | product_category, order_type, customer_type | quantity, sale_price | count | PASS |
| CP-3355 | sales_region | product_category, order_type, customer_type | unit_price, sale_price | sum | PASS |
| CP-3356 | sales_region | product_category, order_type, customer_type | unit_price, sale_price | mean | PASS |
| CP-3357 | sales_region | product_category, order_type, customer_type | unit_price, sale_price | count | PASS |
| CP-3358 | sales_region | product_category, order_type, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3359 | sales_region | product_category, order_type, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3360 | sales_region | product_category, order_type, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-3361 | sales_region | product_category, order_type | quantity | sum | PASS |
| CP-3362 | sales_region | product_category, order_type | quantity | mean | PASS |
| CP-3363 | sales_region | product_category, order_type | quantity | count | PASS |
| CP-3364 | sales_region | product_category, order_type | unit_price | sum | PASS |
| CP-3365 | sales_region | product_category, order_type | unit_price | mean | PASS |
| CP-3366 | sales_region | product_category, order_type | unit_price | count | PASS |
| CP-3367 | sales_region | product_category, order_type | quantity, unit_price | sum | PASS |
| CP-3368 | sales_region | product_category, order_type | quantity, unit_price | mean | PASS |
| CP-3369 | sales_region | product_category, order_type | quantity, unit_price | count | PASS |
| CP-3370 | sales_region | product_category, order_type | sale_price | sum | PASS |
| CP-3371 | sales_region | product_category, order_type | sale_price | mean | PASS |
| CP-3372 | sales_region | product_category, order_type | sale_price | count | PASS |
| CP-3373 | sales_region | product_category, order_type | quantity, sale_price | sum | PASS |
| CP-3374 | sales_region | product_category, order_type | quantity, sale_price | mean | PASS |
| CP-3375 | sales_region | product_category, order_type | quantity, sale_price | count | PASS |
| CP-3376 | sales_region | product_category, order_type | unit_price, sale_price | sum | PASS |
| CP-3377 | sales_region | product_category, order_type | unit_price, sale_price | mean | PASS |
| CP-3378 | sales_region | product_category, order_type | unit_price, sale_price | count | PASS |
| CP-3379 | sales_region | product_category, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3380 | sales_region | product_category, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3381 | sales_region | product_category, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-3382 | sales_region, customer_type | product_category | quantity | sum | PASS |
| CP-3383 | sales_region, customer_type | product_category | quantity | mean | PASS |
| CP-3384 | sales_region, customer_type | product_category | quantity | count | PASS |
| CP-3385 | sales_region, customer_type | product_category | unit_price | sum | PASS |
| CP-3386 | sales_region, customer_type | product_category | unit_price | mean | PASS |
| CP-3387 | sales_region, customer_type | product_category | unit_price | count | PASS |
| CP-3388 | sales_region, customer_type | product_category | quantity, unit_price | sum | PASS |
| CP-3389 | sales_region, customer_type | product_category | quantity, unit_price | mean | PASS |
| CP-3390 | sales_region, customer_type | product_category | quantity, unit_price | count | PASS |
| CP-3391 | sales_region, customer_type | product_category | sale_price | sum | PASS |
| CP-3392 | sales_region, customer_type | product_category | sale_price | mean | PASS |
| CP-3393 | sales_region, customer_type | product_category | sale_price | count | PASS |
| CP-3394 | sales_region, customer_type | product_category | quantity, sale_price | sum | PASS |
| CP-3395 | sales_region, customer_type | product_category | quantity, sale_price | mean | PASS |
| CP-3396 | sales_region, customer_type | product_category | quantity, sale_price | count | PASS |
| CP-3397 | sales_region, customer_type | product_category | unit_price, sale_price | sum | PASS |
| CP-3398 | sales_region, customer_type | product_category | unit_price, sale_price | mean | PASS |
| CP-3399 | sales_region, customer_type | product_category | unit_price, sale_price | count | PASS |
| CP-3400 | sales_region, customer_type | product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-3401 | sales_region, customer_type | product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-3402 | sales_region, customer_type | product_category | quantity, unit_price, sale_price | count | PASS |
| CP-3403 | sales_region | product_category, customer_type | quantity | sum | PASS |
| CP-3404 | sales_region | product_category, customer_type | quantity | mean | PASS |
| CP-3405 | sales_region | product_category, customer_type | quantity | count | PASS |
| CP-3406 | sales_region | product_category, customer_type | unit_price | sum | PASS |
| CP-3407 | sales_region | product_category, customer_type | unit_price | mean | PASS |
| CP-3408 | sales_region | product_category, customer_type | unit_price | count | PASS |
| CP-3409 | sales_region | product_category, customer_type | quantity, unit_price | sum | PASS |
| CP-3410 | sales_region | product_category, customer_type | quantity, unit_price | mean | PASS |
| CP-3411 | sales_region | product_category, customer_type | quantity, unit_price | count | PASS |
| CP-3412 | sales_region | product_category, customer_type | sale_price | sum | PASS |
| CP-3413 | sales_region | product_category, customer_type | sale_price | mean | PASS |
| CP-3414 | sales_region | product_category, customer_type | sale_price | count | PASS |
| CP-3415 | sales_region | product_category, customer_type | quantity, sale_price | sum | PASS |
| CP-3416 | sales_region | product_category, customer_type | quantity, sale_price | mean | PASS |
| CP-3417 | sales_region | product_category, customer_type | quantity, sale_price | count | PASS |
| CP-3418 | sales_region | product_category, customer_type | unit_price, sale_price | sum | PASS |
| CP-3419 | sales_region | product_category, customer_type | unit_price, sale_price | mean | PASS |
| CP-3420 | sales_region | product_category, customer_type | unit_price, sale_price | count | PASS |
| CP-3421 | sales_region | product_category, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3422 | sales_region | product_category, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3423 | sales_region | product_category, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-3424 | sales_region | product_category | quantity | sum | PASS |
| CP-3425 | sales_region | product_category | quantity | mean | PASS |
| CP-3426 | sales_region | product_category | quantity | count | PASS |
| CP-3427 | sales_region | product_category | unit_price | sum | PASS |
| CP-3428 | sales_region | product_category | unit_price | mean | PASS |
| CP-3429 | sales_region | product_category | unit_price | count | PASS |
| CP-3430 | sales_region | product_category | quantity, unit_price | sum | PASS |
| CP-3431 | sales_region | product_category | quantity, unit_price | mean | PASS |
| CP-3432 | sales_region | product_category | quantity, unit_price | count | PASS |
| CP-3433 | sales_region | product_category | sale_price | sum | PASS |
| CP-3434 | sales_region | product_category | sale_price | mean | PASS |
| CP-3435 | sales_region | product_category | sale_price | count | PASS |
| CP-3436 | sales_region | product_category | quantity, sale_price | sum | PASS |
| CP-3437 | sales_region | product_category | quantity, sale_price | mean | PASS |
| CP-3438 | sales_region | product_category | quantity, sale_price | count | PASS |
| CP-3439 | sales_region | product_category | unit_price, sale_price | sum | PASS |
| CP-3440 | sales_region | product_category | unit_price, sale_price | mean | PASS |
| CP-3441 | sales_region | product_category | unit_price, sale_price | count | PASS |
| CP-3442 | sales_region | product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-3443 | sales_region | product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-3444 | sales_region | product_category | quantity, unit_price, sale_price | count | PASS |
| CP-3445 | sales_region, order_type, customer_type | - | quantity | sum | PASS |
| CP-3446 | sales_region, order_type, customer_type | - | quantity | mean | PASS |
| CP-3447 | sales_region, order_type, customer_type | - | quantity | count | PASS |
| CP-3448 | sales_region, order_type, customer_type | - | unit_price | sum | PASS |
| CP-3449 | sales_region, order_type, customer_type | - | unit_price | mean | PASS |
| CP-3450 | sales_region, order_type, customer_type | - | unit_price | count | PASS |
| CP-3451 | sales_region, order_type, customer_type | - | quantity, unit_price | sum | PASS |
| CP-3452 | sales_region, order_type, customer_type | - | quantity, unit_price | mean | PASS |
| CP-3453 | sales_region, order_type, customer_type | - | quantity, unit_price | count | PASS |
| CP-3454 | sales_region, order_type, customer_type | - | sale_price | sum | PASS |
| CP-3455 | sales_region, order_type, customer_type | - | sale_price | mean | PASS |
| CP-3456 | sales_region, order_type, customer_type | - | sale_price | count | PASS |
| CP-3457 | sales_region, order_type, customer_type | - | quantity, sale_price | sum | PASS |
| CP-3458 | sales_region, order_type, customer_type | - | quantity, sale_price | mean | PASS |
| CP-3459 | sales_region, order_type, customer_type | - | quantity, sale_price | count | PASS |
| CP-3460 | sales_region, order_type, customer_type | - | unit_price, sale_price | sum | PASS |
| CP-3461 | sales_region, order_type, customer_type | - | unit_price, sale_price | mean | PASS |
| CP-3462 | sales_region, order_type, customer_type | - | unit_price, sale_price | count | PASS |
| CP-3463 | sales_region, order_type, customer_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-3464 | sales_region, order_type, customer_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-3465 | sales_region, order_type, customer_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-3466 | sales_region, order_type | customer_type | quantity | sum | PASS |
| CP-3467 | sales_region, order_type | customer_type | quantity | mean | PASS |
| CP-3468 | sales_region, order_type | customer_type | quantity | count | PASS |
| CP-3469 | sales_region, order_type | customer_type | unit_price | sum | PASS |
| CP-3470 | sales_region, order_type | customer_type | unit_price | mean | PASS |
| CP-3471 | sales_region, order_type | customer_type | unit_price | count | PASS |
| CP-3472 | sales_region, order_type | customer_type | quantity, unit_price | sum | PASS |
| CP-3473 | sales_region, order_type | customer_type | quantity, unit_price | mean | PASS |
| CP-3474 | sales_region, order_type | customer_type | quantity, unit_price | count | PASS |
| CP-3475 | sales_region, order_type | customer_type | sale_price | sum | PASS |
| CP-3476 | sales_region, order_type | customer_type | sale_price | mean | PASS |
| CP-3477 | sales_region, order_type | customer_type | sale_price | count | PASS |
| CP-3478 | sales_region, order_type | customer_type | quantity, sale_price | sum | PASS |
| CP-3479 | sales_region, order_type | customer_type | quantity, sale_price | mean | PASS |
| CP-3480 | sales_region, order_type | customer_type | quantity, sale_price | count | PASS |
| CP-3481 | sales_region, order_type | customer_type | unit_price, sale_price | sum | PASS |
| CP-3482 | sales_region, order_type | customer_type | unit_price, sale_price | mean | PASS |
| CP-3483 | sales_region, order_type | customer_type | unit_price, sale_price | count | PASS |
| CP-3484 | sales_region, order_type | customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3485 | sales_region, order_type | customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3486 | sales_region, order_type | customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-3487 | sales_region, order_type | - | quantity | sum | PASS |
| CP-3488 | sales_region, order_type | - | quantity | mean | PASS |
| CP-3489 | sales_region, order_type | - | quantity | count | PASS |
| CP-3490 | sales_region, order_type | - | unit_price | sum | PASS |
| CP-3491 | sales_region, order_type | - | unit_price | mean | PASS |
| CP-3492 | sales_region, order_type | - | unit_price | count | PASS |
| CP-3493 | sales_region, order_type | - | quantity, unit_price | sum | PASS |
| CP-3494 | sales_region, order_type | - | quantity, unit_price | mean | PASS |
| CP-3495 | sales_region, order_type | - | quantity, unit_price | count | PASS |
| CP-3496 | sales_region, order_type | - | sale_price | sum | PASS |
| CP-3497 | sales_region, order_type | - | sale_price | mean | PASS |
| CP-3498 | sales_region, order_type | - | sale_price | count | PASS |
| CP-3499 | sales_region, order_type | - | quantity, sale_price | sum | PASS |
| CP-3500 | sales_region, order_type | - | quantity, sale_price | mean | PASS |
| CP-3501 | sales_region, order_type | - | quantity, sale_price | count | PASS |
| CP-3502 | sales_region, order_type | - | unit_price, sale_price | sum | PASS |
| CP-3503 | sales_region, order_type | - | unit_price, sale_price | mean | PASS |
| CP-3504 | sales_region, order_type | - | unit_price, sale_price | count | PASS |
| CP-3505 | sales_region, order_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-3506 | sales_region, order_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-3507 | sales_region, order_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-3508 | sales_region, customer_type | order_type | quantity | sum | PASS |
| CP-3509 | sales_region, customer_type | order_type | quantity | mean | PASS |
| CP-3510 | sales_region, customer_type | order_type | quantity | count | PASS |
| CP-3511 | sales_region, customer_type | order_type | unit_price | sum | PASS |
| CP-3512 | sales_region, customer_type | order_type | unit_price | mean | PASS |
| CP-3513 | sales_region, customer_type | order_type | unit_price | count | PASS |
| CP-3514 | sales_region, customer_type | order_type | quantity, unit_price | sum | PASS |
| CP-3515 | sales_region, customer_type | order_type | quantity, unit_price | mean | PASS |
| CP-3516 | sales_region, customer_type | order_type | quantity, unit_price | count | PASS |
| CP-3517 | sales_region, customer_type | order_type | sale_price | sum | PASS |
| CP-3518 | sales_region, customer_type | order_type | sale_price | mean | PASS |
| CP-3519 | sales_region, customer_type | order_type | sale_price | count | PASS |
| CP-3520 | sales_region, customer_type | order_type | quantity, sale_price | sum | PASS |
| CP-3521 | sales_region, customer_type | order_type | quantity, sale_price | mean | PASS |
| CP-3522 | sales_region, customer_type | order_type | quantity, sale_price | count | PASS |
| CP-3523 | sales_region, customer_type | order_type | unit_price, sale_price | sum | PASS |
| CP-3524 | sales_region, customer_type | order_type | unit_price, sale_price | mean | PASS |
| CP-3525 | sales_region, customer_type | order_type | unit_price, sale_price | count | PASS |
| CP-3526 | sales_region, customer_type | order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3527 | sales_region, customer_type | order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3528 | sales_region, customer_type | order_type | quantity, unit_price, sale_price | count | PASS |
| CP-3529 | sales_region | order_type, customer_type | quantity | sum | PASS |
| CP-3530 | sales_region | order_type, customer_type | quantity | mean | PASS |
| CP-3531 | sales_region | order_type, customer_type | quantity | count | PASS |
| CP-3532 | sales_region | order_type, customer_type | unit_price | sum | PASS |
| CP-3533 | sales_region | order_type, customer_type | unit_price | mean | PASS |
| CP-3534 | sales_region | order_type, customer_type | unit_price | count | PASS |
| CP-3535 | sales_region | order_type, customer_type | quantity, unit_price | sum | PASS |
| CP-3536 | sales_region | order_type, customer_type | quantity, unit_price | mean | PASS |
| CP-3537 | sales_region | order_type, customer_type | quantity, unit_price | count | PASS |
| CP-3538 | sales_region | order_type, customer_type | sale_price | sum | PASS |
| CP-3539 | sales_region | order_type, customer_type | sale_price | mean | PASS |
| CP-3540 | sales_region | order_type, customer_type | sale_price | count | PASS |
| CP-3541 | sales_region | order_type, customer_type | quantity, sale_price | sum | PASS |
| CP-3542 | sales_region | order_type, customer_type | quantity, sale_price | mean | PASS |
| CP-3543 | sales_region | order_type, customer_type | quantity, sale_price | count | PASS |
| CP-3544 | sales_region | order_type, customer_type | unit_price, sale_price | sum | PASS |
| CP-3545 | sales_region | order_type, customer_type | unit_price, sale_price | mean | PASS |
| CP-3546 | sales_region | order_type, customer_type | unit_price, sale_price | count | PASS |
| CP-3547 | sales_region | order_type, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3548 | sales_region | order_type, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3549 | sales_region | order_type, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-3550 | sales_region | order_type | quantity | sum | PASS |
| CP-3551 | sales_region | order_type | quantity | mean | PASS |
| CP-3552 | sales_region | order_type | quantity | count | PASS |
| CP-3553 | sales_region | order_type | unit_price | sum | PASS |
| CP-3554 | sales_region | order_type | unit_price | mean | PASS |
| CP-3555 | sales_region | order_type | unit_price | count | PASS |
| CP-3556 | sales_region | order_type | quantity, unit_price | sum | PASS |
| CP-3557 | sales_region | order_type | quantity, unit_price | mean | PASS |
| CP-3558 | sales_region | order_type | quantity, unit_price | count | PASS |
| CP-3559 | sales_region | order_type | sale_price | sum | PASS |
| CP-3560 | sales_region | order_type | sale_price | mean | PASS |
| CP-3561 | sales_region | order_type | sale_price | count | PASS |
| CP-3562 | sales_region | order_type | quantity, sale_price | sum | PASS |
| CP-3563 | sales_region | order_type | quantity, sale_price | mean | PASS |
| CP-3564 | sales_region | order_type | quantity, sale_price | count | PASS |
| CP-3565 | sales_region | order_type | unit_price, sale_price | sum | PASS |
| CP-3566 | sales_region | order_type | unit_price, sale_price | mean | PASS |
| CP-3567 | sales_region | order_type | unit_price, sale_price | count | PASS |
| CP-3568 | sales_region | order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3569 | sales_region | order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3570 | sales_region | order_type | quantity, unit_price, sale_price | count | PASS |
| CP-3571 | sales_region, customer_type | - | quantity | sum | PASS |
| CP-3572 | sales_region, customer_type | - | quantity | mean | PASS |
| CP-3573 | sales_region, customer_type | - | quantity | count | PASS |
| CP-3574 | sales_region, customer_type | - | unit_price | sum | PASS |
| CP-3575 | sales_region, customer_type | - | unit_price | mean | PASS |
| CP-3576 | sales_region, customer_type | - | unit_price | count | PASS |
| CP-3577 | sales_region, customer_type | - | quantity, unit_price | sum | PASS |
| CP-3578 | sales_region, customer_type | - | quantity, unit_price | mean | PASS |
| CP-3579 | sales_region, customer_type | - | quantity, unit_price | count | PASS |
| CP-3580 | sales_region, customer_type | - | sale_price | sum | PASS |
| CP-3581 | sales_region, customer_type | - | sale_price | mean | PASS |
| CP-3582 | sales_region, customer_type | - | sale_price | count | PASS |
| CP-3583 | sales_region, customer_type | - | quantity, sale_price | sum | PASS |
| CP-3584 | sales_region, customer_type | - | quantity, sale_price | mean | PASS |
| CP-3585 | sales_region, customer_type | - | quantity, sale_price | count | PASS |
| CP-3586 | sales_region, customer_type | - | unit_price, sale_price | sum | PASS |
| CP-3587 | sales_region, customer_type | - | unit_price, sale_price | mean | PASS |
| CP-3588 | sales_region, customer_type | - | unit_price, sale_price | count | PASS |
| CP-3589 | sales_region, customer_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-3590 | sales_region, customer_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-3591 | sales_region, customer_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-3592 | sales_region | customer_type | quantity | sum | PASS |
| CP-3593 | sales_region | customer_type | quantity | mean | PASS |
| CP-3594 | sales_region | customer_type | quantity | count | PASS |
| CP-3595 | sales_region | customer_type | unit_price | sum | PASS |
| CP-3596 | sales_region | customer_type | unit_price | mean | PASS |
| CP-3597 | sales_region | customer_type | unit_price | count | PASS |
| CP-3598 | sales_region | customer_type | quantity, unit_price | sum | PASS |
| CP-3599 | sales_region | customer_type | quantity, unit_price | mean | PASS |
| CP-3600 | sales_region | customer_type | quantity, unit_price | count | PASS |
| CP-3601 | sales_region | customer_type | sale_price | sum | PASS |
| CP-3602 | sales_region | customer_type | sale_price | mean | PASS |
| CP-3603 | sales_region | customer_type | sale_price | count | PASS |
| CP-3604 | sales_region | customer_type | quantity, sale_price | sum | PASS |
| CP-3605 | sales_region | customer_type | quantity, sale_price | mean | PASS |
| CP-3606 | sales_region | customer_type | quantity, sale_price | count | PASS |
| CP-3607 | sales_region | customer_type | unit_price, sale_price | sum | PASS |
| CP-3608 | sales_region | customer_type | unit_price, sale_price | mean | PASS |
| CP-3609 | sales_region | customer_type | unit_price, sale_price | count | PASS |
| CP-3610 | sales_region | customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3611 | sales_region | customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3612 | sales_region | customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-3613 | sales_region | - | quantity | sum | PASS |
| CP-3614 | sales_region | - | quantity | mean | PASS |
| CP-3615 | sales_region | - | quantity | count | PASS |
| CP-3616 | sales_region | - | unit_price | sum | PASS |
| CP-3617 | sales_region | - | unit_price | mean | PASS |
| CP-3618 | sales_region | - | unit_price | count | PASS |
| CP-3619 | sales_region | - | quantity, unit_price | sum | PASS |
| CP-3620 | sales_region | - | quantity, unit_price | mean | PASS |
| CP-3621 | sales_region | - | quantity, unit_price | count | PASS |
| CP-3622 | sales_region | - | sale_price | sum | PASS |
| CP-3623 | sales_region | - | sale_price | mean | PASS |
| CP-3624 | sales_region | - | sale_price | count | PASS |
| CP-3625 | sales_region | - | quantity, sale_price | sum | PASS |
| CP-3626 | sales_region | - | quantity, sale_price | mean | PASS |
| CP-3627 | sales_region | - | quantity, sale_price | count | PASS |
| CP-3628 | sales_region | - | unit_price, sale_price | sum | PASS |
| CP-3629 | sales_region | - | unit_price, sale_price | mean | PASS |
| CP-3630 | sales_region | - | unit_price, sale_price | count | PASS |
| CP-3631 | sales_region | - | quantity, unit_price, sale_price | sum | PASS |
| CP-3632 | sales_region | - | quantity, unit_price, sale_price | mean | PASS |
| CP-3633 | sales_region | - | quantity, unit_price, sale_price | count | PASS |
| CP-3634 | product_category, order_type, customer_type | sales_region | quantity | sum | PASS |
| CP-3635 | product_category, order_type, customer_type | sales_region | quantity | mean | PASS |
| CP-3636 | product_category, order_type, customer_type | sales_region | quantity | count | PASS |
| CP-3637 | product_category, order_type, customer_type | sales_region | unit_price | sum | PASS |
| CP-3638 | product_category, order_type, customer_type | sales_region | unit_price | mean | PASS |
| CP-3639 | product_category, order_type, customer_type | sales_region | unit_price | count | PASS |
| CP-3640 | product_category, order_type, customer_type | sales_region | quantity, unit_price | sum | PASS |
| CP-3641 | product_category, order_type, customer_type | sales_region | quantity, unit_price | mean | PASS |
| CP-3642 | product_category, order_type, customer_type | sales_region | quantity, unit_price | count | PASS |
| CP-3643 | product_category, order_type, customer_type | sales_region | sale_price | sum | PASS |
| CP-3644 | product_category, order_type, customer_type | sales_region | sale_price | mean | PASS |
| CP-3645 | product_category, order_type, customer_type | sales_region | sale_price | count | PASS |
| CP-3646 | product_category, order_type, customer_type | sales_region | quantity, sale_price | sum | PASS |
| CP-3647 | product_category, order_type, customer_type | sales_region | quantity, sale_price | mean | PASS |
| CP-3648 | product_category, order_type, customer_type | sales_region | quantity, sale_price | count | PASS |
| CP-3649 | product_category, order_type, customer_type | sales_region | unit_price, sale_price | sum | PASS |
| CP-3650 | product_category, order_type, customer_type | sales_region | unit_price, sale_price | mean | PASS |
| CP-3651 | product_category, order_type, customer_type | sales_region | unit_price, sale_price | count | PASS |
| CP-3652 | product_category, order_type, customer_type | sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-3653 | product_category, order_type, customer_type | sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-3654 | product_category, order_type, customer_type | sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-3655 | product_category, order_type | sales_region, customer_type | quantity | sum | PASS |
| CP-3656 | product_category, order_type | sales_region, customer_type | quantity | mean | PASS |
| CP-3657 | product_category, order_type | sales_region, customer_type | quantity | count | PASS |
| CP-3658 | product_category, order_type | sales_region, customer_type | unit_price | sum | PASS |
| CP-3659 | product_category, order_type | sales_region, customer_type | unit_price | mean | PASS |
| CP-3660 | product_category, order_type | sales_region, customer_type | unit_price | count | PASS |
| CP-3661 | product_category, order_type | sales_region, customer_type | quantity, unit_price | sum | PASS |
| CP-3662 | product_category, order_type | sales_region, customer_type | quantity, unit_price | mean | PASS |
| CP-3663 | product_category, order_type | sales_region, customer_type | quantity, unit_price | count | PASS |
| CP-3664 | product_category, order_type | sales_region, customer_type | sale_price | sum | PASS |
| CP-3665 | product_category, order_type | sales_region, customer_type | sale_price | mean | PASS |
| CP-3666 | product_category, order_type | sales_region, customer_type | sale_price | count | PASS |
| CP-3667 | product_category, order_type | sales_region, customer_type | quantity, sale_price | sum | PASS |
| CP-3668 | product_category, order_type | sales_region, customer_type | quantity, sale_price | mean | PASS |
| CP-3669 | product_category, order_type | sales_region, customer_type | quantity, sale_price | count | PASS |
| CP-3670 | product_category, order_type | sales_region, customer_type | unit_price, sale_price | sum | PASS |
| CP-3671 | product_category, order_type | sales_region, customer_type | unit_price, sale_price | mean | PASS |
| CP-3672 | product_category, order_type | sales_region, customer_type | unit_price, sale_price | count | PASS |
| CP-3673 | product_category, order_type | sales_region, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3674 | product_category, order_type | sales_region, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3675 | product_category, order_type | sales_region, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-3676 | product_category, order_type | sales_region | quantity | sum | PASS |
| CP-3677 | product_category, order_type | sales_region | quantity | mean | PASS |
| CP-3678 | product_category, order_type | sales_region | quantity | count | PASS |
| CP-3679 | product_category, order_type | sales_region | unit_price | sum | PASS |
| CP-3680 | product_category, order_type | sales_region | unit_price | mean | PASS |
| CP-3681 | product_category, order_type | sales_region | unit_price | count | PASS |
| CP-3682 | product_category, order_type | sales_region | quantity, unit_price | sum | PASS |
| CP-3683 | product_category, order_type | sales_region | quantity, unit_price | mean | PASS |
| CP-3684 | product_category, order_type | sales_region | quantity, unit_price | count | PASS |
| CP-3685 | product_category, order_type | sales_region | sale_price | sum | PASS |
| CP-3686 | product_category, order_type | sales_region | sale_price | mean | PASS |
| CP-3687 | product_category, order_type | sales_region | sale_price | count | PASS |
| CP-3688 | product_category, order_type | sales_region | quantity, sale_price | sum | PASS |
| CP-3689 | product_category, order_type | sales_region | quantity, sale_price | mean | PASS |
| CP-3690 | product_category, order_type | sales_region | quantity, sale_price | count | PASS |
| CP-3691 | product_category, order_type | sales_region | unit_price, sale_price | sum | PASS |
| CP-3692 | product_category, order_type | sales_region | unit_price, sale_price | mean | PASS |
| CP-3693 | product_category, order_type | sales_region | unit_price, sale_price | count | PASS |
| CP-3694 | product_category, order_type | sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-3695 | product_category, order_type | sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-3696 | product_category, order_type | sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-3697 | product_category, customer_type | sales_region, order_type | quantity | sum | PASS |
| CP-3698 | product_category, customer_type | sales_region, order_type | quantity | mean | PASS |
| CP-3699 | product_category, customer_type | sales_region, order_type | quantity | count | PASS |
| CP-3700 | product_category, customer_type | sales_region, order_type | unit_price | sum | PASS |
| CP-3701 | product_category, customer_type | sales_region, order_type | unit_price | mean | PASS |
| CP-3702 | product_category, customer_type | sales_region, order_type | unit_price | count | PASS |
| CP-3703 | product_category, customer_type | sales_region, order_type | quantity, unit_price | sum | PASS |
| CP-3704 | product_category, customer_type | sales_region, order_type | quantity, unit_price | mean | PASS |
| CP-3705 | product_category, customer_type | sales_region, order_type | quantity, unit_price | count | PASS |
| CP-3706 | product_category, customer_type | sales_region, order_type | sale_price | sum | PASS |
| CP-3707 | product_category, customer_type | sales_region, order_type | sale_price | mean | PASS |
| CP-3708 | product_category, customer_type | sales_region, order_type | sale_price | count | PASS |
| CP-3709 | product_category, customer_type | sales_region, order_type | quantity, sale_price | sum | PASS |
| CP-3710 | product_category, customer_type | sales_region, order_type | quantity, sale_price | mean | PASS |
| CP-3711 | product_category, customer_type | sales_region, order_type | quantity, sale_price | count | PASS |
| CP-3712 | product_category, customer_type | sales_region, order_type | unit_price, sale_price | sum | PASS |
| CP-3713 | product_category, customer_type | sales_region, order_type | unit_price, sale_price | mean | PASS |
| CP-3714 | product_category, customer_type | sales_region, order_type | unit_price, sale_price | count | PASS |
| CP-3715 | product_category, customer_type | sales_region, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3716 | product_category, customer_type | sales_region, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3717 | product_category, customer_type | sales_region, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-3718 | product_category | sales_region, order_type, customer_type | quantity | sum | PASS |
| CP-3719 | product_category | sales_region, order_type, customer_type | quantity | mean | PASS |
| CP-3720 | product_category | sales_region, order_type, customer_type | quantity | count | PASS |
| CP-3721 | product_category | sales_region, order_type, customer_type | unit_price | sum | PASS |
| CP-3722 | product_category | sales_region, order_type, customer_type | unit_price | mean | PASS |
| CP-3723 | product_category | sales_region, order_type, customer_type | unit_price | count | PASS |
| CP-3724 | product_category | sales_region, order_type, customer_type | quantity, unit_price | sum | PASS |
| CP-3725 | product_category | sales_region, order_type, customer_type | quantity, unit_price | mean | PASS |
| CP-3726 | product_category | sales_region, order_type, customer_type | quantity, unit_price | count | PASS |
| CP-3727 | product_category | sales_region, order_type, customer_type | sale_price | sum | PASS |
| CP-3728 | product_category | sales_region, order_type, customer_type | sale_price | mean | PASS |
| CP-3729 | product_category | sales_region, order_type, customer_type | sale_price | count | PASS |
| CP-3730 | product_category | sales_region, order_type, customer_type | quantity, sale_price | sum | PASS |
| CP-3731 | product_category | sales_region, order_type, customer_type | quantity, sale_price | mean | PASS |
| CP-3732 | product_category | sales_region, order_type, customer_type | quantity, sale_price | count | PASS |
| CP-3733 | product_category | sales_region, order_type, customer_type | unit_price, sale_price | sum | PASS |
| CP-3734 | product_category | sales_region, order_type, customer_type | unit_price, sale_price | mean | PASS |
| CP-3735 | product_category | sales_region, order_type, customer_type | unit_price, sale_price | count | PASS |
| CP-3736 | product_category | sales_region, order_type, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3737 | product_category | sales_region, order_type, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3738 | product_category | sales_region, order_type, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-3739 | product_category | sales_region, order_type | quantity | sum | PASS |
| CP-3740 | product_category | sales_region, order_type | quantity | mean | PASS |
| CP-3741 | product_category | sales_region, order_type | quantity | count | PASS |
| CP-3742 | product_category | sales_region, order_type | unit_price | sum | PASS |
| CP-3743 | product_category | sales_region, order_type | unit_price | mean | PASS |
| CP-3744 | product_category | sales_region, order_type | unit_price | count | PASS |
| CP-3745 | product_category | sales_region, order_type | quantity, unit_price | sum | PASS |
| CP-3746 | product_category | sales_region, order_type | quantity, unit_price | mean | PASS |
| CP-3747 | product_category | sales_region, order_type | quantity, unit_price | count | PASS |
| CP-3748 | product_category | sales_region, order_type | sale_price | sum | PASS |
| CP-3749 | product_category | sales_region, order_type | sale_price | mean | PASS |
| CP-3750 | product_category | sales_region, order_type | sale_price | count | PASS |
| CP-3751 | product_category | sales_region, order_type | quantity, sale_price | sum | PASS |
| CP-3752 | product_category | sales_region, order_type | quantity, sale_price | mean | PASS |
| CP-3753 | product_category | sales_region, order_type | quantity, sale_price | count | PASS |
| CP-3754 | product_category | sales_region, order_type | unit_price, sale_price | sum | PASS |
| CP-3755 | product_category | sales_region, order_type | unit_price, sale_price | mean | PASS |
| CP-3756 | product_category | sales_region, order_type | unit_price, sale_price | count | PASS |
| CP-3757 | product_category | sales_region, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3758 | product_category | sales_region, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3759 | product_category | sales_region, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-3760 | product_category, customer_type | sales_region | quantity | sum | PASS |
| CP-3761 | product_category, customer_type | sales_region | quantity | mean | PASS |
| CP-3762 | product_category, customer_type | sales_region | quantity | count | PASS |
| CP-3763 | product_category, customer_type | sales_region | unit_price | sum | PASS |
| CP-3764 | product_category, customer_type | sales_region | unit_price | mean | PASS |
| CP-3765 | product_category, customer_type | sales_region | unit_price | count | PASS |
| CP-3766 | product_category, customer_type | sales_region | quantity, unit_price | sum | PASS |
| CP-3767 | product_category, customer_type | sales_region | quantity, unit_price | mean | PASS |
| CP-3768 | product_category, customer_type | sales_region | quantity, unit_price | count | PASS |
| CP-3769 | product_category, customer_type | sales_region | sale_price | sum | PASS |
| CP-3770 | product_category, customer_type | sales_region | sale_price | mean | PASS |
| CP-3771 | product_category, customer_type | sales_region | sale_price | count | PASS |
| CP-3772 | product_category, customer_type | sales_region | quantity, sale_price | sum | PASS |
| CP-3773 | product_category, customer_type | sales_region | quantity, sale_price | mean | PASS |
| CP-3774 | product_category, customer_type | sales_region | quantity, sale_price | count | PASS |
| CP-3775 | product_category, customer_type | sales_region | unit_price, sale_price | sum | PASS |
| CP-3776 | product_category, customer_type | sales_region | unit_price, sale_price | mean | PASS |
| CP-3777 | product_category, customer_type | sales_region | unit_price, sale_price | count | PASS |
| CP-3778 | product_category, customer_type | sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-3779 | product_category, customer_type | sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-3780 | product_category, customer_type | sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-3781 | product_category | sales_region, customer_type | quantity | sum | PASS |
| CP-3782 | product_category | sales_region, customer_type | quantity | mean | PASS |
| CP-3783 | product_category | sales_region, customer_type | quantity | count | PASS |
| CP-3784 | product_category | sales_region, customer_type | unit_price | sum | PASS |
| CP-3785 | product_category | sales_region, customer_type | unit_price | mean | PASS |
| CP-3786 | product_category | sales_region, customer_type | unit_price | count | PASS |
| CP-3787 | product_category | sales_region, customer_type | quantity, unit_price | sum | PASS |
| CP-3788 | product_category | sales_region, customer_type | quantity, unit_price | mean | PASS |
| CP-3789 | product_category | sales_region, customer_type | quantity, unit_price | count | PASS |
| CP-3790 | product_category | sales_region, customer_type | sale_price | sum | PASS |
| CP-3791 | product_category | sales_region, customer_type | sale_price | mean | PASS |
| CP-3792 | product_category | sales_region, customer_type | sale_price | count | PASS |
| CP-3793 | product_category | sales_region, customer_type | quantity, sale_price | sum | PASS |
| CP-3794 | product_category | sales_region, customer_type | quantity, sale_price | mean | PASS |
| CP-3795 | product_category | sales_region, customer_type | quantity, sale_price | count | PASS |
| CP-3796 | product_category | sales_region, customer_type | unit_price, sale_price | sum | PASS |
| CP-3797 | product_category | sales_region, customer_type | unit_price, sale_price | mean | PASS |
| CP-3798 | product_category | sales_region, customer_type | unit_price, sale_price | count | PASS |
| CP-3799 | product_category | sales_region, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3800 | product_category | sales_region, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3801 | product_category | sales_region, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-3802 | product_category | sales_region | quantity | sum | PASS |
| CP-3803 | product_category | sales_region | quantity | mean | PASS |
| CP-3804 | product_category | sales_region | quantity | count | PASS |
| CP-3805 | product_category | sales_region | unit_price | sum | PASS |
| CP-3806 | product_category | sales_region | unit_price | mean | PASS |
| CP-3807 | product_category | sales_region | unit_price | count | PASS |
| CP-3808 | product_category | sales_region | quantity, unit_price | sum | PASS |
| CP-3809 | product_category | sales_region | quantity, unit_price | mean | PASS |
| CP-3810 | product_category | sales_region | quantity, unit_price | count | PASS |
| CP-3811 | product_category | sales_region | sale_price | sum | PASS |
| CP-3812 | product_category | sales_region | sale_price | mean | PASS |
| CP-3813 | product_category | sales_region | sale_price | count | PASS |
| CP-3814 | product_category | sales_region | quantity, sale_price | sum | PASS |
| CP-3815 | product_category | sales_region | quantity, sale_price | mean | PASS |
| CP-3816 | product_category | sales_region | quantity, sale_price | count | PASS |
| CP-3817 | product_category | sales_region | unit_price, sale_price | sum | PASS |
| CP-3818 | product_category | sales_region | unit_price, sale_price | mean | PASS |
| CP-3819 | product_category | sales_region | unit_price, sale_price | count | PASS |
| CP-3820 | product_category | sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-3821 | product_category | sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-3822 | product_category | sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-3823 | order_type, customer_type | sales_region, product_category | quantity | sum | PASS |
| CP-3824 | order_type, customer_type | sales_region, product_category | quantity | mean | PASS |
| CP-3825 | order_type, customer_type | sales_region, product_category | quantity | count | PASS |
| CP-3826 | order_type, customer_type | sales_region, product_category | unit_price | sum | PASS |
| CP-3827 | order_type, customer_type | sales_region, product_category | unit_price | mean | PASS |
| CP-3828 | order_type, customer_type | sales_region, product_category | unit_price | count | PASS |
| CP-3829 | order_type, customer_type | sales_region, product_category | quantity, unit_price | sum | PASS |
| CP-3830 | order_type, customer_type | sales_region, product_category | quantity, unit_price | mean | PASS |
| CP-3831 | order_type, customer_type | sales_region, product_category | quantity, unit_price | count | PASS |
| CP-3832 | order_type, customer_type | sales_region, product_category | sale_price | sum | PASS |
| CP-3833 | order_type, customer_type | sales_region, product_category | sale_price | mean | PASS |
| CP-3834 | order_type, customer_type | sales_region, product_category | sale_price | count | PASS |
| CP-3835 | order_type, customer_type | sales_region, product_category | quantity, sale_price | sum | PASS |
| CP-3836 | order_type, customer_type | sales_region, product_category | quantity, sale_price | mean | PASS |
| CP-3837 | order_type, customer_type | sales_region, product_category | quantity, sale_price | count | PASS |
| CP-3838 | order_type, customer_type | sales_region, product_category | unit_price, sale_price | sum | PASS |
| CP-3839 | order_type, customer_type | sales_region, product_category | unit_price, sale_price | mean | PASS |
| CP-3840 | order_type, customer_type | sales_region, product_category | unit_price, sale_price | count | PASS |
| CP-3841 | order_type, customer_type | sales_region, product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-3842 | order_type, customer_type | sales_region, product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-3843 | order_type, customer_type | sales_region, product_category | quantity, unit_price, sale_price | count | PASS |
| CP-3844 | order_type | sales_region, product_category, customer_type | quantity | sum | PASS |
| CP-3845 | order_type | sales_region, product_category, customer_type | quantity | mean | PASS |
| CP-3846 | order_type | sales_region, product_category, customer_type | quantity | count | PASS |
| CP-3847 | order_type | sales_region, product_category, customer_type | unit_price | sum | PASS |
| CP-3848 | order_type | sales_region, product_category, customer_type | unit_price | mean | PASS |
| CP-3849 | order_type | sales_region, product_category, customer_type | unit_price | count | PASS |
| CP-3850 | order_type | sales_region, product_category, customer_type | quantity, unit_price | sum | PASS |
| CP-3851 | order_type | sales_region, product_category, customer_type | quantity, unit_price | mean | PASS |
| CP-3852 | order_type | sales_region, product_category, customer_type | quantity, unit_price | count | PASS |
| CP-3853 | order_type | sales_region, product_category, customer_type | sale_price | sum | PASS |
| CP-3854 | order_type | sales_region, product_category, customer_type | sale_price | mean | PASS |
| CP-3855 | order_type | sales_region, product_category, customer_type | sale_price | count | PASS |
| CP-3856 | order_type | sales_region, product_category, customer_type | quantity, sale_price | sum | PASS |
| CP-3857 | order_type | sales_region, product_category, customer_type | quantity, sale_price | mean | PASS |
| CP-3858 | order_type | sales_region, product_category, customer_type | quantity, sale_price | count | PASS |
| CP-3859 | order_type | sales_region, product_category, customer_type | unit_price, sale_price | sum | PASS |
| CP-3860 | order_type | sales_region, product_category, customer_type | unit_price, sale_price | mean | PASS |
| CP-3861 | order_type | sales_region, product_category, customer_type | unit_price, sale_price | count | PASS |
| CP-3862 | order_type | sales_region, product_category, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3863 | order_type | sales_region, product_category, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3864 | order_type | sales_region, product_category, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-3865 | order_type | sales_region, product_category | quantity | sum | PASS |
| CP-3866 | order_type | sales_region, product_category | quantity | mean | PASS |
| CP-3867 | order_type | sales_region, product_category | quantity | count | PASS |
| CP-3868 | order_type | sales_region, product_category | unit_price | sum | PASS |
| CP-3869 | order_type | sales_region, product_category | unit_price | mean | PASS |
| CP-3870 | order_type | sales_region, product_category | unit_price | count | PASS |
| CP-3871 | order_type | sales_region, product_category | quantity, unit_price | sum | PASS |
| CP-3872 | order_type | sales_region, product_category | quantity, unit_price | mean | PASS |
| CP-3873 | order_type | sales_region, product_category | quantity, unit_price | count | PASS |
| CP-3874 | order_type | sales_region, product_category | sale_price | sum | PASS |
| CP-3875 | order_type | sales_region, product_category | sale_price | mean | PASS |
| CP-3876 | order_type | sales_region, product_category | sale_price | count | PASS |
| CP-3877 | order_type | sales_region, product_category | quantity, sale_price | sum | PASS |
| CP-3878 | order_type | sales_region, product_category | quantity, sale_price | mean | PASS |
| CP-3879 | order_type | sales_region, product_category | quantity, sale_price | count | PASS |
| CP-3880 | order_type | sales_region, product_category | unit_price, sale_price | sum | PASS |
| CP-3881 | order_type | sales_region, product_category | unit_price, sale_price | mean | PASS |
| CP-3882 | order_type | sales_region, product_category | unit_price, sale_price | count | PASS |
| CP-3883 | order_type | sales_region, product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-3884 | order_type | sales_region, product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-3885 | order_type | sales_region, product_category | quantity, unit_price, sale_price | count | PASS |
| CP-3886 | customer_type | sales_region, product_category, order_type | quantity | sum | PASS |
| CP-3887 | customer_type | sales_region, product_category, order_type | quantity | mean | PASS |
| CP-3888 | customer_type | sales_region, product_category, order_type | quantity | count | PASS |
| CP-3889 | customer_type | sales_region, product_category, order_type | unit_price | sum | PASS |
| CP-3890 | customer_type | sales_region, product_category, order_type | unit_price | mean | PASS |
| CP-3891 | customer_type | sales_region, product_category, order_type | unit_price | count | PASS |
| CP-3892 | customer_type | sales_region, product_category, order_type | quantity, unit_price | sum | PASS |
| CP-3893 | customer_type | sales_region, product_category, order_type | quantity, unit_price | mean | PASS |
| CP-3894 | customer_type | sales_region, product_category, order_type | quantity, unit_price | count | PASS |
| CP-3895 | customer_type | sales_region, product_category, order_type | sale_price | sum | PASS |
| CP-3896 | customer_type | sales_region, product_category, order_type | sale_price | mean | PASS |
| CP-3897 | customer_type | sales_region, product_category, order_type | sale_price | count | PASS |
| CP-3898 | customer_type | sales_region, product_category, order_type | quantity, sale_price | sum | PASS |
| CP-3899 | customer_type | sales_region, product_category, order_type | quantity, sale_price | mean | PASS |
| CP-3900 | customer_type | sales_region, product_category, order_type | quantity, sale_price | count | PASS |
| CP-3901 | customer_type | sales_region, product_category, order_type | unit_price, sale_price | sum | PASS |
| CP-3902 | customer_type | sales_region, product_category, order_type | unit_price, sale_price | mean | PASS |
| CP-3903 | customer_type | sales_region, product_category, order_type | unit_price, sale_price | count | PASS |
| CP-3904 | customer_type | sales_region, product_category, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3905 | customer_type | sales_region, product_category, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3906 | customer_type | sales_region, product_category, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-3907 | customer_type | sales_region, product_category | quantity | sum | PASS |
| CP-3908 | customer_type | sales_region, product_category | quantity | mean | PASS |
| CP-3909 | customer_type | sales_region, product_category | quantity | count | PASS |
| CP-3910 | customer_type | sales_region, product_category | unit_price | sum | PASS |
| CP-3911 | customer_type | sales_region, product_category | unit_price | mean | PASS |
| CP-3912 | customer_type | sales_region, product_category | unit_price | count | PASS |
| CP-3913 | customer_type | sales_region, product_category | quantity, unit_price | sum | PASS |
| CP-3914 | customer_type | sales_region, product_category | quantity, unit_price | mean | PASS |
| CP-3915 | customer_type | sales_region, product_category | quantity, unit_price | count | PASS |
| CP-3916 | customer_type | sales_region, product_category | sale_price | sum | PASS |
| CP-3917 | customer_type | sales_region, product_category | sale_price | mean | PASS |
| CP-3918 | customer_type | sales_region, product_category | sale_price | count | PASS |
| CP-3919 | customer_type | sales_region, product_category | quantity, sale_price | sum | PASS |
| CP-3920 | customer_type | sales_region, product_category | quantity, sale_price | mean | PASS |
| CP-3921 | customer_type | sales_region, product_category | quantity, sale_price | count | PASS |
| CP-3922 | customer_type | sales_region, product_category | unit_price, sale_price | sum | PASS |
| CP-3923 | customer_type | sales_region, product_category | unit_price, sale_price | mean | PASS |
| CP-3924 | customer_type | sales_region, product_category | unit_price, sale_price | count | PASS |
| CP-3925 | customer_type | sales_region, product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-3926 | customer_type | sales_region, product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-3927 | customer_type | sales_region, product_category | quantity, unit_price, sale_price | count | PASS |
| CP-3928 | order_type, customer_type | sales_region | quantity | sum | PASS |
| CP-3929 | order_type, customer_type | sales_region | quantity | mean | PASS |
| CP-3930 | order_type, customer_type | sales_region | quantity | count | PASS |
| CP-3931 | order_type, customer_type | sales_region | unit_price | sum | PASS |
| CP-3932 | order_type, customer_type | sales_region | unit_price | mean | PASS |
| CP-3933 | order_type, customer_type | sales_region | unit_price | count | PASS |
| CP-3934 | order_type, customer_type | sales_region | quantity, unit_price | sum | PASS |
| CP-3935 | order_type, customer_type | sales_region | quantity, unit_price | mean | PASS |
| CP-3936 | order_type, customer_type | sales_region | quantity, unit_price | count | PASS |
| CP-3937 | order_type, customer_type | sales_region | sale_price | sum | PASS |
| CP-3938 | order_type, customer_type | sales_region | sale_price | mean | PASS |
| CP-3939 | order_type, customer_type | sales_region | sale_price | count | PASS |
| CP-3940 | order_type, customer_type | sales_region | quantity, sale_price | sum | PASS |
| CP-3941 | order_type, customer_type | sales_region | quantity, sale_price | mean | PASS |
| CP-3942 | order_type, customer_type | sales_region | quantity, sale_price | count | PASS |
| CP-3943 | order_type, customer_type | sales_region | unit_price, sale_price | sum | PASS |
| CP-3944 | order_type, customer_type | sales_region | unit_price, sale_price | mean | PASS |
| CP-3945 | order_type, customer_type | sales_region | unit_price, sale_price | count | PASS |
| CP-3946 | order_type, customer_type | sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-3947 | order_type, customer_type | sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-3948 | order_type, customer_type | sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-3949 | order_type | sales_region, customer_type | quantity | sum | PASS |
| CP-3950 | order_type | sales_region, customer_type | quantity | mean | PASS |
| CP-3951 | order_type | sales_region, customer_type | quantity | count | PASS |
| CP-3952 | order_type | sales_region, customer_type | unit_price | sum | PASS |
| CP-3953 | order_type | sales_region, customer_type | unit_price | mean | PASS |
| CP-3954 | order_type | sales_region, customer_type | unit_price | count | PASS |
| CP-3955 | order_type | sales_region, customer_type | quantity, unit_price | sum | PASS |
| CP-3956 | order_type | sales_region, customer_type | quantity, unit_price | mean | PASS |
| CP-3957 | order_type | sales_region, customer_type | quantity, unit_price | count | PASS |
| CP-3958 | order_type | sales_region, customer_type | sale_price | sum | PASS |
| CP-3959 | order_type | sales_region, customer_type | sale_price | mean | PASS |
| CP-3960 | order_type | sales_region, customer_type | sale_price | count | PASS |
| CP-3961 | order_type | sales_region, customer_type | quantity, sale_price | sum | PASS |
| CP-3962 | order_type | sales_region, customer_type | quantity, sale_price | mean | PASS |
| CP-3963 | order_type | sales_region, customer_type | quantity, sale_price | count | PASS |
| CP-3964 | order_type | sales_region, customer_type | unit_price, sale_price | sum | PASS |
| CP-3965 | order_type | sales_region, customer_type | unit_price, sale_price | mean | PASS |
| CP-3966 | order_type | sales_region, customer_type | unit_price, sale_price | count | PASS |
| CP-3967 | order_type | sales_region, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-3968 | order_type | sales_region, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-3969 | order_type | sales_region, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-3970 | order_type | sales_region | quantity | sum | PASS |
| CP-3971 | order_type | sales_region | quantity | mean | PASS |
| CP-3972 | order_type | sales_region | quantity | count | PASS |
| CP-3973 | order_type | sales_region | unit_price | sum | PASS |
| CP-3974 | order_type | sales_region | unit_price | mean | PASS |
| CP-3975 | order_type | sales_region | unit_price | count | PASS |
| CP-3976 | order_type | sales_region | quantity, unit_price | sum | PASS |
| CP-3977 | order_type | sales_region | quantity, unit_price | mean | PASS |
| CP-3978 | order_type | sales_region | quantity, unit_price | count | PASS |
| CP-3979 | order_type | sales_region | sale_price | sum | PASS |
| CP-3980 | order_type | sales_region | sale_price | mean | PASS |
| CP-3981 | order_type | sales_region | sale_price | count | PASS |
| CP-3982 | order_type | sales_region | quantity, sale_price | sum | PASS |
| CP-3983 | order_type | sales_region | quantity, sale_price | mean | PASS |
| CP-3984 | order_type | sales_region | quantity, sale_price | count | PASS |
| CP-3985 | order_type | sales_region | unit_price, sale_price | sum | PASS |
| CP-3986 | order_type | sales_region | unit_price, sale_price | mean | PASS |
| CP-3987 | order_type | sales_region | unit_price, sale_price | count | PASS |
| CP-3988 | order_type | sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-3989 | order_type | sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-3990 | order_type | sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-3991 | customer_type | sales_region, order_type | quantity | sum | PASS |
| CP-3992 | customer_type | sales_region, order_type | quantity | mean | PASS |
| CP-3993 | customer_type | sales_region, order_type | quantity | count | PASS |
| CP-3994 | customer_type | sales_region, order_type | unit_price | sum | PASS |
| CP-3995 | customer_type | sales_region, order_type | unit_price | mean | PASS |
| CP-3996 | customer_type | sales_region, order_type | unit_price | count | PASS |
| CP-3997 | customer_type | sales_region, order_type | quantity, unit_price | sum | PASS |
| CP-3998 | customer_type | sales_region, order_type | quantity, unit_price | mean | PASS |
| CP-3999 | customer_type | sales_region, order_type | quantity, unit_price | count | PASS |
| CP-4000 | customer_type | sales_region, order_type | sale_price | sum | PASS |
| CP-4001 | customer_type | sales_region, order_type | sale_price | mean | PASS |
| CP-4002 | customer_type | sales_region, order_type | sale_price | count | PASS |
| CP-4003 | customer_type | sales_region, order_type | quantity, sale_price | sum | PASS |
| CP-4004 | customer_type | sales_region, order_type | quantity, sale_price | mean | PASS |
| CP-4005 | customer_type | sales_region, order_type | quantity, sale_price | count | PASS |
| CP-4006 | customer_type | sales_region, order_type | unit_price, sale_price | sum | PASS |
| CP-4007 | customer_type | sales_region, order_type | unit_price, sale_price | mean | PASS |
| CP-4008 | customer_type | sales_region, order_type | unit_price, sale_price | count | PASS |
| CP-4009 | customer_type | sales_region, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-4010 | customer_type | sales_region, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-4011 | customer_type | sales_region, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-4012 | customer_type | sales_region | quantity | sum | PASS |
| CP-4013 | customer_type | sales_region | quantity | mean | PASS |
| CP-4014 | customer_type | sales_region | quantity | count | PASS |
| CP-4015 | customer_type | sales_region | unit_price | sum | PASS |
| CP-4016 | customer_type | sales_region | unit_price | mean | PASS |
| CP-4017 | customer_type | sales_region | unit_price | count | PASS |
| CP-4018 | customer_type | sales_region | quantity, unit_price | sum | PASS |
| CP-4019 | customer_type | sales_region | quantity, unit_price | mean | PASS |
| CP-4020 | customer_type | sales_region | quantity, unit_price | count | PASS |
| CP-4021 | customer_type | sales_region | sale_price | sum | PASS |
| CP-4022 | customer_type | sales_region | sale_price | mean | PASS |
| CP-4023 | customer_type | sales_region | sale_price | count | PASS |
| CP-4024 | customer_type | sales_region | quantity, sale_price | sum | PASS |
| CP-4025 | customer_type | sales_region | quantity, sale_price | mean | PASS |
| CP-4026 | customer_type | sales_region | quantity, sale_price | count | PASS |
| CP-4027 | customer_type | sales_region | unit_price, sale_price | sum | PASS |
| CP-4028 | customer_type | sales_region | unit_price, sale_price | mean | PASS |
| CP-4029 | customer_type | sales_region | unit_price, sale_price | count | PASS |
| CP-4030 | customer_type | sales_region | quantity, unit_price, sale_price | sum | PASS |
| CP-4031 | customer_type | sales_region | quantity, unit_price, sale_price | mean | PASS |
| CP-4032 | customer_type | sales_region | quantity, unit_price, sale_price | count | PASS |
| CP-4033 | product_category, order_type, customer_type | - | quantity | sum | PASS |
| CP-4034 | product_category, order_type, customer_type | - | quantity | mean | PASS |
| CP-4035 | product_category, order_type, customer_type | - | quantity | count | PASS |
| CP-4036 | product_category, order_type, customer_type | - | unit_price | sum | PASS |
| CP-4037 | product_category, order_type, customer_type | - | unit_price | mean | PASS |
| CP-4038 | product_category, order_type, customer_type | - | unit_price | count | PASS |
| CP-4039 | product_category, order_type, customer_type | - | quantity, unit_price | sum | PASS |
| CP-4040 | product_category, order_type, customer_type | - | quantity, unit_price | mean | PASS |
| CP-4041 | product_category, order_type, customer_type | - | quantity, unit_price | count | PASS |
| CP-4042 | product_category, order_type, customer_type | - | sale_price | sum | PASS |
| CP-4043 | product_category, order_type, customer_type | - | sale_price | mean | PASS |
| CP-4044 | product_category, order_type, customer_type | - | sale_price | count | PASS |
| CP-4045 | product_category, order_type, customer_type | - | quantity, sale_price | sum | PASS |
| CP-4046 | product_category, order_type, customer_type | - | quantity, sale_price | mean | PASS |
| CP-4047 | product_category, order_type, customer_type | - | quantity, sale_price | count | PASS |
| CP-4048 | product_category, order_type, customer_type | - | unit_price, sale_price | sum | PASS |
| CP-4049 | product_category, order_type, customer_type | - | unit_price, sale_price | mean | PASS |
| CP-4050 | product_category, order_type, customer_type | - | unit_price, sale_price | count | PASS |
| CP-4051 | product_category, order_type, customer_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-4052 | product_category, order_type, customer_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-4053 | product_category, order_type, customer_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-4054 | product_category, order_type | customer_type | quantity | sum | PASS |
| CP-4055 | product_category, order_type | customer_type | quantity | mean | PASS |
| CP-4056 | product_category, order_type | customer_type | quantity | count | PASS |
| CP-4057 | product_category, order_type | customer_type | unit_price | sum | PASS |
| CP-4058 | product_category, order_type | customer_type | unit_price | mean | PASS |
| CP-4059 | product_category, order_type | customer_type | unit_price | count | PASS |
| CP-4060 | product_category, order_type | customer_type | quantity, unit_price | sum | PASS |
| CP-4061 | product_category, order_type | customer_type | quantity, unit_price | mean | PASS |
| CP-4062 | product_category, order_type | customer_type | quantity, unit_price | count | PASS |
| CP-4063 | product_category, order_type | customer_type | sale_price | sum | PASS |
| CP-4064 | product_category, order_type | customer_type | sale_price | mean | PASS |
| CP-4065 | product_category, order_type | customer_type | sale_price | count | PASS |
| CP-4066 | product_category, order_type | customer_type | quantity, sale_price | sum | PASS |
| CP-4067 | product_category, order_type | customer_type | quantity, sale_price | mean | PASS |
| CP-4068 | product_category, order_type | customer_type | quantity, sale_price | count | PASS |
| CP-4069 | product_category, order_type | customer_type | unit_price, sale_price | sum | PASS |
| CP-4070 | product_category, order_type | customer_type | unit_price, sale_price | mean | PASS |
| CP-4071 | product_category, order_type | customer_type | unit_price, sale_price | count | PASS |
| CP-4072 | product_category, order_type | customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-4073 | product_category, order_type | customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-4074 | product_category, order_type | customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-4075 | product_category, order_type | - | quantity | sum | PASS |
| CP-4076 | product_category, order_type | - | quantity | mean | PASS |
| CP-4077 | product_category, order_type | - | quantity | count | PASS |
| CP-4078 | product_category, order_type | - | unit_price | sum | PASS |
| CP-4079 | product_category, order_type | - | unit_price | mean | PASS |
| CP-4080 | product_category, order_type | - | unit_price | count | PASS |
| CP-4081 | product_category, order_type | - | quantity, unit_price | sum | PASS |
| CP-4082 | product_category, order_type | - | quantity, unit_price | mean | PASS |
| CP-4083 | product_category, order_type | - | quantity, unit_price | count | PASS |
| CP-4084 | product_category, order_type | - | sale_price | sum | PASS |
| CP-4085 | product_category, order_type | - | sale_price | mean | PASS |
| CP-4086 | product_category, order_type | - | sale_price | count | PASS |
| CP-4087 | product_category, order_type | - | quantity, sale_price | sum | PASS |
| CP-4088 | product_category, order_type | - | quantity, sale_price | mean | PASS |
| CP-4089 | product_category, order_type | - | quantity, sale_price | count | PASS |
| CP-4090 | product_category, order_type | - | unit_price, sale_price | sum | PASS |
| CP-4091 | product_category, order_type | - | unit_price, sale_price | mean | PASS |
| CP-4092 | product_category, order_type | - | unit_price, sale_price | count | PASS |
| CP-4093 | product_category, order_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-4094 | product_category, order_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-4095 | product_category, order_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-4096 | product_category, customer_type | order_type | quantity | sum | PASS |
| CP-4097 | product_category, customer_type | order_type | quantity | mean | PASS |
| CP-4098 | product_category, customer_type | order_type | quantity | count | PASS |
| CP-4099 | product_category, customer_type | order_type | unit_price | sum | PASS |
| CP-4100 | product_category, customer_type | order_type | unit_price | mean | PASS |
| CP-4101 | product_category, customer_type | order_type | unit_price | count | PASS |
| CP-4102 | product_category, customer_type | order_type | quantity, unit_price | sum | PASS |
| CP-4103 | product_category, customer_type | order_type | quantity, unit_price | mean | PASS |
| CP-4104 | product_category, customer_type | order_type | quantity, unit_price | count | PASS |
| CP-4105 | product_category, customer_type | order_type | sale_price | sum | PASS |
| CP-4106 | product_category, customer_type | order_type | sale_price | mean | PASS |
| CP-4107 | product_category, customer_type | order_type | sale_price | count | PASS |
| CP-4108 | product_category, customer_type | order_type | quantity, sale_price | sum | PASS |
| CP-4109 | product_category, customer_type | order_type | quantity, sale_price | mean | PASS |
| CP-4110 | product_category, customer_type | order_type | quantity, sale_price | count | PASS |
| CP-4111 | product_category, customer_type | order_type | unit_price, sale_price | sum | PASS |
| CP-4112 | product_category, customer_type | order_type | unit_price, sale_price | mean | PASS |
| CP-4113 | product_category, customer_type | order_type | unit_price, sale_price | count | PASS |
| CP-4114 | product_category, customer_type | order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-4115 | product_category, customer_type | order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-4116 | product_category, customer_type | order_type | quantity, unit_price, sale_price | count | PASS |
| CP-4117 | product_category | order_type, customer_type | quantity | sum | PASS |
| CP-4118 | product_category | order_type, customer_type | quantity | mean | PASS |
| CP-4119 | product_category | order_type, customer_type | quantity | count | PASS |
| CP-4120 | product_category | order_type, customer_type | unit_price | sum | PASS |
| CP-4121 | product_category | order_type, customer_type | unit_price | mean | PASS |
| CP-4122 | product_category | order_type, customer_type | unit_price | count | PASS |
| CP-4123 | product_category | order_type, customer_type | quantity, unit_price | sum | PASS |
| CP-4124 | product_category | order_type, customer_type | quantity, unit_price | mean | PASS |
| CP-4125 | product_category | order_type, customer_type | quantity, unit_price | count | PASS |
| CP-4126 | product_category | order_type, customer_type | sale_price | sum | PASS |
| CP-4127 | product_category | order_type, customer_type | sale_price | mean | PASS |
| CP-4128 | product_category | order_type, customer_type | sale_price | count | PASS |
| CP-4129 | product_category | order_type, customer_type | quantity, sale_price | sum | PASS |
| CP-4130 | product_category | order_type, customer_type | quantity, sale_price | mean | PASS |
| CP-4131 | product_category | order_type, customer_type | quantity, sale_price | count | PASS |
| CP-4132 | product_category | order_type, customer_type | unit_price, sale_price | sum | PASS |
| CP-4133 | product_category | order_type, customer_type | unit_price, sale_price | mean | PASS |
| CP-4134 | product_category | order_type, customer_type | unit_price, sale_price | count | PASS |
| CP-4135 | product_category | order_type, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-4136 | product_category | order_type, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-4137 | product_category | order_type, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-4138 | product_category | order_type | quantity | sum | PASS |
| CP-4139 | product_category | order_type | quantity | mean | PASS |
| CP-4140 | product_category | order_type | quantity | count | PASS |
| CP-4141 | product_category | order_type | unit_price | sum | PASS |
| CP-4142 | product_category | order_type | unit_price | mean | PASS |
| CP-4143 | product_category | order_type | unit_price | count | PASS |
| CP-4144 | product_category | order_type | quantity, unit_price | sum | PASS |
| CP-4145 | product_category | order_type | quantity, unit_price | mean | PASS |
| CP-4146 | product_category | order_type | quantity, unit_price | count | PASS |
| CP-4147 | product_category | order_type | sale_price | sum | PASS |
| CP-4148 | product_category | order_type | sale_price | mean | PASS |
| CP-4149 | product_category | order_type | sale_price | count | PASS |
| CP-4150 | product_category | order_type | quantity, sale_price | sum | PASS |
| CP-4151 | product_category | order_type | quantity, sale_price | mean | PASS |
| CP-4152 | product_category | order_type | quantity, sale_price | count | PASS |
| CP-4153 | product_category | order_type | unit_price, sale_price | sum | PASS |
| CP-4154 | product_category | order_type | unit_price, sale_price | mean | PASS |
| CP-4155 | product_category | order_type | unit_price, sale_price | count | PASS |
| CP-4156 | product_category | order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-4157 | product_category | order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-4158 | product_category | order_type | quantity, unit_price, sale_price | count | PASS |
| CP-4159 | product_category, customer_type | - | quantity | sum | PASS |
| CP-4160 | product_category, customer_type | - | quantity | mean | PASS |
| CP-4161 | product_category, customer_type | - | quantity | count | PASS |
| CP-4162 | product_category, customer_type | - | unit_price | sum | PASS |
| CP-4163 | product_category, customer_type | - | unit_price | mean | PASS |
| CP-4164 | product_category, customer_type | - | unit_price | count | PASS |
| CP-4165 | product_category, customer_type | - | quantity, unit_price | sum | PASS |
| CP-4166 | product_category, customer_type | - | quantity, unit_price | mean | PASS |
| CP-4167 | product_category, customer_type | - | quantity, unit_price | count | PASS |
| CP-4168 | product_category, customer_type | - | sale_price | sum | PASS |
| CP-4169 | product_category, customer_type | - | sale_price | mean | PASS |
| CP-4170 | product_category, customer_type | - | sale_price | count | PASS |
| CP-4171 | product_category, customer_type | - | quantity, sale_price | sum | PASS |
| CP-4172 | product_category, customer_type | - | quantity, sale_price | mean | PASS |
| CP-4173 | product_category, customer_type | - | quantity, sale_price | count | PASS |
| CP-4174 | product_category, customer_type | - | unit_price, sale_price | sum | PASS |
| CP-4175 | product_category, customer_type | - | unit_price, sale_price | mean | PASS |
| CP-4176 | product_category, customer_type | - | unit_price, sale_price | count | PASS |
| CP-4177 | product_category, customer_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-4178 | product_category, customer_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-4179 | product_category, customer_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-4180 | product_category | customer_type | quantity | sum | PASS |
| CP-4181 | product_category | customer_type | quantity | mean | PASS |
| CP-4182 | product_category | customer_type | quantity | count | PASS |
| CP-4183 | product_category | customer_type | unit_price | sum | PASS |
| CP-4184 | product_category | customer_type | unit_price | mean | PASS |
| CP-4185 | product_category | customer_type | unit_price | count | PASS |
| CP-4186 | product_category | customer_type | quantity, unit_price | sum | PASS |
| CP-4187 | product_category | customer_type | quantity, unit_price | mean | PASS |
| CP-4188 | product_category | customer_type | quantity, unit_price | count | PASS |
| CP-4189 | product_category | customer_type | sale_price | sum | PASS |
| CP-4190 | product_category | customer_type | sale_price | mean | PASS |
| CP-4191 | product_category | customer_type | sale_price | count | PASS |
| CP-4192 | product_category | customer_type | quantity, sale_price | sum | PASS |
| CP-4193 | product_category | customer_type | quantity, sale_price | mean | PASS |
| CP-4194 | product_category | customer_type | quantity, sale_price | count | PASS |
| CP-4195 | product_category | customer_type | unit_price, sale_price | sum | PASS |
| CP-4196 | product_category | customer_type | unit_price, sale_price | mean | PASS |
| CP-4197 | product_category | customer_type | unit_price, sale_price | count | PASS |
| CP-4198 | product_category | customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-4199 | product_category | customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-4200 | product_category | customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-4201 | product_category | - | quantity | sum | PASS |
| CP-4202 | product_category | - | quantity | mean | PASS |
| CP-4203 | product_category | - | quantity | count | PASS |
| CP-4204 | product_category | - | unit_price | sum | PASS |
| CP-4205 | product_category | - | unit_price | mean | PASS |
| CP-4206 | product_category | - | unit_price | count | PASS |
| CP-4207 | product_category | - | quantity, unit_price | sum | PASS |
| CP-4208 | product_category | - | quantity, unit_price | mean | PASS |
| CP-4209 | product_category | - | quantity, unit_price | count | PASS |
| CP-4210 | product_category | - | sale_price | sum | PASS |
| CP-4211 | product_category | - | sale_price | mean | PASS |
| CP-4212 | product_category | - | sale_price | count | PASS |
| CP-4213 | product_category | - | quantity, sale_price | sum | PASS |
| CP-4214 | product_category | - | quantity, sale_price | mean | PASS |
| CP-4215 | product_category | - | quantity, sale_price | count | PASS |
| CP-4216 | product_category | - | unit_price, sale_price | sum | PASS |
| CP-4217 | product_category | - | unit_price, sale_price | mean | PASS |
| CP-4218 | product_category | - | unit_price, sale_price | count | PASS |
| CP-4219 | product_category | - | quantity, unit_price, sale_price | sum | PASS |
| CP-4220 | product_category | - | quantity, unit_price, sale_price | mean | PASS |
| CP-4221 | product_category | - | quantity, unit_price, sale_price | count | PASS |
| CP-4222 | order_type, customer_type | product_category | quantity | sum | PASS |
| CP-4223 | order_type, customer_type | product_category | quantity | mean | PASS |
| CP-4224 | order_type, customer_type | product_category | quantity | count | PASS |
| CP-4225 | order_type, customer_type | product_category | unit_price | sum | PASS |
| CP-4226 | order_type, customer_type | product_category | unit_price | mean | PASS |
| CP-4227 | order_type, customer_type | product_category | unit_price | count | PASS |
| CP-4228 | order_type, customer_type | product_category | quantity, unit_price | sum | PASS |
| CP-4229 | order_type, customer_type | product_category | quantity, unit_price | mean | PASS |
| CP-4230 | order_type, customer_type | product_category | quantity, unit_price | count | PASS |
| CP-4231 | order_type, customer_type | product_category | sale_price | sum | PASS |
| CP-4232 | order_type, customer_type | product_category | sale_price | mean | PASS |
| CP-4233 | order_type, customer_type | product_category | sale_price | count | PASS |
| CP-4234 | order_type, customer_type | product_category | quantity, sale_price | sum | PASS |
| CP-4235 | order_type, customer_type | product_category | quantity, sale_price | mean | PASS |
| CP-4236 | order_type, customer_type | product_category | quantity, sale_price | count | PASS |
| CP-4237 | order_type, customer_type | product_category | unit_price, sale_price | sum | PASS |
| CP-4238 | order_type, customer_type | product_category | unit_price, sale_price | mean | PASS |
| CP-4239 | order_type, customer_type | product_category | unit_price, sale_price | count | PASS |
| CP-4240 | order_type, customer_type | product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-4241 | order_type, customer_type | product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-4242 | order_type, customer_type | product_category | quantity, unit_price, sale_price | count | PASS |
| CP-4243 | order_type | product_category, customer_type | quantity | sum | PASS |
| CP-4244 | order_type | product_category, customer_type | quantity | mean | PASS |
| CP-4245 | order_type | product_category, customer_type | quantity | count | PASS |
| CP-4246 | order_type | product_category, customer_type | unit_price | sum | PASS |
| CP-4247 | order_type | product_category, customer_type | unit_price | mean | PASS |
| CP-4248 | order_type | product_category, customer_type | unit_price | count | PASS |
| CP-4249 | order_type | product_category, customer_type | quantity, unit_price | sum | PASS |
| CP-4250 | order_type | product_category, customer_type | quantity, unit_price | mean | PASS |
| CP-4251 | order_type | product_category, customer_type | quantity, unit_price | count | PASS |
| CP-4252 | order_type | product_category, customer_type | sale_price | sum | PASS |
| CP-4253 | order_type | product_category, customer_type | sale_price | mean | PASS |
| CP-4254 | order_type | product_category, customer_type | sale_price | count | PASS |
| CP-4255 | order_type | product_category, customer_type | quantity, sale_price | sum | PASS |
| CP-4256 | order_type | product_category, customer_type | quantity, sale_price | mean | PASS |
| CP-4257 | order_type | product_category, customer_type | quantity, sale_price | count | PASS |
| CP-4258 | order_type | product_category, customer_type | unit_price, sale_price | sum | PASS |
| CP-4259 | order_type | product_category, customer_type | unit_price, sale_price | mean | PASS |
| CP-4260 | order_type | product_category, customer_type | unit_price, sale_price | count | PASS |
| CP-4261 | order_type | product_category, customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-4262 | order_type | product_category, customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-4263 | order_type | product_category, customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-4264 | order_type | product_category | quantity | sum | PASS |
| CP-4265 | order_type | product_category | quantity | mean | PASS |
| CP-4266 | order_type | product_category | quantity | count | PASS |
| CP-4267 | order_type | product_category | unit_price | sum | PASS |
| CP-4268 | order_type | product_category | unit_price | mean | PASS |
| CP-4269 | order_type | product_category | unit_price | count | PASS |
| CP-4270 | order_type | product_category | quantity, unit_price | sum | PASS |
| CP-4271 | order_type | product_category | quantity, unit_price | mean | PASS |
| CP-4272 | order_type | product_category | quantity, unit_price | count | PASS |
| CP-4273 | order_type | product_category | sale_price | sum | PASS |
| CP-4274 | order_type | product_category | sale_price | mean | PASS |
| CP-4275 | order_type | product_category | sale_price | count | PASS |
| CP-4276 | order_type | product_category | quantity, sale_price | sum | PASS |
| CP-4277 | order_type | product_category | quantity, sale_price | mean | PASS |
| CP-4278 | order_type | product_category | quantity, sale_price | count | PASS |
| CP-4279 | order_type | product_category | unit_price, sale_price | sum | PASS |
| CP-4280 | order_type | product_category | unit_price, sale_price | mean | PASS |
| CP-4281 | order_type | product_category | unit_price, sale_price | count | PASS |
| CP-4282 | order_type | product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-4283 | order_type | product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-4284 | order_type | product_category | quantity, unit_price, sale_price | count | PASS |
| CP-4285 | customer_type | product_category, order_type | quantity | sum | PASS |
| CP-4286 | customer_type | product_category, order_type | quantity | mean | PASS |
| CP-4287 | customer_type | product_category, order_type | quantity | count | PASS |
| CP-4288 | customer_type | product_category, order_type | unit_price | sum | PASS |
| CP-4289 | customer_type | product_category, order_type | unit_price | mean | PASS |
| CP-4290 | customer_type | product_category, order_type | unit_price | count | PASS |
| CP-4291 | customer_type | product_category, order_type | quantity, unit_price | sum | PASS |
| CP-4292 | customer_type | product_category, order_type | quantity, unit_price | mean | PASS |
| CP-4293 | customer_type | product_category, order_type | quantity, unit_price | count | PASS |
| CP-4294 | customer_type | product_category, order_type | sale_price | sum | PASS |
| CP-4295 | customer_type | product_category, order_type | sale_price | mean | PASS |
| CP-4296 | customer_type | product_category, order_type | sale_price | count | PASS |
| CP-4297 | customer_type | product_category, order_type | quantity, sale_price | sum | PASS |
| CP-4298 | customer_type | product_category, order_type | quantity, sale_price | mean | PASS |
| CP-4299 | customer_type | product_category, order_type | quantity, sale_price | count | PASS |
| CP-4300 | customer_type | product_category, order_type | unit_price, sale_price | sum | PASS |
| CP-4301 | customer_type | product_category, order_type | unit_price, sale_price | mean | PASS |
| CP-4302 | customer_type | product_category, order_type | unit_price, sale_price | count | PASS |
| CP-4303 | customer_type | product_category, order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-4304 | customer_type | product_category, order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-4305 | customer_type | product_category, order_type | quantity, unit_price, sale_price | count | PASS |
| CP-4306 | customer_type | product_category | quantity | sum | PASS |
| CP-4307 | customer_type | product_category | quantity | mean | PASS |
| CP-4308 | customer_type | product_category | quantity | count | PASS |
| CP-4309 | customer_type | product_category | unit_price | sum | PASS |
| CP-4310 | customer_type | product_category | unit_price | mean | PASS |
| CP-4311 | customer_type | product_category | unit_price | count | PASS |
| CP-4312 | customer_type | product_category | quantity, unit_price | sum | PASS |
| CP-4313 | customer_type | product_category | quantity, unit_price | mean | PASS |
| CP-4314 | customer_type | product_category | quantity, unit_price | count | PASS |
| CP-4315 | customer_type | product_category | sale_price | sum | PASS |
| CP-4316 | customer_type | product_category | sale_price | mean | PASS |
| CP-4317 | customer_type | product_category | sale_price | count | PASS |
| CP-4318 | customer_type | product_category | quantity, sale_price | sum | PASS |
| CP-4319 | customer_type | product_category | quantity, sale_price | mean | PASS |
| CP-4320 | customer_type | product_category | quantity, sale_price | count | PASS |
| CP-4321 | customer_type | product_category | unit_price, sale_price | sum | PASS |
| CP-4322 | customer_type | product_category | unit_price, sale_price | mean | PASS |
| CP-4323 | customer_type | product_category | unit_price, sale_price | count | PASS |
| CP-4324 | customer_type | product_category | quantity, unit_price, sale_price | sum | PASS |
| CP-4325 | customer_type | product_category | quantity, unit_price, sale_price | mean | PASS |
| CP-4326 | customer_type | product_category | quantity, unit_price, sale_price | count | PASS |
| CP-4327 | order_type, customer_type | - | quantity | sum | PASS |
| CP-4328 | order_type, customer_type | - | quantity | mean | PASS |
| CP-4329 | order_type, customer_type | - | quantity | count | PASS |
| CP-4330 | order_type, customer_type | - | unit_price | sum | PASS |
| CP-4331 | order_type, customer_type | - | unit_price | mean | PASS |
| CP-4332 | order_type, customer_type | - | unit_price | count | PASS |
| CP-4333 | order_type, customer_type | - | quantity, unit_price | sum | PASS |
| CP-4334 | order_type, customer_type | - | quantity, unit_price | mean | PASS |
| CP-4335 | order_type, customer_type | - | quantity, unit_price | count | PASS |
| CP-4336 | order_type, customer_type | - | sale_price | sum | PASS |
| CP-4337 | order_type, customer_type | - | sale_price | mean | PASS |
| CP-4338 | order_type, customer_type | - | sale_price | count | PASS |
| CP-4339 | order_type, customer_type | - | quantity, sale_price | sum | PASS |
| CP-4340 | order_type, customer_type | - | quantity, sale_price | mean | PASS |
| CP-4341 | order_type, customer_type | - | quantity, sale_price | count | PASS |
| CP-4342 | order_type, customer_type | - | unit_price, sale_price | sum | PASS |
| CP-4343 | order_type, customer_type | - | unit_price, sale_price | mean | PASS |
| CP-4344 | order_type, customer_type | - | unit_price, sale_price | count | PASS |
| CP-4345 | order_type, customer_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-4346 | order_type, customer_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-4347 | order_type, customer_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-4348 | order_type | customer_type | quantity | sum | PASS |
| CP-4349 | order_type | customer_type | quantity | mean | PASS |
| CP-4350 | order_type | customer_type | quantity | count | PASS |
| CP-4351 | order_type | customer_type | unit_price | sum | PASS |
| CP-4352 | order_type | customer_type | unit_price | mean | PASS |
| CP-4353 | order_type | customer_type | unit_price | count | PASS |
| CP-4354 | order_type | customer_type | quantity, unit_price | sum | PASS |
| CP-4355 | order_type | customer_type | quantity, unit_price | mean | PASS |
| CP-4356 | order_type | customer_type | quantity, unit_price | count | PASS |
| CP-4357 | order_type | customer_type | sale_price | sum | PASS |
| CP-4358 | order_type | customer_type | sale_price | mean | PASS |
| CP-4359 | order_type | customer_type | sale_price | count | PASS |
| CP-4360 | order_type | customer_type | quantity, sale_price | sum | PASS |
| CP-4361 | order_type | customer_type | quantity, sale_price | mean | PASS |
| CP-4362 | order_type | customer_type | quantity, sale_price | count | PASS |
| CP-4363 | order_type | customer_type | unit_price, sale_price | sum | PASS |
| CP-4364 | order_type | customer_type | unit_price, sale_price | mean | PASS |
| CP-4365 | order_type | customer_type | unit_price, sale_price | count | PASS |
| CP-4366 | order_type | customer_type | quantity, unit_price, sale_price | sum | PASS |
| CP-4367 | order_type | customer_type | quantity, unit_price, sale_price | mean | PASS |
| CP-4368 | order_type | customer_type | quantity, unit_price, sale_price | count | PASS |
| CP-4369 | order_type | - | quantity | sum | PASS |
| CP-4370 | order_type | - | quantity | mean | PASS |
| CP-4371 | order_type | - | quantity | count | PASS |
| CP-4372 | order_type | - | unit_price | sum | PASS |
| CP-4373 | order_type | - | unit_price | mean | PASS |
| CP-4374 | order_type | - | unit_price | count | PASS |
| CP-4375 | order_type | - | quantity, unit_price | sum | PASS |
| CP-4376 | order_type | - | quantity, unit_price | mean | PASS |
| CP-4377 | order_type | - | quantity, unit_price | count | PASS |
| CP-4378 | order_type | - | sale_price | sum | PASS |
| CP-4379 | order_type | - | sale_price | mean | PASS |
| CP-4380 | order_type | - | sale_price | count | PASS |
| CP-4381 | order_type | - | quantity, sale_price | sum | PASS |
| CP-4382 | order_type | - | quantity, sale_price | mean | PASS |
| CP-4383 | order_type | - | quantity, sale_price | count | PASS |
| CP-4384 | order_type | - | unit_price, sale_price | sum | PASS |
| CP-4385 | order_type | - | unit_price, sale_price | mean | PASS |
| CP-4386 | order_type | - | unit_price, sale_price | count | PASS |
| CP-4387 | order_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-4388 | order_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-4389 | order_type | - | quantity, unit_price, sale_price | count | PASS |
| CP-4390 | customer_type | order_type | quantity | sum | PASS |
| CP-4391 | customer_type | order_type | quantity | mean | PASS |
| CP-4392 | customer_type | order_type | quantity | count | PASS |
| CP-4393 | customer_type | order_type | unit_price | sum | PASS |
| CP-4394 | customer_type | order_type | unit_price | mean | PASS |
| CP-4395 | customer_type | order_type | unit_price | count | PASS |
| CP-4396 | customer_type | order_type | quantity, unit_price | sum | PASS |
| CP-4397 | customer_type | order_type | quantity, unit_price | mean | PASS |
| CP-4398 | customer_type | order_type | quantity, unit_price | count | PASS |
| CP-4399 | customer_type | order_type | sale_price | sum | PASS |
| CP-4400 | customer_type | order_type | sale_price | mean | PASS |
| CP-4401 | customer_type | order_type | sale_price | count | PASS |
| CP-4402 | customer_type | order_type | quantity, sale_price | sum | PASS |
| CP-4403 | customer_type | order_type | quantity, sale_price | mean | PASS |
| CP-4404 | customer_type | order_type | quantity, sale_price | count | PASS |
| CP-4405 | customer_type | order_type | unit_price, sale_price | sum | PASS |
| CP-4406 | customer_type | order_type | unit_price, sale_price | mean | PASS |
| CP-4407 | customer_type | order_type | unit_price, sale_price | count | PASS |
| CP-4408 | customer_type | order_type | quantity, unit_price, sale_price | sum | PASS |
| CP-4409 | customer_type | order_type | quantity, unit_price, sale_price | mean | PASS |
| CP-4410 | customer_type | order_type | quantity, unit_price, sale_price | count | PASS |
| CP-4411 | customer_type | - | quantity | sum | PASS |
| CP-4412 | customer_type | - | quantity | mean | PASS |
| CP-4413 | customer_type | - | quantity | count | PASS |
| CP-4414 | customer_type | - | unit_price | sum | PASS |
| CP-4415 | customer_type | - | unit_price | mean | PASS |
| CP-4416 | customer_type | - | unit_price | count | PASS |
| CP-4417 | customer_type | - | quantity, unit_price | sum | PASS |
| CP-4418 | customer_type | - | quantity, unit_price | mean | PASS |
| CP-4419 | customer_type | - | quantity, unit_price | count | PASS |
| CP-4420 | customer_type | - | sale_price | sum | PASS |
| CP-4421 | customer_type | - | sale_price | mean | PASS |
| CP-4422 | customer_type | - | sale_price | count | PASS |
| CP-4423 | customer_type | - | quantity, sale_price | sum | PASS |
| CP-4424 | customer_type | - | quantity, sale_price | mean | PASS |
| CP-4425 | customer_type | - | quantity, sale_price | count | PASS |
| CP-4426 | customer_type | - | unit_price, sale_price | sum | PASS |
| CP-4427 | customer_type | - | unit_price, sale_price | mean | PASS |
| CP-4428 | customer_type | - | unit_price, sale_price | count | PASS |
| CP-4429 | customer_type | - | quantity, unit_price, sale_price | sum | PASS |
| CP-4430 | customer_type | - | quantity, unit_price, sale_price | mean | PASS |
| CP-4431 | customer_type | - | quantity, unit_price, sale_price | count | PASS |

## Individual invalid-input and behavior test cases

The following are the exact test calls/sequences from the interactive validation run. At prompt sequences, values are consumed in order; expected retries followed by valid choices are included in the same test. The 23 grouped input runs are expanded into 26 entries because individual menu choices and custom-pivot stages are listed separately.

| ID | Function/stage | Exact input or setup | Expected/observed result |
|---|---|---|---|
| IV-01 | Main menu | `"", "abc", "-1", "0", "12", "1.5", "1"` | Six invalid entries rejected; choice 1 accepted. |
| IV-02 | Main menu option 1 | `"1"` | Returned menu index 0. |
| IV-03 | Main menu option 2 | `"2"` | Returned menu index 1. |
| IV-04 | Main menu option 3 | `"3"` | Returned menu index 2. |
| IV-05 | Main menu option 4 | `"4"` | Returned menu index 3. |
| IV-06 | Main menu option 5 | `"5"` | Returned menu index 4. |
| IV-07 | Main menu option 6 | `"6"` | Returned menu index 5. |
| IV-08 | Main menu option 7 | `"7"` | Returned menu index 6. |
| IV-09 | Main menu option 8 | `"8"` | Returned menu index 7. |
| IV-10 | Main menu option 9 | `"9"` | Returned menu index 8. |
| IV-11 | Main menu option 10 | `"10"` | Returned menu index 9. |
| IV-12 | Main menu option 11 | `"11"` | Returned menu index 10. |
| IV-13 | Row preview | `"abc", "0", "-1", "4", "1.5", "2", "n"` with a 3-row DataFrame | Rejected malformed, out-of-range and decimal inputs; accepted 2. |
| IV-14 | Row preview all | `"ALL", "n"` | Case-insensitive all accepted and all rows displayed. |
| IV-15 | Row preview skip | `"", ""` | Blank preview returned without printing data or requesting export. |
| IV-16 | Required field selection | `"", "abc", "1,", "0", "4", "1,1,2"` with 3 choices | Blank, malformed, empty-token, out-of-range rejected; duplicates removed; returned choices 1 and 2. |
| IV-17 | Optional field selection | `""` with one available choice | Blank accepted as no grouping. |
| IV-18 | Single aggregation selection | `"1,2", "2"` | Multiple choices rejected; one valid choice accepted. |
| IV-19 | No available choices | Empty options list | Reported that no options were available; returned an empty list. |
| IV-20 | Custom pivot row selector | `"", "foo", "0", "7", "1"` with 6 categorical fields | Required blank, malformed, and out-of-range values rejected; row 1 accepted. |
| IV-21 | Custom pivot column selector | `"x", "9", "1"` with 5 remaining fields | Malformed and out-of-range values rejected; column 1 accepted. |
| IV-22 | Custom pivot values selector | `"", "oops", "0", "4", "1"` with 3 measures | Required blank, malformed and out-of-range values rejected; value 1 accepted. |
| IV-23 | Custom pivot aggregation selector | `"1,2", "2"` | Multi-select rejected; mean accepted as the single aggregation. |
| IV-24 | Export confirmation and filename | `"maybe", "yes", "", existing .xlsx path, new name without extension` | Invalid confirmation and blank filename rejected; overwrite refused; `.xlsx` appended and workbook written. |
| IV-25 | Export decline | `"n"` | Returned without writing a workbook. |
| IV-26 | Export write failure | `"yes", "Z:\no_such_folder\result.xlsx"` | Displayed an export error and did not report success. |

## Individual requirement/integration checks

| ID | Test | Setup/verification | Result |
|---|---|---|---|
| RQ-01 | Drive CSV loads | Fetched the supplied Google Drive CSV; confirmed non-empty DataFrame. | PASS |
| RQ-02 | Loading indicator | Captured output contains `Loading sales_data.csv`. | PASS |
| RQ-03 | Load success status | Captured output contains `loaded successfully`. | PASS |
| RQ-04 | Load duration | Captured output contains `Load time:`. | PASS |
| RQ-05 | Row count | Output row count equals `len(data)` (5,130 rows). | PASS |
| RQ-06 | Available columns | Output includes the available column list. | PASS |
| RQ-07 | Missing values filled | Confirmed `data.isna().any().any()` is false on live file. | PASS |
| RQ-08 | Required fields present | Checked all fields in `ANALYTICS_REQUIRED_FIELDS` exist in live data. | PASS |
| RQ-09 | CSV read failure | Mocked `read_csv` raising `OSError`; verified clear `SystemExit`. | PASS |
| RQ-10 | Empty CSV | Mocked empty DataFrame; verified no-usable-data `SystemExit`. | PASS |
| RQ-11 | Missing-field warning | Used DataFrame containing only `sales_region`; checked warning and missing field names. | PASS |
| RQ-12 | Menu structure | Checked menu is a tuple of `(label, callable)` pairs and contains requested items plus stored-results item. | PASS |
| RQ-13 | Standard report: region/order type | Ran report on representative DataFrame; checked region output and stored result. | PASS |
| RQ-14 | Standard report: regional/state/order average | Ran report on representative DataFrame; checked region output and stored result. | PASS |
| RQ-15 | Standard report: customer/order/state | Ran report on representative DataFrame; checked state output and stored result. | PASS |
| RQ-16 | Standard report: region/product | Ran report on representative DataFrame; checked product output and stored result. | PASS |
| RQ-17 | Standard report: order/customer type | Ran report on representative DataFrame; checked customer output and stored result. | PASS |
| RQ-18 | Standard report: category min/max | Ran report on representative DataFrame; checked category output and stored result. | PASS |
| RQ-19 | Standard report: unique employees | Ran report on representative DataFrame; checked unique employee output and stored result. | PASS |
| RQ-20 | All standard reports reject missing columns | Ran each of seven reports on empty DataFrame; each reported missing fields without crashing. | PASS |
| RQ-21 | Results dictionary | Ran all seven reports; verified seven stored results. | PASS |
| RQ-22 | Results display menu item | Displayed results and verified every stored result name and table appeared. | PASS |
| RQ-23 | Standard report replacement | Reran a standard report on different data; verified its stored result was replaced without increasing key count. | PASS |
| RQ-24 | Custom pivot single storage | Generated a custom pivot and checked `Custom pivot table 1` was stored. | PASS |
| RQ-25 | Custom pivot repeated storage | Generated a second custom pivot and checked both numbered results remained stored. | PASS |
| RQ-26 | Sales calculation | Checked quantity times unit price, including invalid numeric values converted to zero. | PASS |
| RQ-27 | Excel formula text protection | Checked formula-leading text was prefixed with a single quote; ordinary text was unchanged. | PASS |
| RQ-28 | Excel export round trip | Wrote `.xlsx`; reopened workbook with `openpyxl`; checked sheet and data. | PASS |
| RQ-29 | Main initializes and exits | Mocked loaded data, selected Exit, and verified dispatch raised exit status 0. | PASS |
| RQ-30 | Main interrupt handling | Mocked `KeyboardInterrupt`; verified graceful exit message. | PASS |
| RQ-31 | Syntax validation | Parsed application source with Python `ast`. | PASS |
| RQ-32 | Whitespace validation | Ran `git diff --check`. | PASS |

## Test runner note

The exhaustive runs were executed using inline Python test harnesses. At the time of the run, `unittest discover` found no persistent unit-test file and returned ?Ran 0 tests?; that result is **not** counted as a pass. The 4,431 custom pivot rows above enumerate every successful valid custom-pivot invocation from the exhaustive run.
