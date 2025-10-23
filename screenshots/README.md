Screenshots: How to add SMTP environment variables to Netlify

Files:
- step1_dashboard.svg — where to find Site settings → Build & deploy → Environment
- step2_env_vars.svg — example environment variable entries (keys and sample values)
- step3_trigger_deploy.svg — trigger a deploy after saving env vars

Quick steps (copyable):
1. Open your Netlify site dashboard (https://app.netlify.com/sites/<your-site-name>/overview)
2. Click "Site settings" in the left sidebar.
3. Choose "Build & deploy" → scroll to "Environment" and click "Edit variables".
4. Add the following keys and values (replace example values):
   - SMTP_HOST: smtp.gmail.com
   - SMTP_PORT: 587
   - SMTP_USER: diamondminddynasty@gmail.com
   - SMTP_PASS: <your 16-character Gmail App Password>
   - TO_EMAIL: diamondminddynasty@gmail.com  # optional - where forwarded emails will be sent
5. Save the variables.
6. Trigger a new deploy: either click "Deploy site" on the dashboard or push a new commit to your repo.
7. After deploy completes, test the Contact and Booking forms at your production URL.

Security notes:
- Do not commit SMTP_PASS, SMTP_USER, or other secrets to version control.
- Use an App Password for Gmail (recommended) rather than your main account password.
- If you need to rotate the password, update the Netlify env var and trigger a new deploy.

If you want I can also produce a small one-click script that opens the Netlify env page in your browser (macOS) given your site name, or create PNG exports of the SVGs. Tell me which.