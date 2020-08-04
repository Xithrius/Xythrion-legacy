import os
from pathlib import Path


EXTENSIONS = [
    f'xythrion.extensions.{ext_f}' for ext_f in os.listdir(Path.cwd() / 'xythrion') if '__' not in ext_f]
