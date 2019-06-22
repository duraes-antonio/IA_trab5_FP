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
        import imutils

    except ImportError:

        print("Instalando dependências, aguarde...")

        # Se for Windows, dê o comando, instale e limpe a tela
        if (platsys().upper() == "WINDOWS"):
            ossys("pip install --user matplotlib /quiet")
            ossys("pip install --user numpy /quiet")
            ossys("pip install --user imutils /quiet")
            ossys("cls")

        # Senão, é MAC ou Linux
        else:
            ossys("sudo apt-get install python3-tk")
            ossys("sudo apt-get install python3-opencv")
            ossys("pip3 install --user matplotlib")
            ossys("pip3 install --user numpy")
            ossys("pip3 install --user imutils")
            ossys("clear")
            print("Dependências instaladas com êxito!")

    # Se após tentar instalar, o erro ainda persistir, avise e saia
    finally:

        try:
            import matplotlib
            import numpy
            import cv2

        except:
            raise ImportError("Falha ao instalar dependências necessárias. Bye.")
