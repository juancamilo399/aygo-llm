from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.vectorstores import Pinecone
import os

os.environ["OPENAI_API_KEY"] = "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"
os.environ["PINECONE_API_KEY"] = "b67d7612-17d0-4ea6-afa6-39dc431a48a5"
os.environ["PINECONE_ENV"] = "gcp-starter"

def loadText():
    loader = TextLoader("caperucita.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    #text_splitter = RecursiveCharacterTextSplitter(
        #chunk_size = 1000,
        #chunk_overlap  = 200,
        #length_function = len,
        #is_separator_regex = False,
    #)


    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    import pinecone

    # initialize pinecone
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
        environment=os.getenv("PINECONE_ENV"),  # next to api key in console
    )

    index_name = "langchain-demo"

    # First, check if our index already exists. If it doesn't, we create it
    if index_name not in pinecone.list_indexes():
        # we create a new index
        pinecone.create_index(name=index_name, metric="cosine", dimension=1536)
    # The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`
    # docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)

def search():
    embeddings = OpenAIEmbeddings()
    import pinecone

    # initialize pinecone
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
        environment=os.getenv("PINECONE_ENV"),  # next to api key in console
    )

    index_name = "langchain-demo"
    # if you already have an index, you can load it like this
    docsearch = Pinecone.from_existing_index(index_name, embeddings)

    query = "al final que paso con caperucita?"
    docs = docsearch.similarity_search(query)
    print(docs[0].page_content)

loadText()
search()