<template>
  <div class="bg-gray-800 rounded-2xl p-6">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-white text-xl font-bold">📋 Call History</h3>
      <button 
        @click="clearHistory"
        class="text-red-400 hover:text-red-300 text-sm"
      >
        Clear All
      </button>
    </div>
    
    <div v-if="history.length === 0" class="text-gray-400 text-center py-8">
      No calls analyzed yet
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
            <p class="text-white font-semibold">{{ call.caller }}</p>
            <p class="text-gray-400 text-sm">{{ call.number }}</p>
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
          <span>Confidence: {{ Math.round(call.confidence * 100) }}%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'CallHistory',
  emits: ['view-call'],
  
  setup(props, { emit }) {
    const history = ref([])
    
    const loadHistory = () => {
      const stored = localStorage.getItem('vocalguard_history')
      if (stored) {
        history.value = JSON.parse(stored)
      }
    }
    
    const clearHistory = () => {
      if (confirm('Clear all call history?')) {
        localStorage.removeItem('vocalguard_history')
        history.value = []
      }
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
    
    onMounted(() => {
      loadHistory()
      // Refresh history every 5 seconds
      setInterval(loadHistory, 5000)
    })
    
    return {
      history,
      clearHistory,
      viewCall,
      formatDate
    }
  }
}
</script>
