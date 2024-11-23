import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0,groq_api_key=os.getenv("GROQ_API_KEY"),model_name='llama-3.1-70b-versatile')
    def extract_jobs(self,cleaned_text):
        prompt_extract = PromptTemplate.from_template(
        '''
        ### SCRAPED TEXT FROM WEBSITE: 
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the career's page of a website.
        Your job is to extract the job postings nd return them in JSON format containing following keys : 
        'role','skills' and 'description'.
        Only return the valid JSON. 
        ### VALID JSON (NO PREAMBLE):
        '''
        )

        # prompt passing to llm
        chain_extract = prompt_extract | self.llm
        response = chain_extract.invoke(input={'page_data':cleaned_text})

        try:
            json_parser = JsonOutputParser()
            response = json_parser.parse(response.content)
        except OutputParserException:
            raise OutputParserException('Context too big, Unable to parse jobs.')
        return response if isinstance(response,list) else [response]
    
    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
        '''
        ### SCRAPED TEXT FROM WEBSITE: 
        {job_description}
        ### INSTRUCTION:
        Generate a cold email to [Recipient's Name], a [Recipient's Job Title] at [Recipient's Company], offering [Your Product/Service]. The email should include:

        A personalized subject line, relevant to their industry or role.
        A polite and professional greeting.
        A brief introduction about you or your company.
        A value proposition explaining how your product/service can benefit them, focusing on a specific challenge or opportunity relevant to their business.
        A clear and concise call to action (e.g., scheduling a call or meeting).
        A polite closing and your contact information.
        (Optional) A short postscript with an additional incentive or reference.
        Ensure the email is short, respectful of the recipient’s time, and free of jargon.
        Do not provide a preamble.
        ### EMAIL (NO PREAMBLE):
        '''
        )

        chain_email = prompt_email | self.llm
        response_cold_email = chain_email.invoke(input={'job_description':str(job),'link_list':links})
        return response_cold_email.content
    
