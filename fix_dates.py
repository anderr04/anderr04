import re

py_path = 'C:/Users/ander/Downloads/eeguskiza-main/.github/scripts/update-contributions.py'
with open(py_path, 'r', encoding='utf-8') as f:
    py_content = f.read()

new_grouping = """    from datetime import datetime
    import calendar
    monthly = {}
    current_ym = datetime.now().strftime('%Y-%m')
    for day in data["contributions"]:
        ym = day["date"][:7]
        if ym > current_ym:
            continue
        monthly[ym] = monthly.get(ym, 0) + day["count"]
    
    # Sort and take last 5
    sorted_months = sorted(monthly.items())
    last_5 = dict(sorted_months[-5:])
    
    return last_5"""

py_content = re.sub(
    r'    from datetime import datetime\n    import calendar\n    monthly = \{\}\n    for day in data\["contributions"\]:\n        ym = day\["date"\]\[:7\]\n        monthly\[ym\] = monthly\.get\(ym, 0\) \+ day\["count"\]\n    \n    # Sort and take last 5\n    sorted_months = sorted\(monthly\.items\(\)\)\n    last_5 = dict\(sorted_months\[-5:\]\)\n    \n    return last_5',
    new_grouping,
    py_content,
    flags=re.DOTALL
)

with open(py_path, 'w', encoding='utf-8') as f:
    f.write(py_content)
print('Updated update-contributions.py')
