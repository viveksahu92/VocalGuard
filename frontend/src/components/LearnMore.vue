<template>
  <div class="p-8 max-w-4xl mx-auto">
    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-8">
      <h1 class="text-3xl font-bold text-slate-900 mb-6">About VocalGuard</h1>
      
      <div class="prose prose-slate max-w-none text-slate-600">
        <p class="text-lg leading-relaxed mb-6">
          VocalGuard is an advanced AI-powered application designed to protect users from the rising tide of sophisticated voice scams. Using state-of-the-art machine learning, we analyze conversation patterns in real-time to detect threats before they result in financial loss.
        </p>

        <h2 class="text-xl font-bold text-slate-900 mt-8 mb-4">How It Works</h2>
        <ul class="space-y-4 list-disc pl-5 mb-8">
          <li>
            <strong>Real-time Audio Analysis:</strong> Our AI processes audio streams instantly to identify keywords, tone patterns, and scripts used by known scammers.
          </li>
          <li>
            <strong>Scam Pattern Matching:</strong> We maintain a constantly updated database of scam scenarios (IRS impersonation, Tech Support fraud, Grandparent scams) to match against.
          </li>
          <li>
            <strong>Threat Intelligence:</strong> VocalGuard integrates with global threat databases to identify known malicious numbers and caller IDs.
          </li>
        </ul>

        <h2 class="text-xl font-bold text-slate-900 mt-8 mb-4">Our Technology</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
          <div class="bg-slate-50 p-6 rounded-xl border border-slate-100">
            <h3 class="font-bold text-slate-900 mb-2">Natural Language Processing</h3>
            <p class="text-sm">Deep learning models trained on thousands of scam transcripts to understand context and intent.</p>
          </div>
          <div class="bg-slate-50 p-6 rounded-xl border border-slate-100">
            <h3 class="font-bold text-slate-900 mb-2">Local Processing</h3>
            <p class="text-sm">Privacy-first architecture ensures that your conversation data is analyzed locally whenever possible.</p>
          </div>
        </div>
      </div>

      <div class="mt-12 flex justify-center">
        <button 
          @click="$emit('back')"
          class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
        >
          Back to Home
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LearnMore',
  emits: ['back']
}
</script>
