import os
import logging
import requests
from typing import Dict, Any, Optional
from .pollinations_image_service import PollinationsImageService
from .nvidia_llama_service import NvidiaLlamaService
from .nvidia_nemotron_service import NvidiaNemotronService

logger = logging.getLogger(__name__)

class AIService:
    """AI service using NVIDIA Llama for problem solving/concept explanation and Nemotron for formulas/study tips"""
    
    def __init__(self):
        # Initialize NVIDIA Llama service (for Problem Solver and Concept Explainer)
        self.llama_service = NvidiaLlamaService()
        
        # Initialize NVIDIA Nemotron service (for Formula Reference and Study Tips)
        try:
            self.nemotron_service = NvidiaNemotronService()
            logger.info("NVIDIA Nemotron service initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize Nemotron service: {e}. Will fall back to Llama.")
            self.nemotron_service = None
        
        # Initialize Pollinations image service
        self.image_service = PollinationsImageService()
        
        logger.info("AI Service initialized with NVIDIA Llama, Nemotron, and Pollinations")
    
    def solve_problem(self, problem: str, subject: str, difficulty: str, 
                     show_steps: bool = True, include_theory: bool = True, 
                     include_diagrams: bool = True, temperature: float = 0.7,
                     preferred_model: str = "llama") -> Dict[str, Any]:
        """Solve problem using NVIDIA Llama"""
        from datetime import datetime
        
        try:
            logger.info(f"Solving problem with NVIDIA Llama: {problem[:50]}...")
            
            result = self.llama_service.solve_problem(
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
            
            logger.info("Successfully solved problem with NVIDIA Llama")
            return result
            
        except Exception as e:
            logger.error(f"Error solving problem: {str(e)}")
            raise Exception(f"Failed to solve problem: {str(e)}")
    
    def health_check(self) -> Dict[str, Any]:
        """Check health status of AI services"""
        llama_status = self.llama_service.health_check()
        nemotron_status = self.nemotron_service.health_check() if self.nemotron_service else {"available": False, "error": "Not initialized"}
        
        return {
            "llama": llama_status,
            "nemotron": nemotron_status,
            "overall_status": llama_status["available"],
            "overall": "healthy" if llama_status["available"] else "unhealthy"
        }
    
    def explain_concept(self, concept: str, subject: str = "General", level: str = "intermediate",
                       include_examples: bool = True, include_history: bool = False, 
                       temperature: float = 0.7) -> str:
        """Explain a concept using NVIDIA Llama"""
        try:
            logger.info(f"Explaining concept with NVIDIA Llama: {concept}")
            return self.llama_service.explain_concept(
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
        """Get personalized study tips using NVIDIA Nemotron (with Llama fallback)"""
        try:
            # Use Nemotron for study tips
            if self.nemotron_service:
                logger.info(f"Getting study tips with NVIDIA Nemotron for {subject}")
                return self.nemotron_service.get_study_tips(
                    subject=subject,
                    learning_style=learning_style,
                    study_goal=study_goal,
                    challenges=challenges or [],
                    temperature=temperature
                )
            else:
                # Fallback to Llama if Nemotron not available
                logger.info(f"Nemotron not available, using Llama for study tips: {subject}")
                return self.llama_service.get_study_tips(
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
        """Get formulas for a subject/topic using NVIDIA Nemotron (with Llama fallback)"""
        try:
            # Use Nemotron for formulas
            if self.nemotron_service:
                logger.info(f"Getting formulas with NVIDIA Nemotron for {subject} - {topic}")
                return self.nemotron_service.get_formulas(
                    subject=subject,
                    topic=topic,
                    search_term=search_term,
                    temperature=temperature
                )
            else:
                # Fallback to Llama if Nemotron not available
                logger.info(f"Nemotron not available, using Llama for formulas: {subject}")
                prompt = f"""Provide key formulas for {subject}"""
                if topic:
                    prompt += f" focusing on {topic}"
                if search_term:
                    prompt += f" related to {search_term}"
                prompt += """. 

Please format the response with:
1. Formula name and notation
2. Variable definitions
3. When to use each formula
4. Example application

Use clear markdown formatting."""
                
                messages = [
                    {"role": "system", "content": "You are a STEM educator providing clear formula references."},
                    {"role": "user", "content": prompt}
                ]
                
                return self.llama_service._make_request(messages, temperature=temperature, max_tokens=2000)
        except Exception as e:
            logger.error(f"Error getting formulas: {str(e)}")
            return f"Error getting formulas: {str(e)}"
    
    def generate_image(self, prompt: str, context: str = "", size: str = "512x512", 
                      quality: str = "standard", style: str = "educational",
                      subject: str = "General Science") -> Dict[str, Any]:
        """Generate image using Pollinations with subject restriction"""
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
            return {
                "success": False,
                "error": str(e)
            }
    
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
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_problem_illustration(self, problem_text: str, subject: str) -> Dict[str, Any]:
        """Generate illustration for STEM problems"""
        try:
            return self.image_service.generate_problem_illustration(
                problem_text=problem_text,
                subject=subject
            )
        except Exception as e:
            logger.error(f"Error generating problem illustration: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
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
        return {
            "success": False,
            "message": "Fine-tuning not available"
        }
