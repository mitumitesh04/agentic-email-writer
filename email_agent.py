import ollama
import json
from datetime import datetime
from typing import Dict, List

class AgenticEmailAgent:
    def __init__(self):
        self.client = ollama.Client()
        self.model = self.find_working_model()
        
        if not self.model:
            raise Exception("❌ qwen2.5:0.5b model not found. Please install it with: ollama pull qwen2.5:0.5b")
    
    def find_working_model(self):
        """Find qwen2.5:0.5b model specifically"""
        try:
            models_response = self.client.list()
            models = models_response.get('models', [])
            
            print(f"🔍 Looking for qwen2.5:0.5b model...")
            
            # Look specifically for qwen2.5:0.5b
            for model in models:
                # Extract just the name string, not the full object
                if isinstance(model, dict):
                    model_name = model.get('name', '')
                else:
                    # Handle case where model might be an object with name attribute
                    model_name = str(model).split("'")[1] if "name=" in str(model) else str(model)
                
                print(f"   - Found model: {model_name}")
                
                if 'qwen2.5:0.5b' in model_name:
                    # Return just the clean model name
                    clean_name = "qwen2.5:0.5b"
                    print(f"✅ Using qwen2.5:0.5b model")
                    return clean_name
            
            # If qwen2.5:0.5b not found, fail
            print("❌ qwen2.5:0.5b model not found")
            print("💡 Please install it with: ollama pull qwen2.5:0.5b")
            return None
                
        except Exception as e:
            print(f"❌ Error finding qwen2.5:0.5b model: {e}")
            return None
    
    def analyze_context_agentically(self, bullet_points: str) -> Dict:
        """AGENTIC: Let AI autonomously analyze and decide context"""
        
        # Enhanced prompt for better models
        prompt = f"""Analyze this email request and determine the appropriate context:

Email Request:
{bullet_points}

Please analyze and determine:
- Purpose: (meeting_request, follow_up, request, complaint, etc.)
- Tone: (formal, casual, urgent, persuasive, etc.) 
- Urgency: (low, medium, high, critical)
- Relationship: (boss, colleague, client, vendor)

Respond in this format:
Purpose: [your analysis]
Tone: [your decision]
Urgency: [your assessment]
Relationship: [your judgment]"""
        
        response = self.client.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": 0.2, "num_predict": 150}
        )
        
        # Parse the response
        result_text = response['response'].strip()
        lines = result_text.split('\n')
        result = {}
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                result[key.strip().lower()] = value.strip()
        
        return {
            "purpose": result.get('purpose', 'request'),
            "tone": result.get('tone', 'professional'),
            "relationship": result.get('relationship', 'colleague'),
            "urgency": result.get('urgency', 'medium'),
            "formality": "medium",
            "reasoning": f"AI analyzed: {result.get('purpose', 'request')} with {result.get('urgency', 'medium')} urgency"
        }
    
    def simple_analysis_prompt(self, bullet_points: str) -> Dict:
        """Backup agentic analysis if JSON fails"""
        prompt = f"""
        Analyze: {bullet_points}
        
        Purpose: [your decision]
        Tone: [your choice]  
        Relationship: [your assessment]
        Urgency: [your judgment]
        """
        
        response = self.client.generate(model=self.model, prompt=prompt)
        
        # Parse simple format
        lines = response['response'].split('\n')
        result = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                result[key.strip().lower()] = value.strip()
        
        return {
            "purpose": result.get('purpose', 'communication'),
            "tone": result.get('tone', 'professional'),
            "relationship": result.get('relationship', 'colleague'),
            "urgency": result.get('urgency', 'medium'),
            "formality": "medium"
        }
    
    def generate_email_agentically(self, bullet_points: str, context: Dict = None) -> Dict:
        """AGENTIC: Let AI autonomously craft the entire email strategy and content"""
        
        if not context:
            context = self.analyze_context_agentically(bullet_points)
        
        # Enhanced prompt for better models like qwen2.5
        prompt = f"""Write a professional business email based on these requirements:

Key Points:
{bullet_points}

Context: {context.get('tone', 'professional')} tone, {context.get('urgency', 'medium')} urgency

Please write a complete email with:
1. An effective subject line
2. Proper greeting
3. Clear, professional body
4. Appropriate closing

Format:
Subject: [your subject line]

Dear [Name],

[Your email content here]

Best regards,
[Your name]"""
        
        response = self.client.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": 0.3, "num_predict": 300}
        )
        
        email_content = response['response'].strip()
        
        # Extract subject and body
        subject = "Professional Email"
        body = email_content
        
        # Look for subject line
        lines = email_content.split('\n')
        for i, line in enumerate(lines):
            if line.lower().startswith('subject:'):
                subject = line.replace('Subject:', '').replace('subject:', '').strip()
                body = '\n'.join(lines[i+1:]).strip()
                break
        
        # Clean up the email body
        if not body.startswith('Dear') and not body.startswith('Hi'):
            body = f"Dear [Name],\n\n{body}\n\nBest regards,\n[Your name]"
        
        full_email = f"Subject: {subject}\n\n{body}"
        
        return {
            "subject": subject,
            "full_email": full_email,
            "body": body,
            "ai_reasoning": context.get('reasoning', 'AI autonomous decision')
        }
    
    def generate_smart_subject(self, bullet_points: str, context: Dict) -> str:
        """AGENTIC: Let AI decide the optimal subject line"""
        
        prompt = f"""
        You are a subject line optimization agent. Create the most effective subject line for this email.
        
        BULLET POINTS: {bullet_points}
        CONTEXT: {context['purpose']}, {context['tone']}, {context['urgency']}
        
        Consider:
        - What will get opened first in a busy inbox?
        - What conveys the right urgency without being spammy?
        - What gives enough context without being too long?
        
        Return ONLY the subject line, no quotes or explanations.
        """
        
        response = self.client.generate(model=self.model, prompt=prompt)
        return response['response'].strip().strip('"\'')
    
    def improve_email_agentically(self, email_content: str) -> List[str]:
        """AGENTIC: AI analyzes and suggests intelligent improvements"""
        
        prompt = f"""
        You are an email optimization agent. Analyze this email and suggest intelligent improvements.
        
        EMAIL: {email_content}
        
        As an intelligent agent, assess:
        1. Clarity and effectiveness
        2. Tone appropriateness  
        3. Structure and flow
        4. Professional impact
        5. Likelihood of achieving goals
        
        Provide 3-5 specific, actionable suggestions that demonstrate intelligent analysis.
        Return as a simple list, one suggestion per line.
        """
        
        response = self.client.generate(model=self.model, prompt=prompt)
        
        suggestions = [
            line.strip().lstrip('•-*123456789.').strip() 
            for line in response['response'].split('\n') 
            if line.strip()
        ]
        
        return suggestions[:5]
    
    def generate_tone_variations_agentically(self, bullet_points: str) -> List[Dict]:
        """AGENTIC: AI autonomously creates variations with different strategic approaches"""
        
        variations = []
        approaches = [
            ("FORMAL", "professional and corporate"),
            ("FRIENDLY", "warm and collaborative"), 
            ("URGENT", "direct and action-oriented")
        ]
        
        for approach_name, approach_desc in approaches:
            prompt = f"""Write a {approach_desc} email from these points:

{bullet_points}

Make it {approach_desc} style.

Subject: [write subject]

Dear [Name],

[Write email body]

Best regards,
[Your name]

Write the email:"""
            
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={"temperature": 0.4, "num_predict": 200}
            )
            
            email_content = response['response'].strip()
            
            # Extract subject
            subject = f"{approach_name.title()} Email"
            body = email_content
            
            lines = email_content.split('\n')
            for i, line in enumerate(lines):
                if line.lower().startswith('subject:'):
                    subject = line.replace('Subject:', '').replace('subject:', '').strip()
                    body = '\n'.join(lines[i+1:]).strip()
                    break
            
            full_email = f"Subject: {subject}\n\n{body}"
            
            variations.append({
                "subject": subject,
                "full_email": full_email,
                "body": body,
                "tone_used": approach_name.lower(),
                "approach": approach_name
            })
        
        return variations
    
    def fallback_variations(self, bullet_points: str) -> List[Dict]:
        """Create variations if parsing fails"""
        tones = ["formal", "persuasive", "collaborative"]
        variations = []
        
        for tone in tones:
            context = {"tone": tone, "purpose": "communication", "relationship": "colleague"}
            email = self.generate_email_agentically(bullet_points, context)
            email['tone_used'] = tone
            variations.append(email)
        
        return variations
    
    def autonomous_email_strategy(self, bullet_points: str) -> Dict:
        """AGENTIC: AI creates complete communication strategy"""
        
        prompt = f"""
        You are a strategic communication agent. Develop a complete email strategy for these bullet points:
        
        BULLET POINTS: {bullet_points}
        
        AUTONOMOUS STRATEGIC ANALYSIS:
        1. What is the sender trying to achieve?
        2. What obstacles might prevent success?
        3. What approach will be most effective?
        4. What follow-up actions should be planned?
        5. How can this email strengthen the relationship?
        
        Provide your strategic assessment and recommendations.
        """
        
        response = self.client.generate(model=self.model, prompt=prompt)
        
        return {
            "strategy_analysis": response['response'],
            "timestamp": datetime.now().isoformat()
        }

# Test the agentic behavior
def test_agentic_agent():
    try:
        agent = AgenticEmailAgent()
        
        test_bullets = "meeting with sarah tomorrow, need budget approval, project deadline next week"
        
        print("🤖 Testing Agentic Analysis...")
        context = agent.analyze_context_agentically(test_bullets)
        print(f"AI Decision: {context}")
        
        print("\n🤖 Testing Agentic Email Generation...")
        email = agent.generate_email_agentically(test_bullets)
        print(f"Subject: {email['subject']}")
        print(f"Preview: {email['full_email'][:200]}...")
        
        return True
    except Exception as e:
        print(f"❌ Agentic agent test failed: {e}")
        return False

if __name__ == "__main__":
    test_agentic_agent()