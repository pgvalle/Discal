# Discal

Discal is a distributed calculator. It's a project for my Distributed Systems class.

## Requirements

### General

A comunicação entre os componentes (cliente, proxy reverso e servidores) deve ser feita via sockets em Python.
O código deve ser organizado em arquivos separados para o cliente, proxy reverso e servidores.
Testar a aplicação com múltiplos clientes e servidores para garantir o balanceamento correto de carga.

### Client

O cliente deverá se conectar ao proxy reverso e enviar uma requisição de operação matemática (ex: soma, subtração, multiplicação ou divisão) via socket.
O cliente deve ser capaz de receber e exibir o resultado da operação enviada após a intermediação do proxy reverso.

### Reverse Proxy (Load Balancer)

O proxy reverso deve escutar em uma determinada porta para receber as requisições dos clientes.
O proxy reverso deve se comunicar com múltiplos servidores para identificar qual servidor está menos sobrecarregado. Para isso, os servidores devem reportar sua carga atual de CPU ao proxy.
Com base na carga de CPU, o proxy deve selecionar o servidor mais apropriado (com menor carga) para encaminhar a requisição do cliente.
O proxy deve intermediar a comunicação entre o cliente e o servidor selecionado, repassando a resposta do servidor de volta ao cliente.
O proxy reverso deverá ser capaz de lidar com múltiplas requisições de clientes de forma simultânea, implementando controle de concorrência se necessário.

### Servers

Cada servidor deve escutar em duas portas diferentes:
Porta de Status: para responder à solicitação do proxy reverso sobre a carga atual de CPU.
Porta de Serviço de Calculadora: para receber e processar operações matemáticas (soma, subtração, multiplicação, divisão) enviadas pelo proxy reverso.
O servidor deve retornar a carga de CPU quando solicitado pelo proxy reverso.
O servidor deve processar a operação matemática enviada pelo cliente (via proxy) e retornar o resultado ao proxy, que por sua vez o encaminhará de volta ao cliente.
O servidor deve registrar no console cada operação matemática realizada para fins de depuração.
