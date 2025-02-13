# Discord TTS Bot - 24/7 Hosting Guide

## Keeping Your Bot Online 24/7

1. Enable "Always On" in Replit:
   - Go to your project's Tools tab
   - Click on "Always On"
   - Toggle it ON

2. Set up UptimeRobot (Free):
   - Go to [UptimeRobot](https://uptimerobot.com/)
   - Sign up for a free account
   - Click "Add New Monitor"
   - Select "HTTP(s)"
   - Name: "Discord TTS Bot"
   - URL: Your Replit web server URL (find this in the "Webview" tab)
   - Monitoring Interval: Every 5 minutes
   - Click "Create Monitor"

Your bot will now stay online 24/7, even when your computer is off!

## Important Notes
- The web server automatically starts with your bot
- UptimeRobot pings your bot every 5 minutes to keep it active
- You can check your bot's uptime status on UptimeRobot's dashboard
