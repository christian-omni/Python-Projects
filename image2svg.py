import cv2
import svgwrite
import numpy as np
import sys
import os

def convert_jpeg_to_svg(input_path, output_path):
    # Load and preprocess the image
    img = cv2.imread(input_path)
    if img is None:
        print(f"Could not open file: {input_path}")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create SVG
    dwg = svgwrite.Drawing(output_path, profile='tiny')

    for contour in contours:
        points = [(int(pt[0][0]), int(pt[0][1])) for pt in contour]
        if points:
            dwg.add(dwg.polygon(points=points, fill='black'))
    dwg.save()
    print(f"SVG saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert.py <input.jpg> [output.svg]")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(input_file)[0] + '.svg'
        convert_jpeg_to_svg(input_file, output_file)