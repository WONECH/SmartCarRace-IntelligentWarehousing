#!/usr/bin/python3
# coding:utf8

import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np
import pandas as pd
from sensor_msgs.msg import Image
import rospy

class QRCode_Dect:
    def __init__(self):

        # load parameters
        image_topic = rospy.get_param(
            '~image_topic', '/ep_cam/image_raw')

        self.color_image = Image()
        self.getImageStatus = False

        # image subscribe
        self.color_sub = rospy.Subscriber(image_topic, Image, self.image_callback,
                                          queue_size=1, buff_size=52428800)

        # if no image messages
        while not rospy.is_shutdown():
            while (not self.getImageStatus) :
                rospy.loginfo("waiting for image.")
                rospy.sleep(2)

    def image_callback(self, image):
        self.getImageStatus = True
        self.color_image = np.frombuffer(image.data, dtype=np.uint8).reshape(
            image.height, image.width, -1)
        self.gray = cv2.cvtColor(self.color_image, cv2.COLOR_BGR2GRAY)

        im, rects_list, polygon_points_list, QR_info = self.decodeDisplay(self.gray)

        # 把检测到二维码的信息再绘制到BGR彩色图像上
        for data in zip(rects_list, polygon_points_list, QR_info):
            # print(f"data: {data}")
            x, y, w, h = data[0]
            polygon_points = data[1]
            text = data[2]
            self.write_csv(file_path, text)
            self.drop_duplicate(file_path)
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.polylines(self.color_image, [polygon_points], isClosed=True, color=(255, 0, 255), thickness=2,
                        lineType=cv2.LINE_AA)
            cv2.putText(self.color_image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        .5, (0, 0, 125), 2)

        # 因为一个是单通道的灰度图，一个是BGR三通道的彩色图，因此不能够拼接在一起显示，这里就用两个窗口显示
        cv2.imshow("grey_img", im)
        cv2.imshow("color_img", self.color_image)
        cv2.imwrite("/home/tta/图片/test.png", self.color_image)

        cv2.waitKey(1)

    def write_csv(self, filename, str):
        """
        写入csv
        :param filename:
        :return:
        """
        data = [str]
        df = pd.DataFrame(data)
        # # 保存 dataframe
        df.to_csv(filename, index=None, mode='a')

    def drop_duplicate(self, filename):
        """
        去重
        :param filename:
        :return:
        """
        df = pd.read_csv(filename)
        df.drop_duplicates(inplace=True)
        df.to_csv(filename, index=None, mode='w')

    def decodeDisplay(self, image):
        barcodes = pyzbar.decode(image)
        rects_list = []
        polygon_points_list = []
        QR_info = []

        # 这里循环，因为画面中可能有多个二维码
        for barcode in barcodes:
            # 提取条形码的边界框的位置
            # 画出图像中条形码的边界框
            (x, y, w, h) = barcode.rect
            rects_list.append((x, y, w, h))
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            polygon_points = barcode.polygon

            extract_polygon_points = np.zeros((4, 2), dtype=np.int32)
            for idx, points in enumerate(polygon_points):
                point_x, point_y = points  # 默认得到的point_x, point_y是float64类型
                extract_polygon_points[idx] = [point_x, point_y]

            # print(extract_polygon_points.shape)  # (4, 2)

            # 不reshape成 (4,1 2)也是可以的
            extract_polygon_points = extract_polygon_points.reshape((-1, 1, 2))
            polygon_points_list.append(extract_polygon_points)

            # 绘制多边形
            # cv2.polylines(image, [extract_polygon_points], isClosed=True, color=(255, 0, 255), thickness=2,
            #               lineType=cv2.LINE_AA)

            # 二维码数据为字节对象，所以如果我们想在输出图像上画出来，就需要先将它转换成字符串
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # 绘出图像上条形码的数据和条形码类型
            # text = "{} ({})".format(barcodeData, barcodeType)
            text = barcodeData
            QR_info.append(text)
            # cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
            #             .5, (0, 0, 125), 2)

            # 向终端打印条形码数据和条形码类型
            rospy.loginfo("Found {} barcode: {}".format(barcodeType, barcodeData))
        return image, rects_list, polygon_points_list, QR_info

def main():
    rospy.init_node('QRCode_Dect', anonymous=True)
    qrcode_dect = QRCode_Dect()
    rospy.spin()

def delete_first_line(filename):
    """
    删除0
    :return:
    """
    df = pd.read_csv(filename)
    df.drop(labels=1,inplace=True)
    df.to_csv(filename, index=None, header=None, mode='w')

if __name__ == "__main__":
    file_path = '/home/tta/ws_warehouse/src/warehouse/scripts/test.csv'
    main()
    delete_first_line(file_path)
