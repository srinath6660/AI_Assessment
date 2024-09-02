import streamlit as st
import pandas as pd
import os
import re
import time
from openai import OpenAI


def initialize_session_state():
    if 'section' not in st.session_state:
        st.session_state.section = 1
    if 'company_info' not in st.session_state:
        st.session_state.company_info = {}
    if 'form_data' not in st.session_state:
        st.session_state.form_data = None
    if 'feedback' not in st.session_state:
        st.session_state.feedback = None


def main():
    initialize_session_state()

    if st.session_state.section == 1:
        display_client_information()
    elif st.session_state.section == 2:
        display_assessment_areas()
    elif st.session_state.section == 3:
        display_submission_success()
    elif st.session_state.section == 4:
        display_generating_feedback()
    elif st.session_state.section == 5:
        display_scores_and_feedback()







# Helper functions for validation and processing
def validate_email(email):
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return re.match(pattern, email)

def validate_phone(phone):
    pattern = r"^\+?\d[\d -]{8,12}\d$"
    return re.match(pattern, phone)



def display_client_information():
    st.markdown("<h1 style='text-align: center;'>PRI Global AI Assessment</h1>", unsafe_allow_html=True)
    st.header("Client Information")
    
    company_name = st.text_input("Company Name:")
    contact_person = st.text_input("Contact Person:")
    email = st.text_input("Email:")
    phone = st.text_input("Phone:")
    
    if email and not validate_email(email):
        st.error("Invalid email format. Please enter a valid email.")
    if phone and not validate_phone(phone):
        st.error("Invalid phone format. Please enter a valid phone number.")
    
    if st.button("Next"):
        if company_name and contact_person and validate_email(email) and validate_phone(phone):
            st.session_state.company_info = {
                "Company Name": company_name,
                "Contact Person": contact_person,
                "Email": email,
                "Phone": phone
            }
            st.session_state.section = 2
            st.rerun()
        else:
            st.error("Please complete all required fields correctly before proceeding.")





def display_assessment_areas():
    st.header("Assessment Areas")

    # Current AI Implementation
    st.subheader("1. Current AI Implementation")
    ai_implementation = st.radio("Do you currently use any AI/ML technologies in your operations?", ("Yes", "No"))
    ai_details = ""
    if ai_implementation == "Yes":
        ai_details = st.text_input("If yes, please specify:")
    

    # Areas of Interest in AI
    st.subheader("2. Areas of Interest in AI")
    ai_interest = st.multiselect(
        "Select your areas of interest:",
        ["AI for Data Analytics and Business Intelligence", 
         "AI for Process Automation", 
         "AI for Customer Experience Enhancement", 
         "AI for Predictive Maintenance", 
         "Other"]
    )
    ai_interest_other = ""
    if "Other" in ai_interest:
        ai_interest_other = st.text_input("Please specify other areas of interest:") 


   
    # Challenges Faced
    st.subheader("3. Challenges Faced")
    challenges = st.multiselect(
        "What are the current challenges you face in implementing AI solutions? (Multiple selections allowed)",
        ["Budget Constraints", "Lack of Expertise", "Integration with Existing Systems", "Data Privacy Concerns", "Others"]
    )
    challenges_other = ""
    if "Others" in challenges:
        challenges_other = st.text_input("Please specify other challenges:")


    # Desired Outcomes from AI Implementation
    st.subheader("4. Desired Outcomes from AI Implementation")
    desired_outcomes = st.multiselect(
        "What are the key outcomes you wish to achieve with AI? (Rank in order of priority)",
        ["Improved Operational Efficiency", "Enhanced Customer Experience", "Increased Revenue", "Competitive Advantage", "Others"]
    )
    outcomes_other = ""
    if "Others" in desired_outcomes:
        outcomes_other = st.text_input("Please specify other outcomes:")

    # Interest in Specific AI Services
    st.subheader("5. Interest in Specific AI Services")
    ai_services = st.multiselect(
        "Please indicate your interest in the following PRI Global AI services:",
        ["AI Consultation and Strategy Development", 
        "AI Model Development and Deployment", 
        "AI System Integration", 
        "AI Training and Support"]
    )

    # Organizational Commitment
    st.subheader("6. Organizational Commitment")
    org_commitment = st.radio(
        "My organization's leadership is committed to investing in the necessary resources for AI in general:",
        ["Completely disagree", "Disagree", "Neutral -- neither agree nor disagree", "Agree", "Completely agree"]
    )

    # Culture
    st.subheader("7. Culture")
    culture_change = st.radio(
        "My organization is proactive in managing change, ready to drive a cultural shift towards innovation, continuous learning, and adaptability required for successful AI implementation:",
        ["Completely disagree", "Disagree", "Neutral -- neither agree nor disagree", "Agree", "Completely agree"]
    )
    culture_trust = st.radio(
        "There is a culture of trust in AI across my company:",
        ["Completely disagree", "Disagree", "Neutral -- neither agree nor disagree", "Agree", "Completely agree"]
    )
    culture_collaboration = st.radio(
        "There is a strong collaborative culture around AI in my organization:",
        ["Completely disagree", "Disagree", "Neutral -- neither agree nor disagree", "Agree", "Completely agree"]
    )
    culture_ethics = st.radio(
        "The culture around AI is ethical:",
        ["Completely disagree", "Disagree", "Neutral -- neither agree nor disagree", "Agree", "Completely agree"]
    )

    # AI Experimentation
    st.subheader("8. AI Experimentation")
    ai_experimentation = st.radio(
        "People in my company are already experimenting with generative AI:",
        ["They may be doing so at home, but not at work", 
        "They are exploring using open source tools such as ChatGPT",
        "They are building proof of concepts (POCs) against content that may be used for a generative AI application, such as website information",
        "They have moved beyond simple tasks to experiment with POCs using company data in production"]
    )

    # Data Readiness
    st.subheader("9. Data Readiness")
    #under subheader include small heading like 9.1, 9.2, 9.3
    

    data_diversity = st.radio(
        "Which statement BEST describes the kinds of data your organization collects and manages as part of its analytics and AI efforts?",
        ["None", 
        "Structured data (i.e., tables, records)", 
        "Structured data as well as demographic data such as age, location, etc.", 
        "All of the above plus semistructured data (XML and similar)", 
        "All of the above plus 1-2 of the following: internally generated text data (e.g., emails, call interaction notes, survey verbatim), social media data (blogs, tweets), machine-generated data, geospatial data, real-time event data, audio, video, weblogs, clickstreams, scientific data, demographic data", 
        "All of the above, plus 3 or more of the following: internally generated text data (e.g., emails, call interaction notes, survey verbatim), social media data (blogs, tweets), machine-generated data, geospatial data, real-time event data, audio, video, weblogs, clickstreams, scientific data, demographic data"]
    )

    # Skills Readiness
    st.subheader("10. Skills Readiness")
    skills_scope = st.radio(
        "Which of the following statements BEST describes the technologies your organization uses to analyze its data?",
        ["We use spreadsheets", 
        "We use reports, dashboards, and visualizations", 
        "We use the above and self-service data discovery and we are starting with predictive analytics/ML", 
        "We use the above and predictive analytics/ML against multiple data types", 
        "We use the above as well as techniques such as NLP, deep learning, and generative AI"]
    )

    # Roles and Responsibilities
    st.subheader("11. Roles and Responsibilities")
    data_scientists = st.radio(
        "My company has hired data scientists as part of its AI efforts. They possess strong data science skills, including data analysis, statistics, and machine learning:",
        ["No", 
        "No, but we plan to do this soon", 
        "Yes, we have a few data scientists and/or we are outsourcing help for now", 
        "Yes, our data scientists are part of the analytics team", 
        "Yes, data scientists are part of the analytics team and they collaborate with the business"]
    )

    ml_ops = st.radio(
        "My organization employs MLOps or AIOps to deal with AI models in production:",
        ["No, and I'm not sure we are thinking about operations", 
        "No, however we realize this is important and may be trying to work on it ad hoc with existing staff", 
        "We are developing a dedicated group / staff members responsible for this", 
        "We have dedicated team members with a specific mandate and resources for this", 
        "We have a complete team with enough data engineers, dev/ops, and similar personnel to support our full capacity of needs"]
    )

    data_engineers = st.radio(
        "My organization employs data engineers to build data pipelines for AI. They are responsible for managing and preparing large datasets for AI, ensuring data quality and accessibility:",
        ["No, and I'm not sure we are thinking about data engineers", 
        "No, however we realize this is important and may be trying to work on it ad hoc with existing staff or outsource it", 
        "We are developing a dedicated group / staff members responsible for this / working with an outside group", 
        "We have dedicated team members with a specific mandate and resources for this", 
        "We have a complete team with enough data engineers, dev/ops, and similar personnel to support our full capacity of needs"]
    )

    developers = st.radio(
        "My organization employs developers to build AI applications. They are skilled software engineers with experience in developing, deploying, and maintaining AI-powered applications:",
        ["No, and I'm not sure we are thinking about development of AI apps at this point in time", 
        "No, however we realize this is important and may be trying to work on it ad hoc with existing staff", 
        "We are developing a dedicated group / staff members responsible for this", 
        "We have dedicated team members with a specific mandate and resources for this", 
        "We have a complete team with enough developers to support the full capacity of needs"]
    )

    vp_of_ai = st.radio(
        "My company has a VP of AI, CAO, or a similar role in place to support AI efforts:",
        ["No, and I'm not sure we are thinking about that role", 
        "We have a VP of AI but he/she is not a technical AI expert", 
        "We have a CAO or similar role who has technical expertise"]
    )

    # Skills, Knowledge, and Upskilling
    st.subheader("12. Skills, Knowledge, and Upskilling")
    improve_skills = st.radio(
        "My company believes it can improve the skills of its business analysts to become data scientists:",
        ["No, we are not at the point where we need data scientists", 
        "Yes, but they will need help from others", 
        "Yes, they can build models, especially with some easy-to-use tools on the market", 
        "No, we have the data scientists we need"]
    )

    foundational_ai_concepts = st.radio(
        "My company's employees have a solid understanding of foundational AI concepts and how they can be applied to our business processes:",
        ["Completely disagree", "Disagree", "Neutral -- neither agree nor disagree", "Agree", "Completely agree"]
    )

    # Operational Readiness
    st.subheader("13. Operational Readiness")
    production_readiness = st.radio(
        "Analytics, in general, are operationalized/deployed in a business system(s) or an application(s) in my organization:",
        ["No and we have no plans to do so", 
        "No, but we are thinking about it", 
        "Yes, we are trying to implement this now", 
        "Yes, we operationalized this", 
        "Yes, we routinely do this with our analytics and this is often automated"]
    )

    collaboration_readiness = st.radio(
        "There is effective collaboration between development teams, IT operations, and business stakeholders to ensure smooth deployments and eventual operational support for AI models:",
        ["Completely disagree", "Disagree", "Neutral -- neither agree nor disagree", "Agree", "Completely agree"]
    )

    # AI Strategy and Implementation
    st.subheader("14. AI Strategy and Implementation")
    ai_strategy = st.radio(
        "We have or plan to establish a cross-functional team dedicated to deploying and managing AI models, ensuring smooth operation and integration across the business:",
        ["Agree", "Completely agree", "Not applicable", 
        "No and we have no plans to do so", 
        "Not yet, however we are thinking about it", 
        "Yes, we are trying to do this sometimes now", 
        "Yes, we do this regularly now", 
        "Yes, we routinely do this with automated checks and allot the necessary time for our staff to address this"]
    )

    # Data Governance
    st.subheader("15. Data Governance")
    data_governance = st.radio(
        "Data is trusted and governed across platforms in my organization:",
        ["No, we have many data silos that are not governed", 
        "We trust the data that we use for reporting that comes from our data warehouse, but not much else", 
        "We are starting to put processes in place for data governance beyond just the DW or other sources of data that need to be compliant (e.g., HIPAA) so we can trust other key data sources", 
        "We have a solid data governance plan that outlines key policies and processes; these are followed in the organization"]
    )

    data_policies = st.radio(
        "My organization understands our data sources and has the right policies in place to deal with different kinds of data:",
        ["Completely disagree", "Disagree", "Neutral -- neither agree nor disagree", "Agree", "Completely agree"]
    )

    data_governance_policies = st.radio(
        "Users accept and adhere to data governance policies:",
        ["Completely disagree", "Disagree", "Neutral -- neither agree nor disagree", "Agree", "Completely agree"]
    )

    data_catalogs = st.radio(
        "My organization uses tools such as data catalogs to help users access trusted data:",
        ["No, and my company has no plans to do so", 
        "No, but we are planning to implement this kind of tool/platform", 
        "We are actively researching this kind of tool/platform", 
        "We are putting this kind of tool/platform in place, currently", 
        "We have this tool/platform implemented in my organization"]
    )

    # Model Governance
    st.subheader("16. Model Governance")
    model_governance = st.radio(
        "Model deployment processes are in place in your organization. For example, models must be checked so as not to be incorrect or unethical (e.g., have racial bias, etc.) before they are put into production:",
        ["Not applicable/we don't have models in production in my organization", 
        "We have models deployed, but we don't check if they are incorrect. We trust our data scientists", 
        "We are putting controls in place over our models", 
        "We have a strong model control process in place"]
    )

    model_governance_policies = st.radio(
        "We have established clear governance policies for AI models, including approval processes, ethical guidelines, and compliance checks before deployment:",
        ["Completely disagree", "Disagree", "Neutral -- neither agree nor disagree", "Agree", "Completely agree"]
    )

    # Analytics and Model Catalogs
    st.subheader("18. Analytics and Model Catalogs")
    analytics_catalogs = st.radio(
        "My company uses tools such as analytics/model catalogs to keep track of BI and AI applications:",
        ["No or not applicable", "We are moving in this direction", 
        "Yes, we have analytics catalogs in place that can be used for AI models, as well"]
    )

    # Governance Roles
    st.subheader("19. Governance Roles")
    governance_team = st.radio(
        "Your company has a data and analytics governance team in place with representatives from across the company including key business stakeholders. Roles and responsibilities are clearly defined:",
        ["Completely disagree", "Disagree", "Neutral -- neither agree nor disagree", "Agree", "Completely agree"]
    )

    data_steward = st.radio(
        "The role of data steward(s) is in place and that person's (or team's) roles and responsibilities are clearly identified:",
        ["Completely disagree", "Disagree", "Neutral -- neither agree nor disagree", "Agree", "Completely agree"]
    )

    ai_steward = st.radio(
        "The role of AI steward(s) is in place and that person's (or team's) roles and responsibilities are clearly identified:",
        ["Not yet", "Not yet, but we are moving in that direction", "Yes"]
    )

    # Security and Privacy
    st.subheader("20. Security and Privacy")
    security_policies = st.radio(
        "Security policies are in place and enforced for all forms of data in your company:",
        ["No", "Data in the warehouse is secured and governed, but not necessarily in external sources or in data lakes, etc.", 
        "Yes, security policies are in place for all kinds of sensitive data", 
        "Yes, we have carefully thought through how we deal with different kinds of data on our governance team", 
        "Yes, we have carefully thought through and operationalized how we deal with different kinds of data on our governance team"]
    )

    data_privacy = st.radio(
        "My organization adheres to strict data privacy and security protocols, ensuring the protection of sensitive information used in our AI systems against unauthorized access and breaches:",
        ["Completely disagree", "Disagree", "Neutral -- neither agree nor disagree", "Agree", "Completely agree"]
    )

    # Responsible AI
    st.subheader("21. Responsible AI")
    ethical_ai = st.radio(
        "My company has developed and adopted a comprehensive ethical AI framework that guides the development, deployment, and use of AI technologies, ensuring they align with our core values and ethical standards:",
        ["Not yet/Not applicable", "Not yet, but we are moving in that direction", "Yes"]
    )

    transparency = st.radio(
        "We have mechanisms in place to ensure the transparency and explainability of our AI systems, allowing stakeholders to understand how AI decisions are made:",
        ["Not yet/Not applicable", "Not yet, but we are moving in that direction", "Yes"]
    )

    bias_mitigation = st.radio(
        "My organization actively implements processes for detecting and mitigating bias in AI models, ensuring fairness and reducing the risk of unintended harm:",
        ["Not yet/Not applicable", "Not yet, but we are moving in that direction", "Yes"]
    )

    ai_communication = st.radio(
        "Our company engages with stakeholders, including employees, customers, and the wider community, to communicate our responsible AI practices and address any concerns related to AI ethics:",
        ["Not yet/Not applicable", "Not yet, but we are moving in that direction", "Yes"]
    )

    # Demographics and Spend
    st.subheader("22. Demographics and Spend")
    timeframe_ai = st.radio(
        "What is your time frame to purchase a new AI solution to help advance your initiatives?",
        ["Immediately", "Next 3 months", "Next 3-6 months", 
        "Next 6 months to 1 year", "Next 1 year+", "No plans at present"]
    )

    industry = st.selectbox(
        "Which best describes your industry?",
        ["Financial Services", "Insurance", "Public Sector", "Education", 
        "Energy/Utilities", "Retail", "Manufacturing", "Transportation", 
        "Software", "Services", "Healthcare", "Life Sciences", 
        "Media and entertainment", "Engineering/Construction", 
        "Telecommunications", "Utilities", "Other"]
    )

    annual_revenue = st.radio(
        "What is the annual revenue of your organization?",
        [
            "Less than $100 million dollars",
            "100 million dollars to 499 million dollars",
            "500 million dollars to 999 million dollars",
            "1 billion dollars to 4.9 billion dollars",
            "5 billion dollars to 9.9 billion dollars",
            "10 billion dollars or higher",
            "Don't know or cannot disclose"
        ]
    )


    region = st.selectbox(
        "In what region are you located?",
        ["United States of America", "Canada", "Europe", "Australia/New Zealand/Oceania", 
        "Asia", "Africa", "Mexico, Central America, South America, or Caribbean", "Middle East"]
    )


    # Submission
    if st.button("Submit"):
        # Collect all form data into a dictionary
        form_data = {
            **st.session_state.company_info,
            "AI Implementation": ai_implementation,
            "AI Details": ai_details if ai_implementation == "Yes" else "",
            "Areas of Interest": ", ".join(ai_interest),
            "Other Areas of Interest": ai_interest_other,
            "Challenges": ", ".join(challenges),
            "Other Challenges": challenges_other,
            "Desired Outcomes": ", ".join(desired_outcomes),
            "Other Desired Outcomes": outcomes_other,
            "AI Services Interest": ", ".join(ai_services),
            "Organizational Commitment": org_commitment,
            "Culture Change": culture_change,
            "Culture Trust": culture_trust,
            "Culture Collaboration": culture_collaboration,
            "Culture Ethics": culture_ethics,
            "AI Experimentation": ai_experimentation,
            "Data Diversity": data_diversity,
            "Skills Scope": skills_scope,
            "Data Scientists": data_scientists,
            "MLOps": ml_ops,
            "Data Engineers": data_engineers,
            "Developers": developers,
            "VP of AI": vp_of_ai,
            "Improve Skills": improve_skills,
            "Foundational AI Concepts": foundational_ai_concepts,
            "Production Readiness": production_readiness,
            "Collaboration Readiness": collaboration_readiness,
            "AI Strategy": ai_strategy,
            "Data Governance": data_governance,
            "Data Policies": data_policies,
            "Data Governance Policies": data_governance_policies,
            "Data Catalogs": data_catalogs,
            "Model Governance": model_governance,
            "Model Governance Policies": model_governance_policies,
            "Analytics Catalogs": analytics_catalogs,
            "Governance Team": governance_team,
            "Data Steward": data_steward,
            "AI Steward": ai_steward,
            "Security Policies": security_policies,
            "Data Privacy": data_privacy,
            "Ethical AI": ethical_ai,
            "Transparency": transparency,
            "Bias Mitigation": bias_mitigation,
            "AI Communication": ai_communication,
            "Timeframe for AI": timeframe_ai,
            "Industry": industry,
            "Annual Revenue": annual_revenue,
            "Region": region
        }


        # Convert the dictionary to a DataFrame
        df = pd.DataFrame([form_data])
        
        # Save to CSV file
        file_name = 'ai_assessment_data.csv'
        if os.path.exists(file_name):
            # Append the data to the existing file
            df.to_csv(file_name, mode='a', header=False, index=False)
        else:
            # Create a new file and save the data
            df.to_csv(file_name, index=False)
        
        st.success("Form submitted successfully, thank you!.... Generating AI readiness feedback")
                # Display success message
        # message_placeholder.success("Form submitted successfully!")
                # Wait for 2 seconds
        time.sleep(0.5)
        # Store the form data in session state for displaying scores and feedback
        st.session_state.form_data = form_data
        st.session_state.section = 3  # Move to the next section
        st.rerun()



def display_submission_success():
    st.success("Form submitted successfully!")
    time.sleep(2)  # Display success message for 2 seconds
    st.session_state.section = 4
    st.rerun()



def display_generating_feedback():
    st.markdown("<h1 style='text-align: center;'>Generating AI Readiness Feedback</h1>", unsafe_allow_html=True)
    
    with st.spinner("Analyzing your AI readiness..."):
        # Simulate API call delay
        time.sleep(3)
        
        # Actual API call
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        client = OpenAI()
        
        form_data_session = st.session_state.form_data
        prompt = f"Here is the form data collected from a company regarding their AI journey: {form_data_session}. Based on this data, please generate the AI readiness scores following the Response Format."
        
        system_message = """"
You are an AI assistant responsible for evaluating a company's AI readiness based on their assessment data. The data includes details about their current AI implementation, challenges, desired outcomes, organizational commitment, culture, data readiness, and more.

Responce should only be in below example format, replace the scores and stages with the actual values generated from the form data, and provide brief feedback for each score based on the form data.(also display total stages at the end):
- **Overall AI Readiness: 70/100**
  - **Stage:** Standardizing (Stage 3)
    - **Feedback:** one or two sentences explaining the score based on the form data.

- **Organizational Readiness: 15/20**
  - **Stage:** Succeeding (Stage 4)
    - **Feedback:** one or two sentences explaining the score based on the form data.

- **Data Readiness: 13/20**
  - **Stage:** Strategizing (Stage 2)
    - **Feedback:** one or two sentences explaining the score based on the form data.

Stages:
- Pre-embarking (Stage 1)
- Strategizing (Stage 2)
- Standardizing (Stage 3)
- Succeeding (Stage 4)
- Transforming (Stage 5)

--------------------------------------------

Your task is to evaluate the company's readiness across the following categories and generate scores based on the provided information:

Overall AI Readiness (0-100):

This score represents the organization’s overall maturity in adopting AI, encompassing all aspects of AI strategy, governance, culture, and implementation.
Break down the score by comparing their current AI implementation, challenges, and readiness to the five stages: Pre-embarking, Strategizing, Standardizing, Succeeding, and Transforming.
Organizational Readiness (0-20):

Evaluate the organization's commitment to AI, including leadership support, culture, collaboration, and change management.
Assign a stage based on their responses to organizational questions.
Data Readiness (0-20):

Assess the quality, diversity, and governance of their data and how prepared they are to use data effectively in AI projects.
Consider their data collection methods, data engineers, MLOps, and data governance policies.
For each score, also indicate the stage the company is in:

Pre-embarking (Stage 1)
Strategizing (Stage 2)
Standardizing (Stage 3)
Succeeding (Stage 4)
Transforming (Stage 5)
Generate brief feedback for each score that explains why the score was given based on the form data.

--------------------------------------------

To generate meaningful scoring results for clients' AI journeys, you can structure the scores around three main categories: Overall AI Readiness, Organizational Readiness, and Data Readiness. Each category can be associated with specific stages in the AI journey, such as "Pre-embarking," "Strategizing," "Standardizing," "Succeeding," and "Transforming." Here's how you can structure the scoring:

1. Overall AI Readiness Score:
Score Range: 0-100
Stages:
0-20: Pre-embarking (Stage 1)
21-40: Strategizing (Stage 2)
41-60: Standardizing (Stage 3)
61-80: Succeeding (Stage 4)
81-100: Transforming (Stage 5)
Description: This score reflects the organization's overall maturity in adopting AI. It considers the entire AI strategy, governance, culture, and how effectively AI is integrated into operations. The score should provide insights into how far along the organization is in its AI journey and what might be required to progress to the next stage.

2. Organizational Readiness Score:
Score Range: 0-20
Stages:
0-4: Pre-embarking (Stage 1)
5-8: Strategizing (Stage 2)
9-12: Standardizing (Stage 3)
13-16: Succeeding (Stage 4)
17-20: Transforming (Stage 5)
Description: This score measures the organization’s internal readiness for AI, including leadership support, change management, and the overall cultural alignment towards AI adoption. It reflects how committed the leadership is to AI, how well the organization is equipped to handle change, and the level of collaboration and innovation within the organization.

3. Data Readiness Score:
Score Range: 0-20
Stages:
0-4: Pre-embarking (Stage 1)
5-8: Strategizing (Stage 2)
9-12: Standardizing (Stage 3)
13-16: Succeeding (Stage 4)
17-20: Transforming (Stage 5)
Description: This score assesses the organization's data quality, diversity, and governance. It also evaluates how well the organization manages data through roles like data engineers and MLOps, and how ready the data infrastructure is to support AI initiatives. This score should indicate whether the organization has the necessary data foundation to advance in their AI journey.

--------------------------------------------

Example:

*** strictly follow the format below to generate the feedback ***
- **Overall AI Readiness: 70/100**
  - **Stage:** Standardizing (Stage 3)

- **Organizational Readiness: 15/20**
  - **Stage:** Succeeding (Stage 4)

- **Data Readiness: 13/20**
  - **Stage:** Strategizing (Stage 2)

Stages:
- Pre-embarking (Stage 1)
- Strategizing (Stage 2)
- Standardizing (Stage 3)
- Succeeding (Stage 4)
- Transforming (Stage 5)

Ensure that the generated scores and stages are consistent with the form data provided."

--------------------------------------------
"""
        response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ]
            )
        st.session_state.feedback = response.choices[0].message.content

    st.session_state.section = 5
    st.rerun()


def display_scores_and_feedback():
    st.markdown("<h1 style='text-align: center;'>AI Readiness Scores and Feedback</h1>", unsafe_allow_html=True)

    if st.session_state.feedback:
        st.subheader("AI Readiness Feedback:")
        st.write(st.session_state.feedback)
    else:
        st.warning("No feedback generated. Please complete the assessment first.")

if __name__ == "__main__":
    main()