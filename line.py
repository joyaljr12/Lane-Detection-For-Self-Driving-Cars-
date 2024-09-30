import cv2
import numpy as np
import matplotlib.pyplot as plt

def make_coordinates(lane_image, line_parameters):
    if len(line_parameters) != 2:  # Ensure it has slope and intercept
        raise ValueError("Expected two parameters: slope and intercept")

    slope, intercept = line_parameters
    y1 = lane_image.shape[0]
    y2 = int(y1 * 3 / 5)
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])

def average_slope_intercept(lane_image, lines):
    left_fit = []
    right_fit = []
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            fit = np.polyfit((x1, x2), (y1, y2), 1)  # Returns slope and intercept
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))
    
    # Handle empty fits
    if left_fit:
        left_fit_average = np.average(left_fit, axis=0)
    else:
        left_fit_average = None
    
    if right_fit:
        right_fit_average = np.average(right_fit, axis=0)
    else:
        right_fit_average = None
    
    left_line = make_coordinates(lane_image, left_fit_average) if left_fit_average is not None else None
    right_line = make_coordinates(lane_image, right_fit_average) if right_fit_average is not None else None
    
    return left_line, right_line


def process_image(lane_image):
    gray = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY) # used to convert 3 channel RGB to 1 channel Gray 
    blur = cv2.GaussianBlur(gray, (5,5), 0) # 5 by 5 kernal guassian function used to reduce the noise in the gray sacle image
    canny = cv2.Canny(blur, 50, 150) #outline the strongest gradient in the image(edge detection) 150(high threeshold), 50(low threeshold)
    return canny


def region_of_interest(lane_image):
    height = lane_image.shape[0]
    polygons = np.array([
        [(200, height), (1100, height), (550, 250)] #get from matplot image of proceesed image(canny image)
        ])
    mask = np.zeros_like(lane_image) # this code is used to display the mask on black image
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(lane_image, mask)
    return masked_image


def display_lines(lane_image, lines):
    line_image = np.zeros_like(lane_image)  # Create an empty image
    if lines is not None:
        for line in lines:
            if line is not None:  # Check if line is not None
                x1, y1, x2, y2 = line.reshape(4)  # Ensure the line is not None before reshaping
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image





# Existing functions (make_coordinates, average_slope_intercept, etc.) are assumed to be the same

cap = cv2.VideoCapture("D:\\Line Detection\\test2.mp4")

while cap.isOpened():
    ret, frame = cap.read()

    if not ret or frame is None:
        print("Error: Could not read frame from video or end of video reached.")
        break

    # Process the frame if successfully read
    processed_image = process_image(frame)
    cropped_image = region_of_interest(processed_image)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    
    if lines is not None:
        averaged_lines = average_slope_intercept(frame, lines)
        line_image = display_lines(frame, averaged_lines)
        combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

        # Display the result
        cv2.imshow('result', combo_image)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break
    else:
        print("No lines detected in this frame.")

# Release the video capture and destroy all windows
cap.release()
cv2.destroyAllWindows()



   
