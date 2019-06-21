from os import system as ossys
from platform import system as platsys


def instalar_dependencias():
    """Tenta instalar a biblioteca matplotlib no sistema atual.

    Raises:
        ImportError: Se houver falha durante ou após instalar o matplotlib.
    """

    # Tente importar matplotlib, se falhar, tente instalar
    try:
        import cv2
        import matplotlib
        import numpy

    except ImportError:

        print("Instalando matplotlib, aguarde...")

        # Se for Windows, dê o comando, instale e limpe a tela
        if (platsys().upper() == "WINDOWS"):
            ossys("pip install --user matplotlib /quiet")
            ossys("pip install --user numpy /quiet")
            ossys("cls")

        # Senão, é MAC ou Linux
        else:
            ossys("sudo apt-get install python3-tk -y")
            ossys("sudo apt-get install python3-opencv -y")
            ossys("pip3 install --user matplotlib")
            ossys("pip3 install --user numpy")
            ossys("clear")

    # Se após tentar instalar, o erro ainda persistir, avise e saia
    finally:

        try:
            import matplotlib
            import numpy
            import cv2

        except:
            raise ImportError("Falha ao instalar dependências necessárias. Bye.")
