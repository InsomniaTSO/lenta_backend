import csv

def load_ids_from_csv(file_path, column_name):
    """Загружает уникальные ID из указанной колонки CSV файла."""
    with open(file_path, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return {row[column_name] for row in reader}

def main():
    # Загрузка ID из forecast.csv
    forecast_st_ids = load_ids_from_csv('sales_submission.csv', 'st_id')
    forecast_pr_sku_ids = load_ids_from_csv('sales_submission.csv', 'pr_sku_id')

    # Загрузка ID из других CSV файлов (предполагается, что у вас есть два файла: shops.csv и products.csv)
    other_st_ids = load_ids_from_csv('st_df.csv', 'st_id')
    other_pr_sku_ids = load_ids_from_csv('pr_df.csv', 'pr_sku_id')

    # Находим отсутствующие ID
    missing_st_ids = forecast_st_ids - other_st_ids
    missing_pr_sku_ids = forecast_pr_sku_ids - other_pr_sku_ids

    # Вывод результатов
    if missing_st_ids:
        print("Отсутствующие st_id из forecast.csv:")
        for id in missing_st_ids:
            print(id)

    if missing_pr_sku_ids:
        print("\nОтсутствующие pr_sku_id из forecast.csv:")
        for id in missing_pr_sku_ids:
            print(id)

if __name__ == "__main__":
    main()