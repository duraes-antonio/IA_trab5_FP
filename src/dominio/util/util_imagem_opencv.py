import cv2
import numpy
from matplotlib import pyplot, colors
from mpl_toolkits.mplot3d import Axes3D
from numpy import shape


class UtilImgOpenCV():
	"""Classe com filtros para tratar objeto imagem OpenCV"""

	@staticmethod
	def __visualizar_escala_cores(frame_cv2) -> Axes3D:
		col1, col2, col3 = cv2.split(frame_cv2)
		fig = pyplot.figure()
		eixos = fig.add_subplot(1, 1, 1, projection="3d")

		pixel_colors = frame_cv2.reshape(
			(shape(frame_cv2)[0] * shape(frame_cv2)[1], 3))
		norm = colors.Normalize(vmin=-1., vmax=1.)
		norm.autoscale(pixel_colors)
		pixel_colors = norm(pixel_colors).tolist()
		eixos.scatter(
			col1.flatten(), col2.flatten(), col3.flatten(),
			facecolors=pixel_colors, marker=".")
		return eixos

	@staticmethod
	def visualizar_escala_cor(frame_cv2):
		eixos = UtilImgOpenCV.__visualizar_escala_cores(frame_cv2)
		eixos.set_xlabel("Red")
		eixos.set_ylabel("Green")
		eixos.set_zlabel("Blue")
		pyplot.show()
		return None

	@staticmethod
	def visualizar_escala_hsv(frame_cv2_hsv):
		eixos = UtilImgOpenCV.__visualizar_escala_cores(frame_cv2_hsv)
		eixos.set_xlabel("Hue")
		eixos.set_ylabel("Saturation")
		eixos.set_zlabel("Value")
		pyplot.show()
		return None

	@staticmethod
	def obter_contorno(frame_cv2_masc):
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
	def desenhar_contorno(frame_cv2_mascara, frame_cv2_rgb):
		"""Contorna (cor lilás) na img RGB a área em branco na img c/ máscara

		Args:
			frame_cv2_mascara: Imagem HSV e em preto/branco
			frame_cv2_rgb: Imagem BGR a ser demarcada
		"""

		contornos, _ = cv2.findContours(frame_cv2_mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

		# Desenha um contorno roxo, de expessura 2, no frame_cv2 original
		cv2.drawContours(frame_cv2_rgb, contornos, -1, (255, 0, 255), 2)

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
	def desenhar_centro_massa(frame_cv2_masc, frame_cv2_rgb) -> (int, int):
		"""Desenha o centro de massa do objeto no frame RGB

		Args:
			frame_cv2_masc: Imagem OpenCV em HSV
			frame_cv2_rgb: Imagem em que o centro de massa será desenhado

		Returns:
			Tupla com a posição X, Y do centro de massa
		"""

		contornos, hierarchy = cv2.findContours(frame_cv2_masc, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

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

		cv2.circle(frame_cv2_rgb, (cx, cy), 5, 255, -1)

		return cx, cy

	@staticmethod
	def aplicar_mascara(frame_cv2_rgb):
		"""Converte a imagem para HSV e aplica filtro Preto/Branco

		Args:
			frame_cv2_rgb: Imagem BGR a ser convertida

		Returns:
			Nova imagem em HSV e em preto/branco
		"""

		hsv = cv2.cvtColor(frame_cv2_rgb, cv2.COLOR_BGR2HSV)
		cor_intev_min = numpy.array([0, 100, 50])
		cor_intev_max = numpy.array([10, 255, 255])
		# cor_intev_min = numpy.array([20, 40, 40])
		# cor_intev_max = numpy.array([255, 230, 255])

		mascara = cv2.inRange(hsv, cor_intev_min, cor_intev_max)

		return mascara
