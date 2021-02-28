import cv2

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cv2.waitKey(33) != ord('q'):
    ret, frame = capture.read()
    if cv2.waitKey(33) == 32:
        print("asdjfk")
    flipped = cv2.flip(frame, 1)
    cv2.imshow("VideoFrame", flipped)

capture.release()
cv2.destroyAllWindows()