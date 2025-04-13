# Bangla Motorcycle Review API

A FastAPI-based REST API for motorcycle reviews in Bangla with AI integration.

## Features

- Motorcycle reviews in Bangla
- AI-powered content generation
- Firebase integration
- RESTful API endpoints
- Authentication and authorization
- Data scraping capabilities

## Tech Stack

- FastAPI
- Firebase (Firestore, Authentication, Hosting)
- Bangla T5 for AI content generation
- Python 3.8+
- GitHub Actions for CI/CD

## Setup

1. Clone the repository:
```bash
git clone https://github.com/ashifbabu/motobd.git
cd motobd
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the development server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Running Tests
```bash
pytest
```

### Code Style
```bash
# Format code
black app tests
isort app tests

# Check code style
flake8 app tests
```

## CI/CD

The project uses GitHub Actions for continuous integration and deployment. The workflow includes:
- Testing with multiple Python versions
- Code linting
- Coverage reporting
- Firebase deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 