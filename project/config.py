from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

ALLOWED_EXTENSIONS = (
    'BLP',
    'BMP',
    'DDS',
    'DIB',
    'EPS',
    'GIF',
    'ICNS',
    'ICO',
    'IM',
    'JPEG',
    'JPG',
    'MSP',
    'PCX',
    'PNG',
    'PPM',
    'SGI',
    'SPIDER',
    'TGA',
    'TIFF',
    'WebP',
    'XBM',
    'CUR',
    'DCX',
    'FITS',
    'FLI',
    'FLC',
    'FPX',
    'FTEX',
    'GBR',
    'GD',
    'IMT',
    'IPTC',
    'NAA',
    'MCIDAS',
    'MIC',
    'MPO',
    'PCD',
    'PIXAR',
    'PSD',
    'WAL',
    'WMF',
    'XPM',
    'PALM',
    'PDF',
    'XV Thumbnails',
    'BUFR',
    'GRIB',
    'HDF5',
    'MPEG',
)

COMMANDS = (
    '-p', #path to file
    '-pdb', #path to database file
    '-st', # show database table
)