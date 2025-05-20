# 📦 CAN DBC e Kvaser Database Editor

## Índice

- [📘 O que é um ficheiro DBC?](#-o-que-é-um-ficheiro-dbc)
- [✅ Vantagens de utilizar DBC](#-vantagens-de-utilizar-dbc)
- [🛠️ Como usar o Kvaser Database Editor](#-como-usar-o-kvaser-database-editor)
- [⚙️ Compilação Automática para Código C](#-compilação-automática-para-código-c)
- [📟 Exemplo de uso no Teensy 4.1 (C/C++)](#-exemplo-de-uso-no-teensy-41-cc)

---

## 📘 O que é um ficheiro DBC?

Um ficheiro **DBC** (DataBase CAN) é um formato padronizado utilizado para descrever a estrutura das mensagens num barramento **CAN (Controller Area Network)**. Em vez de interpretar manualmente os bytes recebidos, o ficheiro DBC traduz essas mensagens em **sinais legíveis**, como velocidade, temperatura, estado de sensores, entre outros.

### ✅ Vantagens de utilizar DBC:

- **Facilidade de interpretação:** Converte mensagens cruas (em hexadecimal) em valores com nomes e unidades compreensíveis.
- **Consistência:** Permite que múltiplos sistemas interpretem dados CAN da mesma forma.
- **Automatização:** Softwares como o Kvaser Database Editor, Vector CANalyzer, e Python-CAN podem utilizar o DBC para decodificar mensagens automaticamente.
- **Escalabilidade:** Simplifica o trabalho em redes CAN com muitas mensagens e sinais.

---

## 🛠️ Como usar o **Kvaser Database Editor**

O [**Kvaser Database Editor**]([https://www.kvaser.com/database-editor/](https://kvaser.com/single-download/?download_id=47183)) é uma ferramenta gratuita da Kvaser para criar e editar ficheiros DBC.

### 📥 Instalação

1. Visita o site oficial: [https://www.kvaser.com/database-editor/]([https://www.kvaser.com/database-editor/](https://kvaser.com/single-download/?download_id=47183))
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

## ⚙️ Compilação Automática para Código C

Este repositório inclui um workflow do GitHub Actions que gera automaticamente código C a partir dos ficheiros DBC encontrados, usando o `cantools` com o comando `generate_c_source`.

- Sempre que um ficheiro DBC for alterado e enviado para o repositório, o código C correspondente é regenerado automaticamente.
- Os ficheiros gerados são colocados na pasta `generated/`.
- Este código C pode ser usado diretamente em projetos de firmware, permitindo integrar as definições CAN de forma segura e eficiente.

Exemplo de comando para compilação:
   python3 -m cantools generate_c_source Autonomous.dbc --output autonomous_c_output


## Exportação para EXCEL
o workflow do GitHub Actions exporta também para xls, com uma página por ficheiro dbc, e uma tabela por id como se pode ver na figura abaixo
![image](https://github.com/user-attachments/assets/90f69d98-68a3-44f2-98c8-4df361548ea3)


---

## 📟 Exemplo de uso no Teensy 4.1 (C/C++)

Aqui está um exemplo básico para Teensy 4.1 usando a biblioteca [FlexCAN_T4](https://github.com/collin80/FlexCAN_T4) para receber, decodificar e enviar mensagens CAN com o código C gerado a partir do DBC:

```c
#include <Arduino.h>
#include <FlexCAN_T4.h>  // Biblioteca CAN para Teensy 4.x

// Inclui o ficheiro gerado automaticamente pelo cantools
#include "generated/autonomous_dv_driving_dynamics_1.h"

FlexCAN_T4<CAN1, RX_SIZE_256, TX_SIZE_16> CAN;

void setup() {
  Serial.begin(115200);
  CAN.begin();
  CAN.setBaudRate(500000);

  // Ativa filtro para aceitar todas as mensagens (exemplo)
  CAN.setMBFilterAll();

  Serial.println("CAN Teensy 4.1 exemplo iniciado");
}

void loop() {
  CAN_message_t rx_msg;

  // Verifica se chegou alguma mensagem CAN
  if (CAN.read(rx_msg)) {
    Serial.print("Mensagem CAN recebida com ID: 0x");
    Serial.println(rx_msg.id, HEX);

    // Suponhamos que esta mensagem corresponde ao tipo autonomous_dv_driving_dynamics_1
    struct autonomous_dv_driving_dynamics_1_t decoded_data;

    // Decodifica os dados recebidos
    int ret = autonomous_dv_driving_dynamics_1_unpack(&decoded_data, rx_msg.buf, rx_msg.len);
    if (ret == 0) {
      Serial.print("Speed actual: ");
      Serial.println(decoded_data.speed_actual);
      Serial.print("Speed target: ");
      Serial.println(decoded_data.speed_target);
      Serial.print("Steering angle actual: ");
      Serial.println(decoded_data.steering_angle_actual);
      // Outros sinais podem ser lidos da mesma forma
    } else {
      Serial.println("Erro ao decodificar mensagem");
    }

    // Exemplo: prepara uma mensagem para enviar (alterando speed_target)
    struct autonomous_dv_driving_dynamics_1_t tx_data = decoded_data;
    tx_data.speed_target = 150;  // Alterar valor para envio

    uint8_t tx_buf[8];
    autonomous_dv_driving_dynamics_1_pack(tx_buf, &tx_data, sizeof(tx_buf));

    // Prepara mensagem CAN para envio
    CAN_message_t tx_msg;
    tx_msg.id = rx_msg.id;  // Usar mesmo ID ou outro conforme protocolo
    tx_msg.len = 8;
    memcpy(tx_msg.buf, tx_buf, 8);

    // Envia a mensagem CAN
    CAN.write(tx_msg);
    Serial.println("Mensagem CAN enviada com speed_target modificado.");
  }
}
