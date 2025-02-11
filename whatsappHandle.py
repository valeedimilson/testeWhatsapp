import pyautogui
import pygetwindow as gw


def encontrar_campo_mensagem():
    # try:
    #     campo_mensagem = pyautogui.locateOnScreen('captura.png', confidence=0.8)
    #     if campo_mensagem is not None:
    #         return pyautogui.center(campo_mensagem)
    # except pyautogui.ImageNotFoundException:
    #     print("não encontrado no tema claro")

    try:
        campo_mensagem = pyautogui.locateOnScreen(
            'captura.png', confidence=0.8)
        if campo_mensagem is not None:
            posAntiga = pyautogui.center(campo_mensagem)
            pos = [posAntiga[0], posAntiga[1]]
            pos[0] = pos[0] + 50
            return pos
    except IOError:
        print("arquivo print não localizado")

    except pyautogui.ImageNotFoundException:
        print("não encontrado no tema escuro")

    # except pyautogui.OSError:
    #     print("imagem não localizada")

    print("Campo de mensagem não encontrado na tela!")
    return None

# Função para enviar a mensagem ao WhatsApp Web


def enviar_mensagem(mensagem):
    campo_mensagem_centro = encontrar_campo_mensagem()
    if campo_mensagem_centro is None:
        # sys.exit()
        return "CampoNaoEncontrado"

    pyautogui.click(campo_mensagem_centro)

    # Lista todas as janelas abertas
    window = gw.getActiveWindow()

    # Filtra e exibe o título das janelas que contêm o nome do navegador

    if "WhatsApp" not in window.title and "Chrome" not in window.title and "Firefox" not in window.title:
        return

    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('backspace')

    # Quebra a mensagem em linhas
    linhas = mensagem.split('\n')

    for i, linha in enumerate(linhas):
        # Escreve a linha
        pyautogui.write(linha, interval=0)

        # Se não for a última linha, envia a combinação Ctrl + Enter para nova linha
        if i < len(linhas) - 1:
            pyautogui.hotkey('ctrl', 'enter')
