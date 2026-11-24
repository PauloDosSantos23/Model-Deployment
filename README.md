# 🛒 SuperKart Sales Forecasting Service

Este repositório contém a solução completa de previsão de vendas para a rede de supermercados **SuperKart**, utilizando uma arquitetura desacoplada e conteinerizada (Backend em Flask e Frontend em Streamlit) implantada via **GitHub Codespaces**.

## 🏗️ Arquitetura do Projeto
O projeto é dividido em dois microsserviços que rodam em containers Docker independentes conectados por uma rede virtual:

*   **`backend_files/` (Flask API - Porta 7860):** Responsável por carregar o modelo treinado de Random Forest (`superkart_model_v1_0.joblib`), processar as entradas e expor as rotas de predição online e em lote (batch).
*   **`frontend_files/` (Streamlit - Porta 8501):** Interface gráfica amigável onde os gestores e analistas podem inserir dados de produtos manualmente ou carregar planilhas CSV para obter previsões em lote.

## 🚀 Endpoints da API (Backend)

### 1. Rota Principal / Helthcheck
*   **Mapeamento:** `GET /`
*   **Descrição:** Retorna o status atual da API.

### 2. Predição em Tempo Real
*   **Mapeamento:** `POST /v1/predict`
*   **Corpo da Requisição (JSON):**
    ```json
    {
      "Product_Weight": 12.66,
      "Product_Sugar_Content": "Low Sugar",
      "Product_Allocated_Area": 0.027,
      "Product_MRP": 117.08,
      "Store_Size": "Medium",
      "Store_Location_City_Type": "Tier 2",
      "Store_Type": "Supermarket Type2",
      "Product_Id_char": "FD",
      "Store_Age_Years": 16,
      "Product_Type_Category": "Non Perishables"
    }
    ```

### 3. Predição em Lote
*   **Mapeamento:** `POST /v1/productbatch`
*   **Entrada:** Arquivo `.csv` enviado via formulário multipart (`files={'file': ...}`).

## 🛠️ Como rodar o projeto no GitHub Codespaces

1. Abra este repositório em um **GitHub Codespace**.
2. Crie uma rede Docker compartilhada:
   ```bash
   docker network create superkart-net
   ```
3. Construa e execute o container do **Backend**:
   ```bash
   cd backend_files
   docker build -t superkart-backend .
   docker run -d --name backend --network superkart-net -p 7860:7860 superkart-backend
   ```
4. Construa e execute o container do **Frontend**:
   ```bash
   cd ../frontend_files
   docker build -t superkart-frontend .
   docker run -d --name frontend --network superkart-net -p 8501:8501 superkart-frontend
   ```
5. Acesse as portas na aba **Ports** do VS Code.
