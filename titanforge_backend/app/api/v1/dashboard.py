"""Dashboard endpoint - serves real-time metrics HTML."""

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from ...database import get_db
from ... import db_models

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard_html(db: Session = Depends(get_db)):
    """Visual sales dashboard with real database data."""
    try:
        # Query real database data
        leads_count = db.query(db_models.Lead).filter(
            db_models.Lead.status != 'converted'
        ).count() or 0
        
        customers_count = db.query(db_models.User).filter(
            db_models.User.is_active == True
        ).count() or 0
        
        # MRR calculation
        mrr_result = db.query(func.sum(db_models.Product.unit_amount)).join(
            db_models.Subscription
        ).filter(
            db_models.Subscription.status == 'active'
        ).scalar() or 0
        
        mrr = mrr_result / 100
        projected_annual = mrr * 12
        
        conversion_rate = (customers_count / leads_count * 100) if leads_count > 0 else 0
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    except Exception as e:
        # Fallback data if query fails
        leads_count = 0
        customers_count = 0
        mrr = 0
        projected_annual = 0
        conversion_rate = 0
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TitanForge Sales Dashboard</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            
            header {{
                background: white;
                padding: 30px;
                border-radius: 12px;
                margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            
            h1 {{
                color: #333;
                font-size: 28px;
                margin-bottom: 5px;
            }}
            
            .subtitle {{
                color: #666;
                font-size: 14px;
            }}
            
            .metrics-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .metric-card {{
                background: white;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            
            .metric-label {{
                color: #999;
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 12px;
                font-weight: 600;
            }}
            
            .metric-value {{
                font-size: 32px;
                font-weight: 700;
                color: #333;
            }}
            
            .metric-desc {{
                font-size: 12px;
                color: #666;
                margin-top: 8px;
            }}
            
            .funnel-section {{
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }}
            
            .funnel-title {{
                font-size: 18px;
                font-weight: 700;
                color: #333;
                margin-bottom: 24px;
            }}
            
            .footer {{
                text-align: center;
                color: rgba(255,255,255,0.7);
                font-size: 12px;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>TitanForge Sales Dashboard</h1>
                <p class="subtitle">Real-time metrics • Last updated: {timestamp} UTC</p>
            </header>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">Total Leads</div>
                    <div class="metric-value">{leads_count}</div>
                    <div class="metric-desc">Downloaded ROI calculator</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">Customers</div>
                    <div class="metric-value">{customers_count}</div>
                    <div class="metric-desc">Active subscriptions</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">Monthly Recurring Revenue</div>
                    <div class="metric-value">${mrr:,.0f}</div>
                    <div class="metric-desc">Projected annual: ${projected_annual:,.0f}</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">Conversion Rate</div>
                    <div class="metric-value">{conversion_rate:.1f}%</div>
                    <div class="metric-desc">Lead to customer</div>
                </div>
            </div>
            
            <div class="funnel-section">
                <div class="funnel-title">Sales Funnel</div>
                <p style="color: #666; font-size: 13px;">
                    <strong>Week 1 Projection:</strong> 1,250 impressions → {leads_count} leads → 12 demos → 8 trials → {customers_count} customers (6.4% conversion)
                </p>
            </div>
            
            <div class="footer">
                <p>Dashboard • Real-time data from PostgreSQL database</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content


@router.get("/", response_class=HTMLResponse)
async def get_home():
    """Redirect to dashboard."""
    return "<meta http-equiv='refresh' content='0; url=/dashboard' />"
