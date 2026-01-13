<template>
  <div id="app">
    <!-- Navigation Tabs with Enhanced Design -->
    <div class="sticky top-0 z-50 bg-gradient-to-b from-slate-900/95 via-slate-900 to-slate-950 border-b border-slate-800/50 shadow-2xl backdrop-blur-md">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <!-- Logo Section -->
        <div class="mb-4 text-center">
          <h1 class="text-3xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
            🛡️ VocalGuard
          </h1>
          <p class="text-xs text-gray-500 mt-1">Advanced Scam Detection System</p>
        </div>
        
        <!-- Tab Navigation -->
        <div class="flex gap-2 justify-center flex-wrap">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="currentTab = tab.id"
            :class="[
              'px-6 py-2.5 rounded-lg font-semibold transition-all duration-300 backdrop-blur-sm',
              currentTab === tab.id
                ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg shadow-purple-500/50 scale-105'
                : 'text-gray-400 hover:text-white hover:bg-slate-800/50 border border-transparent hover:border-slate-700/50'
            ]"
          >
            {{ tab.name }}
          </button>
        </div>
      </div>
    </div>

    <!-- Content Area -->
    <div>
      <CallScreenEnhanced 
        v-if="currentTab === 'call'"
        :selectedScenario="selectedScenario"
        @call-analyzed="handleCallAnalyzed"
      />
      <ScenarioSelector 
        v-else-if="currentTab === 'scenarios'"
        @scenario-selected="handleScenarioSelected"
      />
      <CallHistory 
        v-else-if="currentTab === 'history'"
      />
      <StatsDashboardEnhanced 
        v-else-if="currentTab === 'analytics'"
      />
    </div>

    <!-- Footer -->
    <div class="border-t border-slate-800/50 bg-gradient-to-t from-slate-950 to-transparent py-6">
      <div class="max-w-7xl mx-auto px-4 text-center text-gray-500 text-sm">
        <p>Built for Nexora Hacks 2026 • 100% Free • No API Costs</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import CallScreenEnhanced from './components/CallScreenEnhanced.vue'
import ScenarioSelector from './components/ScenarioSelector.vue'
import CallHistory from './components/CallHistory.vue'
import StatsDashboardEnhanced from './components/StatsDashboardEnhanced.vue'

export default {
  name: 'App',
  components: {
    CallScreenEnhanced,
    ScenarioSelector,
    CallHistory,
    StatsDashboardEnhanced
  },
  
  setup() {
    const currentTab = ref('call')
    const selectedScenario = ref(null)
    
    const tabs = [
      { id: 'call', name: '📱 Call Analysis' },
      { id: 'scenarios', name: '🎯 Test Scenarios' },
      { id: 'history', name: '📋 Call History' },
      { id: 'analytics', name: '📊 Analytics' }
    ]
    
    const handleScenarioSelected = (scenario) => {
      selectedScenario.value = scenario
      currentTab.value = 'call'
    }
    
    const handleCallAnalyzed = (data) => {
      // Save to history in localStorage
      const history = JSON.parse(localStorage.getItem('vocalguard_history') || '[]')
      history.push({
        id: Date.now(),
        timestamp: new Date().toISOString(),
        ...data
      })
      localStorage.setItem('vocalguard_history', JSON.stringify(history))
    }

    return {
      currentTab,
      selectedScenario,
      tabs,
      handleScenarioSelected,
      handleCallAnalyzed
    }
  }
}
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
}

#app {
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
  min-height: 100vh;
}
</style>
