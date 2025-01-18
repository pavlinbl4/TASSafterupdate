#  encoding="cp1251"

def read_html(offline_html, encoding='utf-8'):
    try:
        with open(offline_html, 'r', encoding=encoding) as input_file:
            return input_file.read()
    except FileNotFoundError:
        print(f'Error: file {offline_html} was not found')
        return None
    except IOError as e:
        print(f"Error: An I/O error occurred while reading the file: {e}")
        return None



