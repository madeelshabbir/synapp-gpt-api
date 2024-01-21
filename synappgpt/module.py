
from PyPDF2 import PdfReader
import os
import glob
import environ
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.chains import VectorDBQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings

env = environ.Env()
environ.Env.read_env()

OPENAI_API_KEY = env('OPENAI_API_KEY')
embeddings = OpenAIEmbeddings()


def load_data(pdf_path,save_path):

    pdf_folder_path = glob.glob(pdf_path)
    context = []
    metadata = []
    for path in pdf_folder_path:
        reader = PdfReader(path)
        page_texts = [page.extract_text() for page in reader.pages]
        splitter = CharacterTextSplitter('\n', chunk_size=1200, chunk_overlap=500)
        doc_context = splitter.split_text(" ".join(page_texts))
        metadata += [{"file_name" : path.split('/')[-1]}] * len(doc_context)
        context += doc_context

    db = FAISS.from_texts(texts=context, embedding = embeddings, metadatas = metadata)
    db.save_local(save_path)



def answer(prompt, save_path,parameter):
    print("answer function call",prompt)
    """From a question asked by the user, generate the answer based on the vectorstore.

    Args:
        prompt (str): Question asked by the user.
        persist_directory (str): Vectorstore directory.

    Returns:
        str: Answer generated with the LLM
    """

    prompt_temp = """I have given you some French documents.

    DOCUMENTS:
    =========
    {context}
    =========

    Answer my question from given documents. Just say "no answer" if relevent answer not found. Just say "no answer" if question is ambiguous.
    QUESTION: {question}
    """
    embeddings = OpenAIEmbeddings()
    # save_path = "pdf_input/"+concatenated_str
    # save_path =  os.path.join(settings.MEDIA_ROOT, save_path)

    vectorstore = FAISS.load_local(save_path, embeddings)
    prompt_template = PromptTemplate(template=prompt_temp, input_variables=["context", "question"])
    doc_chain = load_qa_chain(
        llm = ChatOpenAI(
            openai_api_key = OPENAI_API_KEY,
            model_name = "gpt-3.5-turbo",
            #model_name = parameter.model_name,
            # temperature = 0,
            # max_tokens = 500,
            # top_p = 1,
            # frequency_penalty = 0,
            # presence_penalty = 0

            temperature = parameter.temperature,
            max_tokens = parameter.max_length,
            top_p = parameter.top_p,
            frequency_penalty = parameter.frequency_penalty,
            presence_penalty = parameter.presence_penalty
        ),
        chain_type = "stuff",
        prompt = prompt_template)

    qa = VectorDBQA(
        vectorstore = vectorstore,
        return_source_documents = True,
        combine_documents_chain = doc_chain,
        k = 3)

    result = qa({"query": prompt})
    answer = {}
    answer['result'] = result['result']
    if "noanswer" in result['result'].lower().replace(' ',''):
        answer['sources'] = []
    else:
        answer['sources'] = set([i.metadata['file_name'] for i in result['source_documents']])
    return answer
# temperature = 0,
# max_tokens = 500,
# top_p = 1,
# frequency_penalty = 0,
# presence_penalty = 0
