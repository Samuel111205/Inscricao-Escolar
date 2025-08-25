import cadastro 
from datetime import date
import banco

cadastro.cadastrados=cadastro.carregar_alunos_do_banco()
cadastro.matriculas=cadastro.carregar_matriculas_do_banco()
banco.criar_tabelas()
# Função que cadastra um aluno
def cadastrar_aluno():
    print("\n--- Cadastro de Aluno ---")
    nome = input("Nome do aluno: ").strip().title()
    try:
        nascimento = int(input("Ano de nascimento: "))
    except ValueError:
        print("Ano de nascimento inválido!")
        return None
    idade = date.today().year - nascimento
    try:
        media = float(input("Média do certificado: "))
    except ValueError:
        print("Média inválida!")
        return None
    # Escolha do curso com validação
    while True:
        curso = input("Curso (Informática/Contabilidade): ").strip().capitalize()
        if curso in ["Informática", "Contabilidade"]:
            break
        print("Curso inválido! Tente novamente.")
    # Regras de aceitação
    if idade < 14 or idade > 18:
        print("Idade fora da faixa permitida (14 a 18 anos). Cadastro não realizado.")
        return None
    if media < 10 or media > 20:
        print("Média fora da faixa permitida (10 a 20). Cadastro não realizado.")
        return None
    aluno = cadastro.Aluno(nome, nascimento, idade, media, curso)
    cadastro.cadastrados.append(aluno)
    cadastro.salvar_alunos_no_banco()
    print("Aluno cadastrado com sucesso!\n")
    return aluno

 # função que listas os alunos cadastrados
def listar_alunos():
    print("\n--- Alunos Cadastrados ---")
    if not cadastro.cadastrados:
        print("Nenhum aluno cadastrado.")
        return
    for i in cadastro.cadastrados:
        i.mostrar_dados()
    print("-" * 30)

# Função para listar alunos por curso
def listar_alunos_por_curso():
    print("\n[1] Informática\n[2] Contabilidade")
    escolha = input("Escolha o curso: ").strip()
    if escolha == "1":
        curso = "Informática"
    elif escolha == "2":
        curso = "Contabilidade"
    else:
        print("Opção de curso inválida.")
        return
    alunos = [a for a in cadastro.cadastrados if a.curso == curso]
    print(f"\n--- Alunos do curso de {curso} ---")
    if alunos:
        for aluno in alunos:
            aluno.mostrar_dados()
            print("-" * 30)
    else:
        print("Nenhum aluno cadastrado neste curso.")

# Função para fazer a matrícula
def fazer_matricula():
    nome = input("Digite o nome do aluno a ser matriculado: ").strip().title()
    aluno = next((a for a in cadastro.cadastrados if a.nome == nome), None)
    if not aluno:
        print("Aluno não encontrado")
        return None
    pagamento = input("Pagamento (Sim/Não): ").strip().capitalize()
    while True:
        if pagamento == "Sim":
            try:
                turma = int(input("Digite a turma/Classe: "))
            except ValueError:
                print("Turma inválida. Digite um número.")
                return None
            for m in cadastro.matriculas:
                if m.nome == aluno.nome and m.turma == turma and m.curso == aluno.curso:
                    print("Este aluno já está matriculado nesta classe e curso")
                    return None
            matricula = cadastro.Matricula(aluno.nome, aluno._Pessoa__nascimento, aluno.idade, turma, aluno.curso)
            cadastro.matriculas.append(matricula)
            cadastro.salvar_matriculas_no_banco()
            print(f"Matrícula realizada para o aluno {aluno.nome} na turma {turma} do curso de {aluno.curso}")
            break
        elif pagamento == "Não":
            print("Para continuar o processo de matrícula, faça o pagamento do rupe no seguinte número:", end=" ")
            print(f"{cadastro.sorteio()}")
            return None
        else:
            print("Resposta errada, por favor digite Sim/Não")
            pagamento = input("Pagamento (Sim/Não): ").strip().capitalize()

 # função para registrar as disciplinas do aluno matriculado
def adicionar_disciplinas():
    listar_alunos_matriculados()
    print("\n--- Adicionar Disciplinas ---")
    nome = input("Digite o nome do aluno: ").strip().title()
    aluno = next((a for a in cadastro.matriculas if a.nome == nome), None)
    while True:
        disciplina = input("Digite o nome da disciplina (ou pressione Enter para finalizar): ").strip().title()
        if not disciplina:
            break
        if disciplina not in aluno.disciplinas:
            aluno.disciplinas.append(disciplina)
            print(f"Disciplina '{disciplina}' adicionada.")
        else:
            print("Disciplina já cadastrada para este aluno.")
    cadastro.salvar_matriculas_no_banco()

 # funcão para listar os alunos de cada disciplina
def listar_alunos_por_disciplina():
    disciplina_busca = input("\nDigite o nome da disciplina: ").strip().title()
    encontrados = [aluno for aluno in cadastro.matriculas if disciplina_busca in aluno.disciplinas]
    if encontrados:
        print(f"\nAlunos matriculados em {disciplina_busca}:")
        for aluno in encontrados:
            aluno.mostrar_dados()
            print('-' * 30)
    else:
        print("Nenhum aluno matriculado nesta disciplina.")

def listar_alunos_matriculados():
    if not cadastro.matriculas:
        print("Nenhum aluno matriculado")
        return
    print("--- Lista de matriculados ---")
    for i in cadastro.matriculas:
        i.mostrar_dados()
    print("--" * 10)


"""def adicionar_notas():
    print("\n---Adicionar Notas Trimestrais--- ")
    nome=input("Digite o nome do aluno: ").strip().capitalize()
    aluno=next((a for a in cadastro.matriculas if a.nome==nome),None)
    if not aluno:
        print("Aluno não encotrado")
        return
    if not aluno.disciplinas:
        print("Este aluno não possui nenhuma disciplina cadastradas")
        return
    print("1.Adicionar nota do primeiro trimestre\n2.Adicionar notas dos segundo trimestre\n3.Adicionar notas do terceiro trimestre")
    opcao=int(input("Digite a sua opção: "))

    if opcao==1:
        for disciplina, turma in aluno.disciplinas:
            print(f"\n discipplina: {disciplina} (Turma {turma})")
            for trimestre in ["1º Trimestre"]:
                print(f"{trimestre}")
                notas=[]
                for i in range(1,4):
                    try:
                        nota=float(input(f"Nota {i}: "))
                        notas.append(nota)
                    except ValueError:
                        print("Nota invalida. digite apenas numeros.")
                        return
        aluno.adicionar_nota(disciplina,trimestre,notas)
        cadastro.salvar_notas_no_banco(aluno.nome, disciplina,trimestre,notas)
        cadastro.salvar_matriculas_no_banco()
        print("Notas adicionadas com sucesso.")
    
    elif opcao==2:
        for disciplina, turma in aluno.disciplinas:
            print(f"\n discipplina: {disciplina} (Turma {turma})")
            for trimestre in ["2º Trimestre"]:
                print(f"{trimestre}")
                notas=[]
                for i in range(1,4):
                    try:
                        nota=float(input(f"Nota {i}: "))
                        notas.append(nota)
                    except ValueError:
                        print("Nota invalida. digite apenas numeros.")
                        return
        aluno.adicionar_nota(disciplina,trimestre,notas)
        cadastro.salvar_notas_no_banco(aluno.nome, disciplina,trimestre,notas)
        cadastro.salvar_matriculas_no_banco()
        print("Notas adicionadas com sucesso.")
    
    elif opcao==3:
        for disciplina, turma in aluno.disciplinas:
            print(f"\n discipplina: {disciplina} (Turma {turma})")
            for trimestre in ["3º Trimestre"]:
                print(f"{trimestre}")
                notas=[]
                for i in range(1,4):
                    try:
                        nota=float(input(f"Nota {i}: "))
                        notas.append(nota)
                    except ValueError:
                        print("Nota invalida. digite apenas numeros.")
                        return
        aluno.adicionar_nota(disciplina,trimestre,notas)
        cadastro.salvar_notas_no_banco(aluno.nome, disciplina,trimestre,notas)
        cadastro.salvar_matriculas_no_banco()
        print("Notas adicionadas com sucesso.") """


def adicionar_notas():
    print("\n--- Adicionar Notas Trimestrais --- ")
    nome = input("Digite o nome do aluno: ").strip().title()
    aluno = next((a for a in cadastro.matriculas if a.nome == nome), None)
    if not aluno:
        print("Aluno não encontrado.")
        return
    if not aluno.disciplinas:
        print("Este aluno não possui nenhuma disciplina cadastrada.")
        return
    print("1. Adicionar nota do primeiro trimestre\n2. Adicionar nota do segundo trimestre\n3. Adicionar nota do terceiro trimestre")
    try:
        opcao = int(input("Digite a sua opção: "))
    except ValueError:
        print("Opção inválida.")
        return

    if opcao in [1, 2, 3]:
        trimestre = f"{opcao}º Trimestre"
        for disciplina in aluno.disciplinas:
            print(f"\nDisciplina: {disciplina}")
            notas = []
            for i in range(1, 4):
                try:
                    nota = float(input(f"Nota {i}: "))
                    notas.append(nota)
                except ValueError:
                    print("Nota inválida. Digite apenas números.")
                    return
            aluno.adicionar_nota(disciplina, trimestre, notas)
            cadastro.salvar_notas_no_banco(aluno.nome, disciplina, trimestre, notas)
        cadastro.salvar_matriculas_no_banco()
        print("Notas adicionadas com sucesso.")
    else:
        print("Opção inválida.")



def consultar_por_turma():
    try:
        turma = int(input("Digite o número da turma: "))
    except ValueError:
        print("Valor inválido")
        return
    curso = input("Digite o curso (Informática/Contabilidade): ").strip().capitalize()
    if curso not in ["Informática", "Contabilidade"]:
        print("Curso inválido")
        return
    alunos = [a for a in cadastro.matriculas if a.turma == turma and a.curso == curso]
    if alunos:
        print(f"Alunos da turma {turma} do curso de {curso}")
        for aluno in alunos:
            aluno.mostrar_dados()
            print("-" * 30)
    else:
        print("Nenhum aluno encontrado para esses critérios.")


def gerar_boletim():
    nome=input("Digite o nome do aluno: ").strip().title()
    aluno=next((a for a in cadastro.matriculas if a.nome==nome), None)
    if not aluno:
        print("Aluno não encotrado.")
        return
    if not aluno.notas:
        print("Nenhuma nota registrada para este aluno")
        return
    print(f"\n---Boletim do aluno {aluno.nome}")
    for disciplina in aluno.notas:
        print(f"\n Disciplina {disciplina}")
        for trimestre, notas in aluno.notas[disciplina].items():
            media_tri=aluno.calcular_media_trimestral(disciplina,trimestre)
            print(f"{trimestre}: Notas= {notas} | Media={media_tri:.2f}")
        media_final=aluno.calcular_media_final(disciplina)
        print(f"Media final: {media_final:.2f}")
        print("Situação: ","Aprovado" if media_final>=10 else "Reprovado")

def mostrar_todas_notas():
    cadastro.mostrar_notas_do_banco()

def menu_principal():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Cadastrar aluno")
        print("2. Listar alunos cadastrados")
        print("3. Fazer matrícula")
        print("4. Adicionar disciplinas ao aluno")
        print("5. Listar alunos cadastrados por curso")
        print("6. Adicionar notas trimestrais")
        print("7. Consultar alunos por turma e curso")
        print("8. Gerar boletim")
        print("9. Listar alunos matriculados")
        print("10. Remover aluno")
        print("11. Listar alunos por disciplina")
        print("12. Consultar notas de um aluno")
        print("13. Consultar todas as notas no banco")
        print("14. Sair")
        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Opção inválida! Digite apenas números.")
            continue

        if opcao == 1:
            cadastrar_aluno()
        elif opcao == 2:
            listar_alunos()
        elif opcao == 3:
            fazer_matricula()
        elif opcao == 4:
            adicionar_disciplinas()
        elif opcao == 5:
            listar_alunos_por_curso()
        elif opcao == 6:
            adicionar_notas()
        elif opcao == 7:
            consultar_por_turma()
        elif opcao == 8:
            gerar_boletim()
        elif opcao == 9:
            listar_alunos_matriculados()
        elif opcao == 10:
            nome = input("Digite o nome do aluno a ser removido: ").strip().title()
            cadastro.remover_aluno(nome)
        elif opcao == 11:
            listar_alunos_por_disciplina()
        elif opcao == 12:
            nome = input("Digite o nome do aluno para consultar a nota: ").strip().title()
            cadastro.consultar_notas_do_aluno(nome)
        elif opcao == 13:
            mostrar_todas_notas()
        elif opcao==14:
            break
        else:
            print("Opção inválida! Digite um número entre 1 e 13.")

if __name__ == "__main__":
    menu_principal()

