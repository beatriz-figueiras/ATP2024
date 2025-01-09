import json
import os
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as pfct
from prettytable import PrettyTable as pt
from io import BytesIO
import re

# Funções gerais

def file():
    root = tk.Tk()
    root.withdraw() 
    filepath = filedialog.askopenfilename(
        title="Escolha o arquivo a ser importado",
        filetypes=[("Arquivos JSON", "*.json")])
    return filepath

def verifcautores(autores):
    if not isinstance(autores, list):
        return False
    for autor in autores:
        if not isinstance(autor, dict):
            return False
        if "name" in autor and not isinstance(autor["name"], str):
            return False
        if "affiliation" in autor and not isinstance(autor["affiliation"], str):
            return False
        if "orcid" in autor and not isinstance(autor["orcid"],str):
            return False
    return True

def verifcestrutura(item):
    if "abstract" in item and not isinstance(item["abstract"], str): 
        return False
    if "authors" in item and not verifcautores(item["authors"]):
        return False
    if "doi" in item and not isinstance(item["doi"], str):
        return False
    if "title" in item and not isinstance(item["title"], str):
        return False
    if "url" in item and not isinstance(item["url"], str):
        return False
    if "keywords" in item and not isinstance(item["keywords"], str):
        return False
    if "publish_date" in item and not isinstance(item["publish_date"], str):
        return False
    return True

def salvar(conteudo, filepath):
    with open(filepath, 'w', encoding='UTF-8') as f:
        json.dump(conteudo, f, ensure_ascii=False, indent=4)
    print(f"Ficheiro salvo: {filepath}")
    return conteudo

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Funções só para o cli

def helpUser():
    print("Se pretende importar um ficheiro, salvar como novo ou adicionar um ficheiro a outro ficheiro, use o comando: 1")
    print("Se pretende criar uma nova publicação e adicionar ao seu ficheiro, use o comando: 2")
    print("Se pretende consultar uma publicação, use o comando: 3")
    print("Se pretende consultar publicações, use o comando: 4")
    print("Se pretende eliminar publicação, use o comando: 5")
    print("Se pretende visusalizar os relatórios de estatatísticas, use o comando: 6")
    print("Se pretende listar todos os autores, use o comando: 7")
    print("Se pretende atualizar uma publicação, use o comando: 8")
    print("Se pretende sair do programa, use o comando: 0") 

def importar(filepath):
    try:
        if not filepath:
            print("Nenhum arquivo foi selecionado.")
            return None
        with open(filepath, 'r', encoding='UTF-8') as fread:
            conteudo = json.load(fread)
        if not isinstance(conteudo, list):
            print("Estrutura inválida: Esperado um JSON com uma lista de artigos.")
            return None
        for i, item in enumerate(conteudo):
            if not verifcestrutura(item):
                print(f"Estrutura inválida no item {i}.")
                return None
            elif "ID" not in item:
                item = {"ID": i + 1, **item}
                conteudo[i] = item
            else:
                item["ID"] = i + 1
        print("Importação concluída. Escolha a próxima ação:\n")
        print("1. Salvar ficheiro.\n")
        print("1. Salvar como novo ficheiro.\n")
        print("2. Adicionar a um ficheiro existente.\n")
        opcao = int(input("Digite 1, 2 ou 3: "))
        if opcao == 1:
            salvar(conteudo, filepath)
        elif opcao == 2:
            novofich(conteudo, filepath)
        elif opcao == 3:
            adicionar(conteudo)
        else:
            print("Opção inválida.")
            return False
        return conteudo
    except Exception as e:
        print(f"Erro ao processar o ficheiro: {e}")
        return None

def novofich(conteudo, filepath):
    filepath = input("Digite o nome para o novo arquivo (com a extensão .json): ")
    if not filepath.endswith('.json'):
        filepath = filepath + '.json'
    with open(filepath, 'w', encoding='UTF-8') as fnew:
        json.dump(conteudo, fnew, ensure_ascii=False, indent=4)
    print(f"Novo ficheiro salvo em: {filepath}")
    return conteudo

def adicionar(conteudo):
    filepath = filedialog.askopenfilename(
        title="Escolha o arquivo existente para adicionar os dados",
        filetypes=[("Arquivos JSON", "*.json")]  
    )
    if not filepath:
        print("Nenhum arquivo foi selecionado.")
        return False
    with open(filepath, 'r', encoding='UTF-8') as fexist:
        conteudo_existente = json.load(fexist)
    if not isinstance(conteudo_existente, list):
        print("Estrutura inválida no ficheiro existente.")
        return False
    for i, item in enumerate(conteudo_existente):
        if not verifcestrutura(item):
            print(f"Estrutura inválida no item {i} do ficheiro existente.")
            return False
        elif "ID" not in item:
            item = {"ID": i + 1, **item}
            conteudo_existente[i] = item
        else:
            item["ID"] = i + 1
    conteudo_existente.extend(conteudo)
    for i, item in enumerate(conteudo_existente):
        item["ID"] = i + 1
    conteudo = conteudo_existente
    with open(filepath, 'w', encoding='UTF-8') as fexist:
        json.dump(conteudo, fexist, ensure_ascii=False, indent=4)
    print(f"Dados adicionados ao ficheiro existente: {filepath}")
    return conteudo

def createPub(data, filepath):
    try:
        title = ""
        while not title:
            title = input("Escreva o título da publicação: ").strip()
            if not title:
                print("O título é obrigatório. Por favor, insira um título válido.")       
        publish_date = ""
        valid_date = False
        while not valid_date:
            publish_date = input("Escreva a data de publicação (YYYY-MM-DD) ou deixe em branco: ").strip() or "N/A"
            if publish_date == "N/A":
                valid_date = True
            else:
                try:
                    datetime.strptime(publish_date, "%Y-%m-%d") 
                    valid_date = True
                except ValueError:
                    print("A data deve estar no formato YYYY-MM-DD.")
        keywords = input("Escreva as palavras-chave (separadas por vírgula): ").strip() or "N/A"
        num_authors = -1
        while num_authors <= 0:
            try:
                num_authors = int(input("Quantos autores deseja adicionar? ").strip())
                if num_authors <= 0:
                    print("Por favor, insira um número positivo maior que zero.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número inteiro válido.")
        authors = []
        for _ in range(num_authors):
            name = ""
            while not name:
                name = input("Escreva o nome do autor: ").strip()
                if not name:
                    print("O nome do autor é obrigatório.")         
            affiliation = input("Escreva a afiliação do autor: ").strip() or "N/A"
            orcid = input("Escreva o orcid do autor: ").strip() or "N/A"
            authors.append({"name": name, "affiliation": affiliation, "orcid": orcid})       
        doi = input("Escreva o DOI (ou deixe em branco): ").strip() or "N/A"
        pdf = input("Escreva o link do PDF (ou deixe em branco): ").strip() or "N/A"
        url = input("Escreva o link da URL (ou deixe em branco): ").strip() or "N/A"
        abstract = input("Escreva o resumo da publicação (ou deixe em branco): ").strip() or "N/A"
        ultimo_id = max(item["ID"] for item in data)
        new_publication = {
            "ID": ultimo_id + 1,  
            "abstract": abstract,
            "keywords": keywords,
            "authors": authors,
            "doi": doi,
            "pdf": pdf,
            "publish_date": publish_date,
            "title": title,
            "url": url
        }
        data.append(new_publication)
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("\nPublicação criada com sucesso!")
    except ValueError as ve:
        print(f"\nErro: {ve}")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")

def filterPubs(data):
    title = input("Escreva o Título (ou pressione Enter para ignorar): ").strip() or None
    author = input("Escreva o Nome do Autor (ou pressione Enter para ignorar): ").strip() or None
    affiliation = input("Escreva a Afiliação do Autor (ou pressione Enter para ignorar): ").strip() or None
    keywords = input("Escreva as Palavras-chave separadas por vírgula (ou pressione Enter para ignorar): ").strip()
    keywords = [kw.strip() for kw in keywords.split(',')] if keywords else None
    year = input("Escreva o Ano de publicação (ou pressione Enter para ignorar): ").strip() or None
    filtered_data = []
    for item in data:
        if title and title.lower() not in item.get('title', '').lower():
            continue        
        if author:
            authors = [a.get('name', '').lower() for a in item.get('authors', [])]
            if not any(author.lower() in a for a in authors):
                continue        
        if affiliation:
            affiliations = [a.get('affiliation', '').lower() for a in item.get('authors', [])]
            if not any(affiliation.lower() in a for a in affiliations):
                continue       
        if keywords:
            item_keywords = item.get('keywords', '').split(',')
            item_keywords = [kw.strip().lower() for kw in item_keywords]
            if not any(keyword.lower() in item.get('keywords', '').lower() for keyword in keywords):
                continue        
        if year:
            if year != item.get('publish_date', '').split('-')[0]:
                continue
        filtered_data.append(item)
    return filtered_data

def tabfilterpt(data):
    filtered_data = filterPubs(data)
    if filtered_data:
        table = pt(["ID", "Título", "Abstract", "Palavras-chave", "Autores", "Afiliações", "Orcid", "DOI", "PDF", "Data", "url"])
        table.max_width["Título"] = 25
        table.max_width["Abstract"] = 25
        table.max_width["Autores"] = 20
        table.max_width["Afiliações"] = 30
        table.max_width["Orcid"] = 30
        table.max_width["Palavras-chave"] = 20
        table.max_width["DOI"] = 20
        table.max_width["PDF"] = 20
        table.max_width["url"] = 20
        for item in filtered_data:
            authors = "| ".join([a.get('name', 'N/A') for a in item.get('authors', [])])
            affiliations = "| ".join([a.get('affiliation', 'N/A') for a in item.get('authors', [])])
            orcid = "| ".join([a.get('orcid', 'N/A') for a in item.get('authors', [])])
            table.add_row([
                item.get("ID"),
                item.get("title", "N/A"),
                item.get("abstract", "N/A"),
                item.get("keywords", "N/A"),
                authors,
                affiliations,
                orcid,
                item.get("doi", "N/A"),
                item.get("pdf", "N/A"),
                item.get("publish_date", "N/A"),
                item.get("url", "N/A")
            ])
        print("\nPublicações Encontradas:\n")
        print(table)
        return filtered_data
    else:
        print("\nNenhuma publicação encontrada com os critérios fornecidos.")

def conspub(filterID, filtered_data):
    pub = next((item for item in filtered_data if item.get("ID") == filterID), None)
    if pub:
        showPubDetails(pub)
        return pub
    else:
        print("\nID inválido.")

def showPubDetails(pub):
    table = pt(["ID", "Título", "Abstract", "Palavras-chave", "Autores", "Afiliações", "Orcid", "DOI", "PDF", "Data", "url"])
    table.max_width["Título"] = 25
    table.max_width["Abstract"] = 25
    table.max_width["Autores"] = 20
    table.max_width["Afiliações"] = 30
    table.max_width["Orcid"] = 30
    table.max_width["Palavras-chave"] = 20
    table.max_width["DOI"] = 20
    table.max_width["PDF"] = 20
    table.max_width["url"] = 20
    authors = "| ".join([a.get('name', 'N/A') for a in pub.get('authors', [])])
    affiliations = "| ".join([a.get('affiliation', 'N/A') for a in pub.get('authors', [])])
    orcid = "| ".join([a.get('orcid', 'N/A') for a in pub.get('authors', [])])
    table.add_row([
        pub.get("ID"),
        pub.get("title", "N/A"),
        pub.get("abstract", "N/A"),
        pub.get("keywords", "N/A"),
        authors,
        affiliations,
        orcid,
        pub.get("doi", "N/A"),
        pub.get("pdf", "N/A"),
        pub.get("publish_date", "N/A"),
        pub.get("url", "N/A")
    ])
    print("\nDetalhes da Publicação Selecionada:")
    print(table)

def conspubs(filterIDs_input, filtered_data):
    filterIDs = [int(id.strip()) for id in filterIDs_input if id.strip().isdigit()]
    if filterIDs:
        pubs =[]
        for filterID in filterIDs:
            pub = next((item for item in filtered_data if item.get("ID") == filterID), None)
            if pub:
                pubs.append(pub)
            
        if pubs:
            showPubsDetails(pubs)
        else:
            print("\nID inválido.")
       
def showPubsDetails(pubs):
    table = pt(["ID", "Título", "Abstract", "Palavras-chave", "Autores", "Afiliações", "Orcid", "DOI", "PDF", "Data", "url"])
    table.max_width["Título"] = 25
    table.max_width["Abstract"] = 25
    table.max_width["Autores"] = 20
    table.max_width["Afiliações"] = 30
    table.max_width["Orcid"] = 30
    table.max_width["Palavras-chave"] = 20
    table.max_width["DOI"] = 20
    table.max_width["PDF"] = 20
    table.max_width["url"] = 20
    for pub in pubs:
        authors = "| ".join([a.get('name', 'N/A') for a in pub.get('authors', [])])
        affiliations = "| ".join([a.get('affiliation', 'N/A') for a in pub.get('authors', [])])
        orcid = "| ".join([a.get('orcid', 'N/A') for a in pub.get('authors', [])])
        table.add_row([
            pub.get("ID"),
            pub.get("title", "N/A"),
            pub.get("abstract", "N/A"),
            pub.get("keywords", "N/A"),
            authors,
            affiliations,
            orcid,
            pub.get("doi", "N/A"),
            pub.get("pdf", "N/A"),
            pub.get("publish_date", "N/A"),
            pub.get("url", "N/A")
        ])
    print("\nDetalhes das Publicaçôes selecionadas:")
    print(table)

def DelPub(data, filepath, pubIDtoDel):
    pubDel = next((pub for pub in data if pub["ID"] == pubIDtoDel), None)
    if pubDel:
        data.remove(pubDel)  
    else:
        print(f"\nNenhuma publicação encontrada com o ID {pubIDtoDel}.")
        return data    
    for i, item in enumerate(data):
        item["ID"] = i + 1  
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4) 
        print(f"\nDados atualizados salvos em {filepath}")
    return data

def listPub(data, pub_id=None):
    table = pt(["Index", "Abstract", "Keywords", "Name", "Affiliation", "Publish Date", "Title", "DOI", "PDF", "URL"])
    table.max_width["Index"] = 5
    table.max_width["Abstract"] = 30
    table.max_width["Name"] = 20
    table.max_width["Affiliation"] = 30
    table.max_width["Keywords"] = 25
    table.max_width["Publish Date"] = 10
    table.max_width["Title"] = 15
    table.max_width["DOI"] = 15
    table.max_width["PDF"] = 15
    table.max_width["URL"] = 15
    if pub_id is not None:
        data = [item for item in data if item.get("ID") == pub_id]  # filtra pelo ID
    for i, item in enumerate(data):
        abstract = item.get("abstract", "N/A")
        keywords = item.get("keywords", "N/A")
        doi = item.get("doi", "N/A")
        pdf = item.get("pdf", "N/A")
        publish_date = item.get("publish_date", "N/A")
        title = item.get("title", "N/A")
        url = item.get("url", "N/A")
        authors = item.get("authors", [])
        authors_list = []
        affiliations_list = []
        for author in authors:
            name = author.get("name", "N/A")
            affiliation = author.get("affiliation", "N/A")
            authors_list.append(f"{name}")
            affiliations_list.append(f"{affiliation}")
            authors_str = ", ".join(authors_list) if authors_list else "N/A"
            affiliations_str = ", ".join(affiliations_list) if affiliations_list else "N/A"
        table.add_row([item.get("ID", i), abstract, keywords, authors_str, affiliations_str, publish_date, title, doi, pdf, url]) 
    print(table)

def autores(data):
    authors_set = set()
    for item in data:
        if 'authors' in item:
            for autor in item['authors']:
                if 'name' in autor:
                    authors_set.add(autor['name'])
    authors_list = list(authors_set)
    authors_list = sorted(authors_list)
    for autor in authors_list:
        print(autor)

def relPubAnoster(data):
    pubAnos = Counter()
    for item in data:
        if 'publish_date' in item:
            year = item['publish_date'].split('-')[0]
            pubAnos[year] += 1   
    print("\nNúmero de Publicações por Ano:")
    for year, count in sorted(pubAnos.items()):
        print(f"{year}: {count}")

def distribPubPorMes(data, ano):
    meses = Counter()
    for item in data:
        if 'publish_date' in item and item['publish_date']:
            try:
                match = re.search(r"\d{4}-\d{2}-\d{2}", item['publish_date'])
                if match:
                    data_pub = datetime.strptime(match.group(), "%Y-%m-%d")
                    if data_pub.year == ano:
                        meses[data_pub.month] += 1
                else:
                    print(f"Data inválida encontrada: {item['publish_date']}")
            except ValueError as e:
                print(f"Erro ao processar a data: {item['publish_date']} - {e}")  
    meses_ordenados = {mes: meses.get(mes, 0) for mes in range(1, 13)}    
    return meses_ordenados

def relPubAutor(data):
    autorCount = Counter()
    for item in data:
        if 'authors' in item:
            for author in item['authors']:
                if 'name' in author:
                    autorCount[author['name']] += 1
    autorCountSort = sorted(autorCount.items())
    print("\nNúmero de Publicações por Autor:")
    for author, count in autorCountSort:
        print(f"{author}: {count}")

def distribPubAutorPorAno(data, autor):
    anos = Counter()
    for item in data:
        if 'authors' in item:
            for author in item['authors']:
                if author['name'] == autor:
                    if 'publish_date' in item:
                        ano = datetime.strptime(item['publish_date'], "%Y-%m-%d").year
                        anos[ano] += 1
    return dict(sorted(anos.items()))

def relKeywords(data):
    keywords = []
    for item in data:
        if 'keywords' in item and item['keywords']:
            keywords.extend([keyword.strip() for keyword in item['keywords'].split(',')])
    keywordCount = Counter(keywords)
    keywordSort = sorted(keywordCount.items())
    print("\nFrequência de Palavras-chave:")
    for keyword, count in keywordSort:
        print(f"{keyword}: {count}")

def distribPalavrasChavePorAno(data):
    palavras_por_ano = Counter()
    for item in data:
        if 'publish_date' in item and 'keywords' in item and item['keywords']:
            ano = datetime.strptime(item['publish_date'], "%Y-%m-%d").year
            palavras = [keyword.strip() for keyword in item['keywords'].split(',')]
            palavras_por_ano.update({(ano, palavra): 1 for palavra in palavras})
    resultado = {}
    for (ano, palavra), count in palavras_por_ano.items():
        if ano not in resultado or count > resultado[ano][1]:
            resultado[ano] = (palavra, count)
    return {ano: palavra_count for ano, palavra_count in resultado.items()}

def updatePubs(pub):
    stopUpdate = False
    while not stopUpdate:    
        if pub:
            stopPubUpdate = False  
            while not stopPubUpdate:
                print("\nO que deseja atualizar? (Você pode atualizar vários campos)")
                print("1. Data de publicação")
                print("2. Resumo")
                print("3. Palavras-chave")
                print("4. Autores")
                print("5. Afiliações")
                print("6. Concluir atualizações para esta publicação")
                try:
                    option = int(input("\nDigite o número da opção: ").strip())
                    if option == 1:
                        new_date = input("Digite a nova data de publicação (YYYY-MM-DD): ").strip()
                        pub["publish_date"] = new_date
                        print("\nData de publicação atualizada com sucesso.")
                    elif option == 2:
                        new_abstract = input("Digite o novo resumo: ").strip()
                        pub["abstract"] = new_abstract
                        print("\nResumo atualizado com sucesso.")
                    elif option == 3:
                        new_keywords = input("Digite as novas palavras-chave (separadas por vírgula): ").strip().split(',')
                        pub["keywords"] = [kw.strip() for kw in new_keywords]
                        print("\nPalavras-chave atualizadas com sucesso.")
                    elif option == 4:
                        new_authors = input("Digite os novos autores (separados por vírgula): ").strip().split(',')
                        pub["authors"] = [{"name": author.strip()} for author in new_authors]
                        print("\nAutores atualizados com sucesso.")
                    elif option == 5:
                        new_affiliations = input("Digite as novas afiliações (separadas por vírgula): ").strip().split(',')
                        for i, author in enumerate(pub["authors"]):
                            if i < len(new_affiliations):
                                author["affiliation"] = new_affiliations[i].strip()
                        print("\nAfiliações atualizadas com sucesso.")
                    elif option == 6:
                        print("\nAtualizações concluídas para esta publicação.")
                        stopPubUpdate = True  
                    else:
                        print("\nOpção inválida. Tente novamente.")
                except ValueError:
                    print("\nErro: Digite um número válido.")
        else:
            print("\nNenhuma publicação selecionada.")
        opUpdate = input("\nQuer atualizar outra publicação? (s/n): ").strip().lower()
        if opUpdate == "n":
            stopUpdate = True
            print("\nProcesso de atualização encerrado.")

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Funções só para o grafico
def importargui(filepath):
    try:
        if not filepath:
            print("Nenhum arquivo foi selecionado.")
            return None
        with open(filepath, 'r', encoding='UTF-8') as fread:
            conteudo = json.load(fread)
        if not isinstance(conteudo, list):
            print("Estrutura inválida: Esperado um JSON com uma lista de artigos.")
            return None
        for i, item in enumerate(conteudo):
            if not verifcestrutura(item):
                print(f"Estrutura inválida no item {i}.")
                return None
            elif "ID" not in item:
                item = {"ID": i + 1, **item}
                conteudo[i] = item
            else:
                item["ID"] = i + 1
        salvar(conteudo, filepath)
        return conteudo
    except Exception as e:
        print(f"Erro ao processar o ficheiro: {e}")
        return None
    
def ordpubtitulo(publicacoes,ori):
    titulosord = sorted(publicacoes, key=lambda x: x["title"].upper(), reverse=ori)
    return titulosord

def ordpubnome(publicacoes,ori):
    nomesord = sorted(publicacoes, key=lambda x: x["name"].upper(), reverse=ori)
    return nomesord

def ordpubdata(publicacoes,ori):
    datasord = sorted(publicacoes, key=lambda x: x["publish_date"].upper(), reverse=ori)
    return datasord

def deletepubgui(pub, data, filepath):
    if pub:
        try:
            pubIDtoDel = pub["ID"]
            pubDel = next((pub for pub in data if pub["ID"] == pubIDtoDel), None)
            if pubDel:
                data.remove(pubDel)
                print("Publicação eliminada com sucesso.")   
            else:
                print(f"\nNenhuma publicação encontrada com o ID {pubIDtoDel}.")
                return data    
        except ValueError:
            print("\nErro: ID inválido. Por favor, insira um número inteiro válido.")
            return data
    for i, item in enumerate(data):
        item["ID"] = i + 1  
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4) 
        print(f"\nDados atualizados salvos em {filepath}")
    return data

def autoresgui(data):
    autores = set()  
    for item in data:
        if 'authors' in item: 
            for author in item['authors']:
                if 'name' in author:  
                    autores.add(author['name'])  
    return list(autores)

def relkeywordsgui(data, top_n=20):
    palavrasChaveCount = Counter()
    for item in data:
        if 'keywords' in item:  
            for keyword in item['keywords']:  
                palavrasChaveCount[keyword] += 1
    palavrasChaveSort = palavrasChaveCount.most_common(top_n)  
    palavras, contagens = zip(*palavrasChaveSort)
    plt.figure(figsize=(10, 6))
    plt.bar(palavras, contagens)
    plt.title("Top Palavras-chave mais frequentes")
    plt.xlabel("Palavra-chave")
    plt.ylabel("Frequência")
    plt.xticks(rotation=45, ha='right') 
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return buf

def relPubAutorgui(data, top_n=20):  
    autorCount = Counter()
    for item in data:
        if 'authors' in item:  
            for author in item['authors']: 
                if 'name' in author:
                    autorCount[author['name']] += 1
    autorCountSort = autorCount.most_common(top_n)  
    autores, contagens = zip(*autorCountSort)
    plt.figure(figsize=(10, 6))
    plt.bar(autores, contagens)
    plt.title("Top Autores com Mais Publicações")
    plt.xlabel("Autor")
    plt.ylabel("Número de Publicações")
    plt.xticks(rotation=45, ha='right')  
    plt.tight_layout()  
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf

def relPubAnosgui(data):
    pubAnos = Counter()
    for item in data:
        if 'publish_date' in item:
            year = item['publish_date'].split('-')[0]
            pubAnos[year] += 1
    print("\nNúmero de Publicações por Ano:")
    for year, count in sorted(pubAnos.items()):
        print(f"{year}: {count}")
    years = sorted(pubAnos.keys())
    counts = [pubAnos[year] for year in years]
    plt.figure(figsize=(10, 6))
    plt.plot(years, counts, marker='o')
    plt.title("Número de Publicações por Ano")
    plt.xlabel("Ano")
    plt.ylabel("Número de Publicações")
    plt.grid(True)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)  
    return buffer

def distribPubPorMesgui(data, ano):
    meses = Counter()
    for item in data:
        if 'publish_date' in item:
            data_pub_str = item['publish_date']
            data_pub_str = re.sub(r'\s*—\s*Atualizado.*', '', data_pub_str) 
            try:
                data_pub = datetime.strptime(data_pub_str, "%Y-%m-%d")
                if data_pub.year == ano:
                    meses[data_pub.month] += 1
            except ValueError:
                print(f"Data inválida encontrada: {item['publish_date']}")
                continue
    meses_ordenados = {mes: meses.get(mes, 0) for mes in range(1, 13)}
    plt.figure(figsize=(10, 6))
    plt.bar(range(1, 13), meses_ordenados.values(), tick_label=list(meses_ordenados.keys()))
    plt.title("Distribuição de Publicações por Mês")
    plt.xlabel("Mês")
    plt.ylabel("Número de Publicações")
    plt.grid(axis='y')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer

def PubAutoPorAnogui(data, autor):
    anos = Counter()
    for item in data:
        if 'authors' in item:
            for author in item['authors']:
                if author['name'] == autor:
                    if 'publish_date' in item:
                        try:
                            ano = datetime.strptime(item['publish_date'], "%Y-%m-%d").year
                            anos[ano] += 1
                        except ValueError:
                            print(f"Data inválida encontrada: {item['publish_date']}")
                            continue
    anos_ordenados = dict(sorted(anos.items()))
    if not anos_ordenados:
        print(f"Nenhuma publicação encontrada para o autor: {autor}")
        return None
    plt.figure(figsize=(10, 6))
    plt.bar(anos_ordenados.keys(), anos_ordenados.values())
    plt.title(f"Distribuição de Publicações por Ano - {autor}")
    plt.xlabel("Ano")
    plt.ylabel("Número de Publicações")
    plt.grid(axis='y')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer

def keyfreano(data):
    most_frequent_word_per_year = {}
    for item in data:
        if 'publish_date' in item and 'keywords' in item:
            year = item['publish_date'].split('-')[0]  
            keywords = item['keywords']  
            valid_keywords = []
            for keyword in keywords:
                keyword = keyword.strip().lower()  
                if len(keyword) > 1 and re.match(r'^[a-zá-ú]+$', keyword): 
                    valid_keywords.append(keyword)
            keyword_counter = Counter(valid_keywords)
            if keyword_counter:
                most_common_word, count = keyword_counter.most_common(1)[0]
                most_frequent_word_per_year[year] = (most_common_word, count)
    years = sorted(most_frequent_word_per_year.keys())
    words = [most_frequent_word_per_year[year][0] for year in years]  
    counts = [most_frequent_word_per_year[year][1] for year in years] 
    plt.figure(figsize=(10, 6))
    plt.bar(years, counts, tick_label=words)
    plt.title("Distribuição da Palavra Mais Frequente por Ano")
    plt.xlabel("Ano")
    plt.ylabel("Frequência")
    plt.xticks(rotation=45)
    buffer = BytesIO()
    plt.tight_layout()  
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)  
    return buffer

def analise_publicacoes_por_autor(data, ordenar_por="frequencia"):
    autores = [artigo['name'] for artigo in data]
    contagem_autores = Counter(autores)
    if ordenar_por == "frequencia":
        autores_ordenados = sorted(contagem_autores.items(), key=lambda x: x[1], reverse=True)
    elif ordenar_por == "alfabetica":
        autores_ordenados = sorted(contagem_autores.items(), key=lambda x: x[0])
    result = ""
    for autor, freq in autores_ordenados:
        result += f"Autor: {autor} | Artigos: {freq}\n"
        for artigo in data:
            if artigo['name'] == autor:
                result += f" - {artigo['title']}\n"
        result += "\n"
    return result

def analise_publicacoes_por_palavras_chave(data, ordenar_por="frequencia"):
    palavras = [palavra for artigo in data for palavra in artigo['keywords']]
    contagem_palavras = Counter(palavras)
    if ordenar_por == "frequencia":
        palavras_ordenadas = sorted(contagem_palavras.items(), key=lambda x: x[1], reverse=True)
    elif ordenar_por == "alfabetica":
        palavras_ordenadas = sorted(contagem_palavras.items(), key=lambda x: x[0])
    result = ""
    for palavra, freq in palavras_ordenadas:
        result += f"Palavra-chave: {palavra} | Ocorrências: {freq}\n"
        for artigo in data:
            if palavra in artigo['keywords']:
                result += f" - {artigo['title']}\n"
        result += "\n"
    return result