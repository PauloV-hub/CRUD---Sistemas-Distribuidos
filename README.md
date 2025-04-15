Sistema CRUD com Sockets e SQLite
Este é um sistema de CRUD (Create, Read, Update, Delete) implementado utilizando Sockets para comunicação entre cliente e servidor. Os dados são armazenados em um banco de dados SQLite. O sistema permite adicionar, visualizar, atualizar e excluir dados de pessoas, com informações como nome, cep, time de coração, idade e endereço.

Funcionalidades
Create: Adiciona um novo registro com informações de nome, CEP, time de coração, idade e endereço.

Read: Visualiza todos os registros armazenados no banco de dados.

Update: Atualiza os dados de um registro existente.

Delete: Exclui um registro do banco de dados.

Estrutura de Dados
A estrutura de dados utilizada no sistema é a seguinte:

Nome: Nome completo da pessoa.

CEP: Código Postal da pessoa.

Time de Coração: O time de futebol favorito da pessoa.

Idade: A idade da pessoa.

Endereço: O endereço completo da pessoa.

Requisitos
Para rodar o sistema, você precisará de:

Python 3.x.

SQLite (geralmente já vem com o Python, mas pode ser necessário instalar o pacote sqlite3).
