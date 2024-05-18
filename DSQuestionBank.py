import streamlit as st
from streamlit_option_menu import option_menu
import pymongo

client = pymongo.MongoClient("mongodb://selva7025:generate@ac-hdblj4l-shard-00-00.xb5edcj.mongodb.net:27017,ac-hdblj4l-shard-00-01.xb5edcj.mongodb.net:27017,ac-hdblj4l-shard-00-02.xb5edcj.mongodb.net:27017/?ssl=true&replicaSet=atlas-7gqhz2-shard-0&authSource=admin&retryWrites=true&w=majority")
Bank_DB = client['Question_Bank'] #creating Question_Bank database
Questions_Collection = Bank_DB['Questions'] #creating collection for Questions


st.set_page_config(page_title="Data Science Question Bank",
                   page_icon="",
                   layout="wide",
                   initial_sidebar_state="expanded")

#st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown("<h1 style='color: WHITE;'><b>Question Bank</b></h1>", unsafe_allow_html=True)

skill_list = ["SQL", "Python", "Machine Learning", "Natural Language Processing", 
              "Pandas", "Deep Learning", "Data Analysis", "Data Visualization"]

role_list = ["Data Scientist", "Data Analyst", "Data Engineer", 
               "AIML Engineer", "Python Developer", "Business Analyst"]
difficulty_list = ["Easy", "Medium", "Hard"]

def extract_questions_by_skill(selected_segment,selected_skill,selected_level):
    if selected_segment == "Role":
        query = {selected_segment: selected_skill, "Difficulty":{"$in": selected_level}}
    else:
        query = {selected_segment: {"$in": selected_skill}, "Difficulty":{"$in": selected_level}}
    questions = Questions_Collection.find(query, {"Question": 1, "_id": 0})  # Fetch only the Question field
    return list(questions)

col1_1,col2_2,col3_2 = st.columns([1,0.5,1])


col1,col2,col3 = st.columns([1,2,1])
with col1:
    segment_type = ""
    selected_segment = st.selectbox("Selcet Option Role or Skill",options=["Role","Skill"])

with col2:
    if selected_segment == "Role":
        segment_type = role_list
        selected_skill = st.selectbox(label="Role*",options= segment_type, placeholder="Choose an option",)
    elif selected_segment == "Skill":
        segment_type = skill_list
        selected_skill = st.multiselect(label="Skill*",options= segment_type, default=None,placeholder="Choose an option",)
with col3:
    selected_level = st.multiselect(label="Difficulty Level *",options= difficulty_list, default="Easy",placeholder= "Choose an option")

if st.button("Go"):
    data_scientist_questions = extract_questions_by_skill(selected_segment,selected_skill,selected_level)
    
    col2_1,col2_2,col2_3 = st.columns([1,2,1])
    with col2_2:
        if data_scientist_questions:
            st.dataframe(data=data_scientist_questions)
