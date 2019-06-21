from typing import List

from util import instalar_dependencias
from particula import Particula


# instalar_dependencias()

# import cv2
# import numpy
# from matplotlib import pyplot


def main():
    particulas: List[Particula] = []

    for i in range(10):

        for part in particulas:
            # -----PREDIÇÃO

            # > Atualize a velocidade da partícula
            part.atualizar_veloc()

            # > Atualizar a posição (os eixos) da partícula
            part.atualizar_posicao(1)

        # -----MENSURAÇÃO

        # > Atualize peso (W) da partícula
        # part.atualizar_peso()

        # > Normalize o peso (W) da partícula
        # part.normalizar_peso()

        # RE-Amostragem

    return 0


main()
