<template>
  <div v-if="isOpen" class="modal-overlay" @click="handleOverlayClick">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <h2>🛡️ 보험증권 확인</h2>
        <p class="subtitle">가입하신 보험 정보를 확인해주세요</p>
      </div>

      <div class="modal-body">
        <div class="tab-buttons">
          <button
            :class="['tab-button', { active: loginMethod === 'policy' }]"
            @click="loginMethod = 'policy'"
          >
            보험증권번호
          </button>
          <button
            :class="['tab-button', { active: loginMethod === 'personal' }]"
            @click="loginMethod = 'personal'"
          >
            개인정보
          </button>
        </div>

        <!-- 보험증권번호로 로그인 -->
        <div v-if="loginMethod === 'policy'" class="form-group">
          <label>보험증권번호</label>
          <input
            v-model="policyNumber"
            type="text"
            placeholder="CHB2024-1234567"
            class="input-field"
            @keyup.enter="handleLogin"
          />
          <p class="hint">💡 데모용: CHB2024-1234567</p>
        </div>

        <!-- 개인정보로 로그인 -->
        <div v-else class="form-group">
          <label>이름</label>
          <input
            v-model="name"
            type="text"
            placeholder="김해커"
            class="input-field"
          />

          <label>생년월일</label>
          <input
            v-model="birthDate"
            type="date"
            class="input-field"
            @keyup.enter="handleLogin"
          />
          <p class="hint">💡 데모용: 김해커 / 1990-01-15</p>
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <button class="login-button" @click="handleLogin">
          확인
        </button>

        <div class="demo-notice">
          <p>📌 해커톤 데모용 앱입니다</p>
          <p>위의 샘플 정보를 사용해주세요</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { authenticateUser } from '../../data/mockUserData.js'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close', 'login'])

const loginMethod = ref('policy') // 'policy' or 'personal'
const policyNumber = ref('')
const name = ref('')
const birthDate = ref('')
const errorMessage = ref('')

const handleOverlayClick = () => {
  // 모달 외부 클릭 시 닫지 않음 (필수 입력)
}

const handleLogin = () => {
  errorMessage.value = ''

  let credentials = {}
  if (loginMethod.value === 'policy') {
    if (!policyNumber.value.trim()) {
      errorMessage.value = '보험증권번호를 입력해주세요'
      return
    }
    credentials.policyNumber = policyNumber.value.trim()
  } else {
    if (!name.value.trim() || !birthDate.value) {
      errorMessage.value = '이름과 생년월일을 모두 입력해주세요'
      return
    }
    credentials.name = name.value.trim()
    credentials.birthDate = birthDate.value
  }

  const user = authenticateUser(credentials)

  if (user) {
    emit('login', user)
    emit('close')
  } else {
    errorMessage.value = '일치하는 보험 가입 정보를 찾을 수 없습니다'
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-container {
  background: white;
  border-radius: 20px;
  width: 90%;
  max-width: 450px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: modalSlideUp 0.3s ease-out;
}

@keyframes modalSlideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  padding: 32px 24px 24px;
  text-align: center;
  border-bottom: 1px solid #f0f0f0;
}

.modal-header h2 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.subtitle {
  margin: 8px 0 0;
  font-size: 14px;
  color: #666;
}

.modal-body {
  padding: 24px;
}

.tab-buttons {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  background: #f5f5f5;
  padding: 4px;
  border-radius: 12px;
}

.tab-button {
  flex: 1;
  padding: 12px;
  border: none;
  background: transparent;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-button.active {
  background: white;
  color: #4DBFC8;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

label {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: -8px;
}

.input-field {
  padding: 14px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 15px;
  transition: all 0.2s;
}

.input-field:focus {
  outline: none;
  border-color: #4DBFC8;
  box-shadow: 0 0 0 3px rgba(77, 191, 200, 0.1);
}

.hint {
  font-size: 13px;
  color: #999;
  margin-top: -8px;
  padding-left: 4px;
}

.error-message {
  background: #fff0f0;
  border: 1px solid #ffcccc;
  color: #cc0000;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  margin-top: 16px;
}

.login-button {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #4DBFC8 0%, #3AA8B1 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 24px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(77, 191, 200, 0.3);
}

.login-button:active {
  transform: translateY(0);
}

.demo-notice {
  margin-top: 24px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 12px;
  text-align: center;
}

.demo-notice p {
  margin: 4px 0;
  font-size: 13px;
  color: #666;
}

/* 모바일 최적화 */
@media (max-width: 768px) {
  .modal-container {
    width: 95%;
    max-width: 100%;
    margin: 20px;
  }

  .modal-header {
    padding: 24px 20px 20px;
  }

  .modal-header h2 {
    font-size: 22px;
  }

  .subtitle {
    font-size: 13px;
  }

  .modal-body {
    padding: 20px;
  }

  .tab-button {
    padding: 10px;
    font-size: 13px;
  }

  .input-field {
    padding: 12px 14px;
    font-size: 14px;
  }

  .hint {
    font-size: 12px;
  }

  .login-button {
    padding: 14px;
    font-size: 15px;
  }

  .demo-notice {
    padding: 14px;
  }

  .demo-notice p {
    font-size: 12px;
  }
}

/* 작은 모바일 */
@media (max-width: 375px) {
  .modal-container {
    width: 100%;
    margin: 10px;
    border-radius: 16px;
  }

  .modal-header {
    padding: 20px 16px 16px;
  }

  .modal-header h2 {
    font-size: 20px;
  }

  .modal-body {
    padding: 16px;
  }
}
</style>
