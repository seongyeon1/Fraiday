<!-- PROJECT LOGO -->
<br />
<div align="center">
  <p align="center">
    <h1 align="center">Emergency Response Assistance Solution</h1>
    <h3>Project for <b>Upstage AI Hackathon</b></h3>
    <strong>Team Name : L3K1</strong>
    <a href="https://ko.upstage.ai/global-ai-week-ai-hackathon"><br />
      <img src="https://github.com/user-attachments/assets/9288c8db-4e97-4eb9-b289-38345d41c40b" alt="Logo" width="250" height="100">
    </a>
    <br />
    <a href="https://github.com/seongyeon1/Fraiday"><strong>Explore the Hackathon »</strong></a>
    <br />
    <br />
    <a href="https://docs.google.com/document/d/1ONG75P1bZVpyxKtr2DsYmgyUYKnC-Whs/edit?usp=sharing&ouid=107570799977032888577&rtpof=true&sd=true">Introduction</a>
    ·
    <a href="https://youtu.be/dEEOkgUy4N8">Demo Video</a>
    ·
    <a href="https://docs.google.com/presentation/d/1OV9YCP_De4GIgeO7TcDQ3gVXZyJmTuj7U4ng9Jv_Qso/edit?usp=sharing">Slides</a>
    <br />
    <br />
    <a href="https://github.com/seongyeon1/Fraiday/blob/main/README-ko.md">[Read in Korean]</a>

  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary><h2>Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#Project-Overview">Project Overview</a>
    </li>
    <li>
      <a href="#Getting-Started">Getting Started</a>
      <ul>
        <li>Clone the Repository</li>
        <li>Setup</li>
      </ul>
    </li>
    <li><a href="#Directory-Structure">Directory Structure</a></li>
    <li><a href="#Use-Case-Diagram">Use Case Diagram</a></li>
    <li><a href="#Data-Sources">Data Sources</a></li>
    <li><a href="#Authors-and-Acknowledgment">Authors and Acknowledgment</a></li>
  </ol>
</details>


## Project Overview

### Goals:
>- Assist first responders and medical personnel
>- Enable rapid and efficient emergency response and medical care

### What’s Pre-KTAS?
>- Patient classification system to determine treatment priority in emergencies. 
>- In Korea, the format of triage used in emergency rescue activities is specified in the rules on emergency rescue response activities and field command.
>   - [Reference](https://www.nfa.go.kr/nfa/news/pressrelease/press/?boardId=bbs_0000000000000010&mode=view&cntId=2072)

### Built With
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![fastapi](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![langchain](https://img.shields.io/badge/langchain-1C3C3C?style=for-the-badge&logo=langchain)



<br />


## Getting Started
### 1. **Clone the Repository:**
```bash
git clone https://github.com/seongyeon1/Fraiday.git
cd Fraiday
```
### 2. Setup
#### 2-1 **Using Makefile**
To start the application for the first time:
```bash
make startapp
```
- `setup.sh` will prompt you to enter your UPSTAGE_API_KEY during execution.

To rerun the application:
```bash
make rerun
```
          
#### 2-2. **Using `setup.sh` Script**
```bash
chmod +x setup.sh
./setup.sh
```
- `setup.sh` will prompt you to enter your UPSTAGE_API_KEY during execution.

  > You can check the results at http://0.0.0.0:8000/
  > - http://0.0.0.0:8000/chat/playground 
  > - A model that converses like a real emergency responder and excels in multi-turn conversations.
  > - http://0.0.0.0:8000/main/playground
  > - A model that is proficient in explaining first aid using RAG, informs about KTAS levels, and summarizes conversations.

#### Rerun the App
```bash
python app/main.py
```
         

#### 2-2. **Do it step-by-step**
 Create a Virtual Environment
```bash
python3 -m venv .venv
. .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

#### Create a .env File
```bash
cat > .env
UPSTAGE_API_KEY='Your API key' # e.g., UPSTAGE_API_KEY=up_YW~
```
- After entering, close the `cat` command using Ctrl+C.
      
#### Run the App
```bash
cd app
python main.py
```
</br>

## Result

https://github.com/user-attachments/assets/59b43d8a-8cfb-434b-bf5c-cefb6f41e2cd



## Directory Structure

```plaintext
Fraiday
├── app
│   ├── main.py
│   ├── chat.py
│   ├── rag.py
│   └── template
│       └── (prompt templates)
├── preprocessing
│   ├── ocr.py
│   └── chunking.py
├── setup.sh
├── requirements.txt
└── .env(example)
```

### app
- `app/main.py`: The main page utilizing FastAPI and Langserve.
- `app/chat.py`: 
  - Uses the [**Upstage API**](https://github.com/seongyeon1/Fraiday/blob/main/app/chat.py#L8)(for model, embeddings) to fine-tune prompts for an emergency response chatbot demo (under development).
  - Excels in multi-turn conversations.
  - Chats like a real emergency responder but lacks precise knowledge for professional expertise.
- `app/rag.py`: Uses RAG (Seoul National University First Aid).
  - A more specialized model compared to the `chat` page.
  - Proficient in explaining first aid using [**Upstage API**](https://github.com/seongyeon1/Fraiday/blob/main/app/rag.py#L19)(for model, embeddings) and **RAG**.
  - Informs about KTAS levels and summarizes conversations.
  - Lacks flexibility in conversations as it follows procedures to inform about KTAS levels.
- `app/templates`: Stores prompt templates.

### preprocessing
- Functions for embedding and OCR processing for RAG.
- Currently used for OCR processing and embedding Seoul National University data and the First Aid Guidebook.
</br>

  - `preprocessing/ocr.py`
    - Used [**Upstage API**(UpstageLayoutAnalysisLoader)](https://github.com/seongyeon1/Fraiday/blob/main/preprocessing/ocr.py#L20)
  - `preprocessing/chunking.py`
    - Used [**Upstage API**(Embeddings)](https://github.com/seongyeon1/Fraiday/blob/main/preprocessing/chunking.py#L38)




</br>

## Use Case Diagram

### **Now**
![Now](https://github.com/user-attachments/assets/5cc4ca12-4ad2-42ea-afb6-8069752e615f)

### **Future Work**
![Future Work](https://github.com/user-attachments/assets/d33f0b0c-1500-48e5-b9fc-c4a8d489d58c)

It will be implemented in the form of a router model that combines all of the following features
- **Multi-turn dialogue**: It is possible to respond and respond quickly according to the context by being proficient in multi-turn dialogue (currently, it is possible to implement through `chat.py` model)
- **Provide first aid information**: Provide accurate information based on clear knowledge (Currently, the `rag.py` model has been verified for implementation)
- **Conversation summary**: Summarise the information received at the end of an emergency conversation and use it as an aid for emergency room visits (implemented by tuning the prompt to summarise specific conditions based on history)

</br>

## Data Sources
**First aid resources** (for RAG)
- [Seoul National University Emergency Response Manual](https://health4u.snu.ac.kr/data/download/1_2.pdf)
- [Korea Fire Service Life First Aid Guide](https://fire.go.kr/site/fbn119/board/bbs018/433)
</br>

**Real emergency voice call dataset**
- [Emergency Voice/Audio - 119 Voice Recognition Data](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=71768)
</br>
</br>

## Authors and Acknowledgment
### FRAIDAY was created by L3K1

If you have any questions or comments about our project, please contact below.
EunkyungLee | SungyeonKim | JunghoonLee | JunghuiLee
:-: | :-: | :-: | :-:
 <img width="160px" src="https://avatars.githubusercontent.com/u/58682424?v=4"/><br>[@ek0111](https://github.com/ek0111) | <img width="160px" src="https://avatars.githubusercontent.com/u/83098550?s=400&u=29a89fe1f31aede109cb129c5b4251b0ef6f5070&v=4"/><br>[@seongyeon1](https://github.com/seongyeon1)|<img width="160px" src="https://avatars.githubusercontent.com/u/169136233?v=4"/><br>[@coronarita1991](https://github.com/coronarita1991)| <img width="160px" src="https://avatars.githubusercontent.com/u/82493052?v=4"/><br>[@wjdgml0526](https://github.com/wjdgml0526)
eunkyung0111@gmail.com | ksy974498@gmail.com|coronarita1991@gmail.com|wjdgml0526@gmail.com
