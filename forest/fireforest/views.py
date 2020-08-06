from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib.auth.models import User,auth
import cv2
import numpy as np
import os
# Create your views here.
def index(request):
    return render(request,"index.html") 
def processimg(request):
    if request.method=='POST':
        filename=request.POST['filename']
        ip=imgprocessing(filename)
        ip.pfn()
        return render(request,"output.html")


def processredirect(request):
    return render(request,"uploaddemo.html")

def loginview(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        print(username)
        print(password)
        user=authenticate(request,username=username,password=password)
        print(user)
        if user is not None:
            login(request,user,backend=None)
            return render(request,"uploaddemo.html") 
        else:
            messages.info(request,'invalid credentials!!!')
            return redirect('loginview')
    else:
        return render(request,"loginpage.html") 
def signup(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        #phone_number=request.POST['phone_number']
        username=request.POST['username']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username already exits')
                return redirect('signup')

            else:
                user=User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name)
                user.save()
                messages.info(request,'Successfully created account')
                return redirect('loginview')
        else:
            messages.info(request,'Password not matching')
            return redirect('signup')
        return redirect('/')
    else:
        return render(request,"signuppage.html") 

        
def logoutview(request):
    # auth.logout(request)
    # return redirect('/')
    if request.method=='POST':
        logout(request)
        return render(request,"index.html") 
    else:
        return render(request,"index.html") 
        

class imgprocessing:
    def __init__(self,filename):
        self.filename=filename

    def pfn(self):
        path="C:/projects/2020/UP/forest/static/img/dataset/"
        print(path+self.filename)
        sample=cv2.imread(path+self.filename,0)
        kernel=np.zeros(shape=(3,3))
        kernel[0,0]=-1
        kernel[0,1]=-2
        kernel[0,2]=-1
        kernel[1,0]=0
        kernel[1,1]=0
        kernel[1,2]=0
        kernel[2,0]=1
        kernel[2,1]=2
        kernel[2,2]=1
        gy=self.conv(sample,kernel)
        #cv2.imshow("gradient_y",gy)

        kernel[0,0]=-1
        kernel[0,1]=0
        kernel[0,2]=-1
        kernel[1,0]=-1
        kernel[1,1]=0
        kernel[1,2]=1
        kernel[2,0]=-2
        kernel[2,1]=0
        kernel[2,2]=2
        gx=self.conv(sample,kernel)
        #cv2.imshow("gradient_x",gx)
        g_sobel=self.norm(gx,gy)

        #cv2.imshow("Sobel_edge",g_sobel)
        #cv2.imwrite('Processed_img.png',g_sobel)


        path = 'C:/dummyproj/forest/static/img/Processedimages/'
        cv2.imwrite(os.path.join(path , 'p2.jpg'),g_sobel )
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    

    


    def conv_transform(self,image):
        image_copy=image.copy()
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                image_copy[i][j]=image[image.shape[0]-i-1][image.shape[1]-j-1]
        return image_copy



    def conv(self,image,kernel):
    #the image will be grayscale,otherwise there will be confusion with 3
        kernel=self.conv_transform(kernel)
        image_h=image.shape[0]
        image_w=image.shape[1]

        kernel_h=kernel.shape[0]
        kernel_w=kernel.shape[1]
        h=kernel_h//2#integer
        w=kernel_w//2

        image_conv=np.zeros(image.shape)
        for i in range(h,image_h-h):
            for j in range(w,image_w-w):
                sum=0

                for m in range(kernel_h):
                    for n in range(kernel_w):
                        sum=(sum+kernel[m][n]*image[i-h+m][j-w+n])
            
                image_conv[i][j]=sum
    #cv2.imshow('Convolved_image',image_conv)
        return image_conv


    #SOBEL_FILEDMAN EDGE
    def norm(self,img1,img2):
        img_copy=np.zeros(img1.shape)#image with initial zero values
    #img_copy=img1.copy()
        for i in range(img1.shape[0]):
            for j in range(img1.shape[1]):
                q=(img1[i][j]**2+img2[i][j]**2)**(1/2)
                if(q>200):#threshold
                    img_copy[i][j]=255 #Obtaining a binary image
                else:
                    img_copy[i][j]=0
        return img_copy


