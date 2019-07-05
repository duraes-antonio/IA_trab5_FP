from typing import Tuple, List

import scipy.stats
from numpy import arange, arctan2, array, average, cos, empty, pi, sin, linalg
from numpy.random import choice, randint, randn, uniform


class GrupoParticulas:

	def __init__(
			self, n: int, v_min: float, v_max: float, x_max: int, y_max: int,
			centro: Tuple[int, int] = (0, 0)):
		"""
		Args:
			centro: Centro inicial de massa do objeto
			n: Número de partículas que o grupo terá
			v_min: Velocidade mínima que cada partícula pode assumir
			v_max: Velocidade máxima que cada partícula pode assumir
			x_max: Posição horizontal máxima aceitável
			y_max: Posição vertical máxima aceitável
		"""

		self.__centro_ant: Tuple[int, int] = centro

		self.__vmin = v_min
		self.__vmax = v_max

		self.__n = n

		# Inicialize os N pesos (1 p/ cada partícula) com valor 1
		self.__pesos = array([1.0] * n)

		# Inicialize N partículas, cada uma com dois eixos
		self.__partics = empty((n, 2))

		# Sorteie N partículas, cada uma composta por um valor randômico de
		# x [0 até x_max] e randômico de y [0 até y_max]
		self.__partics[:, 0] = uniform(low=0, high=x_max, size=n)
		self.__partics[:, 1] = uniform(low=0, high=y_max, size=n)

	@property
	def n(self):
		return self.__n

	def atualizar_particulas(self, c_massa_atual: Tuple[int, int]):
		"""Atualiza a velocidade, posição e o peso (e normaliza-o)

		Args:
			c_massa_atual: Par de coord. do centro de massa atual do objeto
		"""

		self.__predicao(self.__centro_ant, c_massa_atual)
		self.__atualizacao(c_massa_atual)
		self.__reamostragem()

		# O centro de massa atual agora deve substituir o antigo
		self.__centro_ant = c_massa_atual

	def __predicao(
			self, c_massa_ant: Tuple[int, int], c_massa_atual: Tuple[int, int]):
		"""Atualiza as posições das partículas de acordo com centro de massa

		Args:
			c_massa_ant: Centro de massa no instante anterior
			c_massa_atual: Centro de massa no instante atual
		"""

		heading = arctan2(
			array([c_massa_atual[1] - c_massa_ant[1]]),
			array([c_massa_ant[0] - c_massa_atual[0]]))

		if heading > 0:
			heading = -(heading - pi)

		else:
			heading = -(pi + heading)

		# Calcule a dist. euclidiana entre o antigo e o novo centro de massa
		dist = linalg.norm(
			array([c_massa_ant]) - array([c_massa_atual]), axis=1)

		# Sorteie a velocidade entre o mínimo e o máximo
		desvios = array(
			[uniform(self.__vmin, self.__vmax + 1) for i in range(self.n)])

		dist_com_ruido = dist + (randn(self.n) * desvios)

		# Incremente as posições
		self.__partics[:, 0] += cos(heading) * dist_com_ruido
		self.__partics[:, 1] += sin(heading) * dist_com_ruido

		return None

	def __atualizacao(self, c_massa_atual: array):
		"""Define o peso (w) de acordo com a dist. ao centro de massa do objeto.

		Args:
			c_massa_atual: Par de coord. do centro atual de massa do objeto
		"""

		# Reinicie todos pesos com valor 1
		self.__pesos.fill(1)

		diff_x = (self.__partics[:, 0] - c_massa_atual[0]) ** 2
		diff_y = (self.__partics[:, 1] - c_massa_atual[1]) ** 2
		dist = (diff_x + diff_y) ** 0.5

		# Aplique uma função normal de densidade de probabilidade
		# para calcular a proximidade de cada partícula
		self.__pesos *= scipy.stats.norm(dist, 20).pdf(0)

		# Divida cada peso pela soma de todos (Normalização)
		self.__pesos /= sum(self.__pesos)

		return None

	def __reamostragem(self):
		"""Repõe as partículas para reduzir a degeneração do algorítimo"""
		prob = 1 / sum(self.__pesos)
		indices = arange(self.n)
		indices = choice(indices, self.n, p=prob * self.__pesos)

		# Re-escolha as partículas de acordo com o índice sorteado
		self.__partics[:] = self.__partics[indices]

		# Atualize o peso para os pesos das partículas sorteadas e normalize-os
		self.__pesos[:] = self.__pesos[indices]
		self.__pesos /= sum(self.__pesos)

		return None

	def obter_coords(self) -> List[Tuple[int, int]]:
		"""Gera uma lista com todos pares de coordenadas de todas partículas
		
		Returns:
			Lista com par de coordenadas das partículas
		"""
		return [(int(p[0]), int(p[1])) for p in self.__partics]

	def ponto_medio(self) -> Tuple[int, int]:
		"""Calcula a média (de x e y) das coordenadas de todas partículas

		Returns:
			Par contendo o X e o Y do ponto médio do grupo de partículas
		"""
		return int(average(self.__partics[:, 0])), int(average(self.__partics[:, 1]))
