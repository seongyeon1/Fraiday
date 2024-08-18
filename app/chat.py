from langchain_upstage import ChatUpstage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
import dotenv

dotenv.load_dotenv()
llm = ChatUpstage(api_key=os.getenv("UPSTAGE_API_KEY"))

from template.prompt_in_eng import PROMPT

# Prompt 설정
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", PROMPT),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# LangChain 표현식 언어 체인 구문을 사용합니다.
chain = prompt | llm | StrOutputParser()