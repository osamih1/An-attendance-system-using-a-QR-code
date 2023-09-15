import cv2
from pyzbar.pyzbar import decode
import numpy as np
import datetime
import time

with open("authorized_users.txt", "r") as f:
    authorized_users = [l[:-1] for l in f.readlines()]
    f.close()

most_recent_access = {}
time_between_logs_th = 5

cap = cv2.VideoCapture(0)

ret = True
while ret:
    ret, frame = cap.read()
    qr_info = decode(frame)
    if len(qr_info) > 0:
        qr_info = qr_info[0]
        data = qr_info.data
        rect = qr_info.rect
        polygon = qr_info.polygon

        if data.decode() in authorized_users:
            cv2.putText(frame, "ACCESS GRANTED", (rect.left, rect.top-15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

            if data.decode() not in most_recent_access.keys() \
                    or time.time() - most_recent_access[data.decode()] > time_between_logs_th:
                most_recent_access[data.decode()] = time.time()
                with open("logs.txt", "a") as f:
                    print(datetime.datetime.now())
                    f.write(f"{data.decode()} {datetime.datetime.now()}\n")
                    f.close()
        else:
            cv2.putText(frame, "ACCESS DENIED", (rect.left, rect.top-15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

        frame = cv2.rectangle(frame, (rect.left, rect.top), (rect.left+rect.width, rect.top+rect.height), (0,255,0), 5)
        frame = cv2.polylines(frame, [np.array(polygon)], True, (255,0,0), 5)

    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break