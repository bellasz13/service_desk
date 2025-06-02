import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="isabella2005",
            database="helpdesk"
        )
        if conn.is_connected():
            print("Conexão ao banco de dados realizada com sucesso!")
        return conn
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def inserir_usuario(nome_completo, nome_usuario, email, tipo_usuario, senha):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            sql = """
                INSERT INTO usuarios (nome_completo, nome_usuario, email, tipo_usuario, senha)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nome_completo, nome_usuario, email, tipo_usuario, senha))
            conn.commit()
            print("Usuário cadastrado com sucesso!")
            return cursor.lastrowid
        except Error as e:
            raise Exception(f"Erro ao criar usuário: {e}")
        finally:
            cursor.close()
            conn.close()

def buscar_usuarios():
    conn = conectar()
    usuarios = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM usuarios")
            usuarios = cursor.fetchall()
        except Error as e:
            print(f"Erro ao buscar usuários: {e}")
        finally:
            cursor.close()
            conn.close()
    return usuarios

def buscar_usuario_por_id(id_usuario):
    conn = conectar()
    usuario = None
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            usuario = cursor.fetchone()
        finally:
            cursor.close()
            conn.close()
    return usuario


def atualizar_usuario(id_usuario, nome_completo, nome_usuario, email, tipo_usuario, senha=None):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            if senha:
                sql = """
                    UPDATE usuarios
                    SET nome_completo=%s, nome_usuario=%s, email=%s, tipo_usuario=%s, senha=%s
                    WHERE id_usuario=%s
                """
                cursor.execute(sql, (nome_completo, nome_usuario, email, tipo_usuario, senha, id_usuario))
            else:
                sql = """
                    UPDATE usuarios
                    SET nome_completo=%s, nome_usuario=%s, email=%s, tipo_usuario=%s
                    WHERE id_usuario=%s
                """
                cursor.execute(sql, (nome_completo, nome_usuario, email, tipo_usuario, id_usuario))
            conn.commit()
            print("Usuário atualizado com sucesso!")
        except Error as e:
            raise Exception(f"Erro ao atualizar usuário: {e}")
        finally:
            cursor.close()
            conn.close()

def excluir_usuario(id_usuario):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            sql = "DELETE FROM usuarios WHERE id_usuario=%s"
            cursor.execute(sql, (id_usuario,))
            conn.commit()
            print("Usuário excluído com sucesso!")
        except Error as e:
            raise Exception(f"Erro ao excluir usuário: {e}")
        finally:
            cursor.close()
            conn.close()

def verificar_usuario(nome_usuario, senha):
    conn = conectar()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM usuarios WHERE nome_usuario = %s"
            cursor.execute(sql, (nome_usuario,))
            resultado = cursor.fetchone()
            if resultado and resultado['senha'] == senha:
                return resultado
            else:
                return None
        except Error as e:
            print(f"Erro ao buscar usuário: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

def inserir_ticket(titulo, descricao, data_criacao, hora_criacao, status, prioridade, urgencia, categoria, sla, id_usuario_criador):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            sql = """
                INSERT INTO tickets (titulo, descricao, data_criacao, hora_criacao, status, prioridade, urgencia, categoria, sla, id_usuario_criador)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (titulo, descricao, data_criacao, hora_criacao, status, prioridade, urgencia, categoria, sla, id_usuario_criador))
            conn.commit()
            print("Ticket criado com sucesso!")
            return cursor.lastrowid
        except Error as e:
            raise Exception(f"Erro ao criar ticket: {e}")
        finally:
            cursor.close()
            conn.close()
            
def contar_tickets_atribuidos():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tickets WHERE status IN ('Aberto', 'Em Atendimento')")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count
    return 0

def contar_tickets_novos():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tickets WHERE status = 'Aberto'")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count
    return 0

def contar_tickets_espera():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tickets WHERE status = 'Em Espera'")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count
    return 0

def buscar_tickets_por_usuario(id_usuario):
    conn = conectar()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM tickets WHERE id_usuario_criador = %s"
            cursor.execute(sql, (id_usuario,))
            return cursor.fetchall()
        except Error as e:
            raise Exception(f"Erro ao buscar tickets: {e}")
        finally:
            cursor.close()
            conn.close()

def inserir_anexo(id_ticket, nome_arquivo, caminho_arquivo, data_upload):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            sql = """
                INSERT INTO anexos (id_ticket, nome_arquivo, caminho_arquivo, data_upload)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (id_ticket, nome_arquivo, caminho_arquivo, data_upload))
            conn.commit()
            print("Anexo adicionado com sucesso!")
        except Error as e:
            raise Exception(f"Erro ao adicionar anexo: {e}")
        finally:
            cursor.close()
            conn.close()

def buscar_anexos_ticket(id_ticket):
    conn = conectar()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM anexos WHERE id_ticket = %s"
            cursor.execute(sql, (id_ticket,))
            return cursor.fetchall()
        except Error as e:
            raise Exception(f"Erro ao buscar anexos: {e}")
        finally:
            cursor.close()
            conn.close()

def inserir_resposta(id_ticket, id_usuario, mensagem, data_resposta, hora_resposta):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            sql = """
                INSERT INTO respostas (id_ticket, id_usuario, mensagem, data_resposta, hora_resposta)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (id_ticket, id_usuario, mensagem, data_resposta, hora_resposta))
            conn.commit()
            print("Resposta adicionada com sucesso!")
        except Error as e:
            raise Exception(f"Erro ao adicionar resposta: {e}")
        finally:
            cursor.close()
            conn.close()

def buscar_respostas_ticket(id_ticket):
    conn = conectar()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM respostas WHERE id_ticket = %s"
            cursor.execute(sql, (id_ticket,))
            return cursor.fetchall()
        except Error as e:
            raise Exception(f"Erro ao buscar respostas: {e}")
        finally:
            cursor.close()
            conn.close()

def buscar_todos_tickets():
    conn = conectar()
    tickets = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM tickets")
            tickets = cursor.fetchall()
        except Error as e:
            print(f"Erro ao buscar todos os tickets: {e}")
        finally:
            cursor.close()
            conn.close()
    return tickets

def atualizar_ticket_status(id_ticket, novo_status):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            sql = "UPDATE tickets SET status = %s WHERE id_ticket = %s"
            cursor.execute(sql, (novo_status, id_ticket))
            conn.commit()
            print("Status do ticket atualizado com sucesso!")
        except Error as e:
            raise Exception(f"Erro ao atualizar status do ticket: {e}")
        finally:
            cursor.close()
            conn.close()

def atualizar_ticket_campos(id_ticket, prioridade, categoria, urgencia, sla):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            sql = """
                UPDATE tickets
                SET prioridade = %s, categoria = %s, urgencia = %s, sla = %s
                WHERE id_ticket = %s
            """
            cursor.execute(sql, (prioridade, categoria, urgencia, sla, id_ticket))
            conn.commit()
            print("Campos do ticket atualizados com sucesso!")
        except Error as e:
            raise Exception(f"Erro ao atualizar campos do ticket: {e}")
        finally:
            cursor.close()
            conn.close()

def tickets_por_dia_e_status():
    """
    Retorna uma tupla (dias, abertos, fechados), onde:
    - dias: lista de nomes dos dias da semana
    - abertos: lista com a contagem de tickets abertos por dia
    - fechados: lista com a contagem de tickets fechados por dia
    """
    conn = conectar()
    dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
    abertos = [0]*7
    fechados = [0]*7
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT DAYOFWEEK(data_criacao) as dia, status, COUNT(*) 
                FROM tickets
                WHERE data_criacao >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
                GROUP BY dia, status
            """)
            for dia, status, count in cursor.fetchall():
                idx = (dia + 5) % 7  
                if status == "Aberto":
                    abertos[idx] = count
                elif status == "Fechado":
                    fechados[idx] = count
        finally:
            cursor.close()
            conn.close()
    return dias, abertos, fechados

def contar_tickets_status():
    """
    Retorna um dicionário com contagem de tickets por status.
    """
    conn = conectar()
    resultado = {"atribuidos": 0, "novos": 0, "em_espera": 0, "fechados": 0}
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT status, COUNT(*) FROM tickets GROUP BY status
            """)
            for status, count in cursor.fetchall():
                if status == "Aberto":
                    resultado["atribuidos"] += count
                    resultado["novos"] += count
                elif status == "Em Espera":
                    resultado["em_espera"] += count
                elif status == "Fechado":
                    resultado["fechados"] += count
        finally:
            cursor.close()
            conn.close()
    return resultado

def pesquisar_tickets(termo):
    conn = conectar()
    tickets = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
                SELECT id_ticket AS id, titulo, status, categoria
                FROM tickets
                WHERE titulo LIKE %s OR CAST(id_ticket AS CHAR) LIKE %s OR categoria LIKE %s
            """
            like_termo = f"%{termo}%"
            cursor.execute(sql, (like_termo, like_termo, like_termo))
            tickets = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    return tickets

def pesquisar_usuarios(termo):
    conn = conectar()
    usuarios = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
                SELECT nome_completo AS nome, email, tipo_usuario AS tipo
                FROM usuarios
                WHERE nome_completo LIKE %s OR email LIKE %s OR tipo_usuario LIKE %s
            """
            like_termo = f"%{termo}%"
            cursor.execute(sql, (like_termo, like_termo, like_termo))
            usuarios = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    return usuarios

def pesquisar_categorias(termo):

    categorias = [
        "Novo cadastro", "Alterar cadastro", "Liberar acesso", "Cancelar cadastro/acesso",
        "Alterar senha", "Problemas com Office 365", "Suporte ao Office 365", "Suporte a impressora",
        "Instalar impressora", "Falha na impressão", "Ativar ponto de rede", "Compartilhamento de rede",
        "Bloquear/liberar site", "Falha de conexão ou rede", "Instalar software", "Software não funciona",
        "Instalar/substituir equipamentos", "Mudança de local", "Manutenção preventiva", "Teste de equipamentos",
        "Falha em computador/periférico", "Outro"
    ]
    return [ {"nome": c} for c in categorias if termo.lower() in c.lower() ]

def buscar_tickets_filtrados(
    status=None, categoria=None, prioridade=None, data_inicio=None, data_fim=None):
    conn = conectar()
    tickets = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
                SELECT t.*, u.nome_completo AS criador
                FROM tickets t
                JOIN usuarios u ON t.id_usuario_criador = u.id_usuario
                WHERE 1=1
            """
            params = []
            if status and status != "Todos":
                sql += " AND t.status = %s"
                params.append(status)
            if categoria and categoria != "Todas":
                sql += " AND t.categoria = %s"
                params.append(categoria)
            if prioridade and prioridade != "Todas":
                sql += " AND t.prioridade = %s"
                params.append(prioridade)
            if data_inicio:
                sql += " AND t.data_criacao >= %s"
                params.append(data_inicio)
            if data_fim:
                sql += " AND t.data_criacao <= %s"
                params.append(data_fim)
            cursor.execute(sql, tuple(params))
            for t in cursor.fetchall():
               
                cursor2 = conn.cursor(dictionary=True)
                cursor2.execute("SELECT * FROM respostas WHERE id_ticket = %s", (t["id_ticket"],))
                t["respostas"] = cursor2.fetchall()
                cursor2.close()
                
                t["id"] = t["id_ticket"]
                t["titulo"] = t["titulo"]
                t["descricao"] = t["descricao"]
                t["criador"] = t["criador"]
                t["data"] = t["data_criacao"]
                tickets.append(t)
        finally:
            cursor.close()
            conn.close()
    return tickets

def buscar_nome_usuario_por_id(id_usuario):
    conn = conectar()
    nome = None
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT nome_completo FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            resultado = cursor.fetchone()
            if resultado:
                nome = resultado[0]
        except Exception as e:
            print(f"Erro ao buscar nome do usuário: {e}")
        finally:
            cursor.close()
            conn.close()
    return nome

