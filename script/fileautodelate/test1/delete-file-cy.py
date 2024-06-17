import os
import datetime

def delete_files(folder_path):
    current_date = datetime.date.today()

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path,file_name)
        
        modified_time = datetime.date.fromtimestamp(os.path.getmtime(file_path))

        days_alive = (current_date - modified_time).days

        if days_alive > 60:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")

folder_path = "./"
delete_files(folder_path)