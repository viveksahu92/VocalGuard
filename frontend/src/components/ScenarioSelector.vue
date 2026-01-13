<template>
  <div class="bg-gray-800 rounded-2xl p-6 mb-6">
    <h3 class="text-white text-xl font-bold mb-2">🎭 Test Scenarios - 15 Scam Types</h3>
    <p class="text-gray-400 text-sm mb-4">Click any scenario to test advanced detection</p>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
      <button
        v-for="scenario in scenarios"
        :key="scenario.id"
        @click="selectScenario(scenario)"
        class="bg-gray-700 hover:bg-gray-600 text-white p-4 rounded-xl text-left transition transform hover:scale-105"
      >
        <div class="flex items-center gap-3">
          <span class="text-2xl">{{ scenario.icon }}</span>
          <div>
            <p class="font-semibold">{{ scenario.name }}</p>
            <p class="text-xs text-gray-400">{{ scenario.type }}</p>
          </div>
        </div>
      </button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'ScenarioSelector',
  emits: ['scenario-selected'],
  
  setup(props, { emit }) {
    const scenarios = ref([
      {
        id: 1,
        name: 'IRS Tax Scam',
        type: 'Government Impersonation',
        icon: '🏛️',
        transcript: 'Hello, this is from the IRS. You need to pay your outstanding taxes immediately using iTunes gift cards or you will be arrested within 24 hours. Please provide your credit card number 4532-1234-5678-9012 to avoid legal action.',
        caller: 'IRS Agent',
        number: '+1 (800) 555-0123'
      },
      {
        id: 2,
        name: 'Tech Support Scam',
        type: 'Tech Support Fraud',
        icon: '💻',
        transcript: 'Hello, this is Microsoft technical support. We detected a virus on your computer. Please give us remote access immediately and provide your credit card to fix the security breach. Your Windows license will expire today if you do not act now.',
        caller: 'Microsoft Support',
        number: '+1 (888) 555-4567'
      },
      {
        id: 3,
        name: 'Bank Fraud Alert',
        type: 'Financial Scam',
        icon: '🏦',
        transcript: 'This is your bank security department. We detected suspicious activity on your account. Please verify your social security number, account password, and credit card CVV immediately to prevent account closure. Wire $5000 to secure your account.',
        caller: 'Bank Security',
        number: '+1 (866) 555-7890'
      },
      {
        id: 4,
        name: 'Lottery Winner Scam',
        type: 'Prize/Lottery Fraud',
        icon: '🎰',
        transcript: 'Congratulations! You won $2.5 million in the international lottery! To claim your prize, please pay $500 processing fee via Western Union and provide your bank account details. This is a limited time offer, act now!',
        caller: 'Lottery Commission',
        number: '+1 (900) 555-2468'
      },
      {
        id: 5,
        name: 'Romance Scam',
        type: 'Romance/Dating Fraud',
        icon: '❤️',
        transcript: 'Hi darling, I am stuck in another country and need money urgently for my flight home. Please send $2000 via MoneyGram. I love you so much and cannot wait to meet you. Send the money to this address immediately.',
        caller: 'Sarah Johnson',
        number: '+44 7700 900123'
      },
      {
        id: 6,
        name: 'Social Security Scam',
        type: 'Government Impersonation',
        icon: '🆔',
        transcript: 'This is the Social Security Administration. Your SSN has been suspended due to suspicious activity. Press 1 now or your benefits will be terminated and you will face criminal prosecution. Provide your social security number to verify.',
        caller: 'SSA Officer',
        number: '+1 (800) 772-1213'
      },
      {
        id: 7,
        name: 'Amazon Refund Scam',
        type: 'Impersonation Fraud',
        icon: '📦',
        transcript: 'Hello, this is Amazon customer service. We need to refund $500 to your account. Please install AnyDesk on your computer so we can process the refund remotely. We need your bank account number to complete the transaction.',
        caller: 'Amazon Support',
        number: '+1 (888) 280-4331'
      },
      {
        id: 8,
        name: 'Cryptocurrency Investment',
        type: 'Investment Scam',
        icon: '₿',
        transcript: 'Exclusive investment opportunity! Double your Bitcoin in 30 days guaranteed. Minimum investment only $1000. Limited spots available. Act now or miss out on financial freedom. Transfer funds immediately to secure your position.',
        caller: 'Crypto Advisor',
        number: '+1 (555) 123-9999'
      },
      {
        id: 9,
        name: 'Grandparent Scam',
        type: 'Emergency Fraud',
        icon: '👴',
        transcript: 'Grandma, it\'s me! I\'m in trouble and need help right now. I was in an accident and I\'m in jail. Please don\'t tell mom and dad. I need $5000 bail money immediately via Western Union. Please hurry, I\'m scared.',
        caller: 'Unknown',
        number: '+1 (555) 000-1234'
      },
      {
        id: 10,
        name: 'Utility Shutoff Scam',
        type: 'Urgency Fraud',
        icon: '⚡',
        transcript: 'This is the electric company. Your power will be shut off in one hour due to non-payment. Pay $350 immediately with a prepaid card to avoid disconnection. Call this number back right now with your payment.',
        caller: 'Power Company',
        number: '+1 (866) 555-POWER'
      },
      {
        id: 11,
        name: 'Job Offer Scam',
        type: 'Employment Fraud',
        icon: '💼',
        transcript: 'Congratulations! You have been selected for a work-from-home position earning $5000 per week. To start immediately, pay $200 training fee via Zelle. This is a limited opportunity. Send payment now to secure your position.',
        caller: 'HR Department',
        number: '+1 (555) 999-JOBS'
      },
      {
        id: 12,
        name: 'Charity Scam',
        type: 'Donation Fraud',
        icon: '🎗️',
        transcript: 'We are calling on behalf of veterans charity. Your donation will help wounded soldiers. We need your credit card information right now to process your tax-deductible donation. Please act fast, these heroes need you immediately.',
        caller: 'Charity Foundation',
        number: '+1 (800) 555-GIVE'
      },
      {
        id: 13,
        name: 'Warrant/Arrest Scam',
        type: 'Law Enforcement Fraud',
        icon: '👮',
        transcript: 'This is Officer Johnson with the sheriff department. There is an active warrant for your arrest. You missed jury duty and now face criminal charges. Pay $2500 fine immediately via Bitcoin ATM or we will send officers to arrest you within the hour.',
        caller: 'Sheriff Officer',
        number: '+1 (911) 555-0000'
      },
      {
        id: 14,
        name: 'Medicare/Insurance Scam',
        type: 'Healthcare Fraud',
        icon: '🏥',
        transcript: 'This is Medicare calling about your health benefits. Your Medicare number has been compromised. We need to verify your information immediately including your social security number and bank account to issue you a new card.',
        caller: 'Medicare Rep',
        number: '+1 (800) MEDICARE'
      },
      {
        id: 15,
        name: 'Legitimate Call',
        type: 'Non-Scam',
        icon: '✅',
        transcript: 'Hello, this is Dr. Smith from Valley Medical Center calling to confirm your appointment scheduled for tomorrow at 2 PM. Please call us back at 555-0100 if you need to reschedule. Thank you and have a great day.',
        caller: 'Dr. Smith',
        number: '+1 (555) 555-0100'
      }
    ])
    
    const selectScenario = (scenario) => {
      emit('scenario-selected', scenario)
    }
    
    return {
      scenarios,
      selectScenario
    }
  }
}
</script>
