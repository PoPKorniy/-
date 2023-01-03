import os
from pathlib import Path
import sys
import shutil
import re
from zipfile import ZipFile

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

name_folders = {
    'images': ('.jpeg', '.png', '.jpg', '.svg'),
    'video': ('.avi', '.mp4', '.mov', '.mkv'),
    'documents': ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
    'audio': ('.mp3', '.ogg', '.wav', '.amr'),
    'archives': ('.zip', '.gz', '.tar'),
    'unknown': ()
}

count = 0


def normalize(string):
    new_string = string.translate(TRANS)
    for i in new_string:
        if not re.search('[a-z A-Z0-9]', i):
            b = new_string.split(i)
            new_string = "_".join(b)
    return  new_string


def sort_folder(path_folder):
    list_path_subfolder = list(path_folder.iterdir())
    if not list_path_subfolder:
        return
    else:
        for file_folder in list_path_subfolder:
            if file_folder.is_dir():
                sort_folder(file_folder)
            else:
                sort_files(file_folder)
    return


def sort_files(path_file):
    name, ext = path_file.stem, path_file.suffix
    global count
    count += 1

    if ext in name_folders['images']:
        new_path = os.path.join(path_start_folder, 'images')

    elif ext in name_folders['video']:
        new_path = os.path.join(path_start_folder, 'video')

    elif ext in name_folders['documents']:
        new_path = os.path.join(path_start_folder, 'documents')

    elif ext in name_folders['audio']:
        new_path = os.path.join(path_start_folder, 'audio')

    elif ext in name_folders['archives']:
        new_path = Path(os.path.join(path_start_folder, 'archives'))
        with ZipFile(path_file, 'r') as zObject:
            zObject.extractall(new_path)

    else:
        new_path = os.path.join(path_start_folder, 'unknown')

    norma_name = normalize(name)

    new_name = f'{norma_name}{ext}'
    new_path_name = os.path.join(new_path, new_name)

    try:
        path_file.rename(new_path_name)
    except:
        new_name = f'{norma_name}_{count}{ext}'
        new_path_name = Path(os.path.join(new_path, new_name))
        path_file.rename(new_path_name)



path_start_folder = Path(sys.argv[-1])


if __name__ == "__main__":
    if not path_start_folder.exists():
        print('[-] Такої директорії не існує')
    else:
        list_path_first = path_start_folder.iterdir()

        for new_folder in name_folders:
            path_new_dir = os.path.join(path_start_folder, new_folder)
            if not os.path.exists(path_new_dir):
                os.makedirs(path_new_dir)

        for any_path in list_path_first:

            if any_path.is_dir():
                sort_folder(any_path)
                if any_path.name in name_folders:
                    continue
                else:
                    shutil.rmtree(any_path)
            else:
                sort_files(any_path)

        list_sort_done = path_start_folder.iterdir()
        print('Сортування пройшло успішно!')


