import os
from PIL import Image
import io
from tqdm import tqdm  # 导入tqdm模块，用于显示进度条

# 设置输入文件夹和输出文件夹路径
input_folder = 'Photo/Photo/'
output_folder = 'photo_compressed/'

# 目标文件大小（以字节为单位，2MB等于2 * 1024 * 1024字节）
target_size = 2 * 1024 * 1024

# 获取输入文件夹中的所有文件
def get_image_files(folder):
    image_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')):
                image_files.append(os.path.join(root, file))
    return image_files

# 压缩图片
def compress_image(input_path, output_path, quality=85):
    image = Image.open(input_path)
    output_buffer = io.BytesIO()
    image.save(output_buffer, format='JPEG', quality=quality)
    output_buffer.seek(0)
    
    with open(output_path, 'wb') as output_file:
        output_file.write(output_buffer.read())

# 创建输出文件夹及子文件夹结构
def create_output_directory(input_file, input_folder, output_folder):
    relative_path = os.path.relpath(input_file, input_folder)
    output_dir = os.path.join(output_folder, os.path.dirname(relative_path))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

# 获取所有图片文件
image_files = get_image_files(input_folder)

# 使用tqdm创建进度条
for input_file in tqdm(image_files, desc="压缩进度", unit="文件"):
    filename = os.path.basename(input_file)
    output_dir = create_output_directory(input_file, input_folder, output_folder)
    output_file = os.path.join(output_dir, filename)
    
    quality = 85
    while True:
        compress_image(input_file, output_file, quality=quality)
        if os.path.getsize(output_file) <= target_size:
            break
        quality -= 5
        if quality < 5:
            break

print("压缩完成！")