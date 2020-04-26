from time import sleep
import logging

from .epd_logical import EPD



def epd_show(image, display_variant):
    """
    Prints preprocessed image to the display.

    Parameters
    ----------
    image : PIL.Image
        The image with corrected colors and the correct size.
    display_variant: display_variants
    """
    epd = EPD(display_variant)
    epd.init()
    sleep(5)
    logging.debug('Converting image to data and sending it to the display')
    epd.display_image(image)
    logging.debug('Data sent successfully')
    logging.debug('Powering off')
    epd.sleep()

def epd_calibrate(display_variant):
    """
    Calibrates the display according to its settings.

    Parameters
    ----------
    display_variant: display_variants
    """
    epd = EPD(display_variant)
    epd.init()
    sleep(5)
    logging.debug('Converting image to data and sending it to the display')
    epd.calibration()
    logging.debug('Data sent successfully')
    logging.debug('Powering off')
    epd.sleep()
