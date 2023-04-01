import sys
import os

def check_input():
    if len(sys.argv) != 2:
        print("Usage: pyhton3 parser.py file.world")
        sys.exit(1)

    world_file = sys.argv[1]
    if not world_file.endswith(".world"):
        print("File extension must be .world")
        sys.exit(1)
    
    if not os.path.isfile(world_file):
        print(f"File '{world_file}' not exist.")
        sys.exit(1)

    return world_file

def get_sdf_version_line(world_file):
    if world_file.tell() != 0:
        world_file.seek(0)

    first_line = world_file.readline()
    if "<sdf version=" in first_line:
        return first_line
    else:
        return '<sdf version="1.5">\n'


def create_sdf_file(world_file, sdf_file_name, sdf_version_line):
    write_flag = False
    sdf_file = open(sdf_file_name, "w")
    sdf_file.write('<?xml version="1.0" ?>\n')
    sdf_file.write(sdf_version_line)

    for linea in world_file:
        # Number spaces at beginning of line
        n_spaces = len(linea) - len(linea.lstrip())
        if write_flag:
            sdf_file.write(" " * (n_spaces - 2) + linea.lstrip())
            if "</model>" in linea:
                break
        else:
            if "<model name=" in linea:
                sdf_file.write(" " * (n_spaces - 2) + linea.lstrip())
                write_flag = True
    sdf_file.write('</sdf>')
    sdf_file.close()
        

def get_model_names(world_file):
    model_names = []
    poses = []
    for linea in world_file:
        if "<state world_name=" in linea:
            break
        if "<model name=" in linea:
            model_name = linea.split('=')[1].strip()  # Extrae la cadena del nombre del modelo
            model_name = model_name.replace(">", "")
            model_name = model_name.replace("'", "")
            model_names.append(model_name)
    world_file.seek(0)
    return model_names

def main():
    world_file = check_input()
    world_file = open(world_file, "r")
    models_array = get_model_names(world_file)
    sdf_version_line = get_sdf_version_line(world_file)
    models_dir = "../models"
    
    for name in models_array:
        model_path = os.path.join(models_dir, name + ".sdf")
        create_sdf_file(world_file, model_path, sdf_version_line)

    world_file.close()
if __name__ == "__main__":
    main()
