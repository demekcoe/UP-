# Deployment Guide for UP Website

## Prerequisites
- Node.js and npm installed
- Heroku CLI installed
- Netlify CLI installed
- Git installed

## Frontend Deployment (Netlify)

1. Install Netlify CLI:
```bash
npm install -g netlify-cli
```

2. Login to Netlify:
```bash
netlify login
```

3. Initialize and deploy:
```bash
netlify init
# Choose "Create & configure a new site"
# Choose your team
# Choose a site name or let Netlify generate one
```

4. Deploy the site:
```bash
netlify deploy --prod
```

## Backend Deployment (Heroku)

1. Login to Heroku:
```bash
heroku login
```

2. Create a new Heroku app:
```bash
heroku create up-website-backend
```

3. Set environment variables:
```bash
heroku config:set EMAIL_PASSWORD=your_gmail_app_password
heroku config:set ALLOWED_ORIGIN=https://your-netlify-domain.netlify.app
```

4. Deploy to Heroku:
```bash
git push heroku main
```

5. Verify the deployment:
```bash
heroku logs --tail
```

## Custom Domain Setup

### Frontend (Netlify)

1. Go to Netlify dashboard > your site > Domain settings
2. Click "Add custom domain"
3. Enter your domain (e.g., www.upwebsite.com)
4. Follow Netlify's DNS instructions:
   - Add CNAME record pointing to your Netlify site
   - Add A record if using apex domain

### Backend (Heroku)

1. Purchase SSL certificate for your backend domain
2. Add custom domain in Heroku:
```bash
heroku domains:add api.yourdomain.com
```
3. Configure DNS settings with your provider
4. Update frontend API URLs to use your custom domain

## Post-Deployment Checks

1. Test contact form submission
2. Test booking form submission
3. Verify email delivery
4. Check mobile responsiveness
5. Verify 3D model loading
6. Test navigation across all pages

## Monitoring

- View Netlify analytics: Netlify Dashboard > your site > Analytics
- Monitor Heroku logs: `heroku logs --tail`
- Check application logs in Heroku dashboard
- Monitor email delivery in Gmail sent folder

## Troubleshooting

### Common Issues

1. CORS errors:
   - Verify ALLOWED_ORIGIN in Heroku config
   - Check frontend API URLs

2. Email not sending:
   - Verify EMAIL_PASSWORD in Heroku config
   - Check Gmail app password validity
   - Review Heroku logs for SMTP errors

3. Form submission errors:
   - Check browser console for errors
   - Verify API endpoints in frontend code
   - Check Heroku application logs

### Support Contacts

- Backend issues: [Your contact info]
- Frontend issues: [Your contact info]
- Domain/DNS issues: [Your domain provider contact]

## Maintenance

1. Regular checks:
   - Monitor Heroku dyno hours
   - Check Netlify build minutes
   - Review application logs
   - Test form submissions

2. Updates:
   - Keep Python packages updated
   - Review security headers
   - Update SSL certificates
   - Monitor Gmail API usage

## Netlify Functions (Email forwarding)

If you want Netlify to forward form submissions as emails automatically, the repository contains a function at `netlify/functions/forward-email.js` that uses `nodemailer`. To enable it:

1. Add the following environment variables in your Netlify site settings (Site settings → Build & deploy → Environment):

    - `SMTP_HOST` (e.g. smtp.gmail.com)
    - `SMTP_PORT` (e.g. 587)
    - `SMTP_USER` (your SMTP username — your email)
    - `SMTP_PASS` (your SMTP app password)
    - `TO_EMAIL` (optional, receiver address; defaults to `SMTP_USER`)

2. Netlify will automatically install `nodemailer` from `package.json` during deploy. The function endpoint will be available under `/.netlify/functions/forward-email`.

3. The frontend code posts Netlify form data to the site root; Netlify captures it. To forward captured submissions immediately, the frontend also sends the same data to the serverless function; this function expects a JSON body with a `type` field set to `contact` or `booking`.

Security notes:
- Keep SMTP credentials secret (use Netlify environment variables). Do not commit them to the repository.
- For Gmail, generate an App Password and use that as `SMTP_PASS`.