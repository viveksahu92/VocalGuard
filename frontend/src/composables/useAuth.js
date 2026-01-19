/**
 * VocalGuard Authentication Composable
 * Manages user authentication state and API calls
 */

import { ref, computed } from 'vue'

const AUTH_TOKEN_KEY = 'vocalguard_token'
const AUTH_USER_KEY = 'vocalguard_user'
const API_BASE_URL = 'http://localhost:5000'

// Global state
const token = ref(localStorage.getItem(AUTH_TOKEN_KEY) || null)
const user = ref(JSON.parse(localStorage.getItem(AUTH_USER_KEY) || 'null'))

export function useAuth() {
    const isAuthenticated = computed(() => !!token.value)

    const setAuthData = (authToken, userData) => {
        token.value = authToken
        user.value = userData
        localStorage.setItem(AUTH_TOKEN_KEY, authToken)
        localStorage.setItem(AUTH_USER_KEY, JSON.stringify(userData))
    }

    const clearAuthData = () => {
        token.value = null
        user.value = null
        localStorage.removeItem(AUTH_TOKEN_KEY)
        localStorage.removeItem(AUTH_USER_KEY)
    }

    const signup = async (email, password) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            })

            const data = await response.json()

            if (!response.ok) {
                throw new Error(data.error || 'Signup failed')
            }

            setAuthData(data.token, data.user)
            return { success: true, user: data.user }
        } catch (error) {
            console.error('Signup error:', error)
            return { success: false, error: error.message }
        }
    }

    const login = async (email, password) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            })

            const data = await response.json()

            if (!response.ok) {
                throw new Error(data.error || 'Login failed')
            }

            setAuthData(data.token, data.user)
            return { success: true, user: data.user }
        } catch (error) {
            console.error('Login error:', error)
            return { success: false, error: error.message }
        }
    }

    const logout = () => {
        clearAuthData()
    }

    const getToken = () => {
        return token.value
    }

    const getCurrentUser = async () => {
        if (!token.value) {
            return { success: false, error: 'Not authenticated' }
        }

        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${token.value}`
                }
            })

            const data = await response.json()

            if (!response.ok) {
                if (response.status === 401) {
                    // Token expired or invalid
                    clearAuthData()
                }
                throw new Error(data.error || 'Failed to fetch user')
            }

            user.value = data.user
            localStorage.setItem(AUTH_USER_KEY, JSON.stringify(data.user))
            return { success: true, user: data.user }
        } catch (error) {
            console.error('Get current user error:', error)
            return { success: false, error: error.message }
        }
    }

    const googleLogin = async (credential) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/google`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ credential })
            })

            const data = await response.json()

            if (!response.ok) {
                throw new Error(data.error || 'Google login failed')
            }

            setAuthData(data.token, data.user)
            return { success: true, user: data.user }
        } catch (error) {
            console.error('Google login error:', error)
            return { success: false, error: error.message }
        }
    }

    const checkAuth = async () => {
        if (token.value) {
            return await getCurrentUser()
        }
        return { success: false }
    }

    return {
        isAuthenticated,
        user,
        signup,
        login,
        googleLogin,
        logout,
        getToken,
        getCurrentUser,
        checkAuth
    }
}
