import flet as ft
from tinydb import TinyDB
from whatsappHandle import enviar_mensagem
from printScreen import ScreenCaptureApp
import threading

# Inicializar o banco de dados
db = TinyDB('db.json')
mensagens_table = db.table('mensagens')
lixeira_table = db.table('lixeira')


# Função chamada quando a mensagem é clicada
def enviaMensagem(mensagem,page):
    def handle_dismissal(e):
        page.close(bs)

    bs = ft.BottomSheet(
        on_dismiss=handle_dismissal,
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text("O campo de mensagem do whatsapp não foi localizado. Vamos localiza-lo agora.  Com o mouse selecione o icone de EMOJI.")
                ],
            ),
        ),
    )
    # page.open(bs)
    status = enviar_mensagem(mensagem)
    if status == "CampoNaoEncontrado":
        page.open(bs)
        ScreenCaptureApp().capture_region()
        
        page.close(bs)
        enviar_mensagem(mensagem)



# Função para adicionar nova mensagem
def adicionar_mensagem(page, nova_mensagem, handleClose):
    # Salvar mensagem no banco de dados
    mensagens_table.insert({'mensagem': nova_mensagem, 'fixado': False})

    # Carregar novamente as mensagens após a inserção
    atualizar_mensagens(page)
    handleClose


# Função para editar mensagem
def editar_mensagem(page, mensagem_id, novo_texto, handleClose):
    # Atualizar o texto da mensagem no banco de dados
    mensagens_table.update({'mensagem': novo_texto}, doc_ids=[mensagem_id])

    # Atualizar a interface após a edição
    atualizar_mensagens(page)
    handleClose


# Função para excluir mensagem (movendo para a lixeira)
def excluir_mensagem(page, mensagem_id):
    # Excluir a mensagem do banco de dados e mover para a lixeira
    mensagens = mensagens_table.get(doc_ids=[mensagem_id])
    if mensagens:
        # A variável 'mensagens' é uma lista, então pegamos o primeiro item
        mensagem = mensagens[0]

        # Extrair os dados da mensagem, sem os metadados (como doc_id)
        mensagem_data = {key: mensagem[key] for key in mensagem if key != 'doc_id'}

        # Mover para a lixeira
        lixeira_table.insert(mensagem_data)  # Agora estamos inserindo um dicionário válido

        # Remover da tabela de mensagens
        mensagens_table.remove(doc_ids=[mensagem_id])

        # Carregar novamente as mensagens após a exclusão
    atualizar_mensagens(page)


# Função para excluir mensagem definitivamente da lixeira
def excluir_definitivamente(page, mensagem_id):
    # Excluir permanentemente a mensagem da lixeira
    lixeira_table.remove(doc_ids=[mensagem_id])

    # Atualizar a lixeira
    atualizar_lixeira(page)


# Função para carregar as mensagens da lixeira
def carregar_lixeira():
    return lixeira_table.all()


# Função para atualizar a lista de mensagens da lixeira
def atualizar_lixeira(page):
    # Carregar as mensagens da lixeira
    mensagens_lixeira = carregar_lixeira()

    cards_lixeira = []
    for mensagem in mensagens_lixeira:
        mensagem_id = mensagem.doc_id
        cards_lixeira.append(create_card_lixeira(mensagem_id, mensagem['mensagem'], page))  # Card para lixeira

    # Atualizar os cards da lixeira na interface
    page.controls.clear()  # Limpar os controles antigos
    page.add(
        topbar_lixeira,
        ft.Row(cards_lixeira, wrap=True),  # Usando wrap=True para permitir quebra de linha
        ft.ElevatedButton("Restaurar Todos", on_click=lambda e: restaurar_todos(page)),  # Botão de restaurar todos
    )
    page.update()


# Função para atualizar a lista de mensagens da lixeira
def atualizar_campoMensagem(page):
    ScreenCaptureApp().capture_region()


# Função para restaurar todas as mensagens da lixeira
def restaurar_todos(page):
    mensagens_lixeira = carregar_lixeira()
    for mensagem in mensagens_lixeira:
        # Remover o campo 'doc_id' para garantir que um novo ID seja gerado
        mensagem_sem_id = {key: mensagem[key] for key in mensagem if key != 'doc_id'}

        # Inserir a mensagem de volta na tabela de mensagens com um novo ID
        mensagens_table.insert(mensagem_sem_id)

    # Limpar a lixeira após a restauração
    lixeira_table.truncate()

    # Atualizar a interface da lixeira
    atualizar_lixeira(page)


# Função para fixar ou desfazer a fixação de uma mensagem
def fixar_mensagem(page, mensagem_id):
    # Buscar a mensagem pelo ID
    mensagens = mensagens_table.get(doc_ids=[mensagem_id])
    if mensagens:
        # Obter o primeiro item da lista, pois 'get' retorna uma lista
        mensagem = mensagens[0]

        # Verificar se a mensagem está fixada
        fixado_atual = mensagem['fixado']

        # Alternar o estado de fixação
        if fixado_atual:
            # Desmarcar como fixada
            mensagens_table.update({'fixado': False}, doc_ids=[mensagem_id])
        else:
            # Marcar como fixada
            mensagens_table.update({'fixado': True}, doc_ids=[mensagem_id])

        # Atualizar as mensagens para refletir as mudanças
        atualizar_mensagens(page)


def create_card_lixeira(mensagem_id, mensagem, page):
    def confirmar_exclusao(e):  # Adicionando o argumento 'e' para o evento
        # Exibe um modal para confirmar a exclusão definitiva
        modal_alerta = ft.AlertDialog(
            title=ft.Text("Confirmação de Exclusão"),
            content=ft.Text(
                "Esta ação não pode ser desfeita. Você tem certeza que deseja excluir a mensagem permanentemente?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.close(modal_alerta)),
                ft.TextButton("Excluir", on_click=lambda e: excluir_definitivamente(page, mensagem_id)),
            ],
        )
        page.open(modal_alerta)

    def restaurar_item(e):
        # Obter a mensagem da lixeira pelo ID
        mensagem = lixeira_table.get(doc_ids=[mensagem_id])[0]

        # Remover o campo 'doc_id' para garantir que um novo ID seja gerado
        mensagem_sem_id = {key: mensagem[key] for key in mensagem if key != 'doc_id'}

        # Inserir a mensagem de volta na tabela de mensagens com um novo ID
        mensagens_table.insert(mensagem_sem_id)

        # Remover a mensagem da lixeira
        lixeira_table.remove(doc_ids=[mensagem_id])

        # Atualizar a lixeira
        atualizar_lixeira(page)

    return ft.Card(
        content=ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            on_tap=lambda e: enviaMensagem(mensagem, page),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(mensagem),
                        ft.Row(
                            [
                                ft.IconButton(ft.Icons.RESTORE, tooltip="Restaurar", on_click=restaurar_item),
                                # Botão para restaurar
                                ft.IconButton(ft.Icons.DELETE_FOREVER, tooltip="Excluir definitivamente",
                                              on_click=confirmar_exclusao),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                padding=10,
            ),
        ),
        width=300,
    )


# Função para voltar para a página principal
def voltar_para_principal(page):
    # Atualiza a interface para mostrar as mensagens principais
    atualizar_mensagens(page)


# Função para esvaziar a lixeira
def esvaziar_lixeira(page):
    # Remover todas as mensagens da lixeira
    lixeira_table.truncate()

    # Atualizar a lixeira após esvaziar
    atualizar_lixeira(page)


# Função para atualizar a lista de mensagens exibidas
def atualizar_mensagens(page):
    # Carregar as mensagens salvas
    mensagens = mensagens_table.all()

    # Dividir mensagens fixadas e não fixadas
    cards_fixados = []
    cards_normais = []

    for mensagem in mensagens:
        mensagem_id = mensagem.doc_id
        if mensagem['fixado']:
            cards_fixados.append(create_card(mensagem_id, mensagem['mensagem'], "true", page))
        else:
            cards_normais.append(create_card(mensagem_id, mensagem['mensagem'], "false", page))

    # Atualizar os cards na interface
    page.controls.clear()  # Limpar os controles antigos
    page.add(
        topbar,
        # Dividir em duas seções: fixados e não fixados
        ft.ListView(
            [
                ft.Row(  # Exibir os cards fixados em uma linha
                    controls=cards_fixados,
                    wrap=True,  # Permitir quebra de linha se os cards não couberem
                ),
                ft.Row(  # Exibir os cards não fixados em uma linha separada
                    controls=cards_normais,
                    wrap=True,  # Permitir quebra de linha se os cards não couberem
                ),
            ],
            height=altura_dinamica,  # Definir altura do ListView
            padding=10  # Adicionar algum preenchimento
        ),
    )
    page.update()


# Função para criar um card de mensagem
def create_card(mensagem_id, mensagem, fixado, page):
    mensagem_editada = mensagem  # Inicialize a variável aqui

    def fixar_card():
        # Alterar o status de fixado no banco de dados
        fixar_mensagem(page, mensagem_id)

    def editar_card(e):
        # Modal para editar a mensagem
        modal_editar = ft.AlertDialog(
            title=ft.Text("Editar Mensagem"),
            content=ft.Column(
                [
                    ft.Text("Digite o novo texto para a mensagem:"),
                    ft.TextField(height=350, label="Mensagem", multiline=True, autofocus=True, value=mensagem,
                                 on_change=lambda e: atualizar_texto(e)),
                ], width=600
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.close(modal_editar)),
                ft.TextButton("Salvar", on_click=lambda e: editar_mensagem(page, mensagem_id, mensagem_editada,
                                                                           page.close(modal_editar))),
            ],
        )
        page.open(modal_editar)

    def atualizar_texto(e):
        nonlocal mensagem_editada
        mensagem_editada = e.control.value

    favoriteIcon = ft.IconButton(ft.Icons.FAVORITE_OUTLINE, tooltip="Fixar", on_click=lambda e: fixar_card())
    if fixado == "true":
        favoriteIcon = ft.IconButton(ft.Icons.FAVORITE, tooltip="Fixar", on_click=lambda e: fixar_card())

    return ft.Card(
        content=ft.GestureDetector(
            on_tap=lambda e: enviaMensagem(mensagem, page),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(mensagem),
                        ft.Row(
                            [
                                ft.IconButton(ft.Icons.EDIT, tooltip="Editar", on_click=editar_card),
                                ft.IconButton(ft.Icons.DELETE, tooltip="Excluir",
                                              on_click=lambda e: excluir_mensagem(page, mensagem_id)),
                                favoriteIcon,
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                padding=10,
            ),
        ),
        width=300,
    )


# Função principal do app
def main(page: ft.Page):
    # Definir altura como 100% da altura da janela
    global altura_dinamica
    altura_dinamica = page.height - 60

    # Função para atualizar a interface quando a janela for redimensionada
    def on_resized(e):
        global altura_dinamica
        altura_dinamica = page.height - 60  # Atualiza a altura dinâmica com a altura da janela
        atualizar_mensagens(page)  # Atualiza o conteúdo com a nova altura

    # Registrar a função on_resized para o evento de redimensionamento
    page.on_resized = on_resized

    # Variável para armazenar a nova mensagem
    nova_mensagem = ""

    def handle_close(modal):
        page.close(modal)

    # Função para atualizar a variável nova_mensagem
    def update_nova_mensagem(e):
        nonlocal nova_mensagem
        nova_mensagem = e.control.value

    # Definindo modais
    modal_novo = ft.AlertDialog(
        title=ft.Text("Nova Mensagem"),
        content=ft.Column(
            [
                ft.Text("Digite a nova mensagem:"),
                ft.TextField(height=350, label="Mensagem", multiline=True, autofocus=True,
                             on_change=update_nova_mensagem),
            ], width=600
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: handle_close(modal_novo)),
            ft.TextButton("Adicionar",
                          on_click=lambda e: adicionar_mensagem(page, nova_mensagem, page.close(modal_novo))),
        ],
    )

    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()

    page.overlay.append(pick_files_dialog)

    modal_backup = ft.AlertDialog(
        title=ft.Text("BACKUP / RESTAURAR"),
        content=ft.Column(
            [
                ft.Row([

                ft.ElevatedButton(
                    "Importar arquivo",
                    icon=ft.Icons.DOWNLOAD,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=True
                    ),
                ),  

                ft.ElevatedButton(
                    "Exportar arquivo",
                    icon=ft.Icons.FILE_UPLOAD,
                    
                )
                
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND,)


            ], width=600
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: handle_close(modal_backup)),
            ft.TextButton("Adicionar",
                          on_click=lambda e: adicionar_mensagem(page, nova_mensagem, page.close(modal_backup))),
        ],
    )

    # Criando a topbar principal
    global topbar
    topbar = ft.Row(
        [
            ft.ElevatedButton(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.ADD),
                        ft.Text("Novo", size=16)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                on_click=lambda e: page.open(modal_novo),
                tooltip="Novo"
            ),

            # ft.Text("Mensagens Automáticas", size=20, weight="bold"),

            ft.ElevatedButton(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.BACKUP),
                        ft.Text("Backup / Restaurar", size=16)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                on_click=lambda e: page.open(modal_backup),
                tooltip="Faça o backup ou restaure mensagens."
            ),

            ft.ElevatedButton(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.DELETE),
                        ft.Text("Lixeira", size=16)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                on_click=lambda e: atualizar_lixeira(page),
                tooltip="Lixeira"
            )
        ],

        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Criando a topbar da lixeira
    global topbar_lixeira
    topbar_lixeira = ft.Row(
        [
            ft.IconButton(ft.Icons.REPLY, tooltip="Voltar", on_click=lambda e: voltar_para_principal(page)),
            # Voltar para a página principal
            ft.Text("Lixeira", size=20, weight="bold"),
            ft.ElevatedButton(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.DELETE_FOREVER),
                        ft.Text("Esvaziar Lixeira", size=16)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                on_click=lambda e: esvaziar_lixeira(page),
                tooltip="Esvaziar Lixeira"
            )  # Esvaziar lixeira
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Carregar e exibir as mensagens
    atualizar_mensagens(page)


# Inicializando o app
ft.app(target=main)
