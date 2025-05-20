
# 📦 CAN DBC e Kvaser Database Editor

## 📘 O que é um ficheiro DBC?

Um ficheiro **DBC** (DataBase CAN) é um formato padronizado utilizado para descrever a estrutura das mensagens num barramento **CAN (Controller Area Network)**. Em vez de interpretar manualmente os bytes recebidos, o ficheiro DBC traduz essas mensagens em **sinais legíveis**, como velocidade, temperatura, estado de sensores, entre outros.

### ✅ Vantagens de utilizar DBC:

- **Facilidade de interpretação:** Converte mensagens cruas (em hexadecimal) em valores com nomes e unidades compreensíveis.
- **Consistência:** Permite que múltiplos sistemas interpretem dados CAN da mesma forma.
- **Automatização:** Softwares como o Kvaser Database Editor, Vector CANalyzer, e Python-CAN podem utilizar o DBC para decodificar mensagens automaticamente.
- **Escalabilidade:** Simplifica o trabalho em redes CAN com muitas mensagens e sinais.

---

## 🛠️ Como usar o **Kvaser Database Editor**

O [**Kvaser Database Editor**](https://www.kvaser.com/database-editor/) é uma ferramenta gratuita da Kvaser para criar e editar ficheiros DBC.

### 📥 Instalação

1. Visita o site oficial: [https://www.kvaser.com/database-editor/](https://www.kvaser.com/database-editor/)
2. Faz o download e instala o programa (Windows).

### 📄 Criar um novo DBC

1. **Abrir o Kvaser Database Editor**.
2. Selecionar `File > New` para criar uma nova base de dados.
3. Introduzir um nome para o **nó transmissor (node)**, por exemplo, `ECU_Principal`.

### ✍️ Adicionar Mensagens e Sinais

1. **Criar uma nova mensagem:**
   - Clicar com o botão direito em “Messages” > `Add message`.
   - Definir:
     - **Name:** Nome da mensagem (ex: `Velocidade_Viatura`)
     - **ID:** Identificador CAN (ex: `0x101`)
     - **DLC:** Comprimento em bytes (ex: `8`)
     - **Transmitter:** Seleciona o nó correspondente

2. **Adicionar sinais:**
   - Dentro da mensagem, clicar com o botão direito > `Add signal`.
   - Definir:
     - **Name:** Nome do sinal (ex: `velocidade`)
     - **Start bit:** Bit de início (ex: `0`)
     - **Length:** Comprimento em bits (ex: `16`)
     - **Byte order:** Intel (Little Endian) ou Motorola (Big Endian)
     - **Value type:** Signed/Unsigned
     - **Factor e Offset:** Conversão para valor real (ex: factor = 0.1 → 100 = 10.0 km/h)
     - **Unit:** Unidade (ex: `km/h`)

3. Guardar o ficheiro: `File > Save as` → escolhe um nome, por exemplo `can_database.dbc`.

---

## 🧪 Dica de Utilização com Python

Podes utilizar bibliotecas como [`cantools`](https://pypi.org/project/cantools/) para carregar e usar o DBC em scripts Python:

```python
import cantools

db = cantools.database.load_file('can_database.dbc')
msg = db.get_message_by_name('Velocidade_Viatura')

data = msg.encode({'velocidade': 50.0})  # Codificar sinal para bytes CAN
decoded = msg.decode(data)              # Decodificar bytes para dicionário
print(decoded)


