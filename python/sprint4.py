#Membros:

#Giovanna Revito Roz - RM558981
#Kaian Gustavo de Oliveira Nascimento - RM558986
#Lucas Kenji Kikuchi - RM554424

#link do vídeo: https://youtu.be/u3U_4sKh3nA?si=XjzQxyMtKUed0Ym-

# módulo importado para utilização de regex
import re
# módulo importado para utilização de uuid
import uuid
# módulo importado para utilização do oracledb --> pip install oracledb
import oracledb
# módulo importado para utilização de json
import json
# módulo importado para utilização de datetime
from datetime import datetime
# módulo importado para utilização de requests
import requests

# para funcionar precisa iniciar a API de Diagnóstico no VSCode ou PyCharm

# URL da API do Diagnóstico (substitua pelo endereço correto, se necessário)
url_api_diagnostico = "http://127.0.0.1:5000/predict"

#marcas disponiveis de veiculos
marcas = {
        'Chevrolet': {'Corsa': [1995, 2002, 2009], 'Onix': [2012, 2017, 2021], 'Prisma': [2006, 2013, 2018]},
        'Ford':{'Ka': [1997, 2005, 2012], 'EcoSport': [2003, 2010, 2018], 'Focus': [1998, 2008, 2015]},
        'Honda': {'Civic': [1996, 2004, 2011], 'Fit': [2001, 2008, 2015], 'HR-V': [2014, 2017, 2020]},
        'Volkswagen': {'Gol': [1980, 1998, 2012], 'Polo': [1995, 2002, 2010], 'Jetta': [1984, 1999, 2007]},
        'Toyota': {'Corolla': [1990, 2002, 2010], 'Hilux': [1998, 2005, 2013], 'Etios': [2010, 2015, 2020]},
        'Hyundai': {'HB20': [2012, 2016, 2020], 'Tucson': [2004, 2010, 2016], 'Creta': [2014, 2018, 2022]},
        'Fiat': {'Uno': [1983, 1996, 2004], 'Argo': [2017, 2020, 2023], 'Toro': [2016, 2019, 2022]},
        'Nissan': {'March': [2002, 2010, 2018], 'Versa': [2006, 2013, 2020], 'Kicks': [2016, 2019, 2023]},
        'Jeep': {'Renegade': [2014, 2017, 2021], 'Compass': [2006, 2012, 2018], 'Grand Cherokee': [1992, 2005, 2014]},
        'Renault': {'Kwid': [2015, 2018, 2022], 'Sandero': [2008, 2014, 2019], 'Duster': [2010, 2015, 2020]}
    }
# perguntas diagnostico
perguntas = {
        "temperatura_alta": "Carro está com a temperatura alta? (S/N): ",
        "sons_estranhos": "Carro está fazendo sons estranhos? (S/N): ",
        "luz_painel": "Carro está com alguma luz no painel? (S/N): ",
        "alto_consumo_combustivel": "Carro está consumindo muita gasolina? (S/N): ",
        "dificuldade_partida": "Carro está com dificuldade de dar partida? (S/N): ",
        "carro_vibrando": "Carro está vibrando muito? (S/N): ",
        "problemas_freio": "Carro está com algum problema na hora de frear? (S/N): ",
        "problemas_direcao": "Carro está com algum problema na direção? (S/N): ",
        "fumaca_escapamento": "Carro está soltando muita fumaça pelo escapamento? (S/N): ",
        "cheiros_incomuns": "Carro está com algum cheiro incomum/ruim? (S/N): ",
        "bateria_fraca": "Carro está com a bateria fraca? (S/N): ",
        "ar_nao_gelando": "O ar-condicionado está emitindo ar frio na opção Cool? (S/N): ",
        "vazamento": "Carro está com vazamento de algum líquido? (S/N): ",
        "fumaca_capo": "Carro está soltando vapor/fumaça pelo capô? (S/N): ",
        "perda_potencia": "Carro está perdendo potência? (S/N): ",
        "problemas_eletricos": "Carro está com algum problema elétrico? (S/N): ",
        "motor_falhando": "Carro está com o motor falhando? (S/N): ",
        "volante_desalinhado": "Carro está com o volante desalinhado? (S/N): ",
        "nivel_oleo": "Carro está com o nível de óleo baixo no painel? (S/N): "
    }

# expressões regulares
regexCpf = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$' 
regexTel = r"^\d{2} \d{5}-\d{4}$" 
regexNome = r"^[A-Za-zÀ-ÿ'\- ]+$"
regexEmail = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
regexPlaca = r'^[A-Z]{3}-\d{1}[A-Z]{1}\d{2}$'
regexIdCentro = r"^C\d{3}$"
regexIdPeca = r"^P\d{5}$"
regexIdCargo = r"^CG\d{2}$"
regexIdServico = r"^S\d{5}$"
regexData = r"^(0[1-9]|[12][0-9]|3[01])-(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)-\d{4}$"
regexHorario = r"^([01][0-9]|2[0-3]):([0-5][0-9])$"
regexHorarioFuncionamento = r"^(?:[01]\d|2[0-3]):[0-5]\d - (?:[01]\d|2[0-3]):[0-5]\d$"
regexMatriculaFunc = r"^M\d{5}$"
regexQuilometragem = r'^\d{1,8}(\.\d{1,2})?$'
regexValor = r'^\d{1,7}(\.\d{1,2})?$'

# definindo conexão com banco de dados.
def conectar():
    return oracledb.connect (
        user="RM554424",
        password="040704",
        dsn="oracle.fiap.com.br:1521/orcl"
    )

# FUNÇÕES REUTILIZÁVEIS
# exporta os registros para json
def exportar_para_json(dados_tabela, nome_arquivo):
    with open(nome_arquivo, 'w') as json_file:
        json.dump(dados_tabela, json_file, indent=4)
    print(f"\nDados exportados para arquivo de nome: {nome_arquivo} com sucesso! ✅")

# retorna os dados da tabela --> retornar_colunas = True para a função de exportar registros para JSON
# utilização de parametros adicionais --> parametros_adicionais = params
def select_registros(select_sql, parametros_adicionais=None, retornar_colunas=False):
    with conectar() as conn:
        cursor = conn.cursor()
        if parametros_adicionais:
            cursor.execute(select_sql, parametros_adicionais)
        else:
            cursor.execute(select_sql)
        dados = cursor.fetchall()
        if retornar_colunas:
            colunas = [coluna[0] for coluna in cursor.description]
            cursor.close()
            return dados, colunas
        cursor.close()
        return dados
    
# verifica se existe algum registro em X tabela
def existem_registros(select_sql):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(select_sql)
        registro_count = cursor.fetchone()[0] > 0
        cursor.close()
        return registro_count

# transforma a data para que possa ser passada ao JSON
def serialize_data(data):
    if isinstance(data, list):
        return [serialize_data(item) for item in data]
    elif isinstance(data, dict):
        return {key: serialize_data(value) for key, value in data.items()}
    elif isinstance(data, datetime):
        return data.isoformat()  # Converte datetime para string no formato ISO
    return data 

# FUNÇÕES DO USUÁRIO
# cadastrar usuario
def cadastro_usuario():
    print("Iniciando cadastro do usuário...\n")
    usuario = {}
    # cadastro nome
    while True:
        try:
            nome = input("Digite o nome..................................: ").strip()
            if re.match(regexNome, nome) is None:
                raise ValueError("Digite um nome válido.") 
            if len(nome) > 80:
                raise ValueError("Digite um nome com até 80 caracteres.") 
            if verificar_nome_repetido(nome):
                raise ValueError("Nome já existente no banco de dados.")   
        except ValueError as e:
            print(e)  
        else:
            usuario['nome'] = nome
            print('Nome registrado com sucesso.')
            break
    # cadastro email
    while True:
        try:
            email = input("Digite o email.................................: ").strip()
            if re.match(regexEmail, email) is None:
                raise ValueError("Digite um email válido.")
            if len(email) > 255:
                raise ValueError("digite um e-mail com até 255 caracteres.")
        except ValueError as e:
            print(e)
        else:
            usuario['email'] = email
            print('Email registrado com sucesso.')
            break
    # cadastro senha
    while True:
        try:
            senha = input("Digite uma nova senha..........................: ").strip()
            if len(senha) <= 6 or len(senha) > 30:
                raise ValueError("Sua senha deve conter ao menos 6 e no máximo 30 caracteres.")
        except ValueError as e:
            print(e)
        else:
            usuario['senha'] = senha
            print("Senha registrada com sucesso.")
            break
    # cadastro CPF
    while True:
        try:
            cpf = input("Digite o CPF (ex: xxx.xxx.xxx-xx)..............: ")
            cpf_repetido = verificar_usuario(cpf)
            if cpf_repetido:
                raise ValueError("O CPF inserido já está sendo utilizado.")
        except ValueError as e:
            print(e) 
        else:
            cpf = re.sub(r"[.-]", "", cpf)
            usuario['cpf'] = cpf
            print('CPF registrado com sucesso.')
            break
    # cadastro telefone
    while True:
        try:
            telefone = input("Digite o número de telefone (ex: xx xxxxx-xxxx): ")
            if re.match(regexTel, telefone) is None:
                raise ValueError("Digite um número de telefone válido.")
        except ValueError as e:
            print(e)
        else:
            telefone_formatado = re.sub(r"[ -]", "", telefone)
            usuario['telefone'] = telefone_formatado
            print("Telefone registrado com sucesso.")
            break
    
    with conectar() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuario (cpf_usuario, nome_usuario, email, telefone, senha) 
                VALUES (:cpf, :nome, :email, :telefone, :senha)""", 
                usuario)
            conn.commit()
            print("\nUsuário cadastrado com sucesso! ✅")
        except oracledb.DatabaseError as e:
            error, = e.args 
            print("\nErro ao cadastrar o usuário no SQL!")
            print("Código do erro:", error.code)
            print("Mensagem do erro:", error.message)
            print("Contexto do erro:", error.context)
        finally:
            cursor.close()

# visualizar um usuário pelo CPF
def read_usuario(cpf):
    try:
        if not verificar_usuario(cpf):
            raise ValueError("\nUsuário não encontrado.")
        cpf = re.sub(r"[.-]", "", cpf)
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT cpf_usuario, nome_usuario, email, telefone, senha FROM usuario WHERE cpf_usuario = :cpf", {"cpf": cpf})
                usuario_atual = cursor.fetchone()
    except ValueError as e:
        print(e)
    else:
        imprimir_usuario(usuario_atual)
        input("Pressione ENTER para voltar ao menu: ")
    finally:
        print("\nRetornando ao menu do usuário...")

# visualizar todos os usuários
def read_all_usuarios():
        usuarios = select_registros("SELECT * FROM usuario")
        if usuarios:
            for usuario in usuarios:
                imprimir_usuario(usuario)
        else:
            print("\nNenhum registro encontrado de usuário.\n")
        input("Pressione ENTER para voltar ao menu: ")
        print("\nRetornando ao menu do usuário...")

# imprime os dados do usuário
def imprimir_usuario(usuario_atual):
        print(f"\n==============[ INFORMAÇÕES DO USUÁRIO {usuario_atual[1]} ]==============\n") 
        print(f"CPF.......: {usuario_atual[0]}")
        print(f"Nome......: {usuario_atual[1]}") 
        print(f"Email.....: {usuario_atual[2]}") 
        print(f"Telefone..: {usuario_atual[3]}") 
        print(f"Senha.....: {usuario_atual[4]}\n") 

# deleta um usuario a partir do CPF
def deletar_usuario(cpf):
    try:
        if not verificar_usuario(cpf):
            raise ValueError("Usuário não encontrado.")
        cpf = re.sub(r"[.-]", "", cpf)
        with conectar() as conn:
            with conn.cursor() as cursor:              
                while True:
                    op_delete = input(f"\nDeseja realmente deletar o usuário de CPF {cpf}? (os veículos, agendamentos e diagnósticos relacionados também serão removidos) S ou N: ")
                    if op_delete.upper() != "S" and op_delete.upper() != "N":
                        print("\nDigite uma opção válida.")
                        continue
                    elif op_delete.upper() == "S":
                        cursor.execute("DELETE FROM usuario WHERE cpf_usuario = :cpf", {"cpf": cpf})
                        conn.commit()
                        print("\nUsuário removido com sucesso! ✅")
                        break
                    elif op_delete.upper() == "N":
                        print("\nUsuário não foi removido.")
                        break
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de usuário...')

# atualiza um usuario
def atualizar_usuario(cpf):
    try:
        if not verificar_usuario(cpf):
            raise ValueError("Usuário não encontrado.")
        cpf = re.sub(r"[.-]", "", cpf)
        with conectar() as conn:
            with conn.cursor() as cursor:                 
                while True:
                    print("\n==============[ ATUALIZAÇÃO DOS DADOS DO USUÁRIO 🚹 ]==============\n")
                    print("1 - Atualizar Nome")
                    print("2 - Atualizar Email")
                    print("3 - Atualizar Telefone")
                    print("4 - Atualizar Senha")  
                    print("0 - Sair")
                    op_atualizar = input("\nSelecione uma opção: ")
                    if not op_atualizar.isdigit() or int(op_atualizar) > 4 or int(op_atualizar) < 0:
                        print("\nSelecione uma opção válida.")
                        continue
                    op_atualizar = int(op_atualizar)
                    if op_atualizar == 0:
                        break
                    match op_atualizar:
                        case 1:
                            while True:
                                try:
                                    nome = input("Digite o novo nome............................: ").strip()
                                    if re.match(regexNome, nome) is None:
                                        raise ValueError("Digite um nome válido.")
                                    if len(nome) > 80:
                                        raise ValueError("Digite um nome com até 80 caracteres.") 
                                    if verificar_nome_repetido(nome):
                                        raise ValueError("Nome já existente no banco de dados.")   
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE usuario SET nome_usuario = :nome WHERE cpf_usuario = :cpf", {"nome": nome, "cpf": cpf})
                                    conn.commit()
                                    print('\nNome atualizado com sucesso. ✅')
                                    break
                        case 2:
                            while True:
                                try:
                                    email = input("Digite o novo email..........................: ").strip()
                                    if re.match(regexEmail, email) is None:
                                        raise ValueError("Digite um email válido.")
                                    if len(email) > 255:
                                        raise ValueError("digite um e-mail com até 255 caracteres.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE usuario SET email = :email WHERE cpf_usuario = :cpf", {"email": email, "cpf": cpf})
                                    conn.commit()
                                    print('\nEmail atualizado com sucesso. ✅')
                                    break
                        case 3:
                            while True:
                                try:
                                    telefone = input("Digite o novo número de telefone (ex: xx xxxxx-xxxx): ")
                                    if re.match(regexTel, telefone) is None:
                                        raise ValueError("Digite um número de telefone válido.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    telefone = re.sub(r"[ -]", "", telefone)
                                    cursor.execute("UPDATE usuario SET telefone = :telefone WHERE cpf_usuario = :cpf", {"telefone": telefone, "cpf": cpf})
                                    conn.commit()
                                    print("\nTelefone atualizado com sucesso. ✅")
                                    break
                        case 4:
                            while True:
                                try:
                                    senha = input("Digite uma nova senha......................: ").strip()
                                    if len(senha) <= 6 or len(senha) > 30:
                                        raise ValueError("Sua senha deve conter ao menos 6 e no máximo 30 caracteres.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE usuario SET senha = :senha WHERE cpf_usuario = :cpf", {"senha": senha, "cpf": cpf})
                                    conn.commit()
                                    print("\nSenha atualizada com sucesso. ✅")
                                    break
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de usuário...')

# verifica a existencia do usuario e retorna o usuario
def verificar_usuario(cpf):
    # verifica formato do CPF
    if re.match(regexCpf, cpf) is None:
        raise ValueError("Digite um CPF válido.")
    cpf = re.sub(r"[.-]", "", cpf) 
    # busca o usuario pelo banco de dados
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuario WHERE cpf_usuario = :cpf", {"cpf": cpf})
        usuario_existe = cursor.fetchone()[0] > 0
        cursor.close()
        return usuario_existe

# exporta os registros de usuario em JSON
def exportar_usuarios_json():
    try:
        if existem_registros("SELECT COUNT(1) FROM usuario") == False:
            raise ValueError("\nNenhum usuário cadastrado.")
        usuarios, colunas = select_registros("SELECT * FROM usuario", None, True)
        while True:
            export_opt = input("Deseja exportar os registros de usuários para JSON? (S ou N): ").upper()
            if export_opt == 'S':
                usuarios_json = [dict(zip(colunas, usuario)) for usuario in usuarios]
                exportar_para_json(usuarios_json, 'usuarios.json')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de usuário...')

# gerenciamento usuario
def gerenciar_usuario():
        print("\nIniciando menu de gerenciamento do usuário...") 
        while True:
            print("\n==============[ GERENCIAMENTO DE USUÁRIOS 🚹​ ]==============\n")
            print("1 - Cadastrar Usuário")
            print("2 - Visualizar Usuário por CPF")
            print("3 - Visualizar todos os Usuários")
            print("4 - Atualizar Usuário")
            print("5 - Deletar Usuário")
            print("6 - Exportar Usuários para JSON")
            print("0 - Sair")
            verif_usuario_op = input("\nSelecione uma opção: ")
            if not verif_usuario_op.isdigit() or int(verif_usuario_op) > 6 or int(verif_usuario_op) < 0:
                print("\nSelecione uma opção válida.")
                continue
            verif_usuario_op = int(verif_usuario_op)
            if verif_usuario_op == 0:
                break
            elif verif_usuario_op == 1:
                cadastro_usuario()
            elif verif_usuario_op == 2:
                input_cpf = input("Digite o CPF do Usuário que deseja visualizar (xxx.xxx.xxx-xx): ")
                read_usuario(input_cpf)
            elif verif_usuario_op == 3:
                read_all_usuarios()
            elif verif_usuario_op == 4:
                input_cpf = input("Digite o CPF do Usuário que deseja atualizar (xxx.xxx.xxx-xx).: ")
                atualizar_usuario(input_cpf)
            elif verif_usuario_op == 5:
                input_cpf = input("Digite o CPF do Usuário que deseja deletar (xxx.xxx.xxx-xx)...: ")
                deletar_usuario(input_cpf)
            elif verif_usuario_op == 6:
                exportar_usuarios_json()

# verifica se o nome do usuário já existe (UNIQUE)
def verificar_nome_repetido(nome):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuario WHERE nome_usuario = :nome_usuario", {"nome_usuario": nome})
        nome_repetido = cursor.fetchone()[0] > 0
        cursor.close()
        return nome_repetido

# FUNÇÕES DO VEÍCULO
#cadastro do veiculo
def cadastro_veiculo():
    print("Iniciando cadastro de veículo...\n")
    veiculo = {}
    # cadastro marca através de um menu
    while True:
        try:
            print("==============[ MARCA ]==============\n")
            for i in range(len(marcas)):
                print(f"{i:<2} - {list(marcas)[i]}")
            marca = input("\nSelecione a marca do carro...........: ")
            if not marca.isdigit() or (int(marca) >= 10 or int(marca) < 0):
                raise ValueError("\nSelecione uma opção válida.\n")
        except ValueError as e:
            print(e)
        else:
            marca = int(marca)
            veiculo['marca'] = list(marcas.keys())[marca]
            print('Marca registrada com sucesso.')
            break
    # cadastro modelo através de um menu
    while True:
        try:
            print("\n==============[ MODELO ]==============\n")
            for i in range(len(marcas[veiculo['marca']])):
                print(f"{i} - {list(marcas[veiculo['marca']])[i]}")
            modelo = input("\nSelecione o modelo do carro..........: ")
            if not modelo.isdigit() or (int(modelo) > 2 or int(modelo) < 0):
                raise ValueError("\nSelecione uma opção válida.")
        except ValueError as e:
            print(e)
        else:
            modelo = int(modelo)
            veiculo['modelo'] = list(marcas[veiculo['marca']].keys())[modelo]
            print('Modelo registrado com sucesso.')
            break
    # cadastro do ano do veículo
    while True:
        try:
            print("\n==============[ ANO ]==============\n")
            for i in range(len(marcas[veiculo['marca']][veiculo['modelo']])):
                print(f"{i} - {list(marcas[veiculo['marca']][veiculo['modelo']])[i]}")
            ano = input("\nSelecione o ano do carro.............: ")
            if not ano.isdigit() or (int(ano) > 2 or int(ano) < 0):
                raise ValueError("\nSelecione uma opção válida.")
        except ValueError as e:
            print(e)
        else:
            ano = int(ano)
            veiculo['ano'] = marcas[veiculo['marca']][veiculo['modelo']][ano]
            print('Ano registrado com sucesso.')
            break
    # cadastro da placa do veículo
    while True:
        try:
            placaVeiculo = input("Qual a placa do carro? (ex: ABC-1D23): ")
            placa_repetida = verificar_veiculo(placaVeiculo)
            if placa_repetida:
                raise ValueError("A placa já pertence a um veículo.")
        except ValueError as e:
            print(e)
        else:
            placaVeiculo = re.sub(r"[-]", "", placaVeiculo)
            veiculo['placa'] = placaVeiculo
            print('Placa registrada com sucesso.')
            break
    # cadastro da quilometragem
    while True:
        try:
            quilometragem = float(input("Qual a quilometragem do veículo?.....: "))
            if quilometragem <= 0:
                raise ValueError("Digite um valor maior que zero.")
            quilometragem = str(quilometragem)
            if re.match(regexQuilometragem, quilometragem) is None:
                    raise ValueError("Digite uma quilometragem válida (10 dígitos no máximo, 2 casas decimais no máximo)") 
            quilometragem = float(quilometragem)
        except ValueError as e:
            if "could not convert string" in str(e):
                print("Digite um valor numérico válido.")
            else:
                print(e)
        else:
            print("Quilometragem registrada com sucesso.")
            veiculo['quilometragem'] = quilometragem
            break
    # cadastro do proprietario do veiculo
    while True:
        try: 
            cpf_usuario = input("Qual o CPF do proprietário do veículo? (ex: xxx.xxx.xxx-xx): ")
            cpf_existe = verificar_usuario(cpf_usuario)
            if cpf_existe == False:
                raise ValueError("Nenhum usuário cadastrado com o CPF informado.")
        except ValueError as e:
            print(e)
        else:
            cpf_usuario = re.sub(r"[.-]", "", cpf_usuario)
            veiculo['cpf_proprietario'] = cpf_usuario
            print("CPF do Proprietário registrado com sucesso.")
            break
    
    with conectar() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO veiculo (placa, marca, modelo, ano, quilometragem, usuario_cpf_usuario) 
                VALUES (:placa, :marca, :modelo, :ano, :quilometragem, :cpf_proprietario)""", 
                veiculo)
            conn.commit()
            print("\nVeículo cadastrado com sucesso! ✅")
        except oracledb.DatabaseError as e:
            error, = e.args 
            print("\nErro ao cadastrar o veículo no SQL!")
            print("Código do erro:", error.code)
            print("Mensagem do erro:", error.message)
            print("Contexto do erro:", error.context)
        finally:
            cursor.close()

# visualizar veiculo pela placa
def read_veiculo(placa):
    try:
        if not verificar_veiculo(placa):
            raise ValueError("Veículo não encontrado.")
        placa = re.sub(r"[-]", "", placa)
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT placa, marca, modelo, ano, quilometragem, usuario_cpf_usuario FROM veiculo WHERE placa = :placa", {'placa': placa})
                veiculo_atual = cursor.fetchone()
    except ValueError as e:
        print(e)
    else:
        imprimir_veiculo(veiculo_atual)
        input("Pressione ENTER para voltar ao menu: ")  
    finally:
        print("\nRetornando ao menu do veículo...")

# visualiza todos os veículos
def read_all_veiculos():
        veiculos = select_registros("SELECT * FROM veiculo")
        if veiculos:
            for veiculo in veiculos:
                imprimir_veiculo(veiculo)
        else:
            print("\nNenhum registro encontrado de veículo.\n")
        
        input("Pressione ENTER para voltar ao menu: ")
        print("\nRetornando ao menu de veículo...")

# imprime um usuário
def imprimir_veiculo(veiculo_atual):
    print(f"\n==============[ INFORMAÇÕES DO VEÍCULO {veiculo_atual[0]} ]==============\n") 
    print(f"Placa......................: {veiculo_atual[0]}")
    print(f"Marca......................: {veiculo_atual[1].capitalize()}") 
    print(f"Modelo.....................: {veiculo_atual[2]}") 
    print(f"Ano........................: {veiculo_atual[3]}") 
    print(f"Quilometragem..............: {veiculo_atual[4]}km")
    print(f"CPF do usuário proprietário: {veiculo_atual[5]}\n")

# atualizar veiculo
def atualizar_veiculo(placa):
    try:
        if not verificar_veiculo(placa):
            raise ValueError('Veículo não encontrado.')
        placa = re.sub(r"[-]", "", placa)      
    except ValueError as e:
        print(e)
    else:
        with conectar() as conn:
            with conn.cursor() as cursor:  
                while True:
                    print("\n==============[ ATUALIZAÇÃO DOS DADOS DO VEÍCULO ​🚗 ]==============\n")
                    print("1 - Atualizar Marca, Modelo e Ano")
                    print("2 - Atualizar Quilometragem")
                    print("3 - Atualizar CPF do Proprietário")
                    print("0 - Sair")
                    op_atualizar = input("\nSelecione uma opção: ")
                    if not op_atualizar.isdigit() or int(op_atualizar) > 3 or int(op_atualizar) < 0:
                        print("\nSelecione uma opção válida.")
                        continue
                    op_atualizar = int(op_atualizar)
                    if op_atualizar == 0:
                        break
                    match op_atualizar:
                        case 1:
                            # atualizar marca, modelo e ano
                            while True:
                                try:
                                    print("==============[ MARCA ]==============\n")
                                    for i in range(len(marcas)):
                                        print(f"{i:<2} - {list(marcas)[i]}")
                                    marca = input("\nSelecione a nova marca do carro...........: ")
                                    if not marca.isdigit() or (int(marca) >= 10 or int(marca) < 0):
                                        raise ValueError("\nSelecione uma opção válida.\n")
                                except ValueError as e:
                                    print(e)
                                else:
                                    marca_index = int(marca)
                                    marca_str = list(marcas.keys())[marca_index]
                                    cursor.execute("UPDATE veiculo SET marca = :marca_str WHERE placa = :placa", {"marca_str": marca_str, "placa": placa})
                                    conn.commit()
                                    print('Marca atualizada com sucesso.')
                                    break
                            # cadastro modelo através de um menu
                            while True:
                                try:
                                    print("\n==============[ MODELO ]==============\n")
                                    for i in range(len(marcas[marca_str])):
                                        print(f"{i} - {list(marcas[marca_str])[i]}")
                                    modelo = input("\nSelecione o novo modelo do carro..........: ")
                                    if not modelo.isdigit() or (int(modelo) > 2 or int(modelo) < 0):
                                        raise ValueError("\nSelecione uma opção válida.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    modelo_index = int(modelo)
                                    modelo_str = list(marcas[marca_str].keys())[modelo_index]
                                    cursor.execute("UPDATE veiculo SET modelo = :modelo_str WHERE placa = :placa", {"modelo_str": modelo_str, "placa": placa})
                                    conn.commit()
                                    print('Modelo atualizado com sucesso.')
                                    break  
                            while True:
                                try:
                                    print("\n==============[ ANO ]==============\n")
                                    for i in range(len(marcas[marca_str][modelo_str])):
                                        print(f"{i} - {list(marcas[marca_str][modelo_str])[i]}")
                                    ano = input("\nSelecione o novo ano do carro.............: ")
                                    if not ano.isdigit() or (int(ano) > 2 or int(ano) < 0):
                                        raise ValueError("\nSelecione uma opção válida.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    ano_index = int(ano)
                                    ano_reg = marcas[marca_str][modelo_str][ano_index]
                                    cursor.execute("UPDATE veiculo SET ano = :ano_reg WHERE placa = :placa", {"ano_reg": ano_reg, "placa": placa})
                                    conn.commit()
                                    print("Ano atualizado com sucesso.")
                                    break
                            print('\nMarca, Modelo e Ano atualizados com sucesso! ✅')      
                        case 2:
                            # atualizar quilometragem
                            while True:
                                try:
                                    quilometragem = float(input("Qual a nova quilometragem do veículo?: "))
                                    if quilometragem <= 0:
                                        raise ValueError("Digite um valor maior que zero.")
                                    quilometragem = str(quilometragem)
                                    if re.match(regexQuilometragem, quilometragem) is None:
                                            raise ValueError("Digite uma quilometragem válida (10 dígitos no máximo, 2 casas decimais no máximo)") 
                                    quilometragem = float(quilometragem)
                                except ValueError as e:
                                    if "could not convert string" in str(e):
                                        print("Digite um valor numérico válido.")
                                    else:
                                        print(e)
                                else: 
                                    cursor.execute("UPDATE veiculo SET quilometragem = :quilometragem WHERE placa = :placa", {"quilometragem": quilometragem, "placa": placa})
                                    conn.commit()
                                    print('\nQuilometragem atualizada com sucesso! ✅')
                                    break
                        case 3:
                            # atualizar cpf do proprietario
                            while True:
                                try: 
                                    cpf_usuario = input("Qual o novo CPF do proprietário do veículo? (ex: xxx.xxx.xxx-xx): ")
                                    cpf_existe = verificar_usuario(cpf_usuario)
                                    if cpf_existe == False:
                                        raise ValueError("Nenhum usuário cadastrado com o CPF informado.")
                                except ValueError as e:
                                    print(e)
                                    break
                                else:
                                    cpf_usuario = re.sub(r"[.-]", "", cpf_usuario)
                                    cursor.execute("UPDATE veiculo SET usuario_cpf_usuario = :cpf_usuario WHERE placa = :placa", {"cpf_usuario": cpf_usuario, "placa": placa})
                                    conn.commit()
                                    print("\nCPF do proprietário atualizado com sucesso! ✅")  
                                    break
    finally:
        print("\nRetornando ao menu de veículo...")

#remover veiculo
def deletar_veiculo(placa):
    try:
        if not verificar_veiculo(placa):
            raise ValueError("Veículo não encontrado.")
        placa = re.sub(r"[-]", "", placa)
        with conectar() as conn:
            with conn.cursor() as cursor:
                while True:
                    op_delete = input(f"\nDeseja realmente deletar o veículo de placa {placa}? (os agendamentos e diagnósticos relacionados também serão removidos) S ou N: ")
                    if op_delete.upper() != "S" and op_delete.upper() != "N":
                        print("\nDigite uma opção válida.")
                        continue
                    elif op_delete.upper() == "S":
                        cursor.execute("DELETE FROM veiculo WHERE placa = :placa", {"placa": placa})
                        conn.commit()
                        print("\nVeículo removido com sucesso. ✅")
                        break
                    elif op_delete.upper() == "N":
                        print("\nVeículo não foi removido.")
                        break

    except ValueError as e:
        print(e)   
    finally:
        print('\nRetornando ao menu de veículo...')
       
# verifica a existencia da placa e retorna se existe ou n
def verificar_veiculo(placa):
    # verifica formato da placa
    if re.match(regexPlaca, placa) is None:
        raise ValueError("Digite uma placa válida.")
    placa = re.sub(r"[-]", "", placa) 
    # busca a placa pelo banco de dados
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM veiculo WHERE placa = :placa", {"placa": placa})
        placa_existe = cursor.fetchone()[0] > 0
        cursor.close()
        return placa_existe

# exporta os registros de agendamento em JSON
def exportar_veiculos_json():
    try:
        if existem_registros("SELECT COUNT(1) FROM veiculo") == False:
            raise ValueError("\nNenhum veículo cadastrado.")
        veiculos, colunas = select_registros("SELECT * FROM veiculo", None, True)
        while True:
            export_opt = input("Deseja exportar os registros de veículos para JSON? (S ou N): ").upper()
            if export_opt == 'S':
                veiculos_json = [dict(zip(colunas, veiculo)) for veiculo in veiculos]
                exportar_para_json(veiculos_json, 'veiculos.json')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de veículo...')

# gerenciamento veiculo
def gerenciar_veiculo():
    print("\nIniciando menu de gerenciamento do veículo...")
    while True:
        print("\n==============[ GERENCIAMENTO DE VEÍCULOS 🚗 ]==============\n")
        print("1 - Cadastrar Veículo")
        print("2 - Visualizar Veículo")
        print("3 - Visualizar todos os Veículos")
        print("4 - Atualizar Veículo")
        print("5 - Deletar Veículo")
        print("6 - Exportar Veículos para JSON")
        print("0 - Sair")
        verif_veic_op = input("\nSelecione uma opção: ")
        if not verif_veic_op.isdigit() or int(verif_veic_op) > 6 or int(verif_veic_op) < 0:
            print("\nSelecione uma opção válida.")
            continue
        verif_veic_op = int(verif_veic_op)
        if verif_veic_op == 0:
            break
        elif verif_veic_op == 1:
            if existem_registros("SELECT COUNT(1) FROM usuario") == False:
                print("\nNenhum usuário cadastrado no sistema. Impossível cadastrar novo veículo.")
            else:
                cadastro_veiculo()
        elif verif_veic_op == 2:
            placa_input = input("Qual a placa do veículo que deseja visualizar? (ex: ABC-1D23): ")
            read_veiculo(placa_input)
        elif verif_veic_op == 3:
            read_all_veiculos()
        elif verif_veic_op == 4:
            placa_input = input("Qual a placa do veículo que deseja atualizar? (ex: ABC-1D23): ")
            atualizar_veiculo(placa_input)
        elif verif_veic_op == 5:
            placa_input = input("Qual a placa do veículo que deseja remover? (ex: ABC-1D23): ")
            deletar_veiculo(placa_input)
        elif verif_veic_op == 6:
            exportar_veiculos_json()

# FUNÇÕES DO AGENDAMENTO
# agenda um serviço 
def agendar_servico(placa):
    agendamento = {}
    try:
        if not verificar_veiculo(placa):
            raise ValueError('Veículo não encontrado.')
        placa = re.sub(r"[-]", "", placa)
        servicos, centros = verificar_centros_servicos()
    except ValueError as e:
            print(e)
    else:
        print("\nIniciando agendamento do serviço...")
        # ID do agendamento criado com uuid
        agendamento['id_agendamento'] = str(uuid.uuid4())
        # adicionando servico   
        while True:
            try:
                if servicos:
                    print("\n==============[ SERVIÇOS ]==============\n")
                    for i in range(len(list(servicos))):
                        print(f"{i} - {servicos[i][1]}")
                    op_servico = input("\nQual serviço será realizado?: ")
                    if not op_servico.isdigit() or int(op_servico) > (len(list(servicos)) - 1) or int(op_servico) < 0:
                        raise ValueError("\nSelecione uma opção válida.")
            except ValueError as e:
                print(e)
            else: 
                op_servico = int(op_servico)
                agendamento['servico_id_servico'] = servicos[op_servico][0]
                print('Serviço registrado com sucesso.')
                break
        # adicionando centro automotivo
        while True:
            try:
                print("\n==============[ CENTROS AUTOMOTIVOS ]==============\n")
                for i in range(len(list(centros))):
                    print(f"{i} - {list(centros)[i][1]}")
                op_centro = input("\nEm qual centro automotivo o serviço será realizado?......: ")
                if not op_centro.isdigit() or int(op_centro) > (len(list(centros)) - 1) or int(op_centro) < 0:
                    raise ValueError("\nSelecione uma opção válida.")
            except ValueError as e:
                print(e)
            else: 
                op_centro = int(op_centro)
                agendamento['centro_automotivo_id_centro'] = centros[op_centro][0]
                print('Centro Automotivo registrado com sucesso.')
                break
        # adicionando data
        while True:
            try:
                data = input("Qual a Data do agendamento (Ex: DD-MON-YYYY. OBS.: Mês no formato americano)....: ")
                if re.match(regexData, data) is None:
                    raise ValueError("Digite uma data válida.")
                # verifica se a data inserida é igual a atual ou posterior
                data_agendamento = datetime.strptime(data, "%d-%b-%Y")
                data_hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                if data_agendamento < data_hoje:
                    raise ValueError("Data inválida. A data inserida é de um dia anterior ao atual.")
            except ValueError as e:
                print(e) 
            else:
                agendamento['data_agendamento'] = data
                print("Data registrada com sucesso.")
                break
        # adicionando horario
        while True:
            try:
                horario = input("Qual o horário que o serviço será realizado?: (ex: 17:30): ")
                if re.match(regexHorario, horario) is None:
                    raise ValueError("Digite um horário válido.")
            except ValueError as e:
                print(e)  
            else:
                agendamento['horario_agendamento'] = horario
                print('Horário registrado com sucesso.')
                break 
        # adicionando descrição
        while True:
            try:
                descricao_agendamento = input("Digite a descrição do agendamento............................: ").strip()
                if not descricao_agendamento:
                    raise ValueError("Descrição vazia.")
                if len(descricao_agendamento) > 255:
                    raise ValueError("A descrição deve ter no máximo 255 caracteres.")
            except ValueError as e:
                print(e)
            else:
                agendamento['descricao_agendamento'] = descricao_agendamento
                print("Descrição registrada com sucesso.")
                break
        # adicionando placa
        agendamento['veiculo_placa'] = placa
        with conectar() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO agendamento (id_agendamento, data_agendamento, horario_agendamento, descricao_agendamento, servico_id_servico, centro_automotivo_id_centro, veiculo_placa) 
                    VALUES (:id_agendamento, :data_agendamento, :horario_agendamento, :descricao_agendamento, :servico_id_servico, :centro_automotivo_id_centro, :veiculo_placa)""", 
                    agendamento)
                conn.commit()
                print(f"\nAgendamento criado com sucesso! ✅ O ID do agendamento é {agendamento['id_agendamento']}")
            except oracledb.DatabaseError as e:
                error, = e.args 
                print("\nErro ao cadastrar o agendamento no SQL!")
                print("Código do erro:", error.code)
                print("Mensagem do erro:", error.message)
                print("Contexto do erro:", error.context)
            finally:
                cursor.close()
    finally:
        print('\nRetornando ao menu de agendamento...')

# visualizar informações de um agendamento pelo id
def read_agendamento(id_agendamento):
    try:
        if not verificar_agendamento(id_agendamento):
            raise ValueError("Agendamento não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_agendamento, data_agendamento, horario_agendamento, descricao_agendamento, servico_id_servico, centro_automotivo_id_centro, veiculo_placa FROM agendamento WHERE id_agendamento = :id_agendamento", {'id_agendamento': id_agendamento})
                agendamento_atual = cursor.fetchone()
    except ValueError as e:
        print(e)
    else:
        imprimir_agendamento(agendamento_atual)
        input("Pressione ENTER para voltar ao menu: ")  
    finally:
        print("\nRetornando ao menu do veículo...")

# imprime todos os agendamentos
def read_all_agendamentos():
    agendamentos = select_registros("SELECT * FROM agendamento")
    if agendamentos:
        for agendamento in agendamentos:
            imprimir_agendamento(agendamento)
    else:
        print("\nNenhum registro encontrado de agendamento.\n")
    input("Pressione ENTER para voltar ao menu: ")
    print("\nRetornando ao menu do agendamento...") 

# imprime as informações do agendamento
def imprimir_agendamento(agendamento_atual):
        print(f"\n==============[ INFORMAÇÕES DO AGENDAMENTO DE ID {agendamento_atual[0]} ]==============\n") 
        print(f"ID do Agendamento............: {agendamento_atual[0]}")
        print(f"ID do Serviço................: {agendamento_atual[4]}")
        print(f"Serviço......................: {verificar_servico_obter(agendamento_atual[4])[1]}") 
        print(f"Preço........................: R${verificar_servico_obter(agendamento_atual[4])[3]}")
        print(f"ID do Centro Automotivo......: {agendamento_atual[5]}")
        print(f"Centro Automotivo............: {verificar_centro_obter(agendamento_atual[5])[1]}") 
        print(f"Data do Agendamento..........: {agendamento_atual[1]}") 
        print(f"Horário......................: {agendamento_atual[2]}")
        print(f"Descrição do Agendamento.....: {agendamento_atual[3]}")
        print(f"Placa do Veículo.............: {agendamento_atual[6]}\n")

# atualizar o agendamento
def atualizar_agendamento(id_agendamento):
    try:
        if not verificar_agendamento(id_agendamento):
            raise ValueError('Agendamento não encontrado.')
        servicos, centros = verificar_centros_servicos()
    except ValueError as e:
        print(e)
    else:
         with conectar() as conn:
            with conn.cursor() as cursor: 
                while True:
                    print("\n==============[ ATUALIZAÇÃO DOS DADOS DO AGENDAMENTO 🕒 ]==============\n")
                    print("1 - Atualizar Serviço")
                    print("2 - Atualizar Centro Automotivo")
                    print("3 - Atualizar Data do Agendamento")
                    print("4 - Atualizar Horário do Agendamento")
                    print("5 - Atualizar Descrição do Agendamento")
                    print("6 - Atualizar Veículo")
                    print("0 - Sair")
                    op_atualizar = input("\nSelecione uma opção: ")
                    if not op_atualizar.isdigit() or int(op_atualizar) > 6 or int(op_atualizar) < 0:
                        print("\nSelecione uma opção válida.")
                        continue
                    op_atualizar = int(op_atualizar)
                    if op_atualizar == 0:
                        break
                    match op_atualizar:
                        case 1:
                            while True:
                                try:
                                    if servicos:
                                        print("\n==============[ SERVIÇOS ]==============\n")
                                        for i in range(len(list(servicos))):
                                            print(f"{i} - {servicos[i][1]}")
                                        op_servico = input("\nQual novo serviço será realizado?: ")
                                        if not op_servico.isdigit() or int(op_servico) > (len(list(servicos)) - 1) or int(op_servico) < 0:
                                            raise ValueError("\nSelecione uma opção válida.")
                                except ValueError as e:
                                    print(e)
                                else: 
                                    id_servico = servicos[int(op_servico)][0]
                                    cursor.execute("UPDATE agendamento SET servico_id_servico = :id_servico WHERE id_agendamento = :id_agendamento", {"id_servico": id_servico, "id_agendamento": id_agendamento})
                                    conn.commit()
                                    print('\nServiço atualizado com sucesso! ✅')
                                    break
                        case 2:
                            while True:
                                try:
                                    print("\n==============[ CENTROS AUTOMOTIVOS ]==============\n")
                                    for i in range(len(list(centros))):
                                        print(f"{i} - {list(centros)[i][1]}")
                                    op_centro = input("\nEm qual novo centro automotivo o serviço será realizado?......: ")
                                    if not op_centro.isdigit() or int(op_centro) > (len(list(centros)) - 1) or int(op_centro) < 0:
                                        raise ValueError("\nSelecione uma opção válida.")
                                except ValueError as e:
                                    print(e)
                                else: 
                                    id_centro = centros[int(op_centro)][0]
                                    cursor.execute("UPDATE agendamento SET centro_automotivo_id_centro = :id_centro WHERE id_agendamento = :id_agendamento", {"id_centro": id_centro, "id_agendamento": id_agendamento})
                                    conn.commit()
                                    print("\nCentro Automotivo atualizado com sucesso! ✅")
                                    break
                        case 3:
                            while True:
                                try:
                                    data = input("Qual a nova data do agendamento (Ex: DD-MON-YYYY. OBS.: Mês no formato americano)....: ")
                                    if re.match(regexData, data) is None:
                                        raise ValueError("Digite uma data válida.")
                                    data_agendamento = datetime.strptime(data, "%d-%b-%Y")
                                    data_hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                                    if data_agendamento < data_hoje:
                                        raise ValueError("Data inválida. A data inserida é de um dia anterior ao atual.")
                                except ValueError as e:
                                    print(e) 
                                else:
                                    cursor.execute("UPDATE agendamento SET data_agendamento = :data WHERE id_agendamento = :id_agendamento", {"data": data, "id_agendamento": id_agendamento})
                                    conn.commit()
                                    print("\nData atualizada com sucesso! ✅")
                                    break 
                        case 4:
                            while True:
                                try:
                                    horario = input("Qual o novo horário que o serviço será realizado?: (ex: 13:30): ")
                                    if re.match(regexHorario, horario) is None:
                                        raise ValueError("Digite um horário válido.")
                                except ValueError as e:
                                    print(e)  
                                else:
                                    cursor.execute("UPDATE agendamento SET horario_agendamento = :horario WHERE id_agendamento = :id_agendamento", {"horario": horario, "id_agendamento": id_agendamento})
                                    conn.commit()
                                    print('\nHorário atualizado com sucesso! ✅')
                                    break 
                        case 5:
                             while True:
                                try:
                                    descricao_agendamento = input("Digite a nova descrição do agendamento............................: ").strip()
                                    if not descricao_agendamento:
                                        raise ValueError("Descrição vazia.")
                                    if len(descricao_agendamento) > 255:
                                        raise ValueError("A descrição deve ter no máximo 255 caracteres.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE agendamento SET descricao_agendamento = :descricao_agendamento WHERE id_agendamento = :id_agendamento", {"descricao_agendamento": descricao_agendamento, "id_agendamento": id_agendamento})
                                    conn.commit()
                                    print("\nDescrição atualizada com sucesso! ✅")
                                    break
                        case 6:
                            while True:
                                try:
                                    placaVeiculo = input("Qual a placa do novo veículo? (ex: ABC-1D23): ")
                                    if not verificar_veiculo(placaVeiculo):
                                        raise ValueError('Veículo não encontrado.')
                                    placa = re.sub(r"[-]", "", placaVeiculo)
                                except ValueError as e:
                                    print(e)
                                    break
                                else:
                                    cursor.execute("UPDATE agendamento SET veiculo_placa = :veiculo_placa WHERE id_agendamento = :id_agendamento", {"veiculo_placa": placa, "id_agendamento": id_agendamento})
                                    conn.commit()
                                    print('\nVeículo atualizado com sucesso! ✅')
                                    break
    finally:
        print("\nRetornando ao menu de agendamento...")

# deletar o agendamento feito
def deletar_agendamento(id_agendamento):
    try:
        if not verificar_agendamento(id_agendamento):
            raise ValueError("Agendamento não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                while True:
                    op_delete = input(f"\nDeseja realmente deletar o Agendamento de ID {id_agendamento}? S ou N: ")
                    if op_delete.upper() != "S" and op_delete.upper() != "N":
                        print("\nDigite uma opção válida.")
                        continue
                    elif op_delete.upper() == "S":
                        cursor.execute("DELETE FROM agendamento WHERE id_agendamento = :id_agendamento", {"id_agendamento": id_agendamento})
                        conn.commit()
                        print("\nAgendamento removido com sucesso. ✅​")
                        break
                    elif op_delete.upper() == "N":
                        print("\nAgendamento não foi removido.")
                        break
    except ValueError as e:
        print(e)   
    finally:
        print('\nRetornando ao menu de agendamento...')
        
# verifica a existencia do agendamento, retornando o agendamento
def verificar_agendamento(id_agendamento):
    # busca o ID no banco de dados
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM agendamento WHERE id_agendamento = :id_agendamento", {"id_agendamento": id_agendamento})
        placa_existe = cursor.fetchone()[0] > 0
        cursor.close()
        return placa_existe

# exporta os registros de agendamento em JSON
def exportar_agendamentos_json():
    try:
        if existem_registros("SELECT COUNT(1) FROM agendamento") == False:
            raise ValueError("\nNenhum agendamento cadastrado.")
        agendamentos, colunas = select_registros("SELECT * FROM agendamento", None, True)
        while True:
            export_opt = input("Deseja exportar os registros de agendamentos para JSON? (S ou N): ").upper()
            if export_opt == 'S':
                agendamentos_json = [dict(zip(colunas, agendamento)) for agendamento in agendamentos]
                dados_serializados = serialize_data(agendamentos_json)
                exportar_para_json(dados_serializados, 'agendamentos.json')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de veículo...')

# gerenciar o serviço agendado
def gerenciar_agendamento():
    print("\nIniciando menu de gerenciamento do serviço...") 
    while True:
        print("\n==============[ GERENCIAMENTO AGENDAMENTO DE SERVIÇO 🕒 ]==============\n")
        print("1 - Realizar Agendamento de Serviço")
        print("2 - Visualizar informações do Agendamento")
        print("3 - Visualizar todos os Agendamentos")
        print("4 - Atualizar Agendamento")
        print("5 - Deletar Agendamento")
        print("6 - Exportar Agendamentos para JSON")
        print("0 - Sair")
        verif_gerenc_op = input("\nSelecione uma opção: ")
        if not verif_gerenc_op.isdigit() or int(verif_gerenc_op) > 6 or int(verif_gerenc_op) < 0:
            print("\nSelecione uma opção válida.")
            continue
        verif_gerenc_op = int(verif_gerenc_op)
        if verif_gerenc_op == 0:
            break
        elif verif_gerenc_op == 1:
            placa_agendamento = input("Qual a placa do veículo para o agendamento?: ")
            agendar_servico(placa_agendamento)
        elif verif_gerenc_op == 2:
            id_agendamento = input("Qual o ID do agendamento que deseja visualizar?: ")
            read_agendamento(id_agendamento)
        elif verif_gerenc_op == 3:
            read_all_agendamentos()
        elif verif_gerenc_op == 4:
            id_agendamento = input("Qual o ID do agendamento que deseja atualizar?: ")
            atualizar_agendamento(id_agendamento)
        elif verif_gerenc_op == 5:
            id_agendamento = input("Qual o ID do agendamento que deseja deletar?: ")
            deletar_agendamento(id_agendamento)
        elif verif_gerenc_op == 6:
            exportar_agendamentos_json()

# verifica se ao menos 1 centro e 1 serviço existem para que o agendamento possa acontecer.
def verificar_centros_servicos():
    servicos = select_registros('SELECT * FROM servico order by 1')
    centros = select_registros('SELECT * FROM centro_automotivo')
    if servicos and centros:
        return servicos, centros
    else: 
        raise ValueError('É necessário ao menos 1 serviço e 1 centro automotivo para realizar um agendamento.')

# FUNÇÕES DO CENTRO AUTOMOTIVO
# gerenciador de centro
def gerenciar_centro():
    print("\nIniciando menu de gerenciamento de Centro Automotivo...") 
    while True:
        print("\n==============[ GERENCIAMENTO CENTRO AUTOMOTIVO ​🏪 ]==============\n")
        print("1 - Criar Centro Automotivo")
        print("2 - Visualizar informações do Centro Automotivo pelo ID")
        print("3 - Visualizar todos os Centros Automotivos")
        print("4 - Atualizar Centro Automotivo")
        print("5 - Deletar Centro Automotivo")
        print("6 - Exportar Centros Automotivos para JSON")
        print("0 - Sair")
        verif_gerenc_op = input("\nSelecione uma opção: ")
        if not verif_gerenc_op.isdigit() or int(verif_gerenc_op) > 6 or int(verif_gerenc_op) < 0:
            print("\nSelecione uma opção válida.")
            continue
        verif_gerenc_op = int(verif_gerenc_op)
        if verif_gerenc_op == 0:
            break
        elif verif_gerenc_op == 1:
            cadastrar_centro()
        elif verif_gerenc_op == 2:
            id_centro = input("Qual o ID do centro automotivo que deseja visualizar? (formato: CXXX): ")
            read_centro(id_centro)
        elif verif_gerenc_op == 3:
            read_all_centros()
        elif verif_gerenc_op == 4:
            id_centro = input("Qual o ID do centro automotivo que deseja atualizar? (formato: CXXX): ")
            atualizar_centro(id_centro)
        elif verif_gerenc_op == 5:
            id_centro = input("Qual o ID do centro automotivo que deseja deletar? (formato: CXXX): ")
            deletar_centro(id_centro)
        elif verif_gerenc_op == 6:
            exportar_centros_json()
        
# cadastra um centro automotivo
def cadastrar_centro():
    print("\nIniciando cadastro de centro automotivo...\n")
    centro = {}
    # cadastro id do centro
    while True:
        try:
            id_centro = input("Digite um ID para o Centro Automotivo (formato: CXXX. Ex: C124): ")
            id_repetido = verificar_centro(id_centro)
            if id_repetido:
                raise ValueError("O ID digitado já existe.")
        except ValueError as e:
            print(e)
        else: 
            centro['id_centro'] = id_centro
            print('ID registrado com sucesso.')
            break
    # cadastro nome centro
    while True:
        try:
            nome_centro = input("Digite o nome do centro automotivo.................................: ").strip()
            if re.match(regexNome, nome_centro) is None:
                raise ValueError("Digite um nome válido.")
            if len(nome_centro) > 155:
                raise ValueError("O nome do centro deve ter no máximo 155 caracteres.")
        except ValueError as e:
            print(e)  
        else:
            centro['nome_centro'] = nome_centro
            print('Nome do centro registrado com sucesso.')
            break
    # cadastro endereço centro
    while True:
        try:
            endereco_centro = input("Digite o endereço do centro automotivo.............................: ").strip()
            if len(endereco_centro) <= 20 or len(endereco_centro) > 255:
                raise ValueError("Insira um endereço com mais de 20 e com no máximo 255 caracteres.")
        except ValueError as e:
            print(e)
        else:
            centro['endereco_centro'] = endereco_centro
            print('Endereço registrado com sucesso.')
            break
    # cadastro telefone centro
    while True:
        try:
            telefone_centro = input("Digite o telefone do centro automotivo (ex: 11 93293-3923)........: ")
            if re.match(regexTel, telefone_centro) is None:
                raise ValueError("Insira um telefone válido.")
        except ValueError as e:
            print(e)
        else:
            telefone_centro = re.sub(r"[ -]", "", telefone_centro)
            centro['telefone_centro'] = telefone_centro
            print("Telefone registrado com sucesso.")
            break
    # cadastro horario funcionamento
    while True:
        try:
            horario_funcionamento = input("Digite o horário de funcionamento (ex: 08:00 - 17:30)..............: ")
            if re.match(regexHorarioFuncionamento, horario_funcionamento) is None:
                raise ValueError("Digite um horário válido.")
        except ValueError as e:
            print(e) 
        else: 
            centro['horario_funcionamento'] = horario_funcionamento
            print('Horário de funcionamento registrado com sucesso.')
            break
    
    with conectar() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO centro_automotivo (id_centro, nome_centro, endereco_centro, telefone_centro, horario_funcionamento) 
                VALUES (:id_centro, :nome_centro, :endereco_centro, :telefone_centro, :horario_funcionamento)""", 
                centro)
            conn.commit()
            print(f"\nCentro Automotivo de ID: {id_centro} cadastrado com sucesso! ✅​") 
        except oracledb.DatabaseError as e:
            error, = e.args 
            print("\nErro ao cadastrar o Centro Automotivo no SQL!")
            print("Código do erro:", error.code)
            print("Mensagem do erro:", error.message)
            print("Contexto do erro:", error.context)
        finally:
            cursor.close()
    
# leitura de um centro automotivo com base no ID
def read_centro(id_centro):
    try:
        if not verificar_centro(id_centro):
            raise ValueError("\nCentro automotivo não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_centro, nome_centro, endereco_centro, telefone_centro, horario_funcionamento FROM centro_automotivo WHERE id_centro = :id_centro", {"id_centro": id_centro})
                centro_atual = cursor.fetchone()
    except ValueError as e:
        print(e)
    else:
        imprimir_centro(centro_atual)
        input("Pressione ENTER para voltar ao menu: ")
    finally:
        print("\nRetornando ao menu de centro...")

# leitura de todos os centros
def read_all_centros():
    centros = select_registros("SELECT * FROM centro_automotivo order by 1")
    if centros:
        for centro in centros:
            imprimir_centro(centro)
    else:
        print("\nNenhum registro encontrado de centro automotivo.\n")
    input("Pressione ENTER para voltar ao menu: ")
    print("\nRetornando ao menu de centro...") 

# imprime as informações de um centro
def imprimir_centro(centro_atual):
    print(f"\n==============[ INFORMAÇÕES DO CENTRO AUTOMOTIVO DE ID {centro_atual[0].upper()} ]==============\n") 
    print(f"ID do Centro............: {centro_atual[0]}")
    print(f"Nome do Centro..........: {centro_atual[1]}")
    print(f"Endereço do Centro......: {centro_atual[2]}")
    print(f"Telefone do Centro......: {centro_atual[3]}")
    print(f"Horário de Funcionamento: {centro_atual[4]}\n")

# atualiza os dados de um centro automotivo
def atualizar_centro(id_centro):
    try:
        if not verificar_centro(id_centro):
            raise ValueError("Centro Automotivo não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                 while True:
                    print("\n==============[ ATUALIZAÇÃO DOS DADOS DO CENTRO AUTOMOTIVO 🏪 ]==============\n")
                    print("1 - Atualizar Nome do Centro")
                    print("2 - Atualizar Endereço do Centro")
                    print("3 - Atualizar Telefone do Centro")
                    print("4 - Atualizar Horário de funcionamento do Centro")
                    print("0 - Sair")
                    op_atualizar = input("\nSelecione uma opção: ")
                    if not op_atualizar.isdigit() or int(op_atualizar) > 4 or int(op_atualizar) < 0:
                        print("\nSelecione uma opção válida.")
                        continue
                    op_atualizar = int(op_atualizar)
                    if op_atualizar == 0:
                        print('Retornando ao menu de centro....')
                        break
                    match op_atualizar: 
                        case 1:
                            while True:
                                try:
                                    nome_centro = input("Digite o novo nome do centro automotivo.................................: ").strip()
                                    if re.match(regexNome, nome_centro) is None:
                                        raise ValueError("Digite um nome válido.")
                                    if len(nome_centro) > 155:
                                        raise ValueError("O nome do centro deve ter no máximo 155 caracteres.")
                                except ValueError as e:
                                    print(e)  
                                else:
                                    cursor.execute("UPDATE centro_automotivo SET nome_centro = :nome_centro WHERE id_centro = :id_centro", {"nome_centro": nome_centro, "id_centro": id_centro})
                                    conn.commit()
                                    print('\nNome do Centro atualizado com sucesso! ✅​')
                                    break
                        case 2:
                            while True:
                                try:
                                    endereco_centro = input("Digite o novo endereço do centro automotivo.............................: ").strip()
                                    if len(endereco_centro) <= 20 or len(endereco_centro) > 255:
                                        raise ValueError("Insira um endereço com mais de 20 e com no máximo 255 caracteres.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE centro_automotivo SET endereco_centro = :endereco_centro WHERE id_centro = :id_centro", {"endereco_centro": endereco_centro, "id_centro": id_centro})
                                    conn.commit()
                                    print('\nEndereço atualizado com sucesso! ✅​')
                                    break
                        case 3:
                            while True:
                                try:
                                    telefone_centro = input("Digite o novo telefone do centro automotivo (ex: 11 93293-3923)........: ")
                                    if re.match(regexTel, telefone_centro) is None:
                                        raise ValueError("Insira um telefone válido.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    telefone_centro = re.sub(r"[ -]", "", telefone_centro)
                                    cursor.execute("UPDATE centro_automotivo SET telefone_centro = :telefone_centro WHERE id_centro = :id_centro", {"telefone_centro": telefone_centro, "id_centro": id_centro})
                                    conn.commit()
                                    print("\nTelefone do Centro atualizado com sucesso! ✅​")
                                    break
                        case 4:
                            while True:
                                try:
                                    horario_funcionamento = input("Digite o novo horário de funcionamento (ex: 08:00 - 17:30)..............: ")
                                    if re.match(regexHorarioFuncionamento, horario_funcionamento) is None:
                                        raise ValueError("Digite um horário válido.")
                                except ValueError as e:
                                    print(e) 
                                else:
                                    cursor.execute("UPDATE centro_automotivo SET horario_funcionamento = :horario_funcionamento WHERE id_centro = :id_centro", {"horario_funcionamento": horario_funcionamento, "id_centro": id_centro})
                                    conn.commit()
                                    print('\nHorário de funcionamento atualizado com sucesso! ✅​')
                                    break
    except ValueError as e:
        print(e) 

# deletar um centro automotivo
def deletar_centro(id_centro):
    try:
        if not verificar_centro(id_centro):
            raise ValueError("\nCentro Automotivo não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                while True:
                    op_delete = input(f"\nDeseja realmente remover o centro automotivo de ID {id_centro}? S ou N: ")
                    if op_delete.upper() != "S" and op_delete.upper() != "N":
                        print("\nDigite uma opção válida.")
                        continue
                    elif op_delete.upper() == "S":
                        cursor.execute("DELETE FROM centro_automotivo WHERE id_centro = :id_centro", {"id_centro": id_centro})
                        conn.commit()
                        print("\nCentro removido com sucesso. ✅​")
                        break
                    elif op_delete.upper() == "N":
                        print("\nO Centro não foi removido.")
                        break
    except ValueError as e:
        print(e)
    finally:
        print("\nRetornando ao menu de centro automotivo...")

# exporta os registros de centro em JSON
def exportar_centros_json():
    try:
        if existem_registros("SELECT COUNT(1) FROM centro_automotivo") == False:
            raise ValueError("\nNenhum centro automotivo cadastrado.")
        centros, colunas = select_registros("SELECT * FROM centro_automotivo", None, True)
        while True:
            export_opt = input("Deseja exportar os registros de centros automotivos para JSON? (S ou N): ").upper()
            if export_opt == 'S':
                centros_json = [dict(zip(colunas, centro)) for centro in centros]
                exportar_para_json(centros_json, 'centros.json')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de centro automotivo...')

# verifica a existencia de um centro automotivo e o formato do ID
def verificar_centro(id_centro):
     # verifica formato do ID
    if re.match(regexIdCentro, id_centro) is None:
        raise ValueError("Digite um ID válido.") 
    # busca o centro pelo banco de dados
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM centro_automotivo WHERE id_centro = :id_centro", {"id_centro": id_centro})
        centro_existe = cursor.fetchone()[0] > 0
        cursor.close()
        return centro_existe

# retorna o centro caso ele exista pelo ID    
def verificar_centro_obter(id_centro):
    # verifica formato do ID
    if re.match(regexIdCentro, id_centro) is None:
        raise ValueError("Digite um ID válido.") 
    # busca o centro pelo banco de dados
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM centro_automotivo WHERE id_centro = :id_centro", {"id_centro": id_centro})
        centro = cursor.fetchone()
        cursor.close()
        return centro

# FUNÇÕES DE CARGO
# gerenciador de cargo
def gerenciar_cargo():
    print("\nIniciando menu de gerenciamento de Cargo...") 
    while True:
        print("\n==============[ GERENCIAMENTO CARGO 📩 ]==============\n")
        print("1 - Criar Cargo")
        print("2 - Visualizar informações do Cargo")
        print("3 - Visualizar todos os Cargos")
        print("4 - Atualizar Cargo")
        print("5 - Deletar Cargo")
        print("6 - Exportar Cargos para JSON")
        print("0 - Sair")
        verif_gerenc_op = input("\nSelecione uma opção: ")
        if not verif_gerenc_op.isdigit() or int(verif_gerenc_op) > 6 or int(verif_gerenc_op) < 0:
            print("\nSelecione uma opção válida.")
            continue
        verif_gerenc_op = int(verif_gerenc_op)
        if verif_gerenc_op == 0:
            break
        elif verif_gerenc_op == 1:
            criar_cargo()
        elif verif_gerenc_op == 2:
            id_cargo = input("Qual o ID do cargo que deseja visualizar? (formato: CGXX): ")
            read_cargo(id_cargo)
        elif verif_gerenc_op == 3:
            read_all_cargos()
        elif verif_gerenc_op == 4:
            id_cargo = input("Qual o ID do cargo que deseja atualizar? (formato: CGXX): ")
            atualizar_cargo(id_cargo)
        elif verif_gerenc_op == 5:
            id_cargo = input("Qual o ID do cargo que deseja deletar? (formato: CGXX): ")
            deletar_cargo(id_cargo)
        elif verif_gerenc_op == 6:
            exportar_cargos_json()

# cria um cargo
def criar_cargo():
    print("Iniciando cadastro de cargo...\n")
    cargo = {}
    # cadastro id do cargo
    while True:
        try:
            id_cargo = input("Digite um ID para o Cargo (formato: CGXX. Ex: CG01): ")
            cargo_repetido = verificar_cargo(id_cargo)
            if cargo_repetido:
                raise ValueError("O ID digitado já existe.")
        except ValueError as e:
            print(e)
        else:
            cargo['id_cargo'] = id_cargo
            print('ID registrado com sucesso.')
            break
    # cadastro nome do cargo
    while True:
        try:
            nome_cargo = input("Digite o nome do cargo.................................: ").strip()
            if re.match(regexNome, nome_cargo) is None:
                raise ValueError("Digite um nome válido.")
            if len(nome_cargo) > 50:
                raise ValueError("O nome do cargo deve ter no máximo 50 caracteres.")
        except ValueError as e:
            print(e) 
        else:
            cargo['nome_cargo'] = nome_cargo
            print('Nome do cargo registrado com sucesso.')
            break 
    # cadastro area cargo
    while True:
        try:
            area_cargo = input("Digite a área do cargo.................................: ").strip()
            if re.match(regexNome, nome_cargo) is None:
                raise ValueError("Área do cargo inválida.")
            if len(area_cargo) > 50:
                raise ValueError("A área do cargo deve ter no máximo 50 caracteres.")
        except ValueError as e:
            print(e)
        else:
            cargo['area_cargo'] = area_cargo
            print('Área registrada com sucesso.')
            break
    # cadastro descricao cargo
    while True:
        try:
            descricao_cargo = input("Digite a descrição do cargo............................: ").strip()
            if not descricao_cargo:
                raise ValueError("Descrição vazia.")
            if len(descricao_cargo) > 255:
                raise ValueError("A descrição deve ter no máximo 255 caracteres.")
        except ValueError as e:
            print(e)
        else:
            cargo['descricao_cargo'] = descricao_cargo
            print("Descrição registrada com sucesso.")
            break
    # cadastro salario cargo
    while True:
        try:
            salario_cargo = float(input("Qual o salário do cargo?...............................: "))
            if salario_cargo <= 0:
                raise ValueError("Digite um valor maior que zero.")
            salario_cargo = str(salario_cargo)
            if re.match(regexValor, salario_cargo) is None:
                    raise ValueError("Digite um salário válido (9 dígitos no máximo, 2 casas decimais no máximo)") 
            salario_cargo = float(salario_cargo)
            if verificar_salario_repetido(salario_cargo):
                raise ValueError("Salário repetido.")    
        except ValueError as e:
            if "could not convert string" in str(e):
                print("Digite um valor numérico válido.")
            else:
                print(e)
        else:
            cargo['salario_cargo'] = salario_cargo
            print("Salário do Cargo registrado com sucesso.")
            break
    
    with conectar() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO cargo (id_cargo, nome_cargo, area_cargo, descricao_cargo, salario_cargo) 
                VALUES (:id_cargo, :nome_cargo, :area_cargo, :descricao_cargo, :salario_cargo)""", 
                cargo)
            conn.commit()
            print(f"\nCargo de ID: {id_cargo} cadastrado com sucesso! ✅​") 
        except oracledb.DatabaseError as e:
            error, = e.args 
            print("\nErro ao cadastrar o Cargo no SQL!")
            print("Código do erro:", error.code)
            print("Mensagem do erro:", error.message)
            print("Contexto do erro:", error.context)
        finally:
            cursor.close()

# visualiza um cargo
def read_cargo(id_cargo):
    try:
        if not verificar_cargo(id_cargo):
            raise ValueError("\nCargo não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_cargo, nome_cargo, area_cargo, descricao_cargo, salario_cargo FROM cargo WHERE id_cargo = :id_cargo", {"id_cargo": id_cargo})
                cargo_atual = cursor.fetchone()
    except ValueError as e:
        print(e)
    else:
        imprimir_cargo(cargo_atual)
        input("Pressione ENTER para voltar ao menu: ")
    finally:
        print("\nRetornando ao menu de cargo...")

# visualiza todos os cargos no banco de dados
def read_all_cargos():
    cargos = select_registros("SELECT * FROM cargo order by 1")
    if cargos:
        for cargo in cargos:
            imprimir_cargo(cargo)
    else:
        print("\nNenhum registro encontrado de cargo.\n")
    input("Pressione ENTER para voltar ao menu: ")
    print("\nRetornando ao menu de cargo...")  

# imprime um cargo
def imprimir_cargo(cargo_atual):
    print(f"\n==============[ INFORMAÇÕES DO CARGO DE ID {cargo_atual[0]} ]==============\n") 
    print(f"ID do Cargo.............: {cargo_atual[0]}")
    print(f"Nome do Cargo...........: {cargo_atual[1]}")
    print(f"Área do Cargo...........: {cargo_atual[2]}")
    print(f"Descrição do Cargo......: {cargo_atual[3]}")
    print(f"Salário do Cargo........: R${cargo_atual[4]}\n")

# atualiza um cargo
def atualizar_cargo(id_cargo):
    try:
        if not verificar_cargo(id_cargo):
            raise ValueError("Cargo não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor: 
                while True:
                    print("\n==============[ ATUALIZAÇÃO DOS DADOS DO CARGO 📩 ]==============\n")
                    print("1 - Atualizar Nome do Cargo")
                    print("2 - Atualizar Área do Cargo")
                    print("3 - Atualizar Descrição do Cargo")
                    print("4 - Atualizar Salário do Cargo")
                    print("0 - Sair")
                    op_atualizar = input("\nSelecione uma opção: ")
                    if not op_atualizar.isdigit() or int(op_atualizar) > 4 or int(op_atualizar) < 0:
                        print("\nSelecione uma opção válida.")
                        continue
                    op_atualizar = int(op_atualizar)
                    if op_atualizar == 0:
                        print('Retornando ao menu de cargo....')
                        break
                    match op_atualizar:               
                        case 1:
                            while True:
                                try:
                                    nome_cargo = input("Digite o novo nome do cargo.................................: ").strip()
                                    if re.match(regexNome, nome_cargo) is None:
                                        raise ValueError("Digite um nome válido.")
                                    if len(nome_cargo) > 50:
                                        raise ValueError("O nome do cargo deve ter no máximo 50 caracteres.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE cargo SET nome_cargo = :nome_cargo WHERE id_cargo = :id_cargo", {"nome_cargo": nome_cargo, "id_cargo": id_cargo})
                                    conn.commit()
                                    print('\nNome do cargo atualizado com sucesso. ✅​')
                                    break 
                        case 2:
                            while True:
                                try:
                                    area_cargo = input("Digite a nova área do cargo.............................: ").strip()
                                    if re.match(regexNome, area_cargo) is None:
                                        raise ValueError("Área do cargo inválida.")
                                    if len(area_cargo) > 50:
                                        raise ValueError("A área do cargo deve ter no máximo 50 caracteres.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE cargo SET area_cargo = :area_cargo WHERE id_cargo = :id_cargo", {"area_cargo": area_cargo, "id_cargo": id_cargo})
                                    conn.commit()
                                    print('\nÁrea do cargo atualizada com sucesso. ✅​')
                                    break
                        case 3:
                            while True:
                                try:
                                    descricao_cargo = input("Digite a nova descrição do cargo........: ").strip()
                                    if not descricao_cargo:
                                        raise ValueError("Descrição do cargo vazia.")
                                    if len(descricao_cargo) > 255:
                                        raise ValueError("A descrição deve ter no máximo 255 caracteres.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE cargo SET descricao_cargo = :descricao_cargo WHERE id_cargo = :id_cargo", {"descricao_cargo": descricao_cargo, "id_cargo": id_cargo})
                                    conn.commit()
                                    print("\nDescrição do cargo atualizada com sucesso. ✅​")
                                    break
                        case 4:
                            while True:
                                try:
                                    salario_cargo = float(input("Qual o novo salário do cargo?: "))
                                    if salario_cargo <= 0:
                                        raise ValueError("Digite um valor maior que zero.")
                                    salario_cargo = str(salario_cargo)
                                    if re.match(regexValor, salario_cargo) is None:
                                            raise ValueError("Digite um salário válido (9 dígitos no máximo, 2 casas decimais no máximo)") 
                                    salario_cargo = float(salario_cargo)
                                    if verificar_salario_repetido(salario_cargo):
                                        raise ValueError("Salário repetido.")
                                except ValueError as e:
                                    if "could not convert string" in str(e):
                                        print("Digite um valor numérico válido.")
                                    else:
                                        print(e)
                                else:
                                    cursor.execute("UPDATE cargo SET salario_cargo = :salario_cargo WHERE id_cargo = :id_cargo", {"salario_cargo": salario_cargo, "id_cargo": id_cargo})
                                    conn.commit()
                                    print("\nSalário do cargo atualizado com sucesso. ✅")
                                    break
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de cargo.....')

# deleta um cargo 
def deletar_cargo(id_cargo):
    try: 
        if not verificar_cargo(id_cargo):
            raise ValueError("\nCargo não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                while True:
                    op_delete = input(f"\nDeseja realmente remover o cargo de ID {id_cargo}? S ou N: ")
                    if op_delete.upper() != "S" and op_delete.upper() != "N":
                        print("\nDigite uma opção válida.")
                        continue
                    elif op_delete.upper() == "S":
                        cursor.execute("DELETE FROM cargo WHERE id_cargo = :id_cargo", {"id_cargo": id_cargo})
                        conn.commit()
                        print("\nCargo removido com sucesso. ✅")
                        break
                    elif op_delete.upper() == "N":
                        print("\nO cargo não foi removido.")
                        break
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de cargo.....')

# exportar todos os cargos para JSON
def exportar_cargos_json():
    try:
        if existem_registros("SELECT COUNT(1) FROM cargo") == False:
            raise ValueError("\nNenhum cargo cadastrado.")
        cargos, colunas = select_registros("SELECT * FROM cargo", None, True)
        while True:
            export_opt = input("Deseja exportar os registros de cargos para JSON? (S ou N): ").upper()
            if export_opt == 'S':
                cargos_json = [dict(zip(colunas, cargo)) for cargo in cargos]
                exportar_para_json(cargos_json, 'cargos.json')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de cargo...')

# verifica a existencia do cargo, retornando um cargo
def verificar_cargo(id_cargo):
     # verifica formato do ID
    if re.match(regexIdCargo, id_cargo) is None:
        raise ValueError("Digite um ID válido.") 
    # busca o cargo pelo banco de dados
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cargo WHERE id_cargo = :id_cargo", {"id_cargo": id_cargo})
        cargo_existe = cursor.fetchone()[0] > 0
        cursor.close()
        return cargo_existe

# retorna o cargo caso ele exista pelo ID    
def verificar_cargo_obter(id_cargo):
    # verifica formato do ID
    if re.match(regexIdCargo, id_cargo) is None:
        raise ValueError("Digite um ID válido.") 
    # busca o cargo pelo banco de dados
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cargo WHERE id_cargo = :id_cargo", {"id_cargo": id_cargo})
        cargo = cursor.fetchone()
        cursor.close()
        return cargo

# verifica se o salário informado já existe
def verificar_salario_repetido(salario_cargo):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cargo WHERE salario_cargo = :salario_cargo", {"salario_cargo": salario_cargo})
        nome_repetido = cursor.fetchone()[0] > 0
        cursor.close()
        return nome_repetido     

# FUNÇÕES DE FUNCIONÁRIO
# gerenciador de funcionario
def gerenciar_funcionario():
    print("\nIniciando menu de gerenciamento de Funcionário...") 
    while True:
        print("\n==============[ GERENCIAMENTO FUNCIONÁRIO 🧑‍💼 ]==============\n")
        print("1 - Cadastrar Funcionário")
        print("2 - Visualizar informações do Funcionário")
        print("3 - Visualizar todos os Funcionários")
        print("4 - Atualizar Funcionário")
        print("5 - Deletar Funcionário")
        print("6 - Exportar Funcionários para JSON")
        print("0 - Sair")
        verif_gerenc_op = input("\nSelecione uma opção: ")
        if not verif_gerenc_op.isdigit() or int(verif_gerenc_op) > 6 or int(verif_gerenc_op) < 0:
            print("\nSelecione uma opção válida.")
            continue
        verif_gerenc_op = int(verif_gerenc_op)
        if verif_gerenc_op == 0:
            break
        elif verif_gerenc_op == 1:
            cadastrar_funcionario()
        elif verif_gerenc_op == 2:
            matricula_funcionario = input("Qual a matrícula do funcionário que deseja visualizar? (formato: MXXXXX): ")
            read_funcionario(matricula_funcionario)
        elif verif_gerenc_op == 3:
            read_all_funcionarios()
        elif verif_gerenc_op == 4:
            matricula_funcionario = input("Qual a matrícula do funcionário que deseja atualizar? (formato: MXXXXX): ")
            atualizar_funcionario(matricula_funcionario)
        elif verif_gerenc_op == 5:
            matricula_funcionario = input("Qual a matrícula do funcionário que deseja deletar? (formato: MXXXXX): ")
            deletar_funcionario(matricula_funcionario)
        elif verif_gerenc_op == 6:
            exportar_funcionarios_json()

# cadastrar um funcionario
def cadastrar_funcionario(): 
    funcionario = {}
    try:
        cargos, centros = verificar_centros_cargos()
    except ValueError as e:
            print(e)
    else:
        print("Iniciando cadastro do funcionário...\n")
        # cadastro matricula
        while True:
            try:
                matricula = input("Digite a matrícula do funcionário (formato: MXXXXX. Ex: M12345): ")
                matricula_repetida = verificar_funcionario(matricula)
                if matricula_repetida:
                    raise ValueError("A matrícula inserida já foi cadastrada.")
            except ValueError as e:
                print(e) 
            else: 
                funcionario['matricula_func'] = matricula
                print('Matrícula registrada com sucesso.')
                break 
        # cadastro nome funcionario
        while True:
            try:
                nome = input("Digite o nome do funcionário...................................: ").strip()
                if re.match(regexNome, nome) is None:
                    raise ValueError("Digite um nome válido.")
                if len(nome) > 70:
                    raise ValueError("O nome do funcionário deve ter no máximo 70 caracteres")
            except ValueError as e:
                print(e) 
            else:
                funcionario['nome_func'] = nome
                print('Nome registrado com sucesso.')
                break
        # cadastro disponibilidade
        while True:
            try: 
                disponibilidade_func = input("Qual a disponibilidade do funcionário? ('S' ou 'N'): ")
                if disponibilidade_func.upper() != "S" and disponibilidade_func.upper() != "N":
                    raise ValueError("Digite uma opção válida.")
            except ValueError as e:
                print(e)
            else:
                funcionario['disponibilidade_func'] = disponibilidade_func.upper()
                print('Disponibilidade registrada com sucesso.')
                break
        # cadastro horario de trabalho
        while True:
            try:
                horario_trabalho = input("Digite o horário de trabalho (ex: 08:00 - 17:30)...............: ")
                if re.match(regexHorarioFuncionamento, horario_trabalho) is None:
                    raise ValueError("Digite um horário válido.")
            except ValueError as e:
                print(e) 
            else:
                funcionario['horario_trabalho'] = horario_trabalho
                print('Horário de trabalho registrado com sucesso.')
                break
        # cadastro centro automotivo
        while True:
            try:
                print("\n==============[ CENTROS AUTOMOTIVOS ]==============\n")
                for i in range(len(list(centros))):
                    print(f"{i} - {list(centros)[i][1]}")
                op_centro = input("\nEm qual centro automotivo o funcionário trabalha?......: ")
                if not op_centro.isdigit() or int(op_centro) > (len(list(centros)) - 1) or int(op_centro) < 0:
                    raise ValueError("\nSelecione uma opção válida.")
            except ValueError as e:
                print(e)
            else: 
                op_centro = int(op_centro)
                funcionario['centro_automotivo_id_centro'] = centros[op_centro][0]
                print('Centro Automotivo registrado com sucesso.')
                break
        # cadastro cargo
        while True:
            try:
                print("\n==============[ CARGOS ]==============\n")
                for i in range(len(list(cargos))):
                    print(f"{i} - {list(cargos)[i][1]}")
                op_cargo = input("\nQual o cargo do funcionário?: ")
                if not op_cargo.isdigit() or int(op_cargo) > (len(list(cargos)) - 1) or int(op_cargo) < 0:
                    raise ValueError("\nSelecione uma opção válida.")
            except ValueError as e:
                print(e)
            else: 
                op_cargo = int(op_cargo)
                funcionario['cargo_id_cargo'] = cargos[op_cargo][0]
                print('Cargo registrado com sucesso.')
                break

        with conectar() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO funcionario (matricula_func, nome_func, horario_trabalho, disponibilidade_func, centro_automotivo_id_centro, cargo_id_cargo) 
                    VALUES (:matricula_func, :nome_func, :horario_trabalho, :disponibilidade_func, :centro_automotivo_id_centro, :cargo_id_cargo)""", 
                    funcionario)
                conn.commit()
                print(f"\nFuncionário de Matrícula: {matricula} cadastrado com sucesso! ✅​") 
            except oracledb.DatabaseError as e:
                error, = e.args 
                print("\nErro ao cadastrar o Funcionário no SQL!")
                print("Código do erro:", error.code)
                print("Mensagem do erro:", error.message)
                print("Contexto do erro:", error.context)
            finally:
                cursor.close()
    finally:
        print('\nRetornando ao menu de funcionário...')

# visualizar um funcionario
def read_funcionario(matricula):
    try:
        if not verificar_funcionario(matricula):
            raise ValueError("\nFuncionário não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT matricula_func, nome_func, horario_trabalho, disponibilidade_func, centro_automotivo_id_centro, cargo_id_cargo FROM funcionario WHERE matricula_func = :matricula_func", {"matricula_func": matricula})
                funcionario_atual = cursor.fetchone()
    except ValueError as e:
        print(e)
    else:
        imprimir_funcionario(funcionario_atual)
        input("Pressione ENTER para voltar ao menu: ")
    finally:
        print('\nRetornando ao menu de funcionário.....')

# visualiza todos os funcionários
def read_all_funcionarios():
    funcionarios = select_registros("SELECT * FROM funcionario")
    if funcionarios:
        for funcionario in funcionarios:
            imprimir_funcionario(funcionario)
    else:
        print("\nNenhum registro encontrado de funcionário.\n")
    input("Pressione ENTER para voltar ao menu: ")
    print("\nRetornando ao menu de funcionário...")  

# imprime um funcionário
def imprimir_funcionario(funcionario_atual):
    print(f"\n==============[ INFORMAÇÕES DO FUNCIONÁRIO DE MATRÍCULA {funcionario_atual[0]} ]==============\n") 
    print(f"Matrícula.........................: {funcionario_atual[0]}")
    print(f"Nome do Funcionário...............: {funcionario_atual[1]}")
    print(f"Horário de Trabalho...............: {funcionario_atual[2]}")
    print(f"ID do Centro Automotivo...........: {funcionario_atual[4] if funcionario_atual[4] else 'Sem Centro Automotivo (inativo)'}")
    print(f"ID do Cargo.......................: {funcionario_atual[5] if funcionario_atual[5] else 'Sem Cargo (inativo)'}")
    print(f"Disponibilidade...................: {'Disponível' if funcionario_atual[3] == 'S' else 'Indisponível'}\n")

# atualizar um funcionario
def atualizar_funcionario(matricula):
    try:
        if not verificar_funcionario(matricula):
            raise ValueError("Funcionário não encontrado.")
        cargos, centros = verificar_centros_cargos()
        with conectar() as conn:
            with conn.cursor() as cursor: 
                while True:
                    print("\n==============[ ATUALIZAÇÃO DOS DADOS DO FUNCIONÁRIO 🧑‍💼 ]==============\n")
                    print("1 - Atualizar Nome do Funcionário")
                    print("2 - Atualizar Horário de Trabalho")
                    print("3 - Atualizar Centro Automotivo")
                    print("4 - Atualizar Cargo")
                    print("5 - Atualizar Disponibilidade")
                    print("0 - Sair")
                    op_atualizar = input("\nSelecione uma opção: ")
                    if not op_atualizar.isdigit() or int(op_atualizar) > 5 or int(op_atualizar) < 0:
                        print("\nSelecione uma opção válida.")
                        continue
                    op_atualizar = int(op_atualizar)
                    if op_atualizar == 0:
                        print('Retornando ao menu de cargo....')
                        break
                    match op_atualizar:
                        case 1:
                            while True:
                                try:
                                    nome = input("Digite o novo nome do funcionário............................: ").strip()
                                    if re.match(regexNome, nome) is None:
                                        raise ValueError("Digite um nome válido.")
                                    if len(nome) > 70:
                                        raise ValueError("O nome do funcionário deve ter no máximo 70 caracteres")
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE funcionario SET nome_func = :nome_func WHERE matricula_func = :matricula_func", {"nome_func": nome, "matricula_func": matricula})
                                    conn.commit()
                                    print('\nNome atualizado com sucesso. ✅')
                                    break 
                        case 2:
                            while True:
                                    try:
                                        horario_trabalho = input("Digite o novo horário de trabalho (ex: 08:00 - 17:30)..............: ")
                                        if re.match(regexHorarioFuncionamento, horario_trabalho) is None:
                                            raise ValueError("Digite um horário válido.")
                                    except ValueError as e:
                                        print(e) 
                                    else:
                                        cursor.execute("UPDATE funcionario SET horario_trabalho = :horario_trabalho WHERE matricula_func = :matricula_func", {"horario_trabalho": horario_trabalho, "matricula_func": matricula})
                                        conn.commit()
                                        print('\nHorário de trabalho atualizado com sucesso. ✅')
                                        break
                        case 3:
                            while True:
                                try:
                                    print("\n==============[ CENTROS AUTOMOTIVOS ]==============\n")
                                    for i in range(len(list(centros))):
                                        print(f"{i} - {list(centros)[i][1]}")
                                    op_centro = input("\nQual o novo centro automotivo que o funcionário trabalhará?......: ")
                                    if not op_centro.isdigit() or int(op_centro) > (len(list(centros)) - 1) or int(op_centro) < 0:
                                        raise ValueError("\nSelecione uma opção válida.")
                                except ValueError as e:
                                    print(e)
                                else: 
                                    op_centro = int(op_centro)
                                    cursor.execute("UPDATE funcionario SET centro_automotivo_id_centro = :centro_automotivo_id_centro WHERE matricula_func = :matricula_func", {"centro_automotivo_id_centro": centros[op_centro][0], "matricula_func": matricula})
                                    conn.commit()
                                    print('\nCentro Automotivo atualizado com sucesso. ✅')
                                    break
                        case 4:
                            while True:
                                try:
                                    print("\n==============[ CARGOS ]==============\n")
                                    for i in range(len(list(cargos))):
                                        print(f"{i} - {list(cargos)[i][1]}")
                                    op_cargo = input("\nQual o novo cargo do funcionário?: ")
                                    if not op_cargo.isdigit() or int(op_cargo) > (len(list(cargos)) - 1) or int(op_cargo) < 0:
                                        raise ValueError("\nSelecione uma opção válida.")
                                except ValueError as e:
                                    print(e)
                                else: 
                                    op_cargo = int(op_cargo)
                                    cursor.execute("UPDATE funcionario SET cargo_id_cargo = :cargo_id_cargo WHERE matricula_func = :matricula_func", {"cargo_id_cargo": cargos[op_cargo][0], "matricula_func": matricula})
                                    conn.commit()
                                    print('\nCargo atualizado com sucesso. ✅')
                                    break
                        case 5:
                            while True:
                                try: 
                                    disponibilidade_func = input("Qual a nova disponibilidade do funcionário? ('S' ou 'N'): ")
                                    if disponibilidade_func.upper() != "S" and disponibilidade_func.upper() != "N":
                                        raise ValueError("Digite uma opção válida.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE funcionario SET disponibilidade_func = :disponibilidade_func WHERE matricula_func = :matricula_func", {"disponibilidade_func": disponibilidade_func, "matricula_func": matricula})
                                    conn.commit()
                                    print('\nDisponibilidade atualizada com sucesso. ✅')
                                    break
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de funcionário.....')

# deletar um funcionario
def deletar_funcionario(matricula):
    try: 
        if not verificar_funcionario(matricula):
            raise ValueError("\nFuncionário não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                while True:
                    op_delete = input(f"\nDeseja realmente remover o funcionário de Matrícula {matricula}? S ou N: ")
                    if op_delete.upper() != "S" and op_delete.upper() != "N":
                        print("\nDigite uma opção válida.")
                        continue
                    elif op_delete.upper() == "S":
                        cursor.execute("DELETE FROM funcionario WHERE matricula_func = :matricula_func", {"matricula_func": matricula})
                        conn.commit()
                        print("\nFuncionário removido com sucesso. ✅")
                        break
                    elif op_delete.upper() == "N":
                        print("\nO Funcionário não foi removido.")
                        break
    except ValueError as e:
        print(e)  
    finally:
        print('\nRetornando ao menu de funcionário.....')

# verifica a existencia de um funcionario, retornando um
def verificar_funcionario(matricula):
     # verifica formato do ID
    if re.match(regexMatriculaFunc, matricula) is None:
        raise ValueError("Digite um ID válido.") 
    # busca o funcionario pelo banco de dados
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM funcionario WHERE matricula_func = :matricula_func", {"matricula_func": matricula})
        funcionario_existe = cursor.fetchone()[0] > 0
        cursor.close()
        return funcionario_existe

# verifica se ao menos 1 centro e 1 cargo existem para que o funcionário possa existir.
def verificar_centros_cargos():
    cargos = select_registros('SELECT * FROM cargo order by 1')
    centros = select_registros('SELECT * FROM centro_automotivo')
    if cargos and centros:
        return cargos, centros
    else: 
        raise ValueError('É necessário ao menos 1 cargo e 1 centro automotivo para cadastrar um funcionário.')

# exporta os registros de funcionarios para JSON
def exportar_funcionarios_json():
    try:
        if existem_registros("SELECT COUNT(1) FROM funcionario") == False:
            raise ValueError("\nNenhum funcionario cadastrado.")
        funcionarios, colunas = select_registros("SELECT * FROM funcionario", None, True)
        while True:
            export_opt = input("Deseja exportar os registros de funcionarios para JSON? (S ou N): ").upper()
            if export_opt == 'S':
                funcionarios_json = [dict(zip(colunas, funcionario)) for funcionario in funcionarios]
                exportar_para_json(funcionarios_json, 'funcionarios.json')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de funcionário...')  

# FUNÇÕES DE SERVIÇO
# gerenciar servico
def gerenciar_servico():
    print("\nIniciando menu de gerenciamento de Serviço...") 
    while True:
        print("\n==============[ GERENCIAMENTO SERVIÇO ⚙️  ]==============\n")
        print("1 - Cadastrar Serviço")
        print("2 - Visualizar informações do Serviço")
        print("3 - Visualizar todos os Serviços")
        print("4 - Atualizar Serviço")
        print("5 - Deletar Serviço")
        print("6 - Exportar Serviços para JSON")
        print("0 - Sair")
        verif_gerenc_op = input("\nSelecione uma opção: ")
        if not verif_gerenc_op.isdigit() or int(verif_gerenc_op) > 6 or int(verif_gerenc_op) < 0:
            print("\nSelecione uma opção válida.")
            continue
        verif_gerenc_op = int(verif_gerenc_op)
        if verif_gerenc_op == 0:
            break
        elif verif_gerenc_op == 1:
            criar_servico()
        elif verif_gerenc_op == 2:
            id_servico = input("Qual o ID do serviço que deseja visualizar? (formato: SXXXXX): ")
            read_servico(id_servico)
        elif verif_gerenc_op == 3:
            read_all_servicos()
        elif verif_gerenc_op == 4:
            id_servico = input("Qual o ID do serviço que deseja atualizar? (formato: SXXXXX): ")
            atualizar_servico(id_servico)
        elif verif_gerenc_op == 5:
            id_servico = input("Qual o ID do serviço que deseja deletar? (formato: SXXXXX): ")
            deletar_servico(id_servico)
        elif verif_gerenc_op == 6:
            exportar_servicos_json()
        
# cria um novo serviço
def criar_servico():
    print("Iniciando cadastro de serviço...\n")
    servico = {}
    # cadastro id do serviço
    while True:
        try:
            id_servico = input("Digite um ID para o Serviço (formato: SXXXXX. Ex: S21234)....: ")
            servico_repetido = verificar_servico(id_servico)
            if servico_repetido:
                raise ValueError("O ID digitado já existe.")
        except ValueError as e:
            print(e)
        else:
            servico['id_servico'] = id_servico
            print('ID registrado com sucesso.')
            break
    # cadastro tipo do serviço
    while True:
        try:
            tipo_servico = input("Digite o tipo do serviço.....................................: ").strip()
            if re.match(regexNome, tipo_servico) is None:
                raise ValueError("Digite um tipo válido.")
            if len(tipo_servico) > 50:
                raise ValueError("O tipo do serviço deve ter no máximo 50 caracteres.")
        except ValueError as e:
            print(e)  
        else:
            servico['tipo_servico'] = tipo_servico
            print('Tipo do serviço registrado com sucesso.')
            break
    # cadastro descrição do serviço
    while True:
        try:
            descricao_servico = input("Digite a descrição do serviço................................: ").strip()
            if not descricao_servico:
                raise ValueError("Digite uma descrição válida.")
            if len(descricao_servico) > 255:
                raise ValueError("A descrição deve ter no máximo 255 caracteres.") 
        except ValueError as e:
            print(e)
        else:
            servico['descricao_servico'] = descricao_servico
            print('Descrição registrada com sucesso.')
            break
    # cadastro preço do serviço
    while True:
        try:
            preco = float(input("Digite o preço do serviço....................................: "))
            if preco <= 0:
                raise ValueError("Digite um valor maior que zero.")
            preco = str(preco)
            if re.match(regexValor, preco) is None:
                raise ValueError("Digite um preço válido (9 dígitos no máximo, 2 casas decimais no máximo)") 
            preco = float(preco)
        except ValueError as e:
            if "could not convert string" in str(e):
                print("Digite um valor numérico válido.")
            else:
                print(e)
        else:
            servico['preco_servico'] = preco
            print("Preço registrado com sucesso.")
            break
    # cadastro duracao do serviço
    while True:
        try:
            duracao = int(input("Qual a duração do serviço? (em minutos): "))
            if duracao <= 0 or duracao > 9999:
                raise ValueError("Digite um valor maior que zero e menor que 5 dígitos para a duração do serviço.")
        except ValueError as e:
            if "invalid literal for int()" in str(e):
                print("Digite um valor numérico válido.")
            else:
                print(e)
        else:
            servico['duracao'] = duracao
            print("Duração registrada com sucesso.")
            break
    
    with conectar() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO servico (id_servico, tipo_servico, descricao_servico, preco_servico, duracao) 
                VALUES (:id_servico, :tipo_servico, :descricao_servico, :preco_servico, :duracao)""", 
                servico)
            conn.commit()
            print(f"\nServiço de ID: {id_servico} cadastrado com sucesso! ✅") 
        except oracledb.DatabaseError as e:
            error, = e.args 
            print("\nErro ao cadastrar o Serviço no SQL!")
            print("Código do erro:", error.code)
            print("Mensagem do erro:", error.message)
            print("Contexto do erro:", error.context)
        finally:
            cursor.close()

# visualiza os dados do serviço
def read_servico(id_servico):
    try:
        if not verificar_servico(id_servico):
            raise ValueError("\nServiço não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_servico, tipo_servico, descricao_servico, preco_servico, duracao FROM servico WHERE id_servico = :id_servico", {"id_servico": id_servico})
                servico_atual = cursor.fetchone()
    except ValueError as e:
        print(e)
    else:
        imprimir_servico(servico_atual)
        input("Pressione ENTER para voltar ao menu: ")
    finally:
        print("\nRetornando ao menu de serviço...")

# visualiza todos os servicos
def read_all_servicos():
    servicos = select_registros("SELECT * FROM servico order by 1")
    print(servicos)
    if servicos:
        for servico in servicos:
            imprimir_servico(servico)
    else:
        print("\nNenhum registro encontrado de Serviço.\n")
    input("Pressione ENTER para voltar ao menu: ")
    print("\nRetornando ao menu de serviço...")  

# imprime um serviço
def imprimir_servico(servico_atual):
    print(f"\n==============[ INFORMAÇÕES DO SERVIÇO DE ID {servico_atual[0]} ]==============\n") 
    print(f"ID do Serviço....................: {servico_atual[0]}")
    print(f"Tipo do Serviço..................: {servico_atual[1]}")
    print(f"Descrição do Serviço.............: {servico_atual[2]}")
    print(f"Preço do Serviço.................: R${servico_atual[3]}")
    print(f"Duração do Serviço...............: {servico_atual[4]} minuto(s)\n")

# atualiza os dados do serviço
def atualizar_servico(id_servico):
    try:
        if not verificar_servico(id_servico):
            raise ValueError("Serviço não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor: 
                while True:
                    print("\n==============[ ATUALIZAÇÃO DOS DADOS DO SERVIÇO ⚙️ ]==============\n")
                    print("1 - Atualizar Tipo do Serviço")
                    print("2 - Atualizar Descrição do Serviço")
                    print("3 - Atualizar Preço do Serviço")
                    print("4 - Atualizar Duração do Serviço")
                    print("0 - Sair")
                    op_atualizar = input("\nSelecione uma opção: ")
                    if not op_atualizar.isdigit() or int(op_atualizar) > 5 or int(op_atualizar) < 0:
                        print("\nSelecione uma opção válida.")
                        continue
                    op_atualizar = int(op_atualizar)
                    if op_atualizar == 0:
                        print('Retornando ao menu de serviço....')
                        break
                    match op_atualizar:
                        case 1:
                            while True:
                                try:
                                    tipo_servico = input("Digite o novo tipo do serviço.................................: ").strip()
                                    if re.match(regexNome, tipo_servico) is None:
                                        raise ValueError("Digite um tipo válido.")
                                    if len(tipo_servico) > 50:
                                        raise ValueError("O tipo do serviço deve ter no máximo 50 caracteres.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE servico SET tipo_servico = :tipo_servico WHERE id_servico = :id_servico", {"tipo_servico": tipo_servico, "id_servico": id_servico})
                                    conn.commit()
                                    print('\nTipo do serviço atualizado com sucesso. ✅')
                                    break  
                        case 2:
                            while True:
                                    try:
                                        descricao_servico = input("Digite a nova descrição do serviço.............................: ").strip()
                                        if not descricao_servico:
                                            raise ValueError("Descrição vazia. Digite novamente.")
                                        if len(descricao_servico) > 255:
                                            raise ValueError("A descrição deve ter no máximo 255 caracteres.") 
                                    except ValueError as e:
                                        print(e)
                                    else:
                                        cursor.execute("UPDATE servico SET descricao_servico = :descricao_servico WHERE id_servico = :id_servico", {"descricao_servico": descricao_servico, "id_servico": id_servico})
                                        conn.commit()
                                        print('\nDescrição do serviço atualizada com sucesso. ✅')
                                        break
                        case 3:
                            while True:
                                try:
                                    preco = float(input("Digite o preço do serviço........: "))
                                    if preco <= 0:
                                        raise ValueError("Digite um valor maior que zero.")
                                    preco = str(preco)
                                    if re.match(regexValor, preco) is None:
                                        raise ValueError("Digite um preço válido (9 dígitos no máximo, 2 casas decimais no máximo)") 
                                    preco = float(preco)
                                except ValueError as e:
                                    if "could not convert string" in str(e):
                                        print("Digite um valor numérico válido.")
                                    else:
                                        print(e)
                                else:
                                    cursor.execute("UPDATE servico SET preco_servico = :preco_servico WHERE id_servico = :id_servico", {"preco_servico": preco, "id_servico": id_servico})
                                    conn.commit()
                                    print("\nPreço atualizado com sucesso. ✅")
                                    break
                        case 4:
                            while True:
                                try:
                                    duracao = int(input("Qual a duração do serviço? (em minutos): "))
                                    if duracao <= 0 or duracao > 9999:
                                        raise ValueError("Digite um valor maior que zero e menor que 5 dígitos para a duração do serviço.")
                                except ValueError as e:
                                    if "invalid literal for int()" in str(e):
                                        print("Digite um valor numérico válido.")
                                    else:
                                        print(e)
                                else:
                                    cursor.execute("UPDATE servico SET duracao = :duracao WHERE id_servico = :id_servico", {"duracao": duracao, "id_servico": id_servico})
                                    conn.commit()
                                    print("\nDuração atualizada com sucesso. ✅")
                                    break
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de serviço.....')

# deleta um serviço
def deletar_servico(id_servico):
    try: 
        if not verificar_servico(id_servico):
            raise ValueError("\nServiço não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                while True:
                    op_delete = input(f"\nDeseja realmente deletar o serviço de ID {id_servico}? S ou N: ")
                    if op_delete.upper() != "S" and op_delete.upper() != "N":
                        print("\nDigite uma opção válida.")
                        continue
                    elif op_delete.upper() == "S":
                        cursor.execute("DELETE FROM servico WHERE id_servico = :id_servico", {"id_servico": id_servico})
                        conn.commit()
                        print("\nServiço removido com sucesso. ✅")
                        break
                    elif op_delete.upper() == "N":
                        print("\nServiço não foi removido.")
                        break
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de serviço.....')

# exporta os serviços para json
def exportar_servicos_json():
    try:
        if existem_registros("SELECT COUNT(1) FROM servico") == False:
            raise ValueError("\nNenhum servico cadastrado.")
        servicos, colunas = select_registros("SELECT * FROM servico order by 1", None, True)
        while True:
            export_opt = input("\nDeseja exportar os registros de servicos para JSON? (S ou N): ").upper()
            if export_opt == 'S':
                servicos_json = [dict(zip(colunas, servico)) for servico in servicos]
                exportar_para_json(servicos_json, 'servicos.json')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de serviço...')

# verifica a existencia do servico e o formato do ID
def verificar_servico(id_servico):
    # verifica formato do ID
    if re.match(regexIdServico, id_servico) is None:
        raise ValueError("Digite um ID válido.") 
    # busca o servico pelo banco de dados
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM servico WHERE id_servico = :id_servico", {"id_servico": id_servico})
        servico_existe = cursor.fetchone()[0] > 0
        cursor.close()
        return servico_existe

# retorna o serviço caso exista pelo ID
def verificar_servico_obter(id_servico):
    # verifica formato do ID
    if re.match(regexIdServico, id_servico) is None:
        raise ValueError("Digite um ID válido.") 
    # busca o servico pelo banco de dados
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM servico WHERE id_servico = :id_servico", {"id_servico": id_servico})
        servico = cursor.fetchone()
        cursor.close()
        return servico

# verifica se pelo menos 1 serviço existe para realizar diagnostico
def verificar_servicos():
    servicos = select_registros('SELECT * FROM servico order by 1')
    if servicos:
        return servicos
    else: 
        raise ValueError('É necessário ao menos 1 serviço cadastrado para realizar um diagnóstico.')

#FUNÇÕES DE PEÇAS
# gerenciar peça
def gerenciar_pecas():
    print("\nIniciando menu de gerenciamento de Peça...") 
    while True:
        print("\n==============[ GERENCIAMENTO PEÇA 🔧 ]==============\n")
        print("1 - Cadastrar Peça")
        print("2 - Visualizar informações da Peça por ID")
        print("3 - Visualizar todas as Peças")
        print("4 - Atualizar Peça")
        print("5 - Deletar Peça")
        print("6 - Exportar Peças para JSON")
        print("0 - Sair")
        verif_gerenc_op = input("\nSelecione uma opção: ")
        if not verif_gerenc_op.isdigit() or int(verif_gerenc_op) > 6 or int(verif_gerenc_op) < 0:
            print("\nSelecione uma opção válida.")
            continue
        verif_gerenc_op = int(verif_gerenc_op)
        if verif_gerenc_op == 0:
            break
        elif verif_gerenc_op == 1:
            cadastrar_peca()
        elif verif_gerenc_op == 2:
            id_peca = input("Qual o ID da peça que deseja visualizar? (formato: PXXXXX): ")
            read_peca(id_peca)
        elif verif_gerenc_op == 3:
            read_all_pecas()
        elif verif_gerenc_op == 4:
            id_peca = input("Qual o ID da peça que deseja atualizar? (formato: PXXXXX): ")
            atualizar_peca(id_peca)
        elif verif_gerenc_op == 5:
            id_peca = input("Qual o ID da peça que deseja deletar? (formato: PXXXXX): ")
            deletar_peca(id_peca)
        elif verif_gerenc_op == 6:
            exportar_pecas_json()

# cadastra uma peça
def cadastrar_peca():
    print("Iniciando cadastro da peça...\n")
    peca = {}
    # cadastro id peca
    while True:
        try:
            id_peca = input("Digite o ID da peça (formato: PXXXXX. Ex: P12345): ")
            peca_repetida = verificar_peca(id_peca)
            if peca_repetida:
                raise ValueError("O ID inserido já foi cadastrado.")
        except ValueError as e:
            print(e)
        else:
            peca['id_peca'] = id_peca
            print('ID registrado com sucesso.')
            break
    # cadastro nome peca
    while True:
        try:
            nome_peca = input("Digite o nome da peça............................: ").strip()
            if re.match(regexNome, nome_peca) is None:
                raise ValueError("Digite um nome válido.")
            if len(nome_peca) > 255:
                raise ValueError("O nome da peça deve ter no máximo 255 caracteres.")
            if verificar_nome_peca(nome_peca):
                raise ValueError("Nome da peça repetido.")
        except ValueError as e:
            print(e)
        else:
            peca['nome_peca'] = nome_peca
            print('Nome registrado com sucesso.')
            break
    # cadastro disponivel
    while True:
        try:
            qtnd_disponivel = int(input("Digite a quantidade disponível...................: "))
            if qtnd_disponivel <= 0 or qtnd_disponivel >= 100000000:
                raise ValueError("Digite uma quantidade maior que zero e com no máximo 8 casas inteiras.")      
        except ValueError as e:
            if "invalid literal for int()" in str(e):
                print("Digite um valor numérico válido.")
            else:
                print(e)
        else:
            peca['disponibilidade_peca'] = qtnd_disponivel
            print('Quantidade disponível registrada com sucesso.')
            break
    # cadastro preço
    while True:
        try:
            preco = float(input("Qual o preço da peça?............................: "))
            if preco <= 0:
                raise ValueError("Digite um valor maior que zero.")
            preco = str(preco)
            if re.match(regexValor, preco) is None:
                raise ValueError("Digite um preço válido (9 dígitos no máximo, 2 casas decimais no máximo).") 
            preco = float(preco)            
        except ValueError as e:
            if "could not convert string" in str(e):
                print("Digite um valor numérico válido.")
            else:
                print(e)
        else:
            peca['preco_peca'] = preco
            print('Preço registrado com sucesso.')
            break
    
    with conectar() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO peca (id_peca, disponibilidade_peca, nome_peca, preco_peca) 
                VALUES (:id_peca, :disponibilidade_peca, :nome_peca, :preco_peca)""", 
                peca)
            conn.commit()
            print(f"\nPeça de ID: {id_peca} cadastrada com sucesso! ✅") 
        except oracledb.DatabaseError as e:
            error, = e.args 
            print("\nErro ao cadastrar a Peça no SQL!")
            print("Código do erro:", error.code)
            print("Mensagem do erro:", error.message)
            print("Contexto do erro:", error.context)
        finally:
            cursor.close()

# visualiza uma peça com base no ID
def read_peca(id_peca):
    try:
        if not verificar_peca(id_peca):
            raise ValueError("\nPeça não encontrada.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_peca, disponibilidade_peca, nome_peca, preco_peca FROM peca WHERE id_peca = :id_peca", {"id_peca": id_peca})
                peca_atual = cursor.fetchone()
    except ValueError as e:
        print(e)
    else:
        imprimir_peca(peca_atual)
        input("Pressione ENTER para voltar ao menu: ")
    finally:
        print("\nRetornando ao menu de peça...")

# visualiza todas as peças da tabela
def read_all_pecas():
    pecas = select_registros("SELECT * FROM peca")
    if pecas:
        for peca in pecas:
            imprimir_peca(peca)
    else:
        print("\nNenhum registro encontrado de peça.\n")
    input("Pressione ENTER para voltar ao menu: ")
    print("\nRetornando ao menu de peça...") 

# imprime os dados de uma peça
def imprimir_peca(peca_atual):
    print(f"\n==============[ INFORMAÇÕES DA PEÇA DE ID {peca_atual[0]} ]==============\n") 
    print(f"ID da Peça....................: {peca_atual[0]}")
    print(f"Nome da Peça..................: {peca_atual[2]}")
    print(f"Disponibilidade da peça.......: {peca_atual[1] if peca_atual[1] > 0 else 'Indisponível'}")
    print(f"Preço da Peça.................: R${peca_atual[3]}\n")

# atualiza uma peça
def atualizar_peca(id_peca):
    try:
        if not verificar_peca(id_peca):
            raise ValueError("Peça não encontrada.")
        with conectar() as conn:
            with conn.cursor() as cursor:     
                while True:
                    print("\n==============[ ATUALIZAÇÃO DOS DADOS DA PEÇA 🔧 ]==============\n")
                    print("1 - Atualizar Nome da Peça")
                    print("2 - Atualizar Disponibilidade da Peça")
                    print("3 - Atualizar Preço da peça")
                    print("0 - Sair")
                    op_atualizar = input("\nSelecione uma opção: ")
                    if not op_atualizar.isdigit() or int(op_atualizar) > 3 or int(op_atualizar) < 0:
                        print("\nSelecione uma opção válida.")
                        continue
                    op_atualizar = int(op_atualizar)
                    if op_atualizar == 0:
                        break
                    match op_atualizar:
                        case 1:
                            while True:
                                try:
                                    nome_peca = input("Digite o novo nome da peça............................: ").strip()
                                    if re.match(regexNome, nome_peca) is None:
                                        raise ValueError("Digite um nome válido.")
                                    if len(nome_peca) > 255:
                                        raise ValueError("O nome da peça deve ter no máximo 255 caracteres.")
                                    if verificar_nome_peca(nome_peca):
                                        raise ValueError("Nome da peça repetido.")
                                except ValueError as e:
                                    print(e)  
                                else: 
                                    cursor.execute("UPDATE peca SET nome_peca = :nome_peca WHERE id_peca = :id_peca", {"nome_peca": nome_peca, "id_peca": id_peca})
                                    conn.commit()
                                    print('\nNome atualizado com sucesso. ✅')
                                    break
                        case 2:
                            while True:
                                try:
                                    disponibilidade_peca = int(input("Digite a nova disponibilidade da peça..............: "))
                                    if disponibilidade_peca <= 0 or disponibilidade_peca >= 100000000:
                                        raise ValueError("Digite uma quantidade maior que zero e com no máximo 8 casas inteiras.")       
                                except ValueError as e:
                                    if "invalid literal for int()" in str(e):
                                        print("Digite um valor numérico válido.")
                                    else:
                                        print(e)
                                else:
                                    cursor.execute("UPDATE peca SET disponibilidade_peca = :disponibilidade_peca WHERE id_peca = :id_peca", {"disponibilidade_peca": disponibilidade_peca, "id_peca": id_peca})
                                    conn.commit()
                                    print('\nDisponibilidade atualizada com sucesso. ✅')
                                    break
                        case 3:
                            while True:
                                try:
                                    preco_peca = float(input("Qual o novo preço da peça?: "))
                                    if preco_peca <= 0:
                                        raise ValueError("Digite um valor maior que zero.")
                                    preco_peca = str(preco_peca)
                                    if re.match(regexValor, preco_peca) is None:
                                        raise ValueError("Digite um preço válido (9 dígitos no máximo, 2 casas decimais no máximo).") 
                                    preco_peca = float(preco_peca)
                                except ValueError as e:
                                    if "could not convert string" in str(e):
                                        print("Digite um valor numérico válido.")
                                    else:
                                        print(e) 
                                else:
                                    cursor.execute("UPDATE peca SET preco_peca = :preco_peca WHERE id_peca = :id_peca", {"preco_peca": preco_peca, "id_peca": id_peca})
                                    conn.commit()
                                    print('\nPreço atualizado com sucesso. ✅')
                                    break
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de peça.....')

# deleta uma peça
def deletar_peca(id_peca):
    try: 
        if not verificar_peca(id_peca):
            raise ValueError("\nPeça não encontrada.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                while True:
                    op_delete = input(f"\nDeseja realmente remover a Peça de ID {id_peca}? S ou N: ")
                    if op_delete.upper() != "S" and op_delete.upper() != "N":
                        print("\nDigite uma opção válida.")
                        continue
                    elif op_delete.upper() == "S":
                        cursor.execute("DELETE FROM peca WHERE id_peca = :id_peca", {"id_peca": id_peca})
                        conn.commit()
                        print("\nPeça removida com sucesso. ✅")
                        break
                    elif op_delete.upper() == "N":
                        print("\nA Peça não foi removida.")
                        break 
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de peça.....')       

# exporta os registros de peças do banco de dados para JSON
def exportar_pecas_json():
    try:
        if existem_registros("SELECT COUNT(1) FROM peca") == False:
            raise ValueError("\nNenhuma peça cadastrada.")
        pecas, colunas = select_registros("SELECT * FROM peca", None, True)
        while True:
            export_opt = input("Deseja exportar os registros de peças para JSON? (S ou N): ").upper()
            if export_opt == 'S':
                pecas_json = [dict(zip(colunas, peca)) for peca in pecas]
                exportar_para_json(pecas_json, 'pecas.json')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de peça...')

# verifica a existencia da peca e verifica o formato do ID
def verificar_peca(id_peca):
     # verifica formato do ID
    if re.match(regexIdPeca, id_peca) is None:
        raise ValueError("Digite um ID válido.") 
    # busca a peca pelo banco de dados
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM peca WHERE id_peca = :id_peca", {"id_peca": id_peca})
        peca_existe = cursor.fetchone()[0] > 0
        cursor.close()
        return peca_existe

# retorna a peça caso exista pelo ID
def verificar_peca_obter(id_peca):
    # verifica formato do ID
    if re.match(regexIdPeca, id_peca) is None:
        raise ValueError("Digite um ID válido.") 
    # busca a peca pelo banco de dados
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM peca WHERE id_peca = :id_peca", {"id_peca": id_peca})
        peca = cursor.fetchone()
        cursor.close()
        return peca

# verifica se o nome da peça é repetido
def verificar_nome_peca(nome_peca):
   with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM peca WHERE nome_peca = :nome_peca", {"nome_peca": nome_peca})
        nome_repetido = cursor.fetchone()[0] > 0
        cursor.close()
        return nome_repetido 

#FUNÇÕES DO AUTODIAGNÓSTICO
# gerenciar autodiagnostico
def gerenciar_autodiagnostico():
    print("\nIniciando menu de gerenciamento de Autodiagnóstico...") 
    while True:
        print("\n==============[ GERENCIAMENTO AUTODIAGNÓSTICO 🩺 ]==============\n")
        print("1 - Realizar Autodiagnóstico")
        print("2 - Visualizar informações do Autodiagnóstico")
        print("3 - Visualizar todos os Autodiagnósticos")
        print("4 - Atualizar Status do Autodiagnóstico")
        print("5 - Deletar Autodiagnóstico")
        print("6 - Exportar Autodiagnósticos para JSON")
        print("0 - Sair")
        verif_gerenc_op = input("\nSelecione uma opção: ")
        if not verif_gerenc_op.isdigit() or int(verif_gerenc_op) > 6 or int(verif_gerenc_op) < 0:
            print("\nSelecione uma opção válida.")
            continue
        verif_gerenc_op = int(verif_gerenc_op)
        if verif_gerenc_op == 0:
            break
        elif verif_gerenc_op == 1:
            placa_input = input("Qual a placa do veículo que irá ser diagnosticado?.....................: ")
            realizar_diagnostico(placa_input)
        elif verif_gerenc_op == 2:
            id_diagnostico = input("Qual o ID do diagnóstico que deseja visualizar?: ")
            read_diagnostico(id_diagnostico)
        elif verif_gerenc_op == 3:
            read_all_diagnosticos()
        elif verif_gerenc_op == 4:
            id_diagnostico = input("Qual o ID do diagnóstico que deseja atualizar o Status?: ")
            atualizar_status_diagnostico(id_diagnostico)
        elif verif_gerenc_op == 5:
            id_diagnostico = input("Qual o ID do diagnóstico que deseja deletar?: ")
            deletar_diagnostico(id_diagnostico)
        elif verif_gerenc_op == 6:
            exportar_diagnosticos_json()

# criação de um diagnóstico com a API de Diagnóstico ML
def realizar_diagnostico(placa):
    respostas = {}
    diagnostico = {}
    diagnostico_concluido = False
    try:
        if not verificar_veiculo(placa):
            raise ValueError('Veículo não encontrado.')
        placa = re.sub(r"[-]", "", placa)
        servicos = verificar_servicos()
    except ValueError as e:
        print(e)
    else:
        while True:
            for key, pergunta in perguntas.items():
                while True:
                    resposta_pergunta = input(pergunta).strip().upper()
                    if resposta_pergunta == "N" or resposta_pergunta == "S":
                        respostas[key] = 1 if resposta_pergunta == "S" else 0
                        break
                    else:
                        print("Escolha uma opção válida.")
            try:
                response_api = requests.post(url_api_diagnostico, json=respostas)
                response_api.raise_for_status()
                resultado_api = response_api.json()
                if resultado_api['diagnostico'] == "Nenhum problema encontrado" or resultado_api['diagnostico'] == "Problema não identificado":
                    print('\nNenhum problema foi identificado. Tente novamente especificando melhor os sintomas encontrados no carro.')
                    break
            except requests.exceptions.ConnectionError:
                print("\nNão foi possível conectar-se à API. Verifique se a API está em execução.")
                break
            print("\nEste foi o problema principal identificado pelo autodiagnóstico: \n")
            print(f"Problema: {resultado_api['diagnostico']}")
            print(f"Sintomas comuns: {', '.join(resultado_api['sintomas'])}")
            print(f"Solução: {resultado_api['solucao']}\n")
            while True:
                opt = input("Deseja gerar o diagnóstico completo ou deseja refazê-lo ('S' ou 'N')?: ")
                if opt.upper() == 'N':
                    respostas.clear()
                    print('\nRecomeçando Diagnóstico...\n')
                    break
                elif opt.upper() == 'S':
                    # Procura por um serviço correspondente
                    servico_encontrado = False
                    for i in range(len(servicos)):
                        if resultado_api['solucao'] == servicos[i][2]:
                            diagnostico['id_diagnostico'] = str(uuid.uuid4())
                            diagnostico['descricao_sintomas'] = ', '.join(resultado_api['sintomas'])
                            diagnostico['categoria_problema'] = resultado_api['diagnostico']
                            diagnostico['solucao'] = resultado_api['solucao']
                            diagnostico['status_diagnostico'] = "EM ANÁLISE"
                            diagnostico['veiculo_placa'] = placa
                            diagnostico['servico_id_servico'] = servicos[i][0]
                            servico_encontrado = True
                            break
                    if servico_encontrado:
                        with conectar() as conn:
                            cursor = conn.cursor()
                            try:
                                cursor.execute("""
                                    INSERT INTO diagnostico (id_diagnostico, descricao_sintomas, categoria_problema, solucao, status_diagnostico, veiculo_placa, servico_id_servico) 
                                    VALUES (:id_diagnostico, :descricao_sintomas, :categoria_problema, :solucao, :status_diagnostico, :veiculo_placa, :servico_id_servico)""", 
                                    diagnostico)
                                conn.commit()
                                print(f'\nDiagnóstico de ID {diagnostico["id_diagnostico"]} criado com sucesso! ✅​')
                                diagnostico_concluido = True
                            except oracledb.DatabaseError as e:
                                error, = e.args
                                print("\nErro ao gerar o Diagnóstico no SQL!")
                                print("Código do erro:", error.code)
                                print("Mensagem do erro:", error.message)
                                print("Contexto do erro:", error.context)
                            finally:
                                cursor.close()
                                break
                    else:
                        print('Nenhum serviço encontrado para o problema especificado.')
                        break
                else: 
                    print("Opção inválida.")
                    continue
            if diagnostico_concluido:
                print('\nRetornando ao menu de diagnóstico....')
                break

# visualizar informacoes do autodiagnostico feito
def read_diagnostico(id_diagnostico):
    try:
        if not verificar_diagnostico(id_diagnostico):
            raise ValueError("\nDiagnóstico não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_diagnostico, descricao_sintomas, categoria_problema, solucao, status_diagnostico, veiculo_placa, orcamento_id_orcamento, servico_id_servico FROM diagnostico WHERE id_diagnostico = :id_diagnostico", {"id_diagnostico": id_diagnostico})
                diagnostico_atual = cursor.fetchone()
    except ValueError as e:
        print(e)
    else:
        imprimir_diagnostico(diagnostico_atual)
        input("Pressione ENTER para voltar ao menu: ")
    finally:
        print("\nRetornando ao menu de diagnóstico...")

# visualiza todos os diagnósticos.
def read_all_diagnosticos():
    diagnosticos = select_registros("SELECT * FROM diagnostico")
    if diagnosticos:
        for diagnostico in diagnosticos:
                imprimir_diagnostico(diagnostico)
    else:
        print("\nNenhum registro encontrado de diagnóstico.\n")
    input("Pressione ENTER para voltar ao menu: ")
    print("\nRetornando ao menu de diagnóstico...") 

# imprime os dados do diagnóstico
def imprimir_diagnostico(diagnostico_atual):
    print(f"\n==============[ INFORMAÇÕES DO DIAGNÓSTICO DE ID {diagnostico_atual[0]} ]==============\n") 
    print(f"ID do diagnóstico.........: {diagnostico_atual[0]}")
    print(f"Categoria do Problema.....: {diagnostico_atual[2]}")
    print(f"Sintomas do Problema......: {diagnostico_atual[1]}")
    print(f"Solução...................: {diagnostico_atual[3]}")
    print(f"Status do Diagnóstico.....: {diagnostico_atual[4]}")
    print(f"ID do Serviço.............: {diagnostico_atual[7]}")
    print(f"Placa do veículo analisado: {diagnostico_atual[5]}")
    print(f"ID do Orçamento...........: {diagnostico_atual[6] if diagnostico_atual[6] else "Não Realizado"}\n")

# atualiza o status do diagnóstico
def atualizar_status_diagnostico(id_diagnostico):
    try:
        if not verificar_diagnostico(id_diagnostico):
            raise ValueError('\nDiagnóstico não encontrado.')
    except ValueError as e:
        print(e)
    else:
        with conectar() as conn:
            with conn.cursor() as cursor: 
                while True:
                    try:
                        status_diagnostico = input("Qual o novo Status do Diagnóstico ('EM ANÁLISE' ou 'ANALISADO')?: ").strip().upper()
                        if status_diagnostico == "EM ANÁLISE" or status_diagnostico == "ANALISADO":
                            cursor.execute("UPDATE diagnostico SET status_diagnostico = :status_diagnostico WHERE id_diagnostico = :id_diagnostico", {"status_diagnostico": status_diagnostico, "id_diagnostico": id_diagnostico})
                            conn.commit()
                            print('\nStatus atualizado com sucesso. ✅​')
                            print("\nRetornando ao menu de diagnóstico...") 
                            break
                        else:
                            raise ValueError('Opção inválida.')
                    except ValueError as e:
                        print(e) 
                        
# deleta o diagnostico a partir do ID
def deletar_diagnostico(id_diagnostico):
    try: 
        if not verificar_diagnostico(id_diagnostico):
            raise ValueError("\nDiagnóstico não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                while True:
                    op_delete = input(f"\nDeseja realmente remover o Diagnóstico de ID {id_diagnostico}? S ou N: ")
                    if op_delete.upper() != "S" and op_delete.upper() != "N":
                        print("\nDigite uma opção válida.")
                        continue
                    elif op_delete.upper() == "S":
                        cursor.execute("DELETE FROM diagnostico WHERE id_diagnostico = :id_diagnostico", {"id_diagnostico": id_diagnostico})
                        conn.commit()
                        print("\nDiagnóstico removido com sucesso. ✅​")
                        break
                    elif op_delete.upper() == "N":
                        print("\nO Diagnóstico não foi removido.")
                        break  
    except ValueError as e:
        print(e)
    finally:
        print("\nRetornando ao menu de diagnóstico...")

# exporta os registros de peças do banco de dados para JSON
def exportar_diagnosticos_json():
    try:
        if existem_registros("SELECT COUNT(1) FROM diagnostico") == False:
            raise ValueError("\nNenhuma diagnóstico cadastrado.")
        diagnosticos, colunas = select_registros("SELECT * FROM diagnostico", None, True)
        while True:
            export_opt = input("Deseja exportar os registros de diagnósticos para JSON? (S ou N): ").upper()
            if export_opt == 'S':
                diagnosticos_json = [dict(zip(colunas, diagnostico)) for diagnostico in diagnosticos]
                exportar_para_json(diagnosticos_json, 'diagnosticos.json')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de diagnóstico...')

# verifica existencia do diagnostico, retornando se existe ou n
def verificar_diagnostico(id_diagnostico):
    # busca o diagnostico pelo banco de dados
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM diagnostico WHERE id_diagnostico = :id_diagnostico", {"id_diagnostico": id_diagnostico})
        diagnostico_existe = cursor.fetchone()[0] > 0
        cursor.close()
        return diagnostico_existe

# retorna a peça caso exista pelo ID
def verificar_diagnostico_obter(id_diagnostico):
    # busca a diagnostico pelo banco de dados
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM diagnostico WHERE id_diagnostico = :id_diagnostico", {"id_diagnostico": id_diagnostico})
        peca = cursor.fetchone()
        cursor.close()
        return peca

# FUNÇÕES DO AUTOORÇAMENTO
# gerencia auto-orcamento
def gerenciar_orcamento():
    print("\nIniciando menu de gerenciamento de Auto-orçamento...") 
    while True:
        print("\n==============[ GERENCIAMENTO AUTO-ORÇAMENTO 💸 ]==============\n")
        print("1 - Realizar Auto-orçamento")
        print("2 - Visualizar informações do Auto-orçamento")
        print("3 - Visualizar todos os Auto-orçamentos")
        print("4 - Atualizar Status do Auto-orçamento")
        print("5 - Deletar Auto-orçamento")
        print("6 - Exportar Auto-orçamentos para JSON")
        print("0 - Sair")
        verif_gerenc_op = input("\nSelecione uma opção: ")
        if not verif_gerenc_op.isdigit() or int(verif_gerenc_op) > 6 or int(verif_gerenc_op) < 0:
            print("\nSelecione uma opção válida.")
            continue
        verif_gerenc_op = int(verif_gerenc_op)
        if verif_gerenc_op == 0:
            break
        elif verif_gerenc_op == 1:
            id_diagnostico = input("Qual o ID do diagnóstico que deseja realizar um auto-orçamento?: ")
            gerar_orcamento(id_diagnostico)
        elif verif_gerenc_op == 2:
            id_orcamento = input("Qual o ID do auto-orçamento que deseja visualizar?: ")
            read_orcamento(id_orcamento)
        elif verif_gerenc_op == 3:
            read_all_orcamentos()
        elif verif_gerenc_op == 4:
            id_orcamento = input("Qual o ID do auto-orçamento que deseja atualizar o status?: ")
            atualizar_status_orcamento(id_orcamento)
        elif verif_gerenc_op == 5:
            id_orcamento = input("Qual o ID do auto-orçamento que deseja deletar?: ")
            deletar_orcamento(id_orcamento)
        elif verif_gerenc_op == 6:
            exportar_orcamentos_json()

# auto-orçamento com base no pré-diagnóstico
def gerar_orcamento(id_diagnostico):
    orcamento = {}
    try:
        if not verificar_diagnostico(id_diagnostico):
            raise ValueError("Diagnóstico não encontrado.")
    except ValueError as e:
        print(e)
    else:
        orcamento['id_orcamento'] = str(uuid.uuid4())
        while True:
            try:
                descricao_orcamento = input("Digite a descrição do orçamento............................: ").strip()
                if not descricao_orcamento:
                    raise ValueError("Descrição vazia.")
                if len(descricao_orcamento) > 255:
                    raise ValueError("A descrição deve ter no máximo 255 caracteres.")
            except ValueError as e:
                print(e)
            else:
                orcamento['descricao_orcamento'] = descricao_orcamento
                print("Descrição registrada com sucesso.​")
                break
        orcamento['valor_total'] = verificar_servico_obter(verificar_diagnostico_obter(id_diagnostico)[7])[3]
        orcamento['status_orcamento'] = "APROVADO"

        with conectar() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO orcamento (id_orcamento, descricao_orcamento, valor_total, status_orcamento) 
                    VALUES (:id_orcamento, :descricao_orcamento, :valor_total, :status_orcamento)""", 
                    orcamento)
                cursor.execute("""
                    UPDATE diagnostico SET orcamento_id_orcamento = :id_orcamento WHERE id_diagnostico = :id_diagnostico
                    """, {"id_orcamento": orcamento['id_orcamento'], "id_diagnostico": id_diagnostico})
                conn.commit()
                print(f'\nAuto-orçamento criado com sucesso! ✅​ O ID do orçamento é {orcamento['id_orcamento']}') 
            except oracledb.DatabaseError as e:
                error, = e.args 
                print("\nErro ao gerar orçamento no SQL!")
                print("Código do erro:", error.code)
                print("Mensagem do erro:", error.message)
                print("Contexto do erro:", error.context)
            finally:
                cursor.close()
    finally:
        print("\nRetornando ao menu de orçamento...")

# visualiza auto-orcamento                   
def read_orcamento(id_orcamento):
    try:
        if not verificar_orcamento(id_orcamento):
            raise ValueError("\nOrçamento não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_orcamento, descricao_orcamento, valor_total, status_orcamento FROM orcamento WHERE id_orcamento = :id_orcamento", {"id_orcamento": id_orcamento})
                orcamento_atual = cursor.fetchone()
    except ValueError as e:
        print(e)
    else:
        imprimir_orcamento(orcamento_atual)
        input("Pressione ENTER para voltar ao menu: ")
    finally:
        print("\nRetornando ao menu de orçamento...")

# visualiza todos os orçamentos
def read_all_orcamentos():
    orcamentos = select_registros("SELECT * FROM orcamento")
    if orcamentos:
        for orcamento in orcamentos:
                imprimir_orcamento(orcamento)
    else:
        print("\nNenhum registro encontrado de orçamento.\n")
    input("Pressione ENTER para voltar ao menu: ")
    print("\nRetornando ao menu de orçamento...") 

# imprime um orçamento
def imprimir_orcamento(orcamento_atual):
        print(f"\n==============[ ORÇAMENTO DE ID {orcamento_atual[0]} ]==============\n")
        print(f"ID do Orçamento.......: {orcamento_atual[0]}")
        print(f"Descrição do Orçamento: {orcamento_atual[1]}")
        print(f"Valor.................: R${orcamento_atual[2]}")
        print(f"Status do Orçamento...: {orcamento_atual[3]}\n")
        
# atualiza o status do orçamento
def atualizar_status_orcamento(id_orcamento):
    try:
        if not verificar_orcamento(id_orcamento):
            raise ValueError('\nOrçamento não encontrado.')
    except ValueError as e:
        print(e)
    else:
        with conectar() as conn:
            with conn.cursor() as cursor: 
                while True:
                    try:
                        status_orcamento = input("Qual o novo Status do Orçamento ('PENDENTE' ou 'APROVADO' ou 'REJEITADO')?: ").strip().upper()
                        if status_orcamento == "PENDENTE" or status_orcamento == "APROVADO" or status_orcamento == 'REJEITADO':
                            cursor.execute("UPDATE orcamento SET status_orcamento = :status_orcamento WHERE id_orcamento = :id_orcamento", {"status_orcamento": status_orcamento, "id_orcamento": id_orcamento})
                            conn.commit()
                            print('\nStatus atualizado com sucesso. ✅​')
                            print("\nRetornando ao menu de orçamento...") 
                            break
                        else:
                            raise ValueError('Opção inválida.')
                    except ValueError as e:
                        print(e) 

# deleta o orcamento
def deletar_orcamento(id_orcamento):
    try: 
        if not verificar_orcamento(id_orcamento):
            raise ValueError("\nOrçamento não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                while True:
                    op_delete = input(f"\nDeseja realmente remover o Orçamento de ID {id_orcamento}? S ou N: ")
                    if op_delete.upper() != "S" and op_delete.upper() != "N":
                        print("\nDigite uma opção válida.")
                        continue
                    elif op_delete.upper() == "S":
                        cursor.execute("DELETE FROM orcamento WHERE id_orcamento = :id_orcamento", {"id_orcamento": id_orcamento})
                        conn.commit()
                        print("\nOrçamento removido com sucesso. ✅​")
                        break
                    elif op_delete.upper() == "N":
                        print("\nO Orçamento não foi removido.")
                        break  
    except ValueError as e:
        print(e)
    finally:
        print("\nRetornando ao menu de Orçamento...")

# exporta os orcamentos para JSON
def exportar_orcamentos_json():
    try:
        if existem_registros("SELECT COUNT(1) FROM orcamento") == False:
            raise ValueError("\nNenhuma diagnóstico cadastrado.")
        orcamentos, colunas = select_registros("SELECT * FROM orcamento", None, True)
        while True:
            export_opt = input("Deseja exportar os registros de orçamentos para JSON? (S ou N): ").upper()
            if export_opt == 'S':
                orcamentos_json = [dict(zip(colunas, orcamento)) for orcamento in orcamentos]
                exportar_para_json(orcamentos_json, 'orcamentos.json')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de diagnóstico...')

# verifica existencia do autoorçamento
def verificar_orcamento(id_orcamento):
    # busca o orcamento pelo banco de dados
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM orcamento WHERE id_orcamento = :id_orcamento", {"id_orcamento": id_orcamento})
        orcamento_existe = cursor.fetchone()[0] > 0
        cursor.close()
        return orcamento_existe

# FUNÇÕES FORNECE
# gerencia relação fornece (servico e peca)
def gerenciar_fornece():
    print("\nIniciando menu de gerenciamento de Fornece...") 
    while True:
        print("\n==============[ GERENCIAMENTO RELAÇÃO SERVIÇO-PEÇA (FORNECE) ]==============\n")
        print("1 - Criar Relação Serviço-Peça")
        print("2 - Visualizar Serviços associados a determinada Peça")
        print("3 - Visualizar Peças associadas a determinado Serviço")
        print("4 - Deletar Relação Serviço-Peça")
        print("5 - Exportar Relações de Fornece para JSON")
        print("0 - Sair")
        verif_gerenc_op = input("\nSelecione uma opção: ")
        if not verif_gerenc_op.isdigit() or int(verif_gerenc_op) > 5 or int(verif_gerenc_op) < 0:
            print("\nSelecione uma opção válida.")
            continue
        verif_gerenc_op = int(verif_gerenc_op)
        if verif_gerenc_op == 0:
            break
        elif verif_gerenc_op == 1:
            criar_fornece()
        elif verif_gerenc_op == 2:
            id_peca = input("Qual o ID da peça que deseja visualizar os serviços atrelados? (formato: PXXXXX): ")
            read_servicos_peca(id_peca)
        elif verif_gerenc_op == 3:
            id_servico = input("Qual o ID do serviço que deseja visualizar as peças atreladas? (formato: SXXXXX): ")
            read_pecas_servico(id_servico)
        elif verif_gerenc_op == 4:
            deletar_fornece()
        elif verif_gerenc_op == 5:
            exportar_fornece_json()

# cria uma relação de uma peça com um serviço
def criar_fornece():
    try:
        verificar_servicos_pecas()
        while True:
            try:
                id_servico = input("Qual o ID do serviço? (formato: SXXXXX. Ex: S00001): ")
                if verificar_servico(id_servico) == False:
                    raise ValueError("Nenhum serviço encontrado com o ID especificado.")
            except ValueError as e:
                print(e)
            else:
                break
        while True:
            try:
                id_peca = input("Qual o ID da peça? (formato: PXXXXX. Ex: P00002): ")
                if verificar_peca(id_peca) == False:
                    raise ValueError("Nenhuma peça encontrada com o ID especificado.")
            except ValueError as e:
                print(e)
            else: 
                break
        if verificar_fornece_existe(id_peca, id_servico):
            raise ValueError('\nAssociação já existe.')
        
        with conectar() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO fornece (peca_id_peca, servico_id_servico) 
                    VALUES (:id_peca, :id_servico)""", 
                    {"id_peca": id_peca, "id_servico": id_servico})
                conn.commit()
                print(f"\nRelação entre {id_peca} e {id_servico} cadastrada com sucesso! ✅") 
            except oracledb.DatabaseError as e:
                error, = e.args 
                print("\nErro ao cadastrar a Relação Fornece no SQL!")
                print("Código do erro:", error.code)
                print("Mensagem do erro:", error.message)
                print("Contexto do erro:", error.context)
            finally:
                cursor.close()  
    except ValueError as e:
        print(e) 

# buscas os serviços relacionados a determinada peça
def read_servicos_peca(id_peca):
    try:
        if not verificar_peca(id_peca):
            raise ValueError("\nPeça não encontrada.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT servico_id_servico FROM fornece WHERE peca_id_peca = :id_peca", {"id_peca": id_peca})
                servicos = cursor.fetchall()
    except ValueError as e:
        print(e)
    else:
        if servicos:
            print(f"\n==============[ SERVIÇOS RELACIONADOS A PEÇA DE ID {id_peca} ]==============") 
            for servico_id in servicos:
                servico_obtido = verificar_servico_obter(servico_id[0])
                imprimir_servico(servico_obtido)
        else:
            print("\nNenhum serviço relacionado a peça informada.\n")
        input("Pressione ENTER para voltar ao menu: ")
    finally:
        print("\nRetornando ao menu de Fornece...")

# busca as peças relacionadas a determinado serviço
def read_pecas_servico(id_servico):
    try:
        if not verificar_servico(id_servico):
            raise ValueError("\nServiço não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT peca_id_peca FROM fornece WHERE servico_id_servico = :id_servico", {"id_servico": id_servico})
                pecas = cursor.fetchall()
    except ValueError as e:
        print(e)
    else:
        if pecas:
            print(f"\n==============[ PEÇAS RELACIONADAS AO SERVIÇO DE ID {id_servico} ]==============") 
            for peca_id in pecas:
                peca_obtida = verificar_peca_obter(peca_id[0])
                imprimir_peca(peca_obtida)
        else:
            print("\nNenhuma peça relacionada ao serviço informado.\n")
        input("Pressione ENTER para voltar ao menu: ")
    finally:
        print("\nRetornando ao menu de Fornece...")

# deleta uma relação Fornece
def deletar_fornece():
    try:
        verificar_servicos_pecas()
        while True:
            try:
                id_servico = input("Qual o ID do serviço? (formato: SXXXXX. Ex: S00001): ")
                if verificar_servico(id_servico) == False:
                    raise ValueError("Nenhum serviço encontrado com o ID especificado.")
            except ValueError as e:
                print(e)
            else:
                break
        while True:
            try:
                id_peca = input("Qual o ID da peça? (formato: PXXXXX. Ex: P00002): ")
                if verificar_peca(id_peca) == False:
                    raise ValueError("Nenhuma peça encontrada com o ID especificado.")
            except ValueError as e:
                print(e)
            else: 
                break
        if verificar_fornece_existe(id_peca, id_servico) == False:
            raise ValueError('\nAssociação inexistente.')
        with conectar() as conn:
            with conn.cursor() as cursor:
                while True:
                    op_delete = input(f"\nDeseja realmente deletar a relação entre {id_peca} e {id_servico}? S ou N: ")
                    if op_delete.upper() != "S" and op_delete.upper() != "N":
                        print("\nDigite uma opção válida.")
                        continue
                    elif op_delete.upper() == "S":
                        cursor.execute("DELETE FROM fornece WHERE peca_id_peca = :id_peca and servico_id_servico = :id_servico", {"id_peca": id_peca, "id_servico": id_servico})
                        conn.commit()
                        print("\nRelação removida com sucesso. ✅")
                        break
                    elif op_delete.upper() == "N":
                        print("\nRelação não foi removida.")
                        break
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de Fornece.....')

# verifica se existem serviços e peças no BD
def verificar_servicos_pecas():
    servicos = select_registros('SELECT * FROM servico order by 1')
    pecas = select_registros('SELECT * FROM peca order by 1')
    if servicos and pecas:
        return servicos, pecas
    else: 
        raise ValueError('É necessário ao menos 1 serviço e 1 peça para criar a relação.')

# verifica se a relação entre uma peça e um serviço já existe.
def verificar_fornece_existe(id_peca, id_servico):
    associacao = select_registros('SELECT * FROM fornece WHERE peca_id_peca = :peca_id_peca AND servico_id_servico = :servico_id_servico', {"peca_id_peca": id_peca, "servico_id_servico": id_servico})
    if associacao:
        return True
    return False

# exporta as relações de Fornece para JSON
def exportar_fornece_json():
    try:
        if existem_registros("SELECT COUNT(1) FROM fornece") == False:
            raise ValueError("\nNenhuma relação de Fornece cadastrada.")
        fornecem, colunas = select_registros("SELECT * FROM fornece", None, True)
        while True:
            export_opt = input("Deseja exportar os registros de relação Fornece para JSON? (S ou N): ").upper()
            if export_opt == 'S':
                fornecem_json = [dict(zip(colunas, fornece)) for fornece in fornecem]
                exportar_para_json(fornecem_json, 'fornecem.json')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de Fornece...')

# FUNÇÕES OFERECE
# gerencia relação oferece (servico e centro)
def gerenciar_oferece():
    print("\nIniciando menu de gerenciamento de Oferece...") 
    while True:
        print("\n==============[ GERENCIAMENTO RELAÇÃO SERVIÇO-CENTRO (OFERECE) ]==============\n")
        print("1 - Criar Relação Serviço-Centro")
        print("2 - Visualizar Serviços associados a determinado Centro")
        print("3 - Visualizar Centros associados a determinado Serviço")
        print("4 - Deletar Relação Serviço-Centro")
        print("5 - Exportar Relações de Oferece para JSON")
        print("0 - Sair")
        verif_gerenc_op = input("\nSelecione uma opção: ")
        if not verif_gerenc_op.isdigit() or int(verif_gerenc_op) > 5 or int(verif_gerenc_op) < 0:
            print("\nSelecione uma opção válida.")
            continue
        verif_gerenc_op = int(verif_gerenc_op)
        if verif_gerenc_op == 0:
            break
        elif verif_gerenc_op == 1:
            criar_oferece()
        elif verif_gerenc_op == 2:
            id_centro = input("Qual o ID do centro que deseja visualizar os serviços atrelados? (formato: CXXX): ")
            read_servicos_centro(id_centro)
        elif verif_gerenc_op == 3:
            id_servico = input("Qual o ID do serviço que deseja visualizar os centros atrelados? (formato: SXXXXX): ")
            read_centros_servico(id_servico)
        elif verif_gerenc_op == 4:
            deletar_oferece()
        elif verif_gerenc_op == 5:
            exportar_oferece_json()

# cria uma relação de um serviço com um centro
def criar_oferece():
    try:
        verificar_servicos_centros()
        while True:
            try:
                id_servico = input("Qual o ID do serviço? (formato: SXXXXX. Ex: S00001): ")
                if verificar_servico(id_servico) == False:
                    raise ValueError("Nenhum serviço encontrado com o ID especificado.")
            except ValueError as e:
                print(e)
            else:
                break
        while True:
            try:
                id_centro = input("Qual o ID do centro automotivo? (formato: CXXX. Ex: C001): ")
                if verificar_centro(id_centro) == False:
                    raise ValueError("Nenhuma peça encontrada com o ID especificado.")
            except ValueError as e:
                print(e)
            else: 
                break
        if verificar_oferece_existe(id_servico, id_centro):
            raise ValueError('\nAssociação já existe.')
        
        with conectar() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO oferece (servico_id_servico, centro_automotivo_id_centro) 
                    VALUES (:id_servico, :id_centro)""", 
                    {"id_servico": id_servico, "id_centro": id_centro})
                conn.commit()
                print(f"\nRelação entre {id_servico} e {id_centro} cadastrada com sucesso! ✅") 
            except oracledb.DatabaseError as e:
                error, = e.args 
                print("\nErro ao cadastrar a Relação Oferece no SQL!")
                print("Código do erro:", error.code)
                print("Mensagem do erro:", error.message)
                print("Contexto do erro:", error.context)
            finally:
                cursor.close()  
    except ValueError as e:
        print(e) 

# imprime os serviços relacionados a X centro
def read_servicos_centro(id_centro):
    try:
        if not verificar_centro(id_centro):
            raise ValueError("\n Centro Automotivo não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT servico_id_servico FROM oferece WHERE centro_automotivo_id_centro = :id_centro", {"id_centro": id_centro})
                servicos = cursor.fetchall()
    except ValueError as e:
        print(e)
    else:
        if servicos:
            print(f"\n==============[ SERVIÇOS RELACIONADOS AO CENTRO AUTOMOTIVO DE ID {id_centro} ]==============") 
            for servico_id in servicos:
                servico_obtido = verificar_servico_obter(servico_id[0])
                imprimir_servico(servico_obtido)
        else:
            print("\nNenhum serviço relacionado ao centro informado.\n")
        input("Pressione ENTER para voltar ao menu: ")
    finally:
        print("\nRetornando ao menu de Oferece...")

# imprime os centros relacionados a X serviço
def read_centros_servico(id_servico):
    try:
        if not verificar_servico(id_servico):
            raise ValueError("\nServiço não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT centro_automotivo_id_centro FROM oferece WHERE servico_id_servico = :id_servico", {"id_servico": id_servico})
                centros = cursor.fetchall()
    except ValueError as e:
        print(e)
    else:
        if centros:
            print(f"\n==============[ CENTROS RELACIONADOS AO SERVIÇO DE ID {id_servico} ]==============") 
            for centro_id in centros:
                centro_obtida = verificar_centro_obter(centro_id[0])
                imprimir_centro(centro_obtida)
        else:
            print("\nNenhum centro relacionado ao serviço informado.\n")
        input("Pressione ENTER para voltar ao menu: ")
    finally:
        print("\nRetornando ao menu de Oferece...")

# deleta uma relação Oferece
def deletar_oferece():
    try:
        verificar_servicos_centros()
        while True:
            try:
                id_servico = input("Qual o ID do serviço? (formato: SXXXXX. Ex: S00001): ")
                if verificar_servico(id_servico) == False:
                    raise ValueError("Nenhum serviço encontrado com o ID especificado.")
            except ValueError as e:
                print(e)
            else:
                break
        while True:
            try:
                id_centro = input("Qual o ID do centro automotivo? (formato: CXXX. Ex: C001): ")
                if verificar_centro(id_centro) == False:
                    raise ValueError("Nenhum centro encontrado com o ID especificado.")
            except ValueError as e:
                print(e)
            else: 
                break
        if verificar_oferece_existe(id_servico, id_centro) == False:
            raise ValueError('\nAssociação inexistente.')
        with conectar() as conn:
            with conn.cursor() as cursor:
                while True:
                    op_delete = input(f"\nDeseja realmente deletar a relação entre {id_servico} e {id_centro}? S ou N: ")
                    if op_delete.upper() != "S" and op_delete.upper() != "N":
                        print("\nDigite uma opção válida.")
                        continue
                    elif op_delete.upper() == "S":
                        cursor.execute("DELETE FROM oferece WHERE servico_id_servico = :id_servico and centro_automotivo_id_centro = :id_centro", {"id_servico": id_servico, "id_centro": id_centro})
                        conn.commit()
                        print("\nRelação removida com sucesso. ✅")
                        break
                    elif op_delete.upper() == "N":
                        print("\nRelação não foi removida.")
                        break
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de Oferece.....')

# verifica se existem serviços e centros no BD
def verificar_servicos_centros():
    servicos = select_registros('SELECT * FROM servico order by 1')
    centros = select_registros('SELECT * FROM centro_automotivo order by 1')
    if servicos and centros:
        return servicos, centros
    else: 
        raise ValueError('É necessário ao menos 1 serviço e 1 centro automotivo para criar a relação.')

# verifica se a relação entre um centro e um serviço já existe.
def verificar_oferece_existe(id_servico, id_centro):
    associacao = select_registros('SELECT * FROM oferece WHERE servico_id_servico = :servico_id_servico AND centro_automotivo_id_centro = :centro_automotivo_id_centro', {"servico_id_servico": id_servico, "centro_automotivo_id_centro": id_centro})
    if associacao:
        return True
    return False

# exporta as relações de oferece para JSON
def exportar_oferece_json():
    try:
        if existem_registros("SELECT COUNT(1) FROM oferece") == False:
            raise ValueError("\nNenhuma relação de Oferece cadastrada.")
        oferecem, colunas = select_registros("SELECT * FROM oferece", None, True)
        while True:
            export_opt = input("Deseja exportar os registros de relação Oferece para JSON? (S ou N): ").upper()
            if export_opt == 'S':
                oferecem_json = [dict(zip(colunas, oferece)) for oferece in oferecem]
                exportar_para_json(oferecem_json, 'oferecem.json')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de Oferece...')

# menu inicial
while True:
    print("\n==============[ MENU DO SISTEMA 🟦 ⬜ ]==============\n")
    print("1  - Gerenciar Usuários 🚹​")
    print("2  - Gerenciar Veículos 🚗")
    print("3  - Gerenciar Agendamentos 🕒") 
    print("4  - Gerenciar Peças 🔧​")
    print("5  - Gerenciar Centros Automotivos 🏪​")
    print("6  - Gerenciar Cargos 📩​")
    print("7  - Gerenciar Funcionários 🧑‍💼") 
    print("8  - Gerenciar Serviços ⚙️​") 
    print("9  - Gerenciar Autodiagnósticos 🩺​") 
    print("10 - Gerenciar Auto-orçamentos 💸​") 
    print("11 - Gerenciar Relacionamento Serviço-Peça (FORNECE)") 
    print("12 - Gerenciar Relacionamento Serviço-Centro (OFERECE)") 
    print("0  - Sair 🚪🏃 \n")
    option = input("Opção: ")
    if not option.isdigit() or (int(option) > 12 or int(option) < 0):
        print("\nSelecione uma opção válida.")
        continue
    option = int(option)
    if option == 0:
        print("\nSolicitação encerrada.\n")
        break
    elif option == 1:
        gerenciar_usuario()
    elif option == 2:
        gerenciar_veiculo()      
    elif option == 3:
        gerenciar_agendamento()    
    elif option == 4:
        gerenciar_pecas()   
    elif option == 5:
        gerenciar_centro()
    elif option == 6:
        gerenciar_cargo()
    elif option == 7:
        gerenciar_funcionario()
    elif option == 8:
        gerenciar_servico()
    elif option == 9:
        gerenciar_autodiagnostico()
    elif option == 10:
        gerenciar_orcamento()
    elif option == 11:
        gerenciar_fornece()
    elif option == 12:
        gerenciar_oferece()
        
        