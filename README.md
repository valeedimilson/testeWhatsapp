# Mensagens Automáticas

Este projeto é uma aplicação desktop desenvolvida em [Flet](https://flet.dev/) para gerenciar mensagens automáticas no WhatsApp Web. Ele oferece funcionalidades como adicionar, editar, excluir, e fixar mensagens, além de manter um sistema de lixeira.

---

## ?? Funcionalidades

- **Adicionar mensagens**: Crie mensagens automáticas para reutilização.
- **Editar mensagens**: Atualize o conteúdo das mensagens existentes.
- **Fixar mensagens**: Destaque mensagens importantes.
- **Lixeira**: Restaure ou exclua mensagens permanentemente.
- **Integração com WhatsApp Web**: Utilize automações para enviar mensagens diretamente no navegador.

---

## ?? Requisitos

Certifique-se de que você tenha o seguinte instalado:

- Python 3.9 ou superior
- [Google Chrome](https://www.google.com/intl/pt-BR/chrome/) (necessário para identificar campos no WhatsApp Web)

---

## ?? Configuração

1. Clone este repositório:

    ```bash
    git clone https://github.com/seu-usuario/mensagens-automaticas.git
    cd mensagens-automaticas
    ```

2. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

3. Adicione as imagens de identificação na pasta `_internal/images/`:
    - `campo_mensagem_light.png`
    - `campo_mensagem_dark.png`

   Essas imagens devem corresponder à área de texto do WhatsApp Web no tema claro e escuro, respectivamente.

4. Execute o aplicativo:

    ```bash
    python app.py
    ```

---

## ??? Layout

O layout principal da aplicação possui:

- **Barra superior**: Opções de adicionar mensagens e acessar a lixeira.
- **Cards de mensagens**: Cada mensagem é exibida como um card com opções para editar, excluir ou fixar.
- **Lixeira**: Interface separada para gerenciar mensagens removidas.

---

## ?? Como funciona

1. A aplicação utiliza a biblioteca `pyautogui` para localizar e interagir com o campo de texto do WhatsApp Web.
2. As mensagens são armazenadas localmente em um banco de dados TinyDB (`db.json`).

---

## ??? Contribuição

Se desejar contribuir:

1. Faça um fork do repositório.
2. Crie um branch para sua feature ou correção de bug.
3. Envie um pull request.

---

## ?? Licença

Este projeto está sob a licença [MIT](LICENSE).
