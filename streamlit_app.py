# streamlit_app.py - Updated for Agentic Email Agent with TinyLlama
import streamlit as st
import json
from email_agent import AgenticEmailAgent

def initialize_agent():
    """Initialize the agentic email agent"""
    try:
        agent = AgenticEmailAgent()
        return agent, None
    except Exception as e:
        error_msg = str(e)
        if "No AI model available" in error_msg:
            return None, "❌ No AI model found. Please run: ollama pull tinyllama"
        else:
            return None, f"❌ Error initializing agent: {error_msg}"

def main():
    st.set_page_config(
        page_title="🤖 Agentic Email Generator",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Agentic Email Generator")
    st.markdown("**AI-powered autonomous email creation - 100% on-device using TinyLlama**")
    
    # Initialize agent
    if 'agent' not in st.session_state or 'agent_error' not in st.session_state:
        with st.spinner("🤖 Initializing AI agent..."):
            agent, error = initialize_agent()
            st.session_state.agent = agent
            st.session_state.agent_error = error
    
    agent = st.session_state.agent
    error = st.session_state.agent_error
    
    # Show status
    if error:
        st.error(error)
        st.info("💡 Make sure you have run: `ollama pull tinyllama`")
        
        if st.button("🔄 Retry Connection"):
            del st.session_state.agent
            del st.session_state.agent_error
            st.rerun()
        
        return
    
    # Sidebar - Agentic Settings
    with st.sidebar:
        st.header("🤖 Agentic AI Settings")
        
        if agent and agent.model:
            st.success(f"✅ AI Model: {agent.model}")
            st.info("🧠 Truly agentic behavior - AI makes all decisions")
        
        st.markdown("### 🎯 Agentic Features:")
        st.markdown("• **Autonomous Analysis** - AI decides context")
        st.markdown("• **Strategic Thinking** - AI chooses approach") 
        st.markdown("• **Creative Writing** - AI crafts content")
        st.markdown("• **Smart Optimization** - AI improves results")
        
        # Generation modes
        st.header("⚙️ Generation Mode")
        mode = st.selectbox(
            "Choose mode:",
            ["🤖 Full Autonomy", "🎨 Creative Variations", "📈 Strategic Analysis"]
        )
        
        # Advanced settings
        with st.expander("🔬 Advanced AI Settings"):
            creativity = st.slider("AI Creativity", 0.1, 1.0, 0.4, 0.1)
            max_length = st.slider("Response Length", 200, 800, 400, 50)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Input")
        
        # Bullet points input
        bullet_points = st.text_area(
            "Enter your bullet points:",
            placeholder="• Meeting with John tomorrow at 2pm\n• Discuss Q4 budget planning\n• Need approval for new project\n• Bring financial reports and proposals",
            height=200,
            help="Enter the key points you want to communicate"
        )
        
        # Generate button
        if st.button("🚀 Generate Agentic Email", type="primary", use_container_width=True):
            if not agent:
                st.error("❌ AI agent not available")
            elif bullet_points.strip():
                with st.spinner("🤖 AI is autonomously analyzing and crafting your email..."):
                    generate_email(agent, bullet_points, mode, creativity, max_length)
            else:
                st.error("Please enter some bullet points first!")
        
        # Quick examples
        st.subheader("💡 Example Scenarios")
        
        examples = {
            "📅 Meeting Request": "• Meeting with Sarah next Friday\n• Discuss Q4 budget planning\n• Need her input on new proposals\n• Bring last quarter's financial reports",
            "📋 Urgent Request": "• Need immediate approval for software purchase\n• $5,000 budget required for team tools\n• Will significantly improve productivity\n• Decision needed by end of week",
            "📧 Follow-up": "• Following up on yesterday's strategy call\n• Discussed new marketing initiatives\n• Need decision on budget allocation\n• Timeline is critical for Q1 launch",
            "🤝 Thank You": "• Thank you for the excellent presentation\n• Learned valuable insights about process improvement\n• Would like to discuss implementation\n• Coffee meeting next week?"
        }
        
        for label, example in examples.items():
            if st.button(label, use_container_width=True):
                st.session_state.example_text = example
                st.rerun()
        
        # Show selected example
        if 'example_text' in st.session_state:
            st.text_area("Selected Example:", value=st.session_state.example_text, height=100, disabled=True)
            if st.button("📋 Use This Example"):
                st.session_state.bullet_input = st.session_state.example_text
                st.rerun()
    
    with col2:
        st.header("📧 AI-Generated Results")
        
        if 'email_result' not in st.session_state:
            st.info("👈 Enter bullet points and click 'Generate Agentic Email' to see AI autonomous decision-making in action!")
            
            # Show what makes it agentic
            st.markdown("### 🧠 What Makes This Agentic?")
            st.markdown("• **Autonomous Context Analysis** - AI decides purpose, tone, relationship")
            st.markdown("• **Strategic Decision Making** - AI chooses optimal communication approach") 
            st.markdown("• **Creative Problem Solving** - AI adapts structure and language")
            st.markdown("• **Intelligent Optimization** - AI suggests improvements")
        else:
            display_results(st.session_state.email_result)

def generate_email(agent, bullet_points, mode, creativity, max_length):
    """Generate email using agentic AI"""
    try:
        if mode == "🤖 Full Autonomy":
            # Full autonomous generation
            result = agent.generate_email_agentically(bullet_points)
            analysis = agent.analyze_context_agentically(bullet_points)
            suggestions = agent.improve_email_agentically(result.get('full_email', ''))
            
            st.session_state.email_result = {
                'type': 'single',
                'data': result,
                'analysis': analysis,
                'suggestions': suggestions
            }
            
        elif mode == "🎨 Creative Variations":
            # Multiple agentic approaches
            variations = agent.generate_tone_variations_agentically(bullet_points)
            
            st.session_state.email_result = {
                'type': 'variations',
                'data': variations
            }
            
        elif mode == "📈 Strategic Analysis":
            # Strategic analysis + email
            strategy = agent.autonomous_email_strategy(bullet_points)
            result = agent.generate_email_agentically(bullet_points)
            analysis = agent.analyze_context_agentically(bullet_points)
            
            st.session_state.email_result = {
                'type': 'strategic',
                'data': result,
                'analysis': analysis,
                'strategy': strategy
            }
        
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ AI generation failed: {str(e)}")
        st.info("💡 Make sure TinyLlama is running: `ollama list` should show tinyllama")

def display_results(result):
    """Display the AI-generated results"""
    
    if result['type'] == 'single':
        # Single email with AI analysis
        email_data = result['data']
        analysis = result.get('analysis', {})
        suggestions = result.get('suggestions', [])
        
        # Show AI's autonomous decisions
        with st.expander("🧠 AI's Autonomous Analysis & Decisions", expanded=True):
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("AI-Detected Purpose", analysis.get('purpose', 'N/A'))
                st.metric("AI-Chosen Tone", analysis.get('tone', 'N/A'))
            with col_b:
                st.metric("AI-Assessed Relationship", analysis.get('relationship', 'N/A'))
                st.metric("AI-Judged Urgency", analysis.get('urgency', 'N/A'))
            
            if 'reasoning' in analysis:
                st.markdown("**🤖 AI's Reasoning:**")
                st.write(analysis['reasoning'])
        
        # Subject line
        subject = email_data.get('subject', 'No Subject')
        st.text_input("🎯 AI-Optimized Subject:", value=subject, disabled=True)
        
        # Email content
        email_body = email_data.get('full_email', 'Error generating email')
        st.text_area(
            "📧 AI-Generated Email (Select All & Copy):",
            value=email_body,
            height=400,
            help="Select all text (Ctrl+A) and copy (Ctrl+C)"
        )
        
        # Copy options
        col_copy1, col_copy2 = st.columns(2)
        with col_copy1:
            with st.expander("📋 Copy-Friendly Format"):
                st.code(email_body, language=None)
        
        with col_copy2:
            st.download_button(
                "📥 Download Email",
                data=email_body,
                file_name=f"agentic_email_{subject.replace(' ', '_').lower()}.txt",
                mime="text/plain"
            )
        
        # AI suggestions
        if suggestions:
            with st.expander("💡 AI's Improvement Suggestions"):
                st.markdown("**🤖 Autonomous optimization recommendations:**")
                for i, suggestion in enumerate(suggestions, 1):
                    st.write(f"{i}. {suggestion}")
    
    elif result['type'] == 'variations':
        # Multiple agentic variations
        variations = result['data']
        
        st.markdown("### 🎨 AI's Creative Variations")
        
        tabs = st.tabs([f"🎯 {var.get('approach', var.get('tone_used', 'Version')).title()}" for var in variations])
        
        for tab, variation in zip(tabs, variations):
            with tab:
                st.text_input(
                    "Subject:",
                    value=variation.get('subject', 'No Subject'),
                    disabled=True,
                    key=f"subj_{variation.get('tone_used', 'var')}"
                )
                
                email_content = variation.get('full_email', 'Error')
                st.text_area(
                    f"AI's {variation.get('approach', 'Creative')} Approach:",
                    value=email_content,
                    height=300,
                    key=f"body_{variation.get('tone_used', 'var')}"
                )
                
                st.download_button(
                    f"📥 Download {variation.get('approach', 'This')} Version",
                    data=email_content,
                    file_name=f"agentic_{variation.get('tone_used', 'version')}.txt",
                    mime="text/plain",
                    key=f"dl_{variation.get('tone_used', 'var')}"
                )
    
    elif result['type'] == 'strategic':
        # Strategic analysis + email
        email_data = result['data']
        analysis = result.get('analysis', {})
        strategy = result.get('strategy', {})
        
        # Strategic analysis
        st.subheader("📈 AI's Strategic Communication Analysis")
        st.markdown(strategy.get('strategy_analysis', 'No strategic analysis available'))
        
        # Generated email
        st.subheader("📧 Strategically Optimized Email")
        
        subject = email_data.get('subject', 'No Subject')
        st.text_input("Subject:", value=subject, disabled=True)
        
        email_body = email_data.get('full_email', 'Error')
        st.text_area(
            "Strategic Email:",
            value=email_body,
            height=300
        )
        
        st.download_button(
            "📥 Download Strategic Email",
            data=email_body,
            file_name=f"strategic_email_{subject.replace(' ', '_').lower()}.txt",
            mime="text/plain"
        )
    
    # Action buttons
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔄 Generate New", use_container_width=True):
            if 'email_result' in st.session_state:
                del st.session_state.email_result
            st.rerun()
    
    with col_btn2:
        if st.button("🎨 Try Different Mode", use_container_width=True):
            st.info("💡 Change the generation mode in the sidebar and generate again")

if __name__ == "__main__":
    main()