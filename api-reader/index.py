from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
import streamlit as streamlit

prompt_webapp_template = """
  You are a web app developer using Javascript.
  Please generate a complete functional javascript app
  following user requirement "Please make a web application. This web application needs to include a button and the following API endpoint: {text}, that is interacted with via button.".
  The JS file and CSS file should be combined into one HTML file, which can be directly run on server.
  If there is no CSS requirement specified, please add an Amazon-style CSS in your response.
  The response should only include the content of the HTML file.
  HTML:

"""

prompt_api_explainer_template = """
  You are a web app developer.
  Please give a detailed explanation of this API 
  in human readable terms: "{text}".
  The explanation must be generated in Markdown format, and should include the sections: what is the API, what does the API do, how to use the API.
  The response should only include the content of the Markdown output.
  Markdown:
"""

prompt_api_swagger_gen_template = """
  You are a web app developer.
  Please generate a swagger template of this API: "{text}".
  This swagger template must be generated in YAML format.
  The response should only include the content of the YAML output.
  YAML:

"""

PROMPT_WEBAPP = PromptTemplate(template=prompt_webapp_template, input_variables=["text"])
PROMPT_EXPLAINER = PromptTemplate(template=prompt_api_explainer_template, input_variables=["text"])
PROMPT_SWAGGER = PromptTemplate(template=prompt_api_swagger_gen_template, input_variables=["text"])

init_html = """
<!DOCTYPE html>
<html>
<head>
  <title>Example App</title>
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
if 'html_swagger' not in streamlit.session_state:
  streamlit.session_state.html_swagger = 'Swagger file will be generated here.'
if 'explainer' not in streamlit.session_state:
  streamlit.session_state.explainer = 'Explanation of the API will be generated here.'

def generate():
  
  requirement = streamlit.session_state.req
  llm = ChatOpenAI(temperature=0.5, openai_api_key=streamlit.session_state.openapi)
  webapp_chain = LLMChain(llm=llm, prompt=PROMPT_WEBAPP, verbose=True)
  swagger_chain = LLMChain(llm=llm, prompt=PROMPT_SWAGGER, verbose=True)
  explainer_chain = LLMChain(llm=llm, prompt=PROMPT_EXPLAINER, verbose=True)

  if requirement != '':
    streamlit.session_state.html = webapp_chain.run(requirement)
    streamlit.session_state.html_swagger = swagger_chain.run(requirement)
    streamlit.session_state.explainer = explainer_chain.run(requirement)

    print(streamlit.session_state.html)
    print(streamlit.session_state.html_swagger)
    print(streamlit.session_state.explainer)

col1, col2 = streamlit.columns([0.5, 0.5], gap='medium')

with col1:
  streamlit.write("**Give an API endpoint and we will generate all information for you.**")
  streamlit.text_area("API endpoint: ", key="req")
  streamlit.text_area("OpenAPI key: ", key="openapi")
  streamlit.button("Create!", on_click=generate)
  streamlit.code(streamlit.session_state.html, language="typescript")

with col2:
  streamlit.code(streamlit.session_state.explainer, language="markdown")
  streamlit.code(streamlit.session_state.html_swagger, language="yaml")
  streamlit.components.v1.html(streamlit.session_state.html, height=600, scrolling=True)
