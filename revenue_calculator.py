import math

def calculate_revenue(customers, avg_employees, user_percentages, growth_rates, churn_rates,
                      base_price, prices_per_user, workspace_cost, workspace_percentages, months):
    yearly_data = []
    total_revenue = 0
    for year in range(1, (months // 12) + 1):
        year_end = min(year * 12, months)
        year_start = (year - 1) * 12
        year_months = year_end - year_start
        
        year_data = {'Year': year, 'Customers': {}, 'Users': {}, 'Subscription Revenue': {}, 'Number of Workspaces': {}, 'Workspace Revenue': {}, 'Total Revenue': {}}
        
        for plan in customers.keys():
            current_customers = customers[plan] * ((1 + growth_rates[plan] - churn_rates[plan]) ** year_start)
            year_data['Customers'][plan] = round(current_customers)
            
            users = current_customers * avg_employees[plan] * user_percentages[plan]
            year_data['Users'][plan] = round(users)
            
            plan_subscription_revenue = 0
            plan_workspace_revenue = 0
            
            for _ in range(year_months):
                subscription_revenue = (current_customers * base_price) + (users * prices_per_user[plan])
                workspaces = math.ceil(users * workspace_percentages[plan])
                workspace_revenue = workspaces * workspace_cost
                
                plan_subscription_revenue += subscription_revenue
                plan_workspace_revenue += workspace_revenue
                
                current_customers *= (1 + growth_rates[plan] - churn_rates[plan])
                users = current_customers * avg_employees[plan] * user_percentages[plan]
            
            year_data['Subscription Revenue'][plan] = round(plan_subscription_revenue, 2)
            year_data['Number of Workspaces'][plan] = round(workspaces)
            year_data['Workspace Revenue'][plan] = round(plan_workspace_revenue, 2)
            year_data['Total Revenue'][plan] = round(plan_subscription_revenue + plan_workspace_revenue, 2)
        
        yearly_data.append(year_data)
        total_revenue += sum(year_data['Total Revenue'].values())
    
    return total_revenue, yearly_data