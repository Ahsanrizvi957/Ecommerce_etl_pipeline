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
