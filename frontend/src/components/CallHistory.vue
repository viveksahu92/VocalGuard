<template>
  <div class="bg-gray-800 rounded-2xl p-6">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-white text-xl font-bold">📋 Call History</h3>
      <button 
        @click="refreshHistory"
        :disabled="loading"
        class="text-purple-400 hover:text-purple-300 text-sm disabled:opacity-50"
      >
        {{ loading ? 'Loading...' : '🔄 Refresh' }}
      </button>
    </div>
    
    <div v-if="error" class="text-red-400 text-center py-4 mb-4 bg-red-500/10 rounded-lg">
      {{ error }}
    </div>
    
    <div v-if="history.length === 0 && !loading" class="text-gray-400 text-center py-8">
      No calls analyzed yet
    </div>
    
    <div v-if="loading && history.length === 0" class="text-gray-400 text-center py-8">
      <div class="flex items-center justify-center gap-2">
        <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Loading call history...
      </div>
    </div>
    
    <div v-else class="space-y-3 max-h-96 overflow-y-auto">
      <div
        v-for="call in history"
        :key="call.id"
        class="bg-gray-700 rounded-xl p-4 cursor-pointer hover:bg-gray-600 transition"
        @click="viewCall(call)"
      >
        <div class="flex justify-between items-start mb-2">
          <div>
            <p class="text-white font-semibold">{{ call.caller_name || 'Unknown' }}</p>
            <p class="text-gray-400 text-sm">{{ call.caller_number || 'Unknown' }}</p>
            <p v-if="call.language && call.language !== 'en'" class="text-xs text-purple-400">
              {{ getLanguageName(call.language) }}
            </p>
          </div>
          <span 
            :class="[
              'px-3 py-1 rounded-full text-xs font-bold',
              call.is_scam 
                ? 'bg-red-500/20 text-red-300' 
                : 'bg-green-500/20 text-green-300'
            ]"
          >
            {{ call.is_scam ? '⚠️ SCAM' : '✓ Safe' }}
          </span>
        </div>
        
        <p class="text-gray-300 text-sm mb-2 truncate">
          {{ call.transcript }}
        </p>
        
        <div class="flex justify-between items-center text-xs text-gray-400">
          <span>{{ formatDate(call.timestamp) }}</span>
          <span>Confidence: {{ Math.round((call.confidence || 0) * 100) }}%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAuth } from '../composables/useAuth'

export default {
  name: 'CallHistory',
  emits: ['view-call'],
  
  setup(props, { emit }) {
    const { getToken } = useAuth()
    const history = ref([])
    const loading = ref(false)
    const error = ref('')
    
    const loadHistory = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const token = getToken()
        if (!token) {
          error.value = 'Please log in to view call history'
          return
        }
        
        const response = await fetch('http://localhost:5000/api/calls/history?limit=50', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        
        const data = await response.json()
        
        if (!response.ok) {
          throw new Error(data.error || 'Failed to fetch call history')
        }
        
        history.value = data.calls || []
      } catch (err) {
        console.error('Load history error:', err)
        error.value = err.message
      } finally {
        loading.value = false
      }
    }
    
    const refreshHistory = () => {
      loadHistory()
    }
    
    const viewCall = (call) => {
      emit('view-call', call)
    }
    
    const formatDate = (timestamp) => {
      const date = new Date(timestamp)
      return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    const getLanguageName = (code) => {
      const langs = {
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'zh': 'Chinese',
        'hi': 'Hindi',
        'ar': 'Arabic'
      }
      return langs[code] || code.toUpperCase()
    }
    
    onMounted(() => {
      loadHistory()
    })
    
    return {
      history,
      loading,
      error,
      refreshHistory,
      viewCall,
      formatDate,
      getLanguageName
    }
  }
}
</script>
