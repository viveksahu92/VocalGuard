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

      <!-- Signup Card -->
      <div class="bg-slate-900/50 backdrop-blur-xl rounded-2xl p-8 shadow-2xl border border-slate-800/50">
        <h2 class="text-2xl font-bold text-white mb-6">Create Account</h2>

        <!-- Error Message -->
        <div v-if="error" class="mb-4 p-4 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 text-sm">
          {{ error }}
        </div>

        <!-- Signup Form -->
        <form @submit.prevent="handleSignup">
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
          <div class="mb-4">
            <label class="block text-gray-300 text-sm font-semibold mb-2" for="password">
              Password
            </label>
            <input
              v-model="password"
              id="password"
              type="password"
              required
              placeholder="At least 8 characters"
              @input="checkPasswordStrength"
              class="w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 transition-all"
            />
            
            <!-- Password Strength Indicator -->
            <div v-if="password.length > 0" class="mt-2">
              <div class="flex gap-1 mb-1">
                <div
                  v-for="i in 4"
                  :key="i"
                  class="h-1 flex-1 rounded-full transition-all"
                  :class="i <= passwordStrength ? strengthColors[passwordStrength] : 'bg-slate-700'"
                ></div>
              </div>
              <p class="text-xs" :class="strengthTextColors[passwordStrength]">
                {{ strengthLabels[passwordStrength] }}
              </p>
            </div>
          </div>

          <!-- Confirm Password Input -->
          <div class="mb-6">
            <label class="block text-gray-300 text-sm font-semibold mb-2" for="confirmPassword">
              Confirm Password
            </label>
            <input
              v-model="confirmPassword"
              id="confirmPassword"
              type="password"
              required
              placeholder="Re-enter your password"
              class="w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 transition-all"
            />
            <p v-if="confirmPassword && password !== confirmPassword" class="text-red-400 text-xs mt-1">
              Passwords do not match
            </p>
          </div>

          <!-- Signup Button -->
          <button
            type="submit"
            :disabled="loading || password !== confirmPassword || password.length < 8"
            class="w-full py-3 px-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-purple-500/50 hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="!loading">Create Account</span>
            <span v-else class="flex items-center justify-center">
              <svg class="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Creating account...
            </span>
          </button>
        </form>

        <!-- Divider -->
        <div class="my-6 flex items-center">
          <div class="flex-1 border-t border-slate-700"></div>
          <span class="px-4 text-gray-500 text-sm">or</span>
          <div class="flex-1 border-t border-slate-700"></div>
        </div>

        <!-- Login Link -->
        <div class="text-center">
          <p class="text-gray-400 text-sm">
            Already have an account?
            <button
              @click="$emit('switch-to-login')"
              class="text-purple-400 hover:text-purple-300 font-semibold transition-colors"
            >
              Sign In
            </button>
          </p>
        </div>
      </div>

      <!-- Footer -->
      <div class="mt-6 text-center text-gray-500 text-sm">
        <p>🔒 Your data is encrypted and secure</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useAuth } from '../composables/useAuth'

export default {
  name: 'Signup',
  emits: ['switch-to-login', 'signup-success'],
  
  setup(props, { emit }) {
    const { signup } = useAuth()
    
    const email = ref('')
    const password = ref('')
    const confirmPassword = ref('')
    const error = ref('')
    const loading = ref(false)
    const passwordStrength = ref(0)
    
    const strengthColors = {
      0: 'bg-red-500',
      1: 'bg-red-500',
      2: 'bg-yellow-500',
      3: 'bg-green-500',
      4: 'bg-green-500'
    }
    
    const strengthTextColors = {
      0: 'text-red-400',
      1: 'text-red-400',
      2: 'text-yellow-400',
      3: 'text-green-400',
      4: 'text-green-400'
    }
    
    const strengthLabels = {
      0: 'Too weak',
      1: 'Weak',
      2: 'Fair',
      3: 'Strong',
      4: 'Very strong'
    }
    
    const checkPasswordStrength = () => {
      const pwd = password.value
      let strength = 0
      
      if (pwd.length >= 8) strength++
      if (pwd.length >= 12) strength++
      if (/[a-z]/.test(pwd) && /[A-Z]/.test(pwd)) strength++
      if (/\d/.test(pwd)) strength++
      if (/[^a-zA-Z0-9]/.test(pwd)) strength++
      
      passwordStrength.value = Math.min(strength, 4)
    }
    
    const handleSignup = async () => {
      error.value = ''
      
      if (password.value !== confirmPassword.value) {
        error.value = 'Passwords do not match'
        return
      }
      
      if (password.value.length < 8) {
        error.value = 'Password must be at least 8 characters long'
        return
      }
      
      loading.value = true
      
      try {
        const result = await signup(email.value, password.value)
        
        if (result.success) {
          emit('signup-success')
        } else {
          error.value = result.error || 'Signup failed. Please try again.'
        }
      } catch (err) {
        error.value = 'An unexpected error occurred'
      } finally {
        loading.value = false
      }
    }
    
    return {
      email,
      password,
      confirmPassword,
      error,
      loading,
      passwordStrength,
      strengthColors,
      strengthTextColors,
      strengthLabels,
      checkPasswordStrength,
      handleSignup
    }
  }
}
</script>
