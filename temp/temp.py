from langchain.chains.router import MultiRouteChain, RouterChain

from langchain.chains import ConversationChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.chains import SimpleSequentialChain, TransformChain


from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain,RouterOutputParser
from langchain.prompts import PromptTemplate
# from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from operator import itemgetter
from typing import Literal
from typing_extensions import TypedDict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_upstage import ChatUpstage
import os
import dotenv

dotenv.load_dotenv()
llm = ChatUpstage(api_key=os.getenv("UPSTAGE_API_KEY"))

# Chain 프롬프트 템플릿 설정
class PromptFactory():
    ask_additional_symptoms = """
        당신은 응급상황을 판단하는 전문가입니다. 환자의 추가적인 증상을 물어보십시오.
        질문: {input}
    """
    provide_first_aid = """
        당신은 응급처치 전문가입니다. 환자의 증상에 따라 적절한 응급처치 방법을 제공하십시오.
        질문: {input}
    """
    provide_emergency_guidance = """
        당신은 응급환자 관리 전문가입니다. 응급환자이므로 구급차를 불러야 합니다. 
        구급차가 도착하기 전까지 환자를 어떻게 대처해야 하는지 제시하십시오.
        질문: {input}
    """

    emergency_judgment = """
        당신은 응급상황을 판단하는 전문가입니다.
        나이, 증상, 생체 징후, 병력 등을 고려하여 환자의 상태를 평가합니다.
        환자의 중증도 분류체계인 KTAS 단계로 환자를 분류해주세요.
        KTAS는 5단계로 분류됩니다. 각 단계는 환자의 상태의 심각성을 기준으로 하며, 1단계가 가장 긴급하고 5단계가 가장 덜 긴급한 상황을 나타냅니다.
        1. 1단계 (즉각적 치료 필요): 생명이 위급하거나 즉시 치료가 필요한 상태입니다. 예를 들어, 심정지나 심각한 호흡 곤란 등이 해당합니다.
        2. 2단계 (긴급 치료 필요): 신속한 평가와 치료가 필요하지만, 1단계보다는 덜 긴급한 상태입니다. 예를 들어, 심각한 통증이나 출혈이 있는 경우입니다.
        3. 3단계 (중간 정도의 긴급성): 상태가 안정적이지만 빠른 평가와 치료가 필요한 상황입니다. 일반적인 외상이나 급성 질환 등이 포함됩니다.
        4. 4단계 (경미한 상태): 상대적으로 덜 긴급한 상태로, 일반적으로 장기적인 문제를 가지고 있는 경우입니다. 예를 들어, 가벼운 상처나 경미한 증상 등이 해당됩니다.
        5. 5단계 (비긴급 상태): 즉각적인 치료가 필요하지 않은 상태로, 일반적으로 외래 치료가 적합한 경우입니다. 예를 들어, 예방적 조치나 경미한 불편감 등이 포함됩니다.

        대화가 장난전화라면 경고 문구와 함께 대화를 종료해주세요.
    """

    classify_hoax_call = """
        당신은 응급상황을 판단하는 전문가입니다. 대화가 장난전화라면 대화를 종료해주세요.
        질문: {input}
    """

    summerize_dialogue = """
        당신은 응급구조 전문가입니다. 환자의 대화만을 사용해서 의사에게 효과적으로 전달할 수 있는 자료를 만들어주세요.
        나이, 증상, 생체 징후, 병력, 환자의 중증도 분류체계인 KTAS 단계를 반드시 제시해주어야 합니다.
    """

    # 목적지 Chain 정보를 담은 리스트
    prompt_info = [
        {
            "name": "emergency_judgment",
            "description": "장난 전화를 분류합니다",
            "prompt_template": classify_hoax_call
        },
        {
            "name": "emergency_judgment",
            "description": "충분한 정보들을 바탕으로 세부 응급상황을 판단합니다.",
            "prompt_template": emergency_judgment
        },
        {
            "name": "ask_additional_symptoms",
            "description": "응급상황을 판단하는데 추가적인 정보가 없으므로 추가적인 증상을 물어봅니다.",
            "prompt_template": ask_additional_symptoms
        },
        {
            "name": "provide_first_aid",
            "description": "환자의 증상을 바탕으로 응급처치가 가능한 상황이라면 응급처치 방법을 제공해줍니다.",
            "prompt_template": provide_first_aid
        },
        {
            "name": "provide_emergency_guidance",
            "description": "응급환자이므로 구급차를 불러야 합니다. 구급차가 도착하기 전까지 대처 방법을 제시해줍니다.",
            "prompt_template": provide_emergency_guidance
        },
        {
            "name": "provide_emergency_guidance",
            "description": "대화를 요약해줍니다.",
            "prompt_template": summerize_dialogue
        }
    ]

from pathlib import Path
from typing import Mapping, List, Union

class MyMultiPromptChain(MultiRouteChain):
    """A multi-route chain that uses an LLM router chain to choose amongst prompts."""

    router_chain: RouterChain
    """Chain for deciding a destination chain and the input to it."""
    destination_chains: Mapping[str, Union[LLMChain, SimpleSequentialChain]]
    """Map of name to candidate chains that inputs can be routed to."""
    default_chain: LLMChain
    """Default chain to use when router doesn't map input to one of the destinations."""

    @property
    def output_keys(self) -> List[str]:
        return ["text"]


def generate_destination_chains():
    """
    Creates a list of LLM chains with different prompt templates.
    Note that some of the chains are sequential chains which are supposed to generate unit tests.
    """
    prompt_factory = PromptFactory()
    destination_chains = {}
    for p_info in prompt_factory.prompt_infos:
        name = p_info['name']
        prompt_template = p_info['prompt_template']
        
        chain = LLMChain(
            llm=llm, 
            prompt=PromptTemplate(template=prompt_template, input_variables=['input']),
            output_key='text',
        )
        
        #if name not in prompt_factory.programmer_test_dict.keys() and name != prompt_factory.word_filler_name:
        destination_chains[name] = chain

        
        # else:
        #     # Normal chain is used to generate code
        #     # Additional chain to generate unit tests
        #     template = prompt_factory.programmer_test_dict[name]
        #     prompt_template = PromptTemplate(input_variables=["input"], template=template)
        #     test_chain = LLMChain(llm=llm, prompt=prompt_template, output_key='text')
        #     destination_chains[name] = SimpleSequentialChain(
        #         chains=[chain, test_chain], verbose=True, output_key='text'
        #     )


    default_chain = ConversationChain(llm=llm, output_key="text")
    return prompt_factory.prompt_info, destination_chains, default_chain











# 목적지 Chain들 생성
triage_chains = {}
for p in prompt_info:
    name = p["name"]
    prompt = ChatPromptTemplate.from_messages([
        ("system", p["prompt_template"]),
        MessagesPlaceholder(variable_name="messages"),
    ])
    triage_chains[name] = prompt | llm | StrOutputParser()

# 목적지 정보 문자열 생성
triages = [f"{p['name']}: {p['description']}" for p in prompt_info]
triages_str = "\n".join(triages)

# RouterChain 프롬프트 템플릿 설정
MULTI_PROMPT_ROUTER_TEMPLATE = """
    입력받은 내용을 바탕으로 가장 적절한 모델 프롬프트를 선택하세요.
    모델 프롬프트 정보는 다음과 같이 주어집니다.

    "프롬프트 이름": "프롬프트 설명"

    << FORMATTING >>
    Return a markdown code snippet with a JSON object formatted to look like:
    ```json
    {{
        "triage": string \ name of the prompt to use or "DEFAULT"
        "next_inputs": string \ a potentially modified version of the original input
    }}
    ```
    REMEMBER: "triage"은 아래 주어진 프롬프트 설명을 바탕으로 프롬프트 이름 중 하나를 선택하거나,
    적절한 프롬프트가 없으면 "DEFAULT"를 선택할 수 있습니다.

    REMEMBER: "next_inputs"은 원본 INPUT을 넣으세요.

    << CANDIDATE PROMPTS >>
    {triages}

    << INPUT >>
    {{input}}

    << OUTPUT (remember to include the ```json)>>
"""

router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
    triages=triages_str
)

router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    output_parser=RouterOutputParser(),
)

# route_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", router_template),
#         MessagesPlaceholder(variable_name="messages"),
#     ]
# )

router_chain = LLMRouterChain.from_llm(llm, router_prompt)

default_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're answering a call as a first responder. \
            Communicate with the caller to determine the patient's emergency as quickly as possible,\
            and You should only ask one question per conversation.\
            Determine the KTAS level based on the patient's condition (Level 1: Resuscitation, Level 2: Urgent, Level 3: Emergency, Level 4: Sub-emergent, Level 5: Non-emergent)",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

default_chain = default_prompt | llm | StrOutputParser()

chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains=triage_chains,
    default_chain=default_chain,
    verbose=True
)

# # Define the prompt templates
# prompt_info = [
#     {
#         "name": "classify_hoax_call",
#         "description": "Classifies hoax calls.",
#         "prompt_template": """
#             You are an expert in determining emergency situations. If the conversation is a prank call, please terminate the conversation.
#             Question: {input}
#         """
#     },
#     {
#         "name": "emergency_judgment",
#         "description": "Makes detailed emergency assessments based on sufficient information.",
#         "prompt_template": """
#             You are an expert in determining emergency situations.
#             Consider age, symptoms, vital signs, medical history, etc. to assess the patient's condition.
#             Classify the patient according to the KTAS, which is a five-level triage system based on the severity of the patient's condition:
#             1. Level 1 (Immediate): Life-threatening conditions requiring immediate treatment, e.g., cardiac arrest or severe respiratory distress.
#             2. Level 2 (Emergency): Conditions requiring urgent evaluation and treatment, e.g., severe pain or significant bleeding.
#             3. Level 3 (Urgent): Stable conditions needing prompt evaluation and treatment, e.g., moderate trauma or acute illness.
#             4. Level 4 (Less Urgent): Relatively less urgent conditions, e.g., minor injuries or mild symptoms.
#             5. Level 5 (Non-Urgent): Conditions not requiring immediate treatment, e.g., preventive care or mild discomfort.
#             If the conversation is a prank call, please terminate the conversation with a warning message.
#         """
#     },
#     {
#         "name": "ask_additional_symptoms",
#         "description": "Asks for additional symptoms when there is insufficient information to determine an emergency.",
#         "prompt_template": """
#             You are an expert in determining emergency situations. Ask the patient for additional symptoms.
#             Question: {input}
#         """
#     },
#     {
#         "name": "provide_first_aid",
#         "description": "Provides first aid instructions based on the patient's symptoms if applicable.",
#         "prompt_template": """
#             You are a first aid expert. Provide appropriate first aid instructions based on the patient's symptoms.
#             Question: {input}
#         """
#     },
#     {
#         "name": "provide_emergency_guidance",
#         "description": "Provides instructions on how to handle the patient until an ambulance arrives.",
#         "prompt_template": """
#             You are an expert in emergency management. The patient is in an emergency situation, and an ambulance should be called.
#             Provide instructions on how to manage the patient until the ambulance arrives.
#             Question: {input}
#         """
#     },
#     {
#         "name": "summarize_dialogue",
#         "description": "Summarizes the conversation.",
#         "prompt_template": """
#             You are an emergency response expert. Create an effective report for the doctor using only the patient's dialogue.
#             Be sure to include age, symptoms, vital signs, medical history, and the KTAS level.
#         """
#     }
# ]

# # Create triage chains
# triage_chains = {}
# for p in prompt_info:
#     name = p["name"]
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", p["prompt_template"]),
#         ("human", "{input}"),
#         MessagesPlaceholder(variable_name="messages")
#     ])
#     triage_chains[name] = prompt | llm | StrOutputParser()

# # Create triages string
# triages = [f"{p['name']}: {p['description']}" for p in prompt_info]
# triages_str = "\n".join(triages)
# print(triages_str)

# # Define the routing system prompt template
# route_system = f"""
#     Based on the input, select the most appropriate model prompt.
#     Route the user's query to one of the CANDIDATE PROMPTS.
#     Model prompt information is provided as follows:

#     "Prompt Name": "Prompt Description"

#     << FORMATTING >>
#     Return a markdown code snippet with a JSON object formatted to look like:
#     ```json
#     {{
#         "triage": string \ name of the prompt to use or "DEFAULT",
#         "next_inputs": string \ a potentially modified version of the original input
#     }}
#     ```
#     REMEMBER: "triage" should be one of the provided prompt names or "DEFAULT" if none are suitable.
#     REMEMBER: "next_inputs" should be the original input.

#     << CANDIDATE PROMPTS >>
#     classify_hoax_call: Classifies hoax calls.
#     emergency_judgment: Makes detailed emergency assessments based on sufficient information.
#     ask_additional_symptoms: Asks for additional symptoms when there is insufficient information to determine an emergency.
#     provide_first_aid: Provides first aid instructions based on the patient's symptoms if applicable.
#     provide_emergency_guidance: Provides instructions on how to handle the patient until an ambulance arrives.
#     summarize_dialogue: Summarizes the conversation.

#     << INPUT >>
#     {{input}}

#     << OUTPUT (remember to include the ```json)>>"""
# # print([p['name'] for p in prompt_info])
# route_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", route_system),
#         ("human", "{input}"),
#         MessagesPlaceholder(variable_name="messages")
#     ]
# )

# class RouteQuery(TypedDict):
#     triage: Literal['classify_hoax_call', 'emergency_judgment', 'ask_additional_symptoms', 'provide_first_aid', 'provide_emergency_guidance', 'summarize_dialogue']
#     next_inputs: str

# router_chain = (
#     route_prompt
#     | llm.with_structured_output(RouteQuery)
#     | itemgetter("triage", "next_inputs")
# )

# # Default prompt
# default_prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You're answering a call as a first responder. \
#             Communicate with the caller to determine the patient's emergency as quickly as possible,\
#             and You should only ask one question per conversation.\
#             Determine the KTAS level based on the patient's condition (Level 1: Resuscitation, Level 2: Urgent, Level 3: Emergency, Level 4: Sub-emergent, Level 5: Non-emergent)",
#         ),
#         ("human", "{input}"),
#         MessagesPlaceholder(variable_name="messages")
#     ],
# )

# default_chain = default_prompt | llm | StrOutputParser()

# def chain_selector(triage, next_inputs):
#     return triage_chains.get(triage, default_chain)

# final_chain = {
#     "destination": router_chain,
#     "input": lambda x: {"input": x["input"], "messages": x.get("messages", [])}  # pass through input query and messages
# } | RunnableLambda(chain_selector) | RunnableLambda(lambda x: {"input": x[1], "messages": x[2]}) | RunnableLambda(chain_selector) | RunnablePassthrough()

# # Example call
# response = final_chain.invoke({"input": "The patient is experiencing difficulty breathing.", "messages": []})
# print(response)