import streamlit as st
import os
from groq import Groq
import json
from datetime import datetime
from style import load_css

def init_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm your AI Sleep Expert. How can I help you today?"}
        ]

def get_chatbot_response(client, message, analysis_context):
    system_prompt = f"""
    You are an AI Sleep Expert. Your role is to analyze sleep data and provide personalized advice.

    Here is the user's sleep analysis summary:
    - Average Sleep Duration: {analysis_context['avg_duration']:.1f} hours
    - Sleep Quality Score: {analysis_context['quality_score']:.1f}/10
    - Sleep Consistency Score: {analysis_context['consistency_score']:.1f}/10
    
    Use this data to answer the user's questions and provide specific, actionable recommendations.
    Be friendly, empathetic, and encouraging.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ]

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=8000
    )
    return completion.choices[0].message.content

load_css('style.css')

# Enhanced Header
st.markdown("""
<div style="text-align: center; margin-bottom: 3rem;">
    <div style="position: relative; display: inline-block;">
        <h1 style="margin-bottom: 0.5rem; position: relative; z-index: 2;">💬 AI Sleep Expert Chat</h1>
        <div style="position: absolute; top: -10px; left: -10px; right: -10px; bottom: -10px; 
                    background: linear-gradient(135deg, rgba(75, 156, 211, 0.1), rgba(96, 165, 250, 0.1)); 
                    border-radius: 20px; z-index: 1; animation: pulse 3s ease-in-out infinite;"></div>
    </div>
    <p style="font-size: 1.2rem; color: #E5E7EB; margin-bottom: 2rem; line-height: 1.6;">
        Get personalized sleep advice and insights from your AI assistant
    </p>
    <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-top: 1rem;">
        <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.2), rgba(96, 165, 250, 0.2)); 
                    border: 1px solid rgba(75, 156, 211, 0.4); border-radius: 12px; padding: 0.8rem 1.5rem;">
            <span style="color: #FFFFFF; font-weight: 600;">🤖 AI-Powered</span>
        </div>
        <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.2), rgba(96, 165, 250, 0.2)); 
                    border: 1px solid rgba(75, 156, 211, 0.4); border-radius: 12px; padding: 0.8rem 1.5rem;">
            <span style="color: #FFFFFF; font-weight: 600;">💡 Personalized</span>
        </div>
        <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.2), rgba(96, 165, 250, 0.2)); 
                    border: 1px solid rgba(75, 156, 211, 0.4); border-radius: 12px; padding: 0.8rem 1.5rem;">
            <span style="color: #FFFFFF; font-weight: 600;">🎯 Actionable</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

init_chat_history()

# Enhanced Welcome Section
st.markdown("""
<div class="chat-container">
    <div class="chat-welcome">
        <h2>🌟 Welcome to the Sleep Expert Chat!</h2>
        <p>I'm here to help you understand your sleep patterns and provide personalized recommendations for better sleep health. Ask me anything about sleep science, your specific patterns, or tips for improving your sleep quality.</p>
        <strong>💡 Try these conversation starters:</strong>
        <ul>
            <li>"How can I improve my sleep quality based on my data?"</li>
            <li>"Tell me about my deep sleep patterns and what they mean."</li>
            <li>"What are some tips for falling asleep faster?"</li>
            <li>"How does my screen time affect my sleep?"</li>
            <li>"What's the ideal sleep schedule for my age?"</li>
            <li>"Can you analyze my sleep consistency patterns?"</li>
            <li>"What lifestyle changes would improve my sleep?"</li>
        </ul>
        <div style="background: rgba(75, 156, 211, 0.1); border: 1px solid rgba(75, 156, 211, 0.3); 
                    border-radius: 12px; padding: 1rem; margin-top: 1.5rem;">
            <p style="color: #E5E7EB; font-size: 0.95rem; margin: 0; text-align: center;">
                💬 <strong>Pro Tip:</strong> The more specific your questions, the better I can help you optimize your sleep!
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(220, 38, 38, 0.1)); 
                border: 1px solid rgba(239, 68, 68, 0.4); 
                border-radius: 16px; 
                padding: 2rem; 
                margin-bottom: 2rem;
                backdrop-filter: blur(20px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                position: relative;
                overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; 
                    background: linear-gradient(90deg, #EF4444, #F87171, #FCA5A5);"></div>
        <div style="display: flex; align-items: center; gap: 16px;">
            <div style="background: linear-gradient(135deg, #EF4444, #F87171); 
                        border-radius: 50%; width: 60px; height: 60px; 
                        display: flex; align-items: center; justify-content: center;
                        box-shadow: 0 4px 16px rgba(239, 68, 68, 0.3);">
                <span style="font-size: 1.8rem;">⚠️</span>
            </div>
            <div style="flex: 1;">
                <strong style="color: #EF4444; font-size: 1.2rem; display: block; margin-bottom: 0.5rem;">
                    🔑 API Key Required
                </strong>
                <p style="margin: 0; color: #E5E7EB; line-height: 1.6; font-size: 1rem;">
                    Please set the GROQ_API_KEY environment variable to use the AI chat feature. 
                    This enables personalized sleep advice and insights.
                </p>
                <div style="margin-top: 1rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <span style="background: rgba(239, 68, 68, 0.2); border-radius: 8px; padding: 0.3rem 0.8rem; 
                               font-size: 0.9rem; color: #E5E7EB;">🔧 Setup Required</span>
                    <span style="background: rgba(239, 68, 68, 0.2); border-radius: 8px; padding: 0.3rem 0.8rem; 
                               font-size: 0.9rem; color: #E5E7EB;">🤖 AI Features</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()
else:
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(220, 38, 38, 0.1)); 
                    border: 1px solid rgba(239, 68, 68, 0.4); 
                    border-radius: 16px; 
                    padding: 2rem; 
                    margin-bottom: 2rem;
                    backdrop-filter: blur(20px);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                    position: relative;
                    overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; 
                        background: linear-gradient(90deg, #EF4444, #F87171, #FCA5A5);"></div>
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="background: linear-gradient(135deg, #EF4444, #F87171); 
                            border-radius: 50%; width: 60px; height: 60px; 
                            display: flex; align-items: center; justify-content: center;
                            box-shadow: 0 4px 16px rgba(239, 68, 68, 0.3);">
                    <span style="font-size: 1.8rem;">❌</span>
                </div>
                <div style="flex: 1;">
                    <strong style="color: #EF4444; font-size: 1.2rem; display: block; margin-bottom: 0.5rem;">
                        🔌 Connection Error
                    </strong>
                    <p style="margin: 0; color: #E5E7EB; line-height: 1.6; font-size: 1rem;">
                        Failed to initialize Groq client: {str(e)}
                    </p>
                    <p style="margin: 0.5rem 0 0 0; color: #E5E7EB; line-height: 1.6; font-size: 1rem;">
                        Please check your GROQ_API_KEY and try again.
                    </p>
                    <div style="margin-top: 1rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                        <span style="background: rgba(239, 68, 68, 0.2); border-radius: 8px; padding: 0.3rem 0.8rem; 
                                   font-size: 0.9rem; color: #E5E7EB;">🔧 Check API Key</span>
                        <span style="background: rgba(239, 68, 68, 0.2); border-radius: 8px; padding: 0.3rem 0.8rem; 
                                   font-size: 0.9rem; color: #E5E7EB;">🔄 Retry Connection</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Enhanced Chat Input
    st.markdown("""
    <div style="margin: 3rem 0;">
        <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.15), rgba(96, 165, 250, 0.1)); 
                    border: 1px solid rgba(75, 156, 211, 0.4); 
                    border-radius: 16px; 
                    padding: 1.5rem; 
                    margin-bottom: 1rem;
                    backdrop-filter: blur(20px);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                    text-align: center;
                    position: relative;
                    overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; 
                        background: linear-gradient(90deg, #4B9CD3, #60A5FA, #93C5FD);"></div>
            <p style="color: #E5E7EB; font-size: 1.1rem; margin-bottom: 0.5rem; font-weight: 600;">
                💭 Ask me anything about your sleep...
            </p>
            <p style="color: #E5E7EB; font-size: 0.95rem; margin-bottom: 0; opacity: 0.8;">
                I'm here to help you optimize your sleep patterns and improve your overall well-being
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if prompt := st.chat_input("Type your question here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("🤔 Analyzing your sleep data and thinking..."):
            with st.chat_message("assistant"):
                analysis_context = st.session_state.get('analysis_results', {})
                df = st.session_state.get('df')
                
                if df is not None:
                    analysis_context['df_summary'] = df.describe().to_string()
                
                response = get_chatbot_response(client, prompt, analysis_context)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})