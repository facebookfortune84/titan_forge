"""Landing page and lead magnet delivery system."""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, FileResponse
import os

router = APIRouter(tags=["landing"])


@router.get("/landing", response_class=HTMLResponse)
async def landing_page():
    """Main landing page - where traffic drives to."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TitanForge - AI Agency-in-a-Box</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                line-height: 1.6;
                color: #333;
            }
            
            .hero {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 80px 20px;
                text-align: center;
                min-height: 600px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }
            
            .hero h1 {
                font-size: 48px;
                margin-bottom: 20px;
                font-weight: 800;
            }
            
            .hero p {
                font-size: 20px;
                margin-bottom: 30px;
                opacity: 0.95;
                max-width: 600px;
            }
            
            .cta-button {
                background: white;
                color: #667eea;
                padding: 16px 40px;
                border-radius: 8px;
                font-size: 18px;
                font-weight: 700;
                border: none;
                cursor: pointer;
                transition: all 0.3s ease;
                display: inline-block;
                text-decoration: none;
            }
            
            .cta-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            }
            
            .benefits {
                padding: 60px 20px;
                background: #f9fafb;
            }
            
            .benefits-container {
                max-width: 1000px;
                margin: 0 auto;
            }
            
            .benefits h2 {
                text-align: center;
                font-size: 32px;
                margin-bottom: 40px;
                color: #333;
            }
            
            .benefits-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 30px;
            }
            
            .benefit-card {
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                text-align: center;
            }
            
            .benefit-icon {
                font-size: 40px;
                margin-bottom: 15px;
            }
            
            .benefit-card h3 {
                margin-bottom: 10px;
                color: #333;
            }
            
            .benefit-card p {
                color: #666;
                font-size: 14px;
            }
            
            .pricing {
                padding: 60px 20px;
                background: white;
            }
            
            .pricing-container {
                max-width: 1000px;
                margin: 0 auto;
            }
            
            .pricing h2 {
                text-align: center;
                font-size: 32px;
                margin-bottom: 40px;
                color: #333;
            }
            
            .pricing-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
            }
            
            .price-card {
                background: #f9fafb;
                padding: 40px 30px;
                border-radius: 12px;
                text-align: center;
                border: 2px solid transparent;
                transition: all 0.3s ease;
            }
            
            .price-card:hover {
                border-color: #667eea;
                transform: translateY(-5px);
                box-shadow: 0 15px 40px rgba(102, 126, 234, 0.1);
            }
            
            .price-card h3 {
                margin-bottom: 15px;
                font-size: 20px;
                color: #333;
            }
            
            .price {
                font-size: 36px;
                font-weight: 700;
                color: #667eea;
                margin-bottom: 10px;
            }
            
            .price-label {
                color: #666;
                font-size: 13px;
                margin-bottom: 20px;
            }
            
            .features {
                text-align: left;
                margin: 25px 0;
                font-size: 14px;
                color: #666;
            }
            
            .features li {
                list-style: none;
                padding: 8px 0;
                border-bottom: 1px solid #e5e7eb;
            }
            
            .features li:before {
                content: "✓ ";
                color: #10b981;
                font-weight: 700;
                margin-right: 8px;
            }
            
            .cta-section {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 60px 20px;
                text-align: center;
            }
            
            .cta-section h2 {
                font-size: 36px;
                margin-bottom: 20px;
            }
            
            .cta-section p {
                font-size: 18px;
                margin-bottom: 30px;
                opacity: 0.95;
            }
            
            .form-container {
                max-width: 500px;
                margin: 0 auto;
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 12px;
                backdrop-filter: blur(10px);
            }
            
            .form-group {
                margin-bottom: 15px;
                text-align: left;
            }
            
            .form-group label {
                display: block;
                margin-bottom: 5px;
                font-weight: 600;
                font-size: 14px;
            }
            
            .form-group input {
                width: 100%;
                padding: 12px;
                border: none;
                border-radius: 6px;
                font-size: 14px;
            }
            
            .form-group input:focus {
                outline: none;
                box-shadow: 0 0 0 3px rgba(255,255,255,0.3);
            }
            
            .submit-btn {
                width: 100%;
                background: white;
                color: #667eea;
                padding: 14px;
                border-radius: 6px;
                border: none;
                font-weight: 700;
                font-size: 16px;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .submit-btn:hover {
                transform: scale(1.02);
            }
        </style>
    </head>
    <body>
        <div class="hero">
            <h1>🚀 Replace Your Expensive Agency</h1>
            <p>TitanForge gives you an AI agency team that works 24/7 - at $2,999/month instead of $10K+.</p>
            <p style="font-size: 16px; color: rgba(255,255,255,0.8);">See your exact savings in 60 seconds</p>
            <button class="cta-button" onclick="scrollToCTA()">Get Free ROI Calculator</button>
        </div>
        
        <div class="benefits">
            <div class="benefits-container">
                <h2>Why TitanForge?</h2>
                <div class="benefits-grid">
                    <div class="benefit-card">
                        <div class="benefit-icon">⚡</div>
                        <h3>3-5x Faster</h3>
                        <p>Generate content, code, and reports in hours instead of weeks</p>
                    </div>
                    <div class="benefit-card">
                        <div class="benefit-icon">💰</div>
                        <h3>Save $84K/Year</h3>
                        <p>Replace $10K agency spend with $2,999/month. ROI in <1 week.</p>
                    </div>
                    <div class="benefit-card">
                        <div class="benefit-icon">🎯</div>
                        <h3>Your Control</h3>
                        <p>Keep IP in-house. Train agents on your brand and process.</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="pricing">
            <div class="pricing-container">
                <h2>Simple Pricing</h2>
                <div class="pricing-grid">
                    <div class="price-card">
                        <h3>Basic Tier</h3>
                        <div class="price">$2,999</div>
                        <div class="price-label">/month (or $2,499/mo annual)</div>
                        <ul class="features">
                            <li>All AI agents</li>
                            <li>Unlimited API calls</li>
                            <li>Email support</li>
                            <li>Concierge onboarding</li>
                        </ul>
                    </div>
                    <div class="price-card">
                        <h3>Professional</h3>
                        <div class="price">$4,999</div>
                        <div class="price-label">/month (or $4,499/mo annual)</div>
                        <ul class="features">
                            <li>All Basic features</li>
                            <li>Dedicated success manager</li>
                            <li>Priority support (2hr response)</li>
                            <li>Advanced analytics</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="cta-section">
            <h2>Ready to Save $84K/Year?</h2>
            <p>Download our free ROI calculator and see your exact savings</p>
            
            <div class="form-container">
                <form onsubmit="submitLeadMagnet(event)">
                    <div class="form-group">
                        <label>Your Email</label>
                        <input type="email" name="email" required placeholder="you@company.com">
                    </div>
                    <div class="form-group">
                        <label>Company Name</label>
                        <input type="text" name="company_name" required placeholder="Acme Corp">
                    </div>
                    <div class="form-group">
                        <label>Company Size</label>
                        <select name="company_size" required style="width: 100%; padding: 12px; border: none; border-radius: 6px; font-size: 14px;">
                            <option value="">Select...</option>
                            <option value="1-10">1-10 people</option>
                            <option value="11-50">11-50 people</option>
                            <option value="51-500">51-500 people</option>
                            <option value="500+">500+ people</option>
                        </select>
                    </div>
                    <button type="submit" class="submit-btn">📥 Download ROI Calculator</button>
                </form>
            </div>
        </div>
        
        <script>
            function scrollToCTA() {
                document.querySelector('.cta-section').scrollIntoView({ behavior: 'smooth' });
            }
            
            async function submitLeadMagnet(event) {
                event.preventDefault();
                
                const formData = new FormData(event.target);
                const data = {
                    email: formData.get('email'),
                    company_name: formData.get('company_name'),
                    company_size: formData.get('company_size'),
                    utm_source: 'landing_page',
                    utm_campaign: 'roi_calculator'
                };
                
                try {
                    const response = await fetch('/api/v1/sales/lead-magnet/download', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    
                    if (response.ok) {
                        alert('✅ Check your email for the ROI Calculator!\\n\\nYou\'ll also receive a 7-day email sequence showing you exactly how much you can save.');
                        event.target.reset();
                    } else {
                        alert('Error: ' + response.statusText);
                    }
                } catch (error) {
                    alert('Error downloading: ' + error.message);
                }
            }
        </script>
    </body>
    </html>
    """


# ============================================================
# LEGAL DOCUMENTS ENDPOINTS
# ============================================================

@router.get("/privacy", response_class=HTMLResponse)
async def privacy_policy():
    """Serve Privacy Policy."""
    try:
        with open("F:\\TitanForge\\PRIVACY_POLICY.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Privacy Policy - TitanForge</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                    line-height: 1.7;
                    color: #333;
                    background: #f5f5f5;
                    padding: 20px;
                }}
                .container {{
                    max-width: 900px;
                    margin: 0 auto;
                    background: white;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                h1, h2, h3 {{ color: #667eea; }}
                h1 {{ border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
                a {{ color: #667eea; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
                code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
                pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div style="margin-bottom: 30px;">
                    <a href="/">&larr; Back to Home</a>
                </div>
                {_markdown_to_html(content)}
            </div>
        </body>
        </html>
        """
    except FileNotFoundError:
        return "<h1>Privacy Policy not found</h1>"


@router.get("/terms", response_class=HTMLResponse)
async def terms_of_service():
    """Serve Terms of Service."""
    try:
        with open("F:\\TitanForge\\TERMS_OF_SERVICE.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Terms of Service - TitanForge</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                    line-height: 1.7;
                    color: #333;
                    background: #f5f5f5;
                    padding: 20px;
                }}
                .container {{
                    max-width: 900px;
                    margin: 0 auto;
                    background: white;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                h1, h2, h3 {{ color: #667eea; }}
                h1 {{ border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
                a {{ color: #667eea; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
                code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
                pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div style="margin-bottom: 30px;">
                    <a href="/">&larr; Back to Home</a>
                </div>
                {_markdown_to_html(content)}
            </div>
        </body>
        </html>
        """
    except FileNotFoundError:
        return "<h1>Terms of Service not found</h1>"


@router.get("/data-sale", response_class=HTMLResponse)
async def data_sale_agreement():
    """Serve Data Sale Agreement."""
    try:
        with open("F:\\TitanForge\\DATA_SALE_AGREEMENT.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Data Sale Agreement - TitanForge</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                    line-height: 1.7;
                    color: #333;
                    background: #f5f5f5;
                    padding: 20px;
                }}
                .container {{
                    max-width: 900px;
                    margin: 0 auto;
                    background: white;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                h1, h2, h3 {{ color: #667eea; }}
                h1 {{ border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
                a {{ color: #667eea; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
                code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
                pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
                .highlight {{ background: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div style="margin-bottom: 30px;">
                    <a href="/">&larr; Back to Home</a>
                </div>
                {_markdown_to_html(content)}
            </div>
        </body>
        </html>
        """
    except FileNotFoundError:
        return "<h1>Data Sale Agreement not found</h1>"


@router.get("/affiliate", response_class=HTMLResponse)
async def affiliate_disclaimer():
    """Serve Affiliate Program Disclaimer."""
    try:
        with open("F:\\TitanForge\\AFFILIATE_DISCLAIMER.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Affiliate Program Disclaimer - TitanForge</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                    line-height: 1.7;
                    color: #333;
                    background: #f5f5f5;
                    padding: 20px;
                }}
                .container {{
                    max-width: 900px;
                    margin: 0 auto;
                    background: white;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                h1, h2, h3 {{ color: #667eea; }}
                h1 {{ border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
                a {{ color: #667eea; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
                code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
                pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
                .warning {{ background: #f8d7da; border-left: 4px solid #dc3545; padding: 15px; margin: 15px 0; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div style="margin-bottom: 30px;">
                    <a href="/">&larr; Back to Home</a>
                </div>
                {_markdown_to_html(content)}
            </div>
        </body>
        </html>
        """
    except FileNotFoundError:
        return "<h1>Affiliate Disclaimer not found</h1>"


def _markdown_to_html(markdown_text: str) -> str:
    """Simple markdown to HTML converter."""
    import re
    html = markdown_text
    
    # Headers
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # Bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'__(.*?)__', r'<strong>\1</strong>', html)
    
    # Italic
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    html = re.sub(r'_(.*?)_', r'<em>\1</em>', html)
    
    # Links
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
    
    # Line breaks to paragraphs
    html = re.sub(r'\n\n+', '</p><p>', html)
    html = '<p>' + html + '</p>'
    
    # Lists
    html = re.sub(r'<p>- (.*?)</p>', r'<ul><li>\1</li></ul>', html)
    html = re.sub(r'</ul>\n*<ul>', '', html)
    
    return html
