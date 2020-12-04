#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import torch
import torchvision
import torchvision.transforms as transforms


# In[ ]:


transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=4,
                                          shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                       download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=4,
                                         shuffle=False, num_workers=2)

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')


# In[ ]:


import matplotlib.pyplot as plt
import numpy as np
#function to show an image

def imshow(img):
    img = img / 2 +0.5
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg,(1,2,0)))
    plt.show()
    
#get som random training images
dataiter = iter(trainloader)
images,labels = dataiter.next()

# show images
imshow(torchvision.utils.make_grid(images))
# 将若干张图像合成一张图像
#print labels
print(' '.join('%5s'%classes[labels[j]] for j in range(4)))


# In[ ]:


import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super(Net,self).__init__()
        self.conv1 = nn.Conv2d(3,6,5)
        self.pool = nn.MaxPool2d(2,2)
        self.conv2 = nn.Conv2d(6,16,5)
        self.fc1 = nn.Linear(16*5*5,120)
        self.fc2 = nn.Linear(120,84)
        self.fc3 = nn.Linear(84,10)
    def forward(self,x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1,16*5*5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

net = Net()    
    
        
        


# In[ ]:


import torch.optim as optim

certerion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(),lr = 0.001,momentum = 0.9)


# In[ ]:


for epoch in range(2):
    running_loss = 0.0
    for i,data in enumerate(trainloader,0):
        inputs,labels = data
        
        optimizer.zero_grad()
        
        outputs = net(inputs)
        loss = certerion(outputs,labels)
        loss.backward()
        optimizer.step()
        
        running_loss == loss.item()
        if i % 2000 == 1999:
            print('[%d,%5d] loss:%.3f'
                 %(epoch+1,i+1,running_loss / 2000))
print('Finished Training')            


# In[ ]:


dataiter = iter(testloader)
images,labels = dataiter.next()
imshow(torchvision.utils.make_grid(images))
print(' '.join('%5s'%classes[labels[j]] for j in range(4)))
output = net(images)
_,predicted = torch.max(outputs,1)#第一个参数返回最大值，第二个返回索引 1表示取行最大值
print('Predicted:',' '.join('%5s'%classes[predicted[j]] for j in range(4)))


# In[ ]:


correct = 0
total = 0
with torch.no_grad():
    for data in testloader:
        images,labels = data
        ouputs = net(images)
        _,predicted = torch.max(outputs.data ,1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
print('Accuracy of the network on the 10000 test images %d %%'%(100*correct/total))        


# In[ ]:




