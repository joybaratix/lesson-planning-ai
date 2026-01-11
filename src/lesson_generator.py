import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import re

class LessonPlanGenerator:
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
    
    def create_prompt(self, input_text: str, subject: str, grade_level: str) -> str:
        """Create prompt for lesson plan generation"""
        
        prompt = f"""
        Create a comprehensive lesson plan based on the following information:
        
        TOPIC: {input_text}
        SUBJECT: {subject}
        GRADE LEVEL: {grade_level}
        
        Generate a lesson plan with the following structure in JSON format:
        
        {{
            "Topic_Name": "appropriate topic name",
            "Learning_Objectives": ["list 3-4 specific learning objectives"],
            "required_resources": ["list required teaching resources"],
            "Teaching_Methods": ["list appropriate teaching methods"],
            "Duration": {{
                "Week_1": "topic and time allocation",
                "Week_2": "topic and time allocation", 
                "Week_3": "topic and time allocation",
                "Week_4": "topic and time allocation"
            }},
            "Activities_Exercises": ["list interactive activities and exercises"],
            "Assessment_Methods": ["list assessment strategies"],
            "Prerequisites": ["list necessary prerequisites"],
            "Keywords": ["list relevant keywords"]
        }}
        
        Instructions:
        - Make learning objectives clear and measurable
        - Include practical resources like Whiteboard, Projector, Lab equipment
        - Use diverse teaching methods appropriate for {grade_level} level
        - Include interactive activities like Q&A, quizzes, group work
        - Ensure duration is realistic and well-distributed
        
        Lesson Plan JSON:
        """
        
        return prompt.strip()
    
    def generate_lesson_plan(self, input_text: str, subject: str, grade_level: str) -> dict:
        """Generate structured lesson plan"""
        prompt = self.create_prompt(input_text, subject, grade_level)
        
        inputs = self.tokenizer.encode(prompt, return_tensors='pt').to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=1500,
                temperature=0.8,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                num_return_sequences=1,
                repetition_penalty=1.1
            )
        
        full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        generated_content = full_text[len(prompt):].strip()
        
        # Try to extract JSON from generated content
        try:
            json_match = re.search(r'\{.*\}', generated_content, re.DOTALL)
            if json_match:
                lesson_plan = json.loads(json_match.group())
                return lesson_plan
            else:
                return self._create_fallback_plan(input_text, subject, grade_level)
        except json.JSONDecodeError:
            return self._create_fallback_plan(input_text, subject, grade_level)
    
    def _create_fallback_plan(self, input_text: str, subject: str, grade_level: str) -> dict:
        """Create a fallback lesson plan when JSON parsing fails"""
        return {
            "Topic_Name": input_text,
            "Learning_Objectives": [
                f"Understand basic concepts of {input_text}",
                f"Apply knowledge of {input_text} to solve problems",
                f"Analyze different aspects of {input_text}"
            ],
            "required_resources": ["Whiteboard", "Projector", "Textbooks", "Worksheets"],
            "Teaching_Methods": ["Lecture", "Group Discussion", "Practical Exercises"],
            "Duration": {
                "Week_1": f"Introduction to {input_text} (2 hours)",
                "Week_2": f"Core Concepts (2 hours)",
                "Week_3": f"Advanced Topics (2 hours)",
                "Week_4": f"Review and Assessment (2 hours)"
            },
            "Activities_Exercises": ["Q&A sessions", "Group activities", "Short quizzes"],
            "Assessment_Methods": ["Class participation", "Assignments", "Final test"],
            "Prerequisites": [f"Basic knowledge of {subject}"],
            "Keywords": [input_text.lower(), subject.lower(), grade_level.lower()]
        }

def test_generator():
    """Test the lesson plan generator"""
    generator = LessonPlanGenerator()
    
    test_cases = [
        ("Algebra Basics", "Mathematics", "Basic"),
        ("Chemical Reactions", "Science", "Intermediate"), 
        ("Shakespeare's Macbeth", "English", "Advanced")
    ]
    
    for topic, subject, level in test_cases:
        print(f"\n{'='*50}")
        print(f"Testing: {topic} | {subject} | {level}")
        print(f"{'='*50}")
        
        result = generator.generate_lesson_plan(topic, subject, level)
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_generator()
    