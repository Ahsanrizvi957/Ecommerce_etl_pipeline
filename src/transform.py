import pandas as pd

# This function clean text columns for every dataframe which contains text data type
def clean_text_columns(df):
    result = df.copy()
    text_columns = df.select_dtypes(include = ['object','string']).columns
    for col in text_columns:
        result[col] = result[col].str.strip()
        result[col] = result[col].replace("",pd.NA)
    return result

def transform_customers(df):
    result = clean_text_columns(df)
    result = result.dropna(subset = ['cst_id'])
    result['cst_create_date'] = pd.to_datetime(result['cst_create_date'], errors = 'coerce')
    result = result.sort_values(by = 'cst_create_date' ,ascending = False)
    result = result.drop_duplicates(subset = ['cst_id'], keep = 'first')
    marital_map = ({'M':'Married','S': 'Single'})
    result['cst_marital_status'] = result['cst_marital_status'].str.upper().map(marital_map).fillna('n/a')
    gender_map = ({'M':'Male','F':'Female'})
    result['cst_gndr'] = result['cst_gndr'].str.upper().map(gender_map).fillna('n/a')
    result['cst_id'] = result['cst_id'].astype('int')
    
    return result.reset_index(drop = True)



def transform_products(df):
    result = clean_text_columns(df)
    result['cat_id'] = result['prd_key'].str[:5].str.replace('-','_')
    result['prd_key'] = result['prd_key'].str[6:]
    result['prd_cost'] = result['prd_cost'].fillna(0)
    line_map = ({
        'R':'Road',
        'S':'other sales',
        'M':'Mountain',
        'T':'Tourung'
    })
    result['prd_line'] = result['prd_line'].str.upper().map(line_map).fillna('n/a')
    result['prd_start_dt'] = pd.to_datetime(result['prd_start_dt'], errors = 'coerce')
    result['prd_end_dt'] = pd.to_datetime(result['prd_end_dt'], errors = 'coerce')
    result['prd_end_dt'] = result.groupby('prd_key')['prd_start_dt'].shift(-1) - pd.Timedelta(days = 1)
    return result.reset_index(drop = True)


def transform_sales(df):
    result = clean_text_columns(df)
    date_columns = ['sls_order_dt','sls_ship_dt','sls_due_dt']
    for columns in date_columns:
       result[columns] = result[columns].astype(str)
       result.loc[(result[columns] == '0')|(result[columns].str.len() != 8),columns] = pd.NA
       result[columns] = pd.to_datetime(result[columns], format = "%Y%m%d", errors = 'coerce')
    
    original_sales = result['sls_sales'].copy()
    calculated_sales = result['sls_quantity'] * result['sls_price'].abs()
    
    result.loc[
        
        (result['sls_sales'] <= 0) | (result['sls_sales'].isna()) | (result['sls_sales'] != calculated_sales),'sls_sales'
        
        ] = calculated_sales

    calculated_price = calculated_sales / result['sls_quantity'].replace(0,float ('nan'))

    result.loc[
        
        (result['sls_price'] <= 0) | (result['sls_price'].isna()) | (result['sls_price'] != calculated_price), 'sls_price'
        
        ] = calculated_price



    return result.reset_index(drop = True)

def transform_category(df):
    
    result = clean_text_columns(df)

    return result.reset_index(drop = True)

def transform_location(df):
    result = clean_text_columns(df)
    result['CID'] = result['CID'].str.replace('-','')
    
    country_map = ({
        'US':'United States',
        'USA':'United States',
        'DE':'Germany',
        '':'n/a'
    })
    result['CNTRY'] = result['CNTRY'].str.upper().map(country_map).fillna(result['CNTRY'])

    return result.reset_index(drop = True)

def transform_additional_customers(df):
    result = clean_text_columns(df)
    mask = result['CID'].str.startswith('NAS')
    result.loc[mask,'CID'] = result.loc[mask,'CID'].str[3:]
    result['BDATE'] = pd.to_datetime(result['BDATE'], errors = 'coerce')
    result.loc[result['BDATE']> pd.Timestamp.today(),'BDATE'] = pd.NaT
    gender_map = ({
        'F':'Female',
        'M':'Male',
        'MALE':'Male',
        'FEMALE':'Female',
        '':'n/a'
    })
    result['GEN'] = result['GEN'].str.upper().map(gender_map).fillna('n/a')
    return result.reset_index(drop = True)

