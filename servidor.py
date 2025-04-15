import bd
import socket

def main():
    try:
        # Criando o socket
        socketConexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        endereco = ("127.0.0.1", 50000)
        socketConexao.bind(endereco)
        
        # Escutando por uma conexão
        socketConexao.listen(1)
        print("Aguardando conexão...")
        
        # Aceitando a conexão
        dados, endereco_cliente = socketConexao.accept()
        print(f"Conexão estabelecida com {endereco_cliente}")

        Banco = bd.Banco()
        
        while True:
            try:
                # Recebe a opção do cliente
                opcao = int.from_bytes(dados.recv(1),'big')

                if opcao == 5:
                    print("Encerrando conexão...")
                    break

                elif opcao == 1:  # Adicionar dados
                    try:
                        nome_tam = int.from_bytes(dados.recv(1),'big')
                        nome = dados.recv(nome_tam).decode('utf-8')  
                        idade = int.from_bytes(dados.recv(1),'big')
                        endereco_tam = int.from_bytes(dados.recv(1),'big')
                        endereco = dados.recv(endereco_tam).decode('utf-8')
                        cep = dados.recv(8).decode('utf-8')
                        time_tam = int.from_bytes(dados.recv(1),'big')
                        time_de_coracao = dados.recv(time_tam).decode('utf-8')  
                        id_cliente = Banco.adicionar(nome, idade, endereco, cep,time_de_coracao) 
                        envio = id_cliente.to_bytes(4, byteorder='big')
                        dados.send(envio)  # Envia o tamanho e o ID para o cliente
                    except (ValueError, UnicodeDecodeError) as e:
                        print(f"Erro ao processar os dados recebidos: {e}")
                          

                elif opcao == 2:  # Buscar dados
                    try:
                        id_buscado = int.from_bytes(dados.recv(1),'big') 
                        retorno = Banco.buscar(id_buscado)
                        
                        if retorno:
                            id_cliente, nome, idade, endereco, cep, time_de_coracao = retorno
                            opcode = b'\x05'
                            msg = opcode  
                            msg += len(nome).to_bytes(1, 'big') + nome.encode()
                            msg += idade.to_bytes(1, 'big')
                            msg += len(endereco.encode()).to_bytes(1, 'big') + endereco.encode()
                            msg += str(cep).encode()
                            msg += len(time_de_coracao).to_bytes(1,'big') + time_de_coracao.encode()
                            dados.send(msg)
                        else:
                            # Caso o ID não seja encontrado, envia um erro para o cliente
                            erro_msg = b'\x06'  # Código de erro
                            dados.send(erro_msg)
                            print(f"ID {id_buscado} não encontrado no Banco de Dados.")
                    
                    except (ValueError, IndexError) as e:
                        # Caso ocorra erro de valor ou índice, envia um erro para o cliente
                        erro_msg = b'\x06'  # Código de erro
                        dados.send(erro_msg)
                        print(f"Erro ao buscar dados: {e}")

                    
                elif opcao == 3:  # Atualizar dados
                    try:
                        id_buscado = int.from_bytes(dados.recv(1),'big') 
                        nome_tam = int.from_bytes(dados.recv(1), 'big') 
                        nome = dados.recv(nome_tam).decode('utf-8')  if nome_tam > 0 else None
                        idade_aux = dados.recv(1)
                        idade = int.from_bytes(idade_aux,'big') if idade_aux != b'\x00' else None
                        endereco_tam = int.from_bytes(dados.recv(1),'big')
                        endereco = dados.recv(endereco_tam).decode('utf-8') if endereco_tam > 0 else None
                        cep_tam = int.from_bytes(dados.recv(1), 'big')
                        cep = dados.recv(cep_tam).decode('utf-8')  if cep_tam > 0 else None
    
                        time_tam = int.from_bytes(dados.recv(1), 'big') 
                        time_de_coracao = dados.recv(time_tam).decode('utf-8')  if time_tam > 0 else None
                        
                        
                        resultado = Banco.atualizar(id_buscado, nome, idade, endereco, cep,time_de_coracao)
                        
                        if resultado:  
                            id_cliente, nome, idade, endereco, cep,time_de_coracao = resultado
                            
                            opcode = b'\x05'  
                            msg = opcode
                            msg += len(nome).to_bytes(1, 'big') + nome.encode()
                            msg += idade.to_bytes(1, 'big')
                            msg += len(endereco.encode()).to_bytes(1, 'big') + endereco.encode()
                            msg += len(cep).to_bytes(1, 'big') + cep.encode()
                            msg += len(time_de_coracao).to_bytes(1,'big') + time_de_coracao.encode()
                            dados.send(msg)
                        else:  
                            print(f"Erro ao atualizar dados: ID {id_buscado} não encontrado.")
                            erro_opcode = b'\x06'  
                            dados.send(erro_opcode)  
                    except (ValueError, IndexError) as e:
                        print(f"Erro ao atualizar dados: {e}")
                        erro_opcode = b'\x06'  
                        dados.send(erro_opcode)  


                elif opcao == 4:  # Remover dados
                    try:
                        id_buscado = int.from_bytes(dados.recv(1),'big') 
                        retorno = Banco.remover(id_buscado)
                        
                        if retorno:
                            id_cliente, nome, idade, endereco, cep,time_de_coracao = retorno
                            opcode = b'\x05'
                            msg = opcode  
                            msg += len(nome).to_bytes(1, 'big') + nome.encode()
                            msg += idade.to_bytes(1, 'big')
                            msg += len(endereco.encode()).to_bytes(1, 'big') + endereco.encode()
                            msg += str(cep).encode()
                            msg += len(time_de_coracao).to_bytes(1,'big') + time_de_coracao.encode()
                            dados.send(msg)
                        else:
                            # Caso o ID não seja encontrado, envia um erro ao cliente
                            erro_msg = b'\x06'  # Opcional: Código de erro
                            dados.send(erro_msg)
                            print("Erro ao encontrar ID no Banco de Dados")  # Log do erro no servidor

                    except Exception as e:
                        # Caso aconteça qualquer outro erro, envia um erro para o cliente
                        erro_msg = b'\x06'  # Opcional: Código de erro
                        dados.send(erro_msg)
                        print(f"Erro ao remover dados: {e}")  # Log do erro no servidor

                else:
                    print('Opção inválida!!')
                    break
                    

            except Exception as e:
                print(f"Erro ao processar a opção: {e}")
                break 

        dados.close()
        socketConexao.close()

    except (socket.error, Exception) as e:
        print(f"Erro de conexão ou erro geral: {e}")
        socketConexao.close()

if __name__ == "__main__":
    main()
