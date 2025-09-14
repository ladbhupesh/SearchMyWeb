#!/bin/bash

# SearchMyWeb Setup Script
# This script sets up the entire SearchMyWeb application

set -e  # Exit on any error

echo "🚀 SearchMyWeb Setup Script"
echo "=========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on supported OS
check_os() {
    print_status "Checking operating system..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_success "Linux detected"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        print_success "macOS detected"
    else
        print_warning "Unsupported OS: $OSTYPE"
        print_warning "This script is designed for Linux and macOS"
    fi
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    # Check Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_success "Node.js $NODE_VERSION found"
    else
        print_error "Node.js is required but not installed"
        exit 1
    fi
    
    # Check npm
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        print_success "npm $NPM_VERSION found"
    else
        print_error "npm is required but not installed"
        exit 1
    fi
    
    # Check PostgreSQL (optional)
    if command -v psql &> /dev/null; then
        print_success "PostgreSQL found"
    else
        print_warning "PostgreSQL not found - will use SQLite for development"
    fi
}

# Setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "../venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv ../venv
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source ../venv/bin/activate
    
    # Install Python dependencies
    print_status "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Setup environment variables
    if [ ! -f ".env" ]; then
        print_status "Creating environment configuration..."
        cp .env.example .env
        print_warning "Please edit backend/.env with your configuration"
    else
        print_success "Environment configuration already exists"
    fi
    
    # Run database migrations
    print_status "Running database migrations..."
    python manage.py migrate
    
    # Create superuser if it doesn't exist
    print_status "Creating superuser (if not exists)..."
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
    
    print_success "Backend setup completed"
    cd ..
}

# Setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Install Node.js dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    print_success "Frontend setup completed"
    cd ..
}

# Create startup scripts
create_startup_scripts() {
    print_status "Creating startup scripts..."
    
    # Backend startup script
    cat > start_backend.sh << 'BACKEND_EOF'
#!/bin/bash
echo "🚀 Starting SearchMyWeb Backend..."
cd backend
source ../venv/bin/activate
python manage.py runserver
BACKEND_EOF
    chmod +x start_backend.sh
    
    # Frontend startup script
    cat > start_frontend.sh << 'FRONTEND_EOF'
#!/bin/bash
echo "🚀 Starting SearchMyWeb Frontend..."
cd frontend
npm start
FRONTEND_EOF
    chmod +x start_frontend.sh
    
    # Combined startup script
    cat > start_all.sh << 'ALL_EOF'
#!/bin/bash
echo "🚀 Starting SearchMyWeb Application..."

# Function to handle cleanup on exit
cleanup() {
    echo "🛑 Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start backend
echo "Starting backend server..."
cd backend
source ../venv/bin/activate
python manage.py runserver &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "Starting frontend server..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo "✅ Both services started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:4200"
echo "Press Ctrl+C to stop all services"

# Wait for processes
wait
ALL_EOF
    chmod +x start_all.sh
    
    print_success "Startup scripts created"
}

# Display final instructions
show_final_instructions() {
    echo ""
    echo "🎉 Setup Complete!"
    echo "================"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Edit backend/.env with your configuration"
    echo "2. Start the application:"
    echo "   - Individual services: ./start_backend.sh and ./start_frontend.sh"
    echo "   - Both services: ./start_all.sh"
    echo ""
    echo "🌐 Access Points:"
    echo "   - Frontend: http://localhost:4200"
    echo "   - Backend API: http://localhost:8000"
    echo "   - Admin Panel: http://localhost:8000/admin"
    echo ""
    echo "👤 Default Login:"
    echo "   - Username: admin"
    echo "   - Password: admin"
    echo ""
    echo "📚 Documentation:"
    echo "   - Main README: ./README.md"
    echo "   - Backend README: ./backend/README.md"
    echo "   - Frontend README: ./frontend/README.md"
    echo ""
    echo "🛠️ Management Commands:"
    echo "   - Crawl and index: cd backend && python manage.py crawl_and_index"
    echo "   - Clear data: cd backend && python manage.py clear_all_data --confirm"
    echo ""
    print_success "Happy searching! 🔍"
}

# Main execution
main() {
    check_os
    check_prerequisites
    setup_backend
    setup_frontend
    create_startup_scripts
    show_final_instructions
}

# Run main function
main "$@"
