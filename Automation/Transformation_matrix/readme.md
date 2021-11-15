# 行列変換スクリプト
自動膜厚計測したデータを好きな行列に変換できる．
フォルダ内のすべての生データを一括変換できる．

`input`: 生データ
`output`: 処理した.csv

---

- [trans.m](trans.m)は基本の変換アルゴリズム．
- [app1.m](/app1.m)は関数[trans.m](/trans.m)を引用したGUIのSourceCode．
- [transfer.mlapp](/transfer.mlapp)はGUIのSourceCode.
- [Transformation_matrix.prj](/Transformation_matrix.prj)は出力オプション．

## 使い方
`Transformation_matrix.mlappinstall`をインストールし，
Matlabのappで実行する．