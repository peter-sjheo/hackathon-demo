<template>
  <div class="progress-bar-container">
    <div class="steps-horizontal">
      <div
        v-for="(step, index) in steps"
        :key="index"
        :class="['step-item', {
          active: index === currentStep,
          completed: index < currentStep
        }]"
      >
        <div class="step-dot"></div>
        <div class="step-label">{{ step.title }}</div>
      </div>
    </div>
    <div class="progress-line">
      <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentStep: {
    type: Number,
    required: true,
    default: 0
  },
  steps: {
    type: Array,
    required: true
  }
})

const progressPercentage = computed(() => {
  if (props.steps.length === 0) return 0
  return (props.currentStep / (props.steps.length - 1)) * 100
})
</script>

<style scoped>
.progress-bar-container {
  background: white;
  padding: 12px 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.steps-horizontal {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  position: relative;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  flex: 1;
  position: relative;
  z-index: 2;
}

.step-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #e0e0e0;
  transition: all 0.3s;
}

.step-item.active .step-dot {
  width: 16px;
  height: 16px;
  background: #4DBFC8;
  box-shadow: 0 0 0 4px rgba(77, 191, 200, 0.2);
  animation: pulse-dot 2s infinite;
}

.step-item.completed .step-dot {
  background: #4caf50;
  width: 14px;
  height: 14px;
}

@keyframes pulse-dot {
  0%, 100% {
    box-shadow: 0 0 0 4px rgba(77, 191, 200, 0.2);
  }
  50% {
    box-shadow: 0 0 0 6px rgba(77, 191, 200, 0.1);
  }
}

.step-label {
  font-size: 11px;
  color: #999;
  text-align: center;
  white-space: nowrap;
  transition: all 0.3s;
}

.step-item.active .step-label {
  color: #4DBFC8;
  font-weight: 600;
  font-size: 12px;
}

.step-item.completed .step-label {
  color: #666;
}

.progress-line {
  height: 3px;
  background: #f0f0f0;
  border-radius: 2px;
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4DBFC8 0%, #3AA8B1 100%);
  transition: width 0.5s ease;
  border-radius: 2px;
}

/* 모바일 */
@media (max-width: 768px) {
  .progress-bar-container {
    padding: 10px 12px;
  }

  .step-label {
    font-size: 10px;
  }

  .step-item.active .step-label {
    font-size: 11px;
  }

  .step-dot {
    width: 10px;
    height: 10px;
  }

  .step-item.active .step-dot {
    width: 14px;
    height: 14px;
  }

  .step-item.completed .step-dot {
    width: 12px;
    height: 12px;
  }
}

/* 작은 모바일 */
@media (max-width: 480px) {
  .step-label {
    font-size: 9px;
    max-width: 60px;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .step-item.active .step-label {
    font-size: 10px;
  }

  .steps-horizontal {
    gap: 4px;
  }
}
</style>
