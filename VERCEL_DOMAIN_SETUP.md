# Vercel + Custom Domain Quick Start

## 🎯 Your Goal
Deploy to **different Vercel account** + connect to **www.realmstoriches.xyz**

---

## ⚡ FASTEST PATH (5 Minutes)

### Step 1: Sign Out & Switch Account
```powershell
vercel logout
vercel login
# Browser opens - authorize with your new account
```

### Step 2: Deploy Frontend
```powershell
cd frontend
vercel deploy --prod
```
✅ Returns: `https://titanforge-frontend.vercel.app`

### Step 3: Add Custom Domain
```powershell
vercel domains add www.realmstoriches.xyz
```

Vercel shows DNS records. Copy them.

### Step 4: Update DNS at Your Registrar
1. Go to where you own **realmstoriches.xyz** (GoDaddy, Namecheap, etc.)
2. Find DNS settings
3. Add the records Vercel showed
4. Wait 5-30 min for propagation

### Step 5: Done!
Visit: `https://www.realmstoriches.xyz`

---

## 🔧 AUTOMATED SCRIPT

```powershell
.\deploy-vercel-domain.ps1 -Domain "www.realmstoriches.xyz"
```

Script will:
1. ✅ Build frontend
2. ✅ Prompt to switch account
3. ✅ Deploy to new account
4. ✅ Add domain
5. ✅ Show DNS instructions

---

## 📍 FINDING YOUR DOMAIN REGISTRAR

Where did you buy **realmstoriches.xyz**?

| Registrar | DNS Link | How to Find |
|-----------|----------|------------|
| **GoDaddy** | godaddy.com | Look for "Manage Domains" |
| **Namecheap** | namecheap.com | Look for "Domain List" → Manage DNS |
| **Google Domains** | domains.google.com | Click domain → DNS |
| **Route53** | AWS Console | Route 53 service |
| **Cloudflare** | cloudflare.com | Nameservers or DNS tab |
| **Domain.com** | domain.com | My Domains → Manage DNS |

Don't know? Check your email for domain confirmation/receipt.

---

## 🔐 Vercel Account Options

### Option A: Different Personal Account
```
Best for: Using your own account
Steps:
1. vercel logout
2. vercel login (with your email)
3. Deploy and add domain
```

### Option B: Same Account, Just Add Domain
```
Best for: If you want to keep realmstoriches account
Steps:
1. vercel domains add www.realmstoriches.xyz
2. Done!
```

### Option C: Vercel Team Account
```
Best for: Multi-person team
Steps:
1. Create team at vercel.com
2. Add domain to team account
```

---

## 🌐 DNS Setup Examples

### GoDaddy
1. Go to godaddy.com → My Domains
2. Find realmstoriches.xyz
3. Click "Manage DNS"
4. Add CNAME record from Vercel
5. Save

### Namecheap
1. Go to namecheap.com → Domain List
2. Click "Manage" next to realmstoriches.xyz
3. Go to "Advanced DNS"
4. Add records
5. Save

### Google Domains
1. Go to domains.google.com
2. Click realmstoriches.xyz
3. Click "DNS"
4. Add records
5. Save

---

## ✅ VERIFY IT WORKS

### Before DNS Propagates
```bash
# Use Vercel URL
curl https://titanforge-frontend.vercel.app
# Should return: Landing page HTML
```

### After DNS Propagates (5-30 min)
```bash
# Use your domain
curl https://www.realmstoriches.xyz
# Should return: Same landing page

# Check DNS
nslookup www.realmstoriches.xyz
# Should show Vercel's IP
```

---

## 🆘 DNS Troubleshooting

### "Domain doesn't work after 30 min"

**Step 1: Check DNS was added correctly**
```bash
nslookup www.realmstoriches.xyz
# Should show Vercel's nameserver
```

**Step 2: Clear browser cache**
- Ctrl+Shift+Delete (clear browsing data)
- Close and reopen browser

**Step 3: Wait longer**
- DNS can take up to 24 hours
- Try again in a few hours

**Step 4: Check Vercel dashboard**
- https://vercel.com/dashboard
- Click project → Domains
- Should show domain status

### "Vercel says domain not verified"

1. Double-check DNS records match exactly
2. Wait longer (DNS propagation)
3. Try from different browser/device
4. Check registrar DNS panel - make sure changes saved

---

## 📚 HELPFUL LINKS

- **Vercel Domains Guide:** https://vercel.com/docs/concepts/projects/domains/add-a-domain
- **DNS Checker:** https://www.whatsmydns.net
- **CNAME Explanation:** https://www.cloudflare.com/learning/dns/dns-records/dns-cname-record/
- **GoDaddy DNS Help:** https://www.godaddy.com/help/
- **Namecheap DNS Help:** https://www.namecheap.com/support/

---

## 🎯 SUMMARY

| Step | Time | Action |
|------|------|--------|
| 1 | 1 min | Sign into new Vercel account |
| 2 | 1 min | Deploy: `vercel deploy --prod` |
| 3 | 1 min | Add domain: `vercel domains add www.realmstoriches.xyz` |
| 4 | 2 min | Copy DNS records |
| 5 | 2 min | Add DNS to registrar |
| 6 | 5-30 min | Wait for DNS propagation |
| 7 | - | Visit `https://www.realmstoriches.xyz` ✅ |

---

## 💡 TIPS

**Don't have DNS access?**
- Use Vercel URL: `https://titanforge-frontend.vercel.app`
- Deploy backend to Railway
- Start selling! (You can add domain later)

**Want both www and without www?**
- Add both: `www.realmstoriches.xyz` + `realmstoriches.xyz`
- Vercel handles redirects automatically

**Already using the domain elsewhere?**
- You may need to move DNS to Vercel or Cloudflare first
- Contact your registrar for help

---

Ready? Let's go! 🚀

```powershell
.\deploy-vercel-domain.ps1
```

Or manually:
```powershell
vercel logout
vercel login
cd frontend
vercel deploy --prod
vercel domains add www.realmstoriches.xyz
```
