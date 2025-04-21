import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Marks Analyzer", page_icon="📊")
st.title("📊 Student Marks Analyzer")

# Grade logic
def assign_grade(avg):
    if avg >= 85:
        return 'A'
    elif avg >= 70:
        return 'B'
    elif avg >= 50:
        return 'C'
    elif avg >= 35:
        return 'D'
    else:
        return 'F'

# Input section
st.sidebar.header("Add Student Marks")
student_name = st.sidebar.text_input("Student Name")
math_marks = st.sidebar.number_input("Math Marks", 0, 100, 0)
science_marks = st.sidebar.number_input("Science Marks", 0, 100, 0)
english_marks = st.sidebar.number_input("English Marks", 0, 100, 0)

if 'students' not in st.session_state:
    st.session_state.students = []

if st.sidebar.button("Add Student"):
    if student_name:
        st.session_state.students.append({
            'Name': student_name,
            'Math': math_marks,
            'Science': science_marks,
            'English': english_marks
        })
        st.sidebar.success(f"Added {student_name}")
    else:
        st.sidebar.error("Please enter a student name.")

# Delete student option
if st.session_state.students:
    st.sidebar.header("Delete a Student")
    student_list = [student['Name'] for student in st.session_state.students]
    delete_student = st.sidebar.selectbox("Select Student to Delete", student_list)

    if st.sidebar.button("Delete Student"):
        st.session_state.students = [s for s in st.session_state.students if s['Name'] != delete_student]
        st.sidebar.success(f"Deleted {delete_student}")

# Display student data if available
if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)
    
    # Calculate averages and grades
    df['Average'] = df[['Math', 'Science', 'English']].mean(axis=1)
    df['Grade'] = df['Average'].apply(assign_grade)

    st.subheader("📋 Student Data")
    st.dataframe(df.style.format({"Average": "{:.2f}"}))

    # Class average per subject
    st.subheader("📊 Class Averages Per Subject")
    class_avg = df[['Math', 'Science', 'English']].mean()
    st.write(class_avg)

    # Bar chart: Average marks per student
    st.subheader("📈 Average Marks Per Student")
    fig1, ax1 = plt.subplots()
    ax1.bar(df['Name'], df['Average'], color='skyblue')
    ax1.set_ylim(0, 100)
    ax1.set_ylabel('Average Marks')
    ax1.set_title('Average Marks Per Student')
    st.pyplot(fig1)

    # Pie chart: Grade distribution (dynamic)
    st.subheader("🍰 Grade Distribution")
    grade_counts = df['Grade'].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.pie(grade_counts.values, labels=grade_counts.index, autopct='%1.1f%%', startangle=140, colors=['#66b3ff','#99ff99','#ffcc99','#ff9999','#c2c2f0'])
    ax2.axis('equal')
    ax2.set_title('Grade Distribution')
    st.pyplot(fig2)
else:
    st.info("Add student marks from the sidebar to get started!")
