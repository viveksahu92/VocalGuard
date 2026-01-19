<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 p-4">
    <div class="w-full max-w-md">
      <!-- Logo and Header -->
      <div class="text-center mb-8">
        <h1 class="text-5xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent mb-2">
          🛡️ VocalGuard
        </h1>
        <p class="text-gray-400">Advanced Scam Detection System</p>
      </div>

      <!-- Login Card -->
      <div class="bg-slate-900/50 backdrop-blur-xl rounded-2xl p-8 shadow-2xl border border-slate-800/50">
        <h2 class="text-2xl font-bold text-white mb-6">Welcome Back</h2>

        <!-- Error Message -->
        <div v-if="error" class="mb-4 p-4 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 text-sm">
          {{ error }}
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin">
          <!-- Email Input -->
          <div class="mb-4">
            <label class="block text-gray-300 text-sm font-semibold mb-2" for="email">
              Email Address
            </label>
            <input
              v-model="email"
              id="email"
              type="email"
              required
              placeholder="your@email.com"
              class="w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 transition-all"
            />
          </div>

          <!-- Password Input -->
          <div class="mb-6">
            <label class="block text-gray-300 text-sm font-semibold mb-2" for="password">
              Password
            </label>
            <input
              v-model="password"
              id="password"
              type="password"
              required
              placeholder="••••••••"
              class="w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 transition-all"
            />
          </div>

          <!-- Login Button -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3 px-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-purple-500/50 hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="!loading">Sign In</span>
            <span v-else class="flex items-center justify-center">
              <svg class="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Signing in...
            </span>
          </button>
        </form>

        <!-- Google Sign-In Button -->
        <div class="mt-4 mb-6">
          <div 
            id="g_id_onload"
            data-client_id="YOUR_GOOGLE_CLIENT_ID_HERE"
            data-context="signin"
            data-ux_mode="popup"
            data-callback="handleGoogleCallback"
            data-auto_prompt="false">
          </div>
          
          <div 
            class="g_id_signin"
            data-type="standard"
            data-shape="rectangular"
            data-theme="filled_blue"
            data-text="signin_with"
            data-size="large"
            data-logo_alignment="left"
            data-width="100%">
          </div>
        </div>

        <!-- Divider -->
        <div class="my-6 flex items-center">
          <div class="flex-1 border-t border-slate-700"></div>
          <span class="px-4 text-gray-500 text-sm">or sign in with email</span>
          <div class="flex-1 border-t border-slate-700"></div>
        </div>

        <!-- Sign Up Link -->
        <div class="text-center">
          <p class="text-gray-400 text-sm">
            Don't have an account?
            <button
              @click="$emit('switch-to-signup')"
              class="text-purple-400 hover:text-purple-300 font-semibold transition-colors"
            >
              Sign Up
            </button>
          </p>
        </div>
      </div>

      <!-- Footer -->
      <div class="mt-6 text-center text-gray-500 text-sm">
        <p>🔒 Secure authentication with encrypted passwords</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAuth } from '../composables/useAuth'

export default {
  name: 'Login',
  emits: ['switch-to-signup', 'login-success'],
  
  setup(props, { emit }) {
    const { login, googleLogin } = useAuth()
    
    const email = ref('')
    const password = ref('')
    const error = ref('')
    const loading = ref(false)
    
    const handleLogin = async () => {
      error.value = ''
      loading.value = true
      
      try {
        const result = await login(email.value, password.value)
        
        if (result.success) {
          emit('login-success')
        } else {
          error.value = result.error || 'Login failed. Please try again.'
        }
      } catch (err) {
        error.value = 'An unexpected error occurred'
      } finally {
        loading.value = false
      }
    }
    
    const handleGoogleResponse = async (response) => {
      error.value = ''
      loading.value = true
      
      try {
        const result = await googleLogin(response.credential)
        
        if (result.success) {
          emit('login-success')
        } else {
          error.value = result.error || 'Google sign-in failed'
        }
      } catch (err) {
        error.value = 'Google sign-in error occurred'
      } finally {
        loading.value = false
      }
    }
    
    onMounted(() => {
      // Register Google callback globally
      window.handleGoogleCallback = handleGoogleResponse
    })
    
    return {
      email,
      password,
      error,
      loading,
      handleLogin
    }
  }
}
</script>
