import cv2
import keyboard

color = {"blue": (255, 0, 0), "red": (0, 0, 255), "green": (0, 255, 0), "white": (255, 255, 255)}


def nose(img, faceCascade):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    features = faceCascade.detectMultiScale(gray_img, 1.1, 8)
    nc = []
    for (x, y, w, h) in features:
        nc = ((2 * x + w) / 2, (2 * y + h) / 2)
    return img, nc


def controller(img, cords):
    size = 30
    x1 = cords[0] - size
    y1 = cords[1] - size
    x2 = cords[0] + size
    y2 = cords[1] + size
    cv2.circle(img, cords, size, color['red'], 2)
    return [(x1, y1), (x2, y2)]


def keyboard_events(nc, cords, cmd):
    try:
        [(x1, y1), (x2, y2)] = cords
        xc, yc = nc
    except Exception as e:
        print(e)
        return
    if xc < x1:
        cmd = "left"
    elif (xc > x2):
        cmd = "right"
    elif (yc < y1):
        cmd = "up"
    elif (yc > y2):
        cmd = "down"
    if cmd:
        print("Detected movement: ", cmd, "\n")
        keyboard.press_and_release(cmd)
    return img, cmd


def reset_press_flag(nc, cords, cmd):
    try:
        [(x1, y1), (x2, y2)] = cords
        xc, yc = nc
    except:
        return True, cmd
    if x1 < xc < x2 and y1 < yc < y2:
        return True, None
    return False, cmd


faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

video_capture = cv2.VideoCapture(0)

width = video_capture.get(3)
height = video_capture.get(4)
press_flag = False
cmd = ""

while True:

    _, img = video_capture.read()
    img = cv2.flip(img, 1)

    img, nc = nose(img, faceCascade)
    cv2.putText(img, cmd, (10, 50), cv2.FONT_HERSHEY_DUPLEX, 2, color['white'], 2, cv2.LINE_4)

    cords = controller(img, (int(width / 2), int(height // 2)))
    if press_flag and len(nc):
        img, cmd = keyboard_events(nc, cords, cmd)
    press_flag, cmd = reset_press_flag(nc, cords, cmd)

    cv2.imshow("face detection", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()

cv2.destroyAllWindows()
