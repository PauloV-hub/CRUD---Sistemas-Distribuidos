import socket

# Conectar ao servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 50000))

while True:
    print("Escolha uma das opções abaixo:")
    print("1 - Inserir")
    print("2 - Buscar")
    print("3 - Atualizar")
    print('4 - Remover')
    print("5 - Sair")

    try:
        opcao = int(input("\nDigite a opção desejada: "))
        if opcao < 1 or opcao > 5:
            print("Opção inválida! Por favor, insira um número entre 1 e 5.")
            continue  # Volta para o início do loop para pedir a opção novamente
    except ValueError:
        print("Opção inválida! Por favor, insira um número de 1 a 5.")
        continue  

    print()

    if opcao == 1:  # Inserção
        nome = input('Digite nome: ')
        idade = input('Digite idade: ')
        endereco = input('Digite endereco: ')
        cep = input('Digite CEP: ')
        time_de_coracao = input('Digite Time de Coração: ')

        try:
            idade = int(idade)  # Garantir que a idade seja um número
        except ValueError:
            print("Idade inválida! Por favor, insira um número válido para a idade.")
            continue  # Volta para a opção de inserção

        msg = opcao.to_bytes(1, 'big')
        msg += len(nome.encode()).to_bytes(1, 'big') + nome.encode()
        msg += idade.to_bytes(1, 'big')
        msg += len(endereco.encode()).to_bytes(1, 'big') + endereco.encode()
        msg += cep.encode()
        msg += len(time_de_coracao.encode()).to_bytes(1,'big') + time_de_coracao.encode()

        try:
            cliente.send(msg)
            # Receber resposta do servidor (ID inserido)
            opcode = cliente.recv(1)
            id_bytes = cliente.recv(4)
            id_usuario = int.from_bytes(id_bytes, byteorder='big')
            print(f'ID do usuário inserido: {id_usuario}')
        except socket.error as e:
            print(f"Erro de comunicação com o servidor: {e}")
            continue  # Volta para a próxima opção em caso de erro na comunicação

    elif opcao == 2:  # Busca
        try:
            id_busca = int(input('Digite id de busca: '))
        except ValueError:
            print("ID inválido! Por favor, insira um número válido.")
            continue  # Volta para a opção de busca

        msg = opcao.to_bytes(1, 'big') + id_busca.to_bytes(1, 'big')
        cliente.send(msg)

        try:
            # Retorno do servidor
            opcode = cliente.recv(1)

            if opcode == b'\x06':  # Erro
                print('Erro encontrado')
            else:
                tamanho_nome = int.from_bytes(cliente.recv(1), 'big')
                nome = cliente.recv(tamanho_nome).decode('utf-8')
                idade = int.from_bytes(cliente.recv(1), 'big')
                tamanho_endereco = int.from_bytes(cliente.recv(1), 'big')
                endereco = cliente.recv(tamanho_endereco).decode()
                cep = cliente.recv(8).decode()
                tamanho_time = int.from_bytes(cliente.recv(1), 'big')
                time_de_coracao = cliente.recv(tamanho_time).decode('utf-8')

                print(f"ID: {id_busca}, Nome: {nome}, Idade: {idade}, Endereço: {endereco}, CEP: {cep}, Time de Coração: {time_de_coracao}")
        except socket.error as e:
            print(f"Erro de comunicação com o servidor: {e}")
            continue  # Volta para a opção de busca

    elif opcao == 3:  # Atualizar
        try:
            id_update = int(input('Digite id de update: '))
        except ValueError:
            print("ID inválido! Por favor, insira um número válido.")
            continue  # Volta para a opção de atualização

        nome = input('Digite nome: ') or None
        idade = input('Digite idade: ')
        idade = int(idade) if idade else None
        endereco = input('Digite endereco: ') or None
        cep = input('Digite CEP: ') or None
        time_de_coracao = input('Digite Time de Coração: ') or None

        Msg_None = b'\x00'
        msg = opcao.to_bytes(1, 'big') + id_update.to_bytes(1, 'big')

        msg += len(nome.encode()).to_bytes(1, 'big') + nome.encode() if nome else Msg_None
        msg += idade.to_bytes(1, 'big') if idade else Msg_None
        msg += len(endereco.encode()).to_bytes(1, 'big') + endereco.encode() if endereco else Msg_None
        msg += len(cep.encode()).to_bytes(1,'big') + cep.encode() if cep else Msg_None
        msg += len(time_de_coracao.encode()).to_bytes(1, 'big') + time_de_coracao.encode() if time_de_coracao else Msg_None
        print(f"mensagem: {msg}")

        try:
            cliente.send(msg)
            opcode = cliente.recv(1)

            if opcode == b'\x06':  # Erro
                print('Erro encontrado')
            else:
                tamanho_nome = int.from_bytes(cliente.recv(1), 'big')
                nome = cliente.recv(tamanho_nome).decode('utf-8')
                idade = int.from_bytes(cliente.recv(1), 'big')
                tamanho_endereco = int.from_bytes(cliente.recv(1), 'big')
                endereco = cliente.recv(tamanho_endereco).decode()
                tamanho_cep = int.from_bytes(cliente.recv(1), 'big')
                cep = cliente.recv(tamanho_cep).decode('utf-8')
                tamanho_time = int.from_bytes(cliente.recv(1), 'big')
                time_de_coracao = cliente.recv(tamanho_time).decode('utf-8')

                print(f"ID: {id_update}, Nome: {nome}, Idade: {idade}, Endereço: {endereco}, CEP: {cep}, Time de Coração: {time_de_coracao}")
        except socket.error as e:
            print(f"Erro de comunicação com o servidor: {e}")
            continue  # Volta para a opção de atualização

    elif opcao == 4:  # Remover
        try:
            id_remove = int(input('Digite id de remoção: '))
        except ValueError:
            print("ID inválido! Por favor, insira um número válido.")
            continue  # Volta para a opção de remoção

        msg = opcao.to_bytes(1, 'big') + id_remove.to_bytes(1, 'big')
        cliente.send(msg)

        try:
            # Retorno do servidor
            opcode = cliente.recv(1)

            if opcode == b'\x06':  # Erro
                print('Erro encontrado')
            else:
                tamanho_nome = int.from_bytes(cliente.recv(1), 'big')
                nome = cliente.recv(tamanho_nome).decode('utf-8')
                idade = int.from_bytes(cliente.recv(1), 'big')
                tamanho_endereco = int.from_bytes(cliente.recv(1), 'big')
                endereco = cliente.recv(tamanho_endereco).decode()
                cep = cliente.recv(8).decode()
                
                tamanho_time = int.from_bytes(cliente.recv(1), 'big')
                time_de_coracao = cliente.recv(tamanho_time).decode('utf-8')
                print(f"ID: {id_remove}, Nome: {nome}, Idade: {idade}, Endereço: {endereco}, CEP: {cep}, Time de Coração: {time_de_coracao}")
        except socket.error as e:
            print(f"Erro de comunicação com o servidor: {e}")
            continue  # Volta para a opção de remoção

    else:  # Sair
        cliente.send(opcao.to_bytes(1, 'big'))
        break

cliente.close()
