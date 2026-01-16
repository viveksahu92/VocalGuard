<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-900 to-black flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- iPhone-style Call Screen -->
      <div class="bg-gray-800 rounded-[3rem] shadow-2xl overflow-hidden border-8 border-gray-900 relative">
        <!-- Status Bar -->
        <div class="bg-black px-8 py-2 flex justify-between items-center text-white text-xs">
          <span>{{ currentTime }}</span>
          <div class="flex gap-1">
            <div class="w-4 h-3 bg-white rounded-sm"></div>
            <div class="w-4 h-3 bg-white rounded-sm"></div>
            <div class="w-4 h-3 bg-white rounded-sm"></div>
          </div>
        </div>

        <!-- Call Information -->
        <div class="px-8 py-12 text-center">
          <!-- Caller Name/Number -->
          <div class="mb-2">
            <p class="text-gray-400 text-sm">{{ callStatus }}</p>
          </div>
          <h2 class="text-white text-3xl font-light mb-1">{{ callerName }}</h2>
          <p class="text-gray-400 text-lg">{{ callerNumber }}</p>
          
          <!-- FEATURE 11: Caller Reputation Badge -->
          <div v-if="analysisResult && analysisResult.caller_reputation" class="mt-2">
            <span :class="[
              'text-xs px-3 py-1 rounded-full font-semibold',
              analysisResult.caller_reputation.trust_level === 'KNOWN SCAMMER' ? 'bg-red-600 text-white' :
              analysisResult.caller_reputation.trust_level === 'HIGH RISK' ? 'bg-red-500/30 text-red-300 border border-red-500' :
              analysisResult.caller_reputation.trust_level === 'SUSPICIOUS' ? 'bg-yellow-500/30 text-yellow-300 border border-yellow-500' :
              analysisResult.caller_reputation.trust_level === 'VERIFIED LEGITIMATE' ? 'bg-green-600 text-white' :
              'bg-gray-600 text-gray-300'
            ]">
              {{ analysisResult.caller_reputation.is_known_scammer ? '🚫 KNOWN SCAMMER' : 
                 analysisResult.caller_reputation.trust_level }}
              <span v-if="analysisResult.caller_reputation.community_reports > 0" class="ml-1">
                ({{ analysisResult.caller_reputation.community_reports }} reports)
              </span>
            </span>
          </div>

          <!-- Call Duration -->
          <div class="mt-8">
            <p class="text-white text-4xl font-light">{{ callDuration }}</p>
          </div>

          <!-- Advanced Risk Meter -->
          <div v-if="analysisResult" class="mt-6 mx-auto max-w-xs">
            <div class="bg-gray-700 rounded-2xl p-4">
              <div class="flex justify-between items-center mb-2">
                <span class="text-gray-300 text-sm font-semibold">Risk Score</span>
                <span :class="[
                  'text-lg font-bold',
                  analysisResult.risk_score >= 70 ? 'text-red-400' :
                  analysisResult.risk_score >= 40 ? 'text-yellow-400' :
                  'text-green-400'
                ]">
                  {{ analysisResult.risk_score || 0 }}/100
                </span>
              </div>
              <div class="w-full bg-gray-600 rounded-full h-3">
                <div 
                  :class="[
                    'h-3 rounded-full transition-all duration-500',
                    analysisResult.risk_score >= 70 ? 'bg-red-500' :
                    analysisResult.risk_score >= 40 ? 'bg-yellow-500' :
                    'bg-green-500'
                  ]"
                  :style="{ width: (analysisResult.risk_score || 0) + '%' }"
                ></div>
              </div>
            </div>
          </div>

 <!-- FEATURE 10: Auto-Disconnect Warning -->
          <div v-if="analysisResult && analysisResult.auto_disconnect_recommended" 
               class="mt-4 mx-auto max-w-xs">
            <div class="bg-red-600 border-4 border-red-400 rounded-2xl p-4 animate-pulse">
              <p class="text-white font-bold text-xl mb-1">🚨 AUTO-DISCONNECT RECOMMENDED</p>
              <p class="text-white text-sm">Extremely high risk detected. Hanging up now...</p>
            </div>
          </div>

          <!-- Scam Alert Badge with Category -->
          <div v-if="analysisResult && analysisResult.is_scam" 
               class="mt-4 mx-auto max-w-xs">
            <div :class="[
              'p-4 rounded-2xl',
              analysisResult.threat_level === 'HIGH' ? 'bg-red-500/20 border-2 border-red-500' :
              analysisResult.threat_level === 'MEDIUM' ? 'bg-yellow-500/20 border-2 border-yellow-500' :
              'bg-orange-500/20 border-2 border-orange-500'
            ]">
              <p class="text-white font-bold text-lg mb-2">⚠️ SCAM ALERT</p>
              <!-- FEATURE 8: Scam Category Display -->
              <p v-if="analysisResult.scam_category" class="text-red-300 text-xs font-semibold mb-2">
                Category: {{ analysisResult.scam_category }}
              </p>
              <p class="text-white text-sm">{{ analysisResult.warning_message }}</p>
              <div class="mt-2 text-xs text-gray-300">
                AI Confidence: {{ Math.round(analysisResult.confidence * 100) }}%
              </div>
            </div>
          </div>
          
          <!-- FEATURE 2 & 6: Voice Analysis & Spoofing Detection -->
          <div v-if="analysisResult && (analysisResult.voice_analysis || analysisResult.spoofing_analysis)" 
               class="mt-3 mx-auto max-w-xs">
            <div class="bg-gray-700/50 rounded-xl p-3 space-y-2">
              <div v-if="analysisResult.voice_analysis" class="text-xs">
                <p class="text-gray-400 font-semibold mb-1">Voice Analysis:</p>
                <p class="text-white">{{ analysisResult.voice_analysis.summary }}</p>
                <div v-if="analysisResult.voice_analysis.robocall" class="mt-1 text-red-300">
                  🤖 Robocall Detected
                </div>
              </div>
              <div v-if="analysisResult.spoofing_analysis && analysisResult.spoofing_analysis.spoofing_detected" 
                   class="text-xs">
                <p class="text-yellow-400 font-semibold">⚡ {{ analysisResult.spoofing_analysis.verdict }}</p>
                <p class="text-gray-300">{{ analysisResult.spoofing_analysis.recommendation }}</p>
              </div>
            </div>
          </div>

          <!-- Transcript Section -->
          <div class="mt-6 bg-gray-700/50 rounded-2xl p-4 max-h-40 overflow-y-auto">
            <div class="flex justify-between items-center mb-2">
              <h3 class="text-white text-sm font-semibold">Transcript</h3>
              <button 
                @click="togglePrivacy"
                class="text-xs bg-gray-600 hover:bg-gray-500 text-white px-3 py-1 rounded-full transition"
              >
                {{ privacyMode ? '👁️ Show' : '👁️‍🗨️ Blur' }} Numbers
              </button>
            </div>
            <p class="text-gray-300 text-sm text-left">
              {{ displayTranscript }}
            </p>
          </div>

          <!-- Detected Threats -->
          <div v-if="analysisResult && analysisResult.detected_threats.length > 0" 
               class="mt-4">
            <div class="flex flex-wrap gap-2 justify-center">
              <span 
                v-for="threat in analysisResult.detected_threats" 
                :key="threat"
                class="bg-red-900/40 text-red-300 text-xs px-3 py-1 rounded-full border border-red-500/50"
              >
                {{ formatThreat(threat) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Call Controls -->
        <div class="px-8 pb-12">
          <div class="grid grid-cols-3 gap-6 mb-8">
            <!-- Mute Button -->
            <button class="flex flex-col items-center gap-2 text-white opacity-50">
              <div class="w-16 h-16 bg-gray-700 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                </svg>
              </div>
              <span class="text-xs">mute</span>
            </button>

            <!-- Keypad Button -->
            <button class="flex flex-col items-center gap-2 text-white opacity-50">
              <div class="w-16 h-16 bg-gray-700 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
                </svg>
              </div>
              <span class="text-xs">keypad</span>
            </button>

            <!-- Speaker Button -->
            <button class="flex flex-col items-center gap-2 text-white opacity-50">
              <div class="w-16 h-16 bg-gray-700 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                </svg>
              </div>
              <span class="text-xs">speaker</span>
            </button>
          </div>

          <!-- FEATURE 15: Report & Block Actions -->
          <div v-if="analysisResult && analysisResult.is_scam" class="flex gap-2 mb-4">
            <button 
              @click="reportAndBlock"
              class="flex-1 bg-orange-600 hover:bg-orange-700 text-white py-2 px-4 rounded-full font-semibold text-sm transition"
            >
              🚫 Report & Block
            </button>
          </div>

          <!-- End Call Button -->
          <button 
            @click="endCall"
            class="w-20 h-20 bg-red-500 hover:bg-red-600 rounded-full mx-auto flex items-center justify-center transition shadow-lg"
          >
            <svg class="w-8 h-8 text-white transform rotate-135" fill="currentColor" viewBox="0 0 24 24">
              <path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 00-1.01.24l-1.57 1.97c-2.83-1.35-5.48-3.9-6.89-6.83l1.95-1.66c.27-.28.35-.67.24-1.02-.37-1.11-.56-2.3-.56-3.53 0-.54-.45-.99-.99-.99H4.19C3.65 3 3 3.24 3 3.99 3 13.28 10.73 21 20.01 21c.71 0 .99-.63.99-1.18v-3.45c0-.54-.45-.99-.99-.99z"/>
            </svg>
          </button>

          <!-- Analyze Button (for demo) -->
          <button 
            v-if="!isAnalyzing && !analysisResult"
            @click="analyzeCall"
            class="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-full font-semibold transition"
          >
            Analyze Call for Scams
          </button>

          <div v-if="isAnalyzing" class="mt-4 text-center">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
            <p class="text-white text-sm mt-2">Analyzing call...</p>
          </div>
        </div>
      </div>

      <!-- Demo Instructions -->
      <div class="mt-6 text-center text-gray-400 text-sm">
        <p>Demo Call Screen - Click "Analyze Call" to test scam detection</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

export default {
  name: 'CallScreen',
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
    
    // Watch for scenario changes
    watch(() => props.selectedScenario, (newScenario) => {
      if (newScenario) {
        transcript.value = newScenario.transcript
        callerName.value = newScenario.caller
        callerNumber.value = newScenario.number
        analysisResult.value = null
        callStatus.value = 'VocalGuard Active'
      }
    })

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
    // Report and block scammer
    const reportAndBlock = async () => {
      if (!analysisResult.value) return
      
      try {
        // Report to community database
        const reportResponse = await fetch('/api/report', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            phone_number: callerNumber.value,
            description: `Scam call detected: ${analysisResult.value.scam_category}`,
            risk_score: analysisResult.value.risk_score,
            scam_category: analysisResult.value.scam_category
          })
        })
        
        // Block number
        const blockResponse = await fetch('/api/block', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            phone_number: callerNumber.value,
            reason: 'Scam reported by user'
          })
        })
        
        if (reportResponse.ok && blockResponse.ok) {
          alert('✅ Scammer reported and blocked successfully!\nThank you for protecting the community.')
          endCall()
        }
      } catch (error) {
        console.error('Report/block error:', error)
        alert('Failed to report scammer')
      }
    }

    const endCall = () => {
      if (durationInterval) {
        clearInterval(durationInterval)
      }
      callStatus.value = 'Call Ended'
      
      // Auto-disconnect if recommended
      if (analysisResult.value?.auto_disconnect_recommended) {
        alert('🚨 Call automatically disconnected due to extremely high scam risk!\n\nRisk Score: ' + 
              analysisResult.value.risk_score + '/100')
      } else {
        alert('Call ended. VocalGuard analysis ' + 
              (analysisResult.value?.is_scam ? 'detected a scam!' : 'found no threats.'))
      }
    }

    // Analyze call
    const analyzeCall = async () => {
      isAnalyzing.value = true
      
      try {
        // Use relative path - Vite proxy will forward to backend
        const backendUrl = '/api/analyze'
        
        console.log('📡 Calling backend at:', backendUrl)
        
        const response = await fetch(backendUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            transcript: transcript.value,
            generate_audio: false
          })
        })
        
        console.log('✅ Backend response status:', response.status)
        
        if (!response.ok) {
          const errorText = await response.text()
          throw new Error(`Backend returned status ${response.status}: ${errorText}`)
        }
        
        const data = await response.json()
        console.log('📊 Analysis result:', data)
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
          warning_message: data.warning_message
        })
        
        // Update call status based on result
        if (data.is_scam) {
          callStatus.value = '⚠️ SCAM DETECTED'
        } else {
          callStatus.value = '✓ Legitimate Call'
        }
      } catch (error) {
        console.error('❌ Analysis failed:', error)
        alert('Failed to analyze call.\n\nError: ' + error.message)
      } finally {
        isAnalyzing.value = false
      }
    }

    onMounted(() => {
      updateTime()
      setInterval(updateTime, 60000) // Update time every minute
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
      reportAndBlock,
      endCall,
      analyzeCall
    }
  }
}
</script>

<style scoped>
/* Custom scrollbar for transcript */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 10px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>
