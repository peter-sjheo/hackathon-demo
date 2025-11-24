// 메시지 타입 상수 정의
export const MessageType = {
  TEXT: 'text',                    // 텍스트 메시지
  MAP: 'map',                      // 지도 메시지
  DOCUMENT_LIST: 'document_list',  // 서류 리스트
  ACTION_BUTTONS: 'action_buttons', // 액션 버튼
  SCRIPT: 'script',                // 스크립트 (음성 읽기 포함)
  CHECKLIST: 'checklist',          // 서류 체크리스트
  TIMELINE: 'timeline'             // 청구 타임라인
}

// 메시지 발신자 타입
export const SenderType = {
  USER: 'user',          // 사용자 메시지
  BOT: 'bot'             // 봇 응답
}
