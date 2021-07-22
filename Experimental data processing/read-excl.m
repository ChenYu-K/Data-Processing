clear
db=ls;   %ファイル内の内容を読み込む
db1=string(db);
db1=deblank(db1);
data=db1([3:50],1);
l=length(data);
for i=1:l
   test_data(i,1)={data(i,1)};
    name=['a=csvread(''',data(i,1),''',20,1);'];
    name1=strcat(name(1,1),name(1,2),name(1,3)); #名前を分ける
    eval(name1);  %名前を合併する
    slipdata=strsplit(test_data{i,1},'.');
    slipdata1(i,1)={slipdata(1,1)};
    slipdata1(i,2)={a};
    clear a;
end
clearvars -except slipdata1   %* 
save('slipdata1')
