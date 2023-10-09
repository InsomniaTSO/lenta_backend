import pandas as pd
import numpy as np

def aggregation(pd_cat, pd_sales, pd_forecast):
    sum_col = ['sales_units', 'sales_units_promo']
    pd_sales['fact'] = pd_sales['sales_units']
    pd_sales = pd_sales.drop(columns=['sales_run_promo', 'sales_rub', 'sales_units_promo', 
                                'sales_units', 'sales_type'], axis=1)
    pd_sales = pd_sales.rename(columns={'shop_id': 'store_id'})
    pd_forecast = pd_forecast.drop('forecast_date', axis=1)
    pd_sal_for = pd.merge(pd_forecast, pd_sales, how='left', on=['store_id','product_id', 'date'],
                        left_index=False, right_index=False).fillna(0).drop(columns=['id_y', 'id_x'], axis=1)
    pd_sal_for.fact = pd_sal_for.fact.astype(int)
    pd_sal_for = pd_sal_for.groupby(['store_id', 'product_id']).agg({'target': ['sum'], 'fact': ['sum']}).reset_index()
    pd_sal_for.columns = ['store_id', 'product_id', 'target', 'fact']
    pd_all = pd.merge(pd_sal_for, pd_cat, how='left', on=['product_id'],
                        left_index=False, right_index=False).drop('uom', axis=1)
    pd_all['date_range'] = '[2023-07-05, 2023-07-18]'
    pd_all['delta'] = pd_all['fact'] - pd_all['target']
    pd_all['WAPE'] = np.where(pd_all['fact'] == 0, np.nan, pd_all['delta'] / pd_all['fact'])*100
    pd_all['WAPE'] = pd_all['WAPE'].replace(np.nan, 0).astype(int)
    return pd_all

def aggregation_by_store(pd_all):
    pd_all_gr = pd_all.groupby(['date_range','store_id']).agg({'target': ['sum'], 'fact': ['sum'],
                                                  'delta': ['mean'], 'WAPE': ['mean'],}).reset_index()
    pd_all_gr.columns = ['date_range', 'store_id', 'target', 'fact', 'delta', 'WAPE']
    pd_all_gr['WAPE'] = pd_all_gr['WAPE'].astype(int)
    pd_all_gr['delta'] = pd_all_gr['delta'].astype(int)
    return pd_all_gr