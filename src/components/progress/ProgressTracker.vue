<template>
  <div class="progress-tracker">
    <div class="steps">
      <div
        v-for="(step, index) in steps"
        :key="index"
        :class="['step', {
          active: index === currentStep,
          completed: index < currentStep
        }]"
      >
        <div class="step-indicator">
          <div class="step-number" v-if="index >= currentStep">{{ index + 1 }}</div>
          <div class="step-check" v-else>✓</div>
        </div>
        <div class="step-content">
          <div class="step-title">{{ step.title }}</div>
          <div class="step-description">{{ step.description }}</div>
        </div>
        <div v-if="index < steps.length - 1" class="step-connector"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  currentStep: {
    type: Number,
    required: true,
    default: 0
  },
  steps: {
    type: Array,
    required: true,
    // Example: [{ title: '사고 접수', description: '상황 파악 중' }, ...]
  }
})
</script>

<style scoped>
.progress-tracker {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 24px;
}

.steps {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.step {
  display: flex;
  align-items: flex-start;
  position: relative;
  transition: all 0.3s;
}

.step-indicator {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.3s;
  z-index: 2;
}

.step.active .step-indicator {
  background: linear-gradient(135deg, #4DBFC8 0%, #3AA8B1 100%);
  box-shadow: 0 4px 12px rgba(77, 191, 200, 0.4);
  animation: pulse-ring 2s infinite;
}

.step.completed .step-indicator {
  background: #4caf50;
}

@keyframes pulse-ring {
  0% {
    box-shadow: 0 0 0 0 rgba(77, 191, 200, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(77, 191, 200, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(77, 191, 200, 0);
  }
}

.step-number {
  font-size: 16px;
  font-weight: 700;
  color: #999;
}

.step.active .step-number {
  color: white;
}

.step-check {
  font-size: 20px;
  color: white;
  font-weight: 700;
}

.step-content {
  margin-left: 16px;
  flex: 1;
}

.step-title {
  font-size: 16px;
  font-weight: 600;
  color: #999;
  margin-bottom: 4px;
  transition: all 0.3s;
}

.step.active .step-title {
  color: #333;
  font-size: 17px;
}

.step.completed .step-title {
  color: #666;
}

.step-description {
  font-size: 13px;
  color: #aaa;
  transition: all 0.3s;
}

.step.active .step-description {
  color: #666;
}

.step-connector {
  position: absolute;
  left: 20px;
  top: 40px;
  width: 2px;
  height: calc(100% + 20px);
  background: #e0e0e0;
  z-index: 1;
}

.step.active .step-connector {
  background: linear-gradient(180deg, #4DBFC8 0%, #e0e0e0 100%);
}

.step.completed .step-connector {
  background: #4caf50;
}

@media (max-width: 768px) {
  .progress-tracker {
    padding: 16px;
  }

  .step-indicator {
    width: 36px;
    height: 36px;
  }

  .step-number {
    font-size: 14px;
  }

  .step-content {
    margin-left: 12px;
  }

  .step-title {
    font-size: 14px;
  }

  .step-description {
    font-size: 12px;
  }

  .step-connector {
    left: 18px;
  }
}
</style>
