import time
import threading
import board
import busio
import numpy as np
import adafruit_mlx90640


class ThermalCamera:
    PROCESSING_DELAY = 0.1

    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
        self.mlx = adafruit_mlx90640.MLX90640(self.i2c)
        self.mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
        self.mlx_shape = (24, 32)
        self.mlx_pixels = self.mlx_shape[0] * self.mlx_shape[1]

    def get_frame(self):
        frame = np.zeros((self.mlx_pixels,))
        self.mlx.getFrame(frame)
        return np.reshape(frame, self.mlx_shape)

    def stream(self, callback):
        while True:
            try:
                callback(self.get_frame())
                time.sleep(ThermalCamera.PROCESSING_DELAY)
            except KeyboardInterrupt:
                return


thermal_camera = ThermalCamera()


def start_stream(callback):
    camera_imagery_thread = threading.Thread(
        target=thermal_camera.stream, args=(callback,)
    )
    camera_imagery_thread.start()
