from pathlib import Path


def subfolder_in_user_folder(subfolder):
    return f'{Path.home()}/{subfolder}'


if __name__ == '__main__':
    print(subfolder_in_user_folder("Downloads/RRRRRRR"))
