from fun import *
import FreeSimpleGUI as sg 
import calendar 
from datetime import datetime 
import matplotlib.pyplot as plt
from io import BytesIO

sg.theme('SystemDefault')

def wprincipal():
    coluna1 = [
        
        [sg.Button('Importar',key='-IMPORTAR-',font=('Times New Romen',20,'bold'),size=(20,1)),
            sg.Text(" " * 5),
            sg.Button('Consultar',key='-CONSULTAR-',font=('Times New Romen',20,'bold'),size=(20,1))],
        [sg.Text(font=15)],
        [sg.Button('Listar Autores',key='-AUTORES-',font=('Times New Romen',20,'bold'),size=(20,1)),
            sg.Text(" " * 5),
            sg.Button('Relatórios',key='-RELATORIO-',font=('Times New Romen',20,'bold'),size=(20,1))],
    ]

    separador = [sg.Canvas(size=(1, 500), background_color='#FFFDD0', key='-SEPARATOR-')]
    
    layout = [
        [
            [sg.Text('Bem vindo ao PubScience', key='-TITULO-', font=('Times New Romen', 30, 'bold'), text_color='Darkblue', expand_y=True,justification='center',expand_x=True)],
            [sg.Button('Help',key='-HELP-',font=('Times New Romen',20,'bold'),size=(5,1))],
            [sg.Text(text='',key='-MAININFO-',font=('Times New Romen', 20), text_color='red', expand_y=True,justification='center',expand_x=True)],
            [
                sg.Column(layout=coluna1, expand_y=True,justification='center')
            ],
            [sg.Button('Sair',key='-SAIR-',font=('Times New Romen',20,'bold'),size=(5,1))]]
    ]

    wprincipal = sg.Window('Sistema de Consulta e Análise de Publicações Científicas', layout, resizable=True).Finalize()
    wprincipal.Maximize()

    global filtered_data
    data = None
    filepath = None
    stop = False
    #ficheiro = None
    while not stop:
        event, values = wprincipal.read()
        if event == sg.WINDOW_CLOSED or event == '-SAIR-':
            stop = True
        elif event == '-HELP-':
            whelp()
        elif event =='-IMPORTAR-':
            data, filepath = wficheirogui()
            if data:
                print(data)
                wprincipal['-MAININFO-'].update("Ficheiro importado com sucesso!", text_color="green")
            else:
                wprincipal['-MAININFO-'].update("Erro ao importar ficheiro!", text_color="red")
        elif event =='-CONSULTAR-' and not data:
            wprincipal['-MAININFO-'].update("Ainda não selecinou um ficheiro")
        elif event =='-CONSULTAR-' and data: 
            wconsultar(data, filepath)
        elif event =='-AUTORES-' and not data:
            wprincipal['-MAININFO-'].update("Ainda não selecinou um ficheiro")
        elif event =='-AUTORES-' and data: 
            wlistar(data)
        elif event =='-RELATORIO-' and not data:
            wprincipal['-MAININFO-'].update("Ainda não selecinou um ficheiro")
        elif event =='-RELATORIO-' and data: 
            wrelatorios(data)
    wprincipal.close()

def whelp():
    layout = [
        [sg.Text("Se pretende importar um ficheiro, clique em: Importar",font=('Times New Romen',7,"bold"), text_color = 'darkblue')],
        [sg.Text("Se pretende consultar publicações, clique em: Consultar",font=('Times New Romen',7,"bold"), text_color = 'darkblue')],
        [sg.Text("Se pretende listar todos os autores, clique em: Listar Autores",font=('Times New Romen',7,"bold"), text_color = 'darkblue')],
        [sg.Text("Se pretende ver relatórios, clique em: Relatório",font=('Times New Romen',7,"bold"), text_color = 'darkblue')]
    ]
    whelp = sg.Window('HELP!',layout, size=(400, 200), resizable=True)
    stop = False
    while not stop:
        event, values = whelp.read()
        if event == sg.WINDOW_CLOSED:
            stop = True
    whelp.close()


def wficheirogui():
    coluna = [
        [sg.Canvas(size=(200, 27), background_color='white'),
            sg.Button("Browse",key='-BROWSE-', font=('Times New Romen',10,"bold"),button_color = 'darkblue', size=(7,1))]
    ]
    
    layout = [
        [sg.Text('Escolha o ficheiro📂',key='-TEXTO-',font=('Times New Romen',20,"bold"), text_color = 'darkblue',justification = 'center', expand_x=True)],
        [
            sg.Column(layout=coluna, expand_y=True,justification='center')
        ],
        [sg.Text('',key='-INF-',font=('Times New Romen',7,"bold"), text_color = 'darkblue', expand_x=True)]
    ]
    wficheiro = sg.Window('Escolha o ficheiro',layout, size=(400, 150), resizable=True)
    data = [] 
    stop = False
    while not stop:
        event, values = wficheiro.read()
        if event == sg.WINDOW_CLOSED:
            data = None
            stop = True
            return data
        elif event == '-BROWSE-': 
            filepath = file()
            data = importargui(filepath)
            if data:
                stop = True
                wficheiro.close()
                return data, filepath
            else:
                wficheiro['-INF-'].update("Erro na importação ou operação cancelada! Tente outravez.",text_color='red') 


def wConfirmacao():
    layout=[
        [sg.Text('Tem a certeza que quer eliminar a publicação?',key='-TEXTO-',font=('Times New Romen',15,"bold"), text_color = 'red',justification = 'center', expand_x=True)],
        [sg.Button("Sim",font=('Times New Romen',10,"bold"), button_color = 'green',size=(7,1)),
            sg.Button("Não",font=('Times New Romen',10,"bold"), button_color = 'red',size=(7,1))]
    ]
    wConfirmacao =sg.Window('Confirmação',layout)

    stop = False
    while not stop:
        event,values= wConfirmacao.read()
        if event == sg.WINDOW_CLOSED:
            stop = True
        elif event == 'Sim':
            res= True
            stop = True
        elif event == 'Não':
            res=False
            stop = True
    wConfirmacao.close()
    return res

def wFilterPub(publicacoes):
    layout = [
        [sg.Text(key='-INFO-', text_color='red', font=('Times New Romen', 15))],
        [sg.Text('Título', key='-TITULO-', font=('Times New Romen', 20, "bold"), text_color='darkblue'),
         sg.Input(key='-FILTROTITULO-', font=('Times New Romen', 20), size=(30, 1))],
        [sg.Text('Autor', key='-AUTOR-', font=('Times New Romen', 20, "bold"), text_color='darkblue'),
         sg.Input(key='-FILTROAUTOR-', font=('Times New Romen', 20), size=(30, 1))],
        [sg.Text('Afiliação', key='-AFIL-', font=('Times New Romen', 20, "bold"), text_color='darkblue'),
         sg.Input(key='-FILTROAFIL-', font=('Times New Romen', 20), size=(30, 1))],
        [sg.Text('Palavras-chave (separadas por vírgulas)', key='-KEY-', font=('Times New Romen', 20, "bold"), text_color='darkblue'),
         sg.Input(key='-FILTROKEY-', font=('Times New Romen', 20), size=(30, 1))],
        [sg.Text('Ano de Publicação', key='-ANO-', font=('Times New Romen', 20, "bold"), text_color='darkblue'),
         sg.Input(key='-FILTROANO-', font=('Times New Romen', 20), size=(10, 1))],
        [sg.Button('Filtrar', key='-ATIVARFILTRO-', font=('Times New Romen', 20, "bold"))]
    ]

    janela = sg.Window('Filtro de Publicações', layout)

    stop = False
    while not stop:
        event, values = janela.read()
        if event == sg.WINDOW_CLOSED:
            stop = True
        elif event == '-ATIVARFILTRO-':
            title = values['-FILTROTITULO-'].strip() or None
            name = values['-FILTROAUTOR-'].strip() or None
            affiliation = values['-FILTROAFIL-'].strip() or None
            keywords = values['-FILTROKEY-'].strip()
            keywords = [kw.strip() for kw in keywords.split(',')] if keywords else None
            year = values['-FILTROANO-'].strip() or None

            filtered_data = []
            for item in publicacoes:
                if title and title.lower() not in item.get('title', '').lower():
                    continue
                if name and name.lower() not in item.get('name', '').lower():
                    continue
                if affiliation and affiliation.lower() not in item.get('affiliation', '').lower():
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

            sg.popup(f"Publicações filtradas: {len(filtered_data)}", title="Resultado")
            print(filtered_data) 
            stop = True
    janela.close()
    return filtered_data

def criarPub(data, filepath):
    layout = [
        [sg.Text("Título da Publicação", font=('Times New Romen', 15)), 
         sg.InputText(key="-TITLE-", font=('Times New Romen', 15), size=(50, 1))],
        [sg.Text("Data de Publicação (YYYY-MM-DD)", font=('Times New Romen', 15)), 
         sg.InputText(key="-DATE-", font=('Times New Romen', 15), size=(20, 1))],
        [sg.Text("Palavras-chave (separadas por vírgula)", font=('Times New Romen', 15)), 
         sg.InputText(key="-KEYWORDS-", font=('Times New Romen', 15), size=(50, 1))],
        [sg.Text("Número de Autores", font=('Times New Romen', 15)),
         sg.Spin([i for i in range(1, 11)], key="-NUM_AUTHORS-", initial_value=1, font=('Times New Romen', 15))],
        [sg.Text("DOI (Opcional)", font=('Times New Romen', 15)), 
         sg.InputText(key="-DOI-", font=('Times New Romen', 15), size=(50, 1))],
        [sg.Text("Link do PDF (Opcional)", font=('Times New Romen', 15)), 
         sg.InputText(key="-PDF-", font=('Times New Romen', 15), size=(50, 1))],
        [sg.Text("Link da URL (Opcional)", font=('Times New Romen', 15)), 
         sg.InputText(key="-URL-", font=('Times New Romen', 15), size=(50, 1))],
        [sg.Text("Resumo da Publicação (Opcional)", font=('Times New Romen', 15)),
         sg.Multiline(key="-ABSTRACT-", font=('Times New Romen', 15), size=(50, 5))],
        [sg.Button("Adicionar Autor", font=('Times New Romen', 15)), sg.Button("Confirmar Publicação", font=('Times New Romen', 15))],
        [sg.Text("", key="-STATUS-", text_color="red", font=('Times New Romen', 12))]
    ]
    
    janela = sg.Window("Criar Publicação", layout)
    
    authors = []
    stop = False
    while not stop:
        event, values = janela.read() 
        if event == sg.WINDOW_CLOSED:
            stop = True    
        elif event == "Adicionar Autor":
            num_authors = values["-NUM_AUTHORS-"]
            for i in range(num_authors):
                name = sg.popup_get_text("Nome do Autor", "Insira o nome do autor", size=(50, 1))
                affiliation = sg.popup_get_text("Afiliação", "Insira a afiliação do autor", size=(50, 1))
                orcid = sg.popup_get_text("ORCID", "Insira o ORCID do autor", size=(50, 1))
                authors.append({"name": name, "affiliation": affiliation, "orcid": orcid})
            
            janela["-STATUS-"].update(f"{num_authors} autor(es) adicionado(s)!", text_color="green")
        elif event == "Confirmar Publicação":
            publish_date = values["-DATE-"].strip()
            
            if publish_date:
                try:
                    datetime.strptime(publish_date, "%Y-%m-%d")
                except ValueError:
                    janela["-STATUS-"].update("A data deve estar no formato YYYY-MM-DD.", text_color="red")
                    continue
            
            new_pub = {
                "ID": max([item["ID"] for item in data]) + 1 if data else 1,
                "title": values["-TITLE-"].strip() or "N/A",
                "publish_date": publish_date,
                "keywords": values["-KEYWORDS-"].strip() or "N/A",
                "authors": authors,
                "doi": values["-DOI-"].strip() or "N/A",
                "pdf": values["-PDF-"].strip() or "N/A",
                "url": values["-URL-"].strip() or "N/A",
                "abstract": values["-ABSTRACT-"].strip() or "N/A"
            }
            
            data.append(new_pub)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            janela["-STATUS-"].update("Publicação criada com sucesso!", text_color="green")
            publicacoes = publicacoesc(data)
            stop = True
            return publicacoes
    janela.close()

def process_authors(pub):
    names = pub['name'].split(" | ")
    affiliations = pub['affiliation'].split(" | ") if 'affiliation' in pub else []
    orcids = pub['orcid'].split(" | ") if 'orcid' in pub else []

    max_len = len(names)
    affiliations.extend(['N/A'] * (max_len - len(affiliations)))
    orcids.extend(['N/A'] * (max_len - len(orcids)))

    authors = []
    for i in range(max_len):
        authors.append({
            "name": names[i],
            "affiliation": affiliations[i],
            "orcid": orcids[i]
        })
    return authors

def format_authors(authors):
    names = " | ".join([author['name'] for author in authors])
    affiliations = " | ".join([author['affiliation'] for author in authors])
    orcids = " | ".join([author['orcid'] for author in authors])
    return names, affiliations, orcids

def editarpublicacao(pub, data, filepath, original_id):
    authors = process_authors(pub)
    num_authors = len(authors)

    layout = [
        [sg.Text("Editar Detalhes da Publicação:", font=('Times New Roman', 30, "bold"), text_color='darkblue')],
        [sg.Text("Título:", font=('Times New Roman', 10, 'bold')),
         sg.Input(pub['title'], key='-TITULO-', font=('Times New Roman', 10), size=(100, 1))],
        [sg.Text("ID:", font=('Times New Roman', 10, 'bold')),
         sg.Input(pub['ID'], key='-ID-', font=('Times New Roman', 10), size=(20, 1))],
        [sg.Text("Data de Publicação:", font=('Times New Roman', 10, 'bold')),
         sg.Input(pub['publish_date'], key='-PUBLISH_DATE-', font=('Times New Roman', 10), size=(20, 1))],
        [sg.Text("Resumo:", font=('Times New Roman', 10, 'bold')),
         sg.Multiline(pub['abstract'], size=(109, 5), key='-ABSTRACT-', font=('Times New Roman', 10))],
        [sg.Text("Palavras-chave:", font=('Times New Roman', 10, 'bold')),
         sg.Multiline(pub['keywords'], size=(109, 3), key='-KEYWORDS-', font=('Times New Roman', 10))],
        [sg.Text("DOI:", font=('Times New Roman', 10, 'bold')),
         sg.Input(pub['doi'], key='-DOI-', font=('Times New Roman', 10), size=(100, 1))],
        [sg.Text("PDF:", font=('Times New Roman', 10, 'bold')),
         sg.Input(pub['pdf'], key='-PDF-', font=('Times New Roman', 10), size=(100, 1))],
        [sg.Text("URL:", font=('Times New Roman', 10, 'bold')),
         sg.Input(pub['url'], key='-URL-', font=('Times New Roman', 10), size=(100, 1))],
    ]

    for i, author in enumerate(authors):
        layout.append([
            sg.Text(f"Autor {i + 1}:", font=('Times New Roman', 10, 'bold')),
            sg.Input(author['name'], key=f'-NAME_{i}-', font=('Times New Roman', 10), size=(30, 1)),
            sg.Input(author['affiliation'], key=f'-AFFILIATION_{i}-', font=('Times New Roman', 10), size=(30, 1)),
            sg.Input(author['orcid'], key=f'-ORCID_{i}-', font=('Times New Roman', 10), size=(30, 1))
        ])

    layout.append([sg.Button("Adicionar Autor", key="-ADICIONAR_AUTOR-"), sg.Button("Confirmar Alterações", key="-CONFIRMAR-")])

    janela = sg.Window('Editar Publicação', layout, resizable=True).Finalize()

    while True:
        event, values = janela.read()

        if event in (sg.WINDOW_CLOSED, '-CANCELAR-'):
            janela.close()
            return data

        elif event == '-ADICIONAR_AUTOR-':
            layout.insert(-1, [
                sg.Text(f"Autor {num_authors + 1}:", font=('Times New Roman', 10, 'bold')),
                sg.Input('', key=f'-NAME_{num_authors}-', font=('Times New Roman', 10), size=(30, 1)),
                sg.Input('N/A', key=f'-AFFILIATION_{num_authors}-', font=('Times New Roman', 10), size=(30, 1)),
                sg.Input('N/A', key=f'-ORCID_{num_authors}-', font=('Times New Roman', 10), size=(30, 1))
            ])
            janela.extend_layout(janela, [layout[-2]])
            num_authors += 1

        elif event == '-CONFIRMAR-':
            updated_authors = []
            for i in range(num_authors):
                name = values.get(f'-NAME_{i}-', '').strip()
                affiliation = values.get(f'-AFFILIATION_{i}-', 'N/A').strip()
                orcid = values.get(f'-ORCID_{i}-', 'N/A').strip()
                if name:  
                    updated_authors.append({"name": name, "affiliation": affiliation, "orcid": orcid})

            pub['title'] = values['-TITULO-']
            pub['ID'] = values['-ID-']
            pub['publish_date'] = values['-PUBLISH_DATE-']
            pub['abstract'] = values['-ABSTRACT-']
            pub['keywords'] = values['-KEYWORDS-']
            pub['doi'] = values['-DOI-']
            pub['pdf'] = values['-PDF-']
            pub['url'] = values['-URL-']

            names, affiliations, orcids = format_authors(updated_authors)
            pub['name'] = names
            pub['affiliation'] = affiliations
            pub['orcid'] = orcids

            updated = False
            for i, p in enumerate(data):
                if p['ID'] == original_id:  
                    data[i] = pub  
                    updated = True
                    break
            if not updated:
                data.append(pub)  
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                sg.popup("Publicação atualizada com sucesso!")
            except Exception as e:
                sg.popup_error(f"Erro ao salvar os dados: {e}")
            finally:
                janela.close()
                return data


def wPublicacao(pub, data, filepath, publicacoes):
    if pub is None:
        pub = {"ID": None,"abstract": "","keywords": "","name": "","affiliation": "", "orcid":"","doi": "","pdf": "","publish_date": "","title": "","url": ""}
    
    coluna1 = [
        [sg.Text("Detalhes da Publicação:", font=('Times New Roman', 30, "bold"), text_color='darkblue')],
        [sg.Text("Título:", font=('Times New Roman', 10,'bold')), sg.Column([[sg.Text(pub['title'], key='-TITULO-', font=('Times New Roman', 10))]],background_color="white",size=(740, 30)),
            sg.Text("ID:", font=('Times New Roman', 10,'bold')), sg.Column([[sg.Text(pub['ID'], key='-ID-', font=('Times New Roman', 10))]],background_color="white",size=(30, 30)),
            sg.Text("Data de Publicação:", font=('Times New Roman', 10,'bold')), sg.Column([[sg.Text(pub['publish_date'], key='-DATA-', font=('Times New Roman', 10))]],background_color="white",size=(90, 30))],
        [sg.Text("Resumo:", font=('Times New Roman', 10,'bold')), sg.Multiline(pub['abstract'], size=(109, 5), disabled=True, key='-ABSTRACT-', font=('Times New Roman', 10)),
            sg.Text("Palavras-chave:", font=('Times New Roman', 10,'bold')), sg.Multiline(pub['keywords'],size=(32, 5), disabled=True, key='-KEYWORDS-', font=('Times New Roman', 10))],
        [sg.Text("Autores:", font=('Times New Roman', 10,'bold')), sg.Multiline(pub['name'], key='-AUTORES-',size=(45, 5), disabled=True, font=('Times New Roman', 10)),
            sg.Text("Afiliação:", font=('Times New Roman', 10,'bold')), sg.Multiline(pub['affiliation'], key='-AFILIACAO-',size=(45, 5), disabled=True, font=('Times New Roman', 10)),
            sg.Text("Orcid:", font=('Times New Roman', 10,'bold')), sg.Multiline(pub['orcid'], key='-ORCID-',size=(45, 5), disabled=True, font=('Times New Roman', 10))],
        [sg.Text("DOI:", font=('Times New Roman', 10,'bold')), sg.Column([[sg.Text(pub['doi'], key='-DOI-', font=('Times New Roman', 10))]],background_color="white",size=(800, 30))],
        [sg.Text("PDF:", font=('Times New Roman', 10,'bold')), sg.Column([[sg.Text(pub['pdf'], key='-PDF-', font=('Times New Roman', 10))]],background_color="white",size=(800, 30))],
        [sg.Text("URL:", font=('Times New Roman', 10,'bold')), sg.Column([[sg.Text(pub['url'], key='-URL-', font=('Times New Roman', 10))]],background_color="white",size=(800, 30))],
        [sg.Button("Fechar", key='-FECHAR-', font=('Times New Roman', 10,'bold'),size=(10,1))] ]

    layout = [
        [sg.Button("Apagar Publicação",key='-APAGAR-',font=('Times New Roman', 15,'bold'),size=(15,1)),
            sg.Button("Criar Publicação",key='-CRIAR-',font=('Times New Roman', 15,'bold'),size=(15,1)),
            sg.Button("Editar Publicação",key='-EDITAR-',font=('Times New Roman', 15,'bold'),size=(15,1))],
        [
            sg.Column(layout=coluna1, expand_y=True,justification='center')
        ],
        [sg.Text(text=" ",key='-ERROS-' ,font=('Times New Romen', 15), text_color='red')]
    ]
    wPublicacao = sg.Window('Consultar Publicação', layout, resizable=True).Finalize()
    wPublicacao.Maximize()
    stoppub = False
    while not stoppub:
        event, values = wPublicacao.read()
        if event == sg.WINDOW_CLOSED or event == '-FECHAR-':
            stoppub = True
        elif event =='-EDITAR-':
            editarpublicacao(pub, data, filepath, original_id=pub['ID'])
            publicacoes = publicacoesc(data)
            wPublicacao.close()
            return publicacoes
        elif event == '-CRIAR-':
            criarPub(data, filepath)
            stoppub = True
            return publicacoes
        elif event== '-APAGAR-':
            res = wConfirmacao()
            if res == True:
                if pub is not None:
                    deletepubgui(pub, data, filepath)
                    sg.popup("Publicação apagada com sucesso!")
                    publicacoes = publicacoesc(data)
                    stoppub = True
                    return publicacoes
            else:
                wPublicacao['-ERROS-'].update("Ação de eliminação cancelada!", text_color='red')        
    wPublicacao.close()

def publicacoesc(data):
    publicacoes = []
    for pub in data:
        if isinstance(pub, dict):
            id = pub.get("ID", "N/A")
            abstract = pub.get("abstract", "N/A")
            keywords = pub.get("keywords", "N/A")
            name = " | ".join([author.get("name", "N/A") for author in pub.get("authors", [])])
            affiliation = " | ".join([author.get("affiliation", "N/A") for author in pub.get("authors", [])])
            orcid = " | ".join([author.get("orcid", "N/A") for author in pub.get("authors", [])])
            doi = pub.get("doi", "N/A")
            pdf = pub.get("pdf", "N/A")
            publish_date = pub.get("publish_date", "N/A")
            title = pub.get("title", "N/A")
            url = pub.get("url", "N/A")
            print(f"ID: {id}, Título: {title}, Keywords: {keywords}, Data: {publish_date}")
            publicacao = {
                "ID": id,
                "abstract": abstract,
                "keywords": keywords,
                "name": name,
                "affiliation": affiliation,
                "orcid": orcid,
                "doi": doi,
                "pdf": pdf,
                "publish_date": publish_date,
                "title": title,
                "url": url
            }
            publicacoes.append(publicacao) 
        else:
            print(f"Invalid data format: {pub}")
    return publicacoes

def wconsultar(data, filepath): 
    ori = True
    publicacoes = publicacoesc(data)
    layout = [
        [sg.Text("Publicações", key='-TITULO-', font=('Times New Roman', 20, 'bold'), text_color='darkblue', expand_y=True)],
        [sg.Button("Filtrar", key='-FILTRO-', font=('Times New Roman', 20, 'bold')),
         sg.Button("Limpar filtros", key='-LIMPAR-', font=('Times New Roman', 20, 'bold'))],
        
        [sg.Table(values=[[pub.get("title", "N/A"),pub.get("name", "N/A"),pub.get("affiliation", "N/A"), pub.get("publish_date", "N/A"),pub.get("keywords", "N/A")
                           ] for pub in publicacoes
            ],
            headings=["Título", "Autores", "Afiliações", "Data de publicação", "Palavras-chave"],
            auto_size_columns=True,
            header_text_color='blue',
            justification='center',
            display_row_numbers=False,
            num_rows=min(5, len(publicacoes)),
            key='-TABELA-',
            enable_events=True,
            enable_click_events=True,
            vertical_scroll_only=True,
            font=('Times New Roman',12),
            expand_x=True,
            expand_y=True
        )],
        [sg.Text("Clique numa publicação para ver mais detalhes", key='-INFO-', font=('Times New Roman', 10), text_color='darkblue')],
        [sg.Button('Sair', key='-SAIR-', font=('Times New Roman', 20, 'bold'), size=(5, 1))],
        [sg.Button('Atualizar', key='-ATUALIZAR-', font=('Times New Roman', 7, 'bold'), size=(10, 1))]
    ]

    wconsultar = sg.Window('Consultar Publicações', layout, resizable=True).Finalize()
    wconsultar.Maximize()  

    stop = False
    while not stop:
        event, values = wconsultar.read()
        if event == sg.WINDOW_CLOSED or event == '-SAIR-':
            stop = True
        elif event == ('-TABELA-', '+CLICKED+', (-1, 0)):
            ori = not ori
            publicacoes = ordpubtitulo(publicacoes,ori)
            wconsultar['-TABELA-'].update(
                values=[
                    [pub.get("title", "N/A"),pub.get("name", "N/A"),pub.get("affiliation", "N/A"), pub.get("publish_date", "N/A"),pub.get("keywords", "N/A")
                           ] for pub in publicacoes
                ]
            )              
        elif event == ('-TABELA-', '+CLICKED+', (-1, 1)):
            ori = not ori
            publicacoes = ordpubnome(publicacoes,ori)
            wconsultar['-TABELA-'].update(
                values=[
                    [pub.get("title", "N/A"),pub.get("name", "N/A"),pub.get("affiliation", "N/A"), pub.get("publish_date", "N/A"),pub.get("keywords", "N/A")
                           ] for pub in publicacoes
                ]
            )
            
        elif event == ('-TABELA-', '+CLICKED+', (-1, 3)):
            ori = not ori
            publicacoes = ordpubdata(publicacoes,ori)
            wconsultar['-TABELA-'].update(
                values=[
                    [pub.get("title", "N/A"),pub.get("name", "N/A"),pub.get("affiliation", "N/A"), pub.get("publish_date", "N/A"),pub.get("keywords", "N/A")
                           ] for pub in publicacoes
                ]
            )
        elif event == '-FILTRO-':
            publicacoes = wFilterPub(publicacoes)  
            wconsultar['-TABELA-'].update(
                values = [
                    [pub.get("title", "N/A"),pub.get("name", "N/A"),pub.get("affiliation", "N/A"), pub.get("publish_date", "N/A"),pub.get("keywords", "N/A")
                    ] for pub in publicacoes]  
            )
        elif event == '-LIMPAR-':
            publicacoes = publicacoesc(data)
            wconsultar['-TABELA-'].update(
                values=[
                    [pub.get("title", "N/A"),pub.get("name", "N/A"),pub.get("affiliation", "N/A"), pub.get("publish_date", "N/A"),pub.get("keywords", "N/A")
                           ] for pub in publicacoes
                ]
            )
        elif event == '-TABELA-' and values['-TABELA-']!=[]:
            linha_selec = values['-TABELA-'][0]
            if linha_selec is not None:
                dadosselec = publicacoes[linha_selec]
                pub = dadosselec
                wPublicacao(pub, data, filepath, publicacoes)
        elif event == '-ATUALIZAR-':
            publicacoes = publicacoesc(data)
            wconsultar['-TABELA-'].update(
                values=[
                    [pub.get("title", "N/A"),pub.get("name", "N/A"),pub.get("affiliation", "N/A"), pub.get("publish_date", "N/A"),pub.get("keywords", "N/A")
                           ] for pub in publicacoes
                ]
            )
    wconsultar.close()

def wrelatorios(data):
    coluna1 = [
        [sg.Button('Distribuição de publicações por ano',key='-PUBANO-',font=('Times New Romen',15,'bold'),size=(40,1)),
            sg.Text(" " * 5),
            sg.Button('Distribuição de publicações por mês',key='-PUBMES-',font=('Times New Romen',15,'bold'),size=(40,1))],
        [sg.Text(font=15)],
        [sg.Button('Número de publicações por autor',key='-NUMPUBAUT-',font=('Times New Romen',15,'bold'),size=(40,1)),
            sg.Text(" " * 5),
            sg.Button('Distribuição de publicações de um autor por anos',key='-PUBAUTANO-',font=('Times New Romen',15,'bold'),size=(40,1))],
        [sg.Text(font=15)],
        [sg.Button('Distribuição de palavras-chave pela sua frequência',key='-KEYFREQ-',font=('Times New Romen',15,'bold'),size=(40,1)),
            sg.Text(" " * 5),
            sg.Button('Distribuição de palavras-chave mais frequente por ano.',key='-KEYANO-',font=('Times New Romen',15,'bold'),size=(40,1))]
    ]
    layout = [
        [
            [sg.Text('Estatísticas de Publicação:', key='-TITULO-', font=('Times New Romen', 30, 'bold'), text_color='darkblue', expand_y=True,justification='center',expand_x=True)],
            [sg.Text(text='',key='-MAININFO-',font=('Times New Romen', 20), text_color='red', expand_y=True,justification='center',expand_x=True)],
            [
                sg.Column(layout=coluna1, expand_y=True,justification='center')
            ],
            [sg.Button('Sair',key='-SAIR-',font=('Times New Romen',20,'bold'),size=(5,1))]]
    ]
    wrelatorios = sg.Window('Gráficos de Estatísticas de Publicações', layout, resizable=True).Finalize()
    wrelatorios.Maximize()

    stop = False
    while not stop:
        event, values = wrelatorios.read()
        if event == sg.WINDOW_CLOSED or event == '-SAIR-':
            stop = True
        elif event == '-PUBANO-':
            wpubano(data)
        elif event == '-PUBMES-':
            wpubmes(data)
        elif event == '-NUMPUBAUT-':
            wpubsautor(data)    
        elif event == '-PUBAUTANO-':
            wpubautorano(data)
        elif event == '-KEYFREQ-':
            wpubskeyword(data)
        elif event == '-KEYANO-':
            wkeyfreano(data)
    wrelatorios.close()  

def wpubano(data):
    graph_buffer = relPubAnosgui(data)
    layout = [
        [sg.Image(data=graph_buffer.getvalue(), key='-GRAPH-')],
        [sg.Button('Sair', font=('Times New Romen', 20, 'bold'))]
    ]
    wpubano = sg.Window('Distribuição de publicações por ano', layout, finalize=True, element_justification='center').Finalize()
    stop=False
    while not stop:
        event, values = wpubano.read()
        if event == sg.WIN_CLOSED or event == 'Sair':
            stop=True
    wpubano.close()
    graph_buffer.close()

def wpubmes(data):

    layout = [
        [sg.Button('Distribuição por Ano', key='-PUBMES-', font=('Times New Romen', 20))],
        [sg.Button('Sair', font=('Times New Romen', 20))]
    ]
    janela = sg.Window('Publicações por Mês', layout, finalize=True, element_justification='center')

    stopp = False
    while not stopp:
        event, values = janela.read()

        if event in (sg.WIN_CLOSED, 'Sair'):
            stopp = True
        elif event == '-PUBMES-':
            ano = sg.popup_get_text('Digite o ano para a análise:', title='Selecionar Ano')
            if not ano or not ano.isdigit():
                sg.popup_error("Ano inválido. Tente novamente.")
                continue
            ano = int(ano)
            graph_buffer = distribPubPorMesgui(data, ano)
            layout_grafico = [
                [sg.Image(data=graph_buffer.read(), key='-GRAPH-')],
                [sg.Button('Fechar', font=('Times New Romen', 20))]
            ]
            janela_grafico = sg.Window(f'Distribuição de Publicações por Mês - {ano}', layout_grafico)
            graph_buffer.close()
            
            stop = True
            while stop:
                event_graph, _ = janela_grafico.read()
                if event_graph in (sg.WIN_CLOSED, 'Fechar'):
                    stop = False
            janela_grafico.close()
    janela.close()

def wpubsautor(data):
    layout = [
        [sg.Image(data=None, key='-GRAPH-')], 
        [sg.Button('Fechar', font=('Times New Romen', 20))]
    ]
    
    janela = sg.Window('Distribuição de Publicações por Autor - Top 20', layout, finalize=True, element_justification='center')

    graph_buffer = relPubAutorgui(data, top_n=20)

    if graph_buffer is None:
        sg.popup_error("Erro ao gerar o gráfico.")
        janela.close()
        return

    graph_data = graph_buffer.read()
    graph_buffer.close() 

    janela['-GRAPH-'].update(data=graph_data)

    event, values = janela.read()
    if event in (sg.WIN_CLOSED, 'Fechar'):
        janela.close()
    janela.close()

def selecionar_autor(data):
    autores_disponiveis = autoresgui(data)
    if not autores_disponiveis:
        sg.popup_error("Nenhum autor disponível para seleção.")
        return None
    autor_parcial = sg.popup_get_text('Digite o nome do autor para a análise (ou parte do nome):', title='Selecionar Autor')
    if not autor_parcial:
        sg.popup_error("Nenhum autor fornecido!")
        return None
    resultados = [autor for autor in autores_disponiveis if autor_parcial.lower() in autor.lower()]
    if not resultados:
        sg.popup_error(f"Nenhum autor encontrado para: {autor_parcial}")
        return None
    autor_escolhido = sg.popup_get_text(f'Escolha um autor da lista (digite o número):\n\n' + '\n'.join([f"{i+1}. {autor}" for i, autor in enumerate(resultados)]), title='Escolher Autor')
    if autor_escolhido:
        try:
            autor_escolhido = int(autor_escolhido)
            if 1 <= autor_escolhido <= len(resultados):
                return resultados[autor_escolhido - 1]
            else:
                sg.popup_error("Seleção inválida!")
        except ValueError:
            sg.popup_error("Entrada inválida! Digite um número.")
    return None

def wpubautorano(data):
    layout = [
        [sg.Button('Distribuição de Publicações por Autor', key='-PUBAUTOR-', font=('Times New Romen', 20))],
        [sg.Button('Sair', font=('Times New Romen', 20))]
    ]
    janela = sg.Window('Publicações por Autor', layout, finalize=True, element_justification='center')
    continue_loop = True 
    while continue_loop:
        event, values = janela.read()
        if event in (sg.WIN_CLOSED, 'Sair'):
            continue_loop = False
        elif event == '-PUBAUTOR-':
            autor = None
            autor = selecionar_autor(data)
            if not autor:
                sg.popup_error("Autor inválido. Tente novamente.")
                continue  
            graph_buffer = PubAutoPorAnogui(data, autor)

            if graph_buffer is None:
                continue  
            layout_grafico = [
                [sg.Image(data=graph_buffer.read(), key='-GRAPH-')],
                [sg.Button('Fechar', font=('fixedsys', 20))]
            ]
            janela_grafico = sg.Window(f'Distribuição de Publicações por Ano - {autor}', layout_grafico)
            graph_buffer.close()

            stop = True 
            while stop:
                event_graph, _ = janela_grafico.read()
                if event_graph in (sg.WIN_CLOSED, 'Fechar'):
                    stop = False
            janela_grafico.close()
    janela.close()

def wpubskeyword(data):
    layout = [
        [sg.Image(data=None, key='-GRAPH-')],  # Local para exibir o gráfi
        [sg.Button('Fechar', font=('fixedsys', 10),size = (10,1))]
    ]
    
    janela = sg.Window('Distribuição de Palavras-chave - Top 20', layout, finalize=True, element_justification='center')
    
    graph_buffer = relkeywordsgui(data, top_n=20)
    if graph_buffer is None:
        sg.popup_error("Erro ao gerar o gráfico.")
        janela.close()
        return
    
    graph_data = graph_buffer.read()
    graph_buffer.close()  

    janela['-GRAPH-'].update(data=graph_data)

    event, values = janela.read()
    if event in (sg.WIN_CLOSED, 'Fechar'):
        janela.close()
    janela.close()
    

def wkeyfreano(data):  
    graph_buffer = keyfreano(data)
    
    layout = [
        [sg.Image(data=graph_buffer.getvalue(), key='-GRAPH-')],  
        [sg.Button('Sair', font=('fixedsys', 20))]  
    ]
    
    wpubano_window = sg.Window('Distribuição da Palavra Mais Frequente por Ano', layout, finalize=True, element_justification='center')
    
    stop = False
    while not stop:
        event, values = wpubano_window.read()
        if event == sg.WIN_CLOSED or event == 'Sair': 
            stop = True
    wpubano_window.close()
    graph_buffer.close()

def wlistar(data):
    layout = [
        [sg.Text("Análise de Publicações", size=(30, 1), font=("Helvetica", 20))],
        [sg.Text("Ordenar autores por:"), 
        sg.Radio("Frequência", "ordenar_autores", default=True, key="autor_frequencia"),
        sg.Radio("Ordem Alfabética", "ordenar_autores", key="autor_alfabetica")],
        [sg.Button("Exibir Publicações por Autor", key="mostrar_autores")],
        [sg.Text("Ordenar palavras-chave por:"), 
        sg.Radio("Frequência", "ordenar_palavras", default=True, key="palavra_frequencia"),
        sg.Radio("Ordem Alfabética", "ordenar_palavras", key="palavra_alfabetica")],
        [sg.Button("Exibir Publicações por Palavra-chave", key="mostrar_palavras")],
        [sg.Multiline("", size=(80, 20), key="resultado", font=("Helvetica", 12))]
    ]

    window = sg.Window("Sistema de Análise de Publicações", layout)

    stop = False
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            window.close()
        if event == "mostrar_autores":
            ordenar_por = "frequencia" if values["autor_frequencia"] else "alfabetica"
            resultado = analise_publicacoes_por_autor(data, ordenar_por)
            window["resultado"].update(resultado)
        if event == "mostrar_palavras":
            ordenar_por = "frequencia" if values["palavra_frequencia"] else "alfabetica"
            resultado = analise_publicacoes_por_palavras_chave(data, ordenar_por)
            window["resultado"].update(resultado)
    window.close()