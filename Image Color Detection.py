import cv2
import pandas as pd
import numpy as np

# Load image
img = cv2.imread("Data\\colours.jpg")

# Resize image to fit window
max_width = 800
max_height = 600
height, width = img.shape[:2]

scale = min(max_width / width, max_height / height)
new_width = int(width * scale)
new_height = int(height * scale)
img = cv2.resize(img, (new_width, new_height))
imgWidth = new_width - 40

# Load color CSV
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv("Data\\colors.csv", header=None, names=index)

# Variables to store color under mouse
r = g = b = xpos = ypos = 0

# Track mouse position
def trackMouse(event, x, y, flags, param):
    global xpos, ypos
    xpos = x
    ypos = y

cv2.namedWindow("Image")
cv2.setMouseCallback("Image", trackMouse)

def colorname(B, G, R):
    minimum = float('inf')
    cname = ""
    for i in range(len(df)):
        d = abs(B-int(df.loc[i,"B"])) + abs(G-int(df.loc[i,"G"])) + abs(R-int(df.loc[i,"R"]))
        if d <= minimum:
            minimum = d
            cname = f"{df.loc[i,'color_name']} Hex:{df.loc[i,'hex']}"
    return cname

while True:
    # Read color under current mouse position
    b, g, r = img[ypos, xpos]
    b = int(b)
    g = int(g)
    r = int(r)

    # Copy image to display
    img_copy = img.copy()
    cv2.rectangle(img_copy, (20, 20), (imgWidth, 60), (b, g, r), -1)
    text = f"{colorname(b, g, r)}   R={r} G={g} B={b}"

    # Choose text color based on brightness
    if r+g+b >= 600:
        cv2.putText(img_copy, text, (50, 50), 2, 0.8, (0,0,0), 2, cv2.LINE_AA)
    else:
        cv2.putText(img_copy, text, (50, 50), 2, 0.8, (255,255,255), 2, cv2.LINE_AA)

    cv2.imshow("Image", img_copy)

    if cv2.waitKey(20) & 0xFF == 27:  # Press ESC to exit
        break

cv2.destroyAllWindows()
