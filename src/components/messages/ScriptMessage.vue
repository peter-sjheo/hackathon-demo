<template>
  <div class="script-message">
    <!-- 헤더 -->
    <div class="script-header">
      <span class="script-icon">{{ scriptIcon }}</span>
      <div class="script-title">
        <h3>{{ currentScript.title }}</h3>
        <p class="subtitle">{{ institutionType === 'police' ? '경찰서 방문 스크립트' : '병원 방문 스크립트' }}</p>
      </div>
    </div>

    <!-- 언어 선택 -->
    <div class="language-selector">
      <label>스크립트 언어 선택:</label>
      <div class="language-buttons">
        <button
          v-for="lang in supportedLanguages"
          :key="lang.code"
          class="language-button"
          :class="{ active: selectedLanguage === lang.code }"
          @click="changeLanguage(lang.code)"
        >
          <span class="flag">{{ lang.flag }}</span>
          <span class="lang-name">{{ lang.name }}</span>
        </button>
      </div>
    </div>

    <!-- 번역 중 표시 -->
    <div v-if="isTranslating" class="translating-indicator">
      <div class="spinner"></div>
      <span class="status-text">스크립트를 번역하고 있습니다...</span>
    </div>

    <!-- 스크립트 내용 -->
    <div class="script-content" v-show="!isTranslating">
      <!-- 정돈 중일 때 로딩 표시 -->
      <div v-if="isRefining" class="refining-indicator">
        <p>✨ 스크립트를 자연스럽게 다듬는 중...</p>
      </div>
      
      <!-- 정돈된 스크립트가 있으면 전체 텍스트로 표시, 없으면 필드별로 표시 -->
      <div v-if="refinedScript && refinedScript.fullText" class="refined-script-full">
        <div class="script-section">
          <p v-html="refinedScript.fullText.replace(/\n\n/g, '<br><br>')"></p>
        </div>
      </div>
      <div v-else class="script-sections">
        <div class="script-section">
          <strong>1. 인사:</strong>
          <p>{{ (refinedScript || currentScript).greeting }}</p>
        </div>
        <div class="script-section">
          <strong>2. 주요 요청:</strong>
          <p>{{ (refinedScript || currentScript).main }}</p>
        </div>
        <div v-if="(refinedScript || currentScript).symptoms" class="script-section">
          <strong>3. 증상:</strong>
          <p>{{ (refinedScript || currentScript).symptoms }}</p>
        </div>
        <div v-if="(refinedScript || currentScript).items" class="script-section">
          <strong>3. 물품:</strong>
          <p>{{ (refinedScript || currentScript).items }}</p>
        </div>
        <div v-if="(refinedScript || currentScript).date" class="script-section">
          <strong>{{ (refinedScript || currentScript).symptoms ? '4' : '4' }}. 날짜 및 시간:</strong>
          <p>{{ (refinedScript || currentScript).date }}</p>
        </div>
        <div v-if="(refinedScript || currentScript).location" class="script-section">
          <strong>{{ (refinedScript || currentScript).symptoms ? '5' : '5' }}. 위치:</strong>
          <p>{{ (refinedScript || currentScript).location }}</p>
        </div>
        <div v-if="(refinedScript || currentScript).documents" class="script-section">
          <strong>4. 필요 서류:</strong>
          <p>{{ (refinedScript || currentScript).documents }}</p>
        </div>
        <div v-if="(refinedScript || currentScript).insurance" class="script-section">
          <strong>5. 보험 정보:</strong>
          <p>{{ (refinedScript || currentScript).insurance }}</p>
        </div>
        <div v-if="(refinedScript || currentScript).payment" class="script-section">
          <strong>6. 결제:</strong>
          <p>{{ (refinedScript || currentScript).payment }}</p>
        </div>
        <div class="script-section">
          <strong>{{ institutionType === 'hospital' ? '7' : '6' }}. 마무리:</strong>
          <p>{{ (refinedScript || currentScript).closing }}</p>
        </div>
      </div>
    </div>

    <!-- 음성 읽기 컨트롤 -->
    <div class="audio-controls">
      <div class="control-header">
        <span class="audio-icon">🔊</span>
        <span class="control-label">음성으로 읽어드릴까요?</span>
      </div>
      <div class="control-buttons">
        <button
          v-if="!isPlaying && !isPaused && !isGenerating"
          class="control-button play"
          @click="playScript"
        >
          <span class="icon">▶</span>
          <span>음성 재생 (AI 음성)</span>
        </button>
        <button
          v-if="isGenerating"
          class="control-button generating"
          disabled
        >
          <span class="icon">⏳</span>
          <span>AI 음성 생성 중...</span>
        </button>
        <button
          v-if="isPlaying"
          class="control-button pause"
          @click="pauseScript"
        >
          <span class="icon">⏸</span>
          <span>일시정지</span>
        </button>
        <button
          v-if="isPaused"
          class="control-button resume"
          @click="resumeScript"
        >
          <span class="icon">▶</span>
          <span>재개</span>
        </button>
        <button
          v-if="isPlaying || isPaused"
          class="control-button stop"
          @click="stopScript"
        >
          <span class="icon">⏹</span>
          <span>정지</span>
        </button>
      </div>
      <div v-if="isGenerating" class="generating-indicator">
        <div class="spinner"></div>
        <span class="status-text">OpenAI로 고품질 AI 음성 생성 중...</span>
      </div>
      <div v-if="isPlaying" class="playing-indicator">
        <div class="wave">
          <span></span>
          <span></span>
          <span></span>
          <span></span>
        </div>
        <span class="status-text">AI 음성 재생 중...</span>
      </div>
      <div v-if="error" class="error-message">
        ⚠️ {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { INSTITUTION_SCRIPTS, SUPPORTED_LANGUAGES, SCRIPT_ICONS } from '../../data/institutionScripts.js'
import { generateSpeech, getVoiceForLanguage, translateText, refineScript } from '../../services/openai.js'

const props = defineProps({
  content: {
    type: Object,
    required: true
    // content: { institutionType: 'police' | 'hospital', defaultLanguage: 'en', personalizedData: {...} }
  }
})

// 수집된 개인정보
const personalizedData = computed(() => props.content.personalizedData || {})

// 원본 사고 내용
const originalAccidentDescription = computed(() => props.content.originalAccidentDescription || '')

// 번역된 개인정보 (언어별로 캐싱)
const translatedData = ref({})

// 정돈된 스크립트 (언어별로 캐싱)
const refinedScripts = ref({})

// 상태 관리
const selectedLanguage = ref(props.content.defaultLanguage || 'en')
const isPlaying = ref(false)
const isPaused = ref(false)
const isGenerating = ref(false)
const isTranslating = ref(false)
const isRefining = ref(false)
const error = ref(null)

// 오디오 관련
let audioElement = null
let audioCache = {} // 언어별 오디오 캐싱

// API 키
const apiKey = import.meta.env.VITE_OPENAI_API_KEY || ''

// Computed
const institutionType = computed(() => props.content.institutionType)
const scriptIcon = computed(() => SCRIPT_ICONS[institutionType.value])
const supportedLanguages = computed(() => SUPPORTED_LANGUAGES)

// 현재 언어의 번역된 데이터 가져오기
const getCurrentTranslatedData = () => {
  const langKey = selectedLanguage.value
  return translatedData.value[langKey] || personalizedData.value
}

// 개인정보 번역 함수
const translatePersonalizedData = async (targetLang) => {
  // 이미 번역된 데이터가 있으면 반환
  if (translatedData.value[targetLang]) {
    return translatedData.value[targetLang]
  }

  // 한국어이거나 번역할 데이터가 없으면 원본 반환
  if (targetLang === 'ko' || !personalizedData.value || Object.keys(personalizedData.value).length === 0) {
    translatedData.value[targetLang] = personalizedData.value
    return personalizedData.value
  }

  isTranslating.value = true

  try {
    const translated = {}

    // 각 필드를 번역
    for (const [key, value] of Object.entries(personalizedData.value)) {
      if (value && typeof value === 'string' && value.trim()) {
        translated[key] = await translateText(value, targetLang, apiKey)
      } else {
        translated[key] = value
      }
    }

    translatedData.value[targetLang] = translated
    return translated

  } catch (err) {
    console.error('Translation error:', err)
    // 번역 실패 시 원본 사용
    translatedData.value[targetLang] = personalizedData.value
    return personalizedData.value
  } finally {
    isTranslating.value = false
  }
}

// 스크립트 텍스트 개인화 함수
const personalizeText = (text) => {
  if (!text) return text

  const currentData = getCurrentTranslatedData()
  if (!currentData) return text

  let result = text

  // 경찰서 스크립트용 치환
  if (currentData.items) {
    result = result
      .replace(/\[describe items here\]/g, currentData.items)
      .replace(/\[물품 설명\]/g, currentData.items)
      .replace(/\[品物の説明\]/g, currentData.items)
      .replace(/\[describir artículos aquí\]/g, currentData.items)
      .replace(/\[décrire les articles ici\]/g, currentData.items)
  }

  if (currentData.date) {
    result = result.replace(/\[date\]/g, currentData.date)
      .replace(/\[날짜\]/g, currentData.date)
      .replace(/\[日付\]/g, currentData.date)
      .replace(/\[fecha\]/g, currentData.date)
  }

  if (currentData.time) {
    result = result.replace(/\[time\]/g, currentData.time)
      .replace(/\[시간\]/g, currentData.time)
      .replace(/\[heure\]/g, currentData.time)
      .replace(/\[時刻\]/g, currentData.time)
      .replace(/\[hora\]/g, currentData.time)
  }

  if (currentData.location) {
    result = result.replace(/\[location\]/g, currentData.location)
      .replace(/\[장소\]/g, currentData.location)
      .replace(/\[lieu\]/g, currentData.location)
      .replace(/\[場所\]/g, currentData.location)
      .replace(/\[ubicación\]/g, currentData.location)
  }

  // 병원 스크립트용 치환
  if (currentData.symptoms) {
    result = result
      .replace(/\[describe symptoms\]/g, currentData.symptoms)
      .replace(/\[증상 설명\]/g, currentData.symptoms)
      .replace(/\[症状の説明\]/g, currentData.symptoms)
      .replace(/\[describir síntomas\]/g, currentData.symptoms)
      .replace(/\[décrire les symptômes\]/g, currentData.symptoms)
  }

  return result
}

// 스크립트 정돈 함수
const refineScriptText = async (text, field, targetLang) => {
  if (!text) return text
  
  // 이미 정돈된 스크립트가 있으면 반환
  const cacheKey = `${targetLang}_${field}`
  if (refinedScripts.value[cacheKey]) {
    return refinedScripts.value[cacheKey]
  }

  // 플레이스홀더가 없는 경우 정돈 불필요
  if (!text.includes('[') || !personalizedData.value || Object.keys(personalizedData.value).length === 0) {
    return personalizeText(text)
  }

  try {
    isRefining.value = true
    const currentData = getCurrentTranslatedData()
    const refined = await refineScript(text, currentData, institutionType.value, targetLang, apiKey)
    
    // 정돈된 텍스트도 개인화 데이터로 치환 (혹시 플레이스홀더가 남아있을 경우 대비)
    const personalized = personalizeText(refined)
    
    // 캐시에 저장
    refinedScripts.value[cacheKey] = personalized
    
    return personalized
  } catch (err) {
    console.error('Script refinement error:', err)
    // 정돈 실패 시 기존 방식으로 개인화
    return personalizeText(text)
  } finally {
    isRefining.value = false
  }
}

const currentScript = computed(() => {
  const baseScript = INSTITUTION_SCRIPTS[institutionType.value][selectedLanguage.value]
  const lang = selectedLanguage.value

  // 기본 템플릿에서 개인화만 적용 (정돈은 비동기로 처리)
  return {
    title: baseScript.title,
    greeting: personalizeText(baseScript.greeting),
    main: personalizeText(baseScript.main),
    items: baseScript.items ? personalizeText(baseScript.items) : null,
    symptoms: baseScript.symptoms ? personalizeText(baseScript.symptoms) : null,
    date: baseScript.date ? personalizeText(baseScript.date) : null,
    location: baseScript.location ? personalizeText(baseScript.location) : null,
    documents: baseScript.documents ? personalizeText(baseScript.documents) : null,
    insurance: baseScript.insurance ? personalizeText(baseScript.insurance) : null,
    payment: baseScript.payment ? personalizeText(baseScript.payment) : null,
    closing: personalizeText(baseScript.closing),
    language: baseScript.language
  }
})

// 정돈된 스크립트 (비동기 로딩)
const refinedScript = ref(null)

// 스크립트 정돈 로드 함수
const loadRefinedScript = async () => {
  if (!personalizedData.value || Object.keys(personalizedData.value).length === 0) {
    refinedScript.value = currentScript.value
    return
  }

  const lang = selectedLanguage.value
  const cacheKey = `${lang}_full`
  
  if (refinedScripts.value[cacheKey]) {
    refinedScript.value = refinedScripts.value[cacheKey]
    return
  }

  try {
    isRefining.value = true
    const baseScript = INSTITUTION_SCRIPTS[institutionType.value][lang]
    const currentData = getCurrentTranslatedData()
    
    // 전체 스크립트를 하나의 텍스트로 만들기
    let fullScriptText = ''
    fullScriptText += `${baseScript.greeting}\n\n`
    fullScriptText += `${baseScript.main}\n\n`
    if (baseScript.items) fullScriptText += `${baseScript.items}\n\n`
    if (baseScript.symptoms) fullScriptText += `${baseScript.symptoms}\n\n`
    if (baseScript.date) fullScriptText += `${baseScript.date}\n\n`
    if (baseScript.location) fullScriptText += `${baseScript.location}\n\n`
    if (baseScript.documents) fullScriptText += `${baseScript.documents}\n\n`
    if (baseScript.insurance) fullScriptText += `${baseScript.insurance}\n\n`
    if (baseScript.payment) fullScriptText += `${baseScript.payment}\n\n`
    fullScriptText += baseScript.closing

    // OpenAI로 정돈 (원본 사고 내용 포함)
    const refinedText = await refineScript(fullScriptText, currentData, institutionType.value, lang, apiKey, originalAccidentDescription.value)
    
    // 정돈된 스크립트 객체 생성 (전체 텍스트 사용)
    const refined = {
      title: baseScript.title,
      fullText: refinedText, // 정돈된 전체 텍스트
      language: baseScript.language
    }
    
    refinedScripts.value[cacheKey] = refined
    refinedScript.value = refined
  } catch (err) {
    console.error('Script refinement error:', err)
    refinedScript.value = currentScript.value
  } finally {
    isRefining.value = false
  }
}

// 언어 변경
const changeLanguage = async (langCode) => {
  if (isPlaying.value) {
    stopScript()
  }
  selectedLanguage.value = langCode
  error.value = null

  // 언어 변경 시 번역 수행
  await translatePersonalizedData(langCode)
  
  // 스크립트 정돈 다시 로드
  await loadRefinedScript()
}

// 컴포넌트 마운트 시 초기 번역 및 스크립트 정돈
onMounted(async () => {
  // 기본 언어로 번역 (한국어가 아니면 번역 실행)
  await translatePersonalizedData(selectedLanguage.value)
  
  // 스크립트 정돈 로드
  await loadRefinedScript()
})

// 스크립트 전체 텍스트 생성
const getFullScriptText = () => {
  // 정돈된 스크립트가 있으면 그걸 사용
  if (refinedScript.value && refinedScript.value.fullText) {
    return refinedScript.value.fullText
  }
  
  // 없으면 기존 방식
  const script = currentScript.value
  let text = ''

  text += `${script.greeting}\n\n`
  text += `${script.main}\n\n`

  if (script.symptoms) {
    text += `${script.symptoms}\n\n`
  }
  if (script.items) {
    text += `${script.items}\n\n`
  }
  if (script.date) {
    text += `${script.date}\n\n`
  }
  if (script.location) {
    text += `${script.location}\n\n`
  }
  if (script.documents) {
    text += `${script.documents}\n\n`
  }
  if (script.insurance) {
    text += `${script.insurance}\n\n`
  }
  if (script.payment) {
    text += `${script.payment}\n\n`
  }

  text += `${script.closing}`

  return text
}

// 오디오 생성 또는 캐시에서 가져오기
const getOrGenerateAudio = async () => {
  const cacheKey = `${institutionType.value}_${selectedLanguage.value}`

  // 캐시에 있으면 반환
  if (audioCache[cacheKey]) {
    return audioCache[cacheKey]
  }

  // 새로 생성
  isGenerating.value = true
  error.value = null

  try {
    const text = getFullScriptText()
    const voice = getVoiceForLanguage(selectedLanguage.value)

    const audioBlob = await generateSpeech(text, apiKey, {
      voice,
      model: 'tts-1', // tts-1-hd는 더 고품질이지만 느림
      speed: 0.9
    })

    // Blob URL 생성
    const audioUrl = URL.createObjectURL(audioBlob)

    // 캐시에 저장
    audioCache[cacheKey] = audioUrl

    return audioUrl

  } catch (err) {
    error.value = err.message || '음성 생성에 실패했습니다.'
    throw err
  } finally {
    isGenerating.value = false
  }
}

// 음성 재생
const playScript = async () => {
  try {
    // 오디오 생성 또는 캐시에서 가져오기
    const audioUrl = await getOrGenerateAudio()

    // 오디오 엘리먼트 생성 (없으면)
    if (!audioElement) {
      audioElement = new Audio()
      audioElement.onended = () => {
        isPlaying.value = false
        isPaused.value = false
      }
      audioElement.onerror = () => {
        error.value = '음성 재생에 실패했습니다.'
        isPlaying.value = false
        isPaused.value = false
      }
    }

    audioElement.src = audioUrl
    await audioElement.play()
    isPlaying.value = true
    isPaused.value = false

  } catch (err) {
    console.error('Audio playback error:', err)
  }
}

// 일시정지
const pauseScript = () => {
  if (audioElement && isPlaying.value) {
    audioElement.pause()
    isPlaying.value = false
    isPaused.value = true
  }
}

// 재개
const resumeScript = () => {
  if (audioElement && isPaused.value) {
    audioElement.play()
    isPlaying.value = true
    isPaused.value = false
  }
}

// 정지
const stopScript = () => {
  if (audioElement) {
    audioElement.pause()
    audioElement.currentTime = 0
    isPlaying.value = false
    isPaused.value = false
  }
}

// 컴포넌트 언마운트
onUnmounted(() => {
  stopScript()
  // Blob URL 해제
  Object.values(audioCache).forEach(url => {
    URL.revokeObjectURL(url)
  })
})
</script>

<style scoped>
.script-message {
  max-width: 700px;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

/* 헤더 */
.script-header {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, #7030A0 0%, #5AB8B8 100%);
  color: white;
}

.script-icon {
  font-size: 32px;
}

.script-title h3 {
  margin: 0 0 4px 0;
  font-size: 18px;
  font-weight: 600;
}

.subtitle {
  margin: 0;
  font-size: 13px;
  opacity: 0.9;
}

/* 언어 선택 */
.language-selector {
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
  background: #f8f9fa;
}

.language-selector label {
  display: block;
  margin-bottom: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #333;
}

.language-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.language-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 12px;
}

.language-button:hover {
  border-color: #7030A0;
  background: #f8f4fc;
}

.language-button.active {
  border-color: #7030A0;
  background: #7030A0;
  color: white;
}

.language-button .flag {
  font-size: 16px;
}

.language-button .lang-name {
  font-weight: 500;
}

/* 스크립트 내용 */
.script-content {
  padding: 16px;
  max-height: 400px;
  overflow-y: auto;
}

.script-section {
  margin-bottom: 16px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 3px solid #7030A0;
}

.script-section:last-child {
  margin-bottom: 0;
}

.script-section strong {
  display: block;
  margin-bottom: 6px;
  color: #7030A0;
  font-size: 13px;
  font-weight: 600;
}

.script-section p {
  margin: 0;
  font-size: 14px;
  color: #333;
  line-height: 1.5;
}

/* 음성 컨트롤 */
.audio-controls {
  padding: 16px;
  border-top: 2px solid #e0e0e0;
  background: #f8f9fa;
}

.control-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.audio-icon {
  font-size: 20px;
}

.control-label {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.control-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.control-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.control-button .icon {
  font-size: 16px;
}

.control-button.play {
  background: #9AC120;
  color: white;
}

.control-button.play:hover {
  background: #82a41a;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(154, 193, 32, 0.3);
}

.control-button.pause {
  background: #E67635;
  color: white;
}

.control-button.pause:hover {
  background: #d4621f;
}

.control-button.resume {
  background: #5AB8B8;
  color: white;
}

.control-button.resume:hover {
  background: #4a9a9a;
}

.control-button.stop {
  background: #D24726;
  color: white;
}

.control-button.stop:hover {
  background: #b23820;
}

.control-button.generating {
  background: #7030A0;
  color: white;
  cursor: not-allowed;
  opacity: 0.8;
}

/* 번역 중 표시 */
.translating-indicator {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 24px;
  background: #f8f9fa;
  justify-content: center;
}

.translating-indicator .spinner {
  width: 20px;
  height: 20px;
  border: 3px solid #e0e0e0;
  border-top-color: #5AB8B8;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.translating-indicator .status-text {
  font-size: 14px;
  font-weight: 600;
  color: #5AB8B8;
}

/* 음성 생성 중 표시 */
.generating-indicator {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
  padding: 12px;
  background: white;
  border-radius: 8px;
  border: 1px solid #7030A0;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid #e0e0e0;
  border-top-color: #7030A0;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 재생 중 표시 */
.playing-indicator {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
  padding: 12px;
  background: white;
  border-radius: 8px;
  border: 1px solid #9AC120;
}

.wave {
  display: flex;
  gap: 3px;
  align-items: center;
  height: 20px;
}

.wave span {
  display: block;
  width: 3px;
  height: 100%;
  background: #9AC120;
  border-radius: 2px;
  animation: wave 1s ease-in-out infinite;
}

.wave span:nth-child(1) { animation-delay: 0s; }
.wave span:nth-child(2) { animation-delay: 0.1s; }
.wave span:nth-child(3) { animation-delay: 0.2s; }
.wave span:nth-child(4) { animation-delay: 0.3s; }

@keyframes wave {
  0%, 100% { height: 30%; }
  50% { height: 100%; }
}

.status-text {
  font-size: 13px;
  font-weight: 600;
  color: #9AC120;
}

/* 에러 메시지 */
.error-message {
  margin-top: 12px;
  padding: 12px;
  background: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: 8px;
  font-size: 12px;
  color: #856404;
  text-align: center;
}

/* 스크롤바 스타일 */
.script-content::-webkit-scrollbar {
  width: 6px;
}

.script-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.script-content::-webkit-scrollbar-thumb {
  background: #7030A0;
  border-radius: 3px;
}

.script-content::-webkit-scrollbar-thumb:hover {
  background: #5a2580;
}
</style>
