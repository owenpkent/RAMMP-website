# Analytics Options for RAMMP Website (Netlify Hosted)

This document outlines available analytics solutions for the RAMMP website, currently hosted on Netlify.

---

## Option 1: Netlify Analytics (Recommended for Simplicity)

**Overview:** Server-side analytics built into Netlify—no JavaScript required.

### Features
- **Page views** and **unique visitors**
- **Top pages** and **sources/referrers**
- **404 error tracking**
- **Bandwidth usage**
- **Geographic data** (country-level)

### Pros
- No client-side JavaScript (better performance, no ad-blockers)
- GDPR-friendly (no cookies, no personal data collection)
- Simple setup—enable in Netlify dashboard
- Historical data available from site creation

### Cons
- Limited metrics compared to Google Analytics
- No user journey/funnel tracking
- No custom events or goals
- No real-time data

### Cost
| Plan | Price |
|------|-------|
| **Pro plan included** | $19/month per site |
| **Standalone add-on** | $9/month per site |

---

## Option 2: Google Analytics 4 (GA4)

**Overview:** Industry-standard, full-featured analytics platform.

### Features
- **Real-time visitor tracking**
- **User behavior and engagement metrics**
- **Conversion tracking and goals**
- **Custom events and dimensions**
- **Audience segmentation**
- **Integration with Google Ads, Search Console**
- **Funnel visualization**
- **E-commerce tracking** (if needed)

### Pros
- Free for most use cases
- Extremely detailed insights
- Industry standard—familiar to most teams
- Advanced reporting and custom dashboards
- Machine learning insights

### Cons
- Requires JavaScript snippet (can be blocked by ad-blockers)
- Privacy concerns—uses cookies
- GDPR compliance requires cookie consent banner
- Steeper learning curve
- Data sampling on free tier for high-traffic sites

### Cost
| Tier | Price |
|------|-------|
| **GA4 Standard** | Free |
| **GA4 360 (Enterprise)** | ~$50,000+/year |

### Implementation
Add to `<head>` of all HTML pages:
```html
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## Option 3: Plausible Analytics

**Overview:** Privacy-focused, lightweight analytics alternative.

### Features
- **Page views and unique visitors**
- **Bounce rate and visit duration**
- **Traffic sources and referrers**
- **Geographic data**
- **Device and browser breakdown**
- **Goal/event tracking**
- **UTM campaign tracking**

### Pros
- Privacy-first—no cookies, GDPR compliant out of the box
- Lightweight script (~1KB vs ~45KB for GA)
- Simple, clean dashboard
- Open source (can self-host)
- No cookie banner required

### Cons
- Paid service (unless self-hosted)
- Fewer features than GA4
- No user-level tracking
- Limited integrations

### Cost
| Plan | Price |
|------|-------|
| **10K pageviews/mo** | $9/month |
| **100K pageviews/mo** | $19/month |
| **1M pageviews/mo** | $69/month |
| **Self-hosted** | Free (server costs apply) |

### Implementation
Add to `<head>`:
```html
<script defer data-domain="rammp.org" src="https://plausible.io/js/script.js"></script>
```

---

## Option 4: Fathom Analytics

**Overview:** Privacy-focused analytics similar to Plausible.

### Features
- **Visitor and pageview tracking**
- **Referrer and UTM tracking**
- **Goal and event tracking**
- **EU isolation option** for GDPR
- **Uptime monitoring**

### Pros
- Privacy-first, no cookies
- GDPR/CCPA/PECR compliant
- Simple interface
- Fast, lightweight script
- Excellent uptime and support

### Cons
- Paid only (no free tier)
- Limited advanced features
- No self-hosting option

### Cost
| Plan | Price |
|------|-------|
| **100K pageviews/mo** | $14/month |
| **1M pageviews/mo** | $44/month |
| **Unlimited sites** | Included in all plans |

---

## Option 5: Umami (Self-Hosted)

**Overview:** Open-source, self-hosted analytics.

### Features
- **Real-time dashboard**
- **Page views and sessions**
- **Referrers and UTM tracking**
- **Device and browser stats**
- **Custom events**
- **Multiple websites**

### Pros
- Completely free and open source
- Full data ownership
- Privacy-focused, no cookies
- Can deploy on Vercel/Railway for free

### Cons
- Requires self-hosting and maintenance
- Limited support (community only)
- Fewer features than GA4

### Cost
| Option | Price |
|--------|-------|
| **Self-hosted** | Free |
| **Umami Cloud** | $9/month (100K events) |

---

## Comparison Summary

| Feature | Netlify | GA4 | Plausible | Fathom | Umami |
|---------|---------|-----|-----------|--------|-------|
| **Cost** | $9-19/mo | Free | $9-69/mo | $14-44/mo | Free |
| **Privacy** | ✅ Excellent | ⚠️ Requires consent | ✅ Excellent | ✅ Excellent | ✅ Excellent |
| **Setup** | ✅ 1-click | ⚠️ Moderate | ✅ Easy | ✅ Easy | ⚠️ Requires hosting |
| **Features** | Basic | Advanced | Moderate | Moderate | Moderate |
| **Cookie-free** | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **Real-time** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Custom events** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |

---

## Recommendation

### For RAMMP Website:

1. **Best for simplicity:** **Netlify Analytics** ($9/mo)
   - Already integrated with hosting
   - No code changes needed
   - Privacy-compliant

2. **Best for detailed insights:** **Google Analytics 4** (Free)
   - Most comprehensive data
   - Requires cookie consent implementation
   - Industry standard for reporting

3. **Best privacy-cost balance:** **Plausible** ($9-19/mo)
   - No cookie banner needed
   - Good feature set
   - Clean dashboard for sharing with stakeholders

### Suggested Approach
Consider using **Netlify Analytics + Plausible** together:
- Netlify for server-side baseline metrics
- Plausible for enhanced tracking with privacy compliance

---

## Next Steps

1. Decide on privacy requirements (cookie consent vs. cookie-free)
2. Determine budget allocation
3. Identify key metrics needed (basic traffic vs. conversion tracking)
4. Implement chosen solution
5. Set up dashboard access for team members

---

*Document created: February 2026*
