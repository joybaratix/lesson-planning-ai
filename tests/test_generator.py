import unittest
import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from lesson_generator import LessonPlanGenerator

class TestLessonGenerator(unittest.TestCase):
    
    def setUp(self):
        self.generator = LessonPlanGenerator("microsoft/DialoGPT-small")
    
    def test_prompt_creation(self):
        """Test prompt creation with different inputs"""
        prompt = self.generator.create_prompt("Test Topic", "Science", "Intermediate")
        
        self.assertIn("Test Topic", prompt)
        self.assertIn("Science", prompt)
        self.assertIn("Intermediate", prompt)
        self.assertIn("JSON format", prompt)
    
    def test_lesson_plan_structure(self):
        """Test that lesson plan has required structure"""
        result = self.generator.generate_lesson_plan("Algebra", "Mathematics", "Basic")
        
        required_keys = [
            "Topic_Name", "Learning_Objectives", "required_resources",
            "Teaching_Methods", "Duration", "Activities_Exercises",
            "Assessment_Methods", "Prerequisites", "Keywords"
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
    
    def test_different_grade_levels(self):
        """Test generation with different grade levels"""
        grade_levels = ["Basic", "Intermediate", "Advanced"]
        
        for level in grade_levels:
            result = self.generator.generate_lesson_plan("Test", "Science", level)
            self.assertIsInstance(result, dict)
            self.assertIn("Topic_Name", result)

if __name__ == '__main__':
    unittest.main()
    