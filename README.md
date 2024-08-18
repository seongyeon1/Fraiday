# 응급구조 챗봇

## 사용법
```
git clone 

# 가상환경 만들기
python -m venv .venv
echo '.venv' >> .gitignore
. .venv/bin/activate
 
pip install --upgrade pip
pip install -r requirements.txt

# .env 파일 만들기
cat > .env
UPSTAGE_API_KEY='발급 받은 API 입력' #ex) UPSTAGE_API_KEY=up_YW~

cd app
python server.py
```
실행후 http://0.0.0.0:8000/ 에서 결과 확인가능

- http://0.0.0.0:8000/chat/playground : 멀티턴 대화에 능숙한 실제 응급구조 대원과 같이 대화하는 모델
- http://0.0.0.0:8000/main/playground : RAG를 사용하여 응급처치 설명에 익숙하며, KTAS 단계를 알려주고 대화 요약까지 가능한 모델

## dir structure

### app
- `main.py` : fastapi, langserve 활용한 메인 페이지
- `chat.py`
  - upstage api 사용해서 프롬프트만 튜닝해서 응급구조 챗봇데모 제작 (고도화 진행중)
  - 멀티턴 대화에 좋은 성능을 보임
  - 실제 응급구조 요원같이 대화하지만 전문적인 지식을 요구할 시 명확한 지식근거가 부족함
 
- `rag.py` : rag 이용 (서울대학교 응급처치)
  - `chat` 페이지보다 전문적인 모델
  - RAG를 사용하여 응급처치 설명에 익숙함
  - KTAS 단계를 알려주고 대화 요약까지 가능한 모델
  - 절차를 따라서 KTAS 단계를 알려주기 떄문에 유연한 대화가 부족함

- `/template` : 프롬프트 템플릿을 저장


[고도화 예정]
- summerize : finetuning version

### preprocessing
- ocr.py
- chunking.py
  - RAG를 위한 임베딩과 OCR 처리를 위한 함수
  - 현재는 서울대학교 데이터, 생활응급처치 길라잡이 데이터를 ocr처리하고 embedding하는 데에 사용


## 실행결과
![Screenshot 2024-08-14 at 2 41 18 PM](https://github.com/user-attachments/assets/c92a18a1-0cf0-447e-8117-e603e6da2842)
![Screenshot 2024-08-14 at 2 41 23 PM](https://github.com/user-attachments/assets/10343291-3cc5-4a40-aeed-55c4fa32d6f2)
![Screenshot 2024-08-14 at 2 41 26 PM](https://github.com/user-attachments/assets/b987a5a3-b6ba-4fb0-bc7f-ce4506c29296)
     
일정 질문이 지나면 알아서 대처방안을 제시해준다
# Fraiday
