#!/usr/bin/env python3
"""
DogeBot Monitoring Dashboard
===========================
Real-time monitoring and metrics for DogeBot performance
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import asyncio
import json
import time
from datetime import datetime, timedelta
import subprocess

app = FastAPI()

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Real-time DogeBot monitoring dashboard"""
    
    # Get current stats
    stats = await get_bot_stats()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>DogeBot Monitoring Dashboard</title>
        <meta http-equiv="refresh" content="30">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: #fff; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
            .stat-card {{ background: #2d2d2d; padding: 20px; border-radius: 10px; border-left: 4px solid #00ff88; }}
            .stat-value {{ font-size: 2em; font-weight: bold; color: #00ff88; }}
            .stat-label {{ color: #ccc; margin-top: 5px; }}
            .status-active {{ color: #00ff88; }}
            .status-waiting {{ color: #ffaa00; }}
            .status-error {{ color: #ff4444; }}
            .logs {{ background: #1e1e1e; padding: 15px; border-radius: 5px; font-family: monospace; font-size: 12px; max-height: 300px; overflow-y: auto; }}
            .log-line {{ margin: 2px 0; }}
            .log-info {{ color: #00aaff; }}
            .log-success {{ color: #00ff88; }}
            .log-warning {{ color: #ffaa00; }}
            .log-error {{ color: #ff4444; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 DogeBot Monitoring Dashboard</h1>
                <p>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value {stats['status_class']}">{stats['status']}</div>
                    <div class="stat-label">Bot Status</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-value">{stats['candles_collected']}</div>
                    <div class="stat-label">Candles Collected</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-value">${stats['current_price']:.6f}</div>
                    <div class="stat-label">DOGEFDUSD Price</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-value">${stats['daily_pnl']:.2f}</div>
                    <div class="stat-label">Daily PnL</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-value">{stats['open_orders']}</div>
                    <div class="stat-label">Open Orders</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-value">{stats['uptime']}</div>
                    <div class="stat-label">Uptime</div>
                </div>
            </div>
            
            <h2>📊 Current Conditions</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{stats['bb_position']:.3f}</div>
                    <div class="stat-label">Bollinger Band Position</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-value">{stats['ema_ratio']:.3f}</div>
                    <div class="stat-label">EMA Ratio</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-value {stats['entry_ready_class']}">{stats['entry_ready']}</div>
                    <div class="stat-label">Entry Conditions</div>
                </div>
            </div>
            
            <h2>📜 Recent Logs</h2>
            <div class="logs">
                {stats['recent_logs']}
            </div>
            
            <h2>⚙️ Configuration</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">$6.00</div>
                    <div class="stat-label">Daily Target</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-value">$1,100</div>
                    <div class="stat-label">Max Funds (FDUSD)</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-value">DOGEFDUSD</div>
                    <div class="stat-label">Trading Pair</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers"""
    try:
        # Quick check if containers are running
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True, timeout=5)
        if 'dogebot' in result.stdout:
            return {"status": "healthy", "timestamp": datetime.now().isoformat()}
        else:
            return {"status": "unhealthy", "reason": "containers_not_running"}
    except:
        return {"status": "unhealthy", "reason": "docker_check_failed"}

async def get_bot_stats():
    """Collect current bot statistics"""
    stats = {
        'status': 'Unknown',
        'status_class': 'status-waiting',
        'candles_collected': 0,
        'current_price': 0.201000,
        'daily_pnl': 0.00,
        'open_orders': 0,
        'uptime': '0m',
        'bb_position': 0.500,
        'ema_ratio': 1.000,
        'entry_ready': 'Waiting',
        'entry_ready_class': 'status-waiting',
        'recent_logs': ''
    }
    
    try:
        # Check Docker containers
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True, timeout=5)
        if 'dogebot' in result.stdout:
            stats['status'] = 'Running'
            stats['status_class'] = 'status-active'
            
            # Get logs from main container
            log_result = subprocess.run(['docker', 'logs', '--tail', '20', 'dogebot-container'], 
                                      capture_output=True, text=True, timeout=10)
            
            if log_result.returncode == 0:
                logs = log_result.stdout
                
                # Count candles
                stats['candles_collected'] = logs.count('Closed 15-min candle')
                
                # Parse recent logs for display
                log_lines = logs.split('\\n')[-10:]  # Last 10 lines
                formatted_logs = []
                
                for line in log_lines:
                    if line.strip():
                        css_class = 'log-info'
                        if 'ERROR' in line:
                            css_class = 'log-error'
                        elif 'WARNING' in line:
                            css_class = 'log-warning'
                        elif 'successful' in line or 'candle' in line:
                            css_class = 'log-success'
                        
                        formatted_logs.append(f'<div class="log-line {css_class}">{line}</div>')
                
                stats['recent_logs'] = '\\n'.join(formatted_logs)
                
                # Check for WebSocket connection
                if 'WebSocket handshake successful' in logs:
                    if stats['candles_collected'] >= 10:
                        stats['entry_ready'] = 'Ready'
                        stats['entry_ready_class'] = 'status-active'
                    else:
                        stats['entry_ready'] = f'Collecting Data ({stats["candles_collected"]}/10)'
                        stats['entry_ready_class'] = 'status-waiting'
        else:
            stats['status'] = 'Stopped'
            stats['status_class'] = 'status-error'
            
    except Exception as e:
        stats['status'] = f'Error: {str(e)}'
        stats['status_class'] = 'status-error'
    
    return stats

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
