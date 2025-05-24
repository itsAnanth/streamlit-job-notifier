import streamlit as st
from utils import load_models, find_match


st.title("Job Finder")

skills_text = st.text_area("Enter your skills eg. (python, js)")


if st.button("Find Jobs"):
    if skills_text:


        prediction = find_match(skills_text)
        if len(prediction) > 0:
            st.markdown(f"Found **{len(prediction)}** jobs that might suit your skillset!")
            for i, row in prediction.iterrows():
                st.markdown(f"### {row['Title']}")
                row = row.drop(['Title', 'Cluster', 'Cluster_Name'])
                for key, value in row.items():
                    st.markdown(f"**{key}**: {value}")  # Cluster info
                st.markdown("---")  # Horizontal separator between jobs
        else:
            st.markdown("Sorry! we could not find any jobs that might suit you")
    else:
        st.warning("Please enter your skills to search for")
