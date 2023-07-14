from pathlib import Path


def make_documents_subfolder(name):  # create folder "name" in User/Documents folder
    (Path.home() / "Documents" / f"{name}").mkdir(parents=True, exist_ok=True)
    return Path.home() / "Documents" / f"{name}"


if __name__ == '__main__':
    make_documents_subfolder('Begemot/crocodile/fox')
