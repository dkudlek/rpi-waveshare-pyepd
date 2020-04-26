from distutils.core import setup

setup(
    name='rpi_waveshare_pyepd',
    version='0.1',
    packages=['rpi_waveshare_pyepd'],
    scripts=['scripts/show_image.py'],
    data_files=[('data', ['data/eink_splash_screen.png',
                          'data/eink_splash_screen_dark.png',
                          'data/eink_splash_screen_light.png'])],
    install_requires=[
      'numpy',
      'pathlib',
      'pillow',
      'RPi.GPIO',
      'spidev'
    ],
)
