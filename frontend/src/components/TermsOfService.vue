<template>
  <div class="p-8 max-w-4xl mx-auto">
    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-8">
      <h1 class="text-3xl font-bold text-slate-900 mb-6">Terms of Service</h1>
      <p class="text-slate-500 text-sm mb-8">Last updated: January 24, 2026</p>
      
      <div class="prose prose-slate max-w-none text-slate-600 relative z-50">
        <p class="mb-6">
          Welcome to VocalGuard. By using our services, you agree to these terms.
        </p>

        <h2 class="text-xl font-bold text-slate-900 mt-8 mb-4">1. Acceptance of Terms</h2>
        <p class="mb-4">
          By accessing or using VocalGuard, you agree to be bound by these Terms of Service. If you do not agree to these terms, please do not use our services.
        </p>

        <h2 class="text-xl font-bold text-slate-900 mt-8 mb-4">2. Description of Service</h2>
        <p class="mb-4">
          VocalGuard provides real-time scam detection analysis for phone calls using artificial intelligence. This service is intended for informational and safety purposes only.
        </p>

        <h2 class="text-xl font-bold text-slate-900 mt-8 mb-4">3. User Responsibilities</h2>
        <ul class="list-disc pl-5 mb-6 space-y-2">
          <li>You are responsible for obtaining necessary consents for recording calls where required by law.</li>
          <li>You agree not to use the service for illegal purposes.</li>
          <li>You agree not to attempt to reverse engineer the AI models.</li>
        </ul>

        <h2 class="text-xl font-bold text-slate-900 mt-8 mb-4">4. Limitation of Liability</h2>
        <p class="mb-6">
          VocalGuard is an assistive tool and may not detect all scams. We are not liable for any financial losses incurred while using the service. Always verify caller identity independently.
        </p>

        <div class="bg-gray-50 p-4 rounded-lg border border-gray-100 mt-8">
          <p class="text-sm text-gray-800">
            <strong>Contact:</strong> legal@vocalguard.com
          </p>
        </div>
      </div>

      <div class="mt-12 flex justify-center">
        <button 
          @click="$emit('close')"
          class="px-6 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg transition-colors"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TermsOfService',
  emits: ['close']
}
</script>
