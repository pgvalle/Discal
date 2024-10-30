from common import *

'''
Dois processos que se comunicam:
  1. Requere o uso da cpu nos servidores de tempos em tempos, guarda os registros
e faz um cálculo estatístico de alguma natureza. Manda o resultado quando requerido
pelo processo 2.
  2. Recebe as conexões dos clientes, manda pro servidor e repassa a resposta pros
clientes. Faz aquela história do fork. Requere o uso da cpu nos servidores do
processo 1.

'''


'''guardar registros de tempos em tempos (na faixa de segundos)
do uso da cpu em cada servidor. Depois fazer algum cálculo em cima
desses valores pra decidir qual servidor vai ser usado'''

'''Threads ou Forks para tratar as conexões com os clientes???'''

