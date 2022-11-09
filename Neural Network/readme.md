# NN network

# BPNN (Matlab, Pytorch)
BackPropagation Neural Network (BPNN)
![](./fig/nnwork.png)

## Train phase
Input: parameter (number) and Turelabel (Predictive value)

## Test Phase
Input: Parameter,  
Output: predevtive value, 
Erro: (Predective value, Ture label)

## Valid phase

Example
Use roughness value to evaluate the slip strength reduction.
### BPNN
- [Use matlab](https://github.com/ChenYu-K/Data-Processing/blob/7d6f18b26541e2dca5fdfdfc1d557058742c3a57/Neural%20Network/BPNN-slip%20coefficient.m)   
- [Use Pytorch](https://github.com/ChenYu-K/Data-Processing/blob/main/Neural%20Network/ANN_train.py)

## Error evaluate

Mean Absolute Error

$$\mathrm{MAE}=\frac{1}{\mathrm{~m}} \sum_{\mathrm{j}=1}^{\mathrm{m}}\left|\widehat{\mathrm{y}_{\mathrm{j}}}-\mathrm{y}_{\mathrm{j}}\right|$$

Root-mean-square deviation

$$
\operatorname{RMSE}=\sqrt{\frac{1}{\mathrm{n}} \sum_{\mathrm{i}=1}^{\mathrm{n}}\left(\widehat{\mathrm{y}_{\mathrm{j}}}-\mathrm{y}_{\mathrm{j}}\right)^2}
$$

correlation coefficient

$$
R^2=\frac{\left[\sum_{j=1}^m\left(y_j-\bar{y}\right)\left(\widehat{y_j}-\bar{y}\right)\right]^2}{\sum_{j=1}^m\left(y_j-\bar{y}\right)^2 \sum_{j=1}^m\left(\widehat{y_j}-\bar{y}\right)^2}
$$

# CNN (Pytorch)
Use Resnet and Obeject detective to check the bolt axial force and bolt head.

![cnn](./fig/boltcnn.png)

![](./fig/rescnn_bolt.png)
