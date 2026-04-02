import sys
import re

readme_path = 'C:/Users/ander/Downloads/eeguskiza-main/README.md'
with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove Tech Stack
new_content = re.sub(r'<h2>⚡ Tech Stack</h2>.*?</div>', '', content, flags=re.DOTALL)
# Remove empty separators
new_content = re.sub(r'---\s*\n\s*---', '---', new_content, flags=re.MULTILINE)

with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
    
# Update contribution python script
py_path = 'C:/Users/ander/Downloads/eeguskiza-main/.github/scripts/update-contributions.py'
with open(py_path, 'r', encoding='utf-8') as f:
    py_content = f.read()

# Change USERNAME
py_content = py_content.replace('USERNAME = "eeguskiza"', 'USERNAME = "anderr04"')

# Rewrite to use only last 5 months instead of all years
# We will inject code for grouping by month
# Find the grouping code
# It is:
#    yearly = {}
#    for day in data["contributions"]:
#        year = int(day["date"][:4])
#        yearly[year] = yearly.get(year, 0) + day["count"]

new_grouping = """    from datetime import datetime
    import calendar
    monthly = {}
    for day in data["contributions"]:
        ym = day["date"][:7]
        monthly[ym] = monthly.get(ym, 0) + day["count"]
    
    # Sort and take last 5
    sorted_months = sorted(monthly.items())
    last_5 = dict(sorted_months[-5:])
    
    return last_5"""
    
py_content = re.sub(
    r'    yearly = \{\}.*?return dict\(sorted\(yearly\.items\(\)\)\)',
    new_grouping,
    py_content,
    flags=re.DOTALL
)

# Text replacements for graph labels
py_content = py_content.replace('yearly.keys()', 'monthly.keys()')
py_content = py_content.replace('yearly.values()', 'monthly.values()')
py_content = py_content.replace('def generate_svg(yearly):', 'def generate_svg(monthly):')
py_content = py_content.replace('years = list(yearly.keys())', 'years = list(monthly.keys())')
py_content = py_content.replace('values = list(yearly.values())', 'values = list(monthly.values())')
py_content = py_content.replace('Contributions by Year', 'Contributions - Last 5 Months')
py_content = py_content.replace('contributions since Nov {first_year}', 'contributions in the last 5 months')

with open(py_path, 'w', encoding='utf-8') as f:
    f.write(py_content)
