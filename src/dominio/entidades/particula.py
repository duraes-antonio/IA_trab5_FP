from random import randint
from typing import List, Optional

from math import log, cos, pi, exp
from numpy.random.mtrand import choice

from ..util.validacoes import Validacao

R_MAX = 2147483647
EIXO_RUIDO = 50


class Particula:
	"""Representa uma partícula em um plano N-dimensional."""

	# Lista com todos eixos que definem a posição em uma dimensão N
	# Exemplo {'x': 10, 'y': 100, 'z': 30}
	__eixos: dict

	# Lista com todas velocidades de todos eixos
	# Exemplo {'x': 13, 'y': 12, 'z': 10}
	__velocidades: dict = {}

	# Instante no tempo em que a partícula encontra-se
	__t: float

	# Peso que define a chance do estado da part. ser o estado real do objeto
	__w: float

	# Atributos para garantir o intervalo possível de valores
	__v_min: float
	__v_max: float
	__eixos_max: dict

	def __init__(
			self, v_min: float, v_max: float,
			eixos: dict, eixos_max: dict):

		Validacao.validar_min_max(v_min, v_max, "VELOCIDADE")
		Validacao.validar_min_max_dict(eixos, eixos_max)

		# Toda partícula nasce em um instante padrão
		self.__t = 1 / 30

		# Atualize a velocidade de cada eixo para vel. dada
		for eixo in eixos:
			self.__velocidades[eixo] = randint(v_min, v_max)

		self.__v_min = v_min
		self.__v_max = v_max
		self.__eixos = eixos
		self.__eixos_max = eixos_max

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

	@property
	def velocidades(self):
		"""Dicionário com o nome da variável como chave e sua velocidade"""
		return self.__velocidades

	def atualizar_posicao(self, delta_t: float):
		"""Atualiza os valores das variáveis posicionais da partícula no espaço

		Args:
			delta_t: Variação do instante T e o instante anterior
		"""

		# Para cada eixo(x, y, z, ...) dentro do vetor de posição
		for chave in self.eixos:
			eixo_ant = self.eixos[chave]
			vel_ant = self.__velocidades[chave]

			self.eixos[chave] = int(eixo_ant + eixo_ant * vel_ant * delta_t)

			# TODO(@duraes-antonio) validar o uso de um ruído na normalização
			# Valide e normalize o valor do eixo atual
			if self.eixos[chave] > self.__eixos_max[chave]:
				self.eixos[chave] = self.__eixos_max[chave] - EIXO_RUIDO

			elif self.eixos[chave] < 0:
				self.eixos[chave] = EIXO_RUIDO

			self.eixos[chave] += randint(-EIXO_RUIDO, EIXO_RUIDO)

		return None

	def atualizar_veloc(self):
		"""Atualiza a velocidade da partícula com uma perturbação gaussiana"""

		def gerar_dist_gauss(centro: float, desvio: float) -> float:
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

		for eixo in self.__velocidades:

			# veloc_nova = self.__velocidades[eixo] + gerar_dist_gauss(0, 0.1)
			veloc_nova = self.__velocidades[eixo] + (self.__v_max - self.__v_min) * 0.1

			# Normalização
			if veloc_nova > self.__v_max:
				self.__velocidades[eixo] = self.__v_max

			elif veloc_nova < self.__v_min:
				self.__velocidades[eixo] = self.__v_min

			else:
				self.__velocidades[eixo] = veloc_nova

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

		# TODO(@duraes-antonio) Fórmula: w = exp(-dist) apresenta PROBLEMAS
		#  para dist > 700
		dist = self.__calc_dist_eucl(self.__eixos, eixos_obj)

		# Se a dist for zero, defina que é 1, para evitar problemas de divisão
		if dist == 0:
			dist = 1
			self.__w = exp(-dist)

		elif dist < 400:
			self.__w = exp(-dist)

		# Se a dist for muito grande, o peso tenderá a zero
		else:
			self.__w = 0

		return None

	def normalizar_peso(self, somatorio_peso: float):
		"""Normaliza o peso da partícula de acordo com o somatório do grupo

		Args:
			somatorio_peso: Somatório de pesos do grupo de partículas.
		"""
		self.__w /= somatorio_peso
		return None


class GrupoParticula:
	"""Conjunto de partículas de mesma velocidade inicial e dimensões"""

	__particulas: List[Particula]
	__n_part: int
	__eixos_max: dict

	def __init__(
			self, n: int, v_min: float, v_max: float,
			eixos_max: dict, ruido: Optional[int]):
		"""
		Args:
			n: Número de partículas que o grupo terá
			v_min: Velocidade mínima (incluvise) permitida
			v_max: Velocidade máxima (inclusive) permitida
			eixos_max: Valores máximo para cada eixo (x, y, z, etc)
			ruido: Valor para inferir na atualização de posição
		"""

		Validacao.validar_min_max(v_min, v_max, "VELOCIDADE")

		self.soma_pesos = 0
		self.__particulas: [Particula] = []
		self.__n_part = n
		self.__eixos_max = eixos_max

		global EIXO_RUIDO

		if ruido is not None:
			EIXO_RUIDO = ruido

		for i in range(self.__n_part):

			eixos_random = {}

			# Para cada eixo, sorteie um inteiro entre 0 e o valor máx
			for chave in eixos_max:
				eixos_random[chave] = randint(0, eixos_max[chave])

			self.__particulas.append(
				Particula(v_min, v_max, eixos_random, eixos_max))

	@property
	def n(self):
		"""Número de partículas pertencentes ao grupo"""
		return self.__n_part

	def atualizar_particulas(self, delta_t: float, eixos_obj: dict):
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

		self.soma_pesos = sum([p.w for p in self.__particulas])

		if self.soma_pesos > 0:
			for particula in self.__particulas:
				particula.normalizar_peso(self.soma_pesos)

	def reamostrar(self):
		"""Realiza a reamostragem do grupo para reduzir a degeneração"""

		self.soma_pesos = sum([p.w for p in self.__particulas])

		if self.soma_pesos > 0:
			# Para gerar uma distribuição de probabilidade, cada parcela
			#  valerá 1 / pela chance total
			unid = 1 / self.soma_pesos

			# Peça ao numpy para gerar uma lista com N elementos, a partir
			#  da lista de partículas, e considerando o peso de cada uma
			lista = choice(
				self.__particulas, self.n,
				p=[unid * p.w for p in self.__particulas])

			# Armazene e converta a lista de selecionados proporc. por peso
			temp_selec: List[Particula] = list(lista)
			media_eixos = {}
			media_veloc = {}

			# Calcule média de todos valores dos eixos
			for eixo in temp_selec[0].eixos:
				media_eixos[eixo] = sum([p.eixos[eixo] for p in temp_selec]) / self.n

			# Calcule média de todos valores das velocidades dos eixos
			for eixo in temp_selec[0].velocidades:
				media_veloc[eixo] = sum([p.velocidades[eixo] for p in temp_selec]) / self.n

			# Substitua as antigas partículas pelas selecionadas
			self.__particulas = temp_selec

			# Para cada partícula, atualize seu eixo com a média ponderada
			#  pelo peso
			for part in self.__particulas:
				for eixo in part.eixos:
					# TODO aqui vai dar erro por part.w estar infinito
					part.eixos[eixo] = int(media_eixos[eixo] * part.w)
					part.velocidades[eixo] = int(media_veloc[eixo] * part.w)

		return None

	def get(self, i: int):

		if i < 0 or i >= len(self.__particulas):
			return None

		return self.__particulas[i]
