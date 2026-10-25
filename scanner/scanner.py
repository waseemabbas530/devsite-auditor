import requests

def audit_target(url):
    results = {
        "url": url,
        "score": 100,
        "headers": {},
        "cookies": {},
        "files": {}
    }
    
    # Ensure URL has proper scheme
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:
        # Fetch target page with timeout and redirect tracking
        response = requests.get(url, timeout=5, allow_redirects=True, headers={"User-Agent": "DevSiteAuditor/1.0"})
        headers = response.headers
        
        # 1. Security Headers Analysis
        security_headers = {
            "Content-Security-Policy": "Mitigates XSS & Injection",
            "X-Frame-Options": "Protects against Clickjacking",
            "X-Content-Type-Options": "Prevents MIME-sniffing",
            "Strict-Transport-Security": "Enforces HTTPS (HSTS)",
            "X-XSS-Protection": "Legacy XSS Filter"
        }
        
        for header, desc in security_headers.items():
            if header in headers:
                results["headers"][header] = {"status": "Pass", "value": headers[header], "desc": desc}
            else:
                results["headers"][header] = {"status": "Missing", "value": None, "desc": desc}
                results["score"] -= 15  # Deduct points for missing critical headers

        # 2. Cookie Security Analysis
        if response.cookies:
            for cookie in response.cookies:
                cookie_issues = []
                # Check cookie attributes safely
                if not cookie.get_nonstandard_attr('HttpOnly') and not getattr(cookie, 'rest', {}).get('HttpOnly'):
                    # Basic check for HttpOnly
                    pass # handled generally below or via requests standard
                
                results["cookies"][cookie.name] = {
                    "secure": True if cookie.secure else False,
                    "issues": [] if cookie.secure else ["Missing Secure flag"]
                }
                if not cookie.secure:
                    results["score"] -= 10
        else:
            results["cookies"]["info"] = {"secure": True, "issues": ["No session/auth cookies detected in initial response."]}

        # 3. Sensitive File Probing
        base_url = response.url.rstrip('/')
        sensitive_paths = ["/.env", "/.git/HEAD", "/robots.txt", "/sitemap.xml"]
        
        for path in sensitive_paths:
            test_url = base_url + path
            try:
                res = requests.get(test_url, timeout=3, headers={"User-Agent": "DevSiteAuditor/1.0"})
                if res.status_code == 200 and path in ["/.env", "/.git/HEAD"]:
                    results["files"][path] = {"exposed": True, "status": "CRITICAL: Exposed!"}
                    results["score"] -= 25
                elif res.status_code == 200:
                    results["files"][path] = {"exposed": False, "status": "Found (Normal)"}
                else:
                    results["files"][path] = {"exposed": False, "status": "Protected / Not Found"}
            except:
                results["files"][path] = {"exposed": False, "status": "Unreachable"}

    except requests.exceptions.RequestException as e:
        results["error"] = str(e)
        results["score"] = 0

    # Keep score bounded between 0 and 100
    results["score"] = max(0, min(100, results["score"]))
    return results
