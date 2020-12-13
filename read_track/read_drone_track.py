import xml.etree.ElementTree as ET
import os

# file from 459 to 503
xml_read_path = "C:/Work_Space/PycharmProjects/read_track/drone/xml_label/"
xml_save_path = "C:/Work_Space/PycharmProjects/read_track/drone/drone_track.txt"
txt_write_form = "Time_ID class xmean ymean xmin ymin xmax ymax img_width img_height img_depth"
classes_operated = ["drone"]


def read_and_write(nameID):
    in_file = open(xml_read_path + nameID + '.xml', encoding='UTF-8')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    depth = int(size.find('depth').text)
    with open(xml_save_path, mode='a') as output_txt:
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            if class_name not in classes_operated:  # or int(obj[3])==1
                continue
            Time_ID = nameID
            bndbox = obj.find('bndbox')
            xmean = round(0.5 * float(bndbox.find('xmin').text) + 0.5 * float(bndbox.find('xmax').text), 3)
            ymean = round(0.5 * float(bndbox.find('ymin').text) + 0.5 * float(bndbox.find('ymax').text), 3)
            bbox = (int(bndbox.find('xmin').text), int(bndbox.find('ymin').text), int(bndbox.find('xmax').text),
                    int(bndbox.find('ymax').text))
            output_txt.write(str(Time_ID) + " " + str(class_name) +" "+str(xmean)+" "+str(ymean)+" "
                             +" ".join(str(a) for a in bbox)+" "+str(width) +" "+ str(height) + " "+str(depth) + '\n')


if __name__ == "__main__":
    print("xml_read_path:" + xml_read_path)
    print("xml_save_path:" + xml_save_path)
    with open(xml_save_path, mode='w') as output_txt:
        output_txt.write(txt_write_form)

    file_list = os.listdir(xml_read_path)
    count = 0
    for file in file_list:
        count+=1
        print("file "+str(count)+" finished.")
        if os.path.splitext(file)[1] == '.xml':  # splitext将文件分为文件名与拓展名
            file_name = os.path.splitext(file)[0]
            read_and_write(file_name)
