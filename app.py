import os
import time
import langchain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from tavily import TavilyClient
import pytesseract as pyt
import numpy as np
from langchain.agents import create_agent
import streamlit as st




#=================API KEYS============================
GOOGLE_KEY = st.sidebar.text_input("Google-API",type = "password")
GROQ_KEY = st.sidebar.text_input("Groq-API",type = "password")
TAVILY_KEY = st.sidebar.text_input("Tavily-API",type = "password")

os.environ["GOOGLE_API_KEY"] = GOOGLE_KEY
os.environ["GROQ_API_KEY"] = GROQ_KEY
os.environ["tavily_API_KEY"] = TAVILY_KEY



ALL_API = [GOOGLE_KEY,  GROQ_KEY,  TAVILY_KEY]

if not all(ALL_API):
  st.sidebar.error("PASS API-KEYS")

elif any(ALL_API):
  st.sidebar.info("MUST PASS ALL API KEYS")

else:
  st.sidebar.success("API KEYS LOADED SUCCESSFULLY")
  #step 1: model call
model = ChatGoogleGenerativeAI(
  model = "gemini-3.5-flash-lite",
  google_api_key = GOOGLE_API_KEY
)

#================frontend-===============================
st.title(AI-Agent-Powered PPT Generator")

 user_query = st.text_area("Write your PPT topic or prompt:")

#=========================ASSESTS========================
#Step 2: Tools Creation
#Tool_1

def search_latest_info(query):
  """This function search latest
  news or content from website
  using tavily, helpful to check
  trending content"""

  client = TavilyClient(api_key = TAVILY_API_KEY)
  response = client.search(query)
  return response

 #Tool 2
def generate_image(img_prompt):
  """This function, helps to generate Image
  using Free api,  with given
  img_prompt using pollinations"""


  url = f"https://image.pollinations.ai/{img_prompt}"
  #file handling
  import requests as r
  content = r.get(url).content
  with open(f"Image.jpeg",'wb') as f:
    f.write(content)

  from PIL import Image
  img = Image.open("Image.jpeg")

#WITH TAB
tab1, tab2, tab3 = st.tabs([GENERATE IMAGE",
                            "CHECK LATEST NEWS",
                            "GENERATE PPT"])

#=====================
# Detailed prompt generator
def prompt_generator(model, query):
  prompt = f"""your task is to give detailed prompt instructions
  for given.

  prompt:
  You are a professional PPT generator, where
  user will give the query and based on that,
  you have to generate dynamic, HTML output based
  ppt with advanced CSS and Dynamic UI and UX with
  PPT toggle button, Based on Query take image reference to generate
  and embed the same in ppt using image ref: url = https://images.unsplash.com/photo, 
  or url = https://image.pollinations.ai/, 
  make sure img src must be valid, and image must be
  present inside html, Generate image caption, and no markdowns
  user query given below:{query}
  """
  response = model.invoke(prompt)
  final_prompt = response.content[-1]['text']

  with open("ppt_prompt.txt",'w') as f:
    f.write(final_prompt)
  return final_prompt

agent = create_agent(
    model = model,
    tools = [search_latest_info,
             generate_image]
             
)
#================display agent=============
st.sidebar.image(agent)


#==================WITH TABS=============
with tab1:
  st.header("GENERATE IMAGE GIVE PROMPT")
  if st.button("Click to generate:"):
    with st.spinner():
      data = generate_image(user_query)
      st.image(data)
      st.image("Image.jpeg")

with tab2:
  st.header("CHECK LATEST NEWS")
  if st.button("Fetch news:"):
    with st.spinner("Running Agent.."):
      prompt = """Give latest news India or world wide related
      to tech, business, jobs, or user requested output
      In Proper HTML News Templates""" + user_query

      response = agent.invoke({'message']:[{'role':"user",
                                            "content":prompt}]})
      code = response['message'][-1].content[-1]['text']

      st.html(code, width-"stretch",
              unsafe_allow_javascript=True)
with tab3:
    st.header("Create PPT")
    if st.button("Click to generate:"):
      with st.spinner("Running Agent.."):
        final_prompy = prompt_generatof(model,user_query)

response = agent.invoke({'message':[{'role':"user",
                                     "content":final_prompt}]})

code = response['message'][-1].content[-1]['text']
st.html(code,width= "stretch",
        unsafe_allow_javascript=True)
st.download_button(lable = "DOWNLOAD PPT",
                   data = code,
                   file_name = 'ppt.html',
                   mime = 'text/html')
st.success("PPT Download Successfully!")









