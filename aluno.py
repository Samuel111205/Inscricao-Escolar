import cadastro
from datetime import date

while True:
    cadastro.menu()
    opcao=int(input("Digite sua opção: "))
    if opcao==1:
        nome=input("Nome: ")
        nascimento=int(input("Data de nascimento: "))
        idade=date.today().year-nascimento
        media=float(input("Media do certificado: "))
        curso=input("Digite seu curso: ")
        aluno=cadastro.Aluno(nome,nascimento,idade,media,curso)
        if idade>=15 and idade<=18 and media>=10:
            cadastro.cad.append(aluno)
            print("Aluno cadastrado com sucesso")
        else:
            cadastro.nao_cadastradas.append(aluno)
            print("Aluno não cadastrado")
    elif opcao==2:
        if cadastro.cad:
            for i in cadastro.cad:
                print(f"{i}: {i.mostrar_dados()}")
        else:
            print("Nenhum aluno cadastrado")
    elif opcao==3:
        for p in cadastro.nao_cadastradas:
            print(f"{p}: {p.mostrar_dados()}")
    elif opcao==4:
        nome=input("Nome: ")
        pagamento=input("Pagamento: ").capitalize()
        while True:
            if pagamento=="Sim":
                idade=int(input("Idade: "))
                classe=int(input("Classe: "))
                curso=input("Curso: ")
                matricula=cadastro.Matricula(nome,pagamento,idade,classe,curso)
                matricula.mostrar_dados()
                break
            elif pagamento=="Nao":
                print("Para continuares o processo de maricula tens de fazer o pagamento do rupe")
                print("dirija-se a secretaria do ceu curso  e receba um rupe")
                break
            else:
                print("Resposta errada por favor digite apenas Sim ou Nao")
                break
    elif opcao==5:
        break
    else:
        print("Opçaõ invalida!")

