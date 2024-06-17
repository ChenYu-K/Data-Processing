import os
from PIL import Image
from tqdm import tqdm

# 设置输入文件夹路径，这里设置为输出文件夹，即覆盖修改
input_folder = 'photo'

# 目标宽度和高度，保持长宽比不变
target_width = 3840  # 4K分辨率的宽度
target_height = 2160  # 4K分辨率的高度

# 获取文件夹内的所有文件
def get_all_files(folder):
    all_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    return all_files

# 调整图片分辨率，保持长宽比不变
def resize_image(input_path, output_path):
    image = Image.open(input_path)
    original_width, original_height = image.size
    if original_width > original_height:
        new_width = target_width
        new_height = int(original_height * (target_width / original_width))
    else:
        new_height = target_height
        new_width = int(original_width * (target_height / original_height))
    image = image.resize((new_width, new_height), Image.ANTIALIAS)
    image.save(output_path)

# 获取所有文件
all_files = get_all_files(input_folder)

# 使用tqdm创建进度条
for input_file in tqdm(all_files, desc="调整分辨率进度", unit="文件"):
    output_file = input_file  # 输出文件直接覆盖原始文件
    resize_image(input_file, output_file)

print("分辨率调整完成！")
