# from util.util import instalar_dependencias

# instalar_dependencias()
from typing import Tuple

import cv2

from dominio.entidades.particula import GrupoParticula
from dominio.util.util_imagem_opencv import UtilImgOpenCV

path_assets = "../assets/"
g_path_v_gow = path_assets + "gow2.mp4"
g_path_v_kof = path_assets + "kof_720.mp4"
g_path_v_boo = path_assets + "boo_dancing.mp4"
g_path_i_ball = path_assets + "basketball.jpg"
g_path_v_ball = path_assets + "basketball_bouncing_animation_in_blender.mp4"
g_path_v_borb_480 = path_assets + "borboleta_480.mp4"
g_path_v_borb_1080 = path_assets + "borboleta_1080.mp4"


def processar_video(
		path_video: str, dimensao_video: Tuple[int, int],
		particulas: GrupoParticula):
	"""Processa cada frame do vídeo com o acompanhamento das partículas

	Args:
		path_video: Caminho do arquivo de vídeo a ser processado
		dimensao_video: Par com a resolução do vídeo em pixel (larg x alt)
		particulas: Grupo já inicializado com suas partículas
	"""

	video = cv2.VideoCapture(path_video)

	# Enquanto o vídeo não finalizar
	while video.isOpened():

		# Leia cada frameq
		ret, frame = video.read()

		# Se o vídeo terminou, finalize a função
		if frame is None:
			break

		# Aplique um borramento para diminuir ruídos e granularidade
		frame_clone = cv2.blur(frame, (40, 25))

		frame_masc = UtilImgOpenCV.aplicar_mascara(frame_clone)
		centro = UtilImgOpenCV.desenhar_centro_massa(frame_masc, frame)
		UtilImgOpenCV.desenhar_contorno(frame_masc, frame)
		UtilImgOpenCV.desenhar_box(frame_masc, frame)

		# TRECHO PERTENCENTE AO GRUPO DE PARTÍCULAS
		particulas.atualizar_particulas(1, {"x": centro[0], "y": centro[1]})
		particulas.reamostrar()

		for i in range(particulas.n):
			p = particulas.get(i)
			cv2.circle(frame, (p.eixos["x"], p.eixos["y"]), 3, (0, 0, 255), -1)

		cv2.imshow("saida_video", frame)

		# Se a tecla 'q' for pressionada, interrompa o processamento
		if cv2.waitKey(10) & 0xFF == ord('q'):
			break

	# Libere o vídeo E destrua todas janelas criadas pelo OpenCV
	video.release()
	cv2.destroyAllWindows()

	return None


def main():
	v_dimensao = (1270, 710)
	eixos_max = {"x": v_dimensao[0], "y": v_dimensao[1]}
	grupo_part: GrupoParticula = GrupoParticula(50, 1, 20, eixos_max, 5)
	processar_video(g_path_v_ball.replace(".mp4", "-ext.mp4"), v_dimensao, grupo_part)

	return 0


if __name__ == '__main__':
	main()
