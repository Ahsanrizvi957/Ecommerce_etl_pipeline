from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from config.database import get_database_engine
from extract import extract_customers,extract_products,extract_sales,extract_location,extract_category,extract_additional_customers
from transform import transform_customers,transform_products,transform_sales,transform_location,transform_category,transform_additional_customers
from load import create_audit_table, load_with_audit

def run_pipeline():

    load_dotenv(PROJECT_ROOT / ".env")

    print("starting pipeline")

#Extract

    customers_raw = extract_customers()
    products_raw = extract_products()
    sales_raw = extract_sales()
    location_raw = extract_location()
    category_raw = extract_category()
    additional_customers_raw = extract_additional_customers()

    print(
    f"Extracted customers {len(customers_raw):,} rows\n"
    f"Extracted products {len(products_raw):,} rows\n"
    f"Extracted sales {len(sales_raw):,} rows\n"
    f"transformed location: {len(location_raw):,} rows\n"
    f"Extracted category {len(category_raw):,} rows\n"
    f"Extracted additional customers {len(additional_customers_raw):,} rows\n")
# Transform
    cleaned_customers = transform_customers(customers_raw)
    cleaned_products = transform_products(products_raw)
    cleaned_sales = transform_sales(sales_raw)
    cleaned_location = transform_location(location_raw)
    cleaned_category = transform_category(category_raw)
    cleaned_additional_customers = transform_additional_customers(additional_customers_raw)

    print(
        f"transformed customers: {len(cleaned_customers):,} rows\n"
        f"transformed products: {len(cleaned_products):,} rows\n"
        f"transformed sales: {len(cleaned_sales):,} rows\n"
        f"transformed category: {len(cleaned_category):,} rows\n"
        f"transformed location: {len(cleaned_location):,} rows\n"
        f"transformed additional customers: {len(cleaned_additional_customers):,} rows\n"
        )
#load

    engine = get_database_engine()

    try:
        create_audit_table(engine)
        
        load_with_audit(cleaned_customers,"customers",engine,"stagging")
        load_with_audit(cleaned_products,"products",engine,"stagging")
        load_with_audit(cleaned_sales,"sales",engine,"stagging")
        load_with_audit(cleaned_location,"location",engine,"stagging")
        load_with_audit(cleaned_category,"category",engine,"stagging")
        load_with_audit(cleaned_additional_customers,"additonal_customers",engine,"stagging")
    finally:
        engine.dispose()

        print("pipeline successfully loaded")

if __name__ == "__main__":
    run_pipeline()
  
