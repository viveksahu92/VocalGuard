<template>
  <div class="bg-gray-800 rounded-2xl p-6">
    <h3 class="text-white text-xl font-bold mb-4">📊 Analytics Dashboard</h3>
    
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-gray-700 rounded-xl p-4 text-center">
        <p class="text-gray-400 text-sm mb-1">Total Calls</p>
        <p class="text-white text-3xl font-bold">{{ stats.totalCalls }}</p>
      </div>
      
      <div class="bg-red-900/30 rounded-xl p-4 text-center border border-red-500/30">
        <p class="text-gray-400 text-sm mb-1">Scams Detected</p>
        <p class="text-red-300 text-3xl font-bold">{{ stats.scamsDetected }}</p>
      </div>
      
      <div class="bg-green-900/30 rounded-xl p-4 text-center border border-green-500/30">
        <p class="text-gray-400 text-sm mb-1">Safe Calls</p>
        <p class="text-green-300 text-3xl font-bold">{{ stats.safeCalls }}</p>
      </div>
      
      <div class="bg-blue-900/30 rounded-xl p-4 text-center border border-blue-500/30">
        <p class="text-gray-400 text-sm mb-1">Detection Rate</p>
        <p class="text-blue-300 text-3xl font-bold">{{ stats.detectionRate }}%</p>
      </div>
    </div>
    
    <div class="bg-gray-700 rounded-xl p-4">
      <h4 class="text-white font-semibold mb-3">Top Threat Types</h4>
      <div class="space-y-2">
        <div
          v-for="threat in stats.topThreats"
          :key="threat.name"
          class="flex justify-between items-center"
        >
          <span class="text-gray-300 text-sm">{{ threat.name }}</span>
          <div class="flex items-center gap-2">
            <div class="w-32 bg-gray-600 rounded-full h-2">
              <div
                :style="{ width: threat.percentage + '%' }"
                class="bg-red-500 rounded-full h-2"
              ></div>
            </div>
            <span class="text-gray-400 text-sm w-12 text-right">{{ threat.count }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'

export default {
  name: 'StatsDashboard',
  
  setup() {
    const history = ref([])
    
    const stats = computed(() => {
      const totalCalls = history.value.length
      const scamsDetected = history.value.filter(c => c.is_scam).length
      const safeCalls = totalCalls - scamsDetected
      const detectionRate = totalCalls > 0 ? Math.round((scamsDetected / totalCalls) * 100) : 0
      
      // Count threat types
      const threatCounts = {}
      history.value.forEach(call => {
        if (call.detected_threats) {
          call.detected_threats.forEach(threat => {
            threatCounts[threat] = (threatCounts[threat] || 0) + 1
          })
        }
      })
      
      const topThreats = Object.entries(threatCounts)
        .map(([name, count]) => ({
          name: name.replace(/_/g, ' ').toUpperCase(),
          count,
          percentage: Math.round((count / scamsDetected) * 100) || 0
        }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 5)
      
      return {
        totalCalls,
        scamsDetected,
        safeCalls,
        detectionRate,
        topThreats
      }
    })
    
    const loadHistory = () => {
      const stored = localStorage.getItem('vocalguard_history')
      if (stored) {
        history.value = JSON.parse(stored)
      }
    }
    
    onMounted(() => {
      loadHistory()
      setInterval(loadHistory, 5000)
    })
    
    return {
      stats
    }
  }
}
</script>
