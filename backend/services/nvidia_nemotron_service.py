import os
import logging
from openai import OpenAI  # type: ignore
from typing import Dict, Any

logger = logging.getLogger(__name__)

class NvidiaNemotronService:
    """NVIDIA Nemotron Nano 9B v2 service for Study Tips and Formula Reference"""
    
    def __init__(self):
        # Load API key from environment variable
        self.api_key = os.getenv('NVIDIA_API_KEY')
        if not self.api_key:
            logger.warning("NVIDIA_API_KEY not found in environment variables")
            raise ValueError("NVIDIA_API_KEY environment variable is required")
        
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=self.api_key
        )
        self.model = "nvidia/nvidia-nemotron-nano-9b-v2"
        logger.info("NVIDIA Nemotron Nano 9B v2 service initialized")
    
    def _make_request(self, messages: list, temperature: float = 0.6, 
                     max_tokens: int = 2048, use_thinking: bool = True) -> str:
        """Make request to NVIDIA Nemotron API"""
        try:
            extra_body = {}
            if use_thinking:
                extra_body = {
                    "min_thinking_tokens": 512,
                    "max_thinking_tokens": 1024
                }
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                top_p=0.95,
                max_tokens=max_tokens,
                frequency_penalty=0,
                presence_penalty=0,
                stream=True,
                extra_body=extra_body if use_thinking else None
            )
            
            full_content = ""
            for chunk in completion:
                # Get reasoning content if available
                reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
                if reasoning:
                    # We can log reasoning but not include in response
                    logger.debug(f"Reasoning: {reasoning}")
                
                # Get actual content
                if chunk.choices[0].delta.content is not None:
                    full_content += chunk.choices[0].delta.content
            
            return full_content
                
        except Exception as e:
            logger.error(f"NVIDIA Nemotron API request failed: {str(e)}")
            raise Exception(f"NVIDIA Nemotron API request failed: {str(e)}")
    
    def get_formulas(self, subject: str, topic: str = "", search_term: str = "",
                    temperature: float = 0.3) -> str:
        """Get formulas for a subject/topic using Nemotron"""
        
        system_message = f"""You are an expert {subject} educator specializing in formulas, equations, and mathematical expressions.
Your role is to provide comprehensive, well-organized formula references that help students understand and apply key equations.

Focus on providing:
1. Clear formula notation with proper mathematical symbols
2. Variable definitions and units
3. When and how to use each formula
4. Common variations and special cases"""

        user_prompt = f"""Please provide a comprehensive formula reference for {subject}"""
        if topic:
            user_prompt += f", specifically focusing on {topic}"
        if search_term:
            user_prompt += f", with emphasis on formulas related to '{search_term}'"
        
        user_prompt += """.

For each formula, please include:
1. **Formula Name**: Clear title
2. **Formula**: The mathematical expression with proper notation
3. **Variables**: Define each variable with units
4. **Application**: When to use this formula
5. **Example**: A brief example of how to apply it

Use clear markdown formatting with proper headers and organize formulas logically.
Include at least 5-8 relevant formulas for this topic."""

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            logger.info(f"Getting formulas with Nemotron for {subject} - {topic}")
            formulas = self._make_request(messages, temperature=temperature, max_tokens=3000)
            return formulas
        except Exception as e:
            logger.error(f"Error getting formulas with Nemotron: {str(e)}")
            raise
    
    def get_study_tips(self, subject: str, learning_style: str = "Visual",
                      study_goal: str = "General Understanding", 
                      challenges: list = None, temperature: float = 0.6) -> str:
        """Get personalized study tips using Nemotron"""
        
        challenges_text = ", ".join(challenges) if challenges else "general learning"
        
        system_message = """You are an expert learning coach and educational psychologist who specializes 
in helping students develop effective study strategies tailored to their individual needs and learning styles.

You have deep knowledge of:
- Cognitive science and memory techniques
- Different learning styles (Visual, Auditory, Reading/Writing, Kinesthetic)
- Time management and productivity strategies
- Test preparation and anxiety management
- Subject-specific study approaches"""

        user_prompt = f"""Please provide personalized study tips for a student with these characteristics:

STUDENT PROFILE:
- Subject: {subject}
- Learning Style: {learning_style}
- Study Goal: {study_goal}
- Challenges: {challenges_text}

Provide comprehensive, actionable study tips that include:

1. **Study Strategies**: Specific techniques suited to their {learning_style} learning style for {subject}
2. **Time Management**: How to structure study sessions effectively
3. **Resource Recommendations**: Types of resources that work best for this learning style
4. **Practice Methods**: Effective ways to practice and retain {subject} information
5. **Overcoming Challenges**: Specific advice for: {challenges_text}
6. **Motivation Tips**: How to stay motivated and engaged
7. **Memory Techniques**: Specific memorization strategies for {subject}
8. **Study Schedule**: A suggested weekly study plan

Make the tips practical, specific to {subject}, and easy to implement.
Use clear markdown formatting with headers and bullet points."""

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            logger.info(f"Getting study tips with Nemotron for {subject} - {learning_style}")
            tips = self._make_request(messages, temperature=temperature, max_tokens=3000)
            return tips
        except Exception as e:
            logger.error(f"Error getting study tips with Nemotron: {str(e)}")
            raise
    
    def health_check(self) -> Dict[str, Any]:
        """Check if Nemotron service is available"""
        try:
            messages = [{"role": "user", "content": "Hello"}]
            response = self._make_request(messages, max_tokens=10, temperature=0.1, use_thinking=False)
            return {
                "available": True,
                "model": self.model,
                "error": None
            }
        except Exception as e:
            return {
                "available": False,
                "model": self.model,
                "error": str(e)
            }
