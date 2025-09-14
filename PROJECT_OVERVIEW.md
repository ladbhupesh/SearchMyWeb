# SearchMyWeb Project Overview

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        SearchMyWeb Platform                     │
├─────────────────────────────────────────────────────────────────┤
│  Frontend (Angular 13)           │  Backend (Django 5.2)        │
│  ┌─────────────────────────────┐ │  ┌─────────────────────────┐ │
│  │ • Test Search Interface     │ │  │ • REST API Endpoints    │ │
│  │ • Analytics Dashboard       │ │  │ • Authentication        │ │
│  │ • User Management           │ │  │ • Web Crawling Engine   │ │
│  │ • Traffic Analytics         │ │  │ • Search Indexing       │ │
│  │ • Word Cloud Visualization  │ │  │ • Data Analytics        │ │
│  │ • Live Logging              │ │  │ • Background Tasks      │ │
│  └─────────────────────────────┘ │  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                                Data Layer                        │
├──────────────────────────────────────────────────────────────────┤
│  PostgreSQL                        │  OpenSearch 2.0+            │
│  ┌─────────────────────────────┐   │  ┌──────────────────────┐   │
│  │ • User Management           │   │  │ • Search Index       │   │
│  │ • Website Links             │   │  │ • Full-text Search   │   │
│  │ • Search Query Logs         │   │  │ • Analytics Data     │   │
│  │ • Click Tracking            │   │  │ • Geographic Data    │   │
│  │ • Analytics Reports         │   │  │ • Performance Metrics│   │
│  └─────────────────────────────┘   │  └──────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

```
1. User Input
   ↓
2. Frontend (Angular)
   ↓ HTTP/HTTPS
3. Backend API (Django)
   ↓
4. Database (PostgreSQL)
   ↓
5. Search Engine (OpenSearch)
   ↓
6. Results Processing
   ↓
7. Frontend Display
```

## 🎯 Core Features

### Web Crawling & Indexing
- **Multi-threaded Crawling**: Concurrent processing with configurable workers
- **Depth-based Indexing**: Configurable crawling depth (-1 for full site)
- **Content Extraction**: HTML, PDF, DOCX, and other document types
- **Link Discovery**: Automatic link discovery and queue management
- **Rate Limiting**: Respectful crawling with configurable delays

### Search Engine
- **Full-text Search**: OpenSearch-powered search across indexed content
- **Relevance Scoring**: Advanced ranking algorithms
- **Query Logging**: Complete search query tracking
- **Click Tracking**: User interaction analytics
- **Search Suggestions**: Auto-complete functionality

### Analytics & Reporting
- **Search Analytics**: Query volume, performance, and trends
- **Traffic Analysis**: Source tracking and geographic distribution
- **User Behavior**: Click patterns and engagement metrics
- **Word Cloud**: Popular terms visualization
- **Real-time Monitoring**: Live logging and status updates

### User Management
- **Role-based Access**: Admin, user, and guest roles
- **Token Authentication**: Secure API access
- **Session Management**: Web interface authentication
- **User Analytics**: Individual user tracking and reporting

## 🛠️ Technology Stack

### Frontend
- **Angular 13.3.0**: Modern web framework
- **Bootstrap 5.1.3**: Responsive UI components
- **Angular Material 13.3.7**: Material Design components
- **FontAwesome 6.0.0**: Icon library
- **Chart.js 2.9.4**: Data visualization
- **AG Grid 27.2.1**: Advanced data grid
- **ngx-toastr 14.3.0**: Notification system

### Backend
- **Django 5.2.6**: Web framework
- **Django REST Framework 3.16.1**: API framework
- **PostgreSQL**: Primary database (development)
- **SQLite**: Production database
- **OpenSearch 3.0.0**: Search engine
- **APScheduler 3.11.0**: Task scheduling
- **python-decouple 3.8**: Environment management

### Infrastructure
- **Docker**: Containerization (optional)
- **Nginx**: Reverse proxy (production)
- **SSL/TLS**: Secure communication
- **Logging**: Structured logging with rotation
- **Monitoring**: Health checks and performance metrics

## 📊 Database Schema

### Core Tables
- **User**: User accounts and roles
- **AuthToken**: API authentication tokens
- **WebsiteLink**: Crawled website links
- **SearchQueryLog**: Search query history
- **WebsiteLinkClick**: Click tracking data

### Analytics Tables
- **DailyAnalyticsReports**: Daily analytics data
- **DailyWorldCluodAnalytics**: Word cloud analytics
- **StateWiseTrafficAnalytic**: Geographic traffic data

## 🔧 Management Commands

### Crawling & Indexing
```bash
# Combined crawling and indexing
python manage.py crawl_and_index --crawl-workers 4 --index-workers 2

# Crawl only
python manage.py crawl_and_index --crawl-only --crawl-workers 4

# Index only
python manage.py crawl_and_index --index-only --index-workers 2

# Continuous mode
python manage.py crawl_and_index --continuous
```

### Data Management
```bash
# Clear all data
python manage.py clear_all_data --confirm

# Clear only OpenSearch
python manage.py clear_all_data --opensearch-only --confirm

# Clear only database
python manage.py clear_all_data --database-only --confirm
```

## 🌐 API Endpoints

### Authentication
- `POST /api/login/` - User login
- `POST /api/register/` - User registration
- `POST /api/logout/` - User logout

### Search
- `POST /api/search/` - Perform search
- `GET /api/search-results/` - Get search results

### Management
- `GET/POST /api/website-links/` - Website link management
- `GET /api/analytics/` - Analytics data
- `GET /api/status/` - Health check

## 🚀 Deployment Architecture

### Development
```
Developer Machine
├── Frontend (Angular Dev Server) - Port 4200
├── Backend (Django Dev Server) - Port 8000
├── PostgreSQL - Port 5432
└── OpenSearch - Port 9200
```

### Production
```
Load Balancer (Nginx)
├── Frontend (Static Files)
├── Backend (Django + Gunicorn)
├── Database (PostgreSQL Cluster)
└── Search Engine (OpenSearch Cluster)
```

## 🔒 Security Features

### Authentication & Authorization
- Token-based API authentication
- Session-based web authentication
- Role-based access control
- CSRF protection
- XSS prevention

### Data Protection
- Environment variable configuration
- Secure password hashing
- Input validation and sanitization
- SQL injection prevention
- Secure headers configuration

## 📈 Performance Optimizations

### Frontend
- Lazy loading and code splitting
- OnPush change detection
- Virtual scrolling for large datasets
- Bundle optimization and minification

### Backend
- Database query optimization
- Caching strategies
- Background task processing
- Connection pooling

### Search Engine
- Index optimization
- Query performance tuning
- Caching frequently accessed data
- Distributed search capabilities

## 🧪 Testing Strategy

### Frontend Testing
- Unit tests with Jasmine/Karma
- E2E tests with Protractor
- Component testing
- Service testing

### Backend Testing
- Unit tests with Django TestCase
- API endpoint testing
- Integration tests
- Performance testing

## 📚 Documentation Structure

- **Main README**: Project overview and quick start
- **Backend README**: Django setup and API documentation
- **Frontend README**: Angular setup and component documentation
- **Environment Setup**: Configuration guide
- **Project Overview**: This comprehensive overview

## 🤝 Development Workflow

1. **Setup**: Run `./setup.sh` for automated setup
2. **Development**: Use `./start_all.sh` for full development environment
3. **Testing**: Run tests before committing changes
4. **Deployment**: Follow production deployment guide
5. **Monitoring**: Use health checks and logging for monitoring

---

**SearchMyWeb** - A comprehensive web search and analytics platform built with modern technologies and best practices.
