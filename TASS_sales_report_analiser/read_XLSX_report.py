def gen_x(sheet):  # функция определяет номер строки с которой начинается ввод данных в табицу
    for row in sheet.iter_rows():
        for cell in row:
            if cell.value == 'компания' or cell.value == 'Компания':
                return cell.row + 1


def gen_y(sheet):  # функция определяет номер строки с которой начинается ввод данных в таблицу
    for row in sheet.iter_rows():
        for cell in row:
            if cell.value == 'ID фото ' or cell.value == 'ID фото':
                return cell.column
