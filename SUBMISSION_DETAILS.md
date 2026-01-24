# VocalGuard - Project Submission

## Inspiration
In an era where AI voice scams (vishing) are becoming increasingly sophisticated, vulnerable individuals—especially the elderly—are losing billions of dollars annually to financial fraud. We were inspired to build **VocalGuard** effectively "fight AI with AI," creating a protective shield that monitors calls in real-time to detect malicious intent, ultimately protecting people's voices and securing their hard-earned money.

## What it does
VocalGuard is an intelligent call protection system that acts as a real-time guardian during phone conversations.
*   **Real-time Call Analysis**: Instantly transcribes and analyzes conversation patterns to identify potential threats.
*   **Dynamic Risk Scoring**: Assigns a live risk score (0-100%) to every call using advanced algorithms that detect specific scam archetypes like romance scams, IRS impersonation, and tech support fraud.
*   **Proactive Warnings**: Automatically generates audio warnings to alert the user if a scam is detected (e.g., "High Risk Scam Detected: Pressure Tactics").
*   **Auto-Disconnect**: Can automatically terminate calls that exceed a critical risk threshold to prevent immediate financial harm.
*   **Caller Intelligence**: Checks numbers against a community-sourced reputation database and detects potential spoofing attempts.

## How we built it
We built VocalGuard using a modern, scalable tech stack designed for speed and reliability:
*   **Frontend**: Built with **Vue.js 3** and **Tailwind CSS** to create a premium, responsive, and accessible user interface.
*   **Backend**: A robust **Python Flask** API that handles real-time data processing.
*   **AI & ML Integration**:
    *   **OpenAI GPT-4o-mini**: For deep semantic analysis of call transcripts to understand context and intent.
    *   **ElevenLabs API**: To generate realistic, real-time audio warnings.
    *   Custom algorithms for **keyword spotting**, **PII redaction**, and **spoofing detection**.
*   **Database**: Custom SQLite implementation for secure storage of call logs and threat intelligence.
*   **Deployment**: Hosted on **Railway** for reliable cloud performance.

## Challenges we ran into
*   **Real-time Latency**: Achieving near-zero latency for analysis was critical. Balancing deep analysis (via LLMs) with the need for instant feedback required optimizing our API calls and implemented efficient caching strategies.
*   **False Positives**: distinguishing between a legitimate urgent call (e.g., from a family member) and a "grandparent scam" was difficult. We had to fine-tune our scoring weights and add a "Caller Reputation" layer to improve accuracy.
*   **Handling Sensitive Data**: Ensuring that personal information (like credit card numbers mentioned in a call) was redacted locally before any storage or display was a top priority for privacy.

## Accomplishments that we're proud of
*   **Integrated Multi-Modal AI**: Successfully combining transcription, semantic analysis, and text-to-speech generation into a single seamless flow.
*   **User-Centric Design**: Creating a "Stats Dashboard" and "Call Screen" that are intuitive enough for non-technical users while providing powerful insights.
*   **The "0ms" Goal**: Optimizing our pipeline to process threats as they happen, rather than after the call has ended.

## What we learned
*   **The sophistication of modern scams**: Researching the various scripts used by scammers (romance, utility, investment) revealed just how structured and psychological these attacks are.
*   **Privacy is paramount**: We learned that users want protection but not at the cost of their privacy, leading us to implement strict PII redaction.
*   **Frontend-Backend Synergy**: The importance of keeping the frontend state perfectly synced with backend risk assessments to provide immediate visual cues.

## What's next for VocalGuard
*   **Mobile App Integration**: Porting the core logic to a native mobile app (iOS/Android) to intercept actual carrier calls.
*   **Voice Biometrics**: Implementing "Voice Printing" to recognize known scammers or trusted contacts instantly by their voice alone.
*   **Carrier Integration**: Partnering with telecom providers to apply VocalGuard's threat intelligence at the network level.

## Built With
*   vue.js
*   tailwind-css
*   python
*   flask
*   openai
*   elevenlabs
*   sqlite
*   railway
