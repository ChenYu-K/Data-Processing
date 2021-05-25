%inputdata & outputdata
in = [Ra(:,1),RaSD(:,1),Rz(:,1),RzSD(:,1),Rzjis(:,1)];
in = in';
out = slipANN(:,1);
out = out';
%dataを正規化する (normalizing the data)
[inn,inputStr] = mapminmax(in);
[outn,outputStr] = mapminmax(out);

%make a BP neural network
net = newff(inn,outn,[5,3,1],{'purelin','logsig','purelin'});
net.trainParam.show = 1;             %10.time get resoult back
net.trainParam.epochs = 10000;         %the max train time
net.trainParam.lr = 0.05;             %net learing rate
net.trainParam.goal = 0.065*10^(-3);  %target deviation
net.divideFcn = '';                   %bug check

%start train
net = train(net,inn,outn);
%使用训练好的网络，基于训练集的数据对BP网络进行仿真得到网络输出结果
answer = sim(net,inn);

%normalizing 
answer1 = mapminmax('reverse',answer,outputStr);

%make fig t = 1990:

a1 = answer1(1,:);     %test data

figure(1);
subplot(2,1,1);plot(Ra,a1,'ro',Ra,slipANN,'b+');
legend('test','ANN');
xlabel('Ra'); ylabel('slip coefiicient');
title('compare the test and ANN');
grid on;

%new data
newinput = [22.36935;6.509416727;107.28235;23.64338718;74.429];
newinput = mapminmax('apply',newinput,inputStr); %normalizing
newoutput = sim(net,newinput);
newoutput = mapminmax('reverse',newoutput,outputStr);

disp('the slip coefficient is :');
newoutput(1,:)
