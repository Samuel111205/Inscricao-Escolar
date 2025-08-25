import banco
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
        salvar_notas_no_banco(self.nome, disciplina, trimestre, notas)
    
    def calcular_media_trimestral(self,disciplina,trimestre):
        if disciplina in self.notas and trimestre in self.notas[disciplina]:
            notas=self.notas[disciplina][trimestre]
            return sum(notas)/len(notas)
        salvar_notas_no_banco(self.nome,disciplina,trimestre,notas)
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
        salvar_notas_no_banco(self.nome,disciplina,trimestre,todas_medias)

    def mostrar_dados(self):
        print(f"Nome: {self.nome} | ",end="")
        print(f"Idade: {self.idade} | ",end="")
        print(f"Classe: {self.turma}ªClasse | ",end="")
        print(f"Curso: {self.curso} | ",end="")
        print(f"Disciplinas: {', '.join([d[0] for d in self.disciplinas]) if self.disciplinas else 'Nenhuma'}")
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
        #salvar_notas_no_banco(self.nome,disciplina,trimestre,notas)

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

# Listas globais
cadastrados = []
matriculas = []

# Funções de persistência

def salvar_alunos_no_banco():
    conn = banco.conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM aluno')
    for aluno in cadastrados:
        cursor.execute('''
            INSERT INTO aluno (nome, nascimento, idade, media, curso)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            aluno.nome,
            aluno._Pessoa__nascimento,
            aluno.idade,
            aluno.media,
            aluno.curso
        ))
    conn.commit()
    conn.close()
    

def carregar_alunos_do_banco():
    lista = []
    conn = banco.conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT nome, nascimento, idade, media, curso FROM aluno')
    for row in cursor.fetchall():
        nome, nascimento, idade, media, curso = row
        aluno = Aluno(nome, nascimento, idade, media, curso)
        lista.append(aluno)
    conn.close()
    return lista

def salvar_matriculas_no_banco():
    conn = banco.conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM matricula')
    for m in matriculas:
        cursor.execute('''
            INSERT INTO matricula (nome, nascimento, idade, turma, curso)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            m.nome,
            m._Pessoa__nascimento,
            m.idade,
            m.turma,
            m.curso
        ))
    conn.commit()
    conn.close()
    salvar_disciplinas_no_banco()


def carregar_matriculas_do_banco():
    lista = []
    conn = banco.conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT nome, nascimento, idade, turma, curso FROM matricula')
    for row in cursor.fetchall():
        nome, nascimento, idade, turma, curso = row
        disciplinas = carregar_disciplinas_aluno(nome)
        m = Matricula(nome, nascimento, idade, turma, curso,disciplinas)
        lista.append(m)
    conn.close()
    return lista

def salvar_disciplinas_no_banco():
    conn = banco.conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM aluno_disciplina')
    cursor.execute('DELETE FROM disciplina')
    disciplinas_set = set()
    for aluno in matriculas:
        for disciplina, turma in aluno.disciplinas:
            disciplinas_set.add((disciplina, turma))
            cursor.execute(
                'INSERT OR IGNORE INTO aluno_disciplina (aluno_nome, disciplina_nome, turma) VALUES (?, ?, ?)',
                (aluno.nome, disciplina, turma)
            )
    for disciplina, turma in disciplinas_set:
        cursor.execute(
            'INSERT OR IGNORE INTO disciplina (nome, turma) VALUES (?, ?)',
            (disciplina, turma)
        )
    conn.commit()
    conn.close()

def carregar_disciplinas_aluno(nome_aluno):
    conn = banco.conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT disciplina_nome, turma FROM aluno_disciplina WHERE aluno_nome=?', (nome_aluno,))
    disciplinas = [(row[0], row[1]) for row in cursor.fetchall()]
    conn.close()
    return disciplinas

def adicionar_disciplina_aluno(nome_aluno, disciplina, turma):
    aluno = next((a for a in matriculas if a.nome == nome_aluno), None)
    if aluno and (disciplina, turma) not in aluno.disciplinas:
        aluno.disciplinas.append((disciplina, turma))
        salvar_disciplinas_no_banco()
        print(f"Disciplina '{disciplina}' adicionada para {nome_aluno} na turma {turma}ª.")
    else:
        print("Aluno não encontrado ou disciplina já cadastrada para esta turma.")

def cadastrar_disciplina_por_turma():
    disciplina = input("Digite o nome da disciplina: ").strip().title()
    try:
        turma = int(input("Digite o número da turma: "))
    except ValueError:
        print("Turma inválida.")
        return
    conn = banco.conectar()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT OR IGNORE INTO disciplina (nome, turma) VALUES (?, ?)',
        (disciplina, turma)
    )
    conn.commit()
    conn.close()
    print(f"Disciplina '{disciplina}' cadastrada para a turma {turma}ª Classe.")


"""def salvar_notas_no_banco(nome_aluno, disciplina,trimestre,notas):
    conn=banco.conectar()
    cursor=conn.cursor()
    #media = sum(notas) / len(notas)
    try:
        cursor.execute("ALTER TABLE aluno_nota ADD COLUMN nota3 REAL")
    except s.OperationalError:
        pass
    
    cursor.execute(
        "INSERT  OR REPLACE INTO aluno_nota (aluno_nome, disciplina, trimestre, nota1, nota2, nota3) VALUES (?, ?, ?, ?, ?, ?)",
        (nome_aluno, disciplina, trimestre, notas[0], notas[1], notas[2])
    )
    conn.commit()
    conn.close()"""
        
def salvar_notas_no_banco(nome_aluno, disciplina, trimestre, notas):
    conn = banco.conectar()
    cursor = conn.cursor()
    # Remove notas antigas desse aluno/disciplina/trimestre
    cursor.execute("""
        DELETE FROM notas WHERE nome_aluno=? AND disciplina=? AND trimestre=?
    """, (nome_aluno, disciplina, trimestre))
    # Insere as três notas novas
    for i, valor in enumerate(notas, 1):
        cursor.execute("""
            INSERT INTO notas (nome_aluno, disciplina, trimestre, numero_nota, nota)
            VALUES (?, ?, ?, ?, ?)
        """, (nome_aluno, disciplina, trimestre, i, valor))
    conn.commit()
    conn.close()


def consultar_notas_do_aluno(nome_aluno):
    conn = banco.conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT disciplina, trimestre, nota1, nota2, nota3 FROM aluno_nota WHERE aluno_nome = ? ORDER BY disciplina, trimestre",
        (nome_aluno,)
    )
    resultados = cursor.fetchall()
    conn.close()
    if resultados:
        for disciplina, trimestre, n1, n2, n3 in resultados:
            print(f"Disciplina: {disciplina} - {trimestre}: Notas = {n1}, {n2}, {n3}")
    else:
        print("Nenhuma nota cadastrada para este aluno.")


def mostrar_notas_do_banco():
    conn = banco.conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nome_aluno, disciplina, trimestre, numero_nota, nota
        FROM aluno_nota
        ORDER BY nome_aluno, disciplina, trimestre, numero_nota
    """)
    resultados = cursor.fetchall()
    conn.close()
    
    if resultados:
        print("\n=== Tabela de Notas e Médias ===")
        ultimo_aluno = ""
        ultima_disciplina = ""
        notas_disciplina = []
        for nome_aluno, disciplina, trimestre, numero_nota, nota in resultados:
            # Mudança de aluno
            if nome_aluno != ultimo_aluno:
                if notas_disciplina:
                    # Média final da disciplina anterior
                    media_final = sum(notas_disciplina) / len(notas_disciplina)
                    print(f"      Média final: {media_final:.2f}")
                    notas_disciplina = []
                print(f"\nAluno: {nome_aluno}")
                ultimo_aluno = nome_aluno
                ultima_disciplina = ""
            # Mudança de disciplina
            if disciplina != ultima_disciplina:
                if notas_disciplina:
                    media_final = sum(notas_disciplina) / len(notas_disciplina)
                    print(f"      Média final: {media_final:.2f}")
                    notas_disciplina = []
                print(f"  Disciplina: {disciplina}")
                ultima_disciplina = disciplina
            # Agrupa notas para cálculo de média
            notas_trimestre = []
            print(f"    {trimestre}: ", end="")
            for nt in [1,2,3]:
                nota_reg = next((n for na, di, tri, num, n in resultados if na==nome_aluno and di==disciplina and tri==trimestre and num==nt), None)
                if nota_reg is not None:
                    print(f"[N{nt}: {nota_reg}] ", end="")
                    notas_trimestre.append(nota_reg)
                    notas_disciplina.append(nota_reg)
            if notas_trimestre:
                media_tri = sum(notas_trimestre) / len(notas_trimestre)
                print(f"| Média do trimestre: {media_tri:.2f}")
            else:
                print()
        # Média final da última disciplina
        if notas_disciplina:
            media_final = sum(notas_disciplina) / len(notas_disciplina)
            print(f"      Média final: {media_final:.2f}")
        print("\n=== Fim da tabela ===")
    else:
        print("Nenhuma nota registrada no banco.")

    
def listar_alunos_por_disciplina(disciplina_nome):
    conn = banco.conectar()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT aluno_nome, turma FROM aluno_disciplina WHERE disciplina_nome=?',
        (disciplina_nome,)
    )
    dados = cursor.fetchall()
    if not dados:
        print(f"Nenhum aluno encontrado na disciplina '{disciplina_nome}'.")
    else:
        print(f"Alunos na disciplina '{disciplina_nome}':")
        for nome, turma in dados:
            aluno = next((a for a in matriculas if a.nome == nome), None)
            if aluno:
                print(f"Nome: {aluno.nome} | Turma: {turma}ª | Curso: {aluno.curso} | Idade: {aluno.idade}")
    conn.close()

def listar_alunos_por_turma(turma_num):
    conn = banco.conectar()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT nome FROM matricula WHERE turma=?',
        (turma_num,)
    )
    nomes = [row[0] for row in cursor.fetchall()]
    if not nomes:
        print(f"Nenhum aluno encontrado na turma {turma_num}ª Classe.")
    else:
        print(f"Alunos na turma {turma_num}ª Classe:")
        for nome in nomes:
            aluno = next((a for a in matriculas if a.nome == nome), None)
            if aluno:
                print(f"- {aluno.nome} | Curso: {aluno.curso} | Idade: {aluno.idade}")
    conn.close()

def listar_disciplinas_disponiveis():
    conn = banco.conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT nome, turma FROM disciplina ORDER BY turma, nome')
    disciplinas = cursor.fetchall()
    conn.close()
    if not disciplinas:
        print("Nenhuma disciplina cadastrada.")
    else:
        print("Disciplinas disponíveis (por turma):")
        for nome, turma in disciplinas:
            print(f"- {nome} (Turma: {turma}ª)")

def listar_turmas_disponiveis():
    conn = banco.conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT turma FROM matricula ORDER BY turma')
    turmas = [row[0] for row in cursor.fetchall()]
    conn.close()
    if not turmas:
        print("Nenhuma turma cadastrada.")
    else:
        print("Turmas disponíveis:")
        for t in turmas:
            print(f"- {t}ª Classe")

def remover_aluno(nome_aluno):
    global cadastrados
    aluno = next((a for a in matriculas if a.nome == nome_aluno), None)
    if not aluno:
        print("Aluno não encontrado.")
        return
    aluno = [a for a in matriculas if a.nome != nome_aluno]
    # Remove do banco
    conn = banco.conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM aluno WHERE nome=?', (nome_aluno,))
    cursor.execute('DELETE FROM aluno_disciplina WHERE aluno_nome=?', (nome_aluno,))
    cursor.execute('DELETE FROM matricula WHERE nome=?', (nome_aluno,))
    conn.commit()
    conn.close()
    salvar_alunos_no_banco()
    salvar_matriculas_no_banco()
    print(f"Aluno {nome_aluno} removido com sucesso.")

def editar_aluno(nome_aluno):
    aluno = next((a for a in matriculas if a.nome == nome_aluno), None)
    if not aluno:
        print("Aluno não encontrado.")
        return
    print("Deixe em branco para manter o valor atual.")
    novo_nome = input(f"Novo nome [{aluno.nome}]: ").strip().title()
    novo_nascimento = input(f"Novo ano de nascimento [{aluno._Pessoa__nascimento}]: ").strip()
    try:
        nova_idade = input(f"Nova idade [{aluno.idade}]: ").strip()
        nova_idade = int(nova_idade) if nova_idade else aluno.idade
    except ValueError:
        print("Idade inválida. Mantendo valor anterior.")
        nova_idade = aluno.idade
    novo_curso = input(f"Novo curso [{aluno.curso}]: ").strip().capitalize() or aluno.curso
    try:
        nova_media = input(f"Nova média [{aluno.media:.2f}]: ").strip()
        nova_media = float(nova_media) if nova_media else aluno.media
    except ValueError:
        print("Média inválida. Mantendo valor anterior.")
        nova_media = aluno.media

    # Atualiza dados
    old_nome = aluno.nome
    aluno.nome = novo_nome or aluno.nome
    aluno._Pessoa__nascimento = novo_nascimento or aluno._Pessoa__nascimento
    aluno.idade = nova_idade
    aluno.curso = novo_curso
    aluno.media = nova_media

    # Atualiza no banco
    conn = banco.conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE aluno SET nome=?, nascimento=?, idade=?, media=?, curso=?
        WHERE nome=?
    ''', (aluno.nome, aluno._Pessoa__nascimento, aluno.idade, aluno.media, aluno.curso, old_nome))
    # Atualiza nome nas relações
    if aluno.nome != old_nome:
        cursor.execute('UPDATE aluno_disciplina SET aluno_nome=? WHERE aluno_nome=?', (aluno.nome, old_nome))
        cursor.execute('UPDATE matricula SET nome=? WHERE nome=?', (aluno.nome, old_nome))
    conn.commit()
    conn.close()
    salvar_alunos_no_banco()
    salvar_matriculas_no_banco()
    print(f"Aluno '{old_nome}' atualizado com sucesso.")



