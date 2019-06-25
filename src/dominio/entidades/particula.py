from math import log, cos, pi, sqrt, exp
from random import uniform, randint
from typing import List, Optional

from ..util.validacoes import Validacao

R_MAX = 2147483647
EIXO_RUIDO = 50


class Particula:
	"""Representa uma partícula em um plano N-dimensional."""

	# Lista com todos eixos que definem a posição em uma dimensão N
	__eixos: dict

	# Velocidade de cada movimento da partícula
	__v: float

	# Instante no tempo em que a partícula encontra-se
	__t: int

	# Peso que define a chance do estado da part. ser o estado real do objeto
	__w: float

	# Atributos para garantir o intervalo possível de valores
	__v_min: float
	__v_max: float
	__eixos_max: dict

	def __init__(
			self, velocidade: float, v_min: float, v_max: float,
			eixos: dict, eixos_max: dict):

		# Validacao.validar_min_max(v_min, v_max, "VELOCIDADE")
		# Validacao.validar_min_max_dict(eixos, eixos_max)

		# Toda partícula nasce no instante 1
		self.__t = 1

		self.__v = velocidade
		self.__v_min = v_min
		self.__v_max = v_max
		self.__eixos = eixos
		self.__eixos_max = eixos_max

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

	@property
	def eixos(self):
		"""Dicionário com o nome do eixo como chave e seu valor"""
		return self.__eixos

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
		if veloc_nova > self.__v_max:
			self.__v = self.__v_max

		elif veloc_nova < self.__v_min:
			self.__v = self.__v_min

		else:
			self.__v = veloc_nova

		return None

	def atualizar_posicao(self, delta_t: int):
		"""Atualiza os valores das variáveis posicionais da partícula no espaço

		Args:
			delta_t: Variação do instante T e o instante anterior
		"""

		# Para cada eixo(x, y, z, ...) dentro do vetor de posição
		for chave in self.eixos:
			eixo_ant = self.eixos[chave]

			# TODO(@duraes-antonio) validar cálc de atualização da posição
			self.eixos[chave] = int(eixo_ant + eixo_ant * self.v * delta_t)

			# TODO(@duraes-antonio) validar o uso de um ruído na normalização
			# Valide e normalize o valor do eixo atual
			if self.eixos[chave] > self.__eixos_max[chave]:
				self.eixos[chave] = randint(1, EIXO_RUIDO)

			elif self.eixos[chave] < 0:
				self.eixos[chave] = randint(1, EIXO_RUIDO)

			self.eixos[chave] += randint(-EIXO_RUIDO, EIXO_RUIDO)

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

		# Se os dicionários não possuírem os mesmos nomes de eixos;
		# Validacao.validar_chaves(eixos_obj1, eixos_obj2)

		soma_quadrados = 0

		for eixo in eixos_obj1:
			soma_quadrados += (eixos_obj1[eixo] - eixos_obj2[eixo]) ** 2

		return soma_quadrados ** 0.5

	def atualizar_peso(self, eixos_obj: dict):
		"""Define o peso (w) de acordo com a dist. ao centro de massa do objeto.

		Args:
			eixos_obj: Eixos posicionais do objeto observado.
		"""

		# TODO(@duraes-antonio) Fórmula: w = e^(-dist) apresenta PROBLEMAS
		dist = self.__calc_dist_eucl(self.__eixos, eixos_obj)

		if dist == 0:
			dist = 1

		self.__w = (1 / sqrt(2 * pi * 1)) * exp(-(dist) ** 0.5 / (2 * 1))

		return None

	def normalizar_peso(self, somatorio_peso: float):
		"""Normaliza o peso da partícula de acordo com o somatório do grupo

		Args:
			somatorio_peso: Somatório de pesos do grupo de partículas.
		"""

		# TODO(@duraes-antonio): Validar se a fórmula está correta
		self.__w /= somatorio_peso
		return None


class GrupoParticula:
	"""Conjunto de partículas de mesma velocidade inicial e dimensões"""

	__particulas: List[Particula]
	__n_part: int

	def __init__(
			self, n: int, v_ini: float, v_min: float, v_max: float,
			eixos_max: dict, ruido: Optional[int]):
		"""
		Args:
			n: Número de partículas que o grupo terá
			v_ini: Velocidade inicial para todas partículas
			v_min: Velocidade mínima (incluvise) permitida
			v_max: Velocidade máxima (inclusive) permitida
			eixos_max: Valores máximo para cada eixo (x, y, z, etc)
			ruido: Valor para inferir na atualização de posição
		"""

		Validacao.validar_min_max(v_min, v_max, "VELOCIDADE")
		Validacao.validar_min_max(v_ini, v_max, "VELOCIDADE")

		self.soma_pesos = 0
		self.__particulas: [Particula] = []
		self.__n_part = n

		global EIXO_RUIDO

		if ruido is not None:
			EIXO_RUIDO = ruido

		for i in range(self.__n_part):

			eixos_random = {}

			# Para cada eixo, sorteie um inteiro entre 0 e o valor máx
			for chave in eixos_max:
				eixos_random[chave] = randint(0, eixos_max[chave])

			self.__particulas.append(
				Particula(v_ini, v_min, v_max, eixos_random, eixos_max))

	@property
	def n(self):
		"""Número de partículas pertencentes ao grupo"""
		return self.__n_part

	def atualizar_particulas(self, delta_t: int, eixos_obj: dict):
		"""Atualiza a velocidade, posição e o peso (e normaliza-o)

		Args:
			delta_t: Variação entre o instante atual e o anterior
			eixos_obj: Valor dos eixos (definem a posição) do centro de massa
		"""
		for particula in self.__particulas:
			particula.atualizar_veloc()

		for particula in self.__particulas:
			particula.atualizar_posicao(delta_t)

		for particula in self.__particulas:
			particula.atualizar_peso(eixos_obj)

		self.soma_pesos = 0

		for particula in self.__particulas:
			self.soma_pesos += particula.w

		for particula in self.__particulas:
			particula.normalizar_peso(self.soma_pesos)

	def reamostrar(self):
		"""Realiza a reamostragem do grupo para reduzir a degeneração"""

		temp_partics = []

		# Enquanto a nova lista não for preenchida com N partículas
		while len(temp_partics) < self.n:

			soma_min_w = uniform(0, self.soma_pesos)
			soma = 0

			for part in self.__particulas:
				soma += part.w

				if soma > soma_min_w:
					temp_partics.append(part)

		self.__particulas = temp_partics

		return None

	def get(self, i: int):

		if i < 0 or i >= len(self.__particulas):
			return None

		return self.__particulas[i]

	# TODO(@duraes-antonio) Remover ou ajustar após definir o máximo de eixos
	def get_media_xyv(self) -> (int, int, int):

		soma_x = soma_y = soma_v = 0

		for part in self.__particulas:
			soma_x += part.eixos["x"]
			soma_y += part.eixos["y"]
			soma_v += part.v

		return int(soma_x / self.n), int(soma_y / self.n), int(soma_v / self.n)
