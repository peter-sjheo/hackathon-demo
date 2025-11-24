<template>
  <div class="dashboard">
    <!-- 도움 섹션을 최상단으로 이동 -->
    <div class="help-section">
      <div class="help-card">
        <div class="help-icon">🆘</div>
        <div class="help-content">
          <h3>도움이 필요하신가요?</h3>
          <p>여행 중 사고가 발생하셨나요? 지금 바로 도와드리겠습니다.</p>
          <button class="help-button" @click="handleStartClaim">
            사고 접수하기
          </button>
        </div>
      </div>
    </div>

    <div class="header">
      <div class="user-info">
        <h2>안녕하세요, <span class="highlight">{{ user.name }}</span>님!</h2>
        <p class="trip-info">{{ user.insurance.destination }} 여행을 응원합니다 ✈️</p>
      </div>
      <div class="period-badge">
        <span class="label">보험 기간</span>
        <span class="dates">{{ formatDate(user.insurance.startDate) }} ~ {{ formatDate(user.insurance.endDate) }}</span>
      </div>
    </div>

    <div class="product-card">
      <div class="product-header">
        <div>
          <h3>{{ user.insurance.productName }}</h3>
          <p class="policy-number">증권번호: {{ user.policyNumber }}</p>
        </div>
        <div class="status-badge">
          <span class="dot"></span>
          보장중
        </div>
      </div>
    </div>

    <div class="section-header">
      <h3>💼 보장 내용</h3>
      <p>가입하신 보험으로 보장받을 수 있는 항목입니다</p>
    </div>

    <div class="coverage-grid">
      <div
        v-for="(coverage, index) in user.insurance.coverages"
        :key="index"
        class="coverage-card"
      >
        <div class="coverage-icon">{{ coverage.icon }}</div>
        <div class="coverage-info">
          <h4>{{ coverage.name }}</h4>
          <p class="description">{{ coverage.description }}</p>
          <div class="coverage-limit">
            <span class="label">보장 한도</span>
            <span class="amount">{{ coverage.limit }}</span>
          </div>
          <div v-if="coverage.deductible" class="deductible">
            자기부담금: {{ coverage.deductible }}
          </div>
        </div>
      </div>
    </div>

    <div class="quick-links">
      <button class="link-button">
        <span class="icon">📞</span>
        <span>고객센터</span>
      </button>
      <button class="link-button">
        <span class="icon">📄</span>
        <span>약관 보기</span>
      </button>
      <button class="link-button">
        <span class="icon">❓</span>
        <span>FAQ</span>
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  user: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['startClaim'])

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  const month = date.getMonth() + 1
  const day = date.getDate()
  return `${month}/${day}`
}

const handleStartClaim = () => {
  emit('startClaim')
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.user-info h2 {
  margin: 0 0 8px;
  font-size: 24px;
  color: #333;
}

.highlight {
  color: #4DBFC8;
  font-weight: 700;
}

.trip-info {
  margin: 0;
  font-size: 15px;
  color: #666;
}

.period-badge {
  background: linear-gradient(135deg, #4DBFC8 0%, #3AA8B1 100%);
  color: white;
  padding: 12px 20px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  box-shadow: 0 4px 12px rgba(77, 191, 200, 0.2);
}

.period-badge .label {
  font-size: 12px;
  opacity: 0.9;
}

.period-badge .dates {
  font-size: 14px;
  font-weight: 600;
}

.product-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 32px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.product-header h3 {
  margin: 0 0 8px;
  font-size: 18px;
  color: #333;
}

.policy-number {
  margin: 0;
  font-size: 13px;
  color: #999;
  font-family: monospace;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #e8f5e9;
  color: #2e7d32;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.status-badge .dot {
  width: 8px;
  height: 8px;
  background: #4caf50;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.section-header {
  margin-bottom: 20px;
}

.section-header h3 {
  margin: 0 0 8px;
  font-size: 20px;
  color: #333;
}

.section-header p {
  margin: 0;
  font-size: 14px;
  color: #666;
}

.coverage-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}

.coverage-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s, box-shadow 0.2s;
  border: 2px solid transparent;
}

.coverage-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  border-color: #4DBFC8;
}

.coverage-icon {
  font-size: 36px;
  margin-bottom: 12px;
}

.coverage-info h4 {
  margin: 0 0 8px;
  font-size: 16px;
  color: #333;
}

.description {
  margin: 0 0 12px;
  font-size: 13px;
  color: #666;
  line-height: 1.5;
}

.coverage-limit {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-top: 12px;
}

.coverage-limit .label {
  font-size: 13px;
  color: #666;
}

.coverage-limit .amount {
  font-size: 15px;
  font-weight: 700;
  color: #4DBFC8;
}

.deductible {
  margin-top: 8px;
  font-size: 12px;
  color: #999;
  padding-left: 12px;
}

.help-section {
  margin-bottom: 32px;
}

.help-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  padding: 32px;
  display: flex;
  gap: 24px;
  align-items: center;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
}

.help-icon {
  font-size: 64px;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
}

.help-content {
  flex: 1;
}

.help-content h3 {
  margin: 0 0 8px;
  font-size: 22px;
  color: white;
}

.help-content p {
  margin: 0 0 20px;
  font-size: 15px;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
}

.help-button {
  background: white;
  color: #667eea;
  border: none;
  padding: 14px 32px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.help-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
}

.help-button:active {
  transform: translateY(0);
}

.quick-links {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.link-button {
  flex: 1;
  min-width: 120px;
  background: white;
  border: 2px solid #e0e0e0;
  padding: 16px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.link-button:hover {
  border-color: #4DBFC8;
  background: #f8fffe;
  transform: translateY(-2px);
}

.link-button .icon {
  font-size: 24px;
}

.link-button span:last-child {
  font-size: 13px;
  font-weight: 500;
  color: #666;
}

/* 모바일 최적화 */
@media (max-width: 768px) {
  .dashboard {
    padding: 12px;
  }

  .header {
    flex-direction: column;
    margin-bottom: 16px;
  }

  .user-info h2 {
    font-size: 20px;
  }

  .trip-info {
    font-size: 14px;
  }

  .period-badge {
    width: 100%;
    padding: 10px 16px;
    align-items: center;
    flex-direction: row;
    justify-content: space-between;
  }

  .period-badge .label {
    font-size: 13px;
  }

  .period-badge .dates {
    font-size: 13px;
  }

  .product-card {
    padding: 16px;
    margin-bottom: 20px;
  }

  .product-header {
    flex-direction: column;
    gap: 12px;
  }

  .product-header h3 {
    font-size: 16px;
  }

  .status-badge {
    align-self: flex-start;
  }

  .section-header h3 {
    font-size: 18px;
  }

  .section-header p {
    font-size: 13px;
  }

  .coverage-grid {
    grid-template-columns: 1fr;
    gap: 12px;
    margin-bottom: 20px;
  }

  .coverage-card {
    padding: 16px;
  }

  .coverage-icon {
    font-size: 32px;
  }

  .coverage-info h4 {
    font-size: 15px;
  }

  .description {
    font-size: 12px;
  }

  .coverage-limit {
    padding: 8px 10px;
  }

  .coverage-limit .label {
    font-size: 12px;
  }

  .coverage-limit .amount {
    font-size: 14px;
  }

  .help-section {
    margin-bottom: 20px;
  }

  .help-card {
    flex-direction: column;
    text-align: center;
    padding: 24px 20px;
  }

  .help-icon {
    font-size: 56px;
  }

  .help-content h3 {
    font-size: 20px;
  }

  .help-content p {
    font-size: 14px;
    margin-bottom: 16px;
  }

  .help-button {
    width: 100%;
    padding: 16px 24px;
    font-size: 15px;
  }

  .quick-links {
    gap: 8px;
  }

  .link-button {
    min-width: 100px;
    padding: 14px 12px;
  }

  .link-button .icon {
    font-size: 20px;
  }

  .link-button span:last-child {
    font-size: 12px;
  }
}

/* 더 작은 모바일 (iPhone SE 등) */
@media (max-width: 375px) {
  .dashboard {
    padding: 10px;
  }

  .user-info h2 {
    font-size: 18px;
  }

  .help-card {
    padding: 20px 16px;
  }

  .help-content h3 {
    font-size: 18px;
  }

  .coverage-card {
    padding: 14px;
  }

  .quick-links {
    flex-direction: column;
  }

  .link-button {
    width: 100%;
  }
}
</style>
