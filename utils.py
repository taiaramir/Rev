import pandas as pd

def format_value(value, is_currency=False):
    if isinstance(value, (int, float)):
        value = int(value)
        formatted = f"{value:,}"
        if is_currency:
            return f"${formatted}"
        return formatted
    return value

def create_styled_dataframe(yearly_data):
    df_data = []
    for year_data in yearly_data:
        year = year_data['Year']
        df_data.extend([
            {'Item': f'Year {year} - Customers', 'Basic': format_value(year_data['Customers']['Basic']), 'Pro': format_value(year_data['Customers']['Pro']), 'Enterprise': format_value(year_data['Customers']['Enterprise'])},
            {'Item': f'Year {year} - Users', 'Basic': format_value(year_data['Users']['Basic']), 'Pro': format_value(year_data['Users']['Pro']), 'Enterprise': format_value(year_data['Users']['Enterprise'])},
            {'Item': f'Year {year} - Subscription Revenue', 'Basic': format_value(year_data['Subscription Revenue']['Basic'], True), 'Pro': format_value(year_data['Subscription Revenue']['Pro'], True), 'Enterprise': format_value(year_data['Subscription Revenue']['Enterprise'], True)},
            {'Item': f'Year {year} - Number of Workspaces', 'Basic': format_value(year_data['Number of Workspaces']['Basic']), 'Pro': format_value(year_data['Number of Workspaces']['Pro']), 'Enterprise': format_value(year_data['Number of Workspaces']['Enterprise'])},
            {'Item': f'Year {year} - Workspace Revenue', 'Basic': format_value(year_data['Workspace Revenue']['Basic'], True), 'Pro': format_value(year_data['Workspace Revenue']['Pro'], True), 'Enterprise': format_value(year_data['Workspace Revenue']['Enterprise'], True)},
            {'Item': f'Year {year} - Total Revenue', 'Basic': format_value(year_data['Total Revenue']['Basic'], True), 'Pro': format_value(year_data['Total Revenue']['Pro'], True), 'Enterprise': format_value(year_data['Total Revenue']['Enterprise'], True)}
        ])
    
    # Add total row
    total_row = {'Item': 'Total', 'Basic': 0, 'Pro': 0, 'Enterprise': 0}
    for plan in ['Basic', 'Pro', 'Enterprise']:
        total_row[plan] = sum(year_data['Total Revenue'][plan] for year_data in yearly_data)
    df_data.append({
        'Item': 'Total',
        'Basic': format_value(total_row['Basic'], True),
        'Pro': format_value(total_row['Pro'], True),
        'Enterprise': format_value(total_row['Enterprise'], True)
    })
    
    df = pd.DataFrame(df_data)
    
    def style_dataframe(s):
        if 'Year' in s['Item']:
            year = int(s['Item'].split()[1])
            if year % 2 == 1:
                return ['background-color: #f0f0f0; color: black'] * len(s)  # Light gray for odd years
            else:
                return ['background-color: #e0e0e0; color: black'] * len(s)  # Slightly darker gray for even years
        elif s['Item'] == 'Total':
            return ['background-color: #333333; color: white'] * len(s)  # Dark color with white text for total
        else:
            return [''] * len(s)

    styled_df = df.style.apply(style_dataframe, axis=1)
    
    return styled_df