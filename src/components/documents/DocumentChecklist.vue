<template>
  <div class="document-checklist">
    <div class="checklist-header">
      <h3>📋 필요 서류 체크리스트</h3>
      <div class="progress-info">
        <span class="completed-count">{{ completedCount }}</span>
        <span class="separator">/</span>
        <span class="total-count">{{ totalCount }}</span>
      </div>
    </div>

    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
    </div>

    <div v-for="(category, categoryIndex) in categories" :key="categoryIndex" class="category">
      <div class="category-header">
        <span class="category-icon">{{ category.icon }}</span>
        <h4>{{ category.title }}</h4>
        <span class="category-badge">{{ category.description }}</span>
      </div>

      <div class="document-list">
        <div
          v-for="(doc, docIndex) in category.documents"
          :key="docIndex"
          :class="['document-item', { checked: doc.checked }]"
          @click="toggleDocument(categoryIndex, docIndex)"
        >
          <div class="checkbox">
            <div v-if="doc.checked" class="check-icon">✓</div>
          </div>
          <div class="document-info">
            <div class="document-name">
              {{ doc.name }}
              <span v-if="doc.required" class="required-badge">필수</span>
            </div>
            <div v-if="doc.description" class="document-description">
              {{ doc.description }}
            </div>
            <div v-if="doc.howToGet" class="how-to-get">
              💡 {{ doc.howToGet }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 마케팅 동의 섹션 -->
    <div class="marketing-consent-section">
      <div
        class="marketing-consent-item"
        :class="{ checked: marketingConsent }"
        @click.stop="toggleMarketingConsent"
      >
        <div class="checkbox">
          <div v-if="marketingConsent" class="check-icon">✓</div>
        </div>
        <div class="marketing-info">
          <div class="marketing-title">
            여행 후에도 생활 전반을 보호할 수 있는 상품 정보를 받아보시겠어요?
          </div>
          <div class="marketing-description">
            보험상품 정보 수신 동의를 통해 평소 걱정됐던 부분을 든든하게 보호받으실 수 있어요
          </div>
        </div>
      </div>
    </div>

    <!-- 확인 버튼 -->
    <div class="checklist-actions">
      <button
        class="confirm-button"
        :class="{ disabled: !canConfirm }"
        @click.stop="handleConfirm"
        :disabled="!canConfirm"
      >
        청구 안내받기
      </button>
    </div>

    <!-- 필수 서류 누락 경고 -->
    <div v-if="showRequiredWarning" class="required-warning">
      ⚠️ 필수 서류가 아직 체크되지 않았어요. 필수 서류를 모두 확인해주세요.
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  categories: {
    type: Array,
    required: true,
    // Example: [{ title: '해외에서 준비', icon: '🌍', description: '현지', documents: [...] }]
  }
})

const emit = defineEmits(['update:categories', 'confirm', 'marketingConsent'])

// 마케팅 동의 상태
const marketingConsent = ref(false)
const showRequiredWarning = ref(false)

// 마케팅 동의 토글
const toggleMarketingConsent = (event) => {
  event?.preventDefault()
  event?.stopPropagation()
  marketingConsent.value = !marketingConsent.value
  console.log('DocumentChecklist - marketingConsent toggled:', marketingConsent.value)
  emit('marketingConsent', marketingConsent.value)
}

const totalCount = computed(() => {
  return props.categories.reduce((sum, category) => {
    return sum + category.documents.length
  }, 0)
})

const completedCount = computed(() => {
  return props.categories.reduce((sum, category) => {
    return sum + category.documents.filter(doc => doc.checked).length
  }, 0)
})

const progressPercentage = computed(() => {
  if (totalCount.value === 0) return 0
  return Math.round((completedCount.value / totalCount.value) * 100)
})

// 필수 서류가 모두 체크되었는지 확인
const allRequiredChecked = computed(() => {
  return props.categories.every(category =>
    category.documents
      .filter(doc => doc.required)
      .every(doc => doc.checked)
  )
})

// 확인 버튼 활성화 여부
const canConfirm = computed(() => {
  return allRequiredChecked.value
})

const toggleDocument = (categoryIndex, docIndex) => {
  console.log('DocumentChecklist - toggleDocument called:', { categoryIndex, docIndex })
  const newCategories = JSON.parse(JSON.stringify(props.categories))
  newCategories[categoryIndex].documents[docIndex].checked =
    !newCategories[categoryIndex].documents[docIndex].checked
  console.log('DocumentChecklist - emitting update:categories:', newCategories)
  emit('update:categories', newCategories)
  
  // 경고 메시지 숨기기
  if (showRequiredWarning.value) {
    showRequiredWarning.value = false
  }
}

// 확인 버튼 클릭 처리
const handleConfirm = () => {
  if (!allRequiredChecked.value) {
    showRequiredWarning.value = true
    return
  }
  
  // 확인 이벤트 발생 (마케팅 동의 정보 포함)
  emit('confirm', {
    marketingConsent: marketingConsent.value
  })
}
</script>

<style scoped>
.document-checklist {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.checklist-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.checklist-header h3 {
  margin: 0;
  font-size: 20px;
  color: #333;
}

.progress-info {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.completed-count {
  font-size: 28px;
  font-weight: 700;
  color: #4DBFC8;
}

.separator {
  font-size: 20px;
  color: #ccc;
}

.total-count {
  font-size: 20px;
  font-weight: 600;
  color: #999;
}

.progress-bar {
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 24px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4DBFC8 0%, #3AA8B1 100%);
  transition: width 0.5s ease;
}

.category {
  margin-bottom: 24px;
}

.category-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f0f0f0;
}

.category-icon {
  font-size: 24px;
}

.category-header h4 {
  margin: 0;
  font-size: 17px;
  color: #333;
  flex: 1;
}

.category-badge {
  background: #f0f0f0;
  color: #666;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.document-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.document-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: #fafafa;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.document-item:hover {
  background: #f5f5f5;
  transform: translateX(4px);
}

.document-item.checked {
  background: #e8f5e9;
  border-color: #4caf50;
}

.checkbox {
  width: 24px;
  height: 24px;
  border: 2px solid #ccc;
  border-radius: 6px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.document-item.checked .checkbox {
  background: #4caf50;
  border-color: #4caf50;
}

.check-icon {
  color: white;
  font-size: 16px;
  font-weight: 700;
}

.document-info {
  flex: 1;
}

.document-name {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.required-badge {
  background: #ff5252;
  color: white;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 700;
}

.document-description {
  font-size: 13px;
  color: #666;
  margin-bottom: 6px;
  line-height: 1.4;
}

.how-to-get {
  font-size: 12px;
  color: #4DBFC8;
  background: rgba(77, 191, 200, 0.1);
  padding: 8px 12px;
  border-radius: 8px;
  margin-top: 8px;
  line-height: 1.5;
}

.completion-message {
  text-align: center;
  padding: 32px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  color: white;
  margin-top: 24px;
  animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.completion-icon {
  font-size: 64px;
  margin-bottom: 16px;
  animation: bounce 1s infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.completion-message h3 {
  margin: 0 0 8px;
  font-size: 22px;
}

.completion-message p {
  margin: 0;
  font-size: 15px;
  opacity: 0.9;
}

/* 마케팅 동의 섹션 */
.marketing-consent-section {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 2px solid #f0f0f0;
}

.marketing-consent-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: #fafafa;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
  user-select: none;
  -webkit-user-select: none;
}

.marketing-consent-item:hover {
  background: #f5f5f5;
  border-color: #e0e0e0;
}

.marketing-consent-item.checked {
  background: #e8f5e9;
  border-color: #4caf50;
}

.marketing-consent-item.checked:hover {
  background: #d4edda;
}

.marketing-consent-item .checkbox {
  width: 24px;
  height: 24px;
  border: 2px solid #ccc;
  border-radius: 6px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.marketing-consent-item.checked .checkbox {
  background: #4caf50;
  border-color: #4caf50;
}

.marketing-consent-item .check-icon {
  color: white;
  font-size: 16px;
  font-weight: 700;
}

.marketing-info {
  flex: 1;
}

.marketing-title {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
  line-height: 1.4;
}

.marketing-description {
  font-size: 13px;
  color: #666;
  line-height: 1.4;
}

/* 확인 버튼 섹션 */
.checklist-actions {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}

.confirm-button {
  background: linear-gradient(135deg, #4DBFC8 0%, #3AA8B1 100%);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 16px 48px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(77, 191, 200, 0.3);
}

.confirm-button:hover:not(.disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(77, 191, 200, 0.4);
}

.confirm-button.disabled {
  background: #e0e0e0;
  color: #999;
  cursor: not-allowed;
  box-shadow: none;
}

/* 필수 서류 누락 경고 */
.required-warning {
  margin-top: 16px;
  padding: 12px 16px;
  background: #fff3cd;
  border: 2px solid #ffc107;
  border-radius: 12px;
  color: #856404;
  font-size: 14px;
  font-weight: 500;
  text-align: center;
  animation: shake 0.5s;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
  20%, 40%, 60%, 80% { transform: translateX(5px); }
}

@media (max-width: 768px) {
  .document-checklist {
    padding: 16px;
  }

  .checklist-header h3 {
    font-size: 18px;
  }

  .document-item {
    padding: 12px;
  }

  .confirm-button {
    padding: 14px 32px;
    font-size: 15px;
  }

  .marketing-consent-item {
    padding: 12px;
  }
}
</style>
