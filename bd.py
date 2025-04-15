import sqlite3

class Banco:

    def __init__(self):
        self.conexao = sqlite3.connect("teste.db")
        cursor = self.conexao.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS teste(id INTEGER PRIMARY KEY, nome, idade, endereco, cep, time_de_coracao)")
        self.conexao.commit()
        cursor.close()

    def adicionar(self, nome, idade, endereco, CEP,time_de_coracao):
        cursor = self.conexao.cursor()
        cursor.execute('INSERT INTO teste(nome, idade, endereco, CEP,time_de_coracao) VALUES(?,?,?,?,?)', (nome, idade, endereco, CEP,time_de_coracao))
        if(cursor.rowcount > 0):
            id = cursor.lastrowid
        else:
            id = None
        self.conexao.commit()
        cursor.close()
        return id
    
    # retorna uma tupla contendo todos os campos, na mesma ordem de criação do banco
    def buscar(self, id):
        cursor = self.conexao.cursor()
        cursor.execute('SELECT * FROM teste WHERE id = ?', (id,))
        retorno = cursor.fetchone()
        cursor.close()
        return retorno
    
    def remover(self,id):
        retorno = self.buscar(id)
        if retorno:
            cursor = self.conexao.cursor()
            cursor.execute('DELETE FROM teste WHERE id = ?', (id,))
            # Commit da transação para garantir que a remoção seja aplicada
            self.conexao.commit()
            cursor.close()
            return retorno
        else:
            return None


    
    def atualizar(self, id, nome = None, idade = None, endereco = None, CEP = None, time_de_coracao = None):
        dados = self.buscar(id)
        if dados:
            nome = nome if nome else dados[1]
            idade = idade if idade else dados[2]
            endereco = endereco if endereco else dados[3]
            CEP = CEP if CEP else dados[4]
            time_de_coracao = time_de_coracao if time_de_coracao else dados[5]
            cursor = self.conexao.cursor()
            cursor.execute('UPDATE teste SET nome = ?, idade = ?, endereco = ?, CEP = ?, time_de_coracao = ? WHERE id = ?', (nome, idade, endereco, CEP,time_de_coracao, id))
            self.conexao.commit()
            if (cursor.rowcount > 0):
                dados = self.buscar(id)
            else:
                dados = None
            cursor.close()
            
            return dados
        else:
            return None