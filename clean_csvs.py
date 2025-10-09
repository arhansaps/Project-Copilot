import pandas as pd

def clean_csv(input_path, output_path, date_cols, extra_processing=None):
    df = pd.read_csv(input_path, on_bad_lines='skip')  # Skip truncated/bad lines
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce').dt.strftime('%Y-%m-%d')
    if extra_processing:
        extra_processing(df)
    df.to_csv(output_path, index=False)

# Production CSV
clean_csv('Updated mines production data by date by equipment.csv', 'production_cleaned.csv', ['Date'])

# Status Logs CSV (compute durations, datetimes)
def status_extra(df):
    if 'duration_minutes' in df.columns:
        df['duration_seconds'] = df['duration_minutes'] * 60
        df['duration_formatted'] = pd.to_timedelta(df['duration_seconds'], unit='s').apply(lambda x: str(x)[-8:])
    if 'start_date' in df.columns and 'start_time' in df.columns:
        df['start_time'] = pd.to_datetime(df['start_date'] + ' ' + df['start_time'], errors='coerce').dt.strftime('%Y-%m-%d %H:%i:%s')
    if 'end_date' in df.columns and 'end_time' in df.columns:
        df['end_time'] = pd.to_datetime(df['end_date'] + ' ' + df['end_time'], errors='coerce').dt.strftime('%Y-%m-%d %H:%i:%s')
    if 'time_created_at' in df.columns:
        df['time_created_at'] = pd.to_datetime(df['time_created_at'], format='%H.%M.%S', errors='coerce').dt.strftime('%H:%M:%s')

clean_csv('equipment_status_logs_rows_cleaned_v5.csv', 'status_logs_cleaned.csv', 
          ['date', 'start_date', 'end_date', 'date_created_at'], status_extra)

# Daily Summary CSV
clean_csv('cleaned_data_by_date.csv', 'daily_summary_cleaned.csv', ['Date'])