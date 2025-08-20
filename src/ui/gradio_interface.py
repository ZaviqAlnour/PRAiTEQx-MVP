"""
PRAiTEQx Gradio Web Interface
Beautiful and intuitive web UI for the Multi-Expert AI System
"""

import gradio as gr
import asyncio
import httpx
import json
from typing import Dict, Any
from loguru import logger
import time

class PRAiTEQxUI:
    """Main UI class for PRAiTEQx interface"""
    
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
        self.client = httpx.AsyncClient()
        logger.info("🎨 PRAiTEQx UI initialized")
    
    async def process_query_async(self, query: str, use_multi_expert: bool) -> Dict[str, Any]:
        """Process query through API"""
        try:
            response = await self.client.post(
                f"{self.api_base_url}/query",
                json={
                    "query": query,
                    "use_multi_expert": use_multi_expert
                },
                timeout=60.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "success": False,
                    "response": f"❌ Error: {response.status_code} - {response.text}",
                    "experts_used": [],
                    "processing_time": 0
                }
                
        except Exception as e:
            logger.error(f"❌ UI Error: {e}")
            return {
                "success": False,
                "response": f"❌ Connection Error: {str(e)}",
                "experts_used": [],
                "processing_time": 0
            }
    
    def process_query_sync(self, query: str, use_multi_expert: bool):
        """Synchronous wrapper for async query processing"""
        if not query.strip():
            return "⚠️ Please enter a query!", "", ""
        
        try:
            # Run async function in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.process_query_async(query, use_multi_expert)
            )
            loop.close()
            
            if result["success"]:
                experts_info = f"**Experts Used:** {', '.join(result['experts_used'])}\n"
                experts_info += f"**Processing Time:** {result.get('processing_time', 0):.2f}s\n"
                experts_info += f"**Response Type:** {result.get('response_type', 'unknown')}\n\n"
                
                return result["response"], experts_info, "✅ Success"
            else:
                return result["response"], "", "❌ Error"
                
        except Exception as e:
            error_msg = f"❌ Processing Error: {str(e)}"
            logger.error(error_msg)
            return error_msg, "", "❌ Error"
    
    async def get_system_status_async(self):
        """Get system status"""
        try:
            response = await self.client.get(f"{self.api_base_url}/status")
            if response.status_code == 200:
                return response.json()
            else:
                return {"status": "error", "message": f"Status code: {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def create_interface(self):
        """Create and return Gradio interface"""
        
        # Custom CSS for beautiful styling
        custom_css = """
        .gradio-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        }
        .gr-button-primary {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4) !important;
            border: none !important;
            font-weight: bold !important;
        }
        .gr-textbox textarea {
            border-radius: 10px !important;
            border: 2px solid #4ECDC4 !important;
        }
        .gr-panel {
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
        """
        
        with gr.Blocks(
            title="🧠 PRAiTEQx Multi-Expert AI System",
            css=custom_css,
            theme=gr.themes.Soft()
        ) as interface:
            
            # Header
            gr.HTML("""
                <div style="text-align: center; padding: 20px;">
                    <h1 style="color: white; font-size: 3em; margin-bottom: 10px;">
                        🧠 PRAiTEQx Multi-Expert AI
                    </h1>
                    <h2 style="color: #4ECDC4; font-size: 1.5em; margin-bottom: 20px;">
                        Powered by 6 Specialized AI Experts
                    </h2>
                    <p style="color: white; font-size: 1.2em;">
                        🎯 Chat Expert • 💻 Code Expert • ✨ Creative Expert • ⚡ Quick Expert • 🔍 Logic Expert • 🌐 Search Expert
                    </p>
                </div>
            """)
            
            # Main Interface
            with gr.Row():
                with gr.Column(scale=2):
                    # Query input
                    query_input = gr.Textbox(
                        label="💬 Ask PRAiTEQx Anything",
                        placeholder="Type your question here... (coding, creative writing, analysis, quick answers, etc.)",
                        lines=3,
                        max_lines=5
                    )
                    
                    # Options
                    with gr.Row():
                        multi_expert_toggle = gr.Checkbox(
                            label="🤝 Multi-Expert Mode (Consult multiple experts)",
                            value=True
                        )
                        
                        submit_btn = gr.Button(
                            "🚀 Generate Response",
                            variant="primary",
                            size="lg"
                        )
                
                with gr.Column(scale=1):
                    # System info
                    gr.HTML("""
                        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; color: white;">
                            <h3 style="color: #4ECDC4;">🔥 System Features</h3>
                            <ul>
                                <li>🧠 6 Specialized AI Experts</li>
                                <li>🤝 Multi-Expert Consensus</li>
                                <li>⚡ Smart Query Routing</li>
                                <li>🌐 Real-time Processing</li>
                                <li>💾 Intelligent Caching</li>
                                <li>🔍 Advanced Reasoning</li>
                            </ul>
                        </div>
                    """)
            
            # Response area
            with gr.Row():
                with gr.Column():
                    response_output = gr.Markdown(
                        label="🎯 AI Response",
                        value="Ready to help! Ask me anything and I'll consult the best experts for you."
                    )
                    
                    expert_info = gr.Markdown(
                        label="🔍 Expert Information",
                        value=""
                    )
                    
                    status_output = gr.Textbox(
                        label="📊 Status",
                        value="Ready",
                        interactive=False
                    )
            
            # Examples
            gr.Examples(
                examples=[
                    ["Write a Python function to calculate fibonacci numbers", True],
                    ["Create a short story about AI and humans working together", True],
                    ["Explain quantum computing in simple terms", True],
                    ["What is the capital of France?", False],
                    ["Help me debug this error: NameError: name 'x' is not defined", True],
                    ["Write a poem about programming", True],
                    ["Compare machine learning algorithms", True],
                ],
                inputs=[query_input, multi_expert_toggle]
            )
            
            # Event handlers
            submit_btn.click(
                fn=self.process_query_sync,
                inputs=[query_input, multi_expert_toggle],
                outputs=[response_output, expert_info, status_output]
            )
            
            # Enter key support
            query_input.submit(
                fn=self.process_query_sync,
                inputs=[query_input, multi_expert_toggle],
                outputs=[response_output, expert_info, status_output]
            )
            
            # Footer
            gr.HTML("""
                <div style="text-align: center; padding: 20px; color: white; margin-top: 30px;">
                    <p style="font-size: 1.1em;">
                        🚀 Built with <span style="color: #FF6B6B;">❤️</span> by PRAiTEQx Team
                    </p>
                    <p style="opacity: 0.8;">
                        Version 1.0.0-MVP | Multi-Expert AI System
                    </p>
                </div>
            """)
        
        return interface

def create_gradio_app(api_base_url: str = "http://localhost:8000"):
    """Create and return Gradio application"""
    ui = PRAiTEQxUI(api_base_url)
    return ui.create_interface()