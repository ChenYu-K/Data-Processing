import pandas as pd
import torch
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import TensorDataset, DataLoader
import os
import cv2 as cv
from torch.utils.data import Dataset
from torchvision import transforms
import torch.nn.functional as F
from PIL import Image
import torch.nn as nn
from torch.optim import Adam
import matplotlib.pyplot as plt
import numpy as np
from torch.autograd import Variable


# Define the data and label
def getlabel(dir):
    labels=[]
    for name in os.listdir(dir):
        if os.path.splitext(name)[1] == '.png':
            fname=os.path.splitext(name)[0]
            labels.append(fname)
    labels = list(map(int, labels))
    labels = torch.tensor(labels)
    # Normalize labels
    #min = torch.min(labels)
    #max = torch.max(labels)
    #labels = (labels - min) / (max - min)
    labels = labels.type(torch.FloatTensor)
    return labels

def generate_dataset(dir):
    """
    set_label should be 'torch.tensor([1])' if two-catogory and positive sample
    """
    train_data = []
    for file_name in os.listdir(dir):
        if file_name != "Thumbs.db":
            img_dir = os.path.join(dir, file_name)
            img = cv.imread(img_dir)
            img = cv.resize(img, (769, 432))   # /5 resize img
            #img_gray = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
            pimg = Image.fromarray(img)
            train_data.append(pimg)
    return train_data


class MyDataset(Dataset):
    def __init__(self, data, labels, transform=None, target_transform=None):
        self.transform = transform
        self.target_transform = target_transform
        imgs = []
        for i in range(len(labels)):
            # print(type(data[i]))    # <class 'PIL.Image.Image'>
            im_tensor = transform(data[i])#.to(torch.device("cpu"))
            imgs.append((im_tensor, labels[i]))
        self.imgs = imgs                         # DataLoader通过getitem读取图片数据
    def __getitem__(self, index):
        fn, label = self.imgs[index]
        return fn, label
    def __len__(self):
        return len(self.imgs)


class Net(torch.nn.Module):
    # Net类的初始化函数
    def __init__(self, n_feature, n_hidden, n_output):
        # 继承父类的初始化函数
        super(Net, self).__init__()
        # 网络的隐藏层创建，名称可以随便起
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=3, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(3)
        self.conv2 = nn.Conv2d(in_channels=3, out_channels=6, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(6)
        self.pool = nn.MaxPool2d(2,2)
        self.fc1 = nn.Linear(6*108*192, n_feature)
        self.hidden_layer = torch.nn.Linear(n_feature, n_hidden)
        # 输出层(预测层)创建，接收来自隐含层的数据
        self.predict_layer = torch.nn.Linear(n_hidden, n_output)

    # 网络的前向传播函数，构造计算图
    def forward(self, x):
        x = self.pool(F.relu(self.bn1(self.conv1(x))))      #432-3+1=430,430/2=215;769-3+1=767,767/2=384
        x = F.relu(self.bn2(self.conv2(x)))                #215-3+1=213,213/2=108;384-3+1=382,382/2=192
        x = self.pool(x)   
        x = x.view(-1, 6*108*192)
        x = F.relu(self.fc1(x))
        # 用relu函数处理隐含层输出的结果并传给输出层
        hidden_result = self.hidden_layer(x)
        relu_result = F.relu(hidden_result)
        predict_result = self.predict_layer(relu_result)
        return predict_result

def testAccuracy():
    
    net.eval()
    accuracy = 0.0
    total = 0.0
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    #device = torch.device("cpu")

    with torch.no_grad():
        for data in valid_loader:
            images, labels = data
            images, labels = images.to(device), labels.to(device)
            # run the model on the test set to predict labels
            outputs = net(images)
            # the label with the highest energy will be our prediction
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            accuracy += (predicted == labels).sum().item()
    
    # compute the accuracy over all test images
    accuracy = (100 * accuracy / total)
    return(accuracy)

def train(num_epochs):
    
    best_accuracy = 0.0

    # Define your execution device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    #device = torch.device("cpu")

    # Convert model parameters and buffers to CPU or Cuda
    net.to(device)
    for epoch in range(num_epochs):  # loop over the dataset multiple times
        running_loss = 0.0
        running_acc = 0.0

        for i, (images, labels) in enumerate(train_loader, 0):
            #images, labels = dataiter.next()
            # 输入数据进行预测
            # get the inputs
            images = Variable(images.to(device))
            labels = Variable(labels.to(device))
            prediction = net(images)
            print(prediction,labels)
            # 计算预测值与真值误差，注意参数顺序问题
            # 第一个参数为预测值，第二个为真值
            loss = loss_func(prediction, labels)

            # 开始优化步骤
            # 每次开始优化前将梯度置为0
            optimizer.zero_grad()
            # 误差反向传播
            loss.backward()
            # 按照最小loss优化参数
            optimizer.step()
            print('epoch:',i,'loss:',loss.item())
            if i % 1000 == 999:    
                # print every 1000 (twice per epoch) 
                print('[%d, %5d] loss: %.3f' %
                      (epoch + 1, i + 1, running_loss / 1000))
                # zero the loss
                running_loss = 0.0
        # 计算准确率
        # Compute and print the average accuracy fo this epoch when tested over all 10000 test images
        accuracy = testAccuracy()
        print('For epoch', epoch+1,'the test accuracy over the whole test set is %d %%' % (accuracy))


    print('Finished Training')
        #可视化训练结果
        # if i % 2 == 0:
        #     # 清空上一次显示结果
        #     plt.cla()
        #     # 无误差真值曲线
        #     plt.plot(images.numpy(), labels.numpy(), c='blue', lw='3')
        #     # 有误差散点
        #     plt.scatter(images.numpy(), labels.numpy(), c='orange')
        #     # 实时预测的曲线
        #     plt.plot(images.numpy(), prediction.data.numpy(), c='red', lw='2')
        #     plt.text(-0.5, -65, 'Time=%d Loss=%.4f' % (i, loss.data.numpy()), fontdict={'size': 15, 'color': 'red'})
        #     plt.pause(0.1)

# prepare the data
def predict(model, device):
    Vdataiter=iter(valid_loader)
    vimg, vlabels = Vdataiter.next()
    model.to(device)
    with torch.no_grad():
        vimg=vimg.to(device)
        out = model(vimg)
        #_, pre = torch.max(out.data, 1)
        return vimg,out, vlabels

# define the net
# 训练次数
#TRAIN_TIMES = len(train_loader)-1
# 输入输出的数据维度，这里都是1维
INPUT_FEATURE_DIM = 1000
OUTPUT_FEATURE_DIM = 1
# 隐含层中神经元的个数
NEURON_NUM = 200
# 学习率，越大学的越快，但也容易造成不稳定，准确率上下波动的情况
LEARNING_RATE = 0.1
# unsqueeze函数可以将一维数据变成二维数据，在torch中只能处理二维数据
#x_data = torch.unsqueeze(torch.linspace(-4, 4, 80), dim=1)
# randn函数用于生成服从正态分布的随机数
#y_data = x_data.pow(3) + 3 * torch.randn(x_data.size())
#y_data_real = x_data.pow(3)

# 定义模型
net = Net(n_feature=INPUT_FEATURE_DIM, n_hidden=NEURON_NUM, n_output=OUTPUT_FEATURE_DIM)
print(net)
# 训练网络
# 这里也可以使用其它的优化方法
optimizer = torch.optim.Adam(net.parameters(), lr=LEARNING_RATE)
# 定义一个误差计算方法
loss_func = torch.nn.MSELoss() # 定义交叉熵损失函数 交叉熵损失函数是用来衡量两个概率分布之间的距离的#nn.MSELoss()
# Define the loss function with Classification Cross-Entropy loss and an optimizer with Adam optimizer

# Vdataiter=iter(valid_loader)
# vimg, vlabels = Vdataiter.next()
# print(vimg.shape)
# print(vlabels.shape)
# print(vlabels)
if __name__ == "__main__":

    torch.cuda.empty_cache()

    # create the data
    traindir= './train/'
    validdir = './test/'
    train_data0 = generate_dataset(traindir)
    train_label0=getlabel(traindir)
    valid_data0 = generate_dataset(validdir)
    valid_label0 = getlabel(validdir)

    # create the data loader
    normMean = [0.5, 0.5, 0.5]
    normStd = [0.5, 0.5, 0.5]
    transform = transforms.Compose(
        [transforms.Grayscale(num_output_channels=1), #彩色图像转灰度图像num_output_channels默认1
        transforms.ToTensor(),  # range [0, 255] -> [0.0,1.0]   
        #transforms.Normalize(normMean, normStd)
        ])

    # 也可以再定义train_transform加入一些数据增强 
    train_data = MyDataset(train_data0, train_label0, transform=transform)
    valid_data = MyDataset(valid_data0, valid_label0, transform=transform)
    train_loader = DataLoader(dataset=train_data, batch_size=1, shuffle=True)
    valid_loader = DataLoader(dataset=valid_data, batch_size=1, shuffle=True)
    dataiter=iter(train_loader)
    images, labels = dataiter.next()
    print(images.shape)
    print(labels.shape)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    #device = torch.device("cpu")
    # Let's build our model
    train(10)
    print('Finished Training')

    # Test which classes performed well
    testAccuracy()
    
    # Let's load the model we just created and test the accuracy per label
    # model = net()
    # path = "myFirstModel.pth"
    # model.load_state_dict(torch.load(path))

    print(predict(net, device))
