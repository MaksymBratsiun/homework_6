import pathlib
import shutil
import sys


def normalize(name):

    cyrillic_trans = {  1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G', 1076: 'd', 1044: 'D', 1077: 'e', 1045: 'E',
                        1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I', 1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K',
                        1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M', 1085: 'n', 1053: 'N', 1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R',
                        1089: 's', 1057: 'S', 1090: 't', 1058: 'T', 1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS',
                        1095: 'ch', 1063: 'CH', 1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH', 1098: '', 1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '',
                        1101: 'e', 1069: 'E', 1102: 'yu', 1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je', 1028: 'JE', 1110: 'i', 1030: 'I', 1111: 'ji', 1031: 'JI',
                        1169: 'g', 1168: 'G'
                     }

    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    normal_name = ''
    latin_name = name.translate(cyrillic_trans)
    for char in latin_name:
        if char in alphabet:
            normal_name += char
        else:
            normal_name += '_'            
    return normal_name


def sort_main(get_path):

    get_path = pathlib.Path(get_path).resolve()
    archives = get_path / 'archives'
    audio = get_path / 'audio'
    documents = get_path / 'documents'
    images = get_path / 'images'
    video = get_path / 'video'
    archives.mkdir(exist_ok=True)
    audio.mkdir(exist_ok=True)
    documents.mkdir(exist_ok=True)
    images.mkdir(exist_ok=True)
    video.mkdir(exist_ok=True)
    for elem in get_path.iterdir():
        if elem.suffix.lower() in ('.zip', '.gz', '.tar'):
            elem.rename(archives / elem.name)
        elif elem.suffix.lower() in ('.mp3', '.ogg', '.wav', '.amr'):
            elem.rename(audio / elem.name)
        elif elem.suffix.lower() in ('.doc', '.docx', '.txt', '.pdf', '.xls', '.xlsx', '.pptx', '.ppt', '.rtf',):
            elem.rename(documents / elem.name)
        elif elem.suffix.lower() in ('.jpeg', '.png', '.jpg', '.svg', '.bmp', '.tiff'):
            elem.rename(images / elem.name)
        elif elem.suffix.lower() in ('.avi', '.mp4', '.mov', '.mkv'):
            elem.rename(video / elem.name)


def to_startfolder(get_path):

    get_path = pathlib.Path(get_path).resolve()
    for elem in get_path.iterdir():
        if elem.is_dir():
            elem = elem.resolve()
            if elem not in [sort_folder, sort_folder / 'archives', sort_folder / 'video', sort_folder / 'audio', sort_folder / 'documents', sort_folder / 'images']:                
                to_startfolder(elem)

        if elem.is_file():            
            try:
                new_name = normalize(elem.stem) + elem.suffix
                elem.rename(sort_folder / new_name )
            except FileExistsError:
                count = 0
                while True:
                    count += 1
                    new_name = normalize(elem.stem) + '(' + str(count) + ')' + elem.suffix
                    if not (sort_folder / new_name).exists:
                        elem.rename(sort_folder / new_name)
                        break
                   
    if get_path not in [sort_folder, sort_folder / 'archives', sort_folder / 'video', sort_folder / 'audio', sort_folder / 'documents', sort_folder / 'images']:
         get_path.rmdir()


def unpack_archive(get_path):
    arcive = get_path / 'archives'
    for elem in arcive.iterdir():
        if elem.suffix.lower() in ('.zip', '.gz', '.tar'):
            stem_folder = arcive / elem.stem
            shutil.unpack_archive(elem, stem_folder)
            elem.unlink()

        

def validation_path():

    user_input = ''

    try:
        user_input = sys.argv[1]
    except IndexError as e:
        print(f'Error: {e}. Input path to directory like this: "sort.py D:\\folder\\sort_folder')
        exit()
    path = pathlib.Path(user_input)
    if path.exists():
        if path.is_dir():
            pass                
        else:
            print(f'{path} is file')
    else:
        print(f'path {path.absolute()} not exists')
    return path

# MAIN 

if __name__ == '__main__':
    sort_folder = validation_path()
    to_startfolder(sort_folder)
    sort_main(sort_folder)
    unpack_archive(sort_folder)
    print('Sorting complite')
    