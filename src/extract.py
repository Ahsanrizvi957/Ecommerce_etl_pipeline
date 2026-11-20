import pandas as pd
from pathlib import Path

# project source directory

PROJECT_ROOT = Path(__file__).resolve().parent.parent
print(PROJECT_ROOT)

# files location

RAW_DATA_DIR = PROJECT_ROOT/ "data" / "raw"

# this function create and read file path and returns a dataframe to extract_csv
def extract_csv(file_name):

    file_path = RAW_DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"source file not found: {file_path}") 

    return pd.read_csv(file_path)


def extract_customers():
  return extract_csv("cust_info.csv")

def extract_products():
   return extract_csv("prd_info.csv")

def extract_sales():
   return extract_csv("sales_details.csv")

def extract_category():
   return extract_csv("PX_CAT_G1V2.csv")

def extract_location():
   return extract_csv("LOC_A101.csv")

def extract_additional_customers():
   return extract_csv("CUST_AZ12.csv")
