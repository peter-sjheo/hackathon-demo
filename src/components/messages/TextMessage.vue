<template>
  <div class="text-message">
    <!-- 텍스트 메시지 내용 -->
    <p v-html="formattedContent"></p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// 부모로부터 메시지 내용을 받음
const props = defineProps({
  content: {
    type: String,
    required: true
  }
})

// **텍스트** 패턴을 <strong>태그로 변환
const formattedContent = computed(() => {
  if (!props.content) return ''
  
  // **텍스트** 패턴을 <strong>텍스트</strong>로 변환
  // 단, **가 연속으로 3개 이상일 때는 제외 (이미 볼드 처리된 텍스트)
  return props.content
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
})
</script>

<style scoped>
.text-message {
  padding: 12px 16px;
  border-radius: 18px;
  background: white;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.text-message p {
  margin: 0;
  line-height: 1.5;
  color: #333;
  word-break: break-word;
  font-size: 14px;
}

.text-message p :deep(strong) {
  font-weight: 700;
  color: inherit;
}
</style>
