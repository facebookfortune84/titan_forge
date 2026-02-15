import os

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

LANDING_PAGE_FILE = "landing_page.html"  # File to store agent-generated HTML


@router.get("/landing_page_html", response_class=HTMLResponse)
async def get_landing_page_html():
    """
    Returns the HTML content for the agent-designed landing page.
    """
    # In a real scenario, this would load content from a database or a file
    # updated by an agent. For now, we return a placeholder.
    if os.path.exists(LANDING_PAGE_FILE):
        with open(LANDING_PAGE_FILE, "r") as f:
            html_content = f.read()
    else:
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Agent-Designed Landing Page</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4; color: #333; }
                .container { max-width: 800px; margin: auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                h1 { color: #0056b3; }
                p { line-height: 1.6; }
                .cta-button {
                    display: inline-block;
                    background-color: #28a745;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 5px;
                    text-decoration: none;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to RealmstoRiches!</h1>
                <p>This is a landing page designed and updated by our autonomous agents.</p>
                <p>Our SAAS product is the focal point. It helps you automate your business processes and generate revenue with the power of AI agents.</p>
                <p>Stay tuned for more updates as our agents refine this page and bring you the best features!</p>
                <a href="#" class="cta-button">Learn More & Get Started</a>
            </div>
        </body>
        </html>
        """
    return HTMLResponse(content=html_content)
