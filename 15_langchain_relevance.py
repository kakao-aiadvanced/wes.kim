from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
import bs4

llm = ChatOpenAI(model="gpt-4o-mini")

urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

loader = WebBaseLoader(
    web_paths=urls,
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(model="text-embedding-3-small"))

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def is_relevant(context, query):
    parser = JsonOutputParser()
    prompt = PromptTemplate(
        template="You will be given the context and the query.\n\nContext: {context}\n\nQuery: {query}\n\nNow, for the key `relevance`, indicate if the context is relevant enough to answer the query by `yes` or `no`.\n{format_instructions}",
        input_variables=["context", "query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    rag_chain = (
        {"context": context, "query": RunnablePassthrough()}
        | prompt
        | llm
        | parser
    )

    msg = rag_chain.invoke(query)
    if "relevance" not in msg:
        print(f"Wrong structure: {msg}")
        return False
    relevant = msg["relevance"]
    if relevant != "yes":
        print(f"Got relevance: {relevant} ({query})")
        return False
    
    return True

def answer(context, query):
    parser = StrOutputParser()
    prompt = PromptTemplate(
        template="Answer the user query.\n\nContext: {context}\n\nQuery: {query}",
        input_variables=["context", "query"],
    )
    rag_chain = (
        {"context": context, "query": RunnablePassthrough()}
        | prompt
        | llm
        | parser
    )
    return rag_chain.invoke(query)

def is_hallucinated(context, query):
    parser = JsonOutputParser()
    prompt = PromptTemplate(
        template="You will be given the context and the query.\n\nContext: {context}\n\nAnswer: {answer}\n\nNow, for the key `hallucination`, indicate if the answer was hallucinated, i.e. not based on the context or truth by `yes` or `no`.\n{format_instructions}",
        input_variables=["context", "answer"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    rag_chain = (
        {"context": context, "answer": RunnablePassthrough()}
        | prompt
        | llm
        | parser
    )

    msg = rag_chain.invoke(query)
    if "hallucination" not in msg:
        print(f"Wrong structure: {msg}")
        return True
    hallucination = msg["hallucination"]
    if hallucination != "no":
        print(f"Got hallucination: {hallucination} ({query})")
        return True

    return False

def run(query):
    context = retriever | format_docs
    relevant = is_relevant(context=context, query=query)
    if not relevant:
        return
    while True:
        result = answer(context=context, query=query)
        ok = not is_hallucinated(context=context, query=query)
        if ok:
            print(result)
            return

run("Give me some finance tips")
run("latest k-pop events?")
run("ELI5 what prompt engineering is.")
