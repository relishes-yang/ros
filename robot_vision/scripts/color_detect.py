#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import cv2
import numpy as np

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import String

class ColorDetector:

    def __init__(self):

        rospy.init_node('color_detector')

        self.bridge = CvBridge()

        # 订阅摄像头图像
        self.image_sub = rospy.Subscriber(
            "/cv_camera/image_raw",
            Image,
            self.image_callback
        )

        # 发布中心坐标
        self.position_pub = rospy.Publisher(
            "/color_position",
            String,
            queue_size=10
        )

    def image_callback(self, msg):

        # ROS图像转OpenCV
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")

        # 调整分辨率
        frame = cv2.resize(frame, (640, 480))

        # 高斯滤波
        blur = cv2.GaussianBlur(frame, (5,5), 0)

        # HSV颜色空间
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        # ======================
        # 红色HSV范围
        # ======================

        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])

        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

        mask = mask1 + mask2

        # ======================
        # 形态学处理
        # ======================

        kernel = np.ones((5,5), np.uint8)

        # 开运算
        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            kernel
        )

        # 闭运算
        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            kernel
        )

        # ======================
        # 查找轮廓
        # ======================

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        for cnt in contours:

            area = cv2.contourArea(cnt)

            # 过滤小面积
            if area < 2000:
                continue

            x, y, w, h = cv2.boundingRect(cnt)

            # 长宽比过滤
            ratio = float(w) / h

            if ratio < 0.5 or ratio > 2.0:
                continue

            # 计算中心点
            cx = int(x + w/2)
            cy = int(y + h/2)

            # 绘制矩形框
            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0,255,0),
                2
            )

            # 绘制中心点
            cv2.circle(
                frame,
                (cx, cy),
                5,
                (255,0,0),
                -1
            )

            # 显示坐标
            text = "x:{} y:{}".format(cx, cy)

            cv2.putText(
                frame,
                text,
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,0),
                2
            )

            # 发布ROS话题
            self.position_pub.publish(text)

            rospy.loginfo(text)

        # 显示窗口
        cv2.imshow("Color Detection", frame)

        # 显示mask调试窗口
        cv2.imshow("Mask", mask)

        cv2.waitKey(1)

if __name__ == '__main__':

    try:
        ColorDetector()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
