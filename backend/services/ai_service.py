import os
import logging
from typing import Dict, Any, Optional
from .pollinations_image_service import PollinationsImageService
from .groq_service import GroqService

logger = logging.getLogger(__name__)

class AIService:
    """AI service using Groq (Together.ai) for all STEM tasks"""
    
    def __init__(self):
        # Initialize Groq service (branded as Together.ai)
        self.groq_service = GroqService()
        
        # Initialize Pollinations image service
        self.image_service = PollinationsImageService()
        
        logger.info("AI Service initialized with Together.ai and Pollinations")
    
    def solve_problem(self, problem: str, subject: str, difficulty: str, 
                     show_steps: bool = True, include_theory: bool = True, 
                     include_diagrams: bool = True, temperature: float = 0.7,
                     preferred_model: str = "default") -> Dict[str, Any]:
        """Solve problem using Together.ai"""
        from datetime import datetime
        
        try:
            logger.info(f"Solving problem: {problem[:50]}...")
            
            result = self.groq_service.solve_problem(
                problem=problem,
                subject=subject,
                difficulty=difficulty,
                show_steps=show_steps,
                include_theory=include_theory,
                include_diagrams=include_diagrams,
                temperature=temperature
            )
            
            # Add timestamp
            result["metadata"]["timestamp"] = datetime.utcnow().isoformat()
            
            logger.info("Successfully solved problem with Together.ai")
            return result
            
        except Exception as e:
            logger.error(f"Error solving problem: {str(e)}")
            raise Exception(f"Failed to solve problem: {str(e)}")
    
    def health_check(self) -> Dict[str, Any]:
        """Check health status of AI services"""
        groq_status = self.groq_service.health_check()
        
        return {
            "together_ai": groq_status,
            "overall_status": groq_status["available"],
            "overall": "healthy" if groq_status["available"] else "unhealthy"
        }
    
    def explain_concept(self, concept: str, subject: str = "General", level: str = "intermediate",
                       include_examples: bool = True, include_history: bool = False, 
                       temperature: float = 0.7) -> str:
        """Explain a concept using Together.ai"""
        try:
            logger.info(f"Explaining concept: {concept}")
            return self.groq_service.explain_concept(
                concept=concept,
                subject=subject,
                level=level,
                include_examples=include_examples,
                include_history=include_history,
                temperature=temperature
            )
        except Exception as e:
            logger.error(f"Error explaining concept: {str(e)}")
            raise Exception(f"Failed to explain concept: {str(e)}")
    
    def get_study_tips(self, subject: str, learning_style: str = "Visual", 
                      study_goal: str = "General Understanding",
                      challenges: list = None, temperature: float = 0.7) -> str:
        """Get personalized study tips using Together.ai"""
        try:
            logger.info(f"Getting study tips for {subject}")
            return self.groq_service.get_study_tips(
                subject=subject,
                learning_style=learning_style,
                study_goal=study_goal,
                challenges=challenges or [],
                temperature=temperature
            )
        except Exception as e:
            logger.error(f"Error getting study tips: {str(e)}")
            raise Exception(f"Failed to get study tips: {str(e)}")
    
    def get_formulas(self, subject: str, topic: str = "", search_term: str = "", 
                    temperature: float = 0.3) -> str:
        """Get formulas for a subject/topic using Together.ai"""
        try:
            logger.info(f"Getting formulas for {subject} - {topic}")
            return self.groq_service.get_formulas(
                subject=subject,
                topic=topic,
                search_term=search_term,
                temperature=temperature
            )
        except Exception as e:
            logger.error(f"Error getting formulas: {str(e)}")
            return f"Error getting formulas: {str(e)}"
    
    def generate_image(self, prompt: str, context: str = "", size: str = "512x512", 
                      quality: str = "standard", style: str = "educational",
                      subject: str = "General Science") -> Dict[str, Any]:
        """Generate image using Pollinations"""
        try:
            return self.image_service.generate_image(
                prompt=prompt,
                context=context,
                size=size,
                quality=quality,
                style=style,
                subject=subject
            )
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def generate_educational_diagram(self, concept: str, subject: str, 
                                   difficulty: str = "intermediate") -> Dict[str, Any]:
        """Generate educational diagrams for STEM concepts"""
        try:
            return self.image_service.generate_educational_diagram(
                concept=concept,
                subject=subject,
                difficulty=difficulty
            )
        except Exception as e:
            logger.error(f"Error generating educational diagram: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def generate_problem_illustration(self, problem_text: str, subject: str) -> Dict[str, Any]:
        """Generate illustration for STEM problems"""
        try:
            return self.image_service.generate_problem_illustration(
                problem_text=problem_text,
                subject=subject
            )
        except Exception as e:
            logger.error(f"Error generating problem illustration: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def analyze_image(self, image_url: str, question: str = "") -> Dict[str, Any]:
        """Analyze images - Feature not available"""
        return {
            "success": False,
            "error": "Image analysis not available",
            "suggestion": "Upload image and use problem-solving features instead"
        }
    
    def get_image_training_stats(self) -> Dict[str, Any]:
        """Get statistics about image service"""
        try:
            return self.image_service.get_training_stats()
        except Exception as e:
            logger.error(f"Error getting training stats: {str(e)}")
            return {"error": str(e)}
    
    def create_fine_tuning_dataset(self) -> Dict[str, Any]:
        """Create fine-tuning dataset - Not available"""
        return {"success": False, "message": "Fine-tuning not available"}
