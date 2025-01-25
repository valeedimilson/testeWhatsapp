# Mensagens Autom�ticas

Este projeto � uma aplica��o desktop desenvolvida em [Flet](https://flet.dev/) para gerenciar mensagens autom�ticas no WhatsApp Web. Ele oferece funcionalidades como adicionar, editar, excluir, e fixar mensagens, al�m de manter um sistema de lixeira.

---

## ?? Funcionalidades

- **Adicionar mensagens**: Crie mensagens autom�ticas para reutiliza��o.
- **Editar mensagens**: Atualize o conte�do das mensagens existentes.
- **Fixar mensagens**: Destaque mensagens importantes.
- **Lixeira**: Restaure ou exclua mensagens permanentemente.
- **Integra��o com WhatsApp Web**: Utilize automa��es para enviar mensagens diretamente no navegador.

---

## ?? Requisitos

Certifique-se de que voc� tenha o seguinte instalado:

- Python 3.9 ou superior
- [Google Chrome](https://www.google.com/intl/pt-BR/chrome/) (necess�rio para identificar campos no WhatsApp Web)

---

## ?? Configura��o

1. Clone este reposit�rio:

    ```bash
    git clone https://github.com/seu-usuario/mensagens-automaticas.git
    cd mensagens-automaticas
    ```

2. Instale as depend�ncias:

    ```bash
    pip install -r requirements.txt
    ```

3. Adicione as imagens de identifica��o na pasta `_internal/images/`:
    - `campo_mensagem_light.png`
    - `campo_mensagem_dark.png`

   Essas imagens devem corresponder � �rea de texto do WhatsApp Web no tema claro e escuro, respectivamente.

4. Execute o aplicativo:

    ```bash
    python app.py
    ```

---

## ??? Layout

O layout principal da aplica��o possui:

- **Barra superior**: Op��es de adicionar mensagens e acessar a lixeira.
- **Cards de mensagens**: Cada mensagem � exibida como um card com op��es para editar, excluir ou fixar.
- **Lixeira**: Interface separada para gerenciar mensagens removidas.

---

## ?? Como funciona

1. A aplica��o utiliza a biblioteca `pyautogui` para localizar e interagir com o campo de texto do WhatsApp Web.
2. As mensagens s�o armazenadas localmente em um banco de dados TinyDB (`db.json`).

---

## ??? Contribui��o

Se desejar contribuir:

1. Fa�a um fork do reposit�rio.
2. Crie um branch para sua feature ou corre��o de bug.
3. Envie um pull request.

---

## ?? Licen�a

Este projeto est� sob a licen�a [MIT](LICENSE).
