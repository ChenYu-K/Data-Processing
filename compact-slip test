clc
clear
load test_data;
load slipdata1;
pm=0;p1=0;
[a,~]=size(slipdata1);
 for n=1:a     %detaimport
    cs=slipdata1{n,2};
    Nmax=max(abs(cs(:,5)));
    a=-1; 
    Pmax1=1;
    i=3;
    while( a < 1)   %すべり荷重の判定（1mm load or MAX load）
    a=0.5*(abs(cs(i,5))+abs(cs(i,6)));
        if abs(cs(i,3)) > Pmax1
         Pmax1=abs(cs(i,3));m=i;
        end
       N1=abs((cs(i,4)));
    i=i+1;
    end
if Pmax1 == abs(cs(i,3))
  p1=p1+1;
else pm=pm+1;
end
 slip1(n)=Pmax1/(2*Nmax);
 slip0(n)=Pmax1/(2*abs(cs(10,4)));
 fric(n)=Pmax1/(2*N1);
 C(n)=0.5*Pmax1-(abs(cs(10,4))^(-1/3));
 Pmax0(n)=Pmax1;
 N(n)=abs(cs(10,4));
 sp(n)=Pmax1/(2*abs(cs(10,4))^(-1/3));
 figure(n);
plot(0.5*(abs(cs(:,5))+abs(cs(:,6))),abs(cs(:,3)),'-o','MarkerIndices',[m])
%plot(abs(cs(:,6)),abs(cs(:,4)),abs(cs(:,7)),abs(cs(:,4)),'-o','MarkerIndices',[m]);
axis([0 1.5 0 65]);
set(gca,'xtick',0:0.2:1.5);
%saveas(n,csv1{2,n});
%print(n,'-djpeg','C:\CY\陳\1.研究\MatLab\fig')
  title(n);xlabel('Displacement(mm)');ylabel('Load(kN)');
end
