import cv2
import time
import serial
import numpy as np
from pyzbar.pyzbar import decode

def connect_to_arduino(port, baud_rate=9600, simulate=False):
    if simulate:
        return None
    try:
        return serial.Serial(port, baud_rate)
    except serial.SerialException as e:
        print(f"Failed to connect on {port}: {e}")
        exit(1)
def send_command(ser, command):
    if ser is None:
        print(f"Simulated command: {command}")
        return
    try:
        ser.write((command + '\n').encode())  # Ensure the command ends with a newline
        print(f"Sent '{command}' to Arduino")
    except serial.SerialException as e:
        print(f"Error sending data: {e}")
        exit(1)

# The QR code value you want to match
target_qr_code = "https://example.com"
cv2_reader = cv2.QRCodeDetector()
cap = cv2.VideoCapture(1)

try:
    ser = connect_to_arduino(port="COM10", baud_rate=9600, simulate=False)
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            break

        try:
            cv2_out, cord, _ = cv2_reader.detectAndDecode(frame)
            if cv2_out == target_qr_code:
                cord = cord.tolist()[0]
                top_left = cord[0]
                top_right = cord[1]
                bottom_right = cord[2]
                bottom_left = cord[3]

                top_left = (int(top_left[0]), int(top_left[1]))
                bottom_right = (int(bottom_right[0]), int(bottom_right[1]))

                mid_x = int((top_left[0] + bottom_right[0]) / 2)
                mid_y = int((top_left[1] + bottom_right[1]) / 2)
                area = (bottom_right[0] - top_left[0]) * (bottom_right[1] - top_left[1])
                print(area)
                print(mid_x, mid_y)
                
                # Send movement commands based on area and position
                if area < 100000:
                    send_command(ser, "forward")
                else:
                    send_command(ser, "stop")

                if mid_x < 500:
                    send_command(ser, "left")
                elif mid_x > 750:
                    send_command(ser, "right")
                

                cv2.circle(frame, (mid_x, mid_y), 5, (0, 0, 255), 5)
                cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

        except Exception as e:
            print(f"Error decoding QR code: {e}")
            pass

        cv2.imshow('QR Code Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
