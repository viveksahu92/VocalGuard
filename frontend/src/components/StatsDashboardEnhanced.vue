<template>
  <div class="p-6">
    <div class="relative z-10">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900 mb-2">
          Analytics Dashboard
        </h1>
        <p class="text-slate-500">Real-time scam detection statistics and threat analysis</p>
      </div>

      <!-- KPI Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <!-- Total Calls Card -->
        <div class="group cursor-pointer">
          <div class="relative bg-white rounded-2xl p-6 border border-slate-200 shadow-sm hover:shadow-md transition-all duration-300 transform hover:-translate-y-1">
            <div class="relative">
              <div class="text-blue-600 text-sm font-semibold mb-2">📞 Total Calls Analyzed</div>
              <div class="text-4xl font-bold text-slate-900 mb-2">{{ stats.totalCalls }}</div>
              <div class="text-xs text-slate-500">{{ stats.todayCallsCount }} calls today</div>
            </div>
          </div>
        </div>

        <!-- Scams Detected Card -->
        <div class="group cursor-pointer">
          <div class="relative bg-white rounded-2xl p-6 border border-slate-200 shadow-sm hover:shadow-md transition-all duration-300 transform hover:-translate-y-1">
            <div class="relative">
              <div class="text-red-600 text-sm font-semibold mb-2">⚠️ Scams Detected</div>
              <div class="text-4xl font-bold text-slate-900 mb-2">{{ stats.scamCount }}</div>
              <div class="text-xs text-slate-500">{{ scamRate }}% detection rate</div>
            </div>
          </div>
        </div>

        <!-- Safe Calls Card -->
        <div class="group cursor-pointer">
          <div class="relative bg-white rounded-2xl p-6 border border-slate-200 shadow-sm hover:shadow-md transition-all duration-300 transform hover:-translate-y-1">
            <div class="relative">
              <div class="text-emerald-600 text-sm font-semibold mb-2">✓ Legitimate Calls</div>
              <div class="text-4xl font-bold text-slate-900 mb-2">{{ stats.safeCount }}</div>
              <div class="text-xs text-slate-500">{{ safeRate }}% verified safe</div>
            </div>
          </div>
        </div>

        <!-- Average Risk Score Card -->
        <div class="group cursor-pointer">
          <div class="relative bg-white rounded-2xl p-6 border border-slate-200 shadow-sm hover:shadow-md transition-all duration-300 transform hover:-translate-y-1">
            <div class="relative">
              <div class="text-orange-600 text-sm font-semibold mb-2">📊 Avg Risk Score</div>
              <div class="text-4xl font-bold text-slate-900 mb-2">{{ averageRiskScore }}/100</div>
              <div class="text-xs text-slate-500">Based on all analyzed calls</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- Threat Type Distribution -->
        <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
          <h3 class="text-slate-900 font-bold text-lg mb-6 flex items-center gap-2">
            🎯 Top Threat Types
          </h3>
          <div class="space-y-4">
            <div v-for="threat in topThreats" :key="threat.type" class="group">
              <div class="flex justify-between items-center mb-1.5">
                <span class="text-slate-700 text-sm font-medium">{{ formatThreat(threat.type) }}</span>
                <span class="text-slate-500 text-sm">{{ threat.count }} detections</span>
              </div>
              <div class="relative h-2.5 bg-slate-100 rounded-full overflow-hidden">
                <div
                  :style="{ width: threat.percentage + '%' }"
                  :class="[
                    'h-full rounded-full transition-all duration-500',
                    getThreatColor(threat.type)
                  ]"
                ></div>
              </div>
              <div class="text-xs text-slate-400 mt-1">{{ threat.percentage }}%</div>
            </div>
          </div>
        </div>

        <!-- Language Distribution -->
        <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
          <h3 class="text-slate-900 font-bold text-lg mb-6 flex items-center gap-2">
            🌍 Language Detection
          </h3>
          <div class="space-y-4">
            <div v-for="lang in languageStats" :key="lang.code" class="group">
              <div class="flex justify-between items-center mb-1.5">
                <span class="text-slate-700 text-sm font-medium">{{ lang.name }}</span>
                <span class="text-slate-500 text-sm">{{ lang.count }} calls</span>
              </div>
              <div class="relative h-2.5 bg-slate-100 rounded-full overflow-hidden">
                <div
                  :style="{ width: lang.percentage + '%' }"
                  class="h-full bg-blue-500 rounded-full transition-all duration-500"
                ></div>
              </div>
              <div class="text-xs text-slate-400 mt-1">{{ lang.percentage }}%</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Detailed Stats Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <!-- High Risk Calls -->
        <div class="bg-red-50 rounded-2xl p-6 border border-red-100 shadow-sm">
          <h3 class="text-red-900 font-bold text-lg mb-4 flex items-center gap-2">
            🚨 High Risk Calls
          </h3>
          <div class="text-4xl font-bold text-red-600 mb-2">
            {{ highRiskCount }}
          </div>
          <p class="text-red-700/70 text-sm">Risk score >= 70</p>
        </div>

        <!-- Medium Risk Calls -->
        <div class="bg-orange-50 rounded-2xl p-6 border border-orange-100 shadow-sm">
          <h3 class="text-orange-900 font-bold text-lg mb-4 flex items-center gap-2">
            ⚠️ Medium Risk Calls
          </h3>
          <div class="text-4xl font-bold text-orange-600 mb-2">
            {{ mediumRiskCount }}
          </div>
          <p class="text-orange-700/70 text-sm">Risk score 40-70</p>
        </div>

        <!-- Low Risk Calls -->
        <div class="bg-emerald-50 rounded-2xl p-6 border border-emerald-100 shadow-sm">
          <h3 class="text-emerald-900 font-bold text-lg mb-4 flex items-center gap-2">
            ✓ Low Risk Calls
          </h3>
          <div class="text-4xl font-bold text-emerald-600 mb-2">
            {{ lowRiskCount }}
          </div>
          <p class="text-emerald-700/70 text-sm">Risk score < 40</p>
        </div>
      </div>

      <!-- Recent Alerts -->
      <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
        <h3 class="text-slate-900 font-bold text-lg mb-6 flex items-center gap-2">
          📋 Recent Scam Alerts
        </h3>
        <div class="space-y-3 max-h-80 overflow-y-auto pr-2 custom-scroll">
          <div v-if="recentAlerts.length === 0" class="text-slate-500 text-center py-8">
            <p>No scam alerts yet. VocalGuard is monitoring...</p>
          </div>
          <div 
            v-for="alert in recentAlerts" 
            :key="alert.id"
            class="bg-slate-50 rounded-lg p-4 border border-slate-200 hover:border-red-200 transition-all duration-200"
          >
            <div class="flex justify-between items-start gap-4">
              <div class="flex-1">
                <p class="text-slate-900 font-semibold">{{ alert.caller }}</p>
                <p class="text-slate-500 text-sm">{{ alert.number }}</p>
                <div class="flex flex-wrap gap-2 mt-2">
                  <span 
                    v-for="threat in alert.threats" 
                    :key="threat"
                    class="text-xs bg-red-100 text-red-700 px-2 py-1 rounded-full border border-red-200"
                  >
                    {{ formatThreat(threat) }}
                  </span>
                </div>
              </div>
              <div class="text-right">
                <div class="text-2xl font-bold text-red-600">{{ alert.risk }}/100</div>
                <p class="text-xs text-slate-400 mt-1">{{ formatTime(alert.timestamp) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="mt-8 text-center text-slate-400 text-sm">
        <p>Data updated in real-time • Last refresh: {{ lastRefreshTime }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'

export default {
  name: 'StatsDashboardEnhanced',
  
  setup() {
    const stats = ref({
      totalCalls: 0,
      scamCount: 0,
      safeCount: 0,
      todayCallsCount: 0,
      averageRiskScore: 0
    })

    const threatStats = ref({
      urgency: 0,
      payment_request: 0,
      personal_info: 0,
      impersonation: 0,
      threats: 0,
      too_good_to_be_true: 0
    })

    const recentAlerts = ref([])
    const lastRefreshTime = ref('just now')

    // Load data from localStorage
    const loadStats = () => {
      const history = JSON.parse(localStorage.getItem('vocalguard_history') || '[]')
      
      stats.value.totalCalls = history.length
      stats.value.scamCount = history.filter(c => c.is_scam).length
      stats.value.safeCount = history.filter(c => !c.is_scam).length
      
      if (stats.value.totalCalls > 0) {
        const totalScore = history.reduce((sum, c) => {
          const score = parseFloat(c.risk_score) || 0
          return sum + score
        }, 0)
        stats.value.averageRiskScore = Math.round(totalScore / stats.value.totalCalls)
      } else {
        stats.value.averageRiskScore = 0
      }

      // Count today's calls
      const today = new Date().toDateString()
      stats.value.todayCallsCount = history.filter(c => {
        const callDate = new Date(c.timestamp).toDateString()
        return callDate === today
      }).length

      // Count threat types
      threatStats.value = {
        urgency: 0,
        payment_request: 0,
        personal_info: 0,
        impersonation: 0,
        threats: 0,
        too_good_to_be_true: 0
      }

      history.forEach(call => {
        if (call.detected_threats && Array.isArray(call.detected_threats)) {
          call.detected_threats.forEach(threat => {
            if (threatStats.value.hasOwnProperty(threat)) {
              threatStats.value[threat]++
            }
          })
        }
      })

      // Get recent scam alerts
      recentAlerts.value = history
        .filter(c => c.is_scam)
        .slice(-10)
        .reverse()
        .map((c, idx) => ({
          id: idx,
          caller: c.caller,
          number: c.number,
          risk: Math.round(c.risk_score),
          threats: c.detected_threats || [],
          timestamp: c.timestamp
        }))

      updateRefreshTime()
    }

    const updateRefreshTime = () => {
      const now = new Date()
      lastRefreshTime.value = now.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        second: '2-digit'
      })
    }

    const topThreats = computed(() => {
      const total = Object.values(threatStats.value).reduce((a, b) => a + b, 1)
      return Object.entries(threatStats.value)
        .map(([type, count]) => ({
          type,
          count,
          percentage: Math.round((count / total) * 100)
        }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 6)
    })

    const languageStats = computed(() => {
      const history = JSON.parse(localStorage.getItem('vocalguard_history') || '[]')
      const langs = { EN: 0, ES: 0, FR: 0, HI: 0, OTHER: 0 }
      
      history.forEach(call => {
        const lang = call.detected_language || 'EN'
        if (langs.hasOwnProperty(lang)) {
          langs[lang]++
        } else {
          langs['OTHER']++
        }
      })

      const total = Object.values(langs).reduce((a, b) => a + b, 1)
      const langNames = {
        EN: '🇬🇧 English',
        ES: '🇪🇸 Spanish',
        FR: '🇫🇷 French',
        HI: '🇮🇳 Hindi',
        OTHER: '🌐 Other'
      }

      return Object.entries(langs)
        .map(([code, count]) => ({
          code,
          name: langNames[code],
          count,
          percentage: Math.round((count / total) * 100)
        }))
        .filter(l => l.count > 0)
        .sort((a, b) => b.count - a.count)
    })

    const scamRate = computed(() => {
      if (stats.value.totalCalls === 0) return 0
      return Math.round((stats.value.scamCount / stats.value.totalCalls) * 100)
    })

    const safeRate = computed(() => {
      if (stats.value.totalCalls === 0) return 0
      return Math.round((stats.value.safeCount / stats.value.totalCalls) * 100)
    })

    const highRiskCount = computed(() => {
      const history = JSON.parse(localStorage.getItem('vocalguard_history') || '[]')
      return history.filter(c => parseFloat(c.risk_score) >= 70).length
    })

    const mediumRiskCount = computed(() => {
      const history = JSON.parse(localStorage.getItem('vocalguard_history') || '[]')
      return history.filter(c => {
        const score = parseFloat(c.risk_score)
        return score >= 40 && score < 70
      }).length
    })

    const lowRiskCount = computed(() => {
      const history = JSON.parse(localStorage.getItem('vocalguard_history') || '[]')
      return history.filter(c => parseFloat(c.risk_score) < 40).length
    })

    const averageRiskScore = computed(() => {
      const val = stats.value.averageRiskScore
      return isNaN(val) || val === undefined ? 0 : Math.round(val)
    })

    const formatThreat = (threat) => {
      return threat.replace(/_/g, ' ').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')
    }

    const formatTime = (timestamp) => {
      const date = new Date(timestamp)
      const now = new Date()
      const diff = now - date
      const seconds = Math.floor(diff / 1000)
      const minutes = Math.floor(seconds / 60)
      const hours = Math.floor(minutes / 60)
      const days = Math.floor(hours / 24)

      if (seconds < 60) return 'just now'
      if (minutes < 60) return `${minutes}m ago`
      if (hours < 24) return `${hours}h ago`
      return `${days}d ago`
    }

    const getThreatColor = (threat) => {
      const colors = {
        urgency: 'bg-gradient-to-r from-red-500 to-red-600',
        payment_request: 'bg-gradient-to-r from-orange-500 to-orange-600',
        personal_info: 'bg-gradient-to-r from-yellow-500 to-yellow-600',
        impersonation: 'bg-gradient-to-r from-pink-500 to-pink-600',
        threats: 'bg-gradient-to-r from-purple-500 to-purple-600',
        too_good_to_be_true: 'bg-gradient-to-r from-blue-500 to-blue-600'
      }
      return colors[threat] || 'bg-gradient-to-r from-gray-500 to-gray-600'
    }

    // Auto-refresh every 5 seconds
    let refreshInterval = null
    onMounted(() => {
      loadStats()
      refreshInterval = setInterval(() => {
        loadStats()
      }, 5000)
    })

    onUnmounted(() => {
      if (refreshInterval) {
        clearInterval(refreshInterval)
      }
    })

    return {
      stats,
      threatStats,
      topThreats,
      languageStats,
      scamRate,
      safeRate,
      highRiskCount,
      mediumRiskCount,
      lowRiskCount,
      averageRiskScore,
      recentAlerts,
      lastRefreshTime,
      formatThreat,
      formatTime,
      getThreatColor,
      loadStats
    }
  }
}
</script>


