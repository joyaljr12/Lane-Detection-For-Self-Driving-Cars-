This project is a lane detection system using OpenCV that processes video footage to identify road lane markings. It starts by preprocessing each video frame through a series of image processing techniques, including converting the image to grayscale, applying Gaussian blur to reduce noise, and using Canny edge detection to highlight edges. The region of interest (ROI) is then masked to focus on the area where road lanes are expected. Hough Line Transform is used to detect lines in the processed image, and the detected lines are filtered based on their slope to differentiate between left and right lanes. The slopes and intercepts of multiple lines are averaged to create smooth, continuous lane markings. These detected lanes are overlaid on the original video frame and displayed in real-time, allowing for robust lane detection even in noisy or complex road conditions. This system can be applied in self-driving car technologies, road safety systems, and real-time lane monitoring applications.
1. Convert the input image to grayscale and apply Gaussian Blur to the image

   ![Blur](https://github.com/user-attachments/assets/2ffca067-c879-4338-873c-e7ea1fc7b856)

2. Apply the Canny function: Apply the Canny function on the image in the previous step to create an image that shows all the edges. The Canny function generates edges by measuring the gradients of adjacent pixels and identifying the edges 
   where there is high change in the gradients:

    ![canny](https://github.com/user-attachments/assets/b55cd73c-9256-47aa-a96f-92b931592879)
