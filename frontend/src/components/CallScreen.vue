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

          <!-- Call Duration -->
          <div class="mt-8">
            <p class="text-white text-4xl font-light">{{ callDuration }}</p>
          </div>

          <!-- Scam Alert Badge -->
          <div v-if="analysisResult && analysisResult.is_scam" 
               class="mt-6 mx-auto max-w-xs">
            <div :class="[
              'p-4 rounded-2xl',
              analysisResult.threat_level === 'HIGH' ? 'bg-red-500/20 border-2 border-red-500' :
              analysisResult.threat_level === 'MEDIUM' ? 'bg-yellow-500/20 border-2 border-yellow-500' :
              'bg-orange-500/20 border-2 border-orange-500'
            ]">
              <p class="text-white font-bold text-lg mb-2">⚠️ SCAM ALERT</p>
              <p class="text-white text-sm">{{ analysisResult.warning_message }}</p>
              <div class="mt-2 text-xs text-gray-300">
                Confidence: {{ Math.round(analysisResult.confidence * 100) }}%
              </div>
            </div>
          </div>

          <!-- Transcript Section -->
          <div class="mt-8 bg-gray-700/50 rounded-2xl p-4 max-h-40 overflow-y-auto">
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
import { ref, computed, onMounted, onUnmounted } from 'vue'

export default {
  name: 'CallScreen',
  
  setup() {
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
      // In a real app, this would navigate away or close the screen
      alert('Call ended. VocalGuard analysis ' + (analysisResult.value?.is_scam ? 'detected a scam!' : 'found no threats.'))
    }

    // Analyze call
    const analyzeCall = async () => {
      isAnalyzing.value = true
      
      try {
        const response = await fetch('http://localhost:5000/analyze', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            transcript: transcript.value,
            generate_audio: false
          })
        })
        
        const data = await response.json()
        analysisResult.value = data
        
        // Update call status based on result
        if (data.is_scam) {
          callStatus.value = '⚠️ SCAM DETECTED'
        } else {
          callStatus.value = '✓ Legitimate Call'
        }
      } catch (error) {
        console.error('Analysis failed:', error)
        alert('Failed to analyze call. Make sure the backend server is running.')
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
