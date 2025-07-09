import cadastro 
from datetime import date

while True:
    cadastro.menu()
    opcao=int(input("Digite sua opção: "))
    if opcao==1:
        cadastro.menu_cadastro()
        opp=int(input("Digite o operação a ser feita: "))
        if opp==1:
            nome=input("Nome: ")
            nascimento=int(input("Data de nascimento: "))
            idade=date.today().year-nascimento
            media=float(input("Media do certificado: "))
            curso=str(input("Digite o curso que qes fazer: ")).capitalize()
            aluno=cadastro.Aluno(nome,nascimento,idade,media,curso)
            if idade>=15 and idade<=18 and media>=10:
                try:
                    if curso=="Informatica":
                        cadastro.tot_aluno_da_informatica.append(aluno)
                        cadastro.cadastrados.append(aluno)
                        print("Aluno cadastrado com sucesso")
                    elif curso=="Contablidade":
                        cadastro.tot_aluno_da_contablidade.append(aluno)
                        cadastro.cadastrados.append(aluno)
                        print("Aluno cadastrado com sucesso")
                except Exception as error:
                    print(f"Inflizmente tivemos um erro, e erro foi {error}")
                else:
                    print("Processo de cadastramento feito com sucesso")
                finally:
                    print("Volte sempre")
            else:
                print("Aluno não cadastrado")
            cadastro.total_inscritos.append(aluno)
        elif opp==2:
            cadastro.menu_alunos()
            pp=int(input("Digite a sua opção: "))
            if pp==1:
                if cadastro.tot_aluno_da_contablidade:
                    print(f"Ao todo foram cadastradas no curso de contablidade {len(cadastro.tot_aluno_da_contablidade)} alunos que são: ")
                    for i in cadastro.tot_aluno_da_contablidade:
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
                    print("Para continuares o processo de maricula tens de fazer o pagamento do rupe no seguinte numero: ",end=" ")
                    print(f"{cadastro.sorteio()}")
                    break
                else:
                    print("Resposta errada por favor digite apenas Sim ou Nao")
                    break
        elif opp==4:
            break
        else:
            print("Opçaõ invalida!")

