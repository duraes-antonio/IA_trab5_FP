# from util.util import instalar_dependencias

# instalar_dependencias()

import cv2
import numpy
from matplotlib import pyplot, colors
from mpl_toolkits.mplot3d import Axes3D

from dominio.entidades.particula import GrupoParticula

path_assets = "../assets/"
g_path_v_gow = path_assets + "gow2.mp4"
g_path_v_kof = path_assets + "kof_720.mp4"
g_path_v_boo = path_assets + "boo_dancing.mp4"
g_path_i_ball = path_assets + "basketball.jpg"
g_path_v_ball = path_assets + "basketball_bouncing_animation_in_blender.mp4"
g_path_v_borb_480 = path_assets + "borboleta_480.mp4"
g_path_v_borb_1080 = path_assets + "borboleta_1080.mp4"


def __visualizar_escala_cores(frame) -> Axes3D:
	col1, col2, col3 = cv2.split(frame)
	fig = pyplot.figure()
	eixos = fig.add_subplot(1, 1, 1, projection="3d")

	pixel_colors = frame.reshape((numpy.shape(frame)[0] * numpy.shape(frame)[1], 3))
	norm = colors.Normalize(vmin=-1., vmax=1.)
	norm.autoscale(pixel_colors)
	pixel_colors = norm(pixel_colors).tolist()

	eixos.scatter(col1.flatten(), col2.flatten(), col3.flatten(), facecolors=pixel_colors, marker=".")

	return eixos


def visualizar_escala_cor(frame):
	eixos = __visualizar_escala_cores(frame)
	eixos.set_xlabel("Red")
	eixos.set_ylabel("Green")
	eixos.set_zlabel("Blue")
	pyplot.show()
	return None


def visualizar_escala_hsv(frame_hsv):
	eixos = __visualizar_escala_cores(frame_hsv)
	eixos.set_xlabel("Hue")
	eixos.set_ylabel("Saturation")
	eixos.set_zlabel("Value")
	pyplot.show()
	return None


# Área para manipulação de imagem
def obter_contorno(frame_masc):
	# Encontra os contornos do frame com máscara (preto e branco)
	_, contornos, _ = cv2.findContours(
		frame_masc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	return contornos


def obter_contorno_tupla(frame_masc):
	# Encontra os contornos do frame com máscara (preto e branco)
	return cv2.findContours(
		frame_masc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


def desenhar_centro_massa_novo(frame_masc, frame_rgb) -> (float, float):
	img2, contornos, hierarquia = cv2.findContours(
		frame_masc, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	# finding contour with maximum area and store it as best_cnt
	max_area = 0
	best_cnt = None

	for cnt in contornos:
		area = cv2.contourArea(cnt)

		if area > max_area:
			max_area = area
			best_cnt = cnt

	momentos = cv2.moments(best_cnt)

	cx = cy = 1

	if momentos['m00'] != 0:
		cx = int(momentos['m10'] / momentos['m00'])
		cy = int(momentos['m01'] / momentos['m00'])

	cv2.circle(frame_rgb, (cx, cy), 5, 255, -1)

	return (cx, cy)


def aplicar_mascara(frame_rgb):
	hsv = cv2.cvtColor(frame_rgb, cv2.COLOR_BGR2HSV)

	cor_intev_min = numpy.array([0, 100, 50])
	cor_intev_max = numpy.array([10, 255, 255])

	mascara = cv2.inRange(hsv, cor_intev_min, cor_intev_max)

	return mascara


def desenhar_contorno(frame_mascara, frame_rgb):
	_, contornos, _ = cv2.findContours(
		frame_mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	# Desenha um contorno roxo, de expessura 1, no frame original
	cv2.drawContours(frame_rgb, contornos, -1, (255, 0, 255), 1)


# -----------------------------------


def processar_video(path_video: str, particulas: GrupoParticula):
	"""Processa cada frame do vídeo com o acompanhamento das partículas

	Args:
		path_video: Caminho do arquivo de vídeo a ser processado
		particulas: Grupo já inicializado com suas partículas
	"""

	video = cv2.VideoCapture(path_video)
	cv2.namedWindow("saida_video", cv2.WINDOW_NORMAL)
	cv2.resizeWindow('saida_video', 900, 650)

	# Enquanto o vídeo não finalizar
	while video.isOpened():

		# Leia cada frameq
		ret, frame = video.read()

		# Se o vídeo terminou, finalize a função
		if frame is None:
			break

		# Aplique um borramento para diminuir ruídos e granularidade
		frame_clone = cv2.blur(frame, (40, 25))

		frame_masc = aplicar_mascara(frame_clone)
		centro = desenhar_centro_massa_novo(frame_masc, frame)
		desenhar_contorno(frame_masc, frame)

		particulas.atualizar_particulas(1, {"x": centro[0], "y": centro[1]})
		particulas.reamostrar()

		for i in range(particulas.n):
			p = particulas.get(i)
			cv2.circle(frame, (p.eixos["x"], p.eixos["y"]), 3, (0, 0, 255), -1)

		c_grupo = particulas.get_media_xyv()
		cv2.circle(frame, (int(c_grupo[0]), int(c_grupo[1])), 7, (0, 255, 0), -1)

		cv2.imshow("saida_video", frame)

		# Se a tecla 'q' for pressionada, interrompa o processamento
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# Libere o vídeo E destrua todas janelas criadas pelo OpenCV
	video.release()
	cv2.destroyAllWindows()

	return None


def main():
	eixos_max = {"x": 900, "y": 650}
	grupo_part: GrupoParticula = GrupoParticula(50, 10, 1, 20, eixos_max, 5)
	processar_video(g_path_v_ball, grupo_part)

	return 0


if __name__ == '__main__':
	main()
