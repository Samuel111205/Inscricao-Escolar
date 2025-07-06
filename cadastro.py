#class Mãe 
class Pessoa:
    def __init__(self,nome,nascimento,idade,media):
        self.nome=nome
        self.__nascimento=nascimento
        self.idade=idade
        self.media=media
    def mostrar_dados(self):
        print("Mostrar os dados do Aluno! ")


#subclasse aluno que herda da classe mãe pessoa 
class Aluno(Pessoa):
    def __init__(self,nome,nascimento,idade,media,curso):
        super().__init__(nome,nascimento,idade, media)
        self.curso=curso
    def mostrar_dados(self):
        print(f"Nome: {self.nome}")
        print(f"Idade: {self.idade}")
        print(f"Media: {self.media}")
        print(f"Curso: {self.curso}")


#sublcasse matricula que herda da classe mãe pessoa
class Matricula(Pessoa):
    def __init__(self, nome, nascimento, idade,classe,media):
        super().__init__(nome, nascimento, idade,media,)
        self.classe=classe
    def mostrar_dados(self):
        print(f"Nome: {self.nome}")
        print(f"Idade: {self.idade}")
        print(f"Classe: {self.classe}ªClasse")
        print(f"Curso: {self.media}")
    
#função que exibe o menu de opções
def menu():
    print("===SISTEMA DE INSCRIÇÃO===")
    print("1.Gerenciamentos de cadastro")
   

def menu_cadastro():
    print("1.Cadastrar alunos")
    print("2.Listar alunos cadastrados")
    print("3.Lisatr alunos não cadastrados")
    print("4.Fazer Matricula")
    print("5.Calcular total de inscrito")
    print("6.Sair")


cadastrados=[]#lista que armazena os alunos cadastrados
nao_cadastradas=[]#lista que armazena os alunos não cadastradas 
total_inscritos=[]#lista que armazena o numero total de pessoas incritas
