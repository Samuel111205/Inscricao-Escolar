import cadastro 
from datetime import date
import sqlite3


def conectar_banco():
    try:
        conn=sqlite3.connect("escola.db")
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados {e}")
        return None


def criar_tabelas():
    conn=conectar_banco()
    cursor=conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS cursos(
                id INEGER PRIMARY KEY AUOINCREMENT,
                nome TEXT NOT NULL UNIQUE)
                """)

 # função que cadastra um aluno
def cadastrar_aluno():
    print("\n--- Cadastro de Aluno ---")
    nome = input("Nome do aluno: ").strip().title()
    nascimento = int(input("Ano de nascimento: "))
    idade = date.today().year-nascimento
    try:
        media=float(input("Media do certificado: "))
    except ValueError:
        print("Media Invalida")
    # Escolha do curso com validação
    while True:
        curso = input("Curso (Informática/Contabilidade): ").strip().capitalize()
        if curso in ["Informatica", "Contabilidade"]:
            break
        print("Curso inválido! Tente novamente.")
     #criando o objecto da classe do modlo cadastro
    aluno = cadastro.Aluno(nome, nascimento, idade, media, curso)
      # Regras de aceitação
    if idade < 14 or idade > 18:
        print("Idade fora da faixa permitida (14 a 25 anos). Cadastro não realizado.")
        return None
    if media < 10 or media > 20:
        print("Média fora da faixa permitida (10 a 20). Cadastro não realizado.")
        return None
     #if 14<idade<=18 and 10>=media<=20:
    cadastro.cadastrados.append(aluno)
    cadastro.total_inscritos.append(aluno)
    if curso == "Contabilidade":
        cadastro.tot_aluno_da_contabilidade.append(aluno)
    else:
        cadastro.tot_aluno_da_informatica.append(aluno)
    print("Aluno cadastrado com sucesso!\n")
    return aluno

 # função que listas os alunos cadastrados
def listar_alunos():
    print("\n--- Alunos Cadastrados ---")
    if not cadastro.cadastrados:
        print("Nenhum aluno cadastrado.")
        return
    else:
        for i in cadastro.cadastrados:
            # print(f"E no geral foram cadastradas {len(cadastro.cadastrados)} alunos que são: ")
            i.mostrar_dados()
    print("-" * 30)

 # função para listar alunos por curso
def listar_alunos_por_curso():
    print("\n[1] Informática\n[2] Contabilidade")
    escolha = input("Escolha o curso: ").strip()
    if escolha == "1":
        alunos = cadastro.tot_aluno_da_informatica
        curso = "Informática"
    elif escolha == "2":
        alunos = cadastro.tot_aluno_da_contabilidade
        curso = "Contabilidade"
    else:
        print("Opção de curso inválida.")
        return
    print(f"\n--- Alunos do curso de {curso} ---")
    if alunos:
        for aluno in alunos:
            aluno.mostrar_dados()
            print("-" * 30)
    else:
        print("Nenhum aluno cadastrado neste curso.")

 # função para fazer a matricula
def fazer_matricula():
    nome=input("Digite o nome do aluno a ser matriculado: ").strip().title()
    aluno=next((a for a in cadastro.cadastrados if a.nome==nome),None)
    if not aluno: # consulta se o aluno esta inscrito, se estiver cadastrado, ele fara a matricula
        print("Aluno não encotrado")
        return
    pagamento=input("Pagamento(Sim/Não): ").capitalize()
    while True:
        if pagamento=="Sim":
            try:
                turma=int(input("Digite a turma/Classe: "))
            except ValueError:
                print("Turma invalida. Digie um numero: ")
                return
            for m in cadastro.matriculados:
                if m.nome==aluno.nome and m.turma==turma and m.curso==aluno.curso:
                    print("Este aluno ja esta matriculado nesta classe e curso")
                    return
            matricula=cadastro.Matricula(aluno.nome,aluno._Pessoa__nascimento,aluno.idade,turma,aluno.curso)
            cadastro.matriculados.append(matricula)
            if aluno.curso=="Informatica":
                cadastro.matricula_da_informatica.append(matricula)
            if aluno.curso=="Contabilidade":
                cadastro.matricula_da_contabilidade.append(matricula)
            print(f"Matricula realizada para o aluno {aluno.nome} na turma {turma} classe do curso de {aluno.curso}")
            break
        if pagamento=="Nao":
            print("Para continuares o processo de maricula tens de fazer o pagamento do rupe no seguinte numero: ",end=" ")
            print(f"{cadastro.sorteio()}")
            break
        else:
            print("Resposta errada por favor digite Sim/Não")
            pagamento=input("Pagamento (Sim/Não): ").strip().capitalize()


 # função para registrar as disciplinas do aluno matriculado
def adicionar_disciplinas(aluno):
    print("\n--- Adicionar Disciplinas ---")
    while True:
        disciplina = input("Digite o nome da disciplina (ou pressione Enter para finalizar): ").strip().title()
        if not disciplina:
            break
        if disciplina not in aluno.disciplinas:
            aluno.disciplinas.append(disciplina)
            print(f"Disciplina '{disciplina}' adicionada.")
        else:
            print("Disciplina já cadastrada para este aluno.")

 # funcão para listar os alunos de cada disciplina
def listar_alunos_por_disciplina():
    disciplina_busca = input("\nDigite o nome da disciplina: ").strip().title()
    encontrados = [aluno for aluno in cadastro.matriculados if disciplina_busca in aluno.disciplinas]
    if encontrados:
        print(f"\nAlunos matriculados em {disciplina_busca}:")
        for aluno in encontrados:
            aluno.mostrar_dados()
            print('-' * 30)
    else:
        print("Nenhum aluno matriculado nesta disciplina.")


def listar_alunos_matriculados():
    if not cadastro.matriculados:
        print("Nenhum aluno matriculado")
        return
    else:
        print("---Lista de matriculados")
        for i in cadastro.matriculados:
            i.mostrar_dados()
        print("--"*0)


def adicionar_notas_trimestrais(aluno):
    print("\n---Adicionar Notas Trimestrais--- ")
    if not aluno.disciplinas:
        print("Esta aluno não possui nenhuma disciplina cadastradas")
        return
    for disciplina in aluno.disciplinas:
        print(f"\n discipplina: {disciplina}")
        for trimestre in ["1º Trimestre","2º Trimestre","3º Trimestre"]:
            print(f"{trimestre}")
            try:
                notas=[]
                for i in range(1,4):
                    nota=float(input(f"Nota {i}: "))
                    notas.append(nota)
                aluno.adicionar_nota(disciplina,trimestre,notas)
            except ValueError:
                print("Erro digite apenas numeros para notas")
                return

 
def menu_principal():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Cadastrar aluno")
        print("2. Listar alunos cadastrados")
        print("3.Fazer matricula")
        print("4.listar alunos matriculados")
        print("5. Listar alunos cadastrados por curso")
        print("6. Adicionar disciplinas a um aluno")
        print("7. Adicionar notas trimestrais")
        print("8. Listar alunos por disciplina")
        print("9. Sair")
        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Opção inválida! Digite apenas números.")
            continue

        if opcao == 1:
            cadastrar_aluno()
        elif opcao == 2:
            listar_alunos()
        elif opcao==3:
            aluno=fazer_matricula()
            if aluno:
               adicionar_disciplinas(aluno)
        elif opcao==4:
            listar_alunos_matriculados()
        elif opcao == 5:
            listar_alunos_por_curso()
        elif opcao == 6:
            nome = input("Digite o nome do aluno: ").strip().title()
            aluno = next((a for a in cadastro.matriculados if a.nome == nome), None)
            if aluno:
                adicionar_disciplinas(aluno)
            else:
                print("Aluno não encontrado.")
        elif opcao==7:
            nome=input("Digite o nome do aluno: ").strip().title()
            aluno=next((a for a in cadastro.matriculados if a.nome==nome),None)
            if aluno:
                adicionar_notas_trimestrais(aluno)
            else:
                print("Aluno não encotrado.")
        elif opcao == 8:
            listar_alunos_por_disciplina()
        elif opcao == 9:
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida! Digite um número entre 1 e 6.")

if __name__ == "__main__":
    menu_principal()
