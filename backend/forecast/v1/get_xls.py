import io
import json
from datetime import datetime

import pandas as pd


def get_xls(data):
    today = datetime.today().strftime('%d-%m-%Y')
    forecasts = json.loads(data)
    forecast_pd = pd.DataFrame()
    for forecast in forecasts:
        temp_forecast_pd = pd.DataFrame.from_dict(forecast)
        forecast_pd = forecast_pd._append(temp_forecast_pd)
    forecast_pd['forecast_to_date'] = forecast_pd.index
    forecast_pd = forecast_pd.loc[:,['store','sku','forecast_date', 
                                    'forecast_to_date', 'forecast']]
    forecast_pd.rename(columns={'store': 'ТК', 'sku': 'Товар',
                                            'forecast_date': 'Дата прогноза', 'forecast_to_date': 'Прогноз на дату',
                                            'forecast': 'Прогноз'}, inplace=True)
    buffer = io.BytesIO()
    writer = pd.ExcelWriter(buffer, engine='xlsxwriter')   
    forecast_pd.to_excel(writer, sheet_name='forecast', index=False)
    workbook  = writer.book
    worksheet = writer.sheets['forecast']
    worksheet.autofilter('A1:D1')
    worksheet.set_column(0, 1, 50)
    worksheet.set_column(2, 3, 20)
    worksheet.set_column(4, 4, 10)
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '003C96',
        'font_color': 'FFB900',
        'font_size' : 13,
        'border': 1})
    for col_num, value in enumerate(forecast_pd.columns.values):
        worksheet.write(0, col_num, value, header_format)
    writer.close()
    return buffer