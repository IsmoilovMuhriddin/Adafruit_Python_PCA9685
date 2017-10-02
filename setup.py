try:
    # Try using ez_setup to install setuptools if not already installed.
    from ez_setup import use_setuptools
    use_setuptools()
except ImportError:
    # Ignore import error and assume Python 3 which already has setuptools.
    pass

from setuptools import setup, find_packages

classifiers = ['Development Status :: 3 - Beta',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(name              = 'rasp_car_PCA9685',
      version           = '1.0.0',
      author            = 'Muhriddin Ismoilov',
      author_email      = 'ismoilovmuh1996@gmail.com',
      description       = 'Python code to use the PCA9685 PWM for Motor control of Smart Car',
      license           = 'MIT',
      classifiers       = classifiers,
      url               = 'https://github.com/IsmoilovMuhriddin/rasp_car_PCA9685/',
      install_requires  = ['wiringpi'],
      packages          = find_packages())
