# paythonを用いてMicrosoft fromsの自動入力

## [Enterroom](https://github.com/kaede-cycy/Automation-script/blob/main/Autofill/Enterroom.py)
  入室用スクリプト，一応答えが全部健康の答えになるので，何回異常があれば手動で修正．
 
## [Laveroom](https://github.com/kaede-cycy/Automation-script/blob/main/Autofill/Leaveroom.py)
　退室用スクリプト，部屋番号はc308に設定している．
 
 ---
## よくあるErro

### 環境配置:
1.最初はseleniumをインストールしなければならない．\
　　`pip install selenium` \
2. chromedriveのバージョンがあっているのか\
　　この[URL](http://chromedriver.storage.googleapis.com/index.html)をクリックして，自分のchromeと一致しているバージョンをダウンロードする．
 Chormeバージョン確認のやり方: chomreの設定→ヘルプ→google chromeについて\
![image](https://user-images.githubusercontent.com/71476156/117744027-de2cdd80-b242-11eb-8b23-4aeea6e9a218.png)

- Downloadした`chromedriver.exe`をchromeのルートディレクトリに入れて実行する．\
  `C:\Program Files (x86)\Google\Chrome\Application` \
- システムの環境変数を先のアドレスをpathに追加すること．\
  ![image](https://user-images.githubusercontent.com/71476156/117744908-7e373680-b244-11eb-9cd5-84f44e4c70eb.png)
