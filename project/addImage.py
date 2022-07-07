from logging import info
import config
import exceptions

import sys
import os

import sqlite3
# from sqlite3 import 
import prettytable
from PIL import Image

FILES = prettytable.PrettyTable()
FILES.align = 'l'
FILES.field_names = ['file_id', 'filename', 'format', 'mode', 'size (in px)', 'size', 'palette', 'info']

def convert_byte(bytes: int) -> str:
    conv_info = {
        'B': 1,
        'KB': 1024 ** 1,
        'MB': 1024 ** 2,
        'GB': 1024 ** 3,
    }

    for arg in conv_info.items():
        conv_value = bytes / arg[1]
        if conv_value < 1024:
            return f'{round(conv_value,2)} {arg[0]}'

def showTable():
        conn = sqlite3.connect(os.path.join(BD_DIR, 'image_database.db'))
        cur = conn.cursor()

        try:
                cur.execute("SELECT * FROM image;")
        except sqlite3.OperationalError:
                print('Database is empty!')

        resultw = cur.fetchall()

        for i in resultw:
                FILES.add_row(i)
        print(FILES)


def main(WORK_DIR: str, BD_DIR: str) -> None:
        conn = sqlite3.connect(os.path.join(BD_DIR, 'image_database.db'))
        cur = conn.cursor()
        
        cur.execute("""CREATE TABLE IF NOT EXISTS image(
        file_id INTEGER PRIMARY KEY,
        filename TEXT,
        format varchar(255),
        mode varchar(255),
        size_px varchar(255),
        size varchar(255),
        palette varchar(255),
        info TEXT);
        """)
        conn.commit()

        try:
                LIST_OF_FILES = os.listdir(WORK_DIR)
        except FileNotFoundError:
                print("Не верно задан путь!")
                return

        cur.execute("SELECT filename FROM image;")
        results = cur.fetchall()

        for res in range(len(results)):
                results[res] = str(results[res])[2:-3].replace('\\\\', '\\')

        for file in LIST_OF_FILES:
                if file.split('.')[-1].upper() in config.ALLOWED_EXTENSIONS:

                        full_path = os.path.join(WORK_DIR, file)
                        openedFile = Image.open(full_path)

                        file_record = (
                                str(openedFile.filename),
                                str(openedFile.format),
                                str(openedFile.mode),
                                str(openedFile.size),
                                str(convert_byte(os.path.getsize(full_path))),
                                str(openedFile.palette),
                                str(openedFile.info),
                        )

                        if results == []:
                                cur.execute("INSERT INTO image(filename, format, mode, size_px, size, palette, info) VALUES(?, ?, ?, ?, ?, ?, ?);", file_record)
                                conn.commit()
                                continue

                        if openedFile.filename in results:
                                info_str = f'File {openedFile.filename} is already added.'
                                # print(f"\033[32;55m{32}")
                                print(info_str)
                        else:
                                cur.execute("INSERT INTO image(filename, format, mode, size_px, size, palette, info) VALUES(?, ?, ?, ?, ?, ?, ?);", file_record)
                                conn.commit()
                                info_str = f'File {openedFile.filename} is added.'
                                print(info_str)



if __name__ == '__main__':
        try:
                for com in sys.argv:
                        if com.startswith('-'):
                                if com not in config.COMMANDS:
                                        raise exceptions.BadRequest('Заданые параметры являются недопустимыми!')
        except exceptions.BadRequest as err:
                print(err)
        # print(len(sys.argv))
        WORK_DIR = os.getcwd()
        BD_DIR = os.getenv('BASIC_BD_URL')

        if len(sys.argv) == 1:
                main(WORK_DIR, BD_DIR)
        else:
                if len(sys.argv) == 2:
                        if sys.argv[1] == '-st':
                                showTable()
                if len(sys.argv) == 3:
                        if sys.argv[1] == '-p':
                                WORK_DIR = sys.argv[2]
                        elif sys.argv[1] == '-pdb':
                                BD_DIR = sys.argv[2]
                if len(sys.argv) == 5:
                        if sys.argv[1] == '-p':
                                WORK_DIR = sys.argv[2]
                                if sys.argv[3] == '-pdb':
                                        BD_DIR = sys.argv[4]
        main(WORK_DIR, BD_DIR)
