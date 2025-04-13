import os
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
from app.services.firebase_service import FirebaseService
from app.services.auth_service import AuthService

class AIService:
    def __init__(self):
        self.model_name = os.getenv("AI_MODEL_NAME", "csebuetnlp/banglat5")
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.firebase_service = FirebaseService()
        self.auth_service = AuthService()

    async def _load_model(self):
        if self.model is None:
            self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
            self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
            self.model.to(self.device)

    async def generate_review(self, bike_id: str, token: str) -> dict:
        """Generate a review for a bike using AI."""
        try:
            # Verify user authentication
            user = await self.auth_service.get_current_user(token)
            
            # Get bike details
            bike = await self.firebase_service.get_bike(bike_id)
            if not bike:
                raise ValueError("Bike not found")

            # Load model if not loaded
            await self._load_model()

            # Create prompt
            prompt = f"বাইক পর্যালোচনা লিখুন: {bike.name}. বৈশিষ্ট্য: {bike.engine}, {bike.power}, {bike.torque}. মূল্য: {bike.price}"
            
            # Generate review
            inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                inputs,
                max_length=int(os.getenv("AI_MAX_LENGTH", 1000)),
                num_beams=int(os.getenv("AI_NUM_BEAMS", 5)),
                no_repeat_ngram_size=int(os.getenv("AI_NO_REPEAT_NGRAM_SIZE", 2)),
                early_stopping=True
            )
            
            review = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return {
                "content": review,
                "bike_id": bike_id,
                "user_id": user.id,
                "ai_generated": True
            }
        except Exception as e:
            raise ValueError(f"Error generating review: {str(e)}")

    async def analyze_review(self, review_id: str, token: str) -> dict:
        """Analyze a review using AI."""
        try:
            # Verify user authentication
            await self.auth_service.get_current_user(token)
            
            # Get review
            review = await self.firebase_service.get_review(review_id)
            if not review:
                raise ValueError("Review not found")

            # Load model if not loaded
            await self._load_model()

            # Create prompt
            prompt = f"পর্যালোচনা বিশ্লেষণ করুন: {review.content}"
            
            # Generate analysis
            inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                inputs,
                max_length=500,
                num_beams=5,
                early_stopping=True
            )
            
            analysis = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return {
                "analysis": analysis,
                "sentiment": "positive" if "positive" in analysis.lower() else "negative",
                "review_id": review_id
            }
        except Exception as e:
            raise ValueError(f"Error analyzing review: {str(e)}")

    async def summarize_reviews(self, bike_id: str, token: str) -> dict:
        """Summarize all reviews for a bike using AI."""
        try:
            # Verify user authentication
            await self.auth_service.get_current_user(token)
            
            # Get bike reviews
            reviews = await self.firebase_service.get_bike_reviews(bike_id)
            if not reviews:
                raise ValueError("No reviews found for this bike")

            # Load model if not loaded
            await self._load_model()

            # Create prompt
            reviews_text = " ".join([r.content for r in reviews])
            prompt = f"পর্যালোচনাগুলি সংক্ষিপ্ত করুন: {reviews_text}"
            
            # Generate summary
            inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                inputs,
                max_length=500,
                num_beams=5,
                early_stopping=True
            )
            
            summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return {
                "summary": summary,
                "bike_id": bike_id,
                "review_count": len(reviews)
            }
        except Exception as e:
            raise ValueError(f"Error summarizing reviews: {str(e)}") 