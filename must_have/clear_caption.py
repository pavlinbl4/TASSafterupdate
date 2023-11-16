import re


def clear_author(text_str):
    pattern = r"Фото ИТАР-ТАСС/ Семен Лиходеев"
    return re.sub(pattern, '', text_str)


if __name__ == '__main__':
    example_text_str = ('Портретура Россия. Москва. '
                        'Актриса Инна Чурикова во время пресс-конференции артистов театра "Ленком" в ДК "Выборгский". '
                        'Фото ИТАР-ТАСС/ Семен Лиходеев')

    print(clear_author(example_text_str))
