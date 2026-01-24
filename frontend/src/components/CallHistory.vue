<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h3 class="text-slate-900 text-xl font-bold">📋 Call History</h3>
      <button 
        @click="refreshHistory"
        :disabled="loading"
        class="text-blue-600 hover:text-blue-700 text-sm font-medium hover:bg-blue-50 px-3 py-1 rounded-lg transition-colors disabled:opacity-50"
      >
        {{ loading ? 'Updating...' : '🔄 Reload' }}
      </button>
    </div>
    
    <div v-if="error" class="text-red-600 text-center py-4 mb-4 bg-red-50 rounded-lg text-sm border border-red-100">
      {{ error }}
    </div>
    
    <div v-if="history.length === 0 && !loading" class="text-slate-400 text-center py-12 bg-slate-50 rounded-xl border border-dashed border-slate-200">
      <p class="mb-2">No calls analyzed yet</p>
      <p class="text-xs">Start a call simulation to see history here</p>
    </div>
    
    <div v-if="loading && history.length === 0" class="text-slate-400 text-center py-12 bg-slate-50 rounded-xl border border-dashed border-slate-200">
      <div class="flex items-center justify-center gap-2">
        <svg class="animate-spin h-5 w-5 text-blue-500" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Loading call history...
      </div>
    </div>
    
    <div v-else class="space-y-3 max-h-96 overflow-y-auto pr-2 custom-scroll">
      <div
        v-for="call in history"
        :key="call.id"
        class="bg-white border border-slate-200 rounded-xl p-4 cursor-pointer hover:border-blue-300 hover:shadow-md transition-all duration-200"
        @click="viewCall(call)"
      >
        <div class="flex justify-between items-start mb-2">
          <div>
            <p class="text-slate-900 font-semibold">{{ call.caller_name || 'Unknown' }}</p>
            <p class="text-slate-500 text-sm">{{ call.caller_number || 'Unknown' }}</p>
            <p v-if="call.language && call.language !== 'en'" class="text-xs text-indigo-500 mt-1">
              {{ getLanguageName(call.language) }}
            </p>
          </div>
          <span 
            :class="[
              'px-3 py-1 rounded-full text-xs font-bold border',
              call.is_scam 
                ? 'bg-red-50 border-red-200 text-red-700' 
                : 'bg-green-50 border-green-200 text-green-700'
            ]"
          >
            {{ call.is_scam ? '⚠️ SCAM' : '✓ Safe' }}
          </span>
        </div>
        
        <p class="text-slate-600 text-sm mb-3 truncate bg-slate-50 p-2 rounded-lg">
          {{ call.transcript }}
        </p>
        
        <div class="flex justify-between items-center text-xs text-slate-400">
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
        const response = await fetch('http://localhost:5000/api/calls/history?limit=50')
        
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
