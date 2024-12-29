import cv2
import pytesseract
from pytesseract import Output
import re

# Camera
cap = cv2.VideoCapture(0)

# Function to extract and display timefrom detected text
def extract_time_and_date(text):
    time_pattern = re.compile(r'\b(\d{1,2}:\d{2})\b')

    times = time_pattern.findall(text)

    if times:
        print("Detected time(s):", ", ".join(times))

while True:
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Adjust these coordinates as needed, I limited field of view otherwise it will use a lot of resources of your CPU
    x, y, w, h = 200, 10, 200, 90
    roi = gray[y:y+h, x:x+w]

    # Draw the rectangle around the ROI to understand where you have to show your clock
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Perform OCR on the ROI
    ocr_result = pytesseract.image_to_string(roi, config='--psm 6', output_type=Output.STRING)

    # Extract time information
    extract_time_and_date(ocr_result)

    for i, line in enumerate(ocr_result.split('\n')):
        cv2.putText(frame, line, (x, y + h + 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

