## flag

MOCSCTF{interactivebrokers}

## 解題步驟

1. From wattergor's Threads post, you observed he mentions two keywords (opmocsctf2025 and phish)

2. Figure out the post is on his twitter by searching either "#Macau #phishing" or "MOCSCTF"
https://x.com/watttttp070501/

3. There is a post about phishing SMS analysis. From the domain patten, you can split MO and IKBR.
https://x.com/watttttp070501/status/1934263339238269395

4. Find the related SMS message by seaching IKBR phishing. Then identify the brand name.
https://blog.darklab.hk/2025/06/06/lurking-behind-the-scenes-keylogger-sites-impersonate-trusted-brokerage-firms-for-account-takeover/

5. The flag is MOCSCTF{interactivebrokers}