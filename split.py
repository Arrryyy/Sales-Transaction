import pandas as pd

file_path = r"C:\Users\aryan\Desktop\SalesTransaction\sales_transaction.csv"

def load_and_transform_data(file_path):
    df = pd.read_csv(file_path)
    df_long = pd.melt(df, id_vars=['Product_Code'], var_name='Week', value_name='Sales')
    df_long['Week'] = df_long['Week'].str.extract('(\d+)').astype(int)
    return df_long

def split_data(df_long, train_size=0.8):
    # Assuming the data is already sorted by 'Product_Code' and 'Week'
    unique_products = df_long['Product_Code'].unique()
    train_data = pd.DataFrame()
    test_data = pd.DataFrame()
    
    for product in unique_products:
        product_data = df_long[df_long['Product_Code'] == product]
        cutoff = int(len(product_data) * train_size)
        train_data = pd.concat([train_data, product_data.iloc[:cutoff]])
        test_data = pd.concat([test_data, product_data.iloc[cutoff:]])
    
    return train_data, test_data

df_long = load_and_transform_data(file_path)
train_df, test_df = split_data(df_long)
train_df.to_csv('train_data.csv', index=False)
test_df.to_csv('test_data.csv', index=False)