import cadastro 
from datetime import date

while True:
    cadastro.menu()
    try:
        opcao=int(input("Digite sua opção: "))
    except ValueError:
        print("Por favor digite apenas numeros!")
        continue

    if opcao==1:
        cadastro.menu_cadastro()
        try:
            opp=int(input("Digite o operação a ser feita: "))
        except ValueError:
            print("Por favor digite apenas numeros!")
            continue

        if opp==1:
            nome=input("Nome: ")
            try:
                nascimento=int(input("Data de nascimento (ex: 2008): "))
            except ValueError:
                print("Ano invalido!")
                continue
            idade=date.today().year-nascimento
            try:
                media=float(input("Media do certificado: "))
            except ValueError:
                print("Media Invalida")
                continue
            curso=str(input("Digite o curso que qes fazer: ")).capitalize()
            aluno=cadastro.Aluno(nome,nascimento,idade,media,curso)
            if idade>=15 and idade<=18 and media>=10:
                try:
                    if curso=="Informatica":
                        cadastro.tot_aluno_da_informatica.append(aluno)
                        cadastro.cadastrados.append(aluno)
                        print("Aluno cadastrado com  sucesso")
                    elif curso=="Contabilidade":
                        cadastro.tot_aluno_da_contabilidade.append(aluno)
                        cadastro.cadastrados.append(aluno)
                        print("Aluno cadastrado com sucesso")
                except Exception as error:
                    print(f"Inflizmente tivemos um erro, e erro foi {error}")
                else:
                    print("Processo de cadastramento feito com sucesso")
                finally:
                    print("Volte sempre")
            else:
                print("Aluno não cadastrado (Idade, media estão fora dos criterios necessarios ou digitaste um curso que não lecionamos)")
            cadastro.total_inscritos.append(aluno)
        elif opp==2:
            cadastro.menu_alunos()
            try:
                pp=int(input("Digite a sua opção: "))
            except ValueError:
                print("Por favor digite apenas um numero inteiro")
                continue
            if pp==1:
                if cadastro.tot_aluno_da_contabilidade:
                    print(f"Ao todo foram cadastradas no curso de contablidade {len(cadastro.tot_aluno_da_contabilidade)} alunos que são: ")
                    for i in cadastro.tot_aluno_da_contabilidade:
                        print(f"{i}: {i.mostrar_dados()}")
                else:
                    print("Nenhum aluno cadastrado no curso de contablidade!")
            elif pp==2:
                if cadastro.tot_aluno_da_informatica:
                    print(f"E no curso de Informatica foram cadastradas {len(cadastro.tot_aluno_da_informatica)} alunos que são: ")
                    for i in cadastro.tot_aluno_da_informatica:
                        print(f"{i}: {i.mostrar_dados()}")
                else:
                    print("nenhum aluno cadastrado na informatica")
            elif pp==3:
                if cadastro.cadastrados:
                    print(f"E no geral foram cadastradas {len(cadastro.cadastrados)} alunos que são: ")
                    for i in cadastro.cadastrados:
                        print(f"{i}: {i.mostrar_dados()}")
                else:
                    print("Nenhum aluno cadastrado")
        elif opp==3:
            nome=input("Nome: ")
            pagamento=input("Pagamento(Sim/Não): ").capitalize()
            while True:
                if pagamento=="Sim":
                    try:
                        idade=int(input("Idade: "))
                        classe=int(input("Classe: "))
                    except ValueError:
                        print("Idade ou Classe Invalida")
                        break
                    curso=input("Curso: ")
                    matricula=cadastro.Matricula(nome,pagamento,idade,classe,curso)
                    matricula.mostrar_dados()
                    break
                elif pagamento=="Nao":
                    print("Para continuares o processo de maricula tens de fazer o pagamento do rupe no seguinte numero: ",end=" ")
                    print(f"{cadastro.sorteio()}")
                    break
                else:
                    print("Resposta errada por favor digite apenas Sim ou Nao")
                    pagamento=input("Pagamento (Sim/Não): ").capitalize()
        elif opp==4:
            continue
        else:
            print("Opçaõ invalida!")
    elif opcao==2:
        while True:
            nome=str(input("Nome: "))
            try:
                nota1=float(input("Nota1: "))
                nota2=float(input("Nota2: "))
                nota3=float(input("Nota3: "))
                media=(nota1+nota2+nota3)/3
            except ValueError:
                print("Digite um numero real ou inteiro")
            cadastro.ficha.append([nome,[nota1,nota2],media])
            resposta=str(input("Ques continuar?: ")).upper()
            if resposta=='N':
                break
        print("="*30)
        print("No°   Nome        Media")
        print("="*30)
        for i,a in enumerate(cadastro.ficha):
            print(f"{i}     {a[0]}       {a[2]}")
        while True:
            print("="*30)
            mostrar=int(input("Mostrar nota de qual aluno? 999 para parar: "))
            if mostrar==999:
                break
            if mostrar<=len(cadastro.ficha)-1:
                print(f"As notas de {cadastro.ficha[mostrar][0]} são {cadastro.ficha[mostrar][1]}")
                

