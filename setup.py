from distutils.core import setup

setup(
    name='waveshare_pyepd',
    version='0.1',
    packages=['waveshare_pyepd'],
    scripts=['scripts/show_image.py'],
    install_requires=[
      'numpy',
      'pathlib',
      'pillow',
      'RPi.GPIO',
      'spidev'
    ],
)
