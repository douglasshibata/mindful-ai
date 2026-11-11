# 📘 Tutorial de Operação e Implantação: MindfulAI Enterprise Clinical Wellness & Cognitive Companion

Guia passo a passo para configuração, inicialização, execução de testes e operação do **MindfulAI** (`mindful-ai`), plataforma enterprise de suporte à saúde mental com Triage Determinística de Crise (Life-Safety Guardrail), reestruturação cognitiva TCC e criptografia em repouso AES-256.

---

## 🛠️ 1. Visão Geral da Arquitetura

O sistema implementa uma camada de segurança clínica multicamadas:
- **Clinical Safety Triage Guardrail:** Intercepta termos de ideação suicida e automutilação com regex determinística de prioridade zero, retornando canais de emergência (188 CVV, 192 SAMU, 988 US Lifeline) sem delegar à LLM.
- **CBT Thought Challenger:** Saídas estruturadas estritas (Pydantic v2 `CognitiveReframing`) identificando distorções cognitivas (Catastrofização, Leitura Mental, Tudo-ou-Nada) com evidências racionais e passos somáticos.
- **Data Protection Tier:** Banco PostgreSQL 16 com criptografia AES-256 (Fernet) em notas sensíveis de diário, protegendo a privacidade clínica (LGPD / HIPAA).
- **Frontend Angular 19:** Banner/modal reativo de suporte emergencial com telefones de crise, formulários com escala clínica e exercícios de respiração 4-7-8.

---

## 📋 2. Pré-requisitos do Sistema

- **Docker Engine 24+ & Docker Compose v2**
- **Python 3.12+**
- **Node.js 20+**
- **Chave de API OpenAI** (opcional para testes locais, pois há motor heurístico offline de contingência)

---

## 🚀 3. Passo a Passo de Setup e Instalação

### Passo 1: Acessar a pasta do módulo
```bash
cd mindful-ai
```

### Passo 2: Configurar variáveis de ambiente
```bash
cp .env.example .env
```
Edite o arquivo `.env` para ajustar senhas e a chave da OpenAI se aplicável:
```ini
POSTGRES_PASSWORD=Secr3tMindful2026
OPENAI_API_KEY=sk-...
DATA_ENCRYPTION_KEY=dGVzdF9lbmNyeXB0aW9uX2tleV8zMl9ieXRlc19sb25nCg==
```

### Passo 3: Executar a stack completa via Docker Compose
```bash
docker compose -f deploy/docker-compose.yml up -d --build
```

Para inspecionar os serviços:
```bash
docker compose -f deploy/docker-compose.yml ps
```

---

## 💻 4. Execução Manual em Desenvolvimento

### Backend (FastAPI)
```bash
cd api
pip install -r requirements.txt
PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Endpoints disponíveis:
- Documentação OpenAPI (Swagger): `http://localhost:8000/docs`
- Healthcheck Clínico: `http://localhost:8000/health`
- TCC Cognitive Challenger: `POST http://localhost:8000/api/v1/challenge-thought`
- Diários de Humor e Ansiedade: `POST http://localhost:8000/api/v1/mood-logs`
- Métricas e Tendências: `GET http://localhost:8000/api/v1/trends`

### Frontend (Angular 19)
```bash
cd frontend
npm install
npm start
```
Acesse `http://localhost:4200` no navegador.

---

## 🧪 5. Testes e Validação de Segurança Clínica

Execute a suíte de testes do backend para certificar que o interceptador de crise e a criptografia estão 100% íntegros:

```bash
PYTHONPATH=mindful-ai/api pytest mindful-ai/api/tests/ -v
```

Os testes cobrem:
1. `test_crisis_guardrail.py`: Validação contra gatilhos em português e inglês de ideação suicida, corte de pulsos e overdose.
2. `test_cbt_service.py`: Validação da geração de esquemas estruturados de TCC e ativação de contingência.
3. `test_clinical_api.py`: Validação da criptografia AES-256 no banco e cálculo de tendências de ansiedade.
4. `test_main.py`: Testes de integração de endpoints retrocompatíveis e de saúde.

---

## 🔍 6. Resolução de Problemas (Troubleshooting)

1. **Gatilho de Crise não exibindo banner no Frontend:**
   - Verifique a resposta da API: ela deve retornar `status: "CRISIS_DETECTED"` com o objeto `helplines`.
2. **Erro de Criptografia nas Notas:**
   - Assegure-se de que `DATA_ENCRYPTION_KEY` contenha uma string válida (chave de 32 bytes).
3. **Conexão com PostgreSQL:**
   - Caso execute a API localmente fora do container, configure `DATABASE_URL` no `.env` para `sqlite+aiosqlite:///./mindful_ai.db`.
