# Automatic script
![GitHub](https://img.shields.io/github/license/Kaede-cycy/data-prossing?logoColor=green&style=plastic)
[![ocu-shield]][ocu]
![abaqus]

> Hi，

# Preface
 Here, i summarized some scripts created by myself and my laboratory for experimental data processing.    
 The scripts are created by <kbd>Python</kbd>,<kbd>Matlab</kbd> and <kbd>Pytorch</kbd>. Although `Python` and `Matlab`'s grammar are very similar, most script have two version,`Python` and `Matlab`,the idea and the algorithm are basically the same.
 
|name|function|
|---|---|
|read csv|read all the csv data where sored the same folder to matlab|
|[transformation_matrix](https://github.com/ChenYu-K/Data-Processing/tree/main/Automation/Transformation_matrix)| transfor matrix of film measurement data|

# Contents
* [Experment Data Processing](#Experment-Data-Processing)
* [Neural Network](#Neural-Network)
* [Abaqus script](#Abaqus-script)
* [Ohter Automation](#Ohter-Automation)


## Experment Data Processing

Automatic data processing Using by MATLAB  
Matlabを用いてデータの自動化処理


目前完成：  
1.文件内容读取，并上传到matlab　（CSVファイルの一括読み取り）  
2.小型滑移实验的数据分析并整理（小型すべり試験のデータ整理）

---

## Neural Network
1. [ANN_train(using `Pytorch` )](Neural%20Network/ANN_train.py)
2. [BPNN (Matlab_BPNN)](Neural%20Network/BPNN-slip%20coefficient.m)


## Abaqus script

### Abaqus自動直列実行 (Abaqus Serial Execution Script)

 There is [Documentation](https://github.com/ChenYu-K/Data-Processing/tree/main/script/abaqus_run)

|License|||
|---|---|---|
|50| CPU:1 を使って計算する|Download|
|75| CPU:4 を使って計算する|Download|
|GPU| CPU:8 + GPU:1 を使って計算する|Download|

 Abaqus<sup id="a1">[1](#f1)</sup>

 
## Ohter Automation]

## Reference
<span id="f1">1. [^](#a1)</span> 脚注1的说明

[abaqus]:https://img.shields.io/badge/Abaqus-V.2020-blue?logo=Dassault%20Syst%C3%A8mes
[ocu]:http://brdg.civil.eng.osaka-cu.ac.jp/index.html
[ocu-shield]:https://img.shields.io/badge/OCU%20-Bridge%20Eng.%20LAB-blue
[^Abaqus]: Dassult System manual 2020.
