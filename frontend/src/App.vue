<template>
  <div id="app">
    <!-- Show Login/Signup when not authenticated -->
    <template v-if="!isAuthenticated">
      <Login 
        v-if="authView === 'login'"
        @switch-to-signup="authView = 'signup'"
        @login-success="handleAuthSuccess"
      />
      <Signup
        v-else
        @switch-to-login="authView = 'login'"
        @signup-success="handleAuthSuccess"
      />
    </template>

    <!-- Main App (when authenticated) -->
    <template v-else>
      <!-- Navigation Tabs with Enhanced Design -->
      <div class="sticky top-0 z-50 bg-gradient-to-b from-slate-900/95 via-slate-900 to-slate-950 border-b border-slate-800/50 shadow-2xl backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-4 py-4">
          <!-- Logo Section with User Profile -->
          <div class="mb-4 flex items-center justify-between">
            <div class="text-center flex-1">
              <h1 class="text-3xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
                🛡️ VocalGuard
              </h1>
              <p class="text-xs text-gray-500 mt-1">Advanced Scam Detection System</p>
            </div>
            
            <!-- User Profile Dropdown -->
            <div class="relative">
              <button
                @click="showUserMenu = !showUserMenu"
                class="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-800/50 border border-slate-700 hover:border-purple-500 transition-all"
              >
                <div class="w-8 h-8 rounded-full bg-gradient-to-r from-purple-500 to-blue-500 flex items-center justify-center text-white font-bold">
                  {{ user?.email?.[0]?.toUpperCase() || 'U' }}
                </div>
                <div class="text-left hidden md:block">
                  <p class="text-sm text-white font-semibold">{{ user?.username || user?.email }}</p>
                  <p class="text-xs text-gray-400">{{ user?.email }}</p>
                </div>
                <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
              </button>
              
              <!-- Dropdown Menu -->
              <div
                v-if="showUserMenu"
                class="absolute right-0 mt-2 w-64 bg-slate-800 border border-slate-700 rounded-lg shadow-2xl py-2"
              >
                <div class="px-4 py-3 border-b border-slate-700">
                  <p class="text-sm text-white font-semibold">{{ user?.username }}</p>
                  <p class="text-xs text-gray-400">{{ user?.email }}</p>
                  <div class="mt-2 flex gap-4 text-xs">
                    <div>
                      <p class="text-gray-400">Calls Analyzed</p>
                      <p class="text-white font-bold">{{ user?.total_calls_analyzed || 0 }}</p>
                    </div>
                    <div>
                      <p class="text-gray-400">Scams Blocked</p>
                      <p class="text-red-400 font-bold">{{ user?.scams_blocked || 0 }}</p>
                    </div>
                  </div>
                </div>
                <button
                  @click="handleLogout"
                  class="w-full px-4 py-2 text-left text-red-400 hover:bg-slate-700 transition-colors flex items-center gap-2"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                  </svg>
                  Logout
                </button>
              </div>
            </div>
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
    </template>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAuth } from './composables/useAuth'
import Login from './components/Login.vue'
import Signup from './components/Signup.vue'
import CallScreenEnhanced from './components/CallScreenEnhanced.vue'
import ScenarioSelector from './components/ScenarioSelector.vue'
import CallHistory from './components/CallHistory.vue'
import StatsDashboardEnhanced from './components/StatsDashboardEnhanced.vue'

export default {
  name: 'App',
  components: {
    Login,
    Signup,
    CallScreenEnhanced,
    ScenarioSelector,
    CallHistory,
    StatsDashboardEnhanced
  },
  
  setup() {
    const { isAuthenticated, user, logout, checkAuth } = useAuth()
    
    const authView = ref('login')
    const currentTab = ref('call')
    const selectedScenario = ref(null)
    const showUserMenu = ref(false)
    
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
      // No longer saving to localStorage - backend handles it
      console.log('Call analyzed:', data)
    }
    
    const handleAuthSuccess = () => {
      console.log('Authentication successful')
      showUserMenu.value = false
    }
    
    const handleLogout = () => {
      logout()
      showUserMenu.value = false
      currentTab.value = 'call'
    }
    
    // Check authentication on mount
    onMounted(async () => {
      await checkAuth()
    })

    return {
      isAuthenticated,
      user,
      authView,
      currentTab,
      selectedScenario,
      showUserMenu,
      tabs,
      handleScenarioSelected,
      handleCallAnalyzed,
      handleAuthSuccess,
      handleLogout
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
