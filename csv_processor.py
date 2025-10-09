import pandas as pd
import numpy as np
import re
import logging
from typing import Dict, Any, List, Tuple
from database import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CSVProcessor:
    def __init__(self, database: Database):
        self.db = database
    
    def process_csv(self, file_path: str, table_name: str, upload_mode: str, has_headers: bool = True) -> Dict[str, Any]:
        """
        Process CSV file and upload to database
        
        Args:
            file_path: Path to CSV file
            table_name: Name for the database table
            upload_mode: 'structured' or 'unstructured'
            has_headers: Whether first row contains headers
            
        Returns:
            Dict with processing results
        """
        try:
            # Read CSV file
            if has_headers:
                df = pd.read_csv(file_path)
            else:
                df = pd.read_csv(file_path, header=None)
                # Generate column names
                df.columns = [f'column_{i+1}' for i in range(len(df.columns))]
            
            logger.info(f"Loaded CSV with {len(df)} rows and {len(df.columns)} columns")
            
            # Clean data if unstructured
            if upload_mode == 'unstructured':
                df = self._clean_data(df)
                logger.info("Data cleaning completed")
            
            # Validate and prepare data for database
            df = self._prepare_for_database(df)
            
            # Create table and insert data
            result = self._create_table_and_insert(df, table_name)
            
            return {
                "success": True,
                "table_name": table_name,
                "rows_inserted": len(df),
                "columns": list(df.columns),
                "data_types": {col: str(dtype) for col, dtype in df.dtypes.to_dict().items()},
                "cleaning_applied": upload_mode == 'unstructured',
                "result": result
            }
            
        except Exception as e:
            logger.error(f"CSV processing error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply basic data cleaning and preprocessing
        """
        logger.info("Starting data cleaning process...")
        
        # Make a copy to avoid modifying original
        df_clean = df.copy()
        
        # 1. Handle missing values
        df_clean = self._handle_missing_values(df_clean)
        
        # 2. Clean text data
        df_clean = self._clean_text_data(df_clean)
        
        # 3. Standardize date formats
        df_clean = self._standardize_dates(df_clean)
        
        # 4. Clean numeric data
        df_clean = self._clean_numeric_data(df_clean)
        
        # 5. Remove duplicates
        df_clean = self._remove_duplicates(df_clean)
        
        # 6. Clean column names
        df_clean.columns = self._clean_column_names(df_clean.columns)
        
        logger.info(f"Data cleaning completed. Final shape: {df_clean.shape}")
        return df_clean
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the dataset"""
        logger.info("Handling missing values...")
        
        for column in df.columns:
            if df[column].dtype == 'object':  # Text columns
                # Fill with 'Unknown' for text columns
                df[column] = df[column].fillna('Unknown')
            else:  # Numeric columns
                # Fill with median for numeric columns
                if not df[column].isna().all():
                    median_val = df[column].median()
                    df[column] = df[column].fillna(median_val)
                else:
                    df[column] = df[column].fillna(0)
        
        return df
    
    def _clean_text_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize text data"""
        logger.info("Cleaning text data...")
        
        for column in df.columns:
            if df[column].dtype == 'object':
                # Convert to string and strip whitespace
                df[column] = df[column].astype(str).str.strip()
                
                # Remove extra whitespace
                df[column] = df[column].str.replace(r'\s+', ' ', regex=True)
                
                # Standardize case for common fields
                if any(keyword in column.lower() for keyword in ['status', 'state', 'type', 'category']):
                    df[column] = df[column].str.title()
                
                # Clean special characters
                df[column] = df[column].str.replace(r'[^\w\s\-\.]', '', regex=True)
        
        return df
    
    def _standardize_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize date formats"""
        logger.info("Standardizing date formats...")
        
        date_columns = []
        for column in df.columns:
            if df[column].dtype == 'object':
                # Check if column contains date-like data
                sample_values = df[column].dropna().head(10)
                if len(sample_values) > 0:
                    # Try to parse as dates
                    try:
                        pd.to_datetime(sample_values, errors='raise')
                        date_columns.append(column)
                    except:
                        pass
        
        for column in date_columns:
            try:
                df[column] = pd.to_datetime(df[column], errors='coerce')
                logger.info(f"Converted {column} to datetime")
            except:
                logger.warning(f"Could not convert {column} to datetime")
        
        return df
    
    def _clean_numeric_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean numeric data"""
        logger.info("Cleaning numeric data...")
        
        for column in df.columns:
            if df[column].dtype == 'object':
                # Try to convert to numeric
                try:
                    # Remove common non-numeric characters
                    cleaned = df[column].astype(str).str.replace(r'[^\d\.\-]', '', regex=True)
                    numeric_series = pd.to_numeric(cleaned, errors='coerce')
                    
                    # If more than 50% of values are numeric, convert the column
                    if not numeric_series.isna().sum() / len(numeric_series) > 0.5:
                        df[column] = numeric_series
                        logger.info(f"Converted {column} to numeric")
                except:
                    pass
        
        return df
    
    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows"""
        logger.info("Removing duplicates...")
        initial_rows = len(df)
        df = df.drop_duplicates()
        removed = initial_rows - len(df)
        if removed > 0:
            logger.info(f"Removed {removed} duplicate rows")
        return df
    
    def _clean_column_names(self, columns: List[str]) -> List[str]:
        """Clean column names for database compatibility"""
        logger.info("Cleaning column names...")
        
        cleaned_columns = []
        for col in columns:
            # Convert to lowercase
            clean_col = str(col).lower()
            
            # Replace spaces and special characters with underscores
            clean_col = re.sub(r'[^\w]', '_', clean_col)
            
            # Remove multiple underscores
            clean_col = re.sub(r'_+', '_', clean_col)
            
            # Remove leading/trailing underscores
            clean_col = clean_col.strip('_')
            
            # Ensure column name is not empty and doesn't start with number
            if not clean_col or clean_col[0].isdigit():
                clean_col = f'col_{clean_col}' if clean_col else 'unnamed_column'
            
            # Ensure uniqueness
            original_col = clean_col
            counter = 1
            while clean_col in cleaned_columns:
                clean_col = f"{original_col}_{counter}"
                counter += 1
            
            cleaned_columns.append(clean_col)
        
        return cleaned_columns
    
    def _prepare_for_database(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare DataFrame for database insertion"""
        logger.info("Preparing data for database...")
        
        # Handle infinite values
        df = df.replace([np.inf, -np.inf], np.nan)
        
        # Convert datetime to string for database storage
        for column in df.columns:
            if df[column].dtype == 'datetime64[ns]':
                df[column] = df[column].dt.strftime('%Y-%m-%d %H:%M:%S')
                df[column] = df[column].fillna('')
        
        # Convert NaN to None for database compatibility
        df = df.where(pd.notnull(df), None)
        
        return df
    
    def _create_table_and_insert(self, df: pd.DataFrame, table_name: str) -> str:
        """Create table and insert data"""
        logger.info(f"Creating table {table_name} and inserting data...")
        
        try:
            # Create table
            self.db.create_table_from_dataframe(df, table_name)
            
            # Insert data
            rows_inserted = self.db.insert_dataframe(df, table_name)
            
            logger.info(f"Successfully inserted {rows_inserted} rows into {table_name}")
            return f"Table {table_name} created with {rows_inserted} rows"
            
        except Exception as e:
            logger.error(f"Database operation failed: {e}")
            raise Exception(f"Failed to create table or insert data: {str(e)}")
