from random import uniform, randint

from math import exp, log, cos, pi

R_MAX = 2147483647


class Particula:
    """Representa uma partícula em um plano N-dimensional."""

    # CONSTANTES
    VEL_MAX: float = 25
    VEL_MIN: float = 0

    # Lista com todos eixos que definem a posição em uma dimensão N
    __vetor_posicao: dict = {}

    # Velocidade de cada movimento da partícula
    __v: float = 0

    # Instante no tempo em que a partícula encontra-se
    __t: int = 0

    # Peso que define a chance do estado da part. ser o estado real do objeto
    __w: float = 0

    def __init__(self, velocidade: float):
        self.__t = 1
        self.__v = velocidade

    @property
    def v(self):
        """Velocidade atual do movimento da partícula"""
        return self.__v

    @property
    def t(self):
        """Instante no tempo em que a partícula encontra-se"""
        return self.__t

    @property
    def w(self):
        """Peso: indica a chance do estado da part. ser o estado do objeto"""
        return self.__w

    @staticmethod
    def __calc_novo_valor_eixo(
            valor_ant: float, veloc_ant: float, delta_t: float) -> float:
        """Função geral para atualização de uma variável eixo

        Args:
            valor_ant: Valor atual da variável eixo, antes da atualização.
            veloc_ant: Velocidade aterior a atualização.
            delta_t: Variação de t, do último movimento até o atual.

        Returns:
            Valor atualizado com base na posição e velocidade anterior,
            e na variação do tempo.
        """

        valor_t = valor_ant + valor_ant * veloc_ant * delta_t
        return valor_t

    def atualizar_veloc(self):
        """Atualiza a velocidade da partícula com uma perturbação gaussiana"""

        def gerar_distrib_gaussiana(centro: float, desvio: float) -> float:
            """
            Função baseada na 'carmen_gaussian_random'
            """

            # TODO(@duraes-antonio) citar nas referências a conta
            # https://github.com/kralf/carmen/blob/master/src/lib/core/global/global.c

            norm = 1.0 / (R_MAX + 1)
            u = 1 - randint(0, R_MAX) * norm
            v = randint(0, R_MAX) * norm
            z = (-2 * log(u)) * cos(2 * pi * v)
            return centro + desvio * z

        veloc_nova = self.v + gerar_distrib_gaussiana(0, 1)

        # Normalização
        if veloc_nova > self.VEL_MAX:
            self.__v = self.VEL_MAX

        elif veloc_nova < self.VEL_MIN:
            self.__v = self.VEL_MIN

        else:
            self.__v = veloc_nova

        return None

    def atualizar_posicao(self, delta_t: int):
        """Atualiza os valores das variáveis posicionais da partícula no espaço

        Args:
            delta_t: Variação do instante T e o instante anterior
        """
        v_pos = self.__vetor_posicao

        # Para cada variável dentro do vetor de posição
        for i in range(len(v_pos)):
            v_pos[i] = self.__calc_novo_valor_eixo(v_pos[i], self.v, delta_t)

        return None

    @staticmethod
    def __calc_dist_eucl(eixos_obj1: dict, eixos_obj2: dict) -> float:

        """Calcula a distância euclidiana entre dois itens de N dimensões

        Args:
            eixos_obj1: Dic. com o título do eixo e seu valor para o 1º ponto.
            eixos_obj2: Dic. com o título do eixo e seu valor para o 2º ponto.

        Raises:
            KeyError: Caso houver eixos ausentes em um dos dicionários.

        Returns:
            Distância euclidiana calculada sobre todos eixos dos dois objetos.
        """

        # Se o nome ou quantidade de eixos forem diferentes nos dois dic.;
        if [*eixos_obj1].sort() != [*eixos_obj2].sort():
            raise KeyError("Chaves com nomes distintos ou ausentes em um dos dicionários.")

        soma_quadrados = 0

        for eixo in eixos_obj1:
            soma_quadrados += (eixos_obj1[eixo] - eixos_obj2[eixo]) ** 2

        return soma_quadrados ** 0.5

    def atualizar_peso(self, eixos_obj: dict):
        """Define o peso (w) de acordo com a dist. ao centro de massa do objeto.

        Args:
            eixos_obj: Eixos posicionais do objeto observado.
        """

        # Fórmula: w = e^(-dist)
        dist = self.__calc_dist_eucl(self.__vetor_posicao, eixos_obj)
        self.__w = exp(-dist)

        return None

    def normalizar_peso(self, somatorio_peso: float):
        """Normaliza o peso da partícula de acordo com o somatório do grupo

        Args:
            somatorio_peso: Somatório de pesos do grupo de partículas.
        """
        self.__w = self.w / somatorio_peso

        return None
