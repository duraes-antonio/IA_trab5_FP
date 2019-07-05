# Inteligência Artificial - Trabalho 5 - Filtro de Partículas

Implementação e observações levantadas sobre o algorítimo Filtro de Partículas.

<p align="center"/>
<img src="https://cdn131.picsart.com/281241735010211.png?r1024x1024" alt="Smiley face" width="420">

## APRESENTAÇÃO

INTEGRANTES:
* Antônio Carlos D. da Silva
* Joel Will Belmiro

CONTEXTO:
* Disciplina: Inteligência Artificial (Sistemas de Informação, optativa do 8º Período)
* Implementação e exploração do algorítimo Filtro de Partículas


## 1. EXPLICAÇÃO TEÓRICA DO ALGORITMO

## 2. PROBLEMA PROPOSTO

<p align="justify"/>
A aplicação escolhida para teste do algoritmo foi o rastreamento de um objeto em um vídeo, mais especificamente, uma bola de basquete.
<br>

<p align="justify"/>
O problema resume-se, essencialmente, na distinção do objeto-alvo de outros itens presentes no cenário, na captura do máximo possível da área do corpo do objeto para que seja possível calcular as coordenadas de seu centro de massa com precisão satisfatória.
<br>

## 3. IMPLEMENTAÇÃO

<p align="justify"/>
Para melhor divisão de tarefas, organização e consequente qualidade do código, a implementação foi particionada em 3 arquivos principais:
    * “main.py”: A aplicação, responsável por capturar e validar brevemente os argumentos de entrada (número de partículas, velocidade, caminho do vídeo, etc), por chamar as funções do opencv para filtro de imagens e por coordenar como o resultado do algorítimo será exibido (cores, box, contorno)
    * “util_imagem_opencv.py”: Um conjunto de funções para manipulação de imagem (blur, conversão RGB para HSV, cálculo do centro de massa) e aplicação de filtros do Opencv
    * “particula.py”: Classe responsável por conter o filtro de partículas e seus métodos.
<br><br>

<p align="justify"/>
O foco do detalhamento da implementação será nos métodos e modelagem do algorítimo de filtro de partículas.
<br>

### 3.1  Grupo de partículas

<p align="justify"/>
Modelagem: O grupo de partículas é um array contendo N sub-arrays com x e y, representando uma partícula. Os pesos estão em um array a parte. Essa modelagem simples, com pouca orientação a objeto foi utilizada com intenção de maximizar ao máximo o desempenho do algoritmo, evitando travamentos durante a exibição do vídeo.
<br><br>

<p align="justify"/>
Instanciação: Para instanciar um grupo de partículas é necessário passar como argumentos: O número desejado, a velocidade mínima, a velocidade máxima, a posição máxima para X e para Y, além de um centro de massa inicial (que é opcional, se nada for passado, é usado a coordenada [0, 0]).
<br><br>

### 3.2  Predição

<p align="justify"/>
A etapa de predição trabalha com o centro de massa do objeto no instante atual (t) e também no instante anterior (t-1). A ideia básica é calcular a distância entre a posição atual do objeto e sua posição anterior, e somar tal valor com uma velocidade randômica entre o mínimo e máximo (o uso de ruídos randômicos também foram utilizados).
<br><br>

<p align="justify"/>
Para encontrar a diferença em graus entre a antiga e a nova posição do objeto, a função arco tangente foi utilizada, também empregou-se o uso das funções cosseno e seno, a primeira para cálculo do incremento do eixo x, e a segunda para incremento de y.
<br><br>

### 3.3  Atualização

<p align="justify"/>
Nesta etapa, os pesos das partículas são calculados e normalizados com base na distância de cada partícula em relação ao centro de massa atual do objeto. Após ter essa distância armazenada, utiliza-se uma função de densidade de probabilidade para atribuir peso a cada partícula.
<br><br>

<p align="justify"/>
Todas as partículas encontram-se com peso igual a 1. Para um desvio theta (neste caso, igual a 20, podendo ser qualquer outro valor), o peso da partícula será multiplicado pela chance dela possuir distância zero até o centro de massa do objeto, isto é, quanto mais próxima do objeto, maior será o peso da partícula.
<br><br>

### 3.4 Reamostragem

<p align="justify"/>
Como já descoberto em testes e documentado em artigos [1] a cada iteração o algorítimo pode sofrer com a degeneração causada pelo aumento constante de peso de algumas partículas.
<br><br>

<p align="justify"/>
Imagine que 100 partículas são sorteadas randomicamente e que somente três delas se aproximaram significativamente do centro de massa do objeto. As outras 97 partículas ficaram dispersas pelo espaço, transmitindo a sensação de pouca convergência do algorítimo, mais do que isso, estão consumindo recursos como memória e processamento, sem contribuir de forma efetiva para a acurácia da aplicação, com a chance de inclusive, estar degradando o desempenho das poucas partículas que obtiveram êxito.
<br><br>

<p align="justify"/>
Para minimizar o problema da degradação, vários modelos do algorítimo implementam a etapa de reamostragem, que é a atualização de partículas do conjunto ou  ou substituição por outras mais aptas.
<br><br>

<p align="justify"/>
A reamostragem implementada faz uso da substituição de partículas ruins por partículas de maior peso, e o faz com o sorteamento de partículas do próprio grupo, levando em consideração o peso de cada partícula. Ou seja, partículas de pesos mais altos possuem chance maior de compor o novo grupo.
<br><br>

<p align="justify"/>
Após aplicar a reamostragem, que é a etapa final do filtro, o centro de massa atual substitui o antigo; a aplicação solicita ao grupo de partículas suas coordenadas e as plotam.
<br><br>

## 4. EXEMPLO DE USO

<p align="justify"/>
Para executar a aplicação, deve-se executar os seguintes comandos para instalar as dependências (NumPy, SciPy, OpenCV) utilizadas:
<br><br>

O comando para Windows é o mesmo, apenas remove-se o ‘3’ depois do ‘pip’:
<br><br>

<p align="justify"/>
O algoritmo foi estruturado sob uma aplicação de linha de comando (CLI), portanto, os parâmetros e taxas envolvidas são livres para entrada do usuário. Abaixo é possível conferir um exemplo de execução com 20 partículas, velocidade mínima de 3 e máxima de 6 e com vídeo no caminho ‘../assets/basketball.mp4’:
<br><br>

Em caso de dúvidas sobre cada parâmetro, basta chamar a aplicação passando o parâmetro '-h':
<br><br>

<p align="justify"/>
Observação: Para sistemas Windows, a chamada é a mesma, porém em vez de utilizar “python3” para chamar a linguagem, usa-se apenas “python”.
<br><br>

Explicação sobre parâmetros de entrada:
    * -n: Número inteiro de partículas;
    * -v1: Número real para velocidade mínima;
    * -v2: Número real para velocidade máxima;
    * -p: Caminho do vídeo a ser processado;
<br>

Parâmetros opcionais:
    * -c: Valor lógico (0 ou 1), define se os centroides das partículas e do objeto serão exibidos;
    * -b: Valor lógico (0 ou 1), define se a box do ponto médio das partículas e a box do objeto serão exibidas;
    * -d: Valor real (entre 0.1 e 1) que definem a dimensão (altura e largura) do vídeo;
    * -f: Valor inteiro que indica o fator de atraso na exibição do vídeo. O valor padrão é 1, quanto maior mais lenta será a exibição, ideal para acompanhar o movimento das partículas;
<br>

## 5. RESULTADOS E OBSERVAÇÕES


## 6. REFERÊNCIAS E OUTROS MATERIAIS BASE

[1]. Página 16. Acesso em 05/07/2019. Disponível em:
http://repositorio.ufes.br/bitstream/10/4241/1/tese_4175_.pdf

[2]. Código base para construção do filtro. Acesso em 03/07/2019. Disponível em:
http://ros-developer.com/2019/04/10/parcticle-filter-explained-with-python-code-from-scratch/
