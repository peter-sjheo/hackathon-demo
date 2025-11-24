<template>
  <div class="claim-timeline">
    <div class="timeline-header">
      <h3>📅 보험금 청구 타임라인</h3>
      <p class="subtitle">예상 처리 기간 및 절차를 안내해드립니다</p>
    </div>

    <div class="timeline">
      <div
        v-for="(event, index) in events"
        :key="index"
        :class="['timeline-event', event.status]"
      >
        <div class="timeline-marker">
          <div class="marker-dot"></div>
          <div v-if="index < events.length - 1" class="marker-line"></div>
        </div>

        <div class="event-card">
          <div class="event-header">
            <div class="event-icon">{{ event.icon }}</div>
            <div class="event-info">
              <h4>{{ event.title }}</h4>
              <p class="event-date">{{ event.date || event.estimatedDate }}</p>
            </div>
            <div v-if="event.status" class="status-badge" :class="event.status">
              {{ getStatusText(event.status) }}
            </div>
          </div>

          <div v-if="event.description" class="event-description">
            {{ event.description }}
          </div>

          <div v-if="event.details && event.details.length > 0" class="event-details">
            <ul>
              <li v-for="(detail, idx) in event.details" :key="idx">
                {{ detail }}
              </li>
            </ul>
          </div>

          <div v-if="event.action" class="event-action">
            <button class="action-button" @click="handleAction(event.action)">
              {{ event.action.label }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="timeline-footer">
      <div class="info-box">
        <div class="info-icon">ℹ️</div>
        <div class="info-content">
          <p><strong>청구 기한:</strong> 사고 발생일로부터 3년 이내</p>
          <p><strong>처리 기간:</strong> 서류 접수 후 영업일 기준 10일 이내</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  events: {
    type: Array,
    required: true,
    // Example: [{
    //   title: '사고 발생',
    //   icon: '⚠️',
    //   date: '2024-11-20',
    //   status: 'completed',
    //   description: '...',
    //   details: ['...'],
    //   action: { label: '...', type: '...' }
    // }]
  }
})

const emit = defineEmits(['action'])

const getStatusText = (status) => {
  const statusMap = {
    completed: '완료',
    inProgress: '진행중',
    pending: '대기',
    upcoming: '예정'
  }
  return statusMap[status] || status
}

const handleAction = (action) => {
  emit('action', action)
}
</script>

<style scoped>
.claim-timeline {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.timeline-header {
  margin-bottom: 32px;
}

.timeline-header h3 {
  margin: 0 0 8px;
  font-size: 20px;
  color: #333;
}

.subtitle {
  margin: 0;
  font-size: 14px;
  color: #666;
}

.timeline {
  position: relative;
}

.timeline-event {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
}

.timeline-event:last-child {
  margin-bottom: 0;
}

.timeline-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.marker-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #e0e0e0;
  border: 3px solid white;
  box-shadow: 0 0 0 2px #e0e0e0;
  transition: all 0.3s;
}

.timeline-event.completed .marker-dot {
  background: #4caf50;
  box-shadow: 0 0 0 2px #4caf50;
}

.timeline-event.inProgress .marker-dot {
  background: #4DBFC8;
  box-shadow: 0 0 0 2px #4DBFC8;
  animation: pulse 2s infinite;
}

.timeline-event.pending .marker-dot {
  background: #ff9800;
  box-shadow: 0 0 0 2px #ff9800;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
}

.marker-line {
  width: 2px;
  flex: 1;
  min-height: 40px;
  background: #e0e0e0;
  margin-top: 8px;
}

.timeline-event.completed .marker-line {
  background: #4caf50;
}

.timeline-event.inProgress .marker-line {
  background: linear-gradient(180deg, #4DBFC8 0%, #e0e0e0 100%);
}

.event-card {
  flex: 1;
  background: #fafafa;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.timeline-event.completed .event-card {
  background: #f1f8f4;
  border-color: #4caf50;
}

.timeline-event.inProgress .event-card {
  background: #f0f9fa;
  border-color: #4DBFC8;
  box-shadow: 0 4px 12px rgba(77, 191, 200, 0.15);
}

.event-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.event-icon {
  font-size: 32px;
  line-height: 1;
}

.event-info {
  flex: 1;
}

.event-info h4 {
  margin: 0 0 4px;
  font-size: 16px;
  color: #333;
}

.event-date {
  margin: 0;
  font-size: 13px;
  color: #999;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.status-badge.completed {
  background: #4caf50;
  color: white;
}

.status-badge.inProgress {
  background: #4DBFC8;
  color: white;
}

.status-badge.pending {
  background: #ff9800;
  color: white;
}

.status-badge.upcoming {
  background: #e0e0e0;
  color: #666;
}

.event-description {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 12px;
}

.event-details ul {
  margin: 0;
  padding-left: 20px;
  font-size: 13px;
  color: #666;
  line-height: 1.8;
}

.event-details li {
  margin-bottom: 4px;
}

.event-action {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.action-button {
  background: #4DBFC8;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.action-button:hover {
  background: #3AA8B1;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(77, 191, 200, 0.3);
}

.timeline-footer {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 2px solid #f0f0f0;
}

.info-box {
  display: flex;
  gap: 16px;
  background: #fff9e6;
  border: 2px solid #ffe066;
  border-radius: 12px;
  padding: 16px;
}

.info-icon {
  font-size: 24px;
}

.info-content p {
  margin: 0 0 8px;
  font-size: 13px;
  color: #666;
  line-height: 1.6;
}

.info-content p:last-child {
  margin-bottom: 0;
}

.info-content strong {
  color: #333;
}

@media (max-width: 768px) {
  .claim-timeline {
    padding: 16px;
  }

  .timeline-event {
    gap: 12px;
  }

  .event-card {
    padding: 16px;
  }

  .event-icon {
    font-size: 24px;
  }
}
</style>
