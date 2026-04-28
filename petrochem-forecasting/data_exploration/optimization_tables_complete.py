import pandas as pd
import numpy as np
import plotly.graph_objects as go
from IPython.display import display, HTML

print("="*120)
print("CREATING PRODUCT OPTIMAL RANGES WITH SUPPORTING UTILITY RANGES")
print("="*120)

import sys
from IPython import get_ipython
ipython = get_ipython()

up_wide = globals().get('up_wide')
if up_wide is None:
    raise NameError("up_wide not defined. Please load data first.")

up_wide.columns = up_wide.columns.str.strip()

# Define product tags
product_tags = [
    'FIC10014_PV', 'FIC20017_PV', 'FIC20018_PV', 'FIC25021_PV', 
    'FIC30018_PV', 'FIC40039_PV', 'FI40039_PV', 'FIC40045_PV', 
    'FIC50011_PV', 'FIC60020_PV', 'FIC65004_PV', 'FIC70053_PV', 'FIC95008_PV'
]

# Get utility tags (all tags not in product list)
utility_tags = [tag for tag in up_wide.columns if tag not in product_tags]

print(f"\nProduct Tags: {len([t for t in product_tags if t in up_wide.columns])}")
print(f"Utility Tags: {len(utility_tags)}\n")

# ============================================================================
# MAIN ALGORITHM: EXTRACT OPTIMAL PRODUCT RANGES & UTILITY SUPPORT
# ============================================================================

optimization_table = []

for prod_tag in product_tags:
    if prod_tag not in up_wide.columns:
        continue
    
    print(f"Processing: {prod_tag}...", end=" ")
    
    # STEP 1: Find product's optimal range
    prod_data = up_wide[prod_tag].dropna()
    
    if len(prod_data) < 50:
        print("(SKIP - insufficient data)")
        continue
    
    # Remove outliers
    Q1, Q3 = prod_data.quantile([0.25, 0.75])
    IQR = Q3 - Q1
    clean_data = prod_data[(prod_data >= Q1 - 1.5*IQR) & (prod_data <= Q3 + 1.5*IQR)]
    
    # Get optimal range (middle 50%)
    prod_opt_min = clean_data.quantile(0.25)
    prod_opt_max = clean_data.quantile(0.75)
    prod_mean = clean_data.mean()
    
    # STEP 2: Find indices when product is in optimal range
    optimal_mask = (prod_data >= prod_opt_min) & (prod_data <= prod_opt_max)
    optimal_indices = prod_data[optimal_mask].index
    
    print(f"({optimal_mask.sum()} optimal points)")
    
    # STEP 3: For each utility, extract range during product's optimal operation
    row_data = {
        'Product': prod_tag,
        'Optimal_Min': prod_opt_min,
        'Optimal_Max': prod_opt_max,
        'Optimal_Mean': prod_mean,
        'Optimal_Range_Str': f"{prod_opt_min:.0f}-{prod_opt_max:.0f}",
        'Num_Optimal_Points': optimal_mask.sum()
    }
    
    for util_tag in utility_tags:
        if util_tag not in up_wide.columns:
            continue
        
        util_data = up_wide.loc[optimal_indices, util_tag]
        
        # Remove NaN values
        util_clean = util_data.dropna()
        
        if len(util_clean) > 5:  # Need at least 5 points
            # Get middle 50% range
            util_min = util_clean.quantile(0.25)
            util_max = util_clean.quantile(0.75)
            util_mean = util_clean.mean()
            
            # Store both numeric and string format
            row_data[f'{util_tag}_Min'] = util_min
            row_data[f'{util_tag}_Max'] = util_max
            row_data[f'{util_tag}_Mean'] = util_mean
            row_data[f'{util_tag}_Range'] = f"{util_min:.0f}-{util_max:.0f}"
        else:
            row_data[f'{util_tag}_Min'] = np.nan
            row_data[f'{util_tag}_Max'] = np.nan
            row_data[f'{util_tag}_Mean'] = np.nan
            row_data[f'{util_tag}_Range'] = 'N/A'
    
    optimization_table.append(row_data)

# ============================================================================
# CREATE MASTER DATAFRAME
# ============================================================================

master_df = pd.DataFrame(optimization_table)

print("\n" + "="*120)
print("MAIN TABLE 1: PRODUCT OPTIMAL RANGES WITH UTILITY RANGES (ALL DATA)")
print("="*120)

# Display master dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print("\n" + master_df.to_string(index=False))

# Store for later use
TABLE_1_MASTER = master_df.copy()

# ============================================================================
# CREATE TABLE 2: SIMPLIFIED VIEW (STRING FORMAT ONLY)
# ============================================================================

print("\n\n" + "="*120)
print("TABLE 2: SIMPLIFIED VIEW (STRING FORMAT - EASY TO READ)")
print("="*120)

table_2_data = []

for _, row in master_df.iterrows():
    table_2_row = {
        'Product': row['Product'],
        'Optimal_Range': row['Optimal_Range_Str']
    }
    
    # Add utility ranges (string format)
    for util in utility_tags:
        util_range_col = f'{util}_Range'
        if util_range_col in row and row[util_range_col] != 'N/A':
            table_2_row[util] = row[util_range_col]
        else:
            table_2_row[util] = '-'
    
    table_2_data.append(table_2_row)

TABLE_2_SIMPLIFIED = pd.DataFrame(table_2_data)

# Display first 15 columns (Product + Optimal_Range + 13 utilities)
display_cols = ['Product', 'Optimal_Range'] + utility_tags[:13]
display_cols = [col for col in display_cols if col in TABLE_2_SIMPLIFIED.columns]

print("\n" + TABLE_2_SIMPLIFIED[display_cols].to_string(index=False))

if len(utility_tags) > 13:
    print(f"\n(Showing first 15 columns; Total utilities: {len(utility_tags)})")

# ============================================================================
# CREATE TABLE 3: NUMERIC ONLY (FOR ANALYSIS)
# ============================================================================

print("\n\n" + "="*120)
print("TABLE 3: NUMERIC ONLY (MIN, MAX, MEAN)")
print("="*120)

table_3_data = []

for _, row in master_df.iterrows():
    table_3_row = {
        'Product': row['Product'],
        'Prod_Opt_Min': row['Optimal_Min'],
        'Prod_Opt_Max': row['Optimal_Max'],
        'Prod_Opt_Mean': row['Optimal_Mean']
    }
    
    # Add first 10 utilities with numeric values
    for util in utility_tags[:10]:
        min_col = f'{util}_Min'
        max_col = f'{util}_Max'
        mean_col = f'{util}_Mean'
        
        if min_col in row:
            table_3_row[f'{util}_Min'] = row[min_col]
            table_3_row[f'{util}_Max'] = row[max_col]
            table_3_row[f'{util}_Mean'] = row[mean_col]
    
    table_3_data.append(table_3_row)

TABLE_3_NUMERIC = pd.DataFrame(table_3_data)

print("\n" + TABLE_3_NUMERIC.to_string(index=False))

# ============================================================================
# CREATE TABLE 4: UTILITY-CENTRIC (PIVOT VIEW)
# ============================================================================

print("\n\n" + "="*120)
print("TABLE 4: UTILITY-CENTRIC VIEW (What each utility should be for each product)")
print("="*120)

table_4_data = []

for util in utility_tags:
    table_4_row = {'Utility': util}
    
    for _, prod_row in master_df.iterrows():
        prod_short = prod_row['Product'].replace('_PV', '')
        util_range_col = f'{util}_Range'
        
        if util_range_col in prod_row and prod_row[util_range_col] != 'N/A':
            table_4_row[prod_short] = prod_row[util_range_col]
        else:
            table_4_row[prod_short] = '-'
    
    table_4_data.append(table_4_row)

TABLE_4_UTILITY_CENTRIC = pd.DataFrame(table_4_data)

# Display first 10 utilities
display_cols_4 = ['Utility'] + [col for col in TABLE_4_UTILITY_CENTRIC.columns if col != 'Utility'][:13]
display_cols_4 = [col for col in display_cols_4 if col in TABLE_4_UTILITY_CENTRIC.columns]

print("\n" + TABLE_4_UTILITY_CENTRIC[display_cols_4].to_string(index=False))

# ============================================================================
# CREATE TABLE 5: SUMMARY STATISTICS
# ============================================================================

print("\n\n" + "="*120)
print("TABLE 5: SUMMARY STATISTICS")
print("="*120)

table_5_data = []

for _, row in master_df.iterrows():
    # Count defined utilities
    defined_count = sum(1 for util in utility_tags if f'{util}_Range' in row and row[f'{util}_Range'] != 'N/A')
    
    table_5_row = {
        'Product': row['Product'],
        'Optimal_Range': row['Optimal_Range_Str'],
        'Num_Optimal_Points': row['Num_Optimal_Points'],
        'Utilities_Defined': defined_count,
        'Total_Utilities': len(utility_tags),
        'Coverage_Percent': round(defined_count / len(utility_tags) * 100, 1)
    }
    
    table_5_data.append(table_5_row)

TABLE_5_SUMMARY = pd.DataFrame(table_5_data)

print("\n" + TABLE_5_SUMMARY.to_string(index=False))

# ============================================================================
# CREATE TABLE 6: TOP UTILITIES PER PRODUCT
# ============================================================================

print("\n\n" + "="*120)
print("TABLE 6: TOP 3 UTILITIES PER PRODUCT (RANKED BY RANGE WIDTH)")
print("="*120)

table_6_data = []

for _, prod_row in master_df.iterrows():
    product_name = prod_row['Product']
    
    # Calculate range width for each utility
    util_ranges = []
    for util in utility_tags:
        min_col = f'{util}_Min'
        max_col = f'{util}_Max'
        
        if min_col in prod_row and not pd.isna(prod_row[min_col]):
            range_width = prod_row[max_col] - prod_row[min_col]
            util_ranges.append({
                'Utility': util,
                'Min': prod_row[min_col],
                'Max': prod_row[max_col],
                'Mean': prod_row[f'{util}_Mean'],
                'Range_Width': range_width
            })
    
    # Sort by range width (descending)
    util_ranges = sorted(util_ranges, key=lambda x: x['Range_Width'], reverse=True)
    
    # Get top 3
    for rank, util_info in enumerate(util_ranges[:3], 1):
        table_6_row = {
            'Product': product_name,
            'Rank': rank,
            'Utility': util_info['Utility'],
            'Range': f"{util_info['Min']:.0f}-{util_info['Max']:.0f}",
            'Range_Width': round(util_info['Range_Width'], 0),
            'Mean': round(util_info['Mean'], 0)
        }
        table_6_data.append(table_6_row)

TABLE_6_TOP_UTILITIES = pd.DataFrame(table_6_data)

print("\n" + TABLE_6_TOP_UTILITIES.to_string(index=False))

# ============================================================================
# CREATE TABLE 7: PRODUCT CHARACTERISTICS
# ============================================================================

print("\n\n" + "="*120)
print("TABLE 7: PRODUCT CHARACTERISTICS")
print("="*120)

table_7_data = []

for _, row in master_df.iterrows():
    prod_range_width = row['Optimal_Max'] - row['Optimal_Min']
    
    table_7_row = {
        'Product': row['Product'],
        'Optimal_Min': round(row['Optimal_Min'], 1),
        'Optimal_Max': round(row['Optimal_Max'], 1),
        'Optimal_Mean': round(row['Optimal_Mean'], 1),
        'Range_Width': round(prod_range_width, 1),
        'Variability_Percent': round((prod_range_width / row['Optimal_Mean'] * 100), 1),
        'Num_Optimal_Points': row['Num_Optimal_Points']
    }
    
    table_7_data.append(table_7_row)

TABLE_7_CHARACTERISTICS = pd.DataFrame(table_7_data)

print("\n" + TABLE_7_CHARACTERISTICS.to_string(index=False))

# ============================================================================
# EXPORT ALL TABLES TO CSV
# ============================================================================

print("\n\n" + "="*120)
print("EXPORTING ALL TABLES TO CSV FILES")
print("="*120)

filenames = {
    'TABLE_1_Master_Data': TABLE_1_MASTER,
    'TABLE_2_Simplified_View': TABLE_2_SIMPLIFIED,
    'TABLE_3_Numeric_Only': TABLE_3_NUMERIC,
    'TABLE_4_Utility_Centric': TABLE_4_UTILITY_CENTRIC,
    'TABLE_5_Summary_Statistics': TABLE_5_SUMMARY,
    'TABLE_6_Top_Utilities_Per_Product': TABLE_6_TOP_UTILITIES,
    'TABLE_7_Product_Characteristics': TABLE_7_CHARACTERISTICS
}

for filename, df in filenames.items():
    csv_file = f'{filename}.csv'
    df.to_csv(csv_file, index=False)
    print(f"\n✓ {csv_file}")
    print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")

# ============================================================================
# STORE ALL DATAFRAMES IN DICTIONARY FOR ACCESS
# ============================================================================

print("\n\n" + "="*120)
print("ALL DATAFRAMES STORED IN 'optimization_tables' DICTIONARY")
print("="*120)

optimization_tables = {
    'TABLE_1_Master': TABLE_1_MASTER,
    'TABLE_2_Simplified': TABLE_2_SIMPLIFIED,
    'TABLE_3_Numeric': TABLE_3_NUMERIC,
    'TABLE_4_Utility_Centric': TABLE_4_UTILITY_CENTRIC,
    'TABLE_5_Summary': TABLE_5_SUMMARY,
    'TABLE_6_Top_Utilities': TABLE_6_TOP_UTILITIES,
    'TABLE_7_Characteristics': TABLE_7_CHARACTERISTICS
}

print("\nAccess tables like:")
print("  • optimization_tables['TABLE_1_Master']")
print("  • optimization_tables['TABLE_2_Simplified']")
print("  • optimization_tables['TABLE_3_Numeric']")
print("  • etc.")

# ============================================================================
# DISPLAY SUMMARY
# ============================================================================

print("\n\n" + "="*120)
print("SUMMARY")
print("="*120)

summary_text = f"""
✓ ANALYSIS COMPLETE!

Products Analyzed: {len(master_df)}
Total Utilities: {len(utility_tags)}
Average Coverage: {TABLE_5_SUMMARY['Coverage_Percent'].mean():.1f}%

TABLES CREATED:
1. TABLE_1_Master: Full data with numeric and string values for all utilities
2. TABLE_2_Simplified: Product + Optimal_Range + Utility Ranges (easy to read)
3. TABLE_3_Numeric: Only numeric values (for calculations)
4. TABLE_4_Utility_Centric: Utilities as rows, Products as columns (pivot view)
5. TABLE_5_Summary: Statistics - coverage, optimal points, etc.
6. TABLE_6_Top_Utilities: Top 3 utilities per product by range width
7. TABLE_7_Characteristics: Product characteristics - range, variability, etc.

HOW TO USE:
1. Use TABLE_2_Simplified for operational reference
2. Use TABLE_4_Utility_Centric to see all utilities in one place
3. Use TABLE_6_Top_Utilities to identify critical utilities
4. Use TABLE_7_Characteristics to understand product variability

FILES EXPORTED:
All 7 tables saved as CSV files for external use
"""

print(summary_text)

# Display first table as sample
print("\n" + "="*120)
print("SAMPLE: TABLE_2_SIMPLIFIED (First 5 rows)")
print("="*120)
print("\n" + TABLE_2_SIMPLIFIED.head().to_string(index=False))