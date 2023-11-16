import shutil


def delete_folder(dir_path):
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print(f"Error: {dir_path} : {e.strerror}")


if __name__ == '__main__':
    delete_folder('tass_html')
