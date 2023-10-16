import string
from pathlib import Path
import shutil
import sys

def normalize(string_):
    transliteration_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g',
        'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
        'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l',
        'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'eh', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G',
        'Д': 'D', 'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh',
        'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L',
        'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts',
        'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '', 'Ы': 'Y', 'Ь': '',
        'Э': 'Eh', 'Ю': 'Yu', 'Я': 'Ya',
    }
    c = string_.rfind('.')
    d = string_[:c]
    new_string = ''
    for i in d:
        if i in transliteration_dict.keys():
            new_string += transliteration_dict[i]
        elif i.isdigit():
            new_string += i
        elif i in string.ascii_letters:
            new_string += i
        elif i == '.':
            new_string+='_'
        else:
            new_string+='_'
    new_string+=string_[c:]
    return new_string


def recursion_file(file):
    file_iter=Path(file)
    categories = {'images':[], 'video':[], 'audio':[], 'documents':[], 'archives':[]}
    known_extensions = {
        'images': ('.jpeg', '.png', '.jpg', '.svg'),
        'video': ('.avi', '.mp4', '.mov', '.mkv'),
        'audio': ('.mp3', '.ogg', '.wav', '.amr'),
        'documents': ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
        'archives': ('.zip', '.gz', '.tar'),
    }
    known_file= set()
    unknown_file= set()
    #рекурсивно обходим все папки и файлы
    for i in file_iter.glob("**/*"):
        category = False
        if i.is_dir():
            #если папка пустая удаляем её
            if not list(i.iterdir()):
                shutil.rmtree(i)
                #сли это файл то проверяем на наличие его разрешения в словаре
        if i.is_file():
            for dir, type in known_extensions.items():
                #Создаем папку по ключу словаря и переносим файл туда также переносим i.suffix в known_file
                if i.suffix in type:
                    new_dir = file_iter / dir
                    new_dir.mkdir(parents=True, exist_ok=True)
                    i.rename(new_dir / normalize(i.name))
                    known_file.add(i.suffix)
                    categories.get(dir,[]).append(i.name)
                    category=True
                    break
            if not category:
                unknown_file.add(i.suffix)


    #Проверяем есть ли папка 'archives'
    zips=Path(file_iter/'archives')
    if zips.is_dir():
        new_zips_file=zips/'archives'
        new_zips_file.mkdir(parents=True,exist_ok=True)
        #Итерируемся по содержимому папки 'archives'
        # Делаем распаковку
        for i in zips.iterdir():
            if i.suffix in known_extensions['archives']:
                shutil.unpack_archive(i,new_zips_file)
    #Проходим рекурсией по папкам и если они пустые то удаляем их если нет меняем имя
    for i in file_iter.glob('**/*'):
        if i.is_dir() and not list(i.iterdir()) and i.name not in known_extensions.keys():
            shutil.rmtree(i)
        else:
            new_name = normalize(i.name)
            i.rename(i.with_name(new_name))
    #Получаем список файлов по категориям
    for i, j in categories.items():
        print(i,j)
    print(f'Список всех известных расширений:{list(known_file)}')
    print(f'Список всех не известных расширений:{list(unknown_file)}')

def main():
    if len(sys.argv) > 1:
        target_directory = sys.argv[1]
        recursion_file(target_directory)
    else:
        print("Укажите путь к целевой папке в аргументах командной строки.")
if __name__ == "__main__":
    main()
