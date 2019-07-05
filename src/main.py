from os import path
from typing import Tuple
from argparse import ArgumentParser, ArgumentTypeError

import cv2

from dominio.entidades.particula import GrupoParticulas
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


class Args:

	def __init__(
			self, num_part: int, v_min: float, v_max: float,
			path_video: str, exib_centro: bool, exib_box: bool,
			dimensao: float, frames_atraso: int):
		self.num_part = num_part
		self.vel_min = v_min
		self.vel_max = v_max
		self.path_video = path_video
		self.exibir_centro = True if exib_centro is None else bool(exib_centro)
		self.exibir_box = True if exib_box is None else bool(exib_box)
		self.atraso = 1 if frames_atraso is None else int(frames_atraso)

		if dimensao is not None and 1 >= dimensao >= 0.1:
			self.dimensao = dimensao

		else:
			self.dimensao = 0.93


def ler_argumentos() -> Args:
	parser = ArgumentParser()

	def __restringir_num(valor, min_v: float, max_v: float) -> float:
		val = float(valor)

		if val < min_v or val > max_v:
			raise ArgumentTypeError(
				f"Argumento fora do intervalo [{min_v}, {max_v}]")
		return val

	def validar_part(valor):
		return __restringir_num(int(valor), 1, 10000)

	def validar_dimensao(dimensao):
		return __restringir_num(float(dimensao), 0.1, 1)

	def validar_path(caminho: str):

		if path.isfile(caminho):
			return caminho

		else:
			raise ArgumentTypeError(
				"O caminho não existe ou não pertence a um arquivo")

	parser.add_argument(
		"-n", type=validar_part, required=True,
		help="Número de partículas")

	parser.add_argument(
		"-v1", type=float, required=True,
		help="Velocidade mínima aceita")

	parser.add_argument(
		"-v2", type=float, required=True,
		help="Velocidade máxima aceita")

	parser.add_argument(
		"-p", type=validar_path, required=True,
		help="Caminho do vídeo a ser processado")

	parser.add_argument(
		"-c", type=int, required=False, choices=[0, 1],
		help="Define se os centróides das partículas e do objeto será exibido")

	parser.add_argument(
		"-b", type=int, required=False, choices=[0, 1],
		help="Define se a caixa das partículas e a do objeto serão exibidas")

	parser.add_argument(
		"-d", type=validar_dimensao, required=False,
		help="Fator que multiplica a dimensão do vídeo (entre 0.1 e 1)")

	parser.add_argument(
		"-f", type=validar_part, required=False,
		help="Quantidade de frames a serem atrasados (Quanto mais, maior a pausa)")

	args = parser.parse_args()

	return Args(args.n, args.v1, args.v2, args.p, args.c, args.b, args.d, args.f)


def processar_video(args: Args):
	"""Processa cada frame do vídeo com o acompanhamento das partículas

	Args:
		args: Objeto contendo argumentos p/ criar as partículas e path do vídeo
	"""
	video = cv2.VideoCapture(args.path_video)
	cv2.namedWindow("Saída")

	# Obtenha a largura e altura do frame (resolução do vídeo)
	dimensao = int(video.get(3) * args.dimensao), int(video.get(4) * args.dimensao)

	grupo_part: GrupoParticulas = None

	if video.isOpened():
		grupo_part = GrupoParticulas(
			int(args.num_part), args.vel_min, args.vel_max, dimensao[0], dimensao[1])

	else:
		raise IOError("Não foi possível abrir o vídeo")

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

		# Execute o algorítimo de filtro de partículas
		grupo_part.atualizar_particulas(centro_obj)

		# Desenhe todas as partículas
		parts = grupo_part.obter_coords()
		[cv2.circle(frame, p, 3, BRANCO, -1) for p in parts]

		larg_alt = UtilImgOpenCV.obter_larg_alt_obj(frame_masc)
		centro_partic = grupo_part.ponto_medio()

		if args.exibir_centro:
			# Desenhe o centro de massa do objeto [Ponto verde]
			cv2.circle(frame, centro_obj, 5, VERMELHO, -1)

			# Desenhe o centro da núvem de partículas [Ponto roxo]
			cv2.circle(frame, centro_partic, 5, ROXO, -1)

		if args.exibir_box:
			# Desenhe de vermelho, a box do objeto
			UtilImgOpenCV.desenhar_box_pt(centro_obj, larg_alt, frame, VERMELHO)

			# E de roxo, a box das partículas
			UtilImgOpenCV.desenhar_box_pt(centro_partic, larg_alt, frame, ROXO)

		# if args.contornar_obj:
		# 	UtilImgOpenCV.desenhar_contorno(frame_masc, frame, VERDE)

		frame = cv2.resize(frame, dimensao)
		cv2.imshow("saida", frame)

		# Se a tecla 'q' for pressionada, interrompa o processamento
		if cv2.waitKey(args.atraso) & 0xFF == ord('q'):
			break

	# Libere o vídeo E destrua todas janelas criadas pelo OpenCV
	video.release()
	cv2.destroyAllWindows()

	return None


def main():
	args: Args = ler_argumentos()
	processar_video(args)
	return 0


main()
