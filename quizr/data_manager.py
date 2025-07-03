"""
Data management for QUIZR - handles loading quizzes and progress tracking
"""

import os
import yaml
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

from .models import Question, Quiz, QuestionProgress, GlobalProgress
from .config import Config


class DataManager:
    """Manages loading and saving quiz data and progress"""
    
    def __init__(self, config: Config):
        """Initialize data manager
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.progress_data: Dict[str, Any] = {}
        self.global_progress: GlobalProgress = GlobalProgress()
        self._load_progress()
    
    def discover_quizzes(self) -> Dict[str, List[str]]:
        """Discover all quiz files in the directory structure
        
        Returns:
            Dict mapping folder paths to lists of quiz filenames
        """
        quizzes = {}
        exercises_path = Path(self.config.get_exercises_dir())
        
        # Walk through all directories starting from exercises directory
        for root, dirs, files in os.walk(exercises_path):
            # Skip the images directory if it somehow got nested in exercises
            if 'images' in Path(root).parts:
                continue
                
            yaml_files = [f for f in files if f.endswith('.yaml') and f != 'progress.yaml']
            
            if yaml_files:
                # Get path relative to exercises directory
                rel_path = os.path.relpath(root, exercises_path)
                if rel_path == '.':
                    rel_path = 'root'
                else:
                    # Convert Windows path separators to forward slashes
                    rel_path = rel_path.replace('\\', '/')
                quizzes[rel_path] = yaml_files
        
        return quizzes
    
    def load_quiz(self, filepath: str) -> Optional[Quiz]:
        """Load a single quiz from a YAML file
        
        Args:
            filepath: Path to the YAML file relative to exercises directory
            
        Returns:
            Quiz object or None if loading fails
        """
        try:
            # Normalize path separators
            filepath = filepath.replace('\\', '/')
            
            # Split into parts and reconstruct path
            parts = filepath.split('/')
            full_path = os.path.join(self.config.get_exercises_dir(), *parts)
            
            with open(full_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            if not data:
                return None
                
            questions = {}
            for question_id, question_data in data.items():
                if not isinstance(question_data, dict):
                    continue
                    
                questions[question_id] = Question(
                    id=question_id,
                    prompt=question_data.get('prompt', ''),
                    answer=question_data.get('answer', ''),
                    image=question_data.get('image'),
                    strict=question_data.get('strict', False)
                )
            
            quiz_name = os.path.splitext(os.path.basename(filepath))[0]
            return Quiz(name=quiz_name, filepath=filepath, questions=questions)
            
        except Exception as e:
            print(f"Error loading quiz from {filepath}: {e}")
            return None
    
    def find_quizzes_by_path(self, target_name: str) -> List[str]:
        """Find quiz files by exact name match
        
        This method has two modes of operation:
        1. Exact file name match (without .yaml extension)
        2. Exact folder name match
        
        If both a file and folder have the same name, raises an error.
        If no match is found, returns an empty list.
        
        Args:
            target_name: The exact name of the quiz file or folder to find
            
        Returns:
            List of matching quiz file paths
        
        Raises:
            ValueError: If both a file and folder match the target name
        """
        # Normalize path separators and remove .yaml if present
        target_name = target_name.replace('\\', '/').rstrip('.yaml')
        if target_name.endswith('.yaml'):
            target_name = target_name[:-5]
            
        all_quizzes = self.discover_quizzes()
        matching_files = []
        
        # First check for exact folder match
        folder_match = None
        for folder_path in all_quizzes:
            folder_name = os.path.basename(folder_path)  # Get last part of path
            if folder_name == target_name:
                folder_match = folder_path
                # Add all quiz files from this folder
                for quiz_file in all_quizzes[folder_path]:
                    matching_files.append(os.path.join(folder_path, quiz_file))
        
        # Then check for exact file match (without .yaml extension)
        file_match = None
        for folder_path, quiz_files in all_quizzes.items():
            for quiz_file in quiz_files:
                quiz_name = os.path.splitext(quiz_file)[0]  # Remove .yaml extension
                if quiz_name == target_name:
                    file_match = os.path.join(folder_path, quiz_file)
                    matching_files = [file_match]  # Replace any folder matches
                    break
            if file_match:
                break
        
        # If both a file and folder match, raise an error
        if folder_match and file_match:
            raise ValueError(f"Ambiguous target '{target_name}' matches both a folder and a file")
        
        return matching_files
    
    def get_question_progress(self, quiz_filepath: str, question_id: str) -> QuestionProgress:
        """Get progress for a specific question
        
        Args:
            quiz_filepath: Path to the quiz file
            question_id: ID of the question
            
        Returns:
            QuestionProgress object
        """
        # Navigate to the question progress in the nested structure
        parts = quiz_filepath.replace('\\', '/').split('/')
        current = self.progress_data
        
        # Navigate through folder structure
        for part in parts[:-1]:  # All but the filename
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Get the filename without extension
        filename = parts[-1]
        if filename not in current:
            current[filename] = {}
        
        if question_id not in current[filename]:
            current[filename][question_id] = {}
        
        progress_dict = current[filename][question_id]
        return QuestionProgress(
            attempts=progress_dict.get('attempts', 0),
            correct=progress_dict.get('correct', 0),
            last_review=progress_dict.get('last_review'),
            last_correct=progress_dict.get('last_correct')
        )
    
    def update_question_progress(self, quiz_filepath: str, question_id: str, progress: QuestionProgress) -> None:
        """Update progress for a specific question
        
        Args:
            quiz_filepath: Path to the quiz file
            question_id: ID of the question
            progress: Updated progress object
        """
        # Navigate to the question progress in the nested structure
        parts = quiz_filepath.replace('\\', '/').split('/')
        current = self.progress_data
        
        # Navigate through folder structure
        for part in parts[:-1]:  # All but the filename
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Get the filename
        filename = parts[-1]
        if filename not in current:
            current[filename] = {}
        
        if question_id not in current[filename]:
            current[filename][question_id] = {}
        
        current[filename][question_id] = {
            'attempts': progress.attempts,
            'correct': progress.correct,
            'last_review': progress.last_review,
            'last_correct': progress.last_correct
        }
    
    def _load_progress(self) -> None:
        """Load progress data from file"""
        progress_file = self.config.get_progress_file()
        
        if os.path.exists(progress_file):
            try:
                with open(progress_file, 'r', encoding='utf-8') as file:
                    data = yaml.safe_load(file) or {}
                
                # Extract global metadata
                meta = data.get('__meta__', {})
                self.global_progress = GlobalProgress(
                    total_questions_seen=meta.get('total_questions_seen', 0),
                    total_reviews=meta.get('total_reviews', 0),
                    first_use=meta.get('first_use'),
                    last_session=meta.get('last_session'),
                    daily_log=meta.get('daily_log', {})
                )
                
                # Store the rest as progress data
                self.progress_data = {k: v for k, v in data.items() if k != '__meta__'}
                
            except Exception as e:
                print(f"Error loading progress: {e}")
                self.progress_data = {}
                self.global_progress = GlobalProgress()
        else:
            self.progress_data = {}
            self.global_progress = GlobalProgress()
    
    def save_progress(self) -> None:
        """Save progress data to file"""
        progress_file = self.config.get_progress_file()
        
        # Combine global metadata with progress data
        data = {
            '__meta__': {
                'total_questions_seen': self.global_progress.total_questions_seen,
                'total_reviews': self.global_progress.total_reviews,
                'first_use': self.global_progress.first_use,
                'last_session': self.global_progress.last_session,
                'daily_log': self.global_progress.daily_log
            }
        }
        data.update(self.progress_data)
        
        try:
            with open(progress_file, 'w', encoding='utf-8') as file:
                yaml.dump(data, file, default_flow_style=False, sort_keys=False)
        except Exception as e:
            print(f"Error saving progress: {e}")
    
    def calculate_folder_stats(self, folder_path: str) -> Dict[str, Any]:
        """Calculate statistics for a folder
        
        Args:
            folder_path: Path to the folder
            
        Returns:
            Dictionary with folder statistics
        """
        quiz_files = self.find_quizzes_by_path(folder_path)
        
        total_questions = 0
        questions_seen = 0
        correct_answers = 0
        total_attempts = 0
        
        for quiz_file in quiz_files:
            quiz = self.load_quiz(quiz_file)
            if not quiz:
                continue
                
            for question_id in quiz.questions:
                progress = self.get_question_progress(quiz_file, question_id)
                total_questions += 1
                
                if progress.attempts > 0:
                    questions_seen += 1
                    total_attempts += progress.attempts
                    correct_answers += progress.correct
        
        return {
            'total_questions': total_questions,
            'questions_seen': questions_seen,
            'correct_answers': correct_answers,
            'total_attempts': total_attempts,
            'completion_rate': (questions_seen / total_questions * 100) if total_questions > 0 else 0,
            'accuracy_rate': (correct_answers / total_attempts * 100) if total_attempts > 0 else 0
        } 