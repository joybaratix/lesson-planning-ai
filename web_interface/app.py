import streamlit as st
import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from lesson_generator import LessonPlanGenerator

# Configure page
st.set_page_config(
    page_title="AI Lesson Plan Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"  # This removes sidebar by default
)

# Remove white bars and improve styling
st.markdown("""
<style>
    /* Remove white bars and padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    
    /* Remove sidebar whitespace */
    section[data-testid="stSidebar"] {
        background-color: #1f1f1f;
    }
    
    /* Header styling */
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }
    
    /* Card styling */
    .lesson-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .content-card {
        background: #ffffff;
        padding: 25px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border: 1px solid #e0e0e0;
    }
    
    /* Input styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        padding: 12px;
    }
    
    .stSelectbox>div>div>select {
        border: 2px solid #e0e0e0;
        border-radius: 8px;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(45deg, #1f77b4, #ff7f0e);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: linear-gradient(45deg, #1668a1, #e67300);
        color: white;
    }
    
    /* Success message */
    .success-msg {
        background: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #28a745;
        margin: 15px 0;
    }
    
    /* Remove extra whitespace */
    .css-1d391kg, .css-1y4p8pa {
        padding: 0;
    }
    
    /* Section headers */
    .section-title {
        font-size: 1.5rem;
        color: #1f77b4;
        margin: 20px 0 10px 0;
        font-weight: bold;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generator' not in st.session_state:
    st.session_state.generator = None
if 'lesson_plan' not in st.session_state:
    st.session_state.lesson_plan = None

# HEADER SECTION
st.markdown('<div class="main-header">🎯 AI Lesson Plan Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Create comprehensive lesson plans in seconds using AI</div>', unsafe_allow_html=True)

# MAIN CONTENT - Input Section
st.markdown('<div class="content-card">', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Lesson Information")
    
    input_text = st.text_area(
        "**Topic or Syllabus Description**",
        placeholder="Examples:\n• 'Quadratic Equations'\n• 'Photosynthesis - Process of energy conversion'\n• 'Introduction to Python programming basics'",
        height=120,
        help="Enter your topic, syllabus, or detailed description"
    )
    
    subject = st.selectbox(
        "**Subject Area**",
        ["Mathematics", "Science", "History", "English", "Computer Science", 
         "Physics", "Chemistry", "Biology", "Geography", "Economics", "General"],
        help="Select the subject for your lesson plan"
    )

with col2:
    st.markdown("### ⚙️ Configuration")
    
    grade_level = st.selectbox(
        "**Grade Level**",
        ["Basic", "Intermediate", "Advanced"],
        help="Choose the complexity level"
    )
    
    duration_weeks = st.slider(
        "**Duration (Weeks)**",
        1, 8, 4,
        help="Select how many weeks the lesson should span"
    )
    
    # Model initialization in the main area instead of sidebar
    st.markdown("---")
    st.markdown("**AI Model Setup**")
    model_choice = st.selectbox(
        "Select Model",
        ["microsoft/DialoGPT-medium", "microsoft/DialoGPT-small", "microsoft/DialoGPT-large"],
        label_visibility="collapsed"
    )
    
    if st.button("🚀 Initialize AI Model", use_container_width=True):
        with st.spinner("Loading AI model..."):
            st.session_state.generator = LessonPlanGenerator(model_choice)
        st.success("AI model loaded and ready!")

st.markdown('</div>', unsafe_allow_html=True)

# GENERATE BUTTON - Centered and prominent
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    generate_clicked = st.button(
        "✨ GENERATE LESSON PLAN", 
        type="primary", 
        use_container_width=True,
        disabled=not st.session_state.generator
    )

if generate_clicked:
    if not input_text:
        st.error("❌ Please enter a topic or syllabus description!")
    else:
        with st.spinner("🤖 AI is creating your customized lesson plan..."):
            result = st.session_state.generator.generate_lesson_plan(input_text, subject, grade_level)
            st.session_state.lesson_plan = result
        
        st.markdown('<div class="success-msg">✅ Lesson plan generated successfully!</div>', unsafe_allow_html=True)

# DISPLAY RESULTS
if st.session_state.lesson_plan:
    plan = st.session_state.lesson_plan
    
    st.markdown("---")
    st.markdown('<div class="section-title">📋 Your Generated Lesson Plan</div>', unsafe_allow_html=True)
    
    # Basic Info Card
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        st.markdown(f"**🎯 Topic:** {plan.get('Topic_Name', 'N/A')}")
    with col_info2:
        st.markdown(f"**📚 Subject:** {subject}")
    with col_info3:
        st.markdown(f"**📊 Level:** {grade_level}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main Content in two columns
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Learning Objectives
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Learning Objectives")
        objectives = plan.get('Learning_Objectives', [])
        for i, obj in enumerate(objectives, 1):
            st.markdown(f"{i}. {obj}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Required Resources
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🛠️ Required Resources")
        resources = plan.get('required_resources', [])
        for resource in resources:
            st.markdown(f"• {resource}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Teaching Methods
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 📚 Teaching Methods")
        methods = plan.get('Teaching_Methods', [])
        for method in methods:
            st.markdown(f"• {method}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        # Activities & Exercises
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🏃 Activities & Exercises")
        activities = plan.get('Activities_Exercises', [])
        for activity in activities:
            st.markdown(f"• {activity}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Assessment Methods
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Assessment Methods")
        assessments = plan.get('Assessment_Methods', [])
        for assessment in assessments:
            st.markdown(f"• {assessment}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Prerequisites & Keywords
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        col_pre, col_key = st.columns(2)
        
        with col_pre:
            st.markdown("### 📋 Prerequisites")
            prerequisites = plan.get('Prerequisites', [])
            for prereq in prerequisites:
                st.markdown(f"• {prereq}")
        
        with col_key:
            st.markdown("### 🔑 Keywords")
            keywords = plan.get('Keywords', [])
            if keywords:
                for keyword in keywords[:5]:  # Show first 5 keywords
                    st.markdown(f"`{keyword}`")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Duration Schedule (Full Width)
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### ⏰ Weekly Schedule")
    duration = plan.get('Duration', {})
    if duration:
        weeks_cols = st.columns(min(4, len(duration)))
        for i, (week, description) in enumerate(duration.items()):
            with weeks_cols[i % len(weeks_cols)]:
                st.markdown(f"**{week}**")
                st.markdown(f"{description}")
    else:
        st.info("Weekly schedule will be generated based on topic complexity.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # DOWNLOAD SECTION
    st.markdown("---")
    st.markdown('<div class="section-title">💾 Export Options</div>', unsafe_allow_html=True)
    
    col_d1, col_d2, col_d3 = st.columns(3)
    
    with col_d1:
        # JSON download
        json_data = json.dumps(plan, indent=2, ensure_ascii=False)
        st.download_button(
            "📥 Download as JSON",
            json_data,
            file_name=f"lesson_plan_{subject}_{grade_level}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col_d2:
        # Text download
        text_data = f"LESSON PLAN: {plan.get('Topic_Name', 'N/A')}\n"
        text_data += f"Subject: {subject} | Grade Level: {grade_level}\n"
        text_data += "="*50 + "\n\n"
        
        text_data += "LEARNING OBJECTIVES:\n"
        for obj in plan.get('Learning_Objectives', []):
            text_data += f"• {obj}\n"
        
        text_data += "\nREQUIRED RESOURCES:\n"
        for resource in plan.get('required_resources', []):
            text_data += f"• {resource}\n"
        
        st.download_button(
            "📄 Download as Text",
            text_data,
            file_name=f"lesson_plan_{subject}_{grade_level}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col_d3:
        if st.button("🔄 Create New Plan", use_container_width=True):
            st.session_state.lesson_plan = None
            st.rerun()

# FOOTER
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; margin-top: 2rem;'>"
    "Minor Project | Lesson Planning Using GenAI"
    "</div>", 
    unsafe_allow_html=True
)