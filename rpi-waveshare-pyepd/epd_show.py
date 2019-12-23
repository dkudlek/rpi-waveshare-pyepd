from time import sleep
import logging

from .epd_logical import EPD



def epd_show(image, display_variant):
    epd = EPD(display_variant)
    epd.init()
    sleep(5)
    logging.debug('Converting image to data and sending it to the display')
    epd.display_image(image)
    logging.debug('Data sent successfully')
    logging.debug('Powering off')
    epd.sleep()

def epd_calibrate(display_variant):
    epd = EPD(display_variant)
    epd.init()
    sleep(5)
    logging.debug('Converting image to data and sending it to the display')
    epd.calibration()
    logging.debug('Data sent successfully')
    logging.debug('Powering off')
    epd.sleep()
