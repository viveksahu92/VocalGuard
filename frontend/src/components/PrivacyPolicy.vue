<template>
  <div class="p-8 max-w-4xl mx-auto">
    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-8">
      <h1 class="text-3xl font-bold text-slate-900 mb-6">Privacy Policy</h1>
      <p class="text-slate-500 text-sm mb-8">Last updated: January 19, 2026</p>
      
      <div class="prose prose-slate max-w-none text-slate-600 relative z-50">
        <p class="mb-6">
          At VocalGuard, we take your privacy seriously. This Privacy Policy explains how we collect, use, and protect your information when you use our scam detection services.
        </p>

        <h2 class="text-xl font-bold text-slate-900 mt-8 mb-4">1. Information We Process</h2>
        <p class="mb-4">
          To provide real-time scam detection, we process:
        </p>
        <ul class="list-disc pl-5 mb-6 space-y-2">
          <li><strong>Audio Data:</strong> Temporary audio streams from calls are analyzed for scam patterns.</li>
          <li><strong>Transcripts:</strong> Text-based transcripts are generated for analysis purposes.</li>
          <li><strong>Call Metadata:</strong> Information such as timestamp, duration, and caller ID (if available).</li>
        </ul>

        <h2 class="text-xl font-bold text-slate-900 mt-8 mb-4">2. Data Storage & Protection</h2>
        <p class="mb-4">
          We prioritize local processing and ephemeral data handling:
        </p>
        <ul class="list-disc pl-5 mb-6 space-y-2">
          <li>Audio streams are processed in real-time and are <strong>not permanently stored</strong> on our servers.</li>
          <li>Transcripts are stored locally on your device for history review unless you choose to clear them.</li>
          <li>We do not sell your personal data to third parties.</li>
        </ul>

        <h2 class="text-xl font-bold text-slate-900 mt-8 mb-4">3. Improvement of Services</h2>
        <p class="mb-6">
          We may strictly use anonymized, aggregated data (scam patterns, detection rates) to improve our AI models and threat databases. No personally identifiable information is included in this dataset.
        </p>

        <div class="bg-blue-50 p-4 rounded-lg border border-blue-100 mt-8">
          <p class="text-sm text-blue-800">
            <strong>Contact Us:</strong> If you have any questions about this Privacy Policy, please contact us at privacy@vocalguard.com
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
  name: 'PrivacyPolicy',
  emits: ['close']
}
</script>
