from os import system as ossys
from platform import system as platsys
from typing import List


def instalar_dependencias():
	"""Tenta instalar as ferramentas no sistema atual.

	Args:
		nomes: Nomes das bibliotecas a serem instaladas

	Raises:
		ImportError: Se houver falha durante ou após instalar
	"""

	# Tente importar cada ferramenta, se falhar, tente instalar
	try:

    import cv2

	except ImportError:

		print("Instalando dependências, aguarde...")

		# ossys("sudo apt-get install python3-tk")
		# ossys("sudo apt-get install python3-opencv")

for lib in ["opencv-python"]:

			print(f">>> Tentando instalar '{lib}'")

			# Se for Windows
			if (platsys().upper() == "WINDOWS"):
ossys(f"pip install --user {lib}")

# Senão, é MAC ou Linux
else:
ossys(f"pip3 install --user {lib}")

# Se for Windows
if (platsys().upper() == "WINDOWS"):
    ossys("cls")

# Senão, é MAC ou Linux
else:
    ossys("clear")

		print("--> Dependências instaladas com êxito!")

	# Se após tentar instalar, o erro ainda persistir, avise e saia
	finally:

		try:
import cv2

		except:
			raise ImportError("Falha ao instalar dependências necessárias. Bye.")
