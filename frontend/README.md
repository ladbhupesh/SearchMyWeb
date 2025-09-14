# SearchMyWeb Frontend

Angular-based frontend application for SearchMyWeb, providing an intuitive user interface for web search, analytics, and content management.

## 🏗️ Architecture

### Technology Stack
- **Framework**: Angular 13.3.0
- **UI Library**: Bootstrap 5.1.3, Angular Material 13.3.7
- **Icons**: FontAwesome 6.0.0
- **Charts**: Chart.js 2.9.4, Highcharts 10.1.0
- **Data Grid**: AG Grid 27.2.1
- **Notifications**: ngx-toastr 14.3.0
- **Styling**: SCSS with custom themes

### Project Structure
```
frontend/
├── src/
│   ├── app/
│   │   ├── analytics/              # Analytics dashboard
│   │   ├── home/                   # Main dashboard with sidebar
│   │   ├── login/                  # Authentication pages
│   │   ├── signup/
│   │   ├── test-search/            # Search interface
│   │   ├── select-search/          # Advanced search
│   │   ├── manage-indexes/         # Index management
│   │   ├── traffic-sources/        # Traffic analytics
│   │   ├── statewise-traffic-sources/ # Geographic analytics
│   │   ├── wordcloud/              # Word cloud visualization
│   │   ├── livelogger/             # Live logging
│   │   ├── list-all-urls/          # URL management
│   │   ├── boolean-cell/           # Custom grid components
│   │   ├── delete-cell/
│   │   ├── update-cell/
│   │   ├── api-service.service.ts  # API communication
│   │   ├── check-auth.service.ts   # Authentication service
│   │   └── app-routing.module.ts   # Routing configuration
│   ├── assets/                     # Static assets
│   │   ├── fonts/                  # Custom fonts (Poppins, Montserrat)
│   │   └── images/                 # Images and icons
│   ├── environments/               # Environment configurations
│   └── styles.scss                 # Global styles
├── angular.json                    # Angular CLI configuration
├── package.json                    # Dependencies and scripts
└── tsconfig.json                   # TypeScript configuration
```

## 🚀 Quick Start

### Prerequisites
- Node.js 14+
- npm 6+ (or yarn)
- Angular CLI 13.3.5+

### Installation

1. **Clone and Navigate**
   ```bash
   git clone <repository-url>
   cd SearchMyWeb/frontend
   ```

2. **Install Dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start Development Server**
   ```bash
   npm start
   # or
   ng serve
   ```

4. **Access Application**
   - Open browser to http://localhost:4200
   - Default login: admin/admin (or create new account)

## ⚙️ Configuration

### Environment Configuration

#### Development Environment (`src/environments/environment.ts`)
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api',
  appName: 'SearchMyWeb',
  version: '1.0.0'
};
```

#### Production Environment (`src/environments/environment.prod.ts`)
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://api.searchmyweb.in/api',
  appName: 'SearchMyWeb',
  version: '1.0.0'
};
```

### API Configuration

Update API endpoints in the environment files:
```typescript
// API Base URL
apiUrl: 'http://localhost:8000/api'

// Specific endpoints
loginUrl: '/login/',
registerUrl: '/register/',
searchUrl: '/search/',
analyticsUrl: '/analytics/'
```

## 🎨 UI Components

### Core Components

#### HomeComponent
Main dashboard with sidebar navigation and content area.
- **Sidebar**: Navigation menu with role-based access
- **Content Area**: Dynamic component loading based on route
- **Responsive Design**: Mobile-friendly layout

#### TestSearchComponent
Advanced search interface with modern UI.
- **Search Input**: Real-time search with suggestions
- **Results Display**: Card-based results with actions
- **Search Statistics**: Query count and timing
- **Toast Notifications**: User feedback system

#### AnalyticsComponent
Comprehensive analytics dashboard.
- **Charts**: Interactive data visualizations
- **Metrics**: Key performance indicators
- **Filters**: Date range and category filters
- **Export**: Data export functionality

### Custom Components

#### BooleanCellComponent
Custom AG Grid cell renderer for boolean values.
```typescript
@Component({
  selector: 'app-boolean-cell',
  template: `
    <span [class]="value ? 'text-success' : 'text-danger'">
      {{ value ? 'Yes' : 'No' }}
    </span>
  `
})
```

#### DeleteCellComponent
Custom AG Grid cell renderer for delete actions.
```typescript
@Component({
  selector: 'app-delete-cell',
  template: `
    <button class="btn btn-danger btn-sm" (click)="delete()">
      <i class="fas fa-trash"></i>
    </button>
  `
})
```

## 🔧 Services

### ApiService
Centralized API communication service.

```typescript
@Injectable({
  providedIn: 'root'
})
export class ApiServiceService {
  private baseUrl = environment.apiUrl;

  // Authentication
  login(credentials: LoginCredentials): Observable<AuthResponse> {
    return this.http.post(`${this.baseUrl}/login/`, credentials);
  }

  // Search
  getSearchResults(query: string): Observable<SearchResponse> {
    return this.http.post(`${this.baseUrl}/search/`, { query });
  }

  // Analytics
  getAnalytics(): Observable<AnalyticsData> {
    return this.http.get(`${this.baseUrl}/analytics/`);
  }
}
```

### CheckAuthService
Authentication and authorization service.

```typescript
@Injectable({
  providedIn: 'root'
})
export class CheckAuthService implements CanActivate {
  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    // Check authentication status
    // Redirect to login if not authenticated
  }
}
```

## 🎯 Features

### Search Functionality
- **Real-time Search**: Instant search with debouncing
- **Search Suggestions**: Auto-complete functionality
- **Search History**: Previous search tracking
- **Advanced Filters**: Category, date, and source filters
- **Search Analytics**: Query performance metrics

### Analytics Dashboard
- **Traffic Sources**: Referrer and source analysis
- **Geographic Data**: State-wise traffic visualization
- **Search Metrics**: Query volume and performance
- **User Behavior**: Click tracking and engagement
- **Word Cloud**: Popular terms visualization

### Content Management
- **URL Management**: Add, edit, and delete website links
- **Index Management**: Control crawling and indexing
- **Bulk Operations**: Mass actions on multiple items
- **Status Monitoring**: Real-time processing status

### User Interface
- **Responsive Design**: Mobile-first approach
- **Dark Theme**: Consistent with backend theme
- **Modern UI**: Clean and intuitive interface
- **Accessibility**: WCAG 2.1 compliance
- **Performance**: Optimized loading and rendering

## 🎨 Styling and Theming

### SCSS Architecture
```scss
// Global styles
@import '~bootstrap/scss/bootstrap';
@import '~@fortawesome/fontawesome-free/scss/fontawesome';

// Custom variables
$primary-color: #1a1c1e;
$secondary-color: #fafafa;
$accent-color: #007bff;

// Component styles
.search-container {
  background: $secondary-color;
  font-family: 'Poppins', Arial, sans-serif;
}
```

### Theme Configuration
- **Primary Color**: #1a1c1e (dark theme)
- **Background**: #fafafa (light background)
- **Accent Color**: #007bff (Bootstrap blue)
- **Typography**: Poppins font family
- **Spacing**: Consistent 8px grid system

### Responsive Breakpoints
```scss
// Mobile first approach
@media (max-width: 768px) {
  .search-container {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .search-container {
    padding: 0.5rem;
  }
}
```

## 🧪 Testing

### Unit Testing
```bash
# Run unit tests
npm test

# Run tests with coverage
npm run test:coverage

# Run tests in watch mode
npm run test:watch
```

### E2E Testing
```bash
# Run e2e tests
npm run e2e

# Run e2e tests in headless mode
npm run e2e:headless
```

### Test Configuration
- **Jasmine**: Testing framework
- **Karma**: Test runner
- **Protractor**: E2E testing
- **Coverage**: Istanbul coverage reports

## 🚀 Build and Deployment

### Development Build
```bash
# Development build
npm run build

# Development build with watch
npm run build:watch
```

### Production Build
```bash
# Production build
npm run build:prod

# Production build with optimization
ng build --configuration production
```

### Build Optimization
- **Tree Shaking**: Remove unused code
- **Minification**: Compress JavaScript and CSS
- **Bundle Splitting**: Code splitting for better performance
- **Lazy Loading**: Route-based lazy loading

### Deployment
```bash
# Build for production
ng build --configuration production

# Deploy to web server
# Copy dist/ contents to web server directory
```

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Mobile Features
- **Touch-friendly**: Large tap targets
- **Swipe Navigation**: Gesture support
- **Offline Support**: Service worker caching
- **Progressive Web App**: PWA capabilities

## 🔒 Security

### Authentication
- **Token-based**: JWT token authentication
- **Session Management**: Secure session handling
- **Route Guards**: Protected routes
- **Auto-logout**: Session timeout

### Data Protection
- **Input Validation**: Client-side validation
- **XSS Prevention**: Sanitized inputs
- **CSRF Protection**: Cross-site request forgery prevention
- **Secure Headers**: Security headers configuration

## 📊 Performance

### Optimization Strategies
- **Lazy Loading**: Route-based code splitting
- **OnPush Change Detection**: Optimized change detection
- **TrackBy Functions**: Efficient list rendering
- **Virtual Scrolling**: Large dataset handling

### Bundle Analysis
```bash
# Analyze bundle size
npm run build:analyze

# Bundle size report
ng build --stats-json
npx webpack-bundle-analyzer dist/stats.json
```

### Performance Monitoring
- **Core Web Vitals**: LCP, FID, CLS metrics
- **Bundle Size**: JavaScript and CSS size tracking
- **Load Time**: Page load performance
- **Runtime Performance**: Component rendering time

## ��️ Development Tools

### Angular CLI Commands
```bash
# Generate component
ng generate component component-name

# Generate service
ng generate service service-name

# Generate guard
ng generate guard guard-name

# Generate module
ng generate module module-name
```

### Code Quality
```bash
# Lint code
ng lint

# Format code
ng format

# Type checking
ng build --dry-run
```

### Debugging
- **Angular DevTools**: Browser extension
- **Source Maps**: Debug-friendly builds
- **Console Logging**: Development logging
- **Error Handling**: Global error handling

## 📚 Additional Resources

- [Angular Documentation](https://angular.io/docs)
- [Bootstrap Documentation](https://getbootstrap.com/docs)
- [FontAwesome Icons](https://fontawesome.com/icons)
- [Chart.js Documentation](https://www.chartjs.org/docs)
- [AG Grid Documentation](https://www.ag-grid.com/)

## 🤝 Contributing

### Development Workflow
1. Create feature branch
2. Make changes with tests
3. Run linting and tests
4. Submit pull request
5. Code review and merge

### Code Standards
- **TypeScript**: Strict type checking
- **ESLint**: Code quality rules
- **Prettier**: Code formatting
- **Conventional Commits**: Commit message format

---

**SearchMyWeb Frontend** - Modern, responsive web interface for powerful search capabilities.
