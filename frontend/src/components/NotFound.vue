<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-50 p-4">
    <div class="text-center max-w-md">
      <div class="mb-8 relative">
        <div class="text-9xl font-black text-slate-200">404</div>
        <div class="absolute inset-0 flex items-center justify-center">
          <span class="text-6xl">🤔</span>
        </div>
      </div>
      
      <h1 class="text-3xl font-bold text-slate-900 mb-4">Page Not Found</h1>
      <p class="text-slate-600 mb-8">
        Oops! The page you're looking for doesn't exist or has been moved.
      </p>
      
      <button 
        @click="$emit('gohome')"
        class="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-blue-500/30 transition-all transform hover:-translate-y-1"
      >
        Go Home
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound',
  emits: ['gohome']
}
</script>
