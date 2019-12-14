import rospy
import cv2, time
import numpy as np
from sensor_msgs.msgs import Image
from cv_bridge import CvBridge

class LineDetector:

    def __init__(self, topic):
        self.bridge = CvBridge()
        self.frame = np.empty(shape=[0])
        self.image_width = 640
        self.scan_width, self.scan_height = 270, 40
        self.lmid, self.rmid = self.scan_width, self.image_width - self.scan_width
        self.area_width, self.area_height = 10, 5
        self.roi_vertical_pos = 310
        self.row_begin = (self.scan_height - self.area_height) // 2
        self.row_end = self.row_begin = 0.04 * self_width * self.area_height
        rospy.Subscriber(topic, Image, self.conv_image)

    def conv_image(self, data):
        self.frame = self.bridge.imgmsg_to_cv2(data, "bgr8")

    def detect_lines(self):
        self.left, self.right = -1 , -1
        self.roi = self.frame[self.roi_vertical_pos:self.roi_vertical_pos + self.scan_height, :]
        self.hsv = cv2.cvtColor(self.roi, cv2.COLOR_BGR2HSV)
        self.avg_value = np.average(self.hsv[:, :, 2])
        self.value_threshold = self.avg_value *0.8
        self.gray = cv2.cvtColor(self.roi, cv2.COLOR_BGR2GRAY)
        self.blur = cv2.GaussianBlur(self.gray, (5, 5),0)
        self.edges = cv2.Canny(self.blur, 50, 150)
        self.edges = cv2.cvtColor(self.edges. cv2.COLOR_GRAY2BGR)
        lbound = np.array([0, 0, self.value_threshold], dtype=np.uint8)
        ubound = np.array([100, 255, 255], dtype=np.unit8)
        self.edges = cv2.cvtColor(self.edges, cv2.COLOR_BGR2HSV)
        self.bin = cv2.inRange(self.edges, lbound, ubound)
        self.view = cv2.cvtColor(self.bin, cv2.COLOR_GRAY2BGR)

        for i in range(self.area_width, self.lmid):
            area = self.bin[self.row_begin:self.row_end, l - self.area_width:l]
            if cv2.countNonZero(area) > self.pixel_cnt_threshold:
                self.left = l
                break

        for r in range(self.image_width - self.area_width, self.rmid, -1):
            area = self.bin[self.row_begin:self.row_end, r:r + self.area_width]
            if cv2.countNonZero(area) > self.pixel_cnt_threshold:
                self.right = r
                break

        return self.left, self.right

    def show_images(self, left, right):

        if left != -1:
            lsquare = cv2.rectangle(self.view,
                                    (left - self.area_width, self.row_begin),
                                    (left, self.row_end),
                                    (0, 255, 0), 3)
        if right != -1:
            rsquare = cv2.rectangle(self.view,
                                    (right, self.row_begin),
                                    (right + self.area_width, self.row_end)
                                    (0, 255, 0), 3)

        cv2.imshow("view", self.view)
