import os.path


def create_directory(path_to_dir: str, sub_dir_name: str) -> str:
    new_path = f'{path_to_dir}/{sub_dir_name}'
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    return new_path


if __name__ == '__main__':
    print(create_directory("..", 'tass_html'))
