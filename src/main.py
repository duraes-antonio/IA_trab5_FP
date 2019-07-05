from typing import Tuple
from argparse import ArgumentParser

import cv2

from dominio.entidades.particula import GrupoParticulaNumpyClean
from dominio.util.util_imagem_opencv import UtilImgOpenCV

path_assets = "../assets/"
g_path_v_ball = path_assets + "basketball_bouncing_animation_in_blender-ext.mp4"
g_path_v_boo = path_assets + "boo_dancing.mp4"
g_path_v_dbz = path_assets + "dbz.mp4"

# Cores BGR
VERMELHO = (0, 0, 255)
ROXO = (255, 0, 140)
VERDE = (0, 255, 0)
BRANCO = (255, 255, 255)


def ler_argumentos():
	global glob_abert_min, glob_num_pontos, glob_increm_ang
	parser = ArgumentParser()
	parser.add_argument("-a", "--angulo", help="Angulo de abertura do setor que se movimenta",
	                    type=float, required=True)
	parser.add_argument("-p", "--pontos", help="Quantidade de pontos que serão plotados",
	                    type=int, required=True)
	parser.add_argument("-v", "--velocidade", help="Número de graus que o setor andará a cada movimento",
	                    type=float, required=True)
	argumentos = parser.parse_args()

	if argumentos.angulo: glob_abert_min = argumentos.angulo
	if argumentos.pontos: glob_num_pontos = argumentos.pontos
	if argumentos.pontos: glob_increm_ang = argumentos.velocidade


def processar_video(
		path_video: str, dimensao_video: Tuple[int, int],
		nome_janela: str, particulas: GrupoParticulaNumpyClean):
	"""Processa cada frame do vídeo com o acompanhamento das partículas

	Args:
		path_video: Caminho do arquivo de vídeo a ser processado
		dimensao_video: Par com a resolução do vídeo em pixel (larg x alt)
		nome_janela: Título da janela em que o vídeo será renderizado
		particulas: Grupo já inicializado com suas partículas
	"""
	video = cv2.VideoCapture(path_video)
	cv2.namedWindow(nome_janela)

	# Enquanto o vídeo não finalizar
	while video.isOpened():

		# Leia cada quadro do vídeo
		ret, frame = video.read()

		# Se o vídeo terminou, finalize a função
		if frame is None:
			break

		# Borre o frame para uniformizar as cores do objeto e remover ruídos
		frame_clone = cv2.blur(frame, (30, 10))

		# Aplique uma máscara na imagem para deixar o objeto branco e o resto
		#  preto. A máscara deve destacar o objeto desejado por sua faixa de cor
		frame_masc = UtilImgOpenCV.aplicar_mascara(frame_clone)

		centro_obj = UtilImgOpenCV.obter_centro_massa(frame_masc)
		larg_alt = UtilImgOpenCV.obter_larg_alt_obj(frame_masc)

		# Execute o algorítimo de filtro de partículas
		particulas.atualizar_particulas(centro_obj)

		# Desenhe o centro de massa do objeto [Ponto verde] e sua box
		cv2.circle(frame, centro_obj, 5, VERMELHO, -1)
		UtilImgOpenCV.desenhar_box_pt(centro_obj, larg_alt, frame, VERMELHO)
		UtilImgOpenCV.desenhar_contorno(frame_masc, frame, VERDE)

		# Desenhe todas as partículas
		parts = particulas.obter_coords()
		[cv2.circle(frame, p, 3, BRANCO, -1) for p in parts]

		centro_partic = particulas.ponto_medio()

		# Desenhe o centro da núvem de partículas [Ponto verde] e sua box
		cv2.circle(frame, centro_partic, 5, ROXO, -1)
		UtilImgOpenCV.desenhar_box_pt(centro_partic, larg_alt, frame, ROXO)

		frame = cv2.resize(frame, dimensao_video)
		cv2.imshow(nome_janela, frame)

		# Se a tecla 'q' for pressionada, interrompa o processamento
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# Libere o vídeo E destrua todas janelas criadas pelo OpenCV
	video.release()
	cv2.destroyAllWindows()

	return None


def main():
	fator = .95
	v_dimensao = (int(1200 * fator), int(720 * fator))
	nome_janela = "saida"
	grupo_part = GrupoParticulaNumpyClean(
		(0, 0), 5, 3, 6, v_dimensao[0], v_dimensao[1])
	processar_video(g_path_v_ball, v_dimensao, nome_janela, grupo_part)
	return 0

main()
