import matplotlib.pyplot as plt
import numpy as np
import os

from modules.output import file_name, path


def main()
    plt.xticks(rotation='vertical')
    plt.legend()
    plt.grid()
    plt.xlabel('Something')
    plt.ylabel('Another thing')
    plt.title('The title')
    plt.gcf().autofmt_xdate()
    _path = path('tmp', f'{file_name}.png')
    plt.savefig(_path)
    plt.clf()
    # send image, or do other things

    os.remove(_path)


if __name__ == "__main__":
    main()
