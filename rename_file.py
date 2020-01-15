import os

def main():
    target_dl_folder_path = r"C:\Temp"
    # filename = ""
    # filename += r"\"
    # filename += "asd"
    # path += "\\" + "asd"
    # print(path)

    old_file_name = "123123"
    new_file_name = "asdqea"
    # os.rename(target_dl_folder_path + "\\" + old_file_name + ".zip ", target_dl_folder_path + "\\" + new_file_name + ".zip")

    try:
        os.path.exists(target_dl_folder_path + "\\" + old_file_name + ".zip ")
    except FileNotFoundError:
        print("666666")

if __name__ == '__main__':
    main()