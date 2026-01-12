# VocalGuard UI/UX Documentation

## CallScreen.vue - iPhone-style Call Interface

### Visual Layout

```
┌────────────────────────────────────────┐
│  ●●● VocalGuard ●●●                    │  Status Bar (Black)
│  9:41                    ▮▮▮          │  Time + Signal
├────────────────────────────────────────┤
│                                        │
│         incoming call...               │  Call Status
│                                        │
│      Unknown Caller                    │  Caller Name (Large)
│      +1 (555) 123-4567                 │  Caller Number
│                                        │
│          00:00                         │  Call Duration
│                                        │
│  ┌────────────────────────────────┐   │
│  │  ⚠️ SCAM ALERT                 │   │  Alert Badge
│  │  HIGH RISK SCAM DETECTED!      │   │  (Red/Yellow/Orange)
│  │  Confidence: 95%                │   │
│  └────────────────────────────────┘   │
│                                        │
│  ┌────────────────────────────────┐   │
│  │ Transcript     👁️‍🗨️ Blur Numbers│   │  Transcript Box
│  │ Hello, this is from the IRS... │   │  (Scrollable)
│  │ ...gift cards...arrested...    │   │
│  └────────────────────────────────┘   │
│                                        │
│  [URGENCY] [PAYMENT] [THREATS]        │  Threat Tags
│                                        │
│    ○       ○       ○                  │  Control Buttons
│   mute   keypad  speaker               │  (Inactive/Gray)
│                                        │
│            ●                          │  End Call Button
│         (Red Phone)                   │  (Red, Rotating)
│                                        │
│     Analyze Call for Scams            │  Action Button
│                                        │
└────────────────────────────────────────┘
```

### Color Scheme

#### Background
- Main: `gradient-to-b from-gray-900 to-black`
- Device: `bg-gray-800` with `border-gray-900`
- Status Bar: `bg-black`

#### Threat Level Colors
- **HIGH**: `bg-red-500/20 border-red-500`
- **MEDIUM**: `bg-yellow-500/20 border-yellow-500`
- **LOW**: `bg-orange-500/20 border-orange-500`

#### Text Colors
- Primary: `text-white`
- Secondary: `text-gray-400`
- Muted: `text-gray-300`

#### Interactive Elements
- End Call: `bg-red-500 hover:bg-red-600`
- Analyze Button: `bg-blue-600 hover:bg-blue-700`
- Control Buttons: `bg-gray-700` (inactive)

### Components Breakdown

#### 1. Status Bar
```vue
<div class="bg-black px-8 py-2 flex justify-between">
  <span>{{ currentTime }}</span>
  <div class="signal-bars">...</div>
</div>
```
- Shows current time (updated every minute)
- Signal indicator (static UI)
- Full-width black background

#### 2. Call Information Section
```vue
<div class="px-8 py-12 text-center">
  <p class="text-gray-400 text-sm">{{ callStatus }}</p>
  <h2 class="text-white text-3xl">{{ callerName }}</h2>
  <p class="text-gray-400 text-lg">{{ callerNumber }}</p>
  <p class="text-white text-4xl">{{ callDuration }}</p>
</div>
```
- Call status (incoming/active/ended)
- Caller name (large, centered)
- Caller phone number
- Live call duration timer

#### 3. Scam Alert Badge
```vue
<div v-if="analysisResult?.is_scam"
     :class="[threat-level-colors]">
  <p class="text-white font-bold">⚠️ SCAM ALERT</p>
  <p class="text-white text-sm">{{ warning_message }}</p>
  <p class="text-xs">Confidence: {{ confidence }}%</p>
</div>
```
- Only shows if scam detected
- Color-coded by threat level
- Displays warning message
- Shows confidence percentage

#### 4. Transcript Display
```vue
<div class="bg-gray-700/50 rounded-2xl p-4 max-h-40 overflow-y-auto">
  <div class="flex justify-between">
    <h3>Transcript</h3>
    <button @click="togglePrivacy">
      {{ privacyMode ? '👁️ Show' : '👁️‍🗨️ Blur' }} Numbers
    </button>
  </div>
  <p>{{ displayTranscript }}</p>
</div>
```
- Scrollable transcript box
- Privacy toggle button
- Numbers blurred when privacy mode active
- Semi-transparent background

#### 5. Threat Tags
```vue
<div v-if="detected_threats.length > 0">
  <span v-for="threat in detected_threats"
        class="bg-red-900/40 text-red-300 px-3 py-1 rounded-full">
    {{ formatThreat(threat) }}
  </span>
</div>
```
- Shows detected threat categories
- Pill-shaped badges
- Red theme for warnings
- Only visible when threats detected

#### 6. Call Controls
```vue
<div class="grid grid-cols-3 gap-6">
  <button class="opacity-50">
    <div class="w-16 h-16 bg-gray-700 rounded-full">
      <svg>...</svg>
    </div>
    <span>mute</span>
  </button>
  <!-- keypad, speaker -->
</div>
```
- Three control buttons (mute, keypad, speaker)
- Circular buttons with icons
- Currently inactive (50% opacity)
- Grid layout for alignment

#### 7. End Call Button
```vue
<button @click="endCall"
        class="w-20 h-20 bg-red-500 rounded-full">
  <svg class="transform rotate-135">
    <!-- Phone icon -->
  </svg>
</button>
```
- Large red circular button
- Phone icon rotated 135°
- Center-aligned
- Hover effect

#### 8. Analyze Button
```vue
<button v-if="!isAnalyzing && !analysisResult"
        @click="analyzeCall"
        class="w-full bg-blue-600 py-3 rounded-full">
  Analyze Call for Scams
</button>
```
- Full-width button
- Only shows before analysis
- Triggers API call
- Loading state during analysis

### Responsive Design

#### Desktop (Default)
- Max width: 28rem (448px)
- Centered on screen
- Full padding and spacing

#### Mobile
- Adapts to screen width
- Maintains iPhone aspect ratio
- Touch-friendly button sizes
- Scrollable transcript area

### Interactions

#### User Actions
1. **Analyze Call** - Sends transcript to backend API
2. **Toggle Privacy** - Blurs/shows numbers in transcript
3. **End Call** - Shows alert with analysis result

#### State Management
- `currentTime` - Updates every 60 seconds
- `callDuration` - Updates every second during call
- `privacyMode` - Boolean toggle
- `isAnalyzing` - Shows loading spinner
- `analysisResult` - Stores API response

### Animation & Transitions

#### Loading Spinner
```vue
<div class="animate-spin rounded-full h-8 w-8 
            border-b-2 border-white"></div>
```
- Appears during analysis
- Smooth rotation animation
- White border on transparent circle

#### Hover Effects
- End Call: `hover:bg-red-600`
- Analyze Button: `hover:bg-blue-700`
- Privacy Toggle: `hover:bg-gray-500`
- Smooth transitions on all interactions

### Accessibility

#### Visual
- High contrast text on dark background
- Large touch targets (min 44x44px)
- Clear iconography with labels
- Color-coded threat levels

#### Screen Readers
- Semantic HTML structure
- Icon labels for all buttons
- Status updates announced
- ARIA labels where needed

### Demo Flow

1. **Initial State**
   - Shows incoming call screen
   - Demo transcript loaded
   - Timer at 00:00

2. **Call Active**
   - Timer starts counting
   - Status shows "incoming call..."
   - Analyze button visible

3. **Analysis Triggered**
   - Loading spinner appears
   - Button disabled
   - API call in progress

4. **Results Displayed**
   - Scam alert badge appears (if scam)
   - Threat tags shown
   - Confidence displayed
   - Warning message visible

5. **Privacy Toggle**
   - Click to blur numbers
   - Instant visual update
   - Reversible action

6. **End Call**
   - Alert shown with summary
   - Session complete
   - Can start new analysis

### Technical Details

#### Vue 3 Composition API
```javascript
setup() {
  const currentTime = ref('9:41')
  const isAnalyzing = ref(false)
  const analysisResult = ref(null)
  
  const displayTranscript = computed(() => {
    return privacyMode.value 
      ? transcript.value.replace(/\d/g, '*')
      : transcript.value
  })
  
  return { currentTime, isAnalyzing, ... }
}
```

#### API Integration
```javascript
const analyzeCall = async () => {
  const response = await fetch('http://localhost:5000/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ transcript, generate_audio: false })
  })
  analysisResult.value = await response.json()
}
```

### Customization Options

#### Colors
- Change theme in Tailwind classes
- Adjust threat level colors
- Modify button colors

#### Layout
- Adjust max-width for larger screens
- Change grid spacing
- Modify transcript height

#### Content
- Update caller name/number
- Change demo transcript
- Customize warning messages

### Performance Considerations

- Efficient re-renders with Vue 3
- Minimal DOM updates
- Lazy loading of analysis results
- Debounced API calls (if needed)
- Small bundle size with Vite

### Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- ES6+ required
- CSS Grid support needed
- Fetch API required
- No IE11 support
