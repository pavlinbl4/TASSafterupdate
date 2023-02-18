from pathlib import Path


def file_exist(path_to_file):
    Path(path_to_file).touch(exist_ok=True)


if __name__ == '__main__':
    print(file_exist('/Users/evgeniy/Pictures/ExportKeywords_UTF8.xlsx'))
