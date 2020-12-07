from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re
import subprocess
import itertools
import io
import json
import cv2
import numpy as np
import requests

def execute(cmd):
#     lcmd = cmd.split()
    cp = subprocess.run(cmd, shell = True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if cp.returncode:
        print('failed: '+cp.stderr)
        
def convert_img(path):
    os.chdir(path)
    files = [file for file in os.listdir() if '.jpg' in file]
    for file in files:
        cmd = "convert {file} -density 300".format(file=file) +\
        " -quality 100 -background white -deskew 80% -fuzz 40% -trim +repage convert/{file}".format(file=file)
        if not os.path.exists('convert'):
            os.mkdir('convert')
    #     print(cmd)
        execute(cmd)

athreshold = np.linspace(100,120,3,dtype=int)
amin_line_length = np.linspace(50,100,3, dtype=int)
amax_line_gap = np.linspace(10,30,3, dtype=int)
#[(1, 1, 1, 100, 50, 10, 1)] (atempi,atemp2i,atemp3i,athreshold,amin_line_length,amax_line_gap,arho))
athreshold = [100]
amin_line_length = [50]
amax_line_gap = [10]
arho = [1]

def cut_img(path):
#     os.chdir(path)
    files = [ file for file in os.listdir(path + '\\convert') if '.jpg' in file]
    dirpath = 'static//cutimg'
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)
    os.makedirs(dirpath, exist_ok = True)
    for file in files:
        file1 = path + '\\convert/' + file
        img = cv2.imread(file1) 
        #X1,Y1,X2,Y2 = #filed[file]/
        X1 = int(img.shape[0]) * 0.55
        X2 = int(img.shape[0]) * 0.70
        y2c = int(img.shape[1]*0.70)
        y1c = int(img.shape[1]*0.15)
        x1c = int(img.shape[0] * 0.15)
        # Taking a matrix of size 5 as the kernel 
        kernel = np.ones((5,5), np.uint8) 
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        low_threshold = 50
        high_threshold = 150
        for i in list(itertools.product(athreshold,amin_line_length,amax_line_gap,arho)):
            list_all = []
            (threshold,min_line_length,max_line_gap,rho) = i
    #         edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
            edges = cv2.Canny(gray,50,150,apertureSize = 3)
            kernel = np.ones((5,5),np.uint8)
            temp3 = cv2.dilate(edges,kernel,iterations = 1)
    #         dis(temp3,file)
            theta = np.pi / 180  # angular resolution in radians of the Hough grid
            line_image = np.copy(img) * 0
            lines = cv2.HoughLinesP(temp3, rho, theta, threshold, np.array([]),
                                min_line_length, max_line_gap)
            www = 0
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if abs(y2-y1) > 500 and x1> X1 and x2 < X2:
                    cv2.line(line_image,(x1,y1),(x2,y2),(255,255,0),5)
                    www =1
                    cv2.imwrite('static\\cutimg/'+file,img[y1c:y2c, x1c:x1])
                    list_all.append(i)
                    break
