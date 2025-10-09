import mysql.connector
import pandas as pd
from datetime import datetime

# Database connection params
db_params = {
    'host': '127.0.0.1',       # MySQL container host
    'port': 3307,              # MySQL container port
    'user': 'root',
    'password': 'rootpass',
    'database': 'MiningAndFactoryData'
}

# File paths (adjust if necessary)
logs_file = '/home/hackysapy/M_ops/ops_copilot/Cleaned Datasets/equipment_status_logs_rows_cleaned_v5.csv'
shift_file = '/home/hackysapy/M_ops/ops_copilot/Cleaned Datasets/cleaned_data_by_date.csv'
prod_file = '/home/hackysapy/M_ops/ops_copilot/Cleaned Datasets/Updated mines production data by date by equipment.csv'

# Table mapping
tables = {
    'logs': 'Factory_Equipment_Logs',
    'shift': 'Mining_Shift_Data',
    'prod': 'Mining_Production_Site'
}

# Convert DD/MM/YYYY to YYYY-MM-DD
def convert_date(date_str):
    if pd.isna(date_str) or date_str == '' or date_str is None:
        return None
    try:
        dt = datetime.strptime(str(date_str), '%d/%m/%Y')
        return dt.strftime('%Y-%m-%d')
    except:
        try:
            dt = datetime.strptime(str(date_str), '%Y-%m-%d')
            return dt.strftime('%Y-%m-%d')
        except:
            return None

# Convert HH.MM.SS to HH:MM:SS
def convert_time(time_str):
    if pd.isna(time_str) or time_str == '' or time_str is None:
        return None
    try:
        return str(time_str).replace('.', ':')
    except:
        return None

# Read CSVs
print("Reading CSV files...")
logs = pd.read_csv(logs_file)
shift = pd.read_csv(shift_file)
prod = pd.read_csv(prod_file)

# Process Factory_Equipment_Logs
print("Processing Factory_Equipment_Logs...")
date_columns_logs = ['date', 'start_date', 'end_date', 'date_created_at']
for col in date_columns_logs:
    if col in logs.columns:
        logs[col] = logs[col].apply(convert_date)

time_columns_logs = ['start_time', 'end_time', 'time_created_at']
for col in time_columns_logs:
    if col in logs.columns:
        logs[col] = logs[col].apply(convert_time)

# Process Mining_Shift_Data
print("Processing Mining_Shift_Data...")
if 'Date' in shift.columns:
    shift['Date'] = shift['Date'].apply(convert_date)

# Rename columns to match table schema
shift = shift.rename(columns={
    'Trip Count for Mining': 'Trip_Count_for_Mining',
    'Trip Count for Reclaim': 'Trip_Count_for_Reclaim',
    'Total Trips': 'Total_Trips',
    'Qty (m3)': 'Qty_m3',
    'Qty m3': 'Qty_m3'
})

# Process Mining_Production_Site
print("Processing Mining_Production_Site...")
if 'Date' in prod.columns:
    prod['Date'] = prod['Date'].apply(convert_date)

# Rename columns to match table schema
prod = prod.rename(columns={
    'Mining_Bench': 'MiningBench',
    'Mining Bench': 'MiningBench',
    'Excavator_ID': 'ExcavatorID',
    'Excavator ID': 'ExcavatorID',
    'Asset_Name': 'Asset_Name',
    'Asset Name': 'Asset_Name',
    'No_of_Trips': 'No_of_Trips',
    'No of Trips': 'No_of_Trips',
    'Production_Per_Trip': 'Production_Per_Trip',
    'Production Per Trip': 'Production_Per_Trip'
})

# Replace NaN with None
logs = logs.where(pd.notnull(logs), None)
shift = shift.where(pd.notnull(shift), None)
prod = prod.where(pd.notnull(prod), None)

# Connect to MySQL
conn = mysql.connector.connect(**db_params)
cursor = conn.cursor()

# Function to insert a DataFrame into a table
def insert_dataframe(df, table):
    columns = df.columns.tolist()
    placeholders = ', '.join(['%s'] * len(columns))
    colnames = ', '.join([f'`{c}`' for c in columns])
    insert_sql = f'INSERT INTO {table} ({colnames}) VALUES ({placeholders})'
    
    success_count = 0
    error_count = 0
    
    for i, row in enumerate(df.itertuples(index=False, name=None)):
        try:
            values = [None if (v is None or (isinstance(v, float) and pd.isna(v))) else v for v in row]
            cursor.execute(insert_sql, values)
            success_count += 1
            
            if (i + 1) % 100 == 0:
                conn.commit()
                print(f"  Progress: {i+1}/{len(df)} rows")
        except Exception as e:
            error_count += 1
            if error_count <= 5:
                print(f"  Error row {i}: {e}")
            continue
    
    conn.commit()
    print(f"  ✓ Completed: {success_count} inserted, {error_count} failed\n")

# Insert data
print("\n=== Inserting Factory_Equipment_Logs ===")
insert_dataframe(logs, tables['logs'])

print("=== Inserting Mining_Shift_Data ===")
insert_dataframe(shift, tables['shift'])

print("=== Inserting Mining_Production_Site ===")
insert_dataframe(prod, tables['prod'])

# Close connection
cursor.close()
conn.close()
print('✓ All data import complete!')
