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
    print("3.fazer matricula")
    print("4.Sair")


def sorteio():
    from random import randint
    try:
        
        cont=1
        while cont<=13:
            n=randint(1,9)
            print(f"{n}",end=" ")
            cont+=1
    except Exception as erro:
        print(f"Infelizmente tivemos um erro. E o erro foi {erro}")


def menu_alunos():
    print("1.Listar alunos do curso de contablidade")
    print("2.Listar alunos do curso de informatica")
    print("3.Listar total de alunos cadastrados")


cadastrados=[] 
total_inscritos=[]
tot_aluno_da_contablidade=[]
tot_aluno_da_informatica=[]

