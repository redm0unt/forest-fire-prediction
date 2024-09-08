import argparse
import json

team_name = "test_team"


def call_api(lat, lng, date):
    results_dict = {}
    # Здесь должна быть логика для обращения к API
    # ...
    # Возвращаем результаты в виде словаря
    return results_dict


# Функция для сохранения результатов в JSON файл
def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, help="Широта")
    parser.add_argument("--lng", type=float, help="Долгота")
    parser.add_argument("--date", type=str, help="Дата в формате YYYY-MM-DD")
    args = parser.parse_args()

    if not all([args.lat, args.lng, args.date]):
        print("Не все обязательные аргументы предоставлены.")
        parser.print_help()
        exit(1)

    results = call_api(args.lat, args.lng, args.date)
    save_json(results, f'{team_name}.json')
