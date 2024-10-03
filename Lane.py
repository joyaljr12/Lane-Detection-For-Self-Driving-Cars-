import cv2
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate coordinates for a line based on slope and intercept
def make_coordinates(lane_image, line_parameters):
    if len(line_parameters) != 2:  # Ensure it has slope and intercept
        raise ValueError("Expected two parameters: slope and intercept")

    slope, intercept = line_parameters
    y1 = lane_image.shape[0]  # Set y1 to the bottom of the image
    y2 = int(y1 * 3 / 5)  # Set y2 to 3/5th of the image height (closer to the center)
    x1 = int((y1 - intercept) / slope)  # Calculate x1 based on slope and intercept
    x2 = int((y2 - intercept) / slope)  # Calculate x2 based on slope and intercept
    return np.array([x1, y1, x2, y2])  # Return the coordinates of the line

# Function to average the slope and intercept of detected lines and categorize into left/right lanes
def average_slope_intercept(lane_image, lines):
    left_fit = []  # List to store left lane line slopes and intercepts
    right_fit = []  # List to store right lane line slopes and intercepts
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            # Fit a linear polynomial (line) to the points and return slope and intercept
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]  # Get the slope
            intercept = fit[1]  # Get the intercept
            if slope < 0:  # Negative slope indicates a left lane line
                left_fit.append((slope, intercept))
            else:  # Positive slope indicates a right lane line
                right_fit.append((slope, intercept))
    
    # Calculate the average slope and intercept for the left lane
    left_fit_average = np.average(left_fit, axis=0) if left_fit else None
    
    # Calculate the average slope and intercept for the right lane
    right_fit_average = np.average(right_fit, axis=0) if right_fit else None
    
    # Convert the average slope and intercept to line coordinates
    left_line = make_coordinates(lane_image, left_fit_average) if left_fit_average is not None else None
    right_line = make_coordinates(lane_image, right_fit_average) if right_fit_average is not None else None
    
    return left_line, right_line  # Return both the left and right lines

# Function to process the image by converting it to grayscale, blurring it, and applying Canny edge detection
def process_image(lane_image):
    gray = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)  # Convert the image to grayscale
    blur = cv2.GaussianBlur(gray, (5,5), 0)  # Apply Gaussian blur to reduce noise
    canny = cv2.Canny(blur, 50, 150)  # Apply Canny edge detection with low and high thresholds
    return canny  # Return the edge-detected image

# Function to mask the region of interest (typically the area where lane lines are expected)
def region_of_interest(lane_image):
    height = lane_image.shape[0]  # Get the height of the image
    # Define a triangular polygon that represents the region of interest (bottom center of the image)
    polygons = np.array([[(200, height), (1100, height), (550, 250)]])
    mask = np.zeros_like(lane_image)  # Create a black mask of the same size as the image
    cv2.fillPoly(mask, polygons, 255)  # Fill the region of interest with white (255)
    masked_image = cv2.bitwise_and(lane_image, mask)  # Mask the image to focus only on the region of interest
    return masked_image  # Return the masked image

# Function to draw lines on a blank image
def display_lines(lane_image, lines):
    line_image = np.zeros_like(lane_image)  # Create an empty image to draw lines on
    if lines is not None:
        for line in lines:
            if line is not None:  # Ensure the line is not None
                x1, y1, x2, y2 = line.reshape(4)  # Reshape the line coordinates to (x1, y1, x2, y2)
                # Draw the line on the blank image
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)  # Draw blue lines with thickness 10
    return line_image  # Return the image with the lines drawn

# Capture video from the specified file
cap = cv2.VideoCapture("test2.mp4")

# Loop through video frames
while cap.isOpened():
    ret, frame = cap.read()  # Read a frame from the video

    if not ret or frame is None:
        print("Error: Could not read frame from video or end of video reached.")
        break

    # Process the frame
    processed_image = process_image(frame)  # Apply Canny edge detection
    cropped_image = region_of_interest(processed_image)  # Mask the region of interest

    # Detect lines in the cropped image using Hough Transform
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    
    if lines is not None:
        # Average the detected lines and draw them
        averaged_lines = average_slope_intercept(frame, lines)
        line_image = display_lines(frame, averaged_lines)
        # Combine the original frame with the lines image
        combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

        # Display the final result
        cv2.imshow('result', combo_image)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break
    else:
        print("No lines detected in this frame.")

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
