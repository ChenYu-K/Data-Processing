# Abaqus自動直列実行スクリプト

Abaqusで作成したモデルから`inp`ファイルを出力して，他の計算機で自動に計算してもらうっという機能．

# 機能

- 計算機に`.inp`ファイルを置くだけで，計算が始まる．
- 終了時Jobに関連するファイルを全部自動で同じフォルダに移動できる．
- 複数の`.inp`を置くとき，同時に流すか，列並べて流すか選択できる．（橋梁研は基本列で並べる，トークン数の制限があるため）

# バージョン

|License|||
|---|---|---|
|50| CPU:1 を使って計算する|Download|
|75| CPU:4 を使って計算する|Download|
|GPU| CPU:8 + GPU:1 を使って計算する|Download|

# 注意点

- 最初の時，スクリプトファイルは目的のパソコンで起動してください．自分パソコンで起動したら，自分のパソコンのCPUとか使うので．
- 自分のパソコンで起動する方法もあるが，こっちに参考してください．（wait）

# 更新Log

## 2022.6.22　現在V10からV11に更新した
変更点：

- 時々`.log`ファイルが正しくフォルダ内に移動できないBUGを修正した
- `Thread=1`にしても，複数`.inp`ファイルを置いたとき，列を並べず，同時に二つ`.inp`流す　BUGを修正した．
-  判定時間及び条件を修正して，流れを最適化した．


# License 

                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/
Copyright@2022 Osaka Metropolitan university Bridge Engineering Lab, yu chen
