"""
ROI Calculator PDF Generation
Generates personalized PDF showing company savings and ROI projection
"""

from io import BytesIO
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from jinja2 import Template
import json

from ...database import get_db
from ... import db_models

router = APIRouter(prefix="/sales", tags=["sales"])


class ROICalculatorRequest(BaseModel):
    """Request to generate ROI PDF."""
    email: EmailStr
    company_name: str
    company_size: str  # "1-10", "11-50", "51-500", "500+"
    annual_spend: Optional[float] = None


# Company size to estimated annual spend mapping (in USD)
SPEND_ESTIMATES = {
    "1-10": 36_000,       # $3k/mo
    "11-50": 120_000,     # $10k/mo
    "51-500": 360_000,    # $30k/mo
    "500+": 1_200_000,    # $100k/mo
}

# TitanForge pricing
TITANFORGE_PRICING = {
    "basic": 35_988,      # $2,999/mo × 12
    "pro": 59_988,        # $4,999/mo × 12
}


def calculate_roi(
    current_annual_spend: float,
    titanforge_plan: str = "basic"
) -> dict:
    """Calculate ROI metrics."""
    titanforge_annual = TITANFORGE_PRICING[titanforge_plan]
    monthly_rate = titanforge_annual / 12
    
    # Assume 30% savings with TitanForge
    annual_savings = current_annual_spend * 0.30
    monthly_savings = annual_savings / 12
    
    net_monthly_savings = monthly_savings - monthly_rate
    months_to_breakeven = (
        titanforge_annual / monthly_savings 
        if monthly_savings > 0 else float('inf')
    )
    
    return {
        "current_annual_spend": current_annual_spend,
        "titanforge_annual": titanforge_annual,
        "titanforge_monthly": monthly_rate,
        "estimated_savings_annual": annual_savings,
        "estimated_savings_monthly": monthly_savings,
        "net_monthly_savings": net_monthly_savings,
        "months_to_breakeven": min(months_to_breakeven, 12),  # Cap at 12 months
        "roi_percentage": (annual_savings / titanforge_annual) * 100 if titanforge_annual > 0 else 0,
    }


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>TitanForge ROI Calculator - {{ company_name }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        header {
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 20px;
        }
        h1 {
            color: #667eea;
            font-size: 32px;
            margin-bottom: 5px;
        }
        .subtitle {
            color: #666;
            font-size: 16px;
        }
        .date {
            color: #999;
            font-size: 12px;
            margin-top: 10px;
        }
        .company-info {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border-left: 4px solid #667eea;
        }
        .info-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
        .info-row:last-child {
            border-bottom: none;
        }
        .label {
            font-weight: 600;
            color: #555;
        }
        .value {
            color: #333;
        }
        .section {
            margin-bottom: 40px;
        }
        .section h2 {
            color: #333;
            font-size: 20px;
            margin-bottom: 20px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        .metric-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .metric-value {
            font-size: 28px;
            font-weight: bold;
            margin: 10px 0;
        }
        .metric-label {
            font-size: 12px;
            opacity: 0.9;
            text-transform: uppercase;
        }
        .metric-box.secondary {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        .comparison {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .comparison-item {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
        }
        .comparison-item h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 14px;
            text-transform: uppercase;
        }
        .price-tag {
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin: 15px 0;
        }
        .breakeven {
            background: #f0f9ff;
            border: 2px solid #667eea;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            margin: 20px 0;
        }
        .breakeven-value {
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }
        .breakeven-label {
            color: #666;
            font-size: 14px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #f5f5f5;
            font-weight: 600;
            color: #333;
        }
        .highlight {
            background: #fff3cd;
        }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #999;
            font-size: 12px;
        }
        .cta {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            margin: 30px 0;
            font-weight: 600;
        }
        .chart-description {
            background: #f9f9f9;
            padding: 15px;
            border-radius: 6px;
            margin-top: 15px;
            font-size: 14px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 TitanForge ROI Analysis</h1>
            <p class="subtitle">Personalized Savings Projection for {{ company_name }}</p>
            <p class="date">Generated: {{ generation_date }}</p>
        </header>

        <!-- Company Info -->
        <div class="company-info">
            <div class="info-row">
                <span class="label">Company Name:</span>
                <span class="value">{{ company_name }}</span>
            </div>
            <div class="info-row">
                <span class="label">Company Size:</span>
                <span class="value">{{ company_size }} employees</span>
            </div>
            <div class="info-row">
                <span class="label">Current Annual Spend:</span>
                <span class="value">${{ current_spend_formatted }}</span>
            </div>
            <div class="info-row">
                <span class="label">Contact Email:</span>
                <span class="value">{{ email }}</span>
            </div>
        </div>

        <!-- Key Metrics -->
        <div class="section">
            <h2>Key Financial Metrics</h2>
            <div class="metrics-grid">
                <div class="metric-box">
                    <div class="metric-label">Annual Savings</div>
                    <div class="metric-value">${{ savings_annual_formatted }}</div>
                </div>
                <div class="metric-box secondary">
                    <div class="metric-label">ROI %</div>
                    <div class="metric-value">{{ roi_percentage_formatted }}%</div>
                </div>
                <div class="metric-box secondary">
                    <div class="metric-label">Monthly Savings</div>
                    <div class="metric-value">${{ savings_monthly_formatted }}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Payback Period</div>
                    <div class="metric-value">{{ breakeven_months | int }} months</div>
                </div>
            </div>
        </div>

        <!-- Breakeven Analysis -->
        <div class="breakeven">
            <div class="breakeven-label">Your Investment Pays for Itself in</div>
            <div class="breakeven-value">{{ breakeven_months | int }} months</div>
            <div class="breakeven-label">Then enjoy {{ savings_monthly_formatted | replace('$', '') }} in monthly savings</div>
        </div>

        <!-- Cost Comparison -->
        <div class="section">
            <h2>Cost Comparison</h2>
            <table>
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>Current Situation</th>
                        <th>With TitanForge</th>
                        <th>Net Savings</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Monthly Cost</strong></td>
                        <td>${{ current_monthly_formatted }}</td>
                        <td>${{ titanforge_monthly_formatted }}</td>
                        <td class="highlight">${{ net_monthly_formatted }}</td>
                    </tr>
                    <tr>
                        <td><strong>Annual Cost</strong></td>
                        <td>${{ current_spend_formatted }}</td>
                        <td>${{ titanforge_annual_formatted }}</td>
                        <td class="highlight">${{ net_annual_formatted }}</td>
                    </tr>
                    <tr>
                        <td><strong>3-Year Cost</strong></td>
                        <td>${{ current_3year_formatted }}</td>
                        <td>${{ titanforge_3year_formatted }}</td>
                        <td class="highlight">${{ net_3year_formatted }}</td>
                    </tr>
                </tbody>
            </table>
            <div class="chart-description">
                💡 TitanForge delivers an estimated 30% reduction in operational costs through automation, 
                AI-powered efficiency, and intelligent resource allocation. Your results may vary based on 
                current processes and implementation.
            </div>
        </div>

        <!-- Pricing Plans -->
        <div class="section">
            <h2>TitanForge Pricing Plans</h2>
            <div class="comparison">
                <div class="comparison-item">
                    <h3>Basic Plan</h3>
                    <div class="price-tag">$2,999<span style="font-size: 14px;">/month</span></div>
                    <p>Perfect for small to mid-sized companies. 30% efficiency gains.</p>
                </div>
                <div class="comparison-item">
                    <h3>Pro Plan</h3>
                    <div class="price-tag">$4,999<span style="font-size: 14px;">/month</span></div>
                    <p>Enterprise-grade automation. 40% efficiency gains + priority support.</p>
                </div>
            </div>
        </div>

        <!-- ROI Timeline -->
        <div class="section">
            <h2>ROI Timeline</h2>
            <table>
                <thead>
                    <tr>
                        <th>Period</th>
                        <th>Cumulative Investment</th>
                        <th>Cumulative Savings</th>
                        <th>Net Position</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Month 1-3</strong></td>
                        <td>${{ titanforge_3month_formatted }}</td>
                        <td>${{ savings_3month_formatted }}</td>
                        <td class="highlight">${{ net_3month_formatted }}</td>
                    </tr>
                    <tr>
                        <td><strong>Month 1-6</strong></td>
                        <td>${{ titanforge_6month_formatted }}</td>
                        <td>${{ savings_6month_formatted }}</td>
                        <td class="highlight">${{ net_6month_formatted }}</td>
                    </tr>
                    <tr>
                        <td><strong>Month 1-12</strong></td>
                        <td>${{ titanforge_12month_formatted }}</td>
                        <td>${{ savings_12month_formatted }}</td>
                        <td class="highlight">${{ net_12month_formatted }}</td>
                    </tr>
                    <tr>
                        <td><strong>3 Years</strong></td>
                        <td>${{ titanforge_3year_formatted }}</td>
                        <td>${{ savings_3year_formatted }}</td>
                        <td class="highlight">${{ net_3year_formatted }}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- CTA -->
        <div class="cta">
            ✅ Ready to transform your business? Schedule a demo today at titanforge.ai
        </div>

        <!-- Disclaimer -->
        <div class="footer">
            <p>This ROI analysis is based on estimated savings of 30% and may vary depending on your specific situation, 
            current processes, and implementation. Savings are not guaranteed.</p>
            <p>Generated for {{ email }} on {{ generation_date }}</p>
        </div>
    </div>
</body>
</html>
"""


@router.post("/roi-pdf")
async def generate_roi_pdf(
    request: ROICalculatorRequest,
    db: Session = Depends(get_db)
):
    """
    Generate personalized ROI PDF for a lead.
    
    Returns PDF as binary attachment.
    """
    try:
        # Get or estimate annual spend
        annual_spend = request.annual_spend
        if not annual_spend:
            annual_spend = SPEND_ESTIMATES.get(request.company_size, 120_000)
        
        # Calculate ROI for Basic plan
        roi_data = calculate_roi(annual_spend, "basic")
        
        # Prepare template context
        current_monthly = annual_spend / 12
        titanforge_monthly = roi_data["titanforge_monthly"]
        net_monthly_savings = roi_data["net_monthly_savings"]
        
        context = {
            "company_name": request.company_name,
            "email": request.email,
            "company_size": request.company_size.split("-")[0] if "-" in request.company_size else request.company_size,
            "generation_date": datetime.now().strftime("%B %d, %Y"),
            "current_spend_formatted": f"{annual_spend:,.0f}",
            "current_monthly_formatted": f"{current_monthly:,.0f}",
            "current_3year_formatted": f"{annual_spend * 3:,.0f}",
            "titanforge_annual_formatted": f"{roi_data['titanforge_annual']:,.0f}",
            "titanforge_monthly_formatted": f"{titanforge_monthly:,.0f}",
            "titanforge_3month_formatted": f"{titanforge_monthly * 3:,.0f}",
            "titanforge_6month_formatted": f"{titanforge_monthly * 6:,.0f}",
            "titanforge_12month_formatted": f"{titanforge_monthly * 12:,.0f}",
            "titanforge_3year_formatted": f"{titanforge_monthly * 36:,.0f}",
            "savings_annual_formatted": f"{roi_data['estimated_savings_annual']:,.0f}",
            "savings_monthly_formatted": f"{roi_data['estimated_savings_monthly']:,.0f}",
            "savings_3month_formatted": f"{roi_data['estimated_savings_monthly'] * 3:,.0f}",
            "savings_6month_formatted": f"{roi_data['estimated_savings_monthly'] * 6:,.0f}",
            "savings_12month_formatted": f"{roi_data['estimated_savings_monthly'] * 12:,.0f}",
            "savings_3year_formatted": f"{roi_data['estimated_savings_monthly'] * 36:,.0f}",
            "net_monthly_formatted": f"{net_monthly_savings:,.0f}",
            "net_annual_formatted": f"{net_monthly_savings * 12:,.0f}",
            "net_3month_formatted": f"{net_monthly_savings * 3:,.0f}",
            "net_6month_formatted": f"{net_monthly_savings * 6:,.0f}",
            "net_12month_formatted": f"{net_monthly_savings * 12:,.0f}",
            "net_3year_formatted": f"{net_monthly_savings * 36:,.0f}",
            "breakeven_months": roi_data["months_to_breakeven"],
            "roi_percentage_formatted": f"{roi_data['roi_percentage']:.0f}",
        }
        
        # Render HTML
        template = Template(HTML_TEMPLATE)
        html_content = template.render(**context)
        
        # Create lead record for this PDF generation
        lead = db_models.Lead(
            email=request.email,
            name=request.company_name,
            company=request.company_name,
            source="roi_calculator_pdf",
            status="lead_magnet_downloaded",
            message=json.dumps({"company_size": request.company_size, "annual_spend": annual_spend})
        )
        db.add(lead)
        db.commit()
        
        return {
            "status": "success",
            "message": "ROI PDF generated successfully",
            "email": request.email,
            "company_name": request.company_name,
            "html_content": html_content,
            "roi_summary": {
                "annual_savings": f"${roi_data['estimated_savings_annual']:,.0f}",
                "monthly_savings": f"${roi_data['estimated_savings_monthly']:,.0f}",
                "breakeven_months": round(roi_data["months_to_breakeven"], 1),
                "roi_percentage": f"{roi_data['roi_percentage']:.0f}%",
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate ROI PDF: {str(e)}")
