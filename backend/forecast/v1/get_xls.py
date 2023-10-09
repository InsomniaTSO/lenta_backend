import io
import json
import pandas as pd
from datetime import datetime


def get_xls(data):
    today = datetime.today().strftime('%d-%m-%Y')
    forecasts = json.loads(data)
    forecast_pd = pd.DataFrame()
    for forecast in forecasts:
        temp_forecast_pd = pd.DataFrame.from_dict(forecast)
        forecast_pd = pd.concat([forecast_pd, temp_forecast_pd])
    forecast_pd['forecast_to_date'] = forecast_pd.index
    forecast_pd.rename(columns={'store': 'ТК', 'group': 'Товарная группа',
                                'category': 'Товарная категория',
                                'subcategory': 'Товарная подкатегория',
                                'sku': 'Товар', 'uom': 'Продажа на вес',
                                'forecast_date': 'Дата прогноза',
                                'forecast_to_date': 'Прогноз на дату',
                                'forecast': 'Прогноз'}, inplace=True)
    forecast_pd = forecast_pd.reindex(
        columns=['ТК', 'Товарная группа', 'Товарная категория',
                 'Товарная подкатегория', 'Товар',
                 'Продажа на вес', 'Дата прогноза',
                 'Прогноз на дату', 'Прогноз']
    )
    buffer = io.BytesIO()
    writer = pd.ExcelWriter(buffer, engine='xlsxwriter')
    forecast_pd.to_excel(writer, sheet_name='forecast', index=False)
    workbook = writer.book
    worksheet = writer.sheets['forecast']
    worksheet.autofilter('A1:G1')
    worksheet.set_column(0, 4, 40)
    worksheet.set_column(5, 7, 20)
    worksheet.set_column(8, 8, 10)
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'center',
        'fg_color': '003C96',
        'font_color': 'FFB900',
        'font_size': 13,
        'border': 1})
    forecast_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'fg_color': '88d7f2',
        'font_color': '000000',
        'border': 1})
    for col_num, value in enumerate(forecast_pd.columns.values):
        worksheet.write(0, col_num, value, header_format)
    worksheet.set_column('I:I', None, forecast_format)
    worksheet.freeze_panes(1, 0)
    writer.close()
    return buffer


def get_quality_xls(forecast_pd):
    forecast_pd.rename(columns={'store_id': 'ТК', 'group_id': 'Товарная группа',
                                'category_id': 'Товарная категория',
                                'subcategory_id': 'Товарная подкатегория',
                                'product_id': 'Товар', 'target': 'Прогноз',
                                'fact': 'Факт', 
                                'date_range': 'Прогноз на даты',
                                'delta': 'Прогноз - Факт',
                                'WAPE': 'WAPE'}, inplace=True)
    forecast_pd = forecast_pd.reindex(columns=['Прогноз на даты', 'ТК', 'Товарная группа', 
                                               'Товарная категория', 'Товарная подкатегория', 
                                               'Товар', 'Факт', 'Прогноз',
                                               'Прогноз - Факт', 'WAPE'])
    buffer = io.BytesIO()
    writer = pd.ExcelWriter(buffer, engine='xlsxwriter')   
    forecast_pd.to_excel(writer, sheet_name='forecast', index=False)
    workbook  = writer.book
    worksheet = writer.sheets['forecast']
    worksheet.autofilter('A1:F1')
    worksheet.set_column(0, 5, 40)
    worksheet.set_column(6, 9, 10)
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'center',
        'fg_color': '003C96',
        'font_color': 'FFB900',
        'font_size' : 13,
        'border': 1})
    for col_num, value in enumerate(forecast_pd.columns.values):
        worksheet.write(0, col_num, value, header_format)
    worksheet.freeze_panes(1, 0)
    writer.close()
    return buffer
