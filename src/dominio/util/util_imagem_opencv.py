from typing import Tuple, List, Any

import cv2
import numpy


class UtilImgOpenCV:
	"""Classe com filtros para tratar objeto imagem OpenCV"""

	@staticmethod
	def obter_contorno(frame_cv2_masc) -> List[Any]:
		"""Encontra os contornos do frame_cv2 com máscara (preto e branco)

		Args:
			frame_cv2_masc: Imagem OpenCV em HSV

		Returns:
			Lista de objetos de contorno OpenCV
		"""
		contornos, _ = cv2.findContours(
			frame_cv2_masc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
		return contornos

	@staticmethod
	def desenhar_contorno(
			frame_cv2_mascara, frame_cv2_rgb,
			cor: Tuple[int, int, int] = (255, 255, 0)):
		"""Contorna (cor lilás) na img RGB a área em branco na img c/ máscara

		Args:
			frame_cv2_mascara: Imagem HSV e em preto/branco
			frame_cv2_rgb: Imagem BGR a ser demarcada
			cor: Tupla contendo as cores RGB [Opcional]
		"""

		contornos, _ = cv2.findContours(frame_cv2_mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

		# Desenha um contorno roxo, de expessura 2, no frame_cv2 original
		cv2.drawContours(frame_cv2_rgb, contornos, -1, cor, 2)
		return None

	@staticmethod
	def desenhar_box(frame_cv2_mascara, frame_cv2_rgb):
		"""Desenha um retângulo verde em torno do objeto na imagem colorida

		Args:
			frame_cv2_mascara: Imagem HSV, em P/B e c/ objeto em branco
			frame_cv2_rgb: Imagem BGR a ser contornada
		"""
		x, y, w, h = cv2.boundingRect(frame_cv2_mascara)
		cv2.rectangle(frame_cv2_rgb, (x, y), (x + w, y + h), (255, 255, 0), 2)
		return None

	@staticmethod
	def desenhar_box_pt(
			c_massa: Tuple[int, int], larg_alt: Tuple[int, int],
			frame_cv2_rgb, cor: Tuple[int, int, int] = (255, 255, 0)):
		"""Desenha um retângulo verde em torno do objeto na imagem colorida

		Args:
			c_massa: Tupla contendo as coordenadas do centro de massa
			larg_alt: Tupla contendo a largura e altura do objeto
			frame_cv2_rgb: Imagem BGR a ser contornada
			cor: Tupla contendo as cores RGB [Opcional]
		"""
		pt_ini = int(c_massa[0] - larg_alt[0] / 2), int(c_massa[1] - larg_alt[1] / 2)
		pt_fim = int(c_massa[0] + larg_alt[0] / 2), int(c_massa[1] + larg_alt[1] / 2)
		cv2.rectangle(frame_cv2_rgb, pt_ini, pt_fim, cor, 2)
		return None

	@staticmethod
	def obter_centro_massa(frame_cv2_masc) -> Tuple[int, int]:
		"""Obtém o centro de massa do objeto a partir de uma imagem HSV

		Args:
			frame_cv2_masc: Imagem OpenCV em HSV

		Returns:
			Tupla com as coordenadas X e Y do centro de massa
		"""

		_, contornos, hierarchy = cv2.findContours(frame_cv2_masc, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

		# Obtenha o contorno que abrange a maior área
		max_area: int = 0
		melhor_contorno = None

		for cont in contornos:
			area = cv2.contourArea(cont)

			if area > max_area:
				max_area = area
				melhor_contorno = cont

		momentos = cv2.moments(melhor_contorno)
		cx = cy = 1

		if momentos['m00'] != 0:
			cx = int(momentos['m10'] / momentos['m00'])
			cy = int(momentos['m01'] / momentos['m00'])

		return cx, cy

	@staticmethod
	def obter_larg_alt_obj(frame_cv2_mascara) -> Tuple[int, int]:
		"""Obtém a largura e altura do objeto da imagem HSV

		Args:
			frame_cv2_mascara: Imagem HSV, em P/B e c/ objeto em branco

		Returns:
			Retorna tupla com par (largura, altura)
		"""
		x, y, w, h = cv2.boundingRect(frame_cv2_mascara)
		return w, h

	@staticmethod
	def aplicar_mascara(frame_cv2_rgb, boo: bool = False):
		"""Converte a imagem para HSV e aplica filtro Preto/Branco

		Args:
			frame_cv2_rgb: Imagem BGR a ser convertida

		Returns:
			Nova imagem em HSV e em preto/branco
		"""

		hsv = cv2.cvtColor(frame_cv2_rgb, cv2.COLOR_BGR2HSV)

		if (boo == False):
			cor_intev_min = numpy.array([0, 100, 50])
			cor_intev_max = numpy.array([10, 255, 255])

		else:
			cor_intev_min = numpy.array([20, 40, 40])
			cor_intev_max = numpy.array([255, 230, 255])

		#
		# cor_intev_min = numpy.array([0, 70, 70])
		# cor_intev_max = numpy.array([40, 255, 255])

		mascara = cv2.inRange(hsv, cor_intev_min, cor_intev_max)

		return mascara
