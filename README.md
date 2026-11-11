# 🧠 MindfulAI: Enterprise Clinical Wellness & Cognitive Companion

O **MindfulAI** é uma plataforma digital de suporte à saúde mental baseada em evidências, integrando técnicas validadas de **Terapia Cognitivo-Comportamental (TCC / CBT)**, exercícios somáticos de autorregulação e orquestração de IA com barreira ativa de segurança clínica (**Deterministic Crisis Safety Guardrails**).

---

## 🏛️ 1. Topologia da Arquitetura e Protocolo de Segurança

```
                               +-----------------------------+
                               |     Client Web Application  |
                               |    (Angular 19 + Signals)   |
                               +--------------+--------------+
                                              |
                                              | HTTPS / WSS Seguro
                                              v
+-------------------------------------------------------------------------------------------------+
|                                GATEWAY & API LAYER (FastAPI 0.115)                              |
|                                                                                                 |
|   - Autenticação JWT / OIDC               - Rate Limiter por Usuário (SlowAPI)                  |
|   - PII Sanitizer (Mascaramento de Nomes) - CORS & Strict Security Headers                      |
+---------------------------------------------┬---------------------------------------------------+
                                              │
                                              ▼
+-------------------------------------------------------------------------------------------------+
|                                 CLINICAL SAFETY TRIAGE ENGINE                                   |
|                                                                                                 |
|   ┌─────────────────────────────────────────────────────────────────────────────────────────┐   |
|   │ 🚨 Deterministic Crisis Filter (Regex + Keyword Graph)                                  │   |
|   │    Varre ideação suicida, automutilação e abuso de substâncias com emergência           │   |
|   └───────────────────────────┬───────────────────────────────────┬─────────────────────────┘   |
|                               │ (Crise Detectada)                 │ (Entrada Segura)            |
|                               ▼                                   ▼                             |
|               +-------------------------------+   +-------------------------------+             |
|               | Crisis Protocol Dispatcher    |   | CBT Thought Challenger Engine |             |
|               | - Intercepta LLM              |   | - Classificação de Distorções |             |
|               | - Retorna Canais: 188 / 988   |   | - Reestruturação Cognitiva    |             |
|               +-------------------------------+   | - OpenAI Structured Outputs   |             |
|                                                   +---------------+---------------+             |
+-------------------------------------------------------------------┼-----------------------------+
                                                                    │
                                                                    v
+-------------------------------------------------------------------------------------------------+
|                                   DATA TIER & COMPLIANCE ENGINE                                 |
|                                                                                                 |
|   +-----------------------------------------------+ +---------------------------------------+   |
|   |         PostgreSQL 16 (Armazenamento Seguro)  | |        Redis 7 (Sessões & Throttling) |   |
|   |   - Diários com Encriptação AES-256           | |   - Pacing do Exercício de Respiração |   |
|   |   - Log Imutável de Eventos Clínicos          | |   - Rate-Limit de Chamadas de IA      |   |
|   +-----------------------------------------------+ +---------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

---

## 📁 2. Estrutura Canônica de Diretórios

```
mindful-ai/
├── api/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                     # Entrypoint e inicialização de middlewares
│   │   ├── core/
│   │   │   ├── config.py               # Pydantic Settings com validação de chaves
│   │   │   ├── security.py             # Encriptação de dados de diário (AES-256) e hash
│   │   │   └── crisis_guardrail.py     # Interceptador determinístico de crise (prioridade zero)
│   │   ├── db/
│   │   │   ├── session.py              # Engine assíncrona/síncrona SQLAlchemy 2.0
│   │   │   └── models.py               # Modelos relacionais (User, MoodLog, ThoughtRecord)
│   │   ├── services/
│   │   │   ├── cbt_service.py          # Integração OpenAI com Structured Outputs & fallback
│   │   │   └── analytics_service.py    # Agregações de humor e variabilidade
│   │   ├── schemas/
│   │   │   ├── clinical_schemas.py     # Schemas Pydantic v2 (Distorções cognitivas e TCC)
│   │   │   └── mood_schemas.py         # Schemas de log de ansiedade e sono
│   │   └── api/
│   │       └── v1/
│   │           ├── router.py           # Agregador de rotas v1
│   │           ├── endpoints_cbt.py    # /thought-records, /challenge-thought
│   │           └── endpoints_mood.py   # /mood-logs, /trends
│   ├── tests/
│   │   ├── test_crisis_guardrail.py    # Teste de 100% de cobertura no interceptor de crise
│   │   ├── test_cbt_service.py         # Testes de estruturação TCC
│   │   └── test_clinical_api.py        # Testes de criptografia e persistência
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── core/                   # CrisisNotificationService
│   │   │   ├── components/             # Breathing Somatic Pacer
│   │   │   ├── features/               # Modular features (mood-tracker, thought-challenger)
│   │   │   └── shared/                 # Componentes táteis com contraste acessível
│   ├── package.json
│   └── angular.json
├── deploy/
│   └── docker-compose.yml              # PostgreSQL, Redis, API e Frontend integrados
├── .env.example
└── README.md
```

---

## 🚨 3. Protocolo Clínico de Intercepção de Crise (`crisis_guardrail.py`)

A IA nunca deve ser deixada sozinha diante de termos que indiquem risco de vida. A verificação determinística roda antes de qualquer chamada externa:

```python
CRISIS_PATTERNS = [
    re.compile(r"(?i)\b(me\s+matar|suic[ií]dio|tirar\s+minha\s+vida|acabar\s+com\s+tudo)\b"),
    re.compile(r"(?i)\b(n[aã]o\s+quero\s+mais\s+viver|cortar\s+meus\s+pulsos|overdose)\b"),
    re.compile(r"(?i)\b(i\s+want\s+to\s+die|kill\s+myself|end\s+my\s+life|suicide)\b"),
]
```

Canais de Apoio Emergencial Injetados:
- **CVV (Centro de Valorização da Vida):** Disque `188` (Brasil - 24/7)
- **SAMU (Emergência Médica):** Disque `192` (Brasil - 24/7)
- **Suicide & Crisis Lifeline:** Disque `988` (EUA - 24/7)

---

## 🧠 4. Motor de Reestruturação Cognitiva (CBT) com Schema Rígido

A estruturação via Pydantic v2 garante que a resposta respeite a taxonomia formal de distorções cognitivas de Beck (Catastrofização, Leitura Mental, Tudo-ou-Nada, Filtro Negativo), trazendo evidências empíricas e um passo imediato de autorregulação somática.

---

## 🔐 5. Proteção de Dados Pessoais Sensíveis (LGPD / HIPAA)

- **Criptografia em Repouso (AES-256 Fernet):** O campo `notes_encrypted` em `mood_logs` é cifrado com chave de 32 bytes antes do commit no banco de dados.
- **Isolamento de Usuário:** Relações vinculadas por `user_id` e índices de auditoria cronológica (`idx_user_recorded_at`).

---

## 🚀 6. Guia de Instalação e Execução

### Pré-requisitos
- Docker Engine 24+ & Docker Compose v2 (ou Python 3.12+ e Node.js 20+)
- Chave de API da OpenAI (opcional para testes com fallback heurístico integrado)

### Execução com Docker Compose
```bash
# 1. Configurar variáveis de ambiente seguras
cp .env.example .env

# 2. Subir a stack completa (Postgres 16, Redis 7, FastAPI e Frontend Angular)
docker compose -f deploy/docker-compose.yml up -d --build

# 3. Validar a integridade dos serviços
docker compose -f deploy/docker-compose.yml ps
```

### Execução Local (Backend)
```bash
cd api
pip install -r requirements.txt
PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Execução Local (Frontend)
```bash
cd frontend
npm install
npm start
```

### Testes Automatizados
```bash
PYTHONPATH=mindful-ai/api pytest mindful-ai/api/tests/ -v
```

---

## 📊 Matriz Comparativa: Versão Anterior vs. Versão Corporativa Refatorada

| Dimensão | Versão Original | Versão Corporativa Refatorada |
|---|---|---|
| **Segurança Clínica** | Inexistente (LLM pura lidando com pensamentos negativos) | Crisis Guardrail determinístico com interceptação e canais de emergência (188, 192, 988) |
| **Garantia de Resposta TCC** | Respostas abertas e desestruturadas da OpenAI | Schema rígido Pydantic (identifica distorção formal e reestruturação) |
| **Persistência de Dados** | SQLite local desprotegido | PostgreSQL 16 com encriptação AES-256 de notas sensíveis e relacionamentos auditados |
| **Escalabilidade & Cache** | Inexistente | Redis 7 para rate limiting e controle de sessões do usuário |
| **Frontend** | Angular servido via dev server na porta 4200 | Build de produção em container com servidor HTTP hardened (Nginx) e alerta de crise ativo |

---
*Aviso Clínico: O MindfulAI é uma ferramenta de suporte ao bem-estar baseada em evidências e não substitui avaliação, diagnóstico ou tratamento médico/psicológico especializado.*
