import yaml
import pandas as pd

# Load the input YAML file
with open("input.yml", "r") as file:
    data = yaml.safe_load(file)

# Load the Excel file with mapping data
df = pd.read_excel("mapping.xlsx")

# Clear any existing sections explicitly
data = {key: value for key, value in data.items() if key not in ["SalesForceCustomerID", "SalesForceCustomerName"]}

# Define new sections
salesforce_customer_id_section = {
    "Name": "Salesforce Customer ID",
    "Source": "User:Defined:FullTenantCost",
    "Rules": []
}

salesforce_customer_name_section = {
    "Name": "Salesforce Customer Name",
    "Child": "User:Defined:K8TenantIDAggregate",
    "Source": "User:Defined:FullTenantCost",
    "Rules": []
}

# Populate the new sections with data
for _, row in df.iterrows():
    tenant_ids = [tid.strip() for tid in str(row["TENANTID"]).split(",") if pd.notna(row["TENANTID"])]
    
    # Add Salesforce Customer ID rules
    if pd.notna(row["SALESFORCECUSTOMERID"]):
        rule_id = {
            "Type": "Group",
            "Name": row["SALESFORCECUSTOMERID"],
            "Conditions": [{"Equals": tenant_ids}],
        }
        # Prevent duplicate rules
        if rule_id not in salesforce_customer_id_section["Rules"]:
            salesforce_customer_id_section["Rules"].append(rule_id)
    
    # Add Salesforce Customer Name rules
    if pd.notna(row["SALESFORCECUSTOMERNAME"]):
        rule_name = {
            "Type": "Group",
            "Name": row["SALESFORCECUSTOMERNAME"],
            "Conditions": [{"Equals": tenant_ids}],
        }
        # Prevent duplicate rules
        if rule_name not in salesforce_customer_name_section["Rules"]:
            salesforce_customer_name_section["Rules"].append(rule_name)

# Add the new sections to the YAML data
data["SalesForceCustomerID"] = salesforce_customer_id_section
data["SalesForceCustomerName"] = salesforce_customer_name_section

# Save the updated YAML file
with open("output2234.yml", "w") as file:
    yaml.dump(data, file, default_flow_style=False, sort_keys=False, width=1000)

print("Updated YAML file saved as output2.yml.")