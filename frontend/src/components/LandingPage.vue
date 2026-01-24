<template>
  <div class="min-h-screen bg-slate-50">
    <!-- Hero Section -->
    <div class="relative overflow-hidden">
      <!-- Background Decorative Elements -->
      <!-- Background Decorative Elements (Removed to fix Cyan Dot artifact) -->

      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16 text-center relative z-10">
        <div class="inline-flex items-center px-4 py-2 rounded-full bg-blue-50 border border-blue-100 mb-8">
          <span class="text-sm font-medium text-blue-700">AI-Powered Scam Protection</span>
        </div>
        
        <h1 class="text-5xl md:text-7xl font-bold text-slate-900 tracking-tight mb-6">
          Protect Your Voice,<br/>
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Secure Your Money</span>
        </h1>
        
        <p class="mt-4 text-xl text-slate-600 max-w-2xl mx-auto mb-10">
          VocalGuard uses advanced AI to detect financial scams in real-time calls. 
          Stay safe from fraud with instant alerts and detailed analysis.
        </p>
        
        <div class="flex justify-center gap-4">
          <button 
            @click="$emit('start')"
            class="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all duration-300 flex items-center group"
          >
            Start Protection
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </button>
          
          <button 
            @click="$emit('learn-more')"
            class="px-8 py-4 bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 text-lg font-semibold rounded-xl hover:shadow-md transition-all duration-300"
          >
            Learn More
          </button>
        </div>
      </div>
    </div>

    <!-- Stats Section -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 text-center hover:shadow-md transition-shadow">
          <div class="text-4xl font-bold text-blue-600 mb-2">99.9%</div>
          <div class="text-slate-600 font-medium">Detection Accuracy</div>
        </div>
        <div class="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 text-center hover:shadow-md transition-shadow">
          <div class="text-4xl font-bold text-indigo-600 mb-2">0ms</div>
          <div class="text-slate-600 font-medium">Analysis Latency</div>
        </div>
        <div class="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 text-center hover:shadow-md transition-shadow">
          <div class="text-4xl font-bold text-sky-600 mb-2">24/7</div>
          <div class="text-slate-600 font-medium">Real-time Monitoring</div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="bg-white py-24">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl font-bold text-slate-900">Why Choose VocalGuard?</h2>
          <p class="mt-4 text-slate-600">Comprehensive protection against modern voice fraud.</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-12">
          <!-- Feature 1 -->
          <div class="group">
            <div class="w-14 h-14 bg-blue-100 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <span class="text-2xl">🛡️</span>
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-3">Real-time Analysis</h3>
            <p class="text-slate-600 leading-relaxed">
              Analyzes conversation patterns instantly to identify potential threats before they cause harm.
            </p>
          </div>

          <!-- Feature 2 -->
          <div class="group">
            <div class="w-14 h-14 bg-indigo-100 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <span class="text-2xl">📊</span>
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-3">Risk Scoring</h3>
            <p class="text-slate-600 leading-relaxed">
              Advanced algorithms assign risk scores to calls, differentiating between safe and suspicious activity.
            </p>
          </div>

          <!-- Feature 3 -->
          <div class="group">
            <div class="w-14 h-14 bg-sky-100 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <span class="text-2xl">📝</span>
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-3">Transcripts & Logs</h3>
            <p class="text-slate-600 leading-relaxed">
              Automatically generates and stores call transcripts for evidence and review purposes.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LandingPage',
  emits: ['start', 'learn-more']
}
</script>
