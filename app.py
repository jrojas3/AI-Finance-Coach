# Importing libraries
import google.generativeai as genai
import streamlit as st
import pandas as pd


# Gemini and Streamlit Configuration
genai.configure(api_key=st.secrets["key"])

st.set_page_config(page_icon="💸", page_title="AI Finance Coach", layout='centered')

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Caching Data, so that we don't have to read the file everytime
@st.cache_data
def get_countries_name():
    countries = pd.read_csv("countries.csv")
    return countries.name

country_list = get_countries_name()

st.header("AI Finance Coach 🥇")
st.write(
    "<h4>Hello, I am your AI Finance Coach. I will help you to get out of debt and achieve your financial goals. I will provide you with a comprehensive financial plan tailored to your specific financial situation. I will consider your current income, existing debts, and the cost of living in your country. I will provide you with a clear breakdown of the financial plan, including detailed timelines, interest rates, and all available financial data. I will ensure that any recommended items are accessible within your local region.</h4>",
    unsafe_allow_html=True
)

# get user name
name_input = st.text_input("What is your name?", value="Joseph")

# get user age
age_input = st.number_input("What is your age?", value=25, min_value=16)

# get user country
country_input = st.selectbox("Where do you live?", country_list)

# get user monthly income
monthly_income = st.number_input("What is your monthly income $?", value=884, min_value=10)

# get user monthly expenses
monthly_expenses = st.number_input("What is your monthly expenses $?", value=249, min_value=10)

# get user current debt amount
current_debt = st.number_input("What is your current debt $?", value=0, min_value=0)

# Get user bad money habits
bad_money_habits = st.text_area("Having any bad money habits? Write it down here:", placeholder="For e.g. Spending too much on food, Shopping too much")

# Get user financial goals
financial_goals = st.text_area("What are your financial goals? Write it down here:", placeholder="For e.g. Buying a house, Buying a car")

prompt = "You are Joseph, an expert financial advisor who has helped multiple people to get out of debt and achieve their financial goals. " +\
"A new user has joined your academy, your job is to guide the user with proper financial plan in order to achieve his idea financial goals. " +\
"I will provide you with the user information, you have to strictly output in a markdown table form. "+\
"User Information: "+\
f"Name: {name_input}, "+\
f"Age: {age_input}, "+\
f"Monthly Income: {monthly_income}, "+\
f"Monthly Expenses: {monthly_expenses}, "+\
f"Current Debt: {current_debt}, "+\
f"Bad Money Habits: {bad_money_habits}, "+\
f"Financial Goals: {financial_goals}. "+\
f"Develop a comprehensive financial plan tailored to an individuals specific financial situation. Consider their current income, existing debts, and the cost of living in their country. Provide a clear breakdown of the financial plan, including detailed timelines, interest rates, and all available financial data. Ensure that any recommended items are accessible within the users local region. Also include a 5 year projection. Conclude with separate sections for the Financial Plan and Recommendations, demarcated by --- for easy reference"

if st.button("Generate Financial Plan"):
    response = model.generate_content(prompt)
    st.write(response.text)
