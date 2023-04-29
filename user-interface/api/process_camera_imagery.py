import base64
import numpy as np
import cv2
from skimage import color

def normalize_data(frame, vmin, vmax):
    frame = np.array(frame).reshape(24, 32)
    return (frame - vmin) / (vmax - vmin)

def apply_colormap(norm_frame, colormap):
    vec_colormap = np.vectorize(colormap, otypes=[np.uint8, np.uint8, np.uint8])
    img_data_r, img_data_g, img_data_b = vec_colormap(norm_frame, colormap)
    img_data = np.stack((img_data_r, img_data_g, img_data_b), axis=-1)
    return img_data

def map_colors(val):
    return tuple(color.hsv2rgb(1 - val, 1, 1) * 255)

def smooth_image(img, new_size=(64, 48)):
    interpolated = cv2.resize(img, new_size, interpolate=cv2.INTER_CUBIC)
    return cv2.GaussianBlur(interpolated, (3, 3), 0)

def create_image(img_data):
    return cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR)

def process_frame(frame, min_temp=0, max_temp=60):
    normalized = normalize_data(frame, min_temp, max_temp)
    mapped = apply_colormap(normalized, map_colors)
    smoothed = smooth_image(mapped)
    return create_image(smoothed)

def encode_frame(frame):
    frame_str = cv2.imencode('.jpg', frame)[1].tostring()
    return base64.b64encode(frame_str).decode('utf-8')

