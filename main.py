import tkinter as tk
from tkinter import filedialog
import os
import shutil
import json


# ----functions----

def rename_file(file_path):
    file_name = os.path.splitext(file_path)[0]
    ext = os.path.splitext(file_path)[1].lower()

    try:
        int(file_name[-1])
        num = str(int(file_name[-1]) + 1)
        new_file_name = file_name.replace(file_name[-1], num) + ext
        return new_file_name
    except:
        return f'{file_name}' + ' ' + str(1) + ext


def get_type(extension):
    extension = extension.upper()
    with open('extensions.json') as f:
        data = json.load(f)

    while True:
        for k, v in data.items():
            if extension in v:
                return k.capitalize()
            else:
                pass
        return "Other"


# ----Get path window prompt----
root = tk.Tk()
root.withdraw()
path = filedialog.askdirectory()

# ----List all the files in the directory----
files = []
for file in os.listdir(path):
    if os.path.isfile(os.path.join(path, file)):
        files.append(file)

# ----Get all files extensions----
extensions = []

for file in files:
    extension = os.path.splitext(file)[1]
    extension = extension.replace('.', '').lower().capitalize()
    if extension and extension not in extensions:
        extensions.append(extension)

# ----Create folders from extensions----
types = []
for extension in extensions:
    file_type = get_type(extension)
    types.append(file_type)
    full_path = f'{path}/{file_type}'
    if not os.path.isdir(full_path):
        os.mkdir(full_path)

# ----Move files to folders----

for file in files:
    extension = os.path.splitext(file)[1]
    extension = extension.replace('.', '')
    file_type = get_type(extension)

    if not file.startswith('.'):
        try:
            shutil.move(f"{path}/{file}", f"{path}/{file_type}")
        except:
            new_name = rename_file(f"{path}/{file}")
            os.rename(f"{path}/{file}", f'{new_name}')
            shutil.move(f"{new_name}", f"{path}/{file_type}")
