import sys
import bcrypt
import sqlite3
import os
import pandas as pd
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox, QLineEdit, QComboBox, QFormLayout, QTableWidget, QTableWidgetItem, QDialog, QListWidget, QInputDialog, QCheckBox, QHeaderView, QAbstractItemView, QDesktopWidget, QFileDialog, QHBoxLayout
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QColor, QIcon
from datetime import datetime, timedelta

def get_database_path():
    """Garante que o banco de dados esteja acessível diretamente do diretório de instalação."""
    # Caminho absoluto do banco de dados
    packaged_db_path = "C:/Program Files (x86)/Controle de Vendas Fabio Pipas & RBShop/banco_de_dados/sistema_vendas.db"
    alternative_db_path = "C:/Program Files/Controle de Vendas Fabio Pipas & RBShop/banco_de_dados/sistema_vendas.db"

    print(f"Packaged DB Path: {packaged_db_path}")

    # Verifica se o banco de dados existe no caminho original
    if os.path.exists(packaged_db_path):
        return packaged_db_path  # Retorna o caminho original se existir

    # Se não existir, verifica o caminho alternativo
    print(f"Verificando caminho alternativo: {alternative_db_path}")
    if os.path.exists(alternative_db_path):
        return alternative_db_path  # Retorna o caminho alternativo se existir

    # Se nenhum dos caminhos existir, exibe uma mensagem de erro
    print("Erro: O banco de dados não foi encontrado em nenhum dos caminhos especificados.")
    QMessageBox.critical(None, "Erro", "O banco de dados não foi encontrado em nenhum dos caminhos especificados.")
    return None  # Retorna None se o banco de dados não existir em nenhum dos caminhos

def resource_path(relative_path):
    """Obtem o caminho absoluto para um recurso, funciona para desenvolvimento e executável."""
    try:
        # PyInstaller cria um caminho temporário para o executável
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

import os
import shutil
from PyQt5.QtWidgets import QMessageBox

def backup_database():
    """Faz um backup do banco de dados, sobrescrevendo o backup anterior se existir."""
    # Caminho do banco de dados original
    db_path_x86 = os.path.join("C:\\", "Program Files (x86)", "Controle de Vendas Fabio Pipas & RBShop", "banco_de_dados", "sistema_vendas.db")
    db_path = os.path.join("C:\\", "Program Files", "Controle de Vendas Fabio Pipas & RBShop", "banco_de_dados", "sistema_vendas.db")
    
    # Caminho do diretório de backup
    backup_dir = os.path.join(os.path.expanduser("~"), "backup_banco_dados")
    
    # Cria o diretório de backup se não existir
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Nome do arquivo de backup
    backup_file = os.path.join(backup_dir, "sistema_vendas_backup.db")

    try:
        # Inicializa a variável db_path como None
        db_path_to_use = None

        # Verifica se o banco de dados existe no caminho x86
        print(f"Verificando caminho x86: {db_path_x86}")
        if os.path.exists(db_path_x86):
            db_path_to_use = db_path_x86  # Usa o caminho x86 se existir
            print(f"Banco de dados encontrado em: {db_path_x86}")
        else:
            print(f"Banco de dados não encontrado em: {db_path_x86}")

        # Verifica se o banco de dados existe no caminho alternativo
        print(f"Verificando caminho alternativo: {db_path}")
        if os.path.exists(db_path):
            db_path_to_use = db_path  # Usa o caminho alternativo se existir
            print(f"Banco de dados encontrado em: {db_path}")
        else:
            print(f"Banco de dados não encontrado em: {db_path}")

        # Se nenhum dos caminhos for encontrado, levanta uma exceção
        if db_path_to_use is None:
            raise FileNotFoundError("O banco de dados não foi encontrado em nenhum dos caminhos especificados.")

        # Se o arquivo de backup já existir, exclua-o
        if os.path.exists(backup_file):
            os.remove(backup_file)
            print(f"Backup anterior removido: {backup_file}")

        # Copia o banco de dados para o diretório de backup
        shutil.copy(db_path_to_use, backup_file)
        print(f"Backup realizado com sucesso: {backup_file}")
    except Exception as e:
        print(f"Erro ao realizar backup: {e}")
        QMessageBox.critical(None, "Erro", f"Erro ao realizar backup: {e}")

class PasswordToggleButton(QPushButton):
    def __init__(self, input_field):
        super().__init__("👁")
        self.setCheckable(True)
        self.input_field = input_field

    def mousePressEvent(self, event):
        if event.button() == 1:  # Botão esquerdo do mouse
            self.input_field.setEchoMode(QLineEdit.Normal)
            self.setText("🙈")  # Muda o ícone para indicar que a senha está visível
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == 1:  # Botão esquerdo do mouse
            self.input_field.setEchoMode(QLineEdit.Password)
            self.setText("👁")  # Muda o ícone de volta para ocultar a senha
        super().mouseReleaseEvent(event)

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 300, 200)

        # Definindo o ícone da janela
        icon_path = resource_path("imagens/logoprincipal.ico")  # Caminho para o ícone
        self.setWindowIcon(QIcon(icon_path))  # Define o ícone da janela

        self.centralizar_janela()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label_username = QLabel("Usuário:")
        self.layout.addWidget(self.label_username)

        self.input_username = QLineEdit()
        self.layout.addWidget(self.input_username)

        self.label_password = QLabel("Senha:")
        self.layout.addWidget(self.label_password)

        # Layout horizontal para o campo de senha e o botão
        self.password_layout = QHBoxLayout()
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.password_layout.addWidget(self.input_password)

        # Botão para mostrar/ocultar senha
        self.btn_toggle_password = PasswordToggleButton(self.input_password)
        self.password_layout.addWidget(self.btn_toggle_password)

        self.layout.addLayout(self.password_layout)

        self.btn_login = QPushButton("Login")
        self.btn_login.clicked.connect(self.login)
        self.layout.addWidget(self.btn_login)

        self.btn_register = QPushButton("Cadastrar")
        self.btn_register.clicked.connect(self.open_registration)
        self.layout.addWidget(self.btn_register)

        # Conectar o pressionar Enter para login
        self.input_password.returnPressed.connect(self.login)
        self.input_username.returnPressed.connect(self.login)

    def centralizar_janela(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)

    def login(self):
        username = self.input_username.text()
        password = self.input_password.text()

        if self.verificar_login(username, password):
            QMessageBox.information(self, "Sucesso", "Login realizado com sucesso!")
            self.open_vendas()
            self.clear_fields()  # Limpa os campos após login bem-sucedido
            self.close()
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha incorretos.")
            self.clear_fields()  # Limpa os campos após erro de login

    def clear_fields(self):
        self.input_username.clear()
        self.input_password.clear()

    def verificar_login(self, username, password):
        conn = None  # Inicializa a variável conn
        try:
            conn = sqlite3.connect(get_database_path())
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM usuarios WHERE username = ?", (username,))
            user = cursor.fetchone()
            if user is not None:
                if bcrypt.checkpw(password.encode('utf-8'), user[0]):
                    return True
                else:
                    print("Senha incorreta.")
                    return False
            else:
                print("Usuário não encontrado.")
                return False
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro de Banco de Dados", f"Erro ao acessar o banco de dados: {e}")
            print(f"Erro: {e}")  # Exibe o erro no console
            return False
        finally:
            if conn is not None:
                conn.close()  # Fecha a conexão se ela foi aberta


    def open_registration(self):
        self.registration_window = RegistrationWindow(self)
        self.registration_window.show()
        self.close()

    def open_vendas(self):
        try:
            self.vendas_window = SistemaVendas()
            self.vendas_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao abrir a janela de vendas: {e}")

class RegistrationWindow(QMainWindow):
    def __init__(self, login_window):
        super().__init__()
        self.setWindowTitle("Cadastro")
        self.setGeometry(300, 300, 300, 200)

        # Definindo o ícone da janela
        icon_path = resource_path("imagens/logoprincipal.ico")  # Caminho para o ícone
        self.setWindowIcon(QIcon(icon_path))  # Define o ícone da janela

        # Centraliza a janela na tela
        self.centralizar_janela()

        self.login_window = login_window  # Armazena a referência da janela de login

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label_username = QLabel("Usuário:")
        self.layout.addWidget(self.label_username)

        self.input_username = QLineEdit()
        self.layout.addWidget(self.input_username)

        self.label_password = QLabel("Senha:")
        self.layout.addWidget(self.label_password)

        # Layout horizontal para o campo de senha e o botão
        self.password_layout = QHBoxLayout()
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.password_layout.addWidget(self.input_password)

        # Botão para mostrar/ocultar senha
        self.btn_toggle_password = PasswordToggleButton(self.input_password)
        self.password_layout.addWidget(self.btn_toggle_password)

        self.layout.addLayout(self.password_layout)

        self.btn_register = QPushButton("Cadastrar")
        self.btn_register.clicked.connect(self.register)
        self.layout.addWidget(self.btn_register)

    def centralizar_janela(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)

    def register(self):
        username = self.input_username.text()
        password = self.input_password.text()

        # Validação do comprimento do nome de usuário e da senha
        if len(username) < 5:
            QMessageBox.warning(self, "Erro", "O nome de usuário deve ter pelo menos 5 caracteres.")
            return

        if len(password) < 5:
            QMessageBox.warning(self, "Erro", "A senha deve ter pelo menos 5 caracteres.")
            return

        if self.cadastrar_usuario(username, password):
            QMessageBox.information(self, "Sucesso", "Cadastro realizado com sucesso!")
            backup_database()
            self.close()  # Fecha a janela de cadastro ao finalizar o cadastro
            self.login_window.show()  # Reabre a janela de login
        else:
            QMessageBox.warning(self, "Erro", "Erro ao cadastrar o usuário.")

    def cadastrar_usuario(self, username, password):
        conn = None  # Inicializa a variável conn
        try:
            conn = sqlite3.connect(get_database_path())
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
            if cursor.fetchone() is not None:
                return False  # Usuário já existe

            # Criptografa a senha
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insere o novo usuário no banco de dados
            cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            return True
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro de Banco de Dados", f"Erro ao acessar o banco de dados: {e}")
            return False
        finally:
            if conn is not None:
                conn.close()  # Fecha a conexão se ela foi aberta

    def closeEvent(self, event):
        self.login_window.show()  # Reabre a janela de login ao fechar a janela de cadastro
        backup_database()
        event.accept()

class SistemaVendas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fabio Pipas & RBHookah")
        self.setGeometry(100, 100, 800, 600)

        # Definindo o ícone da janela
        icon_path = resource_path('imagens/logoprincipal.ico')  # Caminho para o ícone
        self.setWindowIcon(QIcon(icon_path))  # Define o ícone da janela

        # Centraliza a janela na tela
        self.centralizar_janela()
        
        self.conectar_banco()

        layout = QVBoxLayout()
        
        self.label = QLabel("\nBem-vindo ao Sistema de Vendas Fabio Pipas & RBHookah\n")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

       # Adicionando o logo
        self.logo_label = QLabel()
        # Usando um caminho relativo para a imagem do logo
        logo_path = resource_path("imagens/logoprincipal.png")  # Usando a função resource_path
        self.logo_pixmap = QPixmap(logo_path)

        # Verifica se a imagem foi carregada corretamente
        if self.logo_pixmap.isNull():
            QMessageBox.warning(self, "Erro", "Não foi possível carregar a imagem do logo.")
        else:
            self.logo_label.setPixmap(self.logo_pixmap)
            self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Adicionando uma borda arredondada ao QLabel
            self.logo_label.setStyleSheet("border: 4px solid black; border-radius: 10px;")  # Altere a cor, espessura e raio conforme necessário

            layout.addWidget(self.logo_label)
        
        self.btn_vendas = QPushButton("Registrar Venda")
        self.btn_vendas.clicked.connect(self.abrir_tela_venda)
        layout.addWidget(self.btn_vendas)
        
        self.btn_estoque = QPushButton("Gerenciar Estoque")
        self.btn_estoque.clicked.connect(self.abrir_tela_estoque)
        layout.addWidget(self.btn_estoque)
        
        self.btn_clientes = QPushButton("Gerenciar Clientes")
        self.btn_clientes.clicked.connect(self.abrir_tela_clientes)  # Conectar o botão
        layout.addWidget(self.btn_clientes)
        
        self.btn_relatorios = QPushButton("Gerar Relatórios")
        self.btn_relatorios.clicked.connect(self.abrir_tela_relatorios)  # Conectar o botão de relatórios
        layout.addWidget(self.btn_relatorios)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.adjustSize()  # Ajusta o tamanho da janela com base no conteúdo
        self.centralizar_janela()  # Centraliza a janela após ajustar o tamanho

    def centralizar_janela(self):
        # Obtém a geometria da tela
        screen = QDesktopWidget().screenGeometry()
        # Obtém a geometria da janela
        size = self.geometry()
        # Calcula a nova posição da janela
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        # Move a janela para a nova posição
        self.move(x, y)
    
    def conectar_banco(self):
        self.conn = sqlite3.connect(get_database_path())
        self.cursor = self.conn.cursor()
        
        # Criar tabela de clientes
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
        """)
        
        # Criar tabela de vendas com a nova coluna cliente
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            valor REAL NOT NULL,
            pagamento TEXT NOT NULL,
            cliente TEXT  -- Adicionando a coluna cliente
        )
        """)
        
        # Criar tabela de estoque com a nova coluna categoria
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL UNIQUE,
            categoria TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL
        )
        """)
        
        # Adicionar a coluna categoria se a tabela já existir
        try:
            self.cursor.execute("ALTER TABLE estoque ADD COLUMN categoria TEXT")
        except sqlite3.OperationalError:
            pass  # A coluna já existe, não faz nada

        self.conn.commit()

        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS pagamentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente TEXT NOT NULL,
                    produto TEXT NOT NULL,
                    quantidade INTEGER NOT NULL,
                    data_pagamento DATE NOT NULL
                )
            """)
            self.conn.commit()  
        except Exception as e:
            print(f"Erro ao criar tabela: {e}")

    # Criar tabela de vendas com a nova coluna cliente e coluna pago
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            valor REAL NOT NULL,
            pagamento TEXT NOT NULL,
            cliente TEXT,
            pago INTEGER DEFAULT 0  -- Adicionando a coluna pago
        )
        """)
        # Adicionar a coluna pago se não existir
        try:
            self.cursor.execute("ALTER TABLE vendas ADD COLUMN pago INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass  # A coluna já existe, não faz nada
    
    def abrir_tela_venda(self):
        self.tela_venda = TelaVenda(self.conn)
        self.tela_venda.show()
    
    def abrir_tela_estoque(self):
        self.tela_estoque = TelaEstoque(self.conn)
        self.tela_estoque.show()

    def abrir_tela_relatorios(self):
        self.tela_relatorios = TelaRelatorios(self.conn)
        self.tela_relatorios.show()

    def abrir_tela_clientes(self):  # Função para abrir a tela de gerenciamento de clientes
        self.tela_clientes = TelaGerenciarClientes(self.conn)
        self.tela_clientes.show()

    def closeEvent(self, event):
        # Chama a função de backup antes de fechar
        backup_database()
        QMessageBox.information(self, "Backup", "Backup do banco de dados realizado com sucesso.")
        self.conn.close()  # Fecha a conexão com o banco de dados
        event.accept()  # Aceita o evento de fechamento

class TelaVenda(QMainWindow):
    def __init__(self, conn):
        super().__init__()
        self.setWindowTitle("Registrar Venda")
        self.setGeometry(150, 150, 400, 400)

        # Definindo o ícone da janela
        icon_path = resource_path('imagens/logoprincipal.ico')  # Caminho para o ícone
        self.setWindowIcon(QIcon(icon_path))  # Define o ícone da janela

        # Centraliza a janela na tela
        self.centralizar_janela()

        self.conn = conn
        self.cursor = self.conn.cursor()
        self.carrinho = []
        
        layout = QVBoxLayout()
        
        # Label para Categoria
        self.label_categoria = QLabel("Selecione a Categoria:")
        layout.addWidget(self.label_categoria)
        
        self.combo_categoria = QComboBox()
        self.combo_categoria.currentIndexChanged.connect(self.carregar_produtos_por_categoria)  # Conectar o evento
        layout.addWidget(self.combo_categoria)
        
        # Label para Produto
        self.label_produto = QLabel("Selecione o Produto:")
        layout.addWidget(self.label_produto)
        
        self.combo_produto = QComboBox()  # Inicializa o combo_produto aqui
        layout.addWidget(self.combo_produto)
        
        self.label_quantidade_disponivel = QLabel("Quantidade Disponível: 0")
        layout.addWidget(self.label_quantidade_disponivel)
        
        # Label para Quantidade
        self.label_quantidade = QLabel("\nQuantidade:")
        layout.addWidget(self.label_quantidade)
        
        self.input_quantidade = QLineEdit()
        layout.addWidget(self.input_quantidade)
        
        self.btn_adicionar = QPushButton("Adicionar ao Carrinho")
        self.btn_adicionar.clicked.connect(self.adicionar_ao_carrinho)
        layout.addWidget(self.btn_adicionar)
        
        # Botão para remover do carrinho
        self.btn_remover = QPushButton("Remover do Carrinho")
        self.btn_remover.clicked.connect(self.remover_do_carrinho)
        layout.addWidget(self.btn_remover)
        
        self.lista_carrinho = QListWidget() 
        layout.addWidget(self.lista_carrinho)
        
        self.label_total = QLabel("Total: R$ 0.00")
        layout.addWidget(self.label_total)
        
        self.combo_pagamento = QComboBox()
        self.combo_pagamento.addItems(["Dinheiro", "Cartão", "Pix", "Fiado"])
        self.combo_pagamento.currentIndexChanged.connect(self.atualizar_visibilidade_cliente)  # Conectar o evento de alteração
        layout.addWidget(self.combo_pagamento)

        self.combo_cliente = QComboBox()
        layout.addWidget(self.combo_cliente)
        
        self.btn_finalizar = QPushButton("Finalizar Venda")
        self.btn_finalizar.clicked.connect(self.finalizar_venda)
        layout.addWidget(self.btn_finalizar)
        
        # Carregar clientes
        self.carregar_clientes()
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # Carregar categorias e produtos
        self.carregar_categorias()
        
        # Inicializar a visibilidade do cliente
        self.atualizar_visibilidade_cliente()

    def centralizar_janela(self):
        # Obtém a geometria da tela
        screen = QDesktopWidget().screenGeometry()
        # Obtém a geometria da janela
        size = self.geometry()
        # Calcula a nova posição da janela
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        # Move a janela para a nova posição
        self.move(x, y)

    def atualizar_visibilidade_cliente(self):
        forma_pagamento = self.combo_pagamento.currentText()
        if forma_pagamento == "Fiado":
            self.combo_cliente.show()  # Exibir a combobox de clientes
        else:
            self.combo_cliente.hide()  # Ocultar a combobox de clientes
    
    def carregar_categorias(self):
        self.cursor.execute("SELECT nome FROM categorias")  # Busca categorias da tabela categorias
        categorias = self.cursor.fetchall()
        self.combo_categoria.clear()  # Limpa o combo antes de adicionar novas categorias
        self.combo_categoria.addItems([c[0] for c in categorias])
        
        # Se houver pelo menos uma categoria, carregar os produtos da primeira categoria
        if categorias:
            self.combo_categoria.setCurrentIndex(0)  # Seleciona a primeira categoria
            self.carregar_produtos_por_categoria()  # Carrega os produtos dessa categoria
    
    def carregar_produtos_por_categoria(self):
        categoria_selecionada = self.combo_categoria.currentText()
        self.combo_produto.clear()
        self.cursor.execute("SELECT produto FROM estoque WHERE categoria = ?", (categoria_selecionada,))
        produtos = self.cursor.fetchall()
        self.combo_produto.addItems([p[0] for p in produtos])
        
        # Atualiza a quantidade disponível ao selecionar um produto
        self.combo_produto.currentIndexChanged.connect(self.atualizar_quantidade_disponivel)
        self.atualizar_quantidade_disponivel()  # Chama a função para inicializar a quantidade

    def atualizar_quantidade_disponivel(self):
        produto = self.combo_produto.currentText()
        self.cursor.execute("SELECT quantidade FROM estoque WHERE produto = ?", (produto,))
        quantidade = self.cursor.fetchone()
        if quantidade:
            self.label_quantidade_disponivel.setText(f"Quantidade Disponível: {quantidade[0]}")
        else:
            self.label_quantidade_disponivel.setText("Quantidade Disponível: 0")
    
    def adicionar_ao_carrinho(self):
        produto = self.combo_produto.currentText()
        quantidade = self.input_quantidade.text()
        
        if not quantidade.isdigit() or int(quantidade) <= 0:
            QMessageBox.warning(self, "Erro", "Quantidade deve ser um número válido e maior que zero!")
            return
        
        quantidade = int(quantidade)
        self.cursor.execute("SELECT quantidade, preco FROM estoque WHERE produto = ?", (produto,))
        resultado = self.cursor.fetchone()
        
        if resultado:
            estoque_disponivel, preco = resultado
            # Calcular a quantidade total do produto no carrinho
            quantidade_no_carrinho = sum(item[1] for item in self.carrinho if item[0] == produto)
            
            if estoque_disponivel == 0:
                QMessageBox.warning(self, "Erro", "Produto sem estoque!")
                return
            if quantidade + quantidade_no_carrinho > estoque_disponivel:
                QMessageBox.warning(self, "Erro", "Quantidade total no carrinho excede a quantidade disponível no estoque!")
                return
            
            # Verifica se o produto já está no carrinho
            for item in self.carrinho:
                if item[0] == produto:
                    # Atualiza a quantidade e o total do item existente
                    item[1] += quantidade  # Adiciona a nova quantidade
                    item[2] += quantidade * preco  # Atualiza o total do item
                    break
            else:
                # Se o produto não estiver no carrinho, adiciona como novo
                total_item = quantidade * preco
                self.carrinho.append([produto, quantidade, total_item])  # Usando lista em vez de tupla
                self.lista_carrinho.addItem(f"{produto} - {quantidade}x - R$ {total_item:.2f}")
            
            # Atualiza a exibição do carrinho
            self.lista_carrinho.clear()
            for item in self.carrinho:
                self.lista_carrinho.addItem(f"{item[0]} - {item[1]}x - R$ {item[2]:.2f}")
            
            self.atualizar_total()

    def remover_do_carrinho(self):
        item_selecionado = self.lista_carrinho.currentItem()
        if not item_selecionado:
            QMessageBox.warning(self, "Erro", "Selecione um item para remover!")
            return
        
        produto_remover = item_selecionado.text().split(" - ")[0]
        quantidade_remover = self.input_quantidade.text()

        # Se a quantidade não for fornecida, remover o item inteiro
        if not quantidade_remover:
            for item in self.carrinho:
                if item[0] == produto_remover:
                    self.carrinho.remove(item)
                    self.lista_carrinho.takeItem(self.lista_carrinho.row(item_selecionado))
                    self.atualizar_total()
                    break
        else:
            if not quantidade_remover.isdigit():
                QMessageBox.warning(self, "Erro", " Quantidade deve ser um número válido!")
                return
            
            quantidade_remover = int(quantidade_remover)
            for item in self.carrinho:
                if item[0] == produto_remover:
                    if quantidade_remover > item[1]:
                        QMessageBox.warning(self, "Erro", "Quantidade a remover maior do que a quantidade no carrinho!")
                        return
                    
                    # Atualiza a quantidade e o total do item
                    item[1] -= quantidade_remover  # Subtrai a quantidade removida
                    total_item = item[2] / (item[1] + quantidade_remover) * quantidade_remover  # Calcula o total a ser removido
                    item[2] -= total_item  # Atualiza o total do item no carrinho
                    
                    if item[1] == 0:  # Se a quantidade chegar a zero, remove o item do carrinho
                        self.carrinho.remove(item)
                        self.lista_carrinho.takeItem(self.lista_carrinho.row(item_selecionado))
                    else:
                        # Atualiza a exibição do item na lista
                        self.lista_carrinho.item(self.lista_carrinho.row(item_selecionado)).setText(f"{item[0]} - {item[1]}x - R$ {item[2]:.2f}")
                    
                    self.atualizar_total()  # Atualiza o total geral do carrinho
                    break
    
    def atualizar_total(self):
        total = sum(item[2] for item in self.carrinho)  # Soma os totais de cada item
        self.label_total.setText(f"Total: R$ {total:.2f}")  # Atualiza o rótulo do total
    
    def carregar_clientes(self):
        self.cursor.execute("SELECT nome FROM clientes")
        clientes = self.cursor.fetchall()
        self.combo_cliente.addItems([c[0] for c in clientes])

    def finalizar_venda(self):
        if not self.carrinho:
            QMessageBox.warning(self, "Erro", "Carrinho está vazio!")
            return
        
        forma_pagamento = self.combo_pagamento.currentText().strip()  

        cliente_selecionado = self.combo_cliente.currentText() if forma_pagamento == "Fiado" else None
        data_hora_venda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Definição do status "Pago"
        pago = 1 if forma_pagamento != "Fiado" else 0  # 1 para "Sim", 0 para "Não"

        for item in self.carrinho:
            produto, quantidade, total_item = item
            self.cursor.execute("INSERT INTO vendas (produto, quantidade, valor, pagamento, cliente, data_pagamento, pago) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (produto, quantidade, total_item, forma_pagamento, cliente_selecionado, data_hora_venda, pago))
            
            # Se a forma de pagamento for "Fiado", insira na tabela de pagamentos
            if forma_pagamento == "Fiado":
                self.cursor.execute("INSERT INTO pagamentos (cliente, produto, quantidade, data_pagamento) VALUES (?, ?, ?, ?)",
                                    (cliente_selecionado, produto, quantidade, data_hora_venda))
            
            self.cursor.execute("UPDATE estoque SET quantidade = quantidade - ? WHERE produto = ?", (quantidade, produto))
        
        self.conn.commit()
        QMessageBox.information(self, "Sucesso", "Venda finalizada!")
        backup_database()
        self.carrinho.clear()
        self.lista_carrinho.clear()
        self.label_total.setText("Total: R$ 0.00")
        self.input_quantidade.clear()
        self.carregar_categorias()

class TelaEstoque(QMainWindow):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.setWindowTitle("Gerenciar Estoque")
        self.setGeometry(150, 150, 700, 450)

        # Definindo o ícone da janela
        icon_path = resource_path('imagens/logoprincipal.ico')  # Caminho para o ícone
        self.setWindowIcon(QIcon(icon_path))  # Define o ícone da janela
        
        # Centraliza a janela na tela
        self.centralizar_janela()

        layout = QVBoxLayout()
        
        self.btn_adicionar = QPushButton("Adicionar Produto")
        self.btn_adicionar.clicked.connect(self.adicionar_produto)
        layout.addWidget(self.btn_adicionar)

        self.btn_adicionar_categoria = QPushButton("Adicionar Categoria")
        self.btn_adicionar_categoria.clicked.connect(self.adicionar_categoria)
        layout.addWidget(self.btn_adicionar_categoria)
        
        self.btn_editar = QPushButton("Editar Produto")
        self.btn_editar.clicked.connect(self.editar_produto)
        layout.addWidget(self.btn_editar)
        
        self.btn_remover = QPushButton("Remover Produto")
        self.btn_remover.clicked.connect(self.remover_produto)
        layout.addWidget(self.btn_remover)

        # ComboBox para selecionar a categoria
        self.combo_categoria = QComboBox()
        self.combo_categoria.currentIndexChanged.connect(self.filtrar_produtos_por_categoria)
        layout.addWidget(self.combo_categoria)
        
        self.tabela_estoque = QTableWidget()
        self.tabela_estoque.setColumnCount(5)  # Aumenta para 5 colunas
        self.tabela_estoque.setHorizontalHeaderLabels(["Produto", "Categoria", "Quantidade", "Preço", "Imagem"])
        self.tabela_estoque.setAlternatingRowColors(True)
        self.tabela_estoque.setStyleSheet("QTableWidget {selection-background-color: lightblue;}")
        self.tabela_estoque.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela_estoque.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela_estoque.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela_estoque.horizontalHeader().setStretchLastSection(True)
        self.tabela_estoque.horizontalHeader().setFont(QFont("Arial", 8, QFont.Bold))
        self.tabela_estoque.verticalHeader().setVisible(False)
        layout.addWidget(self.tabela_estoque)

        # QLabel para exibir a imagem
        self.label_imagem = QLabel("Selecione um produto para ver a imagem.")
        self.label_imagem.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_imagem)
        
        self.carregar_categorias()  # Carrega as categorias na ComboBox
        self.carregar_estoque()
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Conectar o sinal de seleção da tabela
        self.tabela_estoque.itemSelectionChanged.connect(self.atualizar_imagem)

    def adicionar_categoria(self):
        self.tela_gerenciar_categorias = TelaGerenciarCategorias(self.conn)
        self.tela_gerenciar_categorias.categoria_adicionada.connect(self.carregar_categorias)  # Conecta o sinal
        self.tela_gerenciar_categorias.exec_()  # Abre a tela de gerenciamento de categorias

    def centralizar_janela(self):
        # Obtém a geometria da tela
        screen = QDesktopWidget().screenGeometry()
        # Obtém a geometria da janela
        size = self.geometry()
        # Calcula a nova posição da janela
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        # Move a janela para a nova posição
        self.move(x, y)

    def carregar_categorias(self):
        """Carrega as categorias do banco de dados na ComboBox."""
        self.cursor.execute("SELECT nome FROM categorias")
        categorias = self.cursor.fetchall()
        self.combo_categoria.clear()  # Limpa a ComboBox antes de adicionar novas categorias
        self.combo_categoria.addItem("Todas as Categorias")  # Adiciona a opção para mostrar todas as categorias
        for categoria in categorias:
            self.combo_categoria.addItem(categoria[0])  # Adiciona cada categoria à ComboBox

    def filtrar_produtos_por_categoria(self):
        """Filtra os produtos na tabela com base na categoria selecionada na ComboBox."""
        categoria_selecionada = self.combo_categoria.currentText()
        if categoria_selecionada == "Todas as Categorias":
            self.carregar_estoque()  # Carrega todos os produtos
        else:
            self.cursor.execute("SELECT produto, categoria, quantidade, preco, imagem FROM estoque WHERE categoria = ?", (categoria_selecionada,))
            produtos = self.cursor.fetchall()
            self.atualizar_tabela(produtos)

    def atualizar_tabela(self, produtos):
        """Atualiza a tabela de estoque com os produtos fornecidos."""
        self.tabela_estoque.setRowCount(len(produtos))
        
        for i, produto in enumerate(produtos):
            for j, dado in enumerate(produto):
                if j == 3:  # Se for a coluna do preço
                    try:
                        preco_float = float(dado)
                        preco_formatado = f"R$ {preco_float:.2f}".replace('.', ',')
                    except ValueError:
                        preco_formatado = "R$ 0,00"
                    item = QTableWidgetItem(preco_formatado)
                else:
                    item = QTableWidgetItem(str(dado))
                item.setTextAlignment(Qt.AlignCenter)
                self.tabela_estoque.setItem(i, j, item)

            # Verifica se a quantidade está abaixo de um limite
            if produto[2] < 6:  # Se a quantidade for menor que 6, destaque a linha
                for j in range(self.tabela_estoque.columnCount()):
                    self.tabela_estoque.item(i, j).setBackground(QColor(255, 200, 200))  # Cor de fundo vermelha clara

        self.tabela_estoque.resizeColumnsToContents()  # Ajusta colunas automaticamente
    
    def atualizar_imagem(self):
        row = self.tabela_estoque.currentRow()
        if row >= 0:
            caminho_imagem = self.tabela_estoque.item(row, 4).text()  # Obtém o caminho da imagem
            pixmap = QPixmap(caminho_imagem)
            self.label_imagem.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))  # Ajusta o tamanho da imagem
        else:
            self.label_imagem.clear()  # Limpa a imagem se nenhuma linha estiver selecionada

    def carregar_estoque(self):
        self.cursor.execute("SELECT produto, categoria, quantidade, preco, imagem FROM estoque")
        produtos = self.cursor.fetchall()
        self.tabela_estoque.setRowCount(len(produtos))
        
        for i, produto in enumerate(produtos):
            for j, dado in enumerate(produto):
                if j == 3:  # Se for a coluna do preço
                    try:
                        preco_float = float(dado)
                        preco_formatado = f"R$ {preco_float:.2f}".replace('.', ',')
                    except ValueError:
                        preco_formatado = "R$ 0,00"
                    item = QTableWidgetItem(preco_formatado)
                else:
                    item = QTableWidgetItem(str(dado))
                item.setTextAlignment(Qt.AlignCenter)
                self.tabela_estoque.setItem(i, j, item)

            # Verifica se a quantidade está abaixo de um limite
            if produto[2] < 6:  # Se a quantidade for menor que 10, destaque a linha
                for j in range(self.tabela_estoque.columnCount()):
                    self.tabela_estoque.item(i, j).setBackground(QColor(255, 200, 200))  # Cor de fundo vermelha clara

        self.tabela_estoque.resizeColumnsToContents()  # Ajusta colunas automaticamente
    
    def adicionar_produto(self):
        self.tela_adicionar = TelaAdicionarProduto(self.conn)
        self.tela_adicionar.produto_adicionado.connect(self.carregar_estoque)
        self.carregar_estoque  # Conecta o sinal para atualizar a tabela após adicionar o produto
        self.tela_adicionar.exec_()  # Abre a janela de adicionar produto
    
    def editar_produto(self):
        row = self.tabela_estoque.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erro", "Selecione um produto para editar!")
            return
        
        produto = self.tabela_estoque.item(row, 0).text()
        categoria = self.tabela_estoque.item(row, 1).text()
        quantidade = self.tabela_estoque.item(row, 2).text()
        preco = self.tabela_estoque.item(row, 3).text()
        imagem = self.tabela_estoque.item(row, 4).text()  # Obtém o caminho da imagem

        self.tela_editar = TelaEditarProduto(self.conn, produto, categoria, quantidade, preco, imagem)
        self.tela_editar.exec_()
        backup_database()
        self.carregar_estoque()  # Atualiza a tabela após edição

    def remover_produto(self):
        row = self.tabela_estoque.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erro", "Selecione um produto para remover!")
            return
        
        produto = self.tabela_estoque.item(row, 0).text()
        categoria = self.tabela_estoque.item(row, 1).text()
        resposta = QMessageBox.question(self, "Confirmar Remoção", f"Tem certeza que deseja remover o produto '{produto}'?", QMessageBox.Yes | QMessageBox.No)
        
        if resposta == QMessageBox.Yes:
            self.cursor.execute("DELETE FROM estoque WHERE produto = ?", (produto,))
            self.conn.commit()
            backup_database()
            self.carregar_estoque()  # Atualiza a tabela após remoção
            self.filtrar_produtos_por_categoria()  # Atualiza a ComboBox após remoção

            # Verifica se ainda existem produtos na categoria
            self.cursor.execute("SELECT COUNT(*) FROM estoque WHERE categoria = ?", (categoria,))
            count = self.cursor.fetchone()[0]
            if count == 0:
                QMessageBox.information(self, "Informação", f"Não há mais produtos na categoria '{categoria}'.")
                self.combo_categoria.setCurrentIndex(0)  # Retorna para a exibição de todas as categorias
                self.carregar_estoque()  # Carrega todos os produtos novamente

    def abrir_tela_gerenciar_categorias(self):
        self.tela_gerenciar_categorias = TelaGerenciarCategorias(self.conn)
        self.tela_gerenciar_categorias.categoria_adicionada.connect(self.carregar_categorias)  # Conecta o sinal
        self.tela_gerenciar_categorias.exec_()  # Abre a tela de gerenciamento de categorias

class TelaGerenciarCategorias(QDialog):
    categoria_adicionada = pyqtSignal()  # Sinal que será emitido quando uma categoria for adicionada

    def __init__(self, conn):
        super().__init__()
        self.setWindowTitle("Gerenciar Categorias")

        # Definindo o ícone da janela
        icon_path = resource_path('imagens/logoprincipal.ico')  # Caminho para o ícone
        self.setWindowIcon(QIcon(icon_path))  # Define o ícone da janela

        self.conn = conn
        self.cursor = self.conn.cursor()
        
        layout = QVBoxLayout()
        
        self.lista_categorias = QListWidget()
        self.carregar_categorias()
        layout.addWidget(self.lista_categorias)
        
        self.input_categoria = QLineEdit()
        self.input_categoria.setPlaceholderText("Nova Categoria")
        layout.addWidget(self.input_categoria)
        
        self.btn_adicionar = QPushButton("Adicionar Categoria")
        self.btn_adicionar.clicked.connect(self.adicionar_categoria)
        layout.addWidget(self.btn_adicionar)
        
        self.btn_remover = QPushButton("Remover Categoria")
        self.btn_remover.clicked.connect(self.remover_categoria)
        layout.addWidget(self.btn_remover)
        
        self.setLayout(layout)

    def carregar_categorias(self):
        self.lista_categorias.clear()
        self.cursor.execute("SELECT nome FROM categorias")
        categorias = self.cursor.fetchall()
        for categoria in categorias:
            self.lista_categorias.addItem(categoria[0])

    def adicionar_categoria(self):
        nova_categoria = self.input_categoria.text().strip()
        if nova_categoria:
            try:
                self.cursor.execute("INSERT INTO categorias (nome) VALUES (?)", (nova_categoria,))
                self.conn.commit()
                backup_database()
                self.categoria_adicionada.emit()  # Emite o sinal
                self.carregar_categorias()  # Atualiza a lista de categorias
                self.input_categoria.clear()  # Limpa o campo de entrada
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Erro", "Categoria já existe.")
        else:
            QMessageBox.warning(self, "Erro", "Digite um nome de categoria válido.")

    def remover_categoria(self):
        item_selecionado = self.lista_categorias.currentItem()
        if item_selecionado:
            categoria = item_selecionado.text()
            resposta = QMessageBox.question(self, "Confirmar Remoção", f"Tem certeza que deseja remover a categoria '{categoria}'?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                self.cursor.execute("DELETE FROM categorias WHERE nome = ?", (categoria,))
                self.conn.commit()
                backup_database()
                self.carregar_categorias()  # Atualiza a lista de categorias
        else:
            QMessageBox.warning(self, "Erro", "Selecione uma categoria para remover.")

class TelaAdicionarProduto(QDialog):
    produto_adicionado = pyqtSignal()  # Sinal que será emitido quando um produto for adicionado

    def __init__(self, conn):
        super().__init__()
        self.setWindowTitle("Adicionar Produto")

        # Definindo o ícone da janela
        icon_path = resource_path('imagens/logoprincipal.ico')  # Caminho para o ícone
        self.setWindowIcon(QIcon(icon_path))  # Define o ícone da janela

        self.conn = conn
        self.cursor = self.conn.cursor()
        
        layout = QFormLayout()
        
        self.input_produto = QLineEdit()
        layout.addRow("Produto:", self.input_produto)
        
        self.input_categoria = QComboBox()
        self.carregar_categorias()  # Certifique-se de que este método está definido
        layout.addRow("Categoria:", self.input_categoria)
        
        self.input_quantidade = QLineEdit()
        layout.addRow("Quantidade:", self.input_quantidade)
        
        self.input_preco = QLineEdit()
        layout.addRow("Preço:", self.input_preco)

        # Campo para exibir o caminho da imagem
        self.input_imagem = QLineEdit()
        self.input_imagem.setReadOnly(True)
        layout.addRow("Imagem:", self.input_imagem)

        # Botão para selecionar a imagem
        self.btn_selecionar_imagem = QPushButton("Selecionar Imagem")
        self.btn_selecionar_imagem.clicked.connect(self.selecionar_imagem)
        layout.addWidget(self.btn_selecionar_imagem)

        self.btn_salvar = QPushButton("Salvar")
        self.btn_salvar.clicked.connect(self.salvar_produto)
        layout.addWidget(self.btn_salvar)
        
        self.setLayout(layout)

    def carregar_categorias(self):
        self.input_categoria.clear()  # Limpa as categorias existentes
        self.cursor.execute("SELECT nome FROM categorias")  # Busca categorias da tabela categorias
        categorias = self.cursor.fetchall()
        for categoria in categorias:
            self.input_categoria.addItem(categoria[0])  # Adiciona cada categoria à combobox

    def selecionar_imagem(self):
        options = QFileDialog.Options()
        caminho_imagem, _ = QFileDialog.getOpenFileName(self, "Selecionar Imagem", "", "Imagens (*.png *.jpg *.jpeg *.bmp);;Todos os Arquivos (*)", options=options)
        if caminho_imagem:
            self.input_imagem.setText(caminho_imagem)

    def salvar_produto(self):
        produto = self.input_produto.text().strip()
        categoria = self.input_categoria.currentText()
        quantidade = self.input_quantidade.text().strip()
        preco = self.input_preco.text().strip()
        imagem = self.input_imagem.text().strip()

        # Remove o prefixo "R$" e substitui a vírgula por ponto para conversão
        preco = preco.replace("R$ ", "").replace(",", ".").strip()

        try:
            preco_float = float(preco)
            quantidade_int = int(quantidade)

            if not produto or not categoria or quantidade_int < 0 or preco_float < 0:
                QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos corretamente.")
                return

            self.cursor.execute("INSERT INTO estoque (produto, categoria, quantidade, preco, imagem) VALUES (?, ?, ?, ?, ?)", 
                                (produto, categoria, quantidade_int, preco_float, imagem))
            self.conn.commit()

            self.produto_adicionado.emit()
            backup_database()
            self.close()
        except ValueError:
            QMessageBox.warning(self, "Erro", "Por favor, insira valores válidos para quantidade e preço.")

class TelaEditarProduto(QDialog):
    def __init__(self, conn, produto, categoria, quantidade, preco, imagem):
        super().__init__()
        self.setWindowTitle("Editar Produto")

        # Definindo o ícone da janela
        icon_path = resource_path('imagens/logoprincipal.ico')  # Caminho para o ícone
        self.setWindowIcon(QIcon(icon_path))  # Define o ícone da janela

        self.conn = conn
        self.cursor = self.conn.cursor()
        
        layout = QFormLayout()
        
        self.input_produto = QLineEdit(produto)
        layout.addRow("Produto:", self.input_produto)
        
        self.input_categoria = QComboBox()
        self.carregar_categorias()
        self.input_categoria.setCurrentText(categoria)
        layout.addRow("Categoria:", self.input_categoria)
        
        self.input_quantidade = QLineEdit(quantidade)
        layout.addRow("Quantidade:", self.input_quantidade)
        
        self.input_preco = QLineEdit(preco)
        layout.addRow("Preço:", self.input_preco)

        # Campo para exibir o caminho da imagem
        self.input_imagem = QLineEdit(imagem)
        self.input_imagem.setReadOnly(True)
        layout.addRow("Imagem:", self.input_imagem)

        # Botão para selecionar a nova imagem
        self.btn_selecionar_imagem = QPushButton("Selecionar Imagem")
        self.btn_selecionar_imagem.clicked.connect(self.selecionar_imagem)
        layout.addWidget(self.btn_selecionar_imagem)

        self.btn_salvar = QPushButton("Salvar")
        self.btn_salvar.clicked.connect(self.salvar_produto)
        layout.addWidget(self.btn_salvar)
        
        self.setLayout(layout)
        
        self.produto_original = produto

    def carregar_categorias(self):
        self.input_categoria.clear()
        self.cursor.execute("SELECT nome FROM categorias")
        categorias = self.cursor.fetchall()
        for categoria in categorias:
            self.input_categoria.addItem(categoria[0])

    def selecionar_imagem(self):
        options = QFileDialog.Options()
        caminho_imagem, _ = QFileDialog.getOpenFileName(self, "Selecionar Imagem", "", "Imagens (*.png *.jpg *.jpeg *.bmp);;Todos os Arquivos (*)", options=options)
        if caminho_imagem:
            self.input_imagem.setText(caminho_imagem)

    def salvar_produto(self):
        novo_produto = self.input_produto.text().strip()
        categoria = self.input_categoria.currentText()
        quantidade = self.input_quantidade.text().strip()
        preco = self.input_preco.text().strip()
        imagem = self.input_imagem.text().strip()

        preco = preco.replace("R$ ", "").replace(",", ".").strip()
        
        self.cursor.execute("UPDATE estoque SET produto = ?, categoria = ?, quantidade = ?, preco = ?, imagem = ? WHERE produto = ?", 
                            (novo_produto, categoria, quantidade, preco, imagem, self.produto_original))
        self.conn.commit()
        backup_database()
        self.close() 
        
class TelaRelatorios(QMainWindow):
    def __init__(self, conn):
        super().__init__()
        self.setWindowTitle("Relatórios")
        self.setGeometry(150, 150, 800, 600)

        # Definindo o ícone da janela
        icon_path = resource_path('imagens/logoprincipal.ico')  # Caminho para o ícone
        self.setWindowIcon(QIcon(icon_path))  # Define o ícone da janela

        # Centraliza a janela na tela
        self.centralizar_janela()

        self.conn = conn
        self.cursor = self.conn.cursor()
        
        layout = QVBoxLayout()
        
        # Botão para mostrar histórico de vendas
        self.btn_historico_vendas = QPushButton("Histórico de Vendas")
        self.btn_historico_vendas.clicked.connect(self.mostrar_historico_vendas)
        layout.addWidget(self.btn_historico_vendas)

        # Botão para mostrar relatório de vendas
        self.btn_relatorio_vendas = QPushButton("Relatório de Vendas")
        self.btn_relatorio_vendas.clicked.connect(self.mostrar_relatorio_vendas)
        layout.addWidget(self.btn_relatorio_vendas)
        
        # Botão para mostrar produtos mais vendidos
        self.btn_produtos_vendidos = QPushButton("Produtos Mais Vendidos")
        self.btn_produtos_vendidos.clicked.connect(self.mostrar_produtos_vendidos)
        layout.addWidget(self.btn_produtos_vendidos)
        
        # Botão para Relatórios de Faturamento
        self.btn_faturamento_diario = QPushButton("Faturamento Diário")
        self.btn_faturamento_diario.clicked.connect(self.mostrar_faturamento_diario)
        layout.addWidget(self.btn_faturamento_diario)

        self.btn_faturamento_semanal = QPushButton("Faturamento Semanal")
        self.btn_faturamento_semanal.clicked.connect(self.mostrar_faturamento_semanal)
        layout.addWidget(self.btn_faturamento_semanal)

        self.btn_faturamento_mensal = QPushButton("Faturamento Mensal")
        self.btn_faturamento_mensal.clicked.connect(self.mostrar_faturamento_mensal)
        layout.addWidget(self.btn_faturamento_mensal)

        # Botão para exportar relatório de vendas
        self.btn_exportar_relatorio = QPushButton("Exportar Relatório de Vendas")
        self.btn_exportar_relatorio.clicked.connect(self.exportar_relatorio_vendas)  # Conectar o evento
        layout.addWidget(self.btn_exportar_relatorio)
        
        # Tabela para exibir os resultados
        self.tabela_relatorios = QTableWidget()
        layout.addWidget(self.tabela_relatorios)

        # Ajustar a tabela
        self.tabela_relatorios.setColumnCount(6)  # Definindo o número de colunas
        self.tabela_relatorios.horizontalHeader().setStretchLastSection(True)  # Ajusta a última coluna para ocupar o espaço restante
        self.tabela_relatorios.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # Ajusta a largura das colunas ao conteúdo
        self.tabela_relatorios.horizontalHeader().setFont(QFont("Arial", 8, QFont.Bold))
        self.tabela_relatorios.horizontalHeader().setMinimumSectionSize(100)  # Define uma largura mínima para as colunas
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def centralizar_janela(self):
        # Obtém a geometria da tela
        screen = QDesktopWidget().screenGeometry()
        # Obtém a geometria da janela
        size = self.geometry()
        # Calcula a nova posição da janela
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        # Move a janela para a nova posição
        self.move(x, y)

    def mostrar_relatorio_vendas(self):
        self.cursor.execute("SELECT produto, SUM(quantidade), SUM(valor) FROM vendas GROUP BY produto")
        vendas = self.cursor.fetchall()
        
        self.tabela_relatorios.setRowCount(len(vendas))
        self.tabela_relatorios.setColumnCount(3)
        self.tabela_relatorios.setHorizontalHeaderLabels(["Produto", "Quantidade Vendida", "Total Vendido"])
        
        for i, (produto, quantidade, total) in enumerate(vendas):
            # Adiciona o produto na primeira coluna
            self.tabela_relatorios.setItem(i, 0, QTableWidgetItem(produto))
            
            # Cria o item para a quantidade vendida e centraliza
            item_quantidade = QTableWidgetItem(str(quantidade))
            item_quantidade.setTextAlignment(Qt.AlignCenter)  # Centraliza o texto
            self.tabela_relatorios.setItem(i, 1, item_quantidade)
            
            # Cria o item para o total vendido, formata e centraliza
            item_total = QTableWidgetItem(f"R$ {total:.2f}")
            item_total.setTextAlignment(Qt.AlignCenter)  # Centraliza o texto
            self.tabela_relatorios.setItem(i, 2, item_total)

    def mostrar_produtos_vendidos(self):
        self.cursor.execute("""
            SELECT produto, SUM(quantidade) as total_vendido 
            FROM vendas 
            GROUP BY produto 
            ORDER BY total_vendido DESC 
            LIMIT 10
        """)
        produtos = self.cursor.fetchall()
        
        self.tabela_relatorios.setRowCount(len(produtos))
        self.tabela_relatorios.setColumnCount(2)
        self.tabela_relatorios.setHorizontalHeaderLabels(["Produto", "Quantidade Vendido"])
        
        for i, (produto, total_vendido) in enumerate(produtos):
            # Adiciona o produto na primeira coluna
            self.tabela_relatorios.setItem(i, 0, QTableWidgetItem(produto))
            
            # Cria o item para a quantidade vendida
            item_total_vendido = QTableWidgetItem(str(total_vendido))
            item_total_vendido.setTextAlignment(Qt.AlignCenter)  # Centraliza o texto
            self.tabela_relatorios.setItem(i, 1, item_total_vendido)

    def mostrar_faturamento_diario(self):
        try:
            self.cursor.execute("""
                SELECT DATE(data_pagamento) as data, SUM(valor) as total
                FROM vendas
                WHERE DATE(data_pagamento) = DATE('now', 'localtime')
                GROUP BY data
            """)
            faturamento = self.cursor.fetchall()
            
            # Debug: Verifique o resultado da consulta
            print("Resultado da consulta:", faturamento)

            # Limpa a tabela antes de adicionar novos dados
            self.tabela_relatorios.setRowCount(0)
            self.tabela_relatorios.setColumnCount(2)
            self.tabela_relatorios.setHorizontalHeaderLabels(["Data", "Total Faturado"])
            
            if faturamento:  # Verifica se há dados para mostrar
                self.tabela_relatorios.setRowCount(len(faturamento))
                for i, (data, total) in enumerate(faturamento):
                    # Adiciona e centraliza o item para a data
                    item_data = QTableWidgetItem(data)
                    item_data.setTextAlignment(Qt.AlignCenter)  # Centraliza o texto
                    self.tabela_relatorios.setItem(i, 0, item_data)
                    
                    # Adiciona e centraliza o item para o total faturado
                    item_total = QTableWidgetItem(f"R$ {total:.2f}")
                    item_total.setTextAlignment(Qt.AlignCenter)  # Centraliza o texto
                    self.tabela_relatorios.setItem(i, 1, item_total)
            else:
                print("Nenhum faturamento encontrado para hoje.")
                # Opcional: Adicione uma mensagem na tabela informando que não há dados
                self.tabela_relatorios.setRowCount(1)
                self.tabela_relatorios.setItem(0, 0, QTableWidgetItem("Nenhum faturamento encontrado"))
                self.tabela_relatorios.setItem(0, 1, QTableWidgetItem(""))
        except Exception as e:
            print(f"Erro ao mostrar faturamento diário: {e}")


    def mostrar_faturamento_semanal(self):
        # Obtém a data atual
        data_atual = datetime.now()
        
        # Calcula a data de início da semana (segunda-feira)
        inicio_semana = data_atual - timedelta(days=data_atual.weekday())
        # Calcula a data de fim da semana (domingo)
        fim_semana = inicio_semana + timedelta(days=6)
        
        # Formata as datas para o formato desejado
        inicio_formatado = inicio_semana.strftime("%d/%m/%Y")
        fim_formatado = fim_semana.strftime("%d/%m/%Y")
        
        # Executa a consulta SQL
        self.cursor.execute("""
            SELECT strftime('%Y-%W', data_pagamento) as semana, SUM(valor) as total
            FROM vendas
            WHERE DATE(data_pagamento) >= DATE('now', '-6 days')
            GROUP BY semana
        """)
        faturamento = self.cursor.fetchall()
        
        self.tabela_relatorios.setRowCount(len(faturamento))
        self.tabela_relatorios.setColumnCount(2)
        self.tabela_relatorios.setHorizontalHeaderLabels(["Semana", "Total Faturado"])
        
        for i, (semana, total) in enumerate(faturamento):
            # Exibe o intervalo de datas formatado e centraliza
            item_semana = QTableWidgetItem(f"{inicio_formatado} a {fim_formatado}")
            item_semana.setTextAlignment(Qt.AlignCenter)  # Centraliza o texto
            self.tabela_relatorios.setItem(i, 0, item_semana)
            
            # Adiciona e centraliza o item para o total faturado
            item_total = QTableWidgetItem(f"R$ {total:.2f}")
            item_total.setTextAlignment(Qt.AlignCenter)  # Centraliza o texto
            self.tabela_relatorios.setItem(i, 1, item_total)


    def mostrar_faturamento_mensal(self):
        self.cursor.execute("""
            SELECT strftime('%Y-%m', data_pagamento) as mes, SUM(valor) as total
            FROM vendas
            WHERE DATE(data_pagamento) >= DATE('now', 'start of month')
            GROUP BY mes
        """)
        faturamento = self.cursor.fetchall()
        
        self.tabela_relatorios.setRowCount(len(faturamento))
        self.tabela_relatorios.setColumnCount(2)
        self.tabela_relatorios.setHorizontalHeaderLabels(["Mês", "Total Faturado"])
        
        for i, (mes, total) in enumerate(faturamento):
            # Adiciona e centraliza o item para o mês
            item_mes = QTableWidgetItem(mes)
            item_mes.setTextAlignment(Qt.AlignCenter)  # Centraliza o texto
            self.tabela_relatorios.setItem(i, 0, item_mes)
            
            # Adiciona e centraliza o item para o total faturado
            item_total = QTableWidgetItem(f"R$ {total:.2f}")
            item_total.setTextAlignment(Qt.AlignCenter)  # Centraliza o texto
            self.tabela_relatorios.setItem(i, 1, item_total)

    def mostrar_historico_vendas(self):
        self.cursor.execute("""
            SELECT produto, quantidade, valor, pagamento, cliente, pago, data_pagamento 
            FROM vendas
        """)
        historico = self.cursor.fetchall()

        self.tabela_relatorios.setRowCount(len(historico))
        self.tabela_relatorios.setColumnCount(7)  # Ajuste para 7 colunas
        self.tabela_relatorios.setHorizontalHeaderLabels(["Produto", "Quantidade", "Valor", "Forma de Pagamento", "Cliente", "Pago", "Data da Venda"])

        for i, (produto, quantidade, valor, pagamento, cliente, pago, data_pagamento) in enumerate(historico):
            # Adiciona o produto na primeira coluna
            self.tabela_relatorios.setItem(i, 0, QTableWidgetItem(produto))
            
            # Centraliza os valores numéricos
            item_quantidade = QTableWidgetItem(str(quantidade))
            item_quantidade.setTextAlignment(Qt.AlignCenter)
            self.tabela_relatorios.setItem(i, 1, item_quantidade)

            item_valor = QTableWidgetItem(f"R$ {valor:.2f}")
            item_valor.setTextAlignment(Qt.AlignCenter)
            self.tabela_relatorios.setItem(i, 2, item_valor)

            item_pagamento = QTableWidgetItem(pagamento)
            item_pagamento.setTextAlignment(Qt.AlignCenter)
            self.tabela_relatorios.setItem(i, 3, item_pagamento)

            item_cliente = QTableWidgetItem(cliente if cliente else "-")  # Evita valores None vazios
            item_cliente.setTextAlignment(Qt.AlignCenter)
            self.tabela_relatorios.setItem(i, 4, item_cliente)

            # Ajuste na exibição do status "Pago"
            item_pago = QTableWidgetItem("Sim" if pago == 1 else "Não")  # Converte 0 e 1 para "Sim" e "Não"
            item_pago.setTextAlignment(Qt.AlignCenter)
            self.tabela_relatorios.setItem(i, 5, item_pago)

            item_data_pagamento = QTableWidgetItem(data_pagamento)
            item_data_pagamento.setTextAlignment(Qt.AlignCenter)
            self.tabela_relatorios.setItem(i, 6, item_data_pagamento)

        self.tabela_relatorios.resizeColumnsToContents()  # Ajusta as colunas após preencher os dados
        self.tabela_relatorios.setAlternatingRowColors(True)  # Adiciona cores alternadas às linhas para melhor legibilidade
        self.tabela_relatorios.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Desabilita a edição das células
        self.tabela_relatorios.setSelectionBehavior(QTableWidget.SelectRows)  # Permite selecionar linhas inteiras
        self.tabela_relatorios.setSelectionMode(QTableWidget.SingleSelection)  # Permite apenas uma seleção por vez
        self.tabela_relatorios.setSortingEnabled(True)  # Habilita a ordenação das colunas
        self.tabela_relatorios.setColumnWidth(0, 200)  # Define uma largura específica para a coluna de produtos
        self.tabela_relatorios.setColumnWidth(1, 100)  # Define uma largura específica para a coluna de quantidade
        self.tabela_relatorios.setColumnWidth(2, 100)  # Define uma largura específica para a coluna de valor
        self.tabela_relatorios.setColumnWidth(3, 150)  # Define uma largura específica para a coluna de forma de pagamento

    def exportar_relatorio_vendas(self):
        self.cursor.execute("SELECT produto, quantidade, valor, pagamento, cliente, data_pagamento FROM vendas")
        vendas = self.cursor.fetchall()

        # Cria um DataFrame com os dados
        df = pd.DataFrame(vendas, columns=["Produto", "Quantidade", "Valor", "Forma de Pagamento", "Cliente", "Data da Venda"])

        # Define o caminho absoluto na pasta Documentos
        caminho_pasta = os.path.join(os.path.expanduser("~"), "Documents")  # Para Windows
        caminho_arquivo = os.path.join(caminho_pasta, "relatorio_vendas.xlsx")

        try:
            # Cria um arquivo Excel
            with pd.ExcelWriter(caminho_arquivo, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Vendas')

                # Acessa o objeto do workbook e do worksheet
                workbook = writer.book
                worksheet = writer.sheets['Vendas']

                # Formatação da coluna de valores
                for cell in worksheet['C']:  # Coluna de Valor
                    cell.number_format = '#,##0.00'  # Formato de moeda

                # Ajusta a largura das colunas
                for column in worksheet.columns:
                    max_length = 0
                    column = [cell for cell in column]
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass
                    adjusted_width = (max_length + 2)
                    worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

            QMessageBox.information(self, "Sucesso", f"Relatório de vendas exportado com sucesso!\nLocal: {caminho_arquivo}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao exportar o relatório: {e}")

class TelaGerenciarClientes(QMainWindow):
    def __init__(self, conn):
        super().__init__()
        self.setWindowTitle("Gerenciar Clientes")
        self.setGeometry(150, 150, 400, 300)

        # Definindo o ícone da janela
        icon_path = resource_path('imagens/logoprincipal.ico')  # Caminho para o ícone
        self.setWindowIcon(QIcon(icon_path))  # Define o ícone da janela

        # Centraliza a janela na tela
        self.centralizar_janela()

        self.conn = conn
        self.cursor = self.conn.cursor()
        
        layout = QVBoxLayout()
        
        self.btn_adicionar_cliente = QPushButton("Adicionar Cliente")
        self.btn_adicionar_cliente.clicked.connect(self.adicionar_cliente)
        layout.addWidget(self.btn_adicionar_cliente)

        self.btn_marcar_pago = QPushButton("Pagamentos Pendentes")
        self.btn_marcar_pago.clicked.connect(self.marcar_pago)
        layout.addWidget(self.btn_marcar_pago)

        self.btn_remover_cliente = QPushButton("Remover Cliente")
        self.btn_remover_cliente.clicked.connect(self.remover_cliente)
        layout.addWidget(self.btn_remover_cliente)
        
        self.lista_clientes = QListWidget()
        layout.addWidget(self.lista_clientes)
        
        self.carregar_clientes()
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def centralizar_janela(self):
        # Obtém a geometria da tela
        screen = QDesktopWidget().screenGeometry()
        # Obtém a geometria da janela
        size = self.geometry()
        # Calcula a nova posição da janela
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        # Move a janela para a nova posição
        self.move(x, y)

    def carregar_clientes(self):
        self.cursor.execute("SELECT nome FROM clientes")
        clientes = self.cursor.fetchall()
        self.lista_clientes.clear()
        self.lista_clientes.addItems([c[0] for c in clientes])

    def adicionar_cliente(self):
        nome, ok = QInputDialog.getText(self, "Adicionar Cliente", "Nome do Cliente:")
        if ok and nome:
            self.cursor.execute("INSERT INTO clientes (nome) VALUES (?)", (nome,))
            self.conn.commit()
            backup_database()
            self.carregar_clientes()

    def marcar_pago(self):
        cliente_selecionado = self.lista_clientes.currentItem()
        if cliente_selecionado is None:
            QMessageBox.warning(self, "Erro", "Selecione um cliente primeiro.")
            return
        
        nome_cliente = cliente_selecionado.text()
        
        self.tela_selecionar_itens = TelaSelecionarItens(self.conn, nome_cliente)
        self.tela_selecionar_itens.exec_()
        backup_database()

    def remover_cliente(self):
        cliente_selecionado = self.lista_clientes.currentItem()
        if cliente_selecionado is None:
            QMessageBox.warning(self, "Erro", "Selecione um cliente primeiro.")
            return
        
        nome_cliente = cliente_selecionado.text()

        # Verifica se o cliente tem vendas pendentes (pago = 0)
        self.cursor.execute("SELECT COUNT(*) FROM vendas WHERE cliente = ? AND pago = 0", (nome_cliente,))
        vendas_pendentes = self.cursor.fetchone()[0]

        if vendas_pendentes > 0:
            QMessageBox.warning(self, "Erro", "Não é possível remover o cliente. Ele possui vendas pendentes.")
            return

        # Confirma a remoção
        resposta = QMessageBox.question(self, "Confirmar Remoção", f"Tem certeza que deseja remover o cliente '{nome_cliente}'?", QMessageBox.Yes | QMessageBox.No)
        if resposta == QMessageBox.Yes:
            self.cursor.execute("DELETE FROM clientes WHERE nome = ?", (nome_cliente,))
            self.conn.commit()
            backup_database()
            self.carregar_clientes()  # Atualiza a lista de clientes
            QMessageBox.information(self, "Sucesso", "Cliente removido com sucesso.")

class TelaSelecionarItens(QDialog):
    def __init__(self, conn, cliente):
        super().__init__()
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.cliente = cliente
        self.setWindowTitle(f"Selecionar Itens para {cliente}")
        self.setGeometry(150, 150, 400, 300)

        # Definindo o ícone da janela
        icon_path = resource_path('imagens/logoprincipal.ico')  # Caminho para o ícone
        self.setWindowIcon(QIcon(icon_path))  # Define o ícone da janela

        # Centraliza a janela na tela
        self.centralizar_janela()

        layout = QVBoxLayout()

        # QLabel para exibir o total da dívida
        self.label_total_divida = QLabel("Total da Dívida: R$ 0.00")
        layout.addWidget(self.label_total_divida)

        self.lista_itens = QTableWidget()
        self.lista_itens.setColumnCount(4)
        self.lista_itens.setHorizontalHeaderLabels(["Produto", "Quantidade", "Valor", "Selecionar"])
        layout.addWidget(self.lista_itens)

        self.btn_marcar_pago = QPushButton("Marcar como Pago")
        self.btn_marcar_pago.clicked.connect(self.marcar_pago)
        layout.addWidget(self.btn_marcar_pago)

        self.carregar_itens()

        self.setLayout(layout)

    def centralizar_janela(self):
        # Obtém a geometria da tela
        screen = QDesktopWidget().screenGeometry()
        # Obtém a geometria da janela
        size = self.geometry()
        # Calcula a nova posição da janela
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        # Move a janela para a nova posição
        self.move(x, y)

    def carregar_itens(self):
        self.cursor.execute("""
            SELECT id, produto, quantidade, valor FROM vendas
            WHERE cliente = ? AND pago = 0
        """, (self.cliente,))

        itens_pendentes = self.cursor.fetchall()

        self.lista_itens.setRowCount(len(itens_pendentes))

        total_divida = 0  # Variável para calcular o total da dívida

        # Dicionário para armazenar os IDs das vendas
        self.ids_vendas = {}

        for i, (id_venda, produto, quantidade, valor) in enumerate(itens_pendentes):
            self.lista_itens.setItem(i, 0, QTableWidgetItem(produto))

            item_quantidade = QTableWidgetItem(str(quantidade))
            item_quantidade.setTextAlignment(Qt.AlignCenter)
            self.lista_itens.setItem(i, 1, item_quantidade)

            item_valor = QTableWidgetItem(f"R$ {valor:.2f}")
            item_valor.setTextAlignment(Qt.AlignCenter)
            self.lista_itens.setItem(i, 2, item_valor)

            # Checkbox para selecionar o item
            checkbox = QCheckBox()
            self.lista_itens.setCellWidget(i, 3, checkbox)  # Use setCellWidget para adicionar o QCheckBox

            # Armazena o ID da venda no dicionário
            self.ids_vendas[i] = id_venda  # Mapeia o índice da linha para o ID da venda

            total_divida += valor  # Soma o valor total da dívida

        self.label_total_divida.setText(f"Total da Dívida: R$ {total_divida:.2f}")  # Atualiza o label com o total da dívida

    def marcar_pago(self):
        algum_selecionado = False  # Variável para verificar se algum checkbox foi selecionado

        for row in range(self.lista_itens.rowCount()):
            checkbox = self.lista_itens.cellWidget(row, 3)  # Agora isso deve retornar o QCheckBox
            if checkbox and checkbox.isChecked():  # Verifique se o checkbox não é None
                algum_selecionado = True  # Marque que pelo menos um checkbox foi selecionado
                produto = self.lista_itens.item(row, 0).text()
                quantidade = int(self.lista_itens.item(row, 1).text())
                id_venda = self.ids_vendas[row]  # Obtenha o ID da venda do dicionário
                data_pagamento = QDate.currentDate().toString("yyyy-MM-dd")
                
                # Inserir na tabela de pagamentos
                self.cursor.execute("""
                    INSERT INTO pagamentos (cliente, produto, quantidade, data_pagamento) 
                    VALUES (?, ?, ?, ?)
                """, (self.cliente, produto, quantidade, data_pagamento))
                
                # Atualizar a tabela de vendas para marcar como pago usando o ID
                self.cursor.execute("""
                    UPDATE vendas 
                    SET pago = 1 
                    WHERE id = ?
                """, (id_venda,))
        
        if algum_selecionado:
            self.conn.commit()
            backup_database()
            QMessageBox.information(self, "Sucesso", "Itens marcados como pagos com sucesso.")
            # Recarregar os itens após marcar como pago
            self.carregar_itens()
        else:
            QMessageBox.warning(self, "Erro", "Nenhum item selecionado para marcar como pago.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())