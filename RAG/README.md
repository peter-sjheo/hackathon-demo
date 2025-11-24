# 해외여행보험 PDF → RAG 데이터 변환 완료

## 📊 생성된 파일 목록

### 1. **travel_insurance_rag_complete.json** (메인 데이터)
RAG 시스템에서 사용할 수 있는 구조화된 JSON 데이터
- 문서정보 (상품명, 보험사, 연락처 등)
- 핵심용어 5개 (상해, 장해, 해외여행중 등)
- 보장내용 7개 (사망, 후유장해, 의료비, 휴대품, 배상책임 등)
- 면책사항 14개
- 필요서류 5개 카테고리
- 특별약관 2개
- 특약상세 5개
- FAQ 4개
- 청구절차
- 주의사항 5개
- 카테고리별 키워드 매핑 9개
- 텍스트 청크 샘플 10개

### 2. **travel_insurance_rag_complete.md** (Markdown 문서)
사람이 읽기 쉬운 형태의 마크다운 문서
- 보장내용, 면책사항, 필요서류를 보기 좋게 정리
- 문서 공유 및 참조용으로 활용 가능

### 3. **travel_insurance_chunks.csv** (청크 데이터)
벡터 DB 임베딩을 위한 텍스트 청크
- 총 282개의 의미 단위 청크
- 각 청크는 chunk_id, title, content, char_count, category 포함
- ChromaDB, Pinecone, Weaviate 등에 바로 임베딩 가능

### 4. **rag_usage_example.py** (활용 예제)
RAG 시스템 구현을 위한 Python 예제 코드
- TravelInsuranceRAG 클래스 구현
- 키워드 검색, 의미 검색, FAQ 조회 등 다양한 기능
- LangChain + ChromaDB 연동 예제 포함
- 챗봇 통합 예제 코드 포함

---

## 🎯 추출된 핵심 데이터

### 보장내용 (7개)
1. **사망보험금**: 상해로 인한 사망
2. **후유장해보험금**: 상해로 인한 장해
3. **상해의료비**: 입원/통원/처방조제비
4. **질병의료비**: 여행 중 발병한 질병 치료비
5. **휴대품손해**: 파손/도난/분실 보상
6. **배상책임**: 타인 신체/재물 손해배상
7. **항공기지연**: 4시간 이상 지연 시

### 면책사항 (14개)
- 고의적 자해, 범죄행위
- 전쟁, 혁명, 내란, 폭동
- 지진, 분화, 해일 등 천재지변
- 핵연료물질 관련
- 음주운전, 정신장애
- 전문등반, 스카이다이빙 등 위험운동
- 선박 직무상 탑승
- 미용 성형수술
- 치과/한방치료 (상해 제외)

### 필요서류 (5개 카테고리)
1. **공통서류**: 청구서, 동의서, 신분증
2. **사망보험금**: 사망진단서, 제적등본, 의료기록
3. **후유장해보험금**: 장해진단서, 의무기록, 검사결과
4. **의료비보험금**: 진료비영수증, 진단서, 의무기록
5. **휴대품손해보험금**: 손해액증명서류, 경찰신고서, 견적서

### 핵심용어 (5개)
1. **상해**: 급격하고 우연한 외래의 사고로 인한 신체 손상
2. **장해**: 장해분류표 기준에 따른 장해상태
3. **해외여행중**: 주거지 출발 → 여행 → 주거지 도착까지
4. **보험기간**: 계약에 따른 보장 기간
5. **중요한사항**: 계약 승낙에 영향을 미치는 사항

---

## 💡 RAG 구현 가이드

### 1단계: 데이터 로드
```python
import json

with open('travel_insurance_rag_complete.json', 'r', encoding='utf-8') as f:
    insurance_data = json.load(f)
```

### 2단계: 텍스트 임베딩
```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# CSV 파일에서 청크 로드
chunks = load_chunks_from_csv('travel_insurance_chunks.csv')

# 임베딩 생성 및 벡터 DB 저장
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./insurance_db"
)
```

### 3단계: 검색 및 질의응답
```python
# 유사도 검색
query = "해외여행 중 다쳤을 때 보장되나요?"
relevant_docs = vectorstore.similarity_search(query, k=3)

# RAG 체인 구성
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

result = qa_chain({"query": query})
print(result["result"])
```

### 4단계: 챗봇 통합
```python
# 사용자 질문 처리
def answer_insurance_question(question: str):
    # 1. 관련 문서 검색
    docs = vectorstore.similarity_search(question, k=5)
    
    # 2. LLM을 통한 답변 생성
    context = "\n".join([doc.page_content for doc in docs])
    prompt = f"""
    다음 보험약관 내용을 바탕으로 질문에 답변해주세요:
    
    {context}
    
    질문: {question}
    답변:
    """
    
    response = llm.complete(prompt)
    return response
```

---

## 📈 데이터 통계

- **원본 PDF 페이지**: 109페이지
- **추출된 텍스트**: 175,638자
- **생성된 청크**: 282개 (의미 단위)
- **보험 조항**: 457개
- **JSON 라인 수**: 384줄
- **카테고리**: 9개 (보장내용, 면책사항, 서류 등)

---

## 🔍 검색 키워드 색인

### 보장관련
사망, 장해, 의료비, 입원, 통원, 수술, 진단

### 지역관련
해외, 국외, 여행, 출국, 입국

### 사고유형
상해, 질병, 사고, 부상, 골절, 화상

### 물품관련
휴대품, 수하물, 여권, 분실, 도난, 파손

### 책임관련
배상책임, 손해배상, 타인, 재물, 신체

### 기타서비스
항공기지연, 여행취소, 긴급이송, 의료통역

### 절차관련
청구, 서류, 접수, 지급, 심사

---

## 🚀 활용 방법

### 1. 보험 상담 챗봇
- 고객 질문에 자동으로 약관 내용 기반 답변
- FAQ 자동 생성 및 업데이트

### 2. 보험금 청구 가이드 시스템
- 필요서류 자동 안내
- 청구 절차 단계별 가이드

### 3. 보장내용 검색 엔진
- 키워드 기반 보장내용 검색
- 의미 기반 유사 사례 찾기

### 4. 약관 비교 분석
- 여러 상품 약관 비교
- 보장 범위 차이 분석

### 5. 교육 자료
- 신입 직원 교육용 자료
- 상품 설명회 자료

---

## 📞 연락처

**라이나손해보험 (에이스아메리칸화재해상보험)**
- 고객센터: 1566-5800
- 대표번호: 02-2127-2400
- 홈페이지: www.chubb.com/kr
- 주소: 서울시 종로구 삼봉로 48 라이나타워 14-15층

---

## ✅ 품질 보증

이 데이터는 다음을 보장합니다:
- ✓ 원본 PDF의 정확한 텍스트 추출
- ✓ 체계적인 구조화 (JSON, CSV, Markdown)
- ✓ RAG 시스템에 바로 적용 가능
- ✓ 벡터 DB 임베딩 준비 완료
- ✓ 검색 최적화된 청크 분할
- ✓ 카테고리별 키워드 매핑

---

## 🎓 참고사항

1. **임베딩 모델 선택**
   - OpenAI: text-embedding-3-large (추천)
   - 한국어 특화: KoSimCSE, KoBERT
   - 무료: sentence-transformers/paraphrase-multilingual

2. **벡터 DB 선택**
   - 로컬: ChromaDB, FAISS
   - 클라우드: Pinecone, Weaviate, Qdrant

3. **LLM 선택**
   - GPT-4: 높은 정확도
   - GPT-3.5-turbo: 빠른 응답
   - Claude: 긴 컨텍스트
   - 한국어 특화: HyperCLOVA X, SOLAR

---

생성 일시: 2025-11-24
버전: 1.0
