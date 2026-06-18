# Calculadora de Cashback — Desafio Nology

Aplicação que calcula o cashback de uma compra com base nas regras de negócio de um programa de fintech, incluindo bônus para clientes VIP e promoção de cashback dobrado. Cada consulta é registrada por IP, e o histórico de consultas é exibido apenas para quem realizou aquelas consultas.

## Links em produção

- **App (frontend):** https://fintech-desafio-cashback.netlify.app
- **API (backend):** https://fintech-jyhf.onrender.com

> Observação: o backend está hospedado no plano gratuito do Render, que "dorme" após período de inatividade. A primeira requisição após um tempo sem uso pode demorar alguns segundos para responder enquanto o serviço é reativado.

## Regras de negócio

O cálculo do cashback segue três documentos internos, reconciliados na seguinte ordem:

1. **Cashback base**: 5% sobre o valor final da compra (após desconto).
2. **Bônus VIP**: clientes VIP recebem +10% sobre o cashback base já calculado (não sobre o valor da compra).
3. **Promoção**: compras com valor final acima de R$ 500,00 têm o cashback total dobrado, regra válida para todos os tipos de cliente.

A ordem de cálculo é: base → bônus VIP (se aplicável) → dobra da promoção (se aplicável).

```
valor_final = valor_compra * (1 - desconto)
cashback_base = 0.05 * valor_final
cashback_total = cashback_base
se cliente for VIP:
    cashback_total += 0.10 * cashback_base
se valor_final > 500:
    cashback_total *= 2
```

As respostas detalhadas dos cenários propostos no desafio (perguntas 2 a 4) estão no documento `respostas.docx`, na raiz deste repositório.

## Estrutura do repositório

```
fintech/
├── Cashback-api/          # Backend (Python + Flask + MySQL)
│   ├── app.py              # Rotas da API
│   ├── cashback_oop.py     # Classes Cliente, ClienteVIP, ClientePadrao
│   ├── db.py                # Conexão com o banco MySQL
│   ├── database.sql        # Script de criação da tabela
│   └── requirements.txt    # Dependências Python
├── frontend/                # Frontend estático (HTML, CSS, JS puro)
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── netlify.toml             # Configuração de deploy do frontend no Netlify
└── README.md
```

## Tecnologias utilizadas

- **Backend:** Python, Flask, Flask-CORS, MySQL Connector, Gunicorn
- **Banco de dados:** MySQL
- **Frontend:** HTML5, CSS3, JavaScript (vanilla)
- **Hospedagem:** Render (backend + banco) e Netlify (frontend)

## Como rodar o projeto localmente

### Pré-requisitos

- Python 3.10+ instalado
- MySQL instalado e rodando localmente (ou acesso a uma instância remota)
- Extensão Live Server (VS Code) ou similar, para servir o frontend

### Backend

1. Acesse a pasta do backend:
   ```bash
   cd Cashback-api
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Mac/Linux
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Crie o banco e a tabela:
   ```bash
   mysql -u root -p < database.sql
   ```

5. Defina a senha do MySQL como variável de ambiente (caso sua instalação local tenha senha):
   ```bash
   # Windows (cmd)
   set DB_PASSWORD=sua_senha

   # Windows (PowerShell)
   $env:DB_PASSWORD="sua_senha"

   # Mac/Linux
   export DB_PASSWORD=sua_senha
   ```

6. Rode a aplicação:
   ```bash
   python app.py
   ```

   O servidor estará disponível em `http://127.0.0.1:5000`.

### Frontend

1. Acesse a pasta do frontend:
   ```bash
   cd frontend
   ```

2. Caso o backend esteja rodando localmente, ajuste a constante `API_BASE_URL` no início do arquivo `app.js` para `http://127.0.0.1:5000`.

3. Abra o `index.html` com a extensão Live Server do VS Code (ou rode `python -m http.server 5500` dentro da pasta e acesse `http://127.0.0.1:5500`).

   > Não abra o arquivo `index.html` diretamente com duplo clique: o navegador bloqueia chamadas `fetch` em páginas abertas via `file://`.

## Endpoints da API

### `POST /cashback`

Calcula o cashback de uma compra e registra a consulta no histórico, associada ao IP de quem fez a chamada.

**Corpo da requisição:**
```json
{
  "tipo_cliente": "vip",
  "valor_compra": 600,
  "desconto": 0.15
}
```

- `tipo_cliente`: `"vip"` ou `"padrao"`
- `valor_compra`: valor numérico, em reais
- `desconto`: valor decimal entre 0 e 1 (ex.: 15% = 0.15)

**Resposta:**
```json
{
  "cashback": 56.10
}
```

### `GET /historico`

Retorna o histórico de consultas já realizadas pelo IP de quem está chamando a rota.

**Resposta:**
```json
[
  {
    "tipo_cliente": "vip",
    "valor_compra": 600,
    "cashback": 56.10,
    "criado_em": "2026-06-18 14:32:00"
  }
]
```

## Entregáveis do desafio

- [x] Código Python com a lógica de cálculo de cashback
- [x] Aplicação publicada (frontend + backend + banco de dados)
- [x] Código-fonte completo neste repositório
