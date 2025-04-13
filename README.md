# 🏍️ Bangla Motorcycle Review API

A comprehensive API for motorcycle reviews in Bangladesh, powered by Firebase and AI. This project aims to provide detailed motorcycle reviews, specifications, and AI-generated content in Bangla language.

## 🌟 Features

- **Motorcycle Reviews**: Comprehensive reviews in Bangla
- **AI-Powered Content**: Automated review generation using BanglaBERT/Bangla T5
- **Real-time Database**: Firebase Firestore integration
- **Authentication**: Secure API access with Firebase Auth
- **Cloud Functions**: Serverless backend with FastAPI
- **Automated Deployment**: CI/CD with GitHub Actions

## 🚀 Live Demo

- API Endpoint: [https://motobd-5dc39.web.app](https://motobd-5dc39.web.app)
- API Documentation: [https://motobd-5dc39.web.app/docs](https://motobd-5dc39.web.app/docs)

## 🛠️ Tech Stack

- **Backend**: FastAPI + Firebase Cloud Functions
- **Database**: Firebase Firestore
- **Authentication**: Firebase Auth
- **AI Model**: BanglaBERT/Bangla T5
- **Hosting**: Firebase Hosting
- **CI/CD**: GitHub Actions

## 📝 API Endpoints

### Reviews
- `GET /reviews/bikes/` - List all bike reviews
- `POST /reviews/bikes/` - Create a new bike review
- `GET /reviews/bikes/{bike_id}` - Get specific review
- `PUT /reviews/bikes/{bike_id}` - Update review
- `DELETE /reviews/bikes/{bike_id}` - Delete review

### AI Generation
- `POST /ai/generate/review/` - Generate bike review
- `POST /ai/generate/summary/` - Generate summary
- `POST /ai/generate/comparison/` - Generate comparison

### Bikes
- `GET /bikes/` - List all bikes
- `POST /bikes/` - Add new bike
- `GET /bikes/{bike_id}` - Get bike details
- `PUT /bikes/{bike_id}` - Update bike
- `DELETE /bikes/{bike_id}` - Delete bike

## 🔧 Setup & Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ashifbabu/motobd.git
   cd motobd
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   npm install -g firebase-tools
   ```

3. Configure Firebase:
   ```bash
   firebase login
   firebase init
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update with your Firebase credentials

5. Deploy:
   ```bash
   firebase deploy
   ```

## 🔒 Environment Variables

Required environment variables:

```env
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_API_KEY=your-api-key
HUGGINGFACE_TOKEN=your-token
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Ashif Babu** - *Initial work* - [ashifbabu](https://github.com/ashifbabu)

## 🙏 Acknowledgments

- Firebase team for the excellent BaaS platform
- Hugging Face for the transformer models
- FastAPI team for the amazing framework

## 📊 Project Status

Current Status: In Development (15% Complete)
Last Updated: April 13, 2024

See [PROGRESS.md](PROGRESS.md) for detailed progress tracking. 