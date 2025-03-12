import sys
import bcrypt
import sqlite3
import os
import shutil
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox, QLineEdit, QDesktopWidget, QHBoxLayout, QApplication
from PyQt5.QtGui import QIcon
from main import SistemaVendas

def get_database_path():
    """Garante que o banco de dados esteja acessível diretamente do diretório de instalação."""
    # Caminho absoluto do banco de dados
    packaged_db_path = "C:/Program Files (x86)/Controle de Vendas Fabio Pipas & RBShop/banco_de_dados/sistema_vendas.db"
    alternative_db_path = "C:/Program Files/Controle de Vendas Fabio Pipas & RBShop/banco_de_dados/sistema_vendas.db"

    # Verifica se o banco de dados existe no caminho original
    if os.path.exists(packaged_db_path):
        return packaged_db_path  # Retorna o caminho original se existir

    # Se não existir, verifica o caminho alternativo
    if os.path.exists(alternative_db_path):
        return alternative_db_path  # Retorna o caminho alternativo se existir

    # Se nenhum dos caminhos existir, exibe uma mensagem de erro
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
        if os.path.exists(db_path_x86):
            db_path_to_use = db_path_x86  # Usa o caminho x86 se existir
        else:
            print(f"Banco de dados não encontrado em: {db_path_x86}")

        # Verifica se o banco de dados existe no caminho alternativo
        if os.path.exists(db_path):
            db_path_to_use = db_path  # Usa o caminho alternativo se existir
        else:
            print(f"Banco de dados não encontrado em: {db_path}")

        # Se nenhum dos caminhos for encontrado, levanta uma exceção
        if db_path_to_use is None:
            raise FileNotFoundError("O banco de dados não foi encontrado em nenhum dos caminhos especificados.")

        # Se o arquivo de backup já existir, exclua-o
        if os.path.exists(backup_file):
            os.remove(backup_file)

        # Copia o banco de dados para o diretório de backup
        shutil.copy(db_path_to_use, backup_file)
    except Exception as e:
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
        """Verifica se o usuário e a senha estão corretos."""
        conn = None
        try:
            conn = sqlite3.connect(get_database_path())
            cursor = conn.cursor()
            user = self.get_user(cursor, username)
            
            if user is None:
                print("Usuário não encontrado.")
                return False
            
            if self.check_password(password, user[0]):
                return True
            else:
                print("Senha incorreta.")
                return False
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro de Banco de Dados", f"Erro ao acessar o banco de dados: {e}")
            return False
        finally:
            if conn is not None:
                conn.close()

    def get_user(self, cursor, username):
        """Obtém o usuário do banco de dados."""
        cursor.execute("SELECT password FROM usuarios WHERE username = ?", (username,))
        return cursor.fetchone()

    def check_password(self, password, hashed_password):
        """Verifica se a senha fornecida corresponde à senha armazenada."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())