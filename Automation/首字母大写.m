files = dir('*.pdf');
len = length(files);
for i = 1 : len
    oldname=files(i).name;
    newname=[upper(oldname(1)) oldname(2:end)];%lower小文字
    eval(['!rename' 32 oldname 32 newname]);
end
