"""
Fallback service that provides sample content when AI APIs are unavailable or rate-limited
"""

import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

class FallbackService:
    """Provides fallback content when AI services are unavailable"""
    
    @staticmethod
    def get_sample_formulas(subject: str, topic: str, search_term: str = None) -> Dict[str, Any]:
        """Return sample formulas for testing when API is unavailable"""
        
        sample_formulas = {
            "Physics": {
                "Mechanics": """# Classical Mechanics Formulas

## Newton's Laws
**First Law (Law of Inertia):**
> An object at rest stays at rest, and an object in motion stays in motion at constant velocity, unless acted upon by an external force.

**Second Law:**
> **F = ma**
> - F = Force (Newtons)
> - m = Mass (kg)
> - a = Acceleration (m/s²)

**Third Law:**
> For every action, there is an equal and opposite reaction.

## Kinematic Equations
For constant acceleration:

**Velocity-Time:**
> **v = u + at**
> - v = final velocity
> - u = initial velocity
> - a = acceleration
> - t = time

**Position-Time:**
> **s = ut + ½at²**
> - s = displacement

**Velocity-Position:**
> **v² = u² + 2as**

## Work and Energy
**Work Done:**
> **W = F·d·cos(θ)**
> - W = Work (Joules)
> - F = Force
> - d = distance
> - θ = angle between force and displacement

**Kinetic Energy:**
> **KE = ½mv²**

**Potential Energy (gravitational):**
> **PE = mgh**
> - g = 9.81 m/s² (acceleration due to gravity)
> - h = height

## Momentum
**Linear Momentum:**
> **p = mv**

**Conservation of Momentum:**
> **m₁u₁ + m₂u₂ = m₁v₁ + m₂v₂**
""",
                "Thermodynamics": """# Thermodynamics Formulas

## First Law of Thermodynamics
> **ΔU = Q - W**
> - ΔU = Change in internal energy
> - Q = Heat added to system
> - W = Work done by system

## Ideal Gas Law
> **PV = nRT**
> - P = Pressure
> - V = Volume
> - n = Number of moles
> - R = Gas constant (8.314 J/mol·K)
> - T = Temperature (Kelvin)

## Heat Transfer
**Conduction:**
> **Q = kAΔT/d**
> - k = thermal conductivity
> - A = area
> - ΔT = temperature difference
> - d = thickness

**Heat Capacity:**
> **Q = mcΔT**
> - m = mass
> - c = specific heat capacity
"""
            },
            "Mathematics": {
                "Calculus": """# Calculus Formulas

## Derivatives
**Power Rule:**
> **d/dx(xⁿ) = nxⁿ⁻¹**

**Product Rule:**
> **d/dx(uv) = u'v + uv'**

**Chain Rule:**
> **d/dx(f(g(x))) = f'(g(x))·g'(x)**

## Integrals
**Power Rule:**
> **∫xⁿdx = xⁿ⁺¹/(n+1) + C**

**Integration by Parts:**
> **∫udv = uv - ∫vdu**

## Fundamental Theorem of Calculus
> **∫ₐᵇf'(x)dx = f(b) - f(a)**
""",
                "Algebra": """# Algebra Formulas

## Quadratic Formula
> **x = (-b ± √(b² - 4ac))/2a**

## Factoring
**Difference of Squares:**
> **a² - b² = (a + b)(a - b)**

**Perfect Square:**
> **a² + 2ab + b² = (a + b)²**

## Logarithms
**Properties:**
> **log(ab) = log(a) + log(b)**
> **log(a/b) = log(a) - log(b)**
> **log(aⁿ) = n·log(a)**
"""
            },
            "Chemistry": {
                "Stoichiometry": """# Stoichiometry Formulas

## Mole Calculations
**Number of Moles:**
> **n = m/M**
> - n = number of moles
> - m = mass (g)
> - M = molar mass (g/mol)

**Avogadro's Number:**
> **N = n × Nₐ**
> - N = number of particles
> - Nₐ = 6.022 × 10²³ mol⁻¹

## Gas Laws
**Ideal Gas Law:**
> **PV = nRT**

**Combined Gas Law:**
> **P₁V₁/T₁ = P₂V₂/T₂**

## Concentration
**Molarity:**
> **M = n/V**
> - M = molarity (mol/L)
> - V = volume in liters
"""
            }
        }
        
        # Get the appropriate formulas
        if subject in sample_formulas and topic in sample_formulas[subject]:
            formulas_content = sample_formulas[subject][topic]
        else:
            formulas_content = f"""# {subject} - {topic} Formulas

## Sample Content
This is sample content for {subject} in {topic}.

> **Note:** This is fallback content shown when the AI service is unavailable or rate-limited.

## Common Formulas
Please check back later when the AI service is available for complete formula references.

> **Status:** AI service temporarily unavailable due to rate limiting.
"""
        
        return {
            "success": True,
            "formulas": formulas_content,
            "metadata": {
                "subject": subject,
                "topic": topic,
                "searchTerm": search_term,
                "timestamp": datetime.now().isoformat(),
                "source": "fallback_service",
                "note": "Sample content - AI service unavailable"
            }
        }
    
    @staticmethod
    def get_sample_explanation(concept: str, subject: str, level: str) -> Dict[str, Any]:
        """Return sample concept explanation"""
        
        explanation_content = f"""# Understanding: {concept}

## Overview
This is a sample explanation for the concept of **{concept}** in {subject}.

> **Note:** This is fallback content shown when the AI service is unavailable or rate-limited.

## Key Points
1. **Definition**: {concept} is a fundamental concept in {subject}
2. **Applications**: Used in various practical scenarios
3. **Examples**: Multiple real-world applications exist

## Detailed Explanation
The concept of {concept} plays a crucial role in {subject}. This explanation would normally be generated by our AI service with detailed, personalized content.

## Level: {level}
This explanation is tailored for {level} level understanding.

> **Status:** AI service temporarily unavailable due to rate limiting. Please try again later for a complete AI-generated explanation.
"""
        
        return {
            "success": True,
            "explanation": explanation_content,
            "metadata": {
                "concept": concept,
                "subject": subject,
                "level": level,
                "timestamp": datetime.now().isoformat(),
                "source": "fallback_service",
                "note": "Sample content - AI service unavailable"
            }
        }
    
    @staticmethod
    def get_sample_study_tips(subject: str, learning_style: str, study_goal: str, challenges: list) -> Dict[str, Any]:
        """Return sample study tips"""
        
        tips_content = f"""# Personalized Study Plan for {subject}

## Your Profile
- **Subject**: {subject}
- **Learning Style**: {learning_style}
- **Study Goal**: {study_goal}
- **Challenges**: {', '.join(challenges) if challenges else 'None specified'}

## Study Strategies

### 1. Foundation Building
Start with the fundamentals and build a strong conceptual base in {subject}.

### 2. {learning_style} Learning Approach
Since you're a {learning_style.lower()} learner, focus on:
- Visual aids and diagrams
- Hands-on practice
- Interactive materials

### 3. Goal-Oriented Study
Working towards your goal of "{study_goal}":
- Set weekly milestones
- Track your progress
- Celebrate small wins

## Time Management
- **Pomodoro Technique**: 25-minute focused study sessions
- **Spaced Repetition**: Review materials at increasing intervals
- **Active Recall**: Test yourself regularly

## Challenge Management
{f"Address your specific challenges: {', '.join(challenges)}" if challenges else "Continue building confidence in your studies"}

> **Note:** This is sample content shown when the AI service is unavailable or rate-limited.
> **Status:** AI service temporarily unavailable. Please try again later for personalized AI-generated study tips.
"""
        
        return {
            "success": True,
            "tips": tips_content,
            "metadata": {
                "subject": subject,
                "learningStyle": learning_style,
                "studyGoal": study_goal,
                "challenges": challenges,
                "timestamp": datetime.now().isoformat(),
                "source": "fallback_service",
                "note": "Sample content - AI service unavailable"
            }
        }
    
    @staticmethod
    def get_sample_solution(problem: str, subject: str, difficulty: str) -> Dict[str, Any]:
        """Return sample problem solution"""
        
        solution_content = f"""# Solution: {problem[:100]}{'...' if len(problem) > 100 else ''}

## Problem Analysis
This is a {difficulty.lower()} level {subject} problem.

> **Note:** This is fallback content shown when the AI service is unavailable or rate-limited.

## Solution Approach
1. **Identify**: Key concepts and given information
2. **Plan**: Strategy for solving the problem
3. **Execute**: Step-by-step solution
4. **Verify**: Check the answer

## Step-by-Step Solution

### Step 1: Problem Setup
Analyze the given information and identify what needs to be found.

### Step 2: Apply Concepts
Use relevant formulas and principles from {subject}.

### Step 3: Calculate
Perform the necessary calculations.

### Step 4: Final Answer
Present the solution clearly.

> **Status:** AI service temporarily unavailable due to rate limiting. Please try again later for a complete AI-generated solution.
"""
        
        return {
            "success": True,
            "solution": solution_content,
            "metadata": {
                "problem": problem,
                "subject": subject,
                "difficulty": difficulty,
                "timestamp": datetime.now().isoformat(),
                "source": "fallback_service",
                "note": "Sample content - AI service unavailable"
            }
        }
