from fun import *
import calendar 
from datetime import datetime
from colorama import Fore

def menuRelatorios():
    print(Fore.WHITE + "\n")
    print(Fore.WHITE + "1 -> Distribuição de publicações por ano.")
    print(Fore.WHITE + "2 -> Número de publicações por autor.")
    print(Fore.WHITE + "3 -> Distribuição de palavras-chave pela sua frequência (top 20 palavras-chave).")
    print(Fore.WHITE + "- -> Voltar para o menu anterior\n")

def menuFilter():
    print(Fore.WHITE + "\n")
    print(Fore.WHITE + "1 -> Pretendo filtrar dados")
    print(Fore.WHITE + "- -> Voltar para o menu anterior\n")

def linha():
    op = None
    stop = False 
    data = None
    print(Fore.WHITE + "Sistema de Consulta e Análise de Publicações Científicas\n")
    print(Fore.WHITE + "1 -> Importar ficheiro")
    print(Fore.WHITE + "2 -> Criar uma publicação")
    print(Fore.WHITE + "3 -> Consultar uma publicação")
    print(Fore.WHITE + "4 -> Consultar publicações")
    print(Fore.WHITE + "5 -> Eliminar uma publicação")
    print(Fore.WHITE + "6 -> Relatórios")
    print(Fore.WHITE + "7 -> Listar Autores")
    print(Fore.WHITE + "8 -> Atualizar publicação")
    print(Fore.WHITE + "9 -> Help")
    print(Fore.WHITE + "0 -> Sair")

    while not stop:
        print(Fore.WHITE + "\n")
        op = input(Fore.WHITE + "Escolha uma das opções: ")
        if op == "1":
            filepath = file()
            data = importar(filepath)
            if data is False:
                print(Fore.RED +"Erro na importação ou operação cancelada.\n")
            else:
                print(Fore.GREEN +"Importação concluída.\n")
        elif op == "2":
            if data and filepath:
                createPub(data,filepath)
            else:
                print(Fore.RED + "Primeiro, importe um arquivo com dados para criar uma publicação.\n")
        elif op == "3":
            if data:
                print(Fore.WHITE + "\n")
                filtered_data = tabfilterpt(data)
                if filtered_data:
                    stopcons = False
                    while not stopcons:
                        print(Fore.WHITE + "\n")
                        filterID = int(input(Fore.WHITE +"\nEscolha o ID da publicação para ver detalhes: ").strip())
                        print(Fore.WHITE + "\n")
                        try:
                            filterID = int(filterID)
                            if filterID:
                                conspub(filterID, filtered_data)
                                stopcons = True
                        except ValueError:
                            print(Fore.RED + "ID inválido. Por favor, insira um número válido.")
            else:
                print(Fore.RED + "Primeiro, importe um arquivo com dados para consultar uma publicação.\n")
                
        elif op == "4":
            if data:
                print(Fore.WHITE + "\n")
                filtered_data = tabfilterpt(data)
                if filtered_data:
                    stopconss = False
                    while not stopconss:
                        filterIDs_input = input(Fore.WHITE +"\nEscolha os IDs das publicações para ver detalhes (separados por vírgula): ").split(",")
                        print(Fore.WHITE + "\n")
                        try:
                            if filterIDs_input:
                                conspubs(filterIDs_input, filtered_data)
                                stopconss = True
                        except ValueError:
                            print(Fore.RED + "Opção inválida!")
                            print(Fore.WHITE + "\n")
            else:
                print(Fore.RED + "Primeiro, importe um arquivo com dados para consultar publicações.\n")
            
        elif op == "5": 
            if data and filepath:
                print(Fore.WHITE + "\n")
                filtered_data = tabfilterpt(data)
                if filtered_data:
                    stopdel = False
                    while not stopdel:
                        pubIDtoDel = int(input(Fore.WHITE + "\nEscreva o ID da publicação que deseja excluir: ").strip())
                        print(Fore.WHITE + "\n")
                        try:
                            if pubIDtoDel:
                                DelPub(data, filepath, pubIDtoDel)
                                stopdel = True
                                print(Fore.GREEN +"Publicação eliminada com sucesso.")
                        except ValueError:
                            print(Fore.RED + "Opção inválida!")
                            print(Fore.WHITE + "\n")
            else:
                print(Fore.RED + "Primeiro, importe um arquivo com dados para eliminar uma publicação.\n")
        elif op == "6":
            if data:
                stopSM = False
                while not stopSM:
                    menuRelatorios()
                    opRel = input(Fore.WHITE + "Escolha o número do relatório: ")
                    if opRel == "1":
                        relPubAnoster(data)
                    elif opRel == "2":
                        relPubAutor(data)
                    elif opRel == "3":
                        relKeywords(data)
                    elif opRel == "-":
                        stopSM = True
                        print("Terminar Consulta dos Relatórios!")
                    elif opRel == "":
                        print ("Pode voltar para menu anterior selecionando -")
                    else:
                        print(Fore.RED + "Opção inválida!")
                        print(Fore.WHITE + "\n")
            else:
                print(Fore.RED + "Primeiro, importe um arquivo com dados para visualizar os relatórios.\n")

        elif op== "7":
            if data:
                autores(data)
            else:
                print(Fore.RED + "Primeiro, importe um arquivo com dados para listar os autores.\n")
        elif op== "8":
            if data:
                print(Fore.WHITE + "\n")
                filtered_data = tabfilterpt(data)
                if filtered_data:
                    stopup = False
                    while not stopup:
                        print(Fore.WHITE + "\n")
                        filterID = int(input(Fore.WHITE +"\nEscolha o ID da publicação que deseja atualizar: ").strip())
                        print(Fore.WHITE + "\n")
                        try:
                            filterID = int(filterID)
                            if filterID:
                                pub = conspub(filterID, filtered_data)
                                updatePubs(pub)
                                stopup = True
                        except ValueError:
                            print(Fore.RED + "ID inválido. Por favor, insira um número válido.")
                
            else:
                print(Fore.RED + "Primeiro, importe um arquivo com dados para atualizar uma publicação.\n")

        elif op == "9":
            helpUser()
        
        elif op == "":
            print("Se deseja ajuda para a utilização do programa, use o comando: 9")
        
        elif op == "0":
            stop=True
        
        else:
            print(Fore.RED+"Instrução inválida!")
            print(Fore.WHITE+"\n")
    print(Fore.RED+"\nSaiu do programa")
    print(Fore.WHITE+'\n')

linha()