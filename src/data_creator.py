import pandas as pd
import json
from pathlib import Path

def create_sample_dataset():
    """Create sample dataset for training"""
    
    sample_data = [
        # Mathematics examples
        {
            "input_text": "Quadratic Equations",
            "subject": "Mathematics",
            "grade_level": "Intermediate",
            "expected_output": {
                "Topic_Name": "Quadratic Equations",
                "Learning_Objectives": [
                    "Understand the standard form of quadratic equations",
                    "Solve quadratic equations using factorization method",
                    "Apply quadratic formula to find roots",
                    "Analyze discriminant to determine nature of roots"
                ],
                "required_resources": ["Whiteboard", "Markers", "Textbook", "Calculator", "Worksheets"],
                "Teaching_Methods": ["Lecture", "Demonstration", "Group Problem Solving", "Individual Practice"],
                "Duration": {
                    "Week_1": "Introduction to Quadratic Equations (2 hours)",
                    "Week_2": "Factorization Method (2 hours)",
                    "Week_3": "Quadratic Formula (2 hours)",
                    "Week_4": "Applications and Problem Solving (2 hours)"
                },
                "Activities_Exercises": [
                    "Q&A sessions after each concept",
                    "Group problem-solving activities",
                    "Weekly quizzes",
                    "Real-world application problems"
                ],
                "Assessment_Methods": ["Class participation", "Weekly quizzes", "Final test", "Homework assignments"],
                "Prerequisites": ["Basic algebra", "Linear equations"],
                "Keywords": ["quadratic", "equations", "roots", "discriminant", "factorization"]
            }
        },
        {
            "input_text": "Photosynthesis - Process by which plants convert light energy into chemical energy",
            "subject": "Science",
            "grade_level": "Basic",
            "expected_output": {
                "Topic_Name": "Photosynthesis",
                "Learning_Objectives": [
                    "Define photosynthesis and its importance",
                    "Identify the reactants and products of photosynthesis",
                    "Explain the role of chlorophyll and sunlight",
                    "Describe the process of gas exchange in plants"
                ],
                "required_resources": ["Projector", "Plant specimens", "Microscope", "Diagrams", "Science textbook"],
                "Teaching_Methods": ["Lecture", "Laboratory work", "Group discussion", "Multimedia presentation"],
                "Duration": {
                    "Week_1": "Introduction to Photosynthesis (1.5 hours)",
                    "Week_2": "Light and Dark Reactions (1.5 hours)",
                    "Week_3": "Factors affecting Photosynthesis (1.5 hours)",
                    "Week_4": "Experiments and Applications (1.5 hours)"
                },
                "Activities_Exercises": [
                    "Leaf chromatography experiment",
                    "Q&A on process steps",
                    "Diagram labeling exercise",
                    "Group presentation on importance"
                ],
                "Assessment_Methods": ["Lab reports", "Diagram tests", "Concept explanations", "Group projects"],
                "Prerequisites": ["Basic plant biology", "Cell structure"],
                "Keywords": ["photosynthesis", "chlorophyll", "glucose", "oxygen", "carbon dioxide"]
            }
        },
        {
            "input_text": "Comprehensive study of World War II covering causes, major events, key figures, and consequences",
            "subject": "History",
            "grade_level": "Advanced",
            "expected_output": {
                "Topic_Name": "World War II",
                "Learning_Objectives": [
                    "Analyze the causes and triggers of World War II",
                    "Evaluate the major military campaigns and strategies",
                    "Assess the social and economic impact on different nations",
                    "Understand the geopolitical consequences and establishment of UN"
                ],
                "required_resources": ["Projector", "Historical maps", "Documentary videos", "Primary sources", "History textbooks"],
                "Teaching_Methods": ["Lecture", "Documentary analysis", "Group research", "Debate", "Case studies"],
                "Duration": {
                    "Week_1": "Causes and Outbreak (3 hours)",
                    "Week_2": "Major Theaters of War (3 hours)",
                    "Week_3": "Home Front and Social Impact (3 hours)",
                    "Week_4": "Consequences and Legacy (3 hours)"
                },
                "Activities_Exercises": [
                    "Document analysis of primary sources",
                    "Group debates on key decisions",
                    "Timeline creation activity",
                    "Research project on specific aspects"
                ],
                "Assessment_Methods": ["Research papers", "Document analysis", "Presentations", "Final examination"],
                "Prerequisites": ["World History basics", "World War I knowledge"],
                "Keywords": ["world war", "allies", "axis", "holocaust", "united nations"]
            }
        },
        {
            "input_text": "Python Programming Basics",
            "subject": "Computer Science",
            "grade_level": "Intermediate",
            "expected_output": {
                "Topic_Name": "Python Programming",
                "Learning_Objectives": [
                    "Understand Python syntax and basic programming concepts",
                    "Write and execute simple Python programs",
                    "Use conditional statements and loops effectively",
                    "Create functions and handle basic data structures"
                ],
                "required_resources": ["Computers with Python IDE", "Projector", "Coding examples", "Online compiler"],
                "Teaching_Methods": ["Live coding", "Pair programming", "Project-based learning", "Code reviews"],
                "Duration": {
                    "Week_1": "Introduction to Python (2 hours)",
                    "Week_2": "Control Structures (2 hours)",
                    "Week_3": "Functions and Modules (2 hours)",
                    "Week_4": "Data Structures (2 hours)"
                },
                "Activities_Exercises": [
                    "Coding exercises in class",
                    "Mini-projects after each module",
                    "Code debugging sessions",
                    "Pair programming activities"
                ],
                "Assessment_Methods": ["Coding assignments", "Project submissions", "Code reviews", "Practical exams"],
                "Prerequisites": ["Basic computer literacy", "Logical thinking"],
                "Keywords": ["python", "programming", "functions", "loops", "data structures"]
            }
        }
    ]
    
    # Save the dataset
    data_dir = Path('../data')
    data_dir.mkdir(exist_ok=True)
    
    with open(data_dir / 'training_data.json', 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)
    
    # Also create CSV version
    df_data = []
    for item in sample_data:
        df_data.append({
            'input_text': item['input_text'],
            'subject': item['subject'],
            'grade_level': item['grade_level'],
            'expected_output': json.dumps(item['expected_output'], ensure_ascii=False)
        })
    
    df = pd.DataFrame(df_data)
    df.to_csv(data_dir / 'training_data.csv', index=False, encoding='utf-8')
    
    print(f"Created {len(sample_data)} training samples")
    print("Files saved: training_data.json, training_data.csv")

if __name__ == "__main__":
    create_sample_dataset()