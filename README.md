# RaiderCritic API

RaiderCritic is a comprehensive motorcycle review and rating platform for Bangladesh. This API serves as the backend for the RaiderCritic platform, providing endpoints for managing motorcycle reviews, ratings, and related information.

## Features

- Motorcycle reviews and ratings
- Brand and model information
- User authentication and profiles
- Review search and filtering
- Detailed motorcycle specifications
- Community feedback system

## Tech Stack

- FastAPI (Python web framework)
- Firebase (Authentication & Database)
- Docker (Containerization)
- GitHub Actions (CI/CD)

## Getting Started

### Prerequisites

- Python 3.12+
- Docker
- Firebase account
- Node.js 18+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/raidercritic.git
cd raidercritic
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the development server:
```bash
cd functions
python main.py
```

The API will be available at `http://127.0.0.1:8000`

### Docker Setup

Build and run with Docker:

```bash
docker build -t raidercritic .
docker run -p 8000:8000 raidercritic
```

## API Documentation

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the ISC License. 