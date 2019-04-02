import cv2 as cv
import math
import numpy as np

class Pic:
    def __init__(self, name, path):
         self.name=name
         self.path=path
         self.img=cv.imread(path,0)
    def show(self):
        print("data is {}".format(self.img))
        cv.imshow("7.bmp",self.img)
        cv.waitKey(30)
    def cal_h(self,method, temp_distance, n, d0, height, width):
        if method == 'butterworth_lowpass':
            return 1/(1 + (temp_distance/d0)**(2*n))
        elif method == 'gaussian_lowpass':
            return np.exp(-((temp_distance/d0)**2)/2)
        elif method == 'butterworth_highpass':
            return 1/(1 + (d0/temp_distance)**(2*n))
        elif method == 'gaussian_highpass':
            return 1 - np.exp(-((temp_distance/d0)**2)/2)
        elif method == 'laplace_highpass':
            return 4*temp_distance**2/(height**2+width**2)
        elif method == 'unmask_highpass':
            return 0.5 + 0.75*(1 - np.exp(-((temp_distance/50)**2)/2))
        else:
            print("[ERORR]:Invalid filter:{}!".format(method))
            return 0
    def filter(self,method,n,d0,task_num):
        height, width = self.img.shape
        frequency = np.fft.fft2(self.img)
        transformed = np.fft.fftshift(frequency)
        power1 = sum(np.abs(sum(transformed ** 2)))
        for i in range(height):
            for j in range(width):
                temp_distance = np.sqrt((i - height / 2) ** 2 + (j - width / 2) ** 2)
                H = self.cal_h(method,temp_distance=temp_distance, n=n, d0=d0, height=height, width=width)
                transformed[i][j] = transformed[i][j] * H
        power2 = sum(np.abs(sum(transformed ** 2)))
        freq_image = 20*np.log(np.abs(transformed) + 1)
        filted_image = np.abs(np.fft.ifft2(transformed))
        cv.imwrite('/home/hanninglin/Documents/CV/PROJECT/hw5/img/{}-{}_of_{}_n-{}_d0-{}_sr-{}.bmp'.format(task_num,method,self.name,n,d0,100*power2/power1),filted_image)
        print("[LOG]:{}-{}_of_{}_n:{}_d0:{}_sr:{}.bmp created sucessfully!".format(task_num,method,self.name,n,d0,100*power2/power1))
        print("!!!!!![RESULT]:spetral_ratio={}".format(100*power2/power1))

# 比较并讨论空域低通高通滤波（Project3）与频域低通和高通的关系；
# 按标准格式提交报告； 
test1=Pic("test1","/home/hanninglin/Documents/CV/PROJECT/hw5/test1.pgm")
test2=Pic("test2","/home/hanninglin/Documents/CV/PROJECT/hw5/test2.tif")
test3=Pic("test3_corrupt","/home/hanninglin/Documents/CV/PROJECT/hw5/test3_corrupt.pgm")
test4=Pic("test4","/home/hanninglin/Documents/CV/PROJECT/hw5/test4.tif")
test4_copy=Pic("test4","/home/hanninglin/Documents/CV/PROJECT/hw5/test4 copy.bmp")
print("[LOG]:All object created successfully!\n")
print("#ANS:5-1\n")
print("------------------------------------------")
# 1频域低通滤波器：设计低通滤波器包括 butterworth and Gaussian (选择合适的半径，计算功率谱比),平滑测试图像test1和2;分析各自优缺点；
d0=[10,20,40,100]
for i in range(4):
    test1.filter('gaussian_lowpass',i,d0[i],1)
    test2.filter('gaussian_lowpass',i,d0[i],1)
    for j in range(4):
        test1.filter('butterworth_lowpass',i,d0[j],1)
        test2.filter('butterworth_lowpass',i,d0[j],1)
        
print("\n#ANS:5-2\n")
print("------------------------------------------")
# 2频域高通滤波器：设计高通滤波器包括butterworth and Gaussian，在频域增强边缘。选择半径和计算功率谱比，测试图像test3,4：分析各自优缺点；
for i in range(4):
    test3.filter('gaussian_highpass',i,d0[j],2)
    test4.filter('gaussian_highpass',i,d0[j],2)
    for j in range(4):
        test3.filter('butterworth_highpass',i,d0[j],2)
        test4.filter('butterworth_highpass',i,d0[j],2)
        

print("\n#ANS:5-3\n")
print("------------------------------------------")
# 3其他高通滤波器：拉普拉斯和Unmask，对测试图像test3,4滤波；分析各自优缺点；
test3.filter('laplace_highpass',0,0,3)
test4.filter('laplace_highpass',0,0,3)
test3.filter('unmask_highpass',0,0,3)
test4.filter('unmask_highpass',0,0,3)