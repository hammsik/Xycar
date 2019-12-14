#!/usr/bin/enc python

import rospy, time, cv2
from linedetector_proto import LineDetector
from obstacledetector_proto import ObstacleDetector

class License_test:

    def __init__(self):
        rospy.init_node('xycar_driver')
        self.line_detector = LineDetector('/usb_cam/image_raw')
        self.obstacle_detector = ObstacleDetector('/ultrasonic')
        self.count = 0
        self.depart_start = -5

    def line_test(self):
        line_l, line_r = self.line_detector.detect_lines()
        self.line_detector.show_images(line_l,line_r)
        if 5 < time.time() - self.depart_start:
            if line_l == -1 & line_r == -1:
                self.count += 1
                self.depart_start = time.time()

    def parking_test(self):
        return self.obstacle_detector.get_distance()

    def totalScore(self, line, parking_l, parking_m, parking_r, time):
        if time > 60:
            return 0, "Fail"

        parking = "Success"
        if (parking_l > 3) and (parking_m > 3) and (parking_r > 3):
            totalscore = 100
        else:
            totalscore = 80
            parking = "Fail"

        totalscore -= 5 * line

        return totalscore, parking

    def exit(self):
        print("finished")

if __name__ == '__main__':
    startTime = time.time()
    test_car = License_test()
    time.sleep(3)
    rate = rospy.Rate(15)
    while cv2.waitKey(1) & 0xFF != 27: #escape key
        test_car.line_test()
        rate.sleep()
    while cv2.waitKey(1) & 0xFF != 32: #space bar key
        left, mid, right = test_car.parking_test()
        rate.sleep()

    cv2.destroyAllWindows()
    finishTime = time.time()
    totalTime = finishTime - startTime
    score, result = test_car.totalScore(test_car.count, lefh, mid, right, totalTime)

    #show license result
    print("-" * 40)
    print("Lane Departure : \t%d" %test_car.count)
    print("Parking_mic : \t\t%d" %mid)
    print("Parking_left : \t\t%d" %left)
    print("Parkinf_right :\t%d ... %s" %(right, result))
    print("Running Time : \t\t%.2fsec" %totalTime)

    if score > 60:
        print("\n## PASS ##")
    else:
        print("\n## FAIL ##")
    print("-" * 40)

    rospy.on_shutdown(test_car.exit)
