# 🚘 OCR-Phantera

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&style=for-the-badge)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-0052D4?logo=yolo&style=for-the-badge)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9-blue?logo=opencv&style=for-the-badge)
![PyTorch](https://img.shields.io/badge/PyTorch-2.3-blue?logo=pytorch&style=for-the-badge)
![EasyOCR](https://img.shields.io/badge/EasyOCR-JaidedAI-orange?style=for-the-badge)
![NumPy](https://img.shields.io/badge/NumPy-1.26-blue?logo=numpy&style=for-the-badge)

**OCR-Phantera** é uma solução de **Reconhecimento Automático de Placas de Veículos (ALPR)** usando IA para detectar e ler placas em tempo real com alta precisão.

---

## ✨ Funcionalidades

- ✅ **Detecção em Tempo Real** com YOLOv8
- ✅ **OCR com EasyOCR** (suporte a GPU via CUDA)
- ✅ **Pré-processamento avançado** para melhorar leitura em condições ruins (luz, reflexo, etc)
- ✅ **Registro em CSV**, com imagens do frame e da placa recortada
- ✅ **Cache inteligente** para evitar leituras duplicadas

---

## 🚀 Tecnologias Utilizadas

- **Linguagem:** Python 3.12+
- **Framework:** FastAPI
- **Banco de Dados:** PostgreSQL
- **ORM:** SQLAlchemy 2.0
- **Autenticação:** JWT (com `python-jose`)
- **Hash de Senhas:** Passlib
- **Configuração via `.env`:** python-dotenv

---

## 📦 Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/OCR-Phantera.git
cd OCR-Phantera
````

### 2. Criar e ativar ambiente virtual

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

> 💡 **Para usar GPU**, edite `requirements.txt` e descomente a linha com PyTorch CUDA antes de instalar.

---

## ▶️ Execução

Certifique-se de que seu modelo treinado (`best.pt`) está em:

```
runs/detect/train/weights/best.pt
```

Execute:

```bash
python OCR.py
```

> Pressione `q` na janela de visualização para encerrar.

---

## 🏋️‍♂️ Treinamento

O treinamento foi feito com anotações manuais utilizando a ferramenta:

🔗 [VoTT - Visual Object Tagging Tool](https://github.com/microsoft/VoTT/releases)

As anotações foram convertidas para o formato YOLO com o script:

```bash
python convert_voc_to_yolo.py
```

---

## 📂 Estrutura do Projeto

```
OCR-Phantera/
│
├── docs/                   # Documentação
├── placas-OCR/             # Dataset bruto
├── dataset/                # Dataset pronto para YOLO
│   ├── images/
│   └── labels/
├── runs/                   # Pesos do modelo treinado
│   └── detect/train/
├── .venv/                  # Ambiente virtual
├── OCR.py                  # Script principal
├── treinamento.py          # Treinamento YOLOv8
├── TestedoReconhecimento.py# Teste rápido de OCR
├── convert_voc_to_yolo.py  # Conversor VOC -> YOLO
├── modificarnome.py        # Preparação de imagens
├── data.yaml               # Configuração YOLO
└── requirements.txt        # Dependências
```

---

## 👨‍💻 Autor

Projeto desenvolvido por **Roberth Arnaldo Loogam Souza da Silva**


## 🤝 Contribuições

Contribuições são bem-vindas!

* Sugestões? Abra uma *issue*
* Melhorias? Envie um *pull request*




