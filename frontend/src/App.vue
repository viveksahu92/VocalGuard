<template>
  <div id="app" class="min-h-screen bg-slate-50 text-slate-900 font-sans">
    
    <!-- View Switcher -->
    <template v-if="currentView === 'landing'">
      <LandingPage 
        @start="handleStart" 
        @learn-more="currentView = 'learn'" 
      />
    </template>

    <template v-else-if="currentView === 'not-found'">
      <NotFound @gohome="handleGoHome" />
    </template>

    <template v-else-if="currentView === 'learn'">
      <div class="min-h-screen flex flex-col">
        <nav class="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-200 shadow-sm">
          <div class="max-w-7xl mx-auto px-4 h-16 flex items-center">
            <div class="flex items-center cursor-pointer" @click="currentView = 'landing'">
              <span class="text-2xl mr-2">🛡️</span>
              <h1 class="text-xl font-bold text-slate-900">VocalGuard</h1>
            </div>
          </div>
        </nav>
        <LearnMore @back="currentView = 'landing'" />
      </div>
    </template>

    <template v-else-if="currentView === 'privacy'">
      <div class="min-h-screen flex flex-col">
        <nav class="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-200 shadow-sm">
          <div class="max-w-7xl mx-auto px-4 h-16 flex items-center">
            <div class="flex items-center cursor-pointer" @click="currentView = 'landing'">
              <span class="text-2xl mr-2">🛡️</span>
              <h1 class="text-xl font-bold text-slate-900">VocalGuard</h1>
            </div>
          </div>
        </nav>
        <PrivacyPolicy @close="currentView = 'landing'" />
      </div>
    </template>

    <template v-else-if="currentView === 'terms'">
      <div class="min-h-screen flex flex-col">
        <nav class="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-200 shadow-sm">
          <div class="max-w-7xl mx-auto px-4 h-16 flex items-center">
            <div class="flex items-center cursor-pointer" @click="currentView = 'landing'">
              <span class="text-2xl mr-2">🛡️</span>
              <h1 class="text-xl font-bold text-slate-900">VocalGuard</h1>
            </div>
          </div>
        </nav>
        <TermsOfService @close="currentView = 'landing'" />
      </div>
    </template>

    <!-- Main App View -->
    <div v-else class="min-h-screen flex flex-col">
      <!-- Enhanced Navbar -->
      <nav class="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-200 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between items-center h-16">
            
            <!-- Logo Left -->
            <div class="flex-shrink-0 flex items-center cursor-pointer" @click="currentView = 'landing'">
              <span class="text-2xl mr-2">🛡️</span>
              <div>
                <h1 class="text-xl font-bold text-slate-900 tracking-tight leading-none">VocalGuard</h1>
                <p class="text-[10px] text-slate-500 font-medium tracking-wide uppercase">Scam Detection</p>
              </div>
            </div>

            <!-- Navigation Links Right -->
            <div class="hidden md:flex items-center space-x-1">
              <button
                v-for="tab in tabs"
                :key="tab.id"
                @click="currentTab = tab.id"
                :class="[
                  'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200',
                  currentTab === tab.id
                    ? 'bg-blue-50 text-blue-700 shadow-sm ring-1 ring-blue-100'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                ]"
              >
                {{ tab.name }}
              </button>

              <!-- User Profile Dropdown (Optional Hidden or Simplified) -->
              <!-- Keeping hidden/simplified since we are removing login requirement -->
            </div>

            <!-- Mobile Menu Button (simplified) -->
            <div class="md:hidden flex items-center">
              <button class="text-slate-500 hover:text-slate-700">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
        
        <!-- Mobile Menu (Conditional, simplified for now) -->
        <div class="md:hidden border-t border-slate-100 bg-white" v-if="false">
          <div class="px-2 pt-2 pb-3 space-y-1">
             <button
                v-for="tab in tabs"
                :key="tab.id"
                @click="currentTab = tab.id"
                class="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-slate-700 hover:text-slate-900 hover:bg-slate-50"
              >
                {{ tab.name }}
              </button>
          </div>
        </div>
      </nav>

      <!-- Content Area -->
      <main class="flex-grow max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden min-h-[600px]">
          <CallScreenEnhanced 
            v-if="currentTab === 'call'"
            :selectedScenario="selectedScenario"
            @call-analyzed="handleCallAnalyzed"
            @call-ended="currentTab = 'scenarios'"
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
      </main>

      <!-- Footer -->
      <footer class="bg-white border-t border-slate-200 py-8">
        <div class="max-w-7xl mx-auto px-4 text-center">
          <p class="text-slate-500 text-sm">
            © 2026 VocalGuard • Built for Nexora Hacks • 
            <button @click="currentView = 'privacy'" class="text-blue-600 hover:underline">Privacy Policy</button> • 
            <button @click="currentView = 'terms'" class="text-blue-600 hover:underline">Terms</button>
          </p>
        </div>
      </footer>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAuth } from './composables/useAuth'
import Login from './components/Login.vue'
import Signup from './components/Signup.vue'
import LandingPage from './components/LandingPage.vue'
import LearnMore from './components/LearnMore.vue'
import PrivacyPolicy from './components/PrivacyPolicy.vue'
import CallScreenEnhanced from './components/CallScreenEnhanced.vue'
import ScenarioSelector from './components/ScenarioSelector.vue'
import CallHistory from './components/CallHistory.vue'
import StatsDashboardEnhanced from './components/StatsDashboardEnhanced.vue'
import TermsOfService from './components/TermsOfService.vue'
import NotFound from './components/NotFound.vue'

export default {
  name: 'App',
  components: {
    Login,
    Signup,
    LandingPage,
    LearnMore,
    PrivacyPolicy,
    CallScreenEnhanced,
    ScenarioSelector,
    CallHistory,
    StatsDashboardEnhanced,
    TermsOfService,
    NotFound
  },
  
  setup() {
    const { isAuthenticated, user, logout, checkAuth } = useAuth()
    
    // Auth & View State
    const authView = ref('login')
    const currentView = ref('landing')
    const currentTab = ref('call')
    const selectedScenario = ref(null)
    const showUserMenu = ref(false)
    
    const tabs = [
      { id: 'call', name: '📱 Call Analysis' },
      { id: 'scenarios', name: '🎯 Test Scenarios' },
      { id: 'history', name: '📋 Call History' },
      { id: 'analytics', name: '📊 Analytics' }
    ]
    
    const handleStart = () => {
      currentView.value = 'app'
    }

    const handleScenarioSelected = (scenario) => {
      selectedScenario.value = scenario
      currentTab.value = 'call'
    }
    
    const handleCallAnalyzed = (data) => {
      // Backend handles history saving now, but we can log it or show a toast
      console.log('Call analyzed:', data)
    }
    
    const handleAuthSuccess = () => {
      console.log('Authentication successful')
      showUserMenu.value = false
    }
    
    const handleLogout = () => {
      logout()
      showUserMenu.value = false
      currentView.value = 'landing' // Reset view
      currentTab.value = 'call'
    }
    


    const handleGoHome = () => {
      window.history.pushState({}, '', '/')
      currentView.value = 'landing'
    }
    
    // Check authentication on mount
    onMounted(async () => {
      await checkAuth()
      
      // Simple client-side router
      let path = window.location.pathname
      // Normalize path: remove trailing slash and weird casing if needed
      if (path.length > 1 && path.endsWith('/')) {
        path = path.slice(0, -1)
      }
      
      const lowerPath = path.toLowerCase()
      
      if (lowerPath === '/test-scenarios') {
        currentView.value = 'app'
        currentTab.value = 'scenarios'
      } else if (lowerPath === '/terms') {
        currentView.value = 'terms'
      } else if (lowerPath === '/privacy') {
        currentView.value = 'privacy'
      } else if (lowerPath !== '/' && lowerPath !== '/index.html' && lowerPath !== '/vocalguard') {
        currentView.value = 'not-found'
      }
    })

    return {
      isAuthenticated,
      user,
      authView,
      currentView,
      currentTab,
      selectedScenario,
      showUserMenu,
      tabs,
      handleStart,
      handleScenarioSelected,
      handleCallAnalyzed,
      handleAuthSuccess,
      handleLogout,
      handleGoHome
    }
  }
}
</script>

<style>
/* Global resets if needed, though Tailwind handles most */
html, body {
  height: 100%;
}
</style>
