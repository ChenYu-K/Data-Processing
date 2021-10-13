import os 

##削除するファイルの拡張子を取得する
extension = (".xlsm")   ##削除したい拡張子を入力

## ディレクトリのパスを取得
path_name = ("C:\\テスト")   ##ディレクトリのパスを入力

##全てのディレクトリのファイル名を取得
for curDir, dirs, files in os.walk(path_name):
    for filename in files:
        if filename.endswith(extension):   ##指定された拡張子を持つファイルがあれば
            file_path = os.path.join(curDir,filename)
            os.remove(file_path)   ##完全に削除
