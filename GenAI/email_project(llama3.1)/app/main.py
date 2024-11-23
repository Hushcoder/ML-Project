import streamlit as st 
from chains import Chain
from portfolio import Portfolio
from utils import clean
from langchain_community.document_loaders import WebBaseLoader

def streamlit_app(llm, portfolio, clean):
    st.set_page_config(layout='wide', page_title='Cold Emailer', page_icon="✉️")
    
    st.markdown(
        """
        <h1 style='text-align: center; color: #0072B5;'>Cold Emailer</h1>
        <p style='text-align: center; font-size: 18px;'>powered by llama3.1-70b GenAI Model</p>
        """, 
        unsafe_allow_html=True
    )

    st.markdown("<hr style='border:1px solid #e0e0e0;'>", unsafe_allow_html=True)
    
    st.markdown(
        "<h3 style='text-align: center;'>Enter the Job Listing URL Below</h3>",
        unsafe_allow_html=True
    )
    
    url_input = st.text_input(
        'Job Listing URL:',
        value='https://jobs.nike.com/job/R-34397?from=job%20search%20funnel'
    )
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Center the button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        submit_button = st.button("Generate Cold Email 🚀")
    

    st.markdown("<hr style='border:1px solid #e0e0e0;'>", unsafe_allow_html=True)

    # Processing section when the button is clicked
    if submit_button:
        try:
            # Load the job description from the URL
            st.info("Fetching job data... Please wait.")
            loader = WebBaseLoader([url_input])
            data = clean(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            
            # Display extracted jobs
            if jobs:
                st.success(f"Found {len(jobs)} job(s). Generating emails...")
                for job in jobs:
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    
                    # email in Markdown format
                    st.markdown("### Generated Cold Email")
                    st.code(email, language='markdown')
            else:
                st.warning("No jobs found. Please check the URL.")
        
        except Exception as e:
            st.error(f"⚠️ An Error Occurred: {e}")
            st.markdown(
                "<p style='text-align: center; color: red;'>Please make sure the URL is valid and accessible.</p>",
                unsafe_allow_html=True
            )


if __name__ == '__main__':
    chain = Chain()
    portfolio = Portfolio()
    streamlit_app(chain, portfolio, clean)


######################################### Unbeautified Code ##################################################
# import streamlit as st 
# from chains import Chain
# from portfolio import Portfolio
# from utils import clean
# from langchain_community.document_loaders import WebBaseLoader



# def streamlit_app(llm, portfolio, clean):

#     # st.title('Cold Emailer')
#     st.write("<h2 style='text-align: center;'>Cold Emailer</h2>", unsafe_allow_html=True)
#     # st.write('powered by llama3.1 GenAI Model')
#     st.write("<p style='text-align: center;'>powered by llama3.1 GenAI Model</p>", unsafe_allow_html=True)
    
#     # default value -> nike job link
#     url_input = st.text_input('Enter a URL:', value = 'https://jobs.nike.com/job/R-34397?from=job%20search%20funnel')
#     submit_button = st.button("Send")
    
#     if submit_button:
#         try:
#             loader = WebBaseLoader([url_input])
#             data = clean(loader.load().pop().page_content)
#             portfolio.load_portfolio()
#             jobs = llm.extract_jobs(data)
#             for job in jobs:
#                 skills  = job.get('skills',[])
#                 links = portfolio.query_links(skills)
#                 email = llm.write_mail(job,links)
#                 st.code(email, language='markdown')
#         except Exception as e:
#             st.error(f'An Error Occurred: {e}')



# if __name__ == '__main__':
#     chain = Chain()
#     portfolio = Portfolio()
#     st.set_page_config(layout='wide',page_title='Cold Emailer')
#     streamlit_app(chain, portfolio, clean)
