# SearchMyWeb Backend

Django-based backend API for the SearchMyWeb application, providing web crawling, indexing, search, and analytics capabilities.

## 🏗️ Architecture

### Technology Stack
- **Framework**: Django 5.2.6
- **API**: Django REST Framework 3.16.1
- **Database**: PostgreSQL (dev) / SQLite (prod)
- **Search Engine**: OpenSearch 3.0.0
- **Authentication**: Token-based + Session
- **Task Scheduling**: APScheduler 3.11.0
- **Environment Management**: python-decouple 3.8

### Project Structure
```
backend/
├── MySearchEngine/           # Django project settings
│   ├── settings.py          # Main configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
├── UserManagementApp/        # Main Django application
│   ├── models.py            # Database models
│   ├── views.py             # API views and endpoints
│   ├── utils.py             # Utility functions
│   ├── urls.py              # App URL routing
│   ├── management/          # Django management commands
│   │   └── commands/
│   │       ├── crawl_and_index.py
│   │       ├── clear_all_data.py
│   │       ├── start_crawler.py
│   │       └── start_indexing.py
│   └── static/              # Static files
├── server_status/           # Health check endpoints
├── scripts/                 # Management scripts
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in git)
├── .env.example            # Environment template
└── ENVIRONMENT_SETUP.md    # Environment setup guide
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+ (for development)
- OpenSearch 2.0+ (or Elasticsearch 8.0+)
- Virtual environment

### Installation

1. **Clone and Navigate**
   ```bash
   git clone <repository-url>
   cd SearchMyWeb/backend
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv ../venv
   source ../venv/bin/activate  # On Windows: ..\venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

## ⚙️ Configuration

### Environment Variables

All sensitive configuration is managed through environment variables. See `ENVIRONMENT_SETUP.md` for detailed instructions.

#### Required Variables
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432
```

#### Optional Variables (with defaults)
```env
OPENSEARCH_HOST=localhost
OPENSEARCH_PORT=9200
OPENSEARCH_SCHEME=http
OPENSEARCH_VERIFY_CERTS=True
STATUS_TOKEN=your-status-token
```

### Database Configuration

**Development (PostgreSQL)**:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mywebsearch_db',
        'USER': 'search_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**Production (SQLite)**:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

### OpenSearch Configuration

```python
ELASTIC_SEARCH_OBJ = OpenSearch([
    {
        'host': OPENSEARCH_HOST,
        'port': OPENSEARCH_PORT,
        'scheme': OPENSEARCH_SCHEME
    }
], verify_certs=OPENSEARCH_VERIFY_CERTS)
```

## 📊 API Endpoints

### Authentication
| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/api/login/` | User login | None |
| POST | `/api/register/` | User registration | None |
| POST | `/api/logout/` | User logout | Token/Session |

### Search
| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/api/search/` | Perform search | Token/Session |
| GET | `/api/search-results/` | Get search results | Token/Session |

### Website Management
| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/website-links/` | List website links | Token/Session |
| POST | `/api/website-links/` | Create website link | Token/Session |
| PUT | `/api/website-links/{id}/` | Update website link | Token/Session |
| DELETE | `/api/website-links/{id}/` | Delete website link | Token/Session |

### Analytics
| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/analytics/` | Get analytics data | Token/Session |
| GET | `/api/traffic-sources/` | Get traffic sources | Token/Session |
| GET | `/api/statewise-traffic/` | Get state-wise traffic | Token/Session |
| GET | `/api/wordcloud/` | Get word cloud data | Token/Session |

### System
| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/status/` | Health check | Token |
| GET | `/api/live-logger/` | Live logging data | Token/Session |

## 🗄️ Database Models

### Core Models

#### User
```python
class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    role = models.CharField(max_length=256, choices=USER_CHOICES)
```

#### WebsiteLink
```python
class WebsiteLink(models.Model):
    link = models.CharField(max_length=600, db_index=True)
    click_count = models.IntegerField(default=0)
    search_user = models.ForeignKey(User, on_delete=models.CASCADE)
    index_level = models.IntegerField(help_text='Indexing depth (-1 for full site)')
    hyper_text = models.CharField(max_length=5, choices=HTTP_CHOICES)
    last_indexed = models.DateTimeField(default=timezone.now)
    is_indexed = models.BooleanField(default=False)
    is_crawl = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now, db_index=True)
```

#### AuthToken
```python
class AuthToken(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_used_at = models.DateTimeField(default=timezone.now)
```

### Analytics Models

- **SearchQueryLog**: Search query logging
- **WebsiteLinkClick**: Click tracking
- **DailyAnalyticsReports**: Daily analytics data
- **DailyWorldCluodAnalytics**: Word cloud analytics
- **StateWiseTrafficAnalytic**: Geographic traffic data

## 🔧 Management Commands

### Crawling and Indexing

#### crawl_and_index
Combined crawling and indexing command with configurable workers.

```bash
# Basic usage
python manage.py crawl_and_index

# With custom worker counts
python manage.py crawl_and_index --crawl-workers 4 --index-workers 2

# Crawl only
python manage.py crawl_and_index --crawl-only --crawl-workers 4

# Index only
python manage.py crawl_and_index --index-only --index-workers 2

# Continuous mode
python manage.py crawl_and_index --continuous

# Limit items
python manage.py crawl_and_index --max-crawl-items 100 --max-index-items 50
```

#### start_crawler
Start website crawling process.

```bash
python manage.py start_crawler
```

#### start_indexing
Start website indexing process.

```bash
python manage.py start_indexing
```

### Data Management

#### clear_all_data
Comprehensive data cleanup command.

```bash
# Clear all data (requires confirmation)
python manage.py clear_all_data --confirm

# Clear only OpenSearch indexes
python manage.py clear_all_data --opensearch-only --confirm

# Clear only database data
python manage.py clear_all_data --database-only --confirm

# Keep users and analytics
python manage.py clear_all_data --keep-users --keep-analytics --confirm
```

## 🔍 Core Functionality

### Web Crawling
- **Multi-threaded crawling** with configurable worker pools
- **Depth-based indexing** (configurable levels)
- **Content extraction** (HTML, PDF, DOCX, etc.)
- **Link discovery** and queue management
- **Rate limiting** and respectful crawling

### Search Indexing
- **OpenSearch integration** for fast search
- **Content processing** and text extraction
- **Metadata indexing** (title, description, keywords)
- **Geographic data** extraction and indexing
- **Duplicate detection** and deduplication

### Search Engine
- **Full-text search** across indexed content
- **Relevance scoring** and ranking
- **Query logging** and analytics
- **Click tracking** and user behavior
- **Search suggestions** and autocomplete

### Analytics
- **Search analytics** (queries, clicks, results)
- **Traffic analysis** (sources, geographic)
- **User behavior** tracking
- **Performance metrics** and monitoring
- **Word cloud** generation

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test UserManagementApp

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Test Configuration
Tests use a separate database configuration in `server_status/tests/settings.py`.

## 📝 Logging

### Log Configuration
- **Application logs**: `log/app.log`
- **Error logs**: `log/error.log`
- **Log rotation**: 20MB files, 10 backups
- **Log levels**: INFO, ERROR

### Log Usage
```python
from UserManagementApp.utils import logger, logger_extra

logger.info("Information message", extra=logger_extra)
logger.error("Error message", extra=logger_extra)
```

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG=False` in environment
2. Configure production database
3. Set up SSL certificates
4. Configure OpenSearch cluster
5. Set up logging and monitoring
6. Configure reverse proxy
7. Set up backup procedures

### Environment Variables for Production
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
DB_PASSWORD=your-production-password
OPENSEARCH_HOST=your-opensearch-cluster
STATUS_TOKEN=your-production-token
```

### Health Checks
- **Database**: PostgreSQL/SQLite connectivity
- **OpenSearch**: Search engine connectivity
- **Certificate**: SSL certificate validation
- **Status endpoint**: `/api/status/`

## 🔒 Security

### Authentication
- **Token-based authentication** for API access
- **Session authentication** for web interface
- **Token expiration** (30 minutes)
- **CSRF protection** for forms

### Security Headers
- **CORS configuration** for cross-origin requests
- **Content Security Policy** headers
- **XSS protection** enabled
- **SQL injection** prevention

### Data Protection
- **Environment variables** for sensitive data
- **Database encryption** at rest
- **Secure password** hashing
- **Input validation** and sanitization

## 📊 Monitoring

### Health Monitoring
- **System health** checks
- **Database connectivity** monitoring
- **OpenSearch status** monitoring
- **Application performance** metrics

### Logging and Debugging
- **Structured logging** with context
- **Error tracking** and reporting
- **Performance profiling**
- **Debug information** in development

## 🛠️ Development

### Code Style
- **PEP 8** compliance
- **Type hints** where applicable
- **Docstrings** for functions and classes
- **Comments** for complex logic

### Git Workflow
1. Create feature branch
2. Make changes with tests
3. Run tests and linting
4. Submit pull request
5. Code review and merge

### Debugging
```bash
# Enable debug mode
DEBUG=True

# Run with debug toolbar
pip install django-debug-toolbar

# Use Django shell
python manage.py shell

# Database queries debugging
python manage.py shell_plus --print-sql
```

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [OpenSearch Documentation](https://opensearch.org/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**SearchMyWeb Backend** - Powerful web crawling and search infrastructure.
