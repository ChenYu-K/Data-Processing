function deck2 = importfile(filename, dataLines)
%IMPORTFILE テキスト ファイルからデータをインポート
%  DECK2 = IMPORTFILE(FILENAME) は既定の選択に関してテキスト ファイル FILENAME
%  からデータを読み取ります。  数値データを返します。
%
%  DECK2 = IMPORTFILE(FILE, DATALINES) はテキスト ファイル FILENAME
%  の指定された行区間のデータを読み取ります。DATALINES
%  を正の整数スカラーとして指定するか、行区間が不連続の場合は正の整数スカラーからなる N 行 2 列の配列として指定します。
%
%  例:
%  deck2 = importfile("\\10.108.51.13\sdb\CHEN\陳\1.研究\MatLab\膜厚計測\shirai-makuatsu\deck2.CSV", [2, Inf]);
%
%  READTABLE も参照してください。
%
% MATLAB からの自動生成日: 2021/06/03 00:01:17

%% 入力の取り扱い

% dataLines が指定されていない場合、既定値を定義します
if nargin < 2
    dataLines = [2, Inf];
end

%% インポート オプションの設定およびデータのインポート
opts = delimitedTextImportOptions("NumVariables", 5);

% 範囲と区切り記号の指定
opts.DataLines = dataLines;
opts.Delimiter = ",";

% 列名と型の指定
opts.VariableNames = ["Time", "Address", "Measurements", "Material", "iPmj"];
opts.VariableTypes = ["double", "double", "double", "double", "double"];

% ファイル レベルのプロパティを指定
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% 変数プロパティを指定
opts = setvaropts(opts, ["Time", "Material", "iPmj"], "TrimNonNumeric", true);
opts = setvaropts(opts, ["Time", "Material", "iPmj"], "ThousandsSeparator", ",");

% データのインポート
deck2 = readtable(filename, opts);

%% 出力型への変換
deck2 = table2array(deck2);
end