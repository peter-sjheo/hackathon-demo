"""
해외여행보험 RAG 시스템 활용 예제

이 파일은 추출된 보험 데이터를 RAG(Retrieval-Augmented Generation) 시스템에서
활용하는 방법을 보여주는 예제 코드입니다.
"""

import json
from typing import List, Dict, Any
import re


class TravelInsuranceRAG:
    """해외여행보험 RAG 시스템"""
    
    def __init__(self, json_path: str):
        """
        Args:
            json_path: RAG 데이터 JSON 파일 경로
        """
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.chunks = self._load_chunks()
    
    def _load_chunks(self) -> List[Dict]:
        """청크 데이터 로드"""
        if "청크샘플" in self.data:
            return self.data["청크샘플"]
        return []
    
    def search_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """
        키워드로 관련 정보 검색
        
        Args:
            keyword: 검색할 키워드
            
        Returns:
            관련 정보 리스트
        """
        results = []
        keyword_lower = keyword.lower()
        
        # 보장내용 검색
        for coverage in self.data.get("보장내용", []):
            if keyword_lower in str(coverage).lower():
                results.append({
                    "category": "보장내용",
                    "data": coverage
                })
        
        # 면책사항 검색
        for exclusion in self.data.get("면책사항", []):
            if keyword_lower in exclusion.lower():
                results.append({
                    "category": "면책사항",
                    "data": exclusion
                })
        
        # FAQ 검색
        for faq in self.data.get("FAQ", []):
            if keyword_lower in faq["질문"].lower() or keyword_lower in faq["답변"].lower():
                results.append({
                    "category": "FAQ",
                    "data": faq
                })
        
        return results
    
    def get_coverage_info(self, coverage_type: str = None) -> List[Dict]:
        """
        보장내용 조회
        
        Args:
            coverage_type: 특정 보장 구분 (None이면 전체)
            
        Returns:
            보장내용 리스트
        """
        coverages = self.data.get("보장내용", [])
        
        if coverage_type:
            return [c for c in coverages if coverage_type in c.get("구분", "")]
        
        return coverages
    
    def get_required_documents(self, claim_type: str = None) -> Dict:
        """
        필요서류 조회
        
        Args:
            claim_type: 청구 유형 (예: "사망보험금", "의료비보험금")
            
        Returns:
            필요서류 딕셔너리
        """
        documents = self.data.get("필요서류", {})
        
        if claim_type:
            return {claim_type: documents.get(claim_type, [])}
        
        return documents
    
    def get_exclusions(self) -> List[str]:
        """면책사항 조회"""
        return self.data.get("면책사항", [])
    
    def get_faq(self, query: str = None) -> List[Dict]:
        """
        FAQ 조회
        
        Args:
            query: 검색 쿼리 (None이면 전체)
            
        Returns:
            FAQ 리스트
        """
        faqs = self.data.get("FAQ", [])
        
        if query:
            query_lower = query.lower()
            return [
                faq for faq in faqs 
                if query_lower in faq["질문"].lower() or 
                   query_lower in faq["답변"].lower()
            ]
        
        return faqs
    
    def get_claim_process(self) -> Dict:
        """보험금 청구 절차 조회"""
        return self.data.get("청구절차", {})
    
    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        의미 기반 검색 (간단한 키워드 매칭 버전)
        실제 프로덕션에서는 임베딩 벡터와 유사도 검색 사용
        
        Args:
            query: 검색 쿼리
            top_k: 상위 k개 결과 반환
            
        Returns:
            관련도 높은 청크 리스트
        """
        query_lower = query.lower()
        query_terms = query_lower.split()
        
        scored_chunks = []
        for chunk in self.chunks:
            content = chunk.get("content", "").lower()
            title = chunk.get("title", "").lower()
            
            # 간단한 점수 계산 (실제로는 임베딩 유사도 사용)
            score = 0
            for term in query_terms:
                score += content.count(term) * 2  # 내용 매칭
                score += title.count(term) * 5    # 제목 매칭은 가중치 더 높게
            
            if score > 0:
                scored_chunks.append({
                    "chunk": chunk,
                    "score": score
                })
        
        # 점수순 정렬
        scored_chunks.sort(key=lambda x: x["score"], reverse=True)
        
        return [item["chunk"] for item in scored_chunks[:top_k]]
    
    def get_category_keywords(self) -> Dict[str, List[str]]:
        """카테고리별 키워드 매핑 조회"""
        return self.data.get("카테고리_키워드매핑", {})
    
    def get_contact_info(self) -> Dict:
        """연락처 정보 조회"""
        return self.data.get("문서정보", {}).get("연락처", {})


# 사용 예제
def main():
    """RAG 시스템 사용 예제"""
    
    # RAG 시스템 초기화
    rag = TravelInsuranceRAG("travel_insurance_rag_complete.json")
    
    print("=" * 60)
    print("해외여행보험 RAG 시스템 예제")
    print("=" * 60)
    
    # 1. 키워드 검색
    print("\n[1] 키워드 검색: '의료비'")
    results = rag.search_by_keyword("의료비")
    for result in results[:3]:
        print(f"  - 카테고리: {result['category']}")
        print(f"    데이터: {result['data']}")
    
    # 2. 보장내용 조회
    print("\n[2] 보장내용 전체 조회")
    coverages = rag.get_coverage_info()
    for coverage in coverages[:3]:
        print(f"  - {coverage['구분']}: {coverage['지급사유']}")
    
    # 3. 필요서류 조회
    print("\n[3] 의료비보험금 청구 필요서류")
    docs = rag.get_required_documents("의료비보험금")
    for doc_type, doc_list in docs.items():
        print(f"  {doc_type}:")
        for doc in doc_list:
            print(f"    - {doc}")
    
    # 4. 면책사항 조회
    print("\n[4] 면책사항 (일부)")
    exclusions = rag.get_exclusions()
    for exclusion in exclusions[:5]:
        print(f"  - {exclusion}")
    
    # 5. FAQ 검색
    print("\n[5] FAQ 검색: '서류'")
    faqs = rag.get_faq("서류")
    for faq in faqs:
        print(f"  Q: {faq['질문']}")
        print(f"  A: {faq['답변']}")
    
    # 6. 의미 기반 검색
    print("\n[6] 의미 기반 검색: '사고가 났을 때 어떻게 하나요'")
    chunks = rag.semantic_search("사고가 났을 때 어떻게 하나요", top_k=3)
    for i, chunk in enumerate(chunks, 1):
        print(f"  [{i}] {chunk['title']}")
        print(f"      {chunk['content'][:100]}...")
    
    # 7. 청구 절차
    print("\n[7] 보험금 청구 절차")
    process = rag.get_claim_process()
    for step in process.get("절차", []):
        print(f"  {step['단계']}. {step['내용']}: {step['설명']}")
    
    # 8. 연락처 정보
    print("\n[8] 고객센터 연락처")
    contact = rag.get_contact_info()
    print(f"  고객센터: {contact.get('고객센터')}")
    print(f"  대표번호: {contact.get('대표번호')}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()


# ============================================================
# 벡터 DB 연동 예제 (LangChain + ChromaDB)
# ============================================================

"""
실제 프로덕션 환경에서는 아래와 같이 벡터 DB를 사용합니다:

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import JSONLoader

# 1. JSON 데이터 로드
loader = JSONLoader(
    file_path="travel_insurance_rag_complete.json",
    jq_schema=".text_chunks[]",
    text_content=False
)
documents = loader.load()

# 2. 텍스트 분할
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(documents)

# 3. 임베딩 및 벡터 저장
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 4. 검색
query = "해외여행 중 다쳤을 때 보장되나요?"
docs = vectorstore.similarity_search(query, k=3)

for doc in docs:
    print(doc.page_content)
"""


# ============================================================
# 챗봇 통합 예제 (LangChain + OpenAI)
# ============================================================

"""
RAG 기반 보험 상담 챗봇:

from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# RAG 체인 구성
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

# 질문 답변
query = "해외여행보험에서 보장하지 않는 경우는 어떤 것이 있나요?"
result = qa_chain({"query": query})

print("답변:", result["result"])
print("\n참조 문서:")
for doc in result["source_documents"]:
    print(f"- {doc.page_content[:200]}...")
"""
