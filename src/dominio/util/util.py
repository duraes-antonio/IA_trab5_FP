from os import system as ossys
from platform import system as platsys
from typing import List


def instalar_dependencias(nomes: List[str]):
	"""Tenta instalar as ferramentas no sistema atual.

	Args:
		nomes: Nomes das bibliotecas a serem instaladas

	Raises:
		ImportError: Se houver falha durante ou após instalar
	"""

	faltantes = list(nomes)

	# Tente importar cada ferramenta, se falhar, tente instalar
	try:

		for lib in nomes:
			import lib
			faltantes.remove(lib)

	except ImportError:

		print("Instalando dependências, aguarde...")

		# ossys("sudo apt-get install python3-tk")
		# ossys("sudo apt-get install python3-opencv")

		for lib in faltantes:

			print(f">>> Tentando instalar '{lib}'")

			# Se for Windows
			if (platsys().upper() == "WINDOWS"):
				ossys(f"pip install --user {lib} /quiet")

			# Senão, é MAC ou Linux
			else:
				ossys(f"pip3 install --user {lib} -q")

		print("--> Dependências instaladas com êxito!")

	# Se após tentar instalar, o erro ainda persistir, avise e saia
	finally:

		try:
			for lib in nomes:
				import lib

		except:
			raise ImportError("Falha ao instalar dependências necessárias. Bye.")
