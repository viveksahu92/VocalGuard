<template>
  <div class="min-h-full py-8">
    <!-- Main Content -->
    <div class="relative z-10">
      <!-- Enhanced Call Screen Container -->
      <div class="min-h-screen flex items-center justify-center p-4 py-8">
        <div class="w-full max-w-2xl">
          <!-- iPhone Frame with 3D Effect -->
          <div class="relative">
            <!-- 3D Shadow & Depth -->
            <div class="absolute inset-0 bg-gradient-to-b from-purple-500/30 to-blue-500/30 rounded-[3.5rem] blur-2xl transform -translate-z-10"></div>
            
            <!-- Main Phone Frame -->
            <div class="relative bg-gradient-to-b from-gray-900 to-gray-800 rounded-[3rem] shadow-2xl overflow-hidden border-8 border-gray-950 backdrop-blur-sm">
              
              <!-- Status Bar with Gradient -->
              <div class="bg-gradient-to-r from-gray-950 via-gray-900 to-gray-950 px-8 py-3 flex justify-between items-center text-white text-xs border-b border-gray-800">
                <span class="font-semibold">{{ currentTime }}</span>
                <div class="flex gap-1.5">
                  <div class="w-4 h-3 bg-white rounded-sm"></div>
                  <div class="w-4 h-3 bg-white rounded-sm"></div>
                  <div class="w-4 h-3 bg-white rounded-sm"></div>
                </div>
              </div>

              <!-- Call Information Section -->
              <div class="px-8 py-10 text-center bg-gradient-to-b from-gray-800/50 to-transparent">
                <!-- Call Status with Animation -->
                <div class="mb-4">
                  <p class="text-gray-400 text-sm animate-pulse">{{ callStatus }}</p>
                </div>
                
                <!-- Caller Info -->
                <h2 class="text-white text-3xl font-light mb-2 drop-shadow-lg">{{ callerName }}</h2>
                <p class="text-gray-500 text-lg font-mono">{{ callerNumber }}</p>

                <!-- Call Duration -->
                <div class="mt-8 mb-6">
                  <p class="text-white text-5xl font-light tracking-wider drop-shadow-lg">{{ callDuration }}</p>
                </div>

                <!-- Enhanced Risk Score Display -->
                <div v-if="analysisResult" class="mb-6">
                  <div class="bg-gradient-to-r from-gray-700/50 to-gray-600/50 backdrop-blur rounded-2xl p-4 mb-4 border border-gray-500/30">
                    <div class="flex justify-between items-center mb-2">
                      <span class="text-gray-300 text-sm font-semibold">Risk Score</span>
                      <span :class="[
                        'text-2xl font-bold',
                        analysisResult.risk_score >= 70 ? 'text-red-400' :
                        analysisResult.risk_score >= 40 ? 'text-yellow-400' :
                        'text-green-400'
                      ]">
                        {{ Math.round(analysisResult.risk_score) }}/100
                      </span>
                    </div>
                    <!-- Risk Bar -->
                    <div class="w-full bg-gray-600 rounded-full h-2 overflow-hidden">
                      <div
                        :style="{ width: analysisResult.risk_score + '%' }"
                        :class="[
                          'h-full rounded-full transition-all duration-500',
                          analysisResult.risk_score >= 70 ? 'bg-gradient-to-r from-red-500 to-red-600' :
                          analysisResult.risk_score >= 40 ? 'bg-gradient-to-r from-yellow-500 to-orange-500' :
                          'bg-gradient-to-r from-green-500 to-emerald-500'
                        ]"
                      ></div>
                    </div>
                  </div>
                </div>

                <!-- Enhanced Scam Alert Badge -->
                <div v-if="analysisResult && analysisResult.is_scam" class="mb-6 mx-auto max-w-md">
                  <div :class="[
                    'p-5 rounded-3xl backdrop-blur-sm border-2 shadow-lg transform transition-transform hover:scale-105',
                    analysisResult.threat_level === 'HIGH' ? 'bg-red-500/20 border-red-500/50 shadow-red-500/20' :
                    analysisResult.threat_level === 'MEDIUM' ? 'bg-yellow-500/20 border-yellow-500/50 shadow-yellow-500/20' :
                    'bg-orange-500/20 border-orange-500/50 shadow-orange-500/20'
                  ]">
                    <p class="text-white font-bold text-lg mb-2">⚠️ SCAM ALERT</p>
                    <p class="text-white text-sm leading-relaxed">{{ analysisResult.warning_message }}</p>
                    <div class="mt-3 text-xs text-gray-300 font-mono">
                      Confidence: {{ Math.round(analysisResult.confidence * 100) }}%
                    </div>
                  </div>
                </div>

                <!-- Legitimate Call Badge -->
                <div v-else-if="analysisResult && !analysisResult.is_scam" class="mb-6 mx-auto max-w-md">
                  <div class="p-5 rounded-3xl backdrop-blur-sm border-2 border-green-500/50 bg-green-500/20 shadow-lg shadow-green-500/20">
                    <p class="text-white font-bold text-lg mb-2">✓ LEGITIMATE</p>
                    <p class="text-white text-sm">This call appears to be safe</p>
                    <div class="mt-3 text-xs text-gray-300 font-mono">
                      Risk Level: LOW
                    </div>
                  </div>
                </div>

                <!-- Transcript Section with Glassmorphism -->
                <div class="mt-6 bg-gray-700/30 backdrop-blur-md rounded-2xl p-4 max-h-48 overflow-y-auto border border-gray-600/50">
                  <div class="flex justify-between items-center mb-3">
                    <h3 class="text-white text-sm font-semibold">Transcript</h3>
                    <button 
                      @click="togglePrivacy"
                      class="text-xs bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white px-3 py-1 rounded-full transition transform hover:scale-105"
                    >
                      {{ privacyMode ? '👁️ Show' : '🔒 Blur' }}
                    </button>
                  </div>
                  <p class="text-gray-300 text-sm text-left leading-relaxed">
                    {{ displayTranscript }}
                  </p>
                </div>

                <!-- Detected Threats -->
                <div v-if="analysisResult && analysisResult.detected_threats.length > 0" class="mt-4">
                  <div class="flex flex-wrap gap-2 justify-center">
                    <span 
                      v-for="threat in analysisResult.detected_threats" 
                      :key="threat"
                      class="bg-red-900/40 text-red-300 text-xs px-3 py-1 rounded-full border border-red-500/50 backdrop-blur-sm"
                    >
                      {{ formatThreat(threat) }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- Enhanced Call Controls -->
              <div class="px-8 pb-12 bg-gradient-to-t from-gray-900/50 to-transparent">
                <div class="grid grid-cols-3 gap-6 mb-8">
                  <!-- Mute Button -->
                  <button class="flex flex-col items-center gap-2 text-gray-400 hover:text-white transition">
                    <div class="w-16 h-16 bg-gradient-to-br from-gray-700 to-gray-800 hover:from-gray-600 hover:to-gray-700 rounded-full flex items-center justify-center transition transform hover:scale-110 shadow-lg">
                      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                      </svg>
                    </div>
                    <span class="text-xs">mute</span>
                  </button>

                  <!-- Keypad Button -->
                  <button class="flex flex-col items-center gap-2 text-gray-400 hover:text-white transition">
                    <div class="w-16 h-16 bg-gradient-to-br from-gray-700 to-gray-800 hover:from-gray-600 hover:to-gray-700 rounded-full flex items-center justify-center transition transform hover:scale-110 shadow-lg">
                      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
                      </svg>
                    </div>
                    <span class="text-xs">keypad</span>
                  </button>

                  <!-- Speaker Button -->
                  <button class="flex flex-col items-center gap-2 text-gray-400 hover:text-white transition">
                    <div class="w-16 h-16 bg-gradient-to-br from-gray-700 to-gray-800 hover:from-gray-600 hover:to-gray-700 rounded-full flex items-center justify-center transition transform hover:scale-110 shadow-lg">
                      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                      </svg>
                    </div>
                    <span class="text-xs">speaker</span>
                  </button>
                </div>

                <!-- End Call Button with Glow -->
                <button 
                  @click="endCall"
                  class="w-20 h-20 bg-gradient-to-br from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 rounded-full mx-auto flex items-center justify-center transition transform hover:scale-110 shadow-lg shadow-red-500/50"
                >
                  <svg class="w-8 h-8 text-white transform rotate-135" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 00-1.01.24l-1.57 1.97c-2.83-1.35-5.48-3.9-6.89-6.83l1.95-1.66c.27-.28.35-.67.24-1.02-.37-1.11-.56-2.3-.56-3.53 0-.54-.45-.99-.99-.99H4.19C3.65 3 3 3.24 3 3.99 3 13.28 10.73 21 20.01 21c.71 0 .99-.63.99-1.18v-3.45c0-.54-.45-.99-.99-.99z"/>
                  </svg>
                </button>

                <!-- Analyze Button -->
                <button 
                  v-if="!isAnalyzing && !analysisResult"
                  @click="analyzeCall"
                  class="mt-6 w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white py-3 rounded-full font-semibold transition transform hover:scale-105 shadow-lg shadow-purple-500/50"
                >
                  🔍 Analyze Call for Scams
                </button>

                <!-- Loading State -->
                <div v-if="isAnalyzing" class="mt-6 text-center">
                  <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-purple-400"></div>
                  <p class="text-white text-sm mt-2 animate-pulse">Analyzing call...</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Info Footer -->
          <div class="mt-8 text-center text-gray-400 text-sm">
            <p>🛡️ VocalGuard - Advanced Scam Detection for Hackathon 🏆</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

export default {
  name: 'CallScreenEnhanced',
  props: {
    selectedScenario: {
      type: Object,
      default: null
    }
  },
  emits: ['call-analyzed'],
  
  setup(props, { emit }) {
    const currentTime = ref('9:41')
    const callStatus = ref('incoming call...')
    const callerName = ref('Unknown Caller')
    const callerNumber = ref('+1 (555) 123-4567')
    const callDuration = ref('00:00')
    const transcript = ref('Hello, this is from the IRS. You need to pay your outstanding taxes immediately using iTunes gift cards or you will be arrested within 24 hours. Please provide your credit card number 4532-1234-5678-9012 to avoid legal action.')
    const privacyMode = ref(false)
    const isAnalyzing = ref(false)
    const analysisResult = ref(null)
    
    let durationInterval = null
    let startTime = null
    
    // Watch for scenario changes - with immediate and deep options
    watch(() => props.selectedScenario, (newScenario) => {
      console.log('📡 Scenario changed:', newScenario)
      if (newScenario) {
        console.log('✅ Updating transcript to:', newScenario.name)
        transcript.value = newScenario.transcript
        callerName.value = newScenario.caller
        callerNumber.value = newScenario.number
        analysisResult.value = null
        callStatus.value = 'VocalGuard Active'
        console.log('✅ Transcript updated successfully')
      }
    }, { immediate: true, deep: true })

    // Format transcript based on privacy mode
    const displayTranscript = computed(() => {
      if (!transcript.value) return ''
      if (privacyMode.value) {
        return transcript.value.replace(/\d/g, '*')
      }
      return transcript.value
    })

    // Toggle privacy mode
    const togglePrivacy = () => {
      privacyMode.value = !privacyMode.value
    }

    // Format threat names
    const formatThreat = (threat) => {
      return threat.replace(/_/g, ' ').toUpperCase()
    }

    // Update time
    const updateTime = () => {
      const now = new Date()
      currentTime.value = now.toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit',
        hour12: false 
      })
    }

    // Update call duration
    const updateDuration = () => {
      if (!startTime) return
      const elapsed = Math.floor((Date.now() - startTime) / 1000)
      const minutes = Math.floor(elapsed / 60)
      const seconds = elapsed % 60
      callDuration.value = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
    }

    // Start call timer
    const startCall = () => {
      callStatus.value = 'VocalGuard Active'
      startTime = Date.now()
      durationInterval = setInterval(updateDuration, 1000)
    }

    // End call
    const endCall = () => {
      if (durationInterval) {
        clearInterval(durationInterval)
      }
      callStatus.value = 'Call Ended'
      alert('Call ended. VocalGuard analysis ' + (analysisResult.value?.is_scam ? 'detected a scam!' : 'found no threats.'))
    }

    // Analyze call
    const analyzeCall = async () => {
      isAnalyzing.value = true
      try {
        const backendUrl = '/api/analyze'
        
        const response = await fetch(backendUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            transcript: transcript.value,
            caller_name: callerName.value,
            caller_number: callerNumber.value,
            generate_audio: false
          })
        })
        
        if (!response.ok) {
          throw new Error(`Backend error: ${response.status}`)
        }
        
        const data = await response.json()
        analysisResult.value = data
        
        // Emit call data for history
        emit('call-analyzed', {
          transcript: transcript.value,
          caller: callerName.value,
          number: callerNumber.value,
          is_scam: data.is_scam,
          confidence: data.confidence,
          threat_level: data.threat_level,
          detected_threats: data.detected_threats,
          warning_message: data.warning_message,
          risk_score: data.risk_score
        })
        
        // Update call status
        if (data.is_scam) {
          callStatus.value = '⚠️ SCAM DETECTED'
        } else {
          callStatus.value = '✓ Legitimate Call'
        }
      } catch (error) {
        console.error('Analysis failed:', error)
        alert('Failed to analyze call. Error: ' + error.message)
      } finally {
        isAnalyzing.value = false
      }
    }

    onMounted(() => {
      updateTime()
      setInterval(updateTime, 60000)
      startCall()
    })

    onUnmounted(() => {
      if (durationInterval) {
        clearInterval(durationInterval)
      }
    })

    return {
      currentTime,
      callStatus,
      callerName,
      callerNumber,
      callDuration,
      transcript,
      privacyMode,
      isAnalyzing,
      analysisResult,
      displayTranscript,
      togglePrivacy,
      formatThreat,
      endCall,
      analyzeCall
    }
  }
}
</script>

<style scoped>
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #8b5cf6, #3b82f6);
  border-radius: 10px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #a78bfa, #60a5fa);
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}
</style>
