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
    def __init__(self, nome, nascimento, idade,classe,curso):
        # Aqui, "media" não faz sentido para a matricula, então substitui por curso
        super().__init__(nome, nascimento, idade,None)
        self.classe=classe
        self.curso=curso

    def mostrar_dados(self):
        print(f"Nome: {self.nome}")
        print(f"Idade: {self.idade}")
        print(f"Classe: {self.classe}ªClasse")
        print(f"Curso: {self.curso}")


#função que exibe o menu de opções
def menu():
    print("===SISTEMA DE INSCRIÇÃO===")
    print("1.Gerenciamentos de cadastro")
    print("2.Gerenciamento do aluno")


def menu_cadastro():
    print("1.Cadastrar alunos")
    print("2.Listar alunos cadastrados")
    print("3.fazer matricula")
    print("4.Sair")


def sorteio():
    from random import randint
    try:
        codigo=" " 
        for _ in range(13):
            n=randint(0,9)
            #print(f"{n}",end=" ")
            codigo+=str(n)
        print()
        return codigo
    except Exception as erro:
        print(f"Infelizmente tivemos um erro. E o erro foi {erro}")


def menu_alunos():
    print("1.Listar alunos do curso de contablidade")
    print("2.Listar alunos do curso de informatica")
    print("3.Listar total de alunos cadastrados")
    print("4.Sair do menu")

def menu_escolha_outtro_curso():
    print("1.Informatica")
    print("2.contabilidade")


def menu_gerenciameno_de_alnos():
    print("1.Gerenciar alunos do curso de Informatica")
    print("2.Gerenciar alnos do curso de conabilidade")
    print("3.Mostrar a media final do aluno")


cadastrados=list()
total_inscritos=list()
tot_aluno_da_contabilidade=list()
tot_aluno_da_informatica=list()
ficha=list()
