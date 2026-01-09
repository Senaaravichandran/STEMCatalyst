import os
import logging
import requests
import json
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class NvidiaLlamaService:
    """NVIDIA Llama 4 Scout service for STEM problem solving and concept explanation"""
    
    def __init__(self):
        # Load API key from environment variable
        self.api_key = os.getenv('NVIDIA_API_KEY')
        if not self.api_key:
            logger.warning("NVIDIA_API_KEY not found in environment variables")
            raise ValueError("NVIDIA_API_KEY environment variable is required")
        
        self.invoke_url = os.getenv('NVIDIA_API_URL', 'https://integrate.api.nvidia.com/v1/chat/completions')
        self.model = "meta/llama-4-scout-17b-16e-instruct"
        logger.info("NVIDIA Llama service initialized with API key from environment")
    
    def _make_request(self, messages: list, max_tokens: int = 4000, 
                     temperature: float = 0.7, stream: bool = False) -> str:
        """Make request to NVIDIA API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream" if stream else "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 1.00,
            "frequency_penalty": 0.00,
            "presence_penalty": 0.00,
            "stream": stream
        }
        
        try:
            response = requests.post(self.invoke_url, headers=headers, json=payload, timeout=120)
            
            if stream:
                # Handle streaming response
                full_content = ""
                for line in response.iter_lines():
                    if line:
                        line_text = line.decode("utf-8")
                        if line_text.startswith("data: "):
                            data_str = line_text[6:]
                            if data_str.strip() == "[DONE]":
                                break
                            try:
                                data = json.loads(data_str)
                                if "choices" in data and len(data["choices"]) > 0:
                                    delta = data["choices"][0].get("delta", {})
                                    content = delta.get("content", "")
                                    full_content += content
                            except json.JSONDecodeError:
                                continue
                return full_content
            else:
                # Handle non-streaming response
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
                
        except requests.exceptions.RequestException as e:
            logger.error(f"NVIDIA API request failed: {str(e)}")
            raise Exception(f"NVIDIA API request failed: {str(e)}")
    
    def solve_problem(self, problem: str, subject: str, difficulty: str,
                     show_steps: bool = True, include_theory: bool = True,
                     include_diagrams: bool = True, temperature: float = 0.7) -> Dict[str, Any]:
        """Solve a STEM problem using NVIDIA Llama"""
        
        system_message = f"""You are a world-class {subject} professor with decades of teaching experience. 
You excel at breaking down complex problems into understandable steps and explaining concepts clearly 
to students at all levels from beginner to graduate level. Your teaching style is patient, thorough, 
and always focused on helping students truly understand both the solution process and underlying principles.

CRITICAL INSTRUCTION - SUBJECT RESTRICTION:
You MUST ONLY answer questions related to {subject}. 
- If the user asks about a topic outside of {subject}, politely decline and say: "I'm currently set to help with {subject} questions only. Please change the subject selector if you'd like help with a different topic."
- Do NOT provide answers, hints, or information about other subjects like {'Mathematics, Physics, Chemistry, or General Science' if subject == 'Biology' else 'Biology, Physics, Chemistry, or General Science' if subject == 'Mathematics' else 'Biology, Mathematics, Chemistry, or General Science' if subject == 'Physics' else 'Biology, Mathematics, Physics, or General Science' if subject == 'Chemistry' else 'Biology, Mathematics, Physics, or Chemistry'}.
- Stay strictly within the domain of {subject}."""

        user_prompt = f"""You are an expert STEM educator and problem solver specializing ONLY in {subject}. 

IMPORTANT: You must ONLY answer questions about {subject}. If this question is not related to {subject}, politely decline and ask the user to change their subject selection.

PROBLEM/QUESTION:
{problem}

CONTEXT:
- Subject: {subject} (ONLY answer if the question is about {subject})
- Difficulty Level: {difficulty}
- Student needs: {"Step-by-step breakdown" if show_steps else "Direct solution"}
- Theory requirement: {"Include underlying concepts" if include_theory else "Focus on solution only"}
- Visual aids: {"Suggest diagrams/graphs" if include_diagrams else "Text-based solution"}

FIRST: Determine if this question is about {subject}. If NOT, respond with:
"This question appears to be about [detected subject], but I'm currently set to help with {subject} only. Please select the appropriate subject from the options panel to get help with this topic."

IF THE QUESTION IS ABOUT {subject.upper()}, THEN PROVIDE:
1. **Problem Analysis**: Briefly identify the key concepts and approach needed
2. **Solution Strategy**: {"Provide detailed step-by-step breakdown" if show_steps else "Present the solution clearly"}
3. **Mathematical Work**: Show all calculations with proper notation
4. **Conceptual Explanation**: {"Explain underlying theories and principles" if include_theory else "Focus on the problem-solving process"}
5. **Key Insights**: Summarize the most important takeaways
6. **Practice Direction**: Suggest related problems or concepts to explore

FORMAT:
- Use clear markdown formatting with proper headers
- Include mathematical expressions where applicable
- Organize content with bullet points and numbered lists for clarity
- Make explanations appropriate for {difficulty} level

Please provide a comprehensive solution that helps the student both solve this specific problem and understand the underlying concepts."""

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            logger.info(f"Solving problem with NVIDIA Llama: {problem[:50]}...")
            solution = self._make_request(messages, temperature=temperature)
            
            return {
                "solution": solution,
                "model_used": "NVIDIA Llama 4 Scout",
                "model_version": self.model,
                "success": True,
                "confidence": "high",
                "processing_time": 0,
                "metadata": {
                    "subject": subject,
                    "difficulty": difficulty,
                    "temperature": temperature,
                    "timestamp": None
                }
            }
        except Exception as e:
            logger.error(f"Error solving problem with NVIDIA Llama: {str(e)}")
            raise
    
    def explain_concept(self, concept: str, subject: str = "General", 
                       level: str = "intermediate", include_examples: bool = True,
                       include_history: bool = False, temperature: float = 0.7) -> str:
        """Explain a concept using NVIDIA Llama"""
        
        system_message = f"""You are an expert {subject} educator with a gift for explaining complex concepts 
in simple, understandable terms. You adapt your explanations to the student's level and always provide 
clear, engaging content that promotes deep understanding.

CRITICAL INSTRUCTION - SUBJECT RESTRICTION:
You MUST ONLY explain concepts related to {subject}. 
- If the user asks about a concept outside of {subject}, politely decline and say: "I'm currently set to help with {subject} concepts only. Please change the subject selector if you'd like to learn about a different topic."
- Do NOT provide explanations about other subjects.
- Stay strictly within the domain of {subject}."""

        user_prompt = f"""Please explain the concept of '{concept}' - but ONLY if it relates to {subject}.

IMPORTANT: You must ONLY explain concepts about {subject}. If '{concept}' is not related to {subject}, politely decline and ask the user to change their subject selection.

FIRST: Determine if '{concept}' is a {subject} concept. If NOT, respond with:
"The concept '{concept}' appears to be related to [detected subject], but I'm currently set to help with {subject} only. Please select the appropriate subject from the options panel to learn about this topic."

IF THE CONCEPT IS ABOUT {subject.upper()}, PROVIDE:

REQUIREMENTS:
- Level: {level} (adjust complexity accordingly)
- {"Include practical, real-world examples" if include_examples else "Focus on the theoretical explanation"}
- {"Include historical context and development of this concept" if include_history else "Focus on current understanding"}

STRUCTURE YOUR RESPONSE WITH:
1. **Introduction**: What is this concept and why is it important?
2. **Core Explanation**: The main principles and mechanics
3. **Key Points**: Bullet points of the most important aspects
{"4. **Examples**: Practical applications and examples" if include_examples else ""}
{"5. **Historical Context**: How this concept developed" if include_history else ""}
6. **Summary**: A brief recap of the main points
7. **Further Learning**: Related concepts to explore

Use clear markdown formatting and make the explanation engaging and educational."""

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            logger.info(f"Explaining concept with NVIDIA Llama: {concept}")
            explanation = self._make_request(messages, temperature=temperature, max_tokens=3000)
            return explanation
        except Exception as e:
            logger.error(f"Error explaining concept with NVIDIA Llama: {str(e)}")
            raise
    
    def get_study_tips(self, subject: str, learning_style: str = "Visual",
                      study_goal: str = "General Understanding", 
                      challenges: list = None, temperature: float = 0.7) -> str:
        """Get personalized study tips using NVIDIA Llama"""
        
        challenges_text = ", ".join(challenges) if challenges else "general learning"
        
        system_message = """You are an expert learning coach and educational psychologist who specializes 
in helping students develop effective study strategies tailored to their individual needs and learning styles."""

        user_prompt = f"""Please provide personalized study tips for a student with these characteristics:

STUDENT PROFILE:
- Subject: {subject}
- Learning Style: {learning_style}
- Study Goal: {study_goal}
- Challenges: {challenges_text}

Provide comprehensive, actionable study tips that include:
1. **Study Strategies**: Specific techniques suited to their learning style
2. **Time Management**: How to structure study sessions
3. **Resource Recommendations**: Types of resources that work best
4. **Practice Methods**: Effective ways to practice and retain information
5. **Overcoming Challenges**: Specific advice for their stated challenges
6. **Motivation Tips**: How to stay motivated and engaged

Make the tips practical, specific, and easy to implement."""

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            logger.info(f"Getting study tips with NVIDIA Llama for {subject}")
            tips = self._make_request(messages, temperature=temperature, max_tokens=2000)
            return tips
        except Exception as e:
            logger.error(f"Error getting study tips with NVIDIA Llama: {str(e)}")
            raise
    
    def health_check(self) -> Dict[str, Any]:
        """Check if NVIDIA Llama service is available"""
        try:
            messages = [{"role": "user", "content": "Hello"}]
            response = self._make_request(messages, max_tokens=10, temperature=0.1)
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
