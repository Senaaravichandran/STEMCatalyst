import logging
import urllib.parse
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PollinationsImageService:
    """Image Generation Service using Pollinations.ai API"""
    
    def __init__(self):
        self.base_url = "https://image.pollinations.ai/prompt/"
        logger.info("Pollinations Image Service initialized successfully")
        
        # Subject keywords for validation
        self.subject_keywords = {
            "Mathematics": ["math", "equation", "geometry", "algebra", "calculus", "graph", "number", "formula", "triangle", "circle", "angle", "function", "derivative", "integral", "matrix", "vector", "probability", "statistics", "arithmetic", "fraction", "polynomial", "trigonometry", "sin", "cos", "tan", "logarithm", "exponential"],
            "Physics": ["physics", "force", "motion", "energy", "gravity", "velocity", "acceleration", "momentum", "wave", "light", "electricity", "magnetism", "quantum", "thermodynamics", "heat", "atom", "particle", "radiation", "circuit", "pressure", "density", "mass", "weight", "friction", "newton", "electromagnetic"],
            "Chemistry": ["chemistry", "chemical", "molecule", "atom", "reaction", "compound", "element", "bond", "electron", "proton", "neutron", "acid", "base", "periodic table", "organic", "inorganic", "solution", "concentration", "ph", "oxidation", "reduction", "catalyst", "polymer", "ion", "covalent", "ionic"],
            "Biology": ["biology", "cell", "dna", "rna", "protein", "gene", "organism", "plant", "animal", "bacteria", "virus", "evolution", "ecology", "photosynthesis", "respiration", "metabolism", "tissue", "organ", "species", "chromosome", "mitosis", "meiosis", "enzyme", "membrane", "nucleus", "ecosystem"],
            "General Science": ["science", "experiment", "hypothesis", "theory", "research", "data", "observation", "scientific method", "laboratory", "measurement"]
        }
    
    def _is_related_to_subject(self, prompt: str, subject: str) -> bool:
        """Check if the prompt is related to the selected subject"""
        prompt_lower = prompt.lower()
        
        # If General Science, allow all STEM topics
        if subject == "General Science":
            return True
        
        # Check if prompt contains keywords from the selected subject
        if subject in self.subject_keywords:
            for keyword in self.subject_keywords[subject]:
                if keyword in prompt_lower:
                    return True
        
        # Check if prompt contains keywords from OTHER subjects (to reject)
        other_subjects = [s for s in self.subject_keywords.keys() if s != subject and s != "General Science"]
        for other_subject in other_subjects:
            for keyword in self.subject_keywords[other_subject]:
                if keyword in prompt_lower:
                    # Found keyword from different subject
                    return False
        
        # If no specific keywords found, allow it (could be general educational request)
        return True
    
    def _detect_subject(self, prompt: str) -> str:
        """Detect which subject the prompt is about"""
        prompt_lower = prompt.lower()
        
        subject_scores = {}
        for subject, keywords in self.subject_keywords.items():
            if subject == "General Science":
                continue
            score = sum(1 for keyword in keywords if keyword in prompt_lower)
            if score > 0:
                subject_scores[subject] = score
        
        if subject_scores:
            return max(subject_scores, key=subject_scores.get)
        return "General"
    
    def _enhance_prompt(self, prompt: str, context: str = "", style: str = "educational") -> str:
        """Enhance the prompt for better educational image generation"""
        
        # Style-specific enhancements
        style_additions = {
            "educational": "educational diagram, clear visualization, professional, detailed, labeled, informative",
            "scientific": "scientific illustration, accurate, detailed, professional, research quality",
            "artistic": "beautiful, artistic, creative, visually appealing, colorful",
            "diagram": "technical diagram, schematic, blueprint style, clean lines, labeled components",
            "realistic": "photorealistic, high quality, detailed, professional photography"
        }
        
        enhancement = style_additions.get(style, style_additions["educational"])
        
        # Build enhanced prompt
        enhanced_parts = [prompt.strip()]
        
        if context:
            enhanced_parts.append(f"Context: {context}")
        
        enhanced_parts.append(enhancement)
        enhanced_parts.append("high resolution, 4k quality")
        
        enhanced_prompt = ", ".join(enhanced_parts)
        return enhanced_prompt
    
    def generate_image(self, prompt: str, context: str = "", size: str = "512x512", 
                      quality: str = "standard", style: str = "educational",
                      subject: str = "General Science") -> Dict[str, Any]:
        """Generate image using Pollinations.ai API"""
        try:
            # Check if the prompt is related to the selected subject
            if subject and subject != "General Science":
                if not self._is_related_to_subject(prompt, subject):
                    detected_subject = self._detect_subject(prompt)
                    return {
                        "success": False,
                        "error": f"subject_mismatch",
                        "message": f"Your image request appears to be about {detected_subject}, but you have {subject} selected. Please change your subject selection to {detected_subject} to generate this image.",
                        "detected_subject": detected_subject,
                        "selected_subject": subject
                    }
            
            # Enhance the prompt with subject context
            if subject and subject != "General Science":
                prompt = f"{prompt}, {subject} educational illustration"
            
            # Enhance the prompt
            enhanced_prompt = self._enhance_prompt(prompt, context, style)
            
            # URL encode the prompt
            encoded_prompt = urllib.parse.quote(enhanced_prompt)
            
            # Parse size
            try:
                width, height = size.split('x')
                width = int(width)
                height = int(height)
            except:
                width, height = 512, 512
            
            # Build the image URL with parameters
            image_url = f"{self.base_url}{encoded_prompt}?width={width}&height={height}&nologo=true"
            
            logger.info(f"Generated Pollinations image URL for prompt: {prompt[:50]}...")
            
            return {
                "success": True,
                "image_url": image_url,
                "enhanced_prompt": enhanced_prompt,
                "revised_prompt": enhanced_prompt,
                "model": "pollinations-ai",
                "size": size
            }
            
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
            # Create educational prompt based on subject
            subject_styles = {
                "Physics": "physics diagram showing forces, motion, or energy concepts",
                "Chemistry": "chemistry diagram showing molecular structures, reactions, or bonds",
                "Mathematics": "mathematical visualization showing graphs, geometry, or equations",
                "Biology": "biology diagram showing cells, organisms, or biological processes",
                "Computer Science": "computer science diagram showing algorithms, data structures, or system architecture"
            }
            
            subject_style = subject_styles.get(subject, "educational diagram")
            
            prompt = f"{concept}, {subject_style}, {difficulty} level explanation, labeled diagram, educational illustration"
            
            return self.generate_image(
                prompt=prompt,
                context=f"Educational {subject} content for {difficulty} level students",
                style="diagram"
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
            # Extract key concepts from problem
            prompt = f"Illustration for: {problem_text[:200]}, {subject} problem visualization, educational, clear diagram"
            
            return self.generate_image(
                prompt=prompt,
                context=f"STEM problem illustration for {subject}",
                style="educational"
            )
            
        except Exception as e:
            logger.error(f"Error generating problem illustration: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_training_stats(self) -> Dict[str, Any]:
        """Get service statistics"""
        return {
            "service": "Pollinations.ai",
            "status": "active",
            "model": "pollinations-ai",
            "features": ["text-to-image", "educational-diagrams", "problem-illustrations"]
        }
    
    def create_fine_tuning_dataset(self) -> Dict[str, Any]:
        """Not applicable for Pollinations API"""
        return {
            "success": False,
            "message": "Fine-tuning not available with Pollinations.ai API"
        }
