import pandas as pd
import numpy as np
import plotly.graph_objects as go
from IPython.display import display, HTML

print("="*120)
print("CREATING PRODUCT OPTIMAL RANGES WITH SUPPORTING UTILITY RANGES")
print("="*120)

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
    
    # STEP 2: Find indices when product is in optimal range
    optimal_mask = (prod_data >= prod_opt_min) & (prod_data <= prod_opt_max)
    optimal_indices = prod_data[optimal_mask].index
    
    print(f"({optimal_mask.sum()} optimal points)")
    
    # STEP 3: For each utility, extract range during product's optimal operation
    row_data = {
        'Product': prod_tag,
        'Optimal_Range': f"{prod_opt_min:.0f}-{prod_opt_max:.0f}"
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
            
            row_data[util_tag] = f"{util_min:.0f}-{util_max:.0f}"
        else:
            row_data[util_tag] = "N/A"
    
    optimization_table.append(row_data)

# ============================================================================
# CREATE DATAFRAME
# ============================================================================

final_df = pd.DataFrame(optimization_table)

print("\n" + "="*120)
print("OPTIMIZATION TABLE CREATED")
print("="*120)

# ============================================================================
# DISPLAY TABLE 1: FULL TABLE WITH ALL UTILITIES
# ============================================================================

print("\n\nTABLE 1: COMPLETE OPTIMIZATION RANGES")
print("-"*120)

# Select key columns for display
display_columns = ['Product', 'Optimal_Range'] + utility_tags[:15]  # Show first 15 utilities

if len(utility_tags) > 15:
    print(f"Note: Showing first 15 utilities out of {len(utility_tags)}")

display_df = final_df[display_columns].copy() if all(col in final_df.columns for col in display_columns) else final_df.copy()

print("\n" + display_df.to_string(index=False))

# ============================================================================
# DISPLAY TABLE 2: HTML FORMATTED (PRETTIER)
# ============================================================================

print("\n\n" + "="*120)
print("TABLE 2: FORMATTED HTML VIEW")
print("="*120)

# Create HTML table with styling
html_df = final_df.copy()

# Create HTML
html_string = """
<style>
    table {
        border-collapse: collapse;
        font-family: Arial, sans-serif;
        margin: 20px 0;
    }
    th {
        background-color: #2c3e50;
        color: white;
        padding: 12px;
        text-align: left;
        font-weight: bold;
        border: 1px solid #34495e;
        font-size: 11px;
    }
    td {
        padding: 10px;
        border: 1px solid #bdc3c7;
        font-size: 11px;
    }
    tr:nth-child(even) {
        background-color: #ecf0f1;
    }
    tr:hover {
        background-color: #d5dbdb;
    }
    .product {
        font-weight: bold;
        color: #2c3e50;
    }
    .range {
        background-color: #fff3cd;
        font-weight: bold;
    }
    .utility-range {
        color: #16a085;
        font-family: monospace;
    }
</style>

<table>
    <thead>
        <tr>
            <th>Product Tag</th>
            <th class="range">Optimal Range</th>
"""

# Add utility columns
for util in utility_tags[:12]:  # Show first 12 utilities
    html_string += f"<th>{util}</th>"

html_string += """
        </tr>
    </thead>
    <tbody>
"""

# Add rows
for _, row in final_df.iterrows():
    html_string += f"""
        <tr>
            <td class="product">{row['Product']}</td>
            <td class="range">{row['Optimal_Range']}</td>
"""
    for util in utility_tags[:12]:
        if util in row and pd.notna(row[util]):
            html_string += f'<td class="utility-range">{row[util]}</td>'
        else:
            html_string += '<td>-</td>'
    
    html_string += '</tr>'

html_string += """
    </tbody>
</table>
"""

display(HTML(html_string))

# ============================================================================
# DISPLAY TABLE 3: DETAILED BREAKDOWN (TEXT VIEW)
# ============================================================================

print("\n\n" + "="*120)
print("TABLE 3: DETAILED BREAKDOWN BY PRODUCT")
print("="*120)

for idx, (_, row) in enumerate(final_df.iterrows(), 1):
    print(f"\n{idx}. {row['Product']}")
    print(f"   Optimal Range: {row['Optimal_Range']} KG/H")
    print("   Supporting Utility Ranges:")
    
    util_count = 0
    for util in utility_tags:
        if util in row and row[util] != 'N/A':
            util_count += 1
            if util_count <= 8:  # Show first 8 utilities
                print(f"      • {util:20} : {row[util]:20}")
    
    if len(utility_tags) > 8:
        remaining = len([u for u in utility_tags if u in row and row[u] != 'N/A']) - 8
        if remaining > 0:
            print(f"      ... and {remaining} more utilities")

# ============================================================================
# DISPLAY TABLE 4: PIVOT VIEW (Utilities as rows, Products as columns)
# ============================================================================

print("\n\n" + "="*120)
print("TABLE 4: UTILITY-CENTRIC VIEW (What each utility should be for each product)")
print("="*120)

# Create pivot: Utility x Product
pivot_data = []

for util in utility_tags[:10]:  # First 10 utilities
    row_data = {'Utility': util}
    
    for _, prod_row in final_df.iterrows():
        prod_name = prod_row['Product'].replace('_PV', '')
        if util in prod_row and prod_row[util] != 'N/A':
            row_data[prod_name] = prod_row[util]
        else:
            row_data[prod_name] = '-'
    
    pivot_data.append(row_data)

pivot_df = pd.DataFrame(pivot_data)

print("\n" + pivot_df.to_string(index=False))

if len(utility_tags) > 10:
    print(f"\n(Showing first 10 utilities out of {len(utility_tags)})")

# ============================================================================
# DISPLAY TABLE 5: SUMMARY STATISTICS
# ============================================================================

print("\n\n" + "="*120)
print("TABLE 5: SUMMARY STATISTICS")
print("="*120)

summary_stats = []

for _, row in final_df.iterrows():
    # Count how many utilities have defined ranges
    util_count = sum(1 for util in utility_tags if util in row and row[util] != 'N/A')
    
    summary_stats.append({
        'Product': row['Product'],
        'Optimal_Range': row['Optimal_Range'],
        'Utilities_Defined': util_count,
        'Total_Utilities': len(utility_tags)
    })

summary_df = pd.DataFrame(summary_stats)
summary_df['Coverage_%'] = (summary_df['Utilities_Defined'] / summary_df['Total_Utilities'] * 100).round(1)

print("\n" + summary_df.to_string(index=False))

# ============================================================================
# EXPORT TO CSV
# ============================================================================

print("\n\n" + "="*120)
print("EXPORTING TABLE TO CSV")
print("="*120)

# Select columns to export (Product + Optimal_Range + first 20 utilities)
export_cols = ['Product', 'Optimal_Range'] + utility_tags[:20]
export_df = final_df[[col for col in export_cols if col in final_df.columns]].copy()

csv_filename = 'product_optimization_ranges.csv'
export_df.to_csv(csv_filename, index=False)

print(f"\n✓ Table exported to: {csv_filename}")
print(f"  Rows: {len(export_df)}")
print(f"  Columns: {len(export_df.columns)}")

# ============================================================================
# VISUAL HEATMAP OF RANGES
# ============================================================================

print("\n\n" + "="*120)
print("CREATING VISUALIZATION: HEATMAP OF UTILITY RANGES")
print("="*120)

# Create heatmap showing which utilities have defined ranges
heatmap_data = []
heatmap_rows = []
heatmap_cols = []

for _, prod_row in final_df.iterrows():
    row_data = []
    heatmap_rows.append(prod_row['Product'])
    
    for util in utility_tags[:15]:
        if util in prod_row and prod_row[util] != 'N/A':
            row_data.append(1)  # Has range defined
        else:
            row_data.append(0)  # No range defined
        
        if len(heatmap_cols) < 15:
            heatmap_cols.append(util)
    
    heatmap_data.append(row_data)

fig = go.Figure(data=go.Heatmap(
    z=heatmap_data,
    x=heatmap_cols,
    y=heatmap_rows,
    colorscale='RdYlGn',
    text=[['✓' if val == 1 else '✗' for val in row] for row in heatmap_data],
    texttemplate='%{text}',
    textfont={"size": 14},
    colorbar=dict(title='Has<br>Range'),
    hovertemplate='Product: %{y}<br>Utility: %{x}<extra></extra>'
))

fig.update_layout(
    title='Utility Range Coverage by Product (Green=Defined, Red=Not Defined)',
    xaxis_title='Utility Tags',
    yaxis_title='Product Tags',
    height=600,
    width=1000,
    xaxis_tickangle=45
)

fig.show()

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "="*120)
print("ANALYSIS COMPLETE!")
print("="*120)

summary_text = f"""
✓ Created optimization table for {len(final_df)} products
✓ Defined optimal ranges based on Q1-Q3 of clean data
✓ Extracted supporting utility ranges for each product
✓ Total utilities analyzed: {len(utility_tags)}
✓ Average utilities defined per product: {summary_df['Utilities_Defined'].mean():.1f}

HOW TO USE THIS TABLE:

1. Find your product in the table (e.g., FIC10014_PV)
2. Note its Optimal Range (e.g., 5000-12000 KG/H)
3. To maintain product at optimal status:
   └─ Keep each utility in its specified range
   └─ Example: Keep FI91510 at 8000-15000 to support FIC10014

4. If product drifts out of optimal:
   └─ Check if utilities are still in range
   └─ If utilities OK but product drifts → Equipment issue
   └─ If utilities drift first → Control issue

FILES EXPORTED:
• {csv_filename} - Full table in CSV format
"""

print(summary_text)