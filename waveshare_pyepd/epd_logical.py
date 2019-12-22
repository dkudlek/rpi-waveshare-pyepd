# *****************************************************************************
# * | File        :	  epd7in5bc.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V4.0
# * | Date        :   2019-06-20
# # | Info        :   python3 demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and//or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import time
from PIL import Image
import logging

try:
    from . import epd_physical as epdif
except:
    from . import fake_physical as epdif

display_variants = {"epd7in5":{
                            "name": "7.5inch e-paper HAT",
                            "height": 384,
                            "width": 640,
                            "color": "bw"},
                    "epd7in5bc":{
                             "name": "7.5inch e-paper HAT (B) or (C)",
                             "height": 384,
                             "width": 640,
                             "color": "bwc"},
                    }


# EPD7IN5 commands
PANEL_SETTING                               = 0x00
POWER_SETTING                               = 0x01
POWER_OFF                                   = 0x02
POWER_OFF_SEQUENCE_SETTING                  = 0x03
POWER_ON                                    = 0x04
POWER_ON_MEASURE                            = 0x05
BOOSTER_SOFT_START                          = 0x06
DEEP_SLEEP                                  = 0x07
DATA_START_TRANSMISSION_1                   = 0x10
DATA_STOP                                   = 0x11
DISPLAY_REFRESH                             = 0x12
IMAGE_PROCESS                               = 0x13
LUT_FOR_VCOM                                = 0x20
LUT_BLUE                                    = 0x21
LUT_WHITE                                   = 0x22
LUT_GRAY_1                                  = 0x23
LUT_GRAY_2                                  = 0x24
LUT_RED_0                                   = 0x25
LUT_RED_1                                   = 0x26
LUT_RED_2                                   = 0x27
LUT_RED_3                                   = 0x28
LUT_XON                                     = 0x29
PLL_CONTROL                                 = 0x30
TEMPERATURE_SENSOR_COMMAND                  = 0x40
TEMPERATURE_CALIBRATION                     = 0x41
TEMPERATURE_SENSOR_WRITE                    = 0x42
TEMPERATURE_SENSOR_READ                     = 0x43
VCOM_AND_DATA_INTERVAL_SETTING              = 0x50
LOW_POWER_DETECTION                         = 0x51
TCON_SETTING                                = 0x60
TCON_RESOLUTION                             = 0x61
SPI_FLASH_CONTROL                           = 0x65
REVISION                                    = 0x70
GET_STATUS                                  = 0x71
AUTO_MEASUREMENT_VCOM                       = 0x80
READ_VCOM_VALUE                             = 0x81
VCM_DC_SETTING                              = 0x82

class EPD:
    """
    Info:
    -------

    The e-ink display is in front of you with the connector facing
    towards you. The first pixel is in the top left corner. The display is
    driven in landscape mode.

    8' E-Ink is width x height: 640 x 384 ! Turn image beforehand!
    """
    def __init__(self, display="epd7in5"):
        self.width = display_variants[display]["width"]
        self.height = display_variants[display]["height"]
        self.mode = display_variants[display]["color"]
        logging.debug("Initialize e-ink display with {}".format(str(display)))
        self.init()


    def digital_write(self, pin, value):
        epdif.epd_digital_write(pin, value)


    def digital_read(self, pin):
        return epdif.epd_digital_read(pin)


    def delay_ms(self, delaytime):
        epdif.epd_delay_ms(delaytime)


    def init(self):
        if (epdif.epd_init() != 0):
            return -1
        self.reset()
        epdif.send_command(POWER_SETTING)
        epdif.send_data(0x37)
        epdif.send_data(0x00)
        epdif.send_command(PANEL_SETTING)
        epdif.send_data(0xCF)
        epdif.send_data(0x08)
        epdif.send_command(BOOSTER_SOFT_START)
        epdif.send_data(0xc7)
        epdif.send_data(0xcc)
        epdif.send_data(0x28)
        epdif.send_command(POWER_ON)
        self.wait_until_idle()
        epdif.send_command(PLL_CONTROL)
        epdif.send_data(0x3c)
        epdif.send_command(TEMPERATURE_CALIBRATION)
        epdif.send_data(0x00)
        epdif.send_command(VCOM_AND_DATA_INTERVAL_SETTING)
        epdif.send_data(0x77)
        epdif.send_command(TCON_SETTING)
        epdif.send_data(0x22)
        epdif.send_command(TCON_RESOLUTION)
        epdif.send_data(0x02)     #source 640
        epdif.send_data(0x80)
        epdif.send_data(0x01)     #gate 384
        epdif.send_data(0x80)
        epdif.send_command(VCM_DC_SETTING)
        epdif.send_data(0x1E)      #decide by LUT file
        epdif.send_command(0xe5)           #FLASH MODE
        epdif.send_data(0x03)


    def wait_until_idle(self):
        while(epdif.is_busy()):      # 0: busy, 1: idle
            self.delay_ms(100)


    def reset(self):
        epdif.reset_low()
        self.delay_ms(200)
        epdif.reset_high()
        self.delay_ms(200)

    def serialize(self, image):
        # serialize
        buffer = [0x00] * int(self.width * self.height / 2)
        pixels = list(image.getdata())
        byte = 0x00
        for idx, val in enumerate(pixels):
            # Set the bits for the column of pixels at the current position.
            nibble = None
            if val == 0:  # black
                nibble = 0x0
            elif val == 255:  # white
                nibble = 0x3
            else:  # red
                nibble = 0x4

            if idx % 2:
                byte |= (nibble << 4)
            else:
                byte |= nibble
                buffer[int((idx - 1) / 2)] = byte
                byte = 0x00
        return buffer

    def send_buffer(self, buffer):
        epdif.send_command(DATA_START_TRANSMISSION_1)
        for el in buffer:
            epdif.send_data(el)
        epdif.send_command(DISPLAY_REFRESH)
        self.delay_ms(100)
        self.wait_until_idle()

    def convert_image(self, image):
        # sanity check
        imwidth, imheight = image.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).' .format(self.width, self.height))

        image_converted = None
        if self.mode == 'bwc':
            image_converted = image.convert('L', dither=None)
        else:  # default
            image_converted = image.convert('1')
        return image_converted

    def display_image(self, image):
        image_converted = self.convert_image(image)
        buffer = self.serialize(image_converted)
        self.send_buffer(buffer)

    def sleep(self):
        epdif.send_command(POWER_OFF)
        self.wait_until_idle()
        epdif.send_command(DEEP_SLEEP)
        epdif.send_data(0xa5)

    def calibration(self):
        """Function for Calibration"""
        black_img = Image.new('RGB', (self.width, self.height), "black")
        red_img = Image.new('RGB', (self.width, self.height), "red")
        white_img = Image.new('RGB', (self.width, self.height), "white")
        turns = 2
        for i in range(turns):
            logging.debug('Calibrate black...')
            self.display_image(black_img)

            if self.mode == "bwc":
                logging.debug('Calibrate red...')
                self.display_image(red_img)

            logging.debug('Calibrate white...')
            self.display_image(white_img)

            self.sleep()
            logging.info('Completed cycle {}/{} ... '.format(str(i+1), turns))



if __name__ == '__main__':
    """Added timer"""
    logging.info("Start calibration of e-ink display ...")
    start = time.time()
    epd = EPD()

    logging.debug("Calibrate display ...")
    epd.calibration()
    end = time.time()

    logging.info('Calibration complete in {} seconds'.format(int(end - start)))
