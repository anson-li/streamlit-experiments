from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
import streamlit as streamlit

prompt_webapp_template = """
  You are a web app developer using Javascript.
  Please generate a complete functional javascript app.
  This application needs to look and function like a Google search webpage, except it needs to pull its information from
  Bing using the following endpoint: "https://api.bing.microsoft.com/v7.0/search".
  Additionally, the following key should be used for Bing authentication: "{text}".
  Please include the Google logo.
  The JS file and CSS file should be combined into one HTML file, which can be directly run on server.
  The response should only include the content of the HTML file.
  HTML:

"""

PROMPT_WEBAPP = PromptTemplate(template=prompt_webapp_template, input_variables=["text"])

init_html = """
<!DOCTYPE html>
<html>
<head>
  <title>Example</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f5f5f5;
    }
    h3 {
      padding: 25px;
      font-size: 0.9em;
    }
  </style>
</head>
<body>
  <h3>Your application will be displayed here.</h3>
</body>
</html>
"""

streamlit.set_page_config(layout="wide")
if 'html' not in streamlit.session_state:
  streamlit.session_state.html = init_html

def generate():
  
  apikey = streamlit.session_state.key
  llm = ChatOpenAI(temperature=0.5, openai_api_key=streamlit.session_state.openapi)
  webapp_chain = LLMChain(llm=llm, prompt=PROMPT_WEBAPP, verbose=True)

  if apikey != '':
    streamlit.session_state.html = webapp_chain.run(apikey)
    print(streamlit.session_state.html)

streamlit.title('Bing API to Google Webpage')
streamlit.subheader('Given your Bing authentication key, create a Google search page')
col1, col2 = streamlit.columns([0.5, 0.5], gap='medium')

with col1:
  streamlit.text_area("Bing API key: ", key="key")
  streamlit.text_area("OpenAPI key: ", key="openapi")
  streamlit.button("Create!", on_click=generate)
  streamlit.code(streamlit.session_state.html, language="typescript")

with col2:
  streamlit.components.v1.html(streamlit.session_state.html, height=600, scrolling=True)