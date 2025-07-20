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
    def __init__(self, nome, nascimento, idade, media, curso):
        super().__init__(nome, nascimento, idade, media)
        self.curso = curso
        
    def mostrar_dados(self):
        print(f"Nome: {self.nome}")
        print(f"Idade: {self.idade}")
        print(f"Media: {self.media:.2f}")
        print(f"Curso: {self.curso}")

#sublcasse matricula que herda da classe mãe pessoa
class Matricula(Pessoa):
    def __init__(self, nome, nascimento, idade,turma,curso,disciplinas=None):
        # Aqui, "media" não faz sentido para a matricula, então substitui por curso
        super().__init__(nome, nascimento, idade,None)
        self.turma=turma
        self.curso=curso
        self.disciplinas = disciplinas if disciplinas is not None else []
        self.notas={}
    
    def adicionar_nota(self,disciplina,trimestre,notas):
        if disciplina not in self.notas:
            self.notas[disciplina]={}
        self.notas[disciplina][trimestre]=notas
    
    def calcular_media_trimestral(self,disciplina,trimestre):
        if disciplina in self.notas and trimestre in self.notas[disciplina]:
            notas=self.notas[disciplina][trimestre]
            return sum(notas)/len(notas)
        return 0
    
    def calcular_media_final(self,disciplina):
        if disciplina in self.notas:
            todas_medias=[]
            for trimestre in self.notas[disciplina]:
                media=self.calcular_media_trimestral(disciplina,trimestre)
                todas_medias.append(media)
            if todas_medias:
                return sum(todas_medias)/len(todas_medias)
            return 0

    def mostrar_dados(self):
        print(f"Nome: {self.nome}")
        print(f"Idade: {self.idade}")
        print(f"Classe: {self.turma}ªClasse")
        print(f"Curso: {self.curso}")
        print(f"Disciplinas: {', '.join(self.disciplinas) if self.disciplinas else 'Nenhuma'}")
        if self.notas:
            for disciplina in self.notas:
                print(f"Notas da disciplina {disciplina}: ")
                for trimestre, notas in self.notas[disciplina].items():
                    media_tri=self.calcular_media_trimestral(disciplina,trimestre)
                    print(f"{trimestre}: Notas={notas}, Media={media_tri:.2f}")
                media_final=self.calcular_media_final(disciplina)
                print(f"Media final de {disciplina}: {media_final:.2f}")
                if media_final<10:
                    print("Aluno REPROVADO")
                else:
                    print("Aluno APROVADO")

# Função para gerar código de matrícula ()
def sorteio():
    from random import randint
    try:
        codigo = ""
        for _ in range(13):
            codigo += str(randint(0, 9))
        return codigo
    except Exception as erro:
        print(f"Erro ao gerar código: {erro}")


cadastrados=[]
total_inscritos=[]
tot_aluno_da_contabilidade=[]
tot_aluno_da_informatica=[]
ficha=[]
matriculados=[]
matricula_da_informatica=[]
matricula_da_contabilidade=[]
