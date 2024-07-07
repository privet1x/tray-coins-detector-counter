import numpy as np
import cv2 as cv

# Read the image, apply blur, and convert to grayscale
img_original = cv.imread('tray8.jpg', cv.IMREAD_COLOR)
img_blur = cv.medianBlur(img_original, 21)
img_gray = cv.cvtColor(img_blur, cv.COLOR_BGR2GRAY)

# Get binary level photo and contours
ret, thresh = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# Find the contour of the TRAY - it is the contour with the biggest area
imax = 0
areamax = 0
for i, contour in enumerate(contours):
    area = cv.contourArea(contour)
    if area > areamax:
        imax = i
        areamax = area
tray = contours[imax]

# Draw the tray contour
cv.drawContours(img_original, [tray], 0, (0, 255, 0), 3)

# Find circles using Hough Transform
circles = cv.HoughCircles(img_gray, cv.HOUGH_GRADIENT, dp=1, minDist=20,
                          param1=50, param2=25, minRadius=20, maxRadius=40)

circles = np.uint16(np.around(circles))

# Draw circles
for i in circles[0, :]:
    center = (i[0], i[1])
    radius = i[2]
    # Draw the outer circle
    cv.circle(img_original, center, radius, (255, 0, 0), 2)
    # Draw the center of the circle
    cv.circle(img_original, center, 2, (0, 0, 255), 3)

# Initialize counts
big_coin_in_tray = 0
small_coin_in_tray = 0
big_coin_out_tray = 0
small_coin_out_tray = 0

big_coin_radius_threshold = 31 #by pixels found

# Calculate coins
for i in circles[0, :]:
    center = (i[0], i[1])
    radius = i[2]

    # Check if the center of the circle is inside the tray contour
    distance = cv.pointPolygonTest(tray, center, True)
    inside = distance >= 0

    if inside:
        if radius >= big_coin_radius_threshold:
            big_coin_in_tray += 1
        else:
            small_coin_in_tray += 1
    else:
        if radius >= big_coin_radius_threshold:
            big_coin_out_tray += 1
        else:
            small_coin_out_tray += 1

# Annotate the image with counts
cv.putText(img_original, "BigCoinInTray = " + str(big_coin_in_tray), (50, 50),
           fontFace=cv.FONT_HERSHEY_DUPLEX, fontScale=1.0, color=(255, 0, 0), thickness=2)
cv.putText(img_original, "BigCoinOutTray = " + str(big_coin_out_tray), (50, 100),
           fontFace=cv.FONT_HERSHEY_DUPLEX, fontScale=1.0, color=(255, 0, 0), thickness=2)
cv.putText(img_original, "SmallCoinInTray = " + str(small_coin_in_tray), (50, 150),
           fontFace=cv.FONT_HERSHEY_DUPLEX, fontScale=1.0, color=(255, 0, 0), thickness=2)
cv.putText(img_original, "SmallCoinOutTray = " + str(small_coin_out_tray), (50, 200),
           fontFace=cv.FONT_HERSHEY_DUPLEX, fontScale=1.0, color=(255, 0, 0), thickness=2)
cv.putText(img_original, "Area = " + str(areamax), (50, 250),
           fontFace=cv.FONT_HERSHEY_DUPLEX, fontScale=1.0, color=(255, 0, 0), thickness=2)

# Display results
img_resized = cv.resize(img_original, (0, 0), fx=0.8, fy=0.8)
cv.imshow('COINS', img_resized)
cv.waitKey(0)
