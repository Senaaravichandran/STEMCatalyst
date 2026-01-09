import os
import json
import pandas as pd
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class DataService:
    """Service for managing and loading data from the /data folder"""
    
    def __init__(self, data_path: str = "../data"):
        self.data_path = data_path
        self.loaded_data = {}
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all available data files on initialization"""
        try:
            if not os.path.exists(self.data_path):
                logger.warning(f"Data path {self.data_path} does not exist")
                return
            
            # Load math data
            math_path = os.path.join(self.data_path, "maths")
            if os.path.exists(math_path):
                self._load_math_data(math_path)
            
            # Load science data
            science_path = os.path.join(self.data_path, "science")
            if os.path.exists(science_path):
                self._load_science_data(science_path)
                
            logger.info(f"Loaded data from {len(self.loaded_data)} sources")
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
    
    def _load_math_data(self, math_path: str):
        """Load mathematics data files"""
        try:
            # Load JSONL files
            jsonl_files = ['train.jsonl', 'test.jsonl', 'train_socratic.jsonl', 'test_socratic.jsonl', 'example_model_solutions.jsonl']
            
            for file in jsonl_files:
                file_path = os.path.join(math_path, file)
                if os.path.exists(file_path):
                    data = self._load_jsonl(file_path)
                    self.loaded_data[f"math_{file.replace('.jsonl', '')}"] = data
                    logger.info(f"Loaded {len(data)} entries from {file}")
                    
        except Exception as e:
            logger.error(f"Error loading math data: {str(e)}")
    
    def _load_science_data(self, science_path: str):
        """Load science data files"""
        try:
            # Load captions.json
            captions_path = os.path.join(science_path, "data", "captions.json")
            if os.path.exists(captions_path):
                with open(captions_path, 'r', encoding='utf-8') as f:
                    self.loaded_data["science_captions"] = json.load(f)
                    logger.info("Loaded science captions data")
            
            # Load ScienceQA data
            scienceqa_path = os.path.join(science_path, "data", "scienceqa")
            if os.path.exists(scienceqa_path):
                self._load_scienceqa_data(scienceqa_path)
                
        except Exception as e:
            logger.error(f"Error loading science data: {str(e)}")
    
    def _load_scienceqa_data(self, scienceqa_path: str):
        """Load ScienceQA dataset"""
        try:
            problems_path = os.path.join(scienceqa_path, "problems.json")
            splits_path = os.path.join(scienceqa_path, "pid_splits.json")
            
            if os.path.exists(problems_path):
                with open(problems_path, 'r', encoding='utf-8') as f:
                    self.loaded_data["scienceqa_problems"] = json.load(f)
                    logger.info("Loaded ScienceQA problems data")
            
            if os.path.exists(splits_path):
                with open(splits_path, 'r', encoding='utf-8') as f:
                    self.loaded_data["scienceqa_splits"] = json.load(f)
                    logger.info("Loaded ScienceQA splits data")
                    
        except Exception as e:
            logger.error(f"Error loading ScienceQA data: {str(e)}")
    
    def _load_jsonl(self, file_path: str) -> List[Dict]:
        """Load JSONL file"""
        data = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        data.append(json.loads(line))
        except Exception as e:
            logger.error(f"Error loading JSONL file {file_path}: {str(e)}")
        return data
    
    def get_data(self, data_key: str) -> Optional[Any]:
        """Get loaded data by key"""
        return self.loaded_data.get(data_key)
    
    def get_available_datasets(self) -> List[str]:
        """Get list of available dataset keys"""
        return list(self.loaded_data.keys())
    
    def search_problems(
        self,
        subject: str,
        difficulty: Optional[str] = None,
        topic: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        Search for relevant problems based on criteria
        
        Args:
            subject: Subject area to search
            difficulty: Optional difficulty filter
            topic: Optional topic filter
            limit: Maximum number of results
            
        Returns:
            List of matching problems
        """
        results = []
        
        try:
            # Search in math data
            if subject.lower() in ['math', 'mathematics']:
                for key in self.loaded_data:
                    if key.startswith('math_'):
                        data = self.loaded_data[key]
                        for item in data[:limit]:
                            if self._matches_criteria(item, difficulty, topic):
                                results.append({
                                    'source': key,
                                    'problem': item.get('problem', ''),
                                    'solution': item.get('solution', ''),
                                    'subject': 'Mathematics'
                                })
            
            # Search in science data
            elif subject.lower() in ['science', 'physics', 'chemistry', 'biology']:
                if 'scienceqa_problems' in self.loaded_data:
                    problems = self.loaded_data['scienceqa_problems']
                    count = 0
                    for pid, problem in problems.items():
                        if count >= limit:
                            break
                        if self._matches_science_criteria(problem, subject, difficulty, topic):
                            results.append({
                                'source': 'scienceqa',
                                'problem': problem.get('question', ''),
                                'solution': problem.get('solution', ''),
                                'subject': problem.get('subject', subject),
                                'topic': problem.get('topic', ''),
                                'difficulty': problem.get('grade', '')
                            })
                            count += 1
            
        except Exception as e:
            logger.error(f"Error searching problems: {str(e)}")
        
        return results
    
    def _matches_criteria(self, item: Dict, difficulty: Optional[str], topic: Optional[str]) -> bool:
        """Check if item matches search criteria"""
        # Simple matching logic - can be enhanced
        if difficulty and difficulty.lower() not in str(item).lower():
            return False
        if topic and topic.lower() not in str(item).lower():
            return False
        return True
    
    def _matches_science_criteria(
        self,
        problem: Dict,
        subject: str,
        difficulty: Optional[str],
        topic: Optional[str]
    ) -> bool:
        """Check if science problem matches criteria"""
        problem_subject = problem.get('subject', '').lower()
        problem_topic = problem.get('topic', '').lower()
        problem_grade = str(problem.get('grade', '')).lower()
        
        # Subject matching
        if subject.lower() not in problem_subject and subject.lower() != 'science':
            return False
        
        # Difficulty matching (map grade to difficulty)
        if difficulty:
            diff_map = {
                'beginner': ['1', '2', '3', '4', '5'],
                'intermediate': ['6', '7', '8', '9'],
                'advanced': ['10', '11', '12'],
                'university': ['college', 'university']
            }
            if difficulty.lower() in diff_map:
                if not any(grade in problem_grade for grade in diff_map[difficulty.lower()]):
                    return False
        
        # Topic matching
        if topic and topic.lower() not in problem_topic:
            return False
        
        return True
    
    def get_context_for_problem(self, problem: str, subject: str) -> str:
        """
        Get relevant context from loaded data for enhanced problem solving
        
        Args:
            problem: The problem statement
            subject: Subject area
            
        Returns:
            Relevant context string
        """
        context_parts = []
        
        try:
            # Find similar problems
            similar_problems = self.search_problems(subject, limit=3)
            
            if similar_problems:
                context_parts.append("Similar problems and solutions for reference:")
                for i, prob in enumerate(similar_problems[:2], 1):
                    context_parts.append(f"\nExample {i}:")
                    context_parts.append(f"Problem: {prob['problem'][:200]}...")
                    context_parts.append(f"Solution approach: {prob['solution'][:300]}...")
            
            # Add subject-specific context
            if subject.lower() in ['physics', 'chemistry', 'biology']:
                if 'science_captions' in self.loaded_data:
                    context_parts.append("\nRelevant scientific concepts and terminology available for reference.")
            
        except Exception as e:
            logger.error(f"Error getting context: {str(e)}")
        
        return "\n".join(context_parts)
