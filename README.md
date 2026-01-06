# Newspaper Agency — Projeto Django (Portfólio)

Um sistema simples de gerenciamento para uma Agência de Jornais feito com **Python + Django**, um projeto de portfólio com: models, CBVs, forms, templates e testes.

**Link do projeto (deploy):**
https://newspaper-agency-system-ob81.onrender.com/

**Acesso para testes:**
- **Usuário:** admin
- **Senha:** Adm12345

## Models

- **Redactor** — usuário customizado (extende `AbstractUser`) com `years_of_experience`
- **Topic** — tópico/assunto de jornais (`name`)
- **Newspaper** — jornal com `title`, `content`, `published_date` (auto), `topics` (M2M) e `publishers` (M2M com `Redactor`)

## Recursos principais

- CRUD completo para **Topic**, **Newspaper** e **Redactor** (Create / List / Detail / Update / Delete).
- **Redactor** usado como `AUTH_USER_MODEL` (usuário customizado com `years_of_experience`).
- `Newspaper.topics` como relacionamento **Many-to-Many** (um jornal pode ter vários tópicos).
- ListViews com **paginação** e **search** via formulários GET.
- Include reutilizável para paginação (`templates/includes/pagination.html`) e template tag `query_transform` para preservar a querystring.
- Formulários customizados (`ModelForm`) com widgets para melhorar a renderização (ex.: `CheckboxSelectMultiple` para M2M).
- Admin customizado:
  - Campo `years_of_experience` no `RedactorAdmin`
  - `filter_horizontal` para M2M em `NewspaperAdmin`
- Testes unitários focados apenas em **lógica customizada** (models, search, admin fieldset e view index).

## Decisões de design / notas técnicas

- Relacionamento **Many-to-Many** entre `Newspaper` e `Topic` para refletir que um jornal pode pertencer a múltiplos tópicos.
- O campo `published_date` é preenchido automaticamente (`auto_now_add=True`).
- Para evitar problemas de N+1 quando aplicável, as views utilizam `select_related` e `prefetch_related` conforme o tipo de relacionamento (FK vs M2M).
- Autenticação via `django.contrib.auth` (login/logout padrão) e proteção de views com `LoginRequiredMixin` onde necessário.

## Instalação (desenvolvimento) — passo a passo

Clone o repositório:

```bash
git clone https://github.com/TimoteoRJanzen/newspaper-agency-system
cd newspaper-agency-system
```

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```
Configurar variáveis de ambiente:

```bash
# Windows
copy .env.sample .env
# macOS / Linux
cp .env.sample .env

```
Abra o arquivo `.env` e configure os valores:

```.env
# Se for usar Postgres (para produção)
POSTGRES_DB=seu_nome_do_banco
POSTGRES_DB_PORT=5432
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_HOST=localhost

# Django
DJANGO_SECRET_KEY=sua_secret_key
DJANGO_SETTINGS_MODULE=newspaper_agency.settings.prod # ou .dev para testar localmente
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie e aplique as migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Crie um superuser (para acessar o admin):

```bash
python manage.py createsuperuser
```

## Rodando o projeto

Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

Abra no navegador:

- Aplicação: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Login (padrão Django): http://127.0.0.1:8000/accounts/login/

## Administração

- Acesse `/admin/` com o superuser criado.
- `RedactorAdmin` inclui o campo `years_of_experience` no formulário de edição.
- `NewspaperAdmin` utiliza `filter_horizontal = ("topics", "publishers")` para facilitar o gerenciamento das relações M2M.

## Testes

Execute toda a suíte de testes:

```bash
python manage.py test
```

### Testes incluídos (resumo)

- **Models**
  - `test_redactor_str`
  - `test_create_redactor_with_years_of_experience`
  - `test_topic_str`
  - `test_newspaper_str`
- **View**
  - `test_index_view` (contadores do dashboard)
- **Admin**
  - `test_redactor_years_of_experience_listed_in_admin_detail`
- **Search (forms / list views)**
  - `test_search_topic_by_name`
  - `test_search_newspaper_by_title`
  - `test_search_redactor_by_username`

> Os testes foram planejados para cobrir apenas comportamentos **customizados**, evitando duplicar garantias já fornecidas pelo Django.

## Estilização — organização de templates e static

Estrutura utilizada no projeto:

- `templates/includes/navbar.html` — include do cabeçalho / navbar reutilizável.
- `static/css/styles.css` — arquivo CSS principal (navbar, layout e ajustes visuais).
- `templates/newspaper/` — templates do app (index, lists, details, forms, etc.).
- `templates/registration/` — templates de autenticação do Django (`login.html`, `logged_out.html`).

Notas importantes:

- O arquivo `templates/base.html` inclui `includes/navbar.html` e carrega `static/css/styles.css` usando `{% load static %}`.
- A paginação reutilizável fica em `templates/includes/pagination.html` e depende da template tag `query_transform` (definida em `newspaper/templatetags/`).

## Estrutura de pastas (resumida)

```
newspaper-agency-system/
├── newspaper/                # app principal
│   ├── migrations/
│   ├── templatetags/
│   └── tests/
├── templates/
│   ├── includes/
│   │   ├── navbar.html
│   │   └── pagination.html
│   ├── newspaper/
│   │   └── *.html
│   ├── registration/
│   │   ├── login.html
│   │   └── logged_out.html
│   └── base.html
├── static/
│   └── css/
│       └── styles.css
├── newspaper_agency/         # project settings
├── requirements.txt
└── README.md
```
