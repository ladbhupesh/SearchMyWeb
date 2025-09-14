# SearchMyWeb

A comprehensive web search and indexing platform built with Django and Angular. SearchMyWeb allows users to crawl, index, and search websites with advanced analytics and user management capabilities.

## 🚀 Features

### Core Functionality
- **Web Crawling**: Automated website crawling with configurable depth levels
- **Search Indexing**: OpenSearch-based indexing for fast and accurate search results
- **Real-time Search**: Instant search across indexed content
- **User Management**: Role-based authentication and authorization
- **Analytics Dashboard**: Comprehensive analytics with traffic sources, word clouds, and geographic data

### Advanced Features
- **Multi-threaded Processing**: Concurrent crawling and indexing for improved performance
- **Geographic Analytics**: IP-based location tracking and state-wise traffic analysis
- **Search Analytics**: Query logging, click tracking, and search statistics
- **Live Logging**: Real-time monitoring of crawling and indexing activities
- **Data Management**: Comprehensive data cleanup and management tools

## 🏗️ Architecture

### Backend (Django)
- **Framework**: Django 5.2.6 with Django REST Framework
- **Database**: PostgreSQL (development) / SQLite (production)
- **Search Engine**: OpenSearch (formerly Elasticsearch)
- **Authentication**: Token-based authentication with session support
- **Task Scheduling**: APScheduler for background tasks

### Frontend (Angular)
- **Framework**: Angular 13.3.0
- **UI Components**: Bootstrap 5, Angular Material, FontAwesome
- **Charts**: Chart.js, Highcharts for analytics visualization
- **State Management**: Angular services and reactive programming

## 📁 Project Structure

```
SearchMyWeb/
├── backend/                 # Django backend application
│   ├── MySearchEngine/     # Django project settings
│   ├── UserManagementApp/  # Main Django app
│   ├── server_status/      # Health check endpoints
│   ├── scripts/           # Management scripts
│   └── requirements.txt   # Python dependencies
├── frontend/               # Angular frontend application
│   ├── src/app/           # Angular components and services
│   ├── src/assets/        # Static assets
│   └── package.json       # Node.js dependencies
└── venv/                  # Python virtual environment
```

## 🛠️ Prerequisites

### System Requirements
- Python 3.8+
- Node.js 14+
- PostgreSQL 12+ (for development)
- OpenSearch 2.0+ (or Elasticsearch 8.0+)

### Development Tools
- Git
- Virtual environment (venv)
- npm/yarn

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd SearchMyWeb
```

### 2. Backend Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### 3. Frontend Setup
```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm start
```

### 4. Access the Application
- Frontend: http://localhost:4200
- Backend API: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

## 📖 Detailed Setup

## 📚 Documentation

- **[Main README](README.md)** - Project overview and quick start
- **[Backend README](backend/README.md)** - Django setup and API documentation
- **[Frontend README](frontend/README.md)** - Angular setup and component documentation
- **[Project Overview](PROJECT_OVERVIEW.md)** - Comprehensive system architecture
- **[Environment Setup](backend/ENVIRONMENT_SETUP.md)** - Configuration guide

## �� Quick Setup

For automated setup, run:
```bash
./setup.sh
```

This script will:
- Check prerequisites
- Set up Python virtual environment
- Install all dependencies
- Configure database
- Create startup scripts
- Provide next steps


### Backend Configuration

1. **Environment Variables**: Copy `.env.example` to `.env` and configure:
   - Database credentials
   - OpenSearch connection
   - Security tokens
   - Domain settings

2. **Database Setup**: 
   - Development: PostgreSQL with configured credentials
   - Production: SQLite (automatic)

3. **OpenSearch Setup**:
   - Install OpenSearch 2.0+
   - Configure connection in `.env`
   - Verify health check endpoint

### Frontend Configuration

1. **API Configuration**: Update API endpoints in `src/environments/`
2. **Build Configuration**: Modify `angular.json` for production builds
3. **Theme Customization**: Update SCSS files in component directories

## 🔧 Management Commands

### Crawling and Indexing
```bash
# Crawl and index websites simultaneously
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
# Clear all data (with confirmation)
python manage.py clear_all_data --confirm

# Clear only OpenSearch indexes
python manage.py clear_all_data --opensearch-only --confirm

# Clear only database data
python manage.py clear_all_data --database-only --confirm
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 API Documentation

### Authentication
- **Login**: `POST /api/login/`
- **Register**: `POST /api/register/`
- **Logout**: `POST /api/logout/`

### Search
- **Search**: `POST /api/search/`
- **Search Results**: `GET /api/search-results/`

### Management
- **Website Links**: `GET/POST /api/website-links/`
- **Analytics**: `GET /api/analytics/`
- **Health Check**: `GET /api/status/`

## 🚀 Deployment

### Production Environment
1. Set `DEBUG=False` in environment variables
2. Configure production database
3. Set up SSL certificates
4. Configure OpenSearch cluster
5. Set up reverse proxy (nginx/Apache)

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

## 🔒 Security

- Environment variables for sensitive data
- Token-based authentication
- CSRF protection
- SQL injection prevention
- XSS protection
- Secure headers configuration

## 📈 Monitoring

- Health check endpoints
- Application logging
- Error tracking
- Performance monitoring
- Search analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## �� Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the troubleshooting guide

## 🔄 Version History

- **v1.0.0**: Initial release with basic crawling and search
- **v1.1.0**: Added analytics dashboard
- **v1.2.0**: Implemented OpenSearch migration
- **v1.3.0**: Enhanced UI and user experience

---

**SearchMyWeb** - Empowering web search with advanced indexing and analytics capabilities.
