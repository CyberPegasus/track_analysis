import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import re

#py_path = "/home/pegasus/vscode_workspace/py/"
xml_path = "/home/pegasus/vscode_workspace/py/xml/"
txt_save_path = "/home/pegasus/vscode_workspace/py/txt/"
classes=["drone"]

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def read_and_write(nameID):
    in_file = open(xml_path+nameID+'.xml',encoding='UTF-8')
    out_file = open(txt_save_path+nameID+'.txt','w',encoding='UTF-8')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        cls = obj.find('name').text
        difficult = obj.find('difficult').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        xml_bbox = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        txt_bbox = convert((w,h),xml_bbox)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in txt_bbox]) + '\n')

#print("current_path:"+py_path)
print("xml_path:"+xml_path)
print("txt_save_path:"+txt_save_path)
filelist = os.listdir(xml_path)
for file in filelist:
    if os.path.splitext(file)[1] == '.xml':#目录下包含.json的文件
        name=os.path.splitext(file)[0]
        read_and_write(name)
