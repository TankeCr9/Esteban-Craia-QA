# 🧪 Esteban Gabriel Craia — QA Automation Portfolio

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=00D9FF&center=true&vCenter=true&width=600&lines=QA+Analyst+%7C+5%2B+Years+Experience;API+Testing+%7C+Selenium+%7C+Playwright;Banking+%7C+Insurtech+%7C+Healthtech;Manual+%26+Automation+Expert" alt="Typing SVG" />

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Esteban%20Craia-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/esteban-craia-446a47b5/)
[![Email](https://img.shields.io/badge/Email-esteban.craia%40gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:esteban.craia@gmail.com)
[![Location](https://img.shields.io/badge/Location-Rosario%2C%20Argentina-4CAF50?style=for-the-badge&logo=googlemaps&logoColor=white)](#)
[![English](https://img.shields.io/badge/English-C1%20Advanced-8A2BE2?style=for-the-badge&logo=duolingo&logoColor=white)](#)

</div>

---

## 📋 About This Repository

This portfolio showcases **real-world QA practices** across three automation frameworks, covering the complete testing lifecycle: manual test design, API validation, regression automation, and end-to-end testing.

> Built to demonstrate the skills I apply daily across Banking, Insurtech, and Healthtech projects.

---

## 📁 Repository Structure

```
qa-portfolio/
│
├── 📄 README.md                    ← You are here
├── 📬 postman_collection.json      ← REST API test suite (Postman)
├── 🐍 selenium_tests.py            ← UI automation (Selenium + Python + pytest)
└── 🎭 playwright_tests.spec.js     ← E2E + Integration testing (Playwright)
```

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| **API Testing** | Postman, SoapUI, Swagger |
| **UI Automation** | Selenium WebDriver (Python), Playwright (JS) |
| **Test Management** | Azure DevOps, Jira, HP Octane, MS TFS |
| **Languages** | Python, JavaScript/TypeScript (Roadmap), SQL |
| **Methodologies** | Agile (Scrum / Kanban) |
| **Databases** | SQL – complex queries & data validation |
| **CI/CD** | GitHub Actions compatible |

---

## 📬 1. Postman Collection — `postman_collection.json`

**Target API:** [JSONPlaceholder](https://jsonplaceholder.typicode.com) — public REST sandbox

### Test Cases

| ID | Method | Endpoint | Coverage |
|---|---|---|---|
| TC-PM-001 | `GET` | `/posts` | Status, schema, array length, headers |
| TC-PM-002 | `GET` | `/posts/{id}` | ID match, field types, response time |
| TC-PM-003 | `GET` | `/posts/99999` | **Negative** — 404 handling |
| TC-PM-004 | `POST` | `/posts` | 201 Created, body validation, variable capture |
| TC-PM-005 | `PUT` | `/posts/1` | Full replace, field persistence |
| TC-PM-006 | `PATCH` | `/posts/1` | Partial update, non-modified fields intact |
| TC-PM-007 | `DELETE` | `/posts/{id}` | 200 OK, empty body confirmed |
| TC-PM-008 | `GET` | `/users` | Schema + nested objects + email regex |
| TC-PM-009 | `GET` | `/posts?userId={id}` | Relational integrity |
| TC-PM-010 | `GET` | `/comments?postId={id}` | Email format, non-empty bodies |
| TC-PM-011 | `GET` | `/todos` | Boolean types, completed/pending counts |

### ▶️ How to Run — Postman

**Option A: Postman GUI**
1. Open Postman → **Import** → select `postman_collection.json`
2. Click the collection → **Run collection**
3. Review results in the Collection Runner

**Option B: Newman (CLI)**
```bash
# Install Newman
npm install -g newman newman-reporter-htmlextra

# Run with HTML report
newman run postman_collection.json \
  --reporters cli,htmlextra \
  --reporter-htmlextra-export reports/api-report.html
```

**Option C: VS Code**
- Install the **Postman** or **Thunder Client** VS Code extension
- Import `postman_collection.json` directly

---

## 🐍 2. Selenium Tests — `selenium_tests.py`

**Target:** [The Internet](https://the-internet.herokuapp.com) — Selenium practice site  
**Framework:** `pytest` + `selenium` + `webdriver-manager`

### Test Cases

| ID | Class | Scenario | Technique |
|---|---|---|---|
| TC-SE-001 | `TestLogin` | Valid login → redirect + flash | Explicit Wait, URL assertion |
| TC-SE-002 | `TestLogin` | Invalid login → error flash | **Negative test**, CSS locator |
| TC-SE-003 | `TestLogin` | Session persistence after navigation | Cookie/session validation |
| TC-SE-004 | `TestCheckboxes` | Toggle all checkboxes, assert state flip | State comparison before/after |
| TC-SE-005 | `TestDropdown` | Select option by visible text | `Select` class, initial state check |
| TC-SE-006 | `TestDynamicLoading` | Start → spinner disappears → content shows | Explicit Wait, `invisibility_of_element` |
| TC-SE-007 | `TestFileUpload` | Upload file via input, confirm filename | `send_keys` on file input |
| TC-SE-008 | `TestAlerts` | Accept JS alert, verify result | `alert_is_present`, `.accept()` |
| TC-SE-009 | `TestHoverActions` | Hover reveals hidden caption | `ActionChains`, visibility assertion |
| TC-SE-010 | `TestWindowHandling` | New window open, switch, validate, return | Window handle management |

### ▶️ How to Run — Selenium

**Prerequisites:**
```bash
pip install selenium pytest pytest-html webdriver-manager
```

**Run all tests:**
```bash
pytest selenium_tests.py -v
```

**Run with HTML report:**
```bash
pytest selenium_tests.py -v --html=reports/selenium-report.html --self-contained-html
```

**Run a single test class:**
```bash
pytest selenium_tests.py::TestLogin -v
```

**Run a single test:**
```bash
pytest selenium_tests.py::TestLogin::test_TC_SE_001_login_valid_credentials -v
```

> **Note:** Tests run in **headless Chrome** by default. Remove `--headless=new` from the options in the fixture to see the browser.

---

## 🎭 3. Playwright Tests — `playwright_tests.spec.js`

**E2E Target:** [The Internet](https://the-internet.herokuapp.com)  
**Integration Target:** [JSONPlaceholder](https://jsonplaceholder.typicode.com)  
**Framework:** `@playwright/test`

### E2E Test Cases

| ID | Suite | Scenario | Assertion Type |
|---|---|---|---|
| TC-PW-E2E-001 | Auth | Valid login flow | URL, flash text, heading |
| TC-PW-E2E-002 | Auth | Invalid credentials error state | Negative, CSS class check |
| TC-PW-E2E-003 | Auth | Logout → back to login | URL + flash message |
| TC-PW-E2E-004 | Interaction | Drag & Drop column swap | Position state comparison |
| TC-PW-E2E-005 | Interaction | Key press event capture | Keyboard API, text assertion |
| TC-PW-E2E-006 | Interaction | Table column structure | Header count & content |
| TC-PW-E2E-007 | Interaction | Checkbox state toggle | Checked state before/after |
| TC-PW-E2E-008 | Wait Strategy | Dynamic content lazy load | `toBeHidden` + `toBeVisible` with timeout |

### Integration Test Cases

| ID | Method | Endpoint | Coverage |
|---|---|---|---|
| TC-PW-INT-001 | `GET` | `/posts` | Schema, array length, types |
| TC-PW-INT-002 | `POST` | `/posts` | 201 Created, full body match |
| TC-PW-INT-003 | `PUT` | `/posts/1` | Full replace validation |
| TC-PW-INT-004 | `DELETE` | `/posts/1` | 200 + empty body |
| TC-PW-INT-005 | `GET` | `/posts?userId=1` | Relational integrity |
| TC-PW-INT-006 | `GET` | `/posts/99999` | **Negative** — 404 |
| TC-PW-INT-007 | `GET` | `/comments?postId=1` | Email regex + non-empty body |

### ▶️ How to Run — Playwright

**Prerequisites:**
```bash
npm install -D @playwright/test
npx playwright install chromium
```

**Run all tests:**
```bash
npx playwright test playwright_tests.spec.js
```

**Run with HTML report (opens in browser):**
```bash
npx playwright test playwright_tests.spec.js --reporter=html
npx playwright show-report
```

**Run only E2E tests:**
```bash
npx playwright test playwright_tests.spec.js --grep "E2E"
```

**Run only Integration tests:**
```bash
npx playwright test playwright_tests.spec.js --grep "Integration"
```

**Run headed (with browser visible):**
```bash
npx playwright test playwright_tests.spec.js --headed
```

---

## 🚀 Setup Guide — GitHub & Local (VS Code)

### Step 1 — Clone or Fork the Repository

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/qa-portfolio.git
cd qa-portfolio
```

### Step 2 — Local Setup (VS Code)

1. **Open VS Code** → `File → Open Folder` → select `qa-portfolio`
2. Install recommended extensions:
   - `Python` (Microsoft)
   - `Playwright Test for VS Code` (Microsoft)
   - `Postman` or `Thunder Client`

### Step 3 — Python Environment (Selenium)

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install selenium pytest pytest-html webdriver-manager

# Run tests
pytest selenium_tests.py -v
```

### Step 4 — Node Environment (Playwright)

```bash
npm init -y
npm install -D @playwright/test
npx playwright install chromium

npx playwright test playwright_tests.spec.js --reporter=html
```

### Step 5 — Upload to GitHub

```bash
git init
git add .
git commit -m "feat: initial QA portfolio – Esteban Craia"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/qa-portfolio.git
git push -u origin main
```

### Step 6 — Enable GitHub Pages (for the HTML portfolio page)

1. Go to your repo → **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` / folder: `/ (root)`
4. Save — your site will be at `https://YOUR_USERNAME.github.io/qa-portfolio/`

---

## 📊 Professional Experience Summary

```
5+ years │ QA Analyst & Technical Lead
─────────────────────────────────────────────────────────
Signaris Inc.   │ 2024–Present │ Banking / Wire Transfers
Wigou S.A.      │ 2022–2023   │ Insurtech / GuideWire Migration
Doc 24          │ 2021–2022   │ Healthtech / Telemedicine
Holistor S.A.   │ 2020–2021   │ ERP / Retail Systems
─────────────────────────────────────────────────────────
• API Testing expert: Postman, SoapUI, Swagger
• Test management: Azure DevOps, Jira, Octane, TFS
• Co-Lead experience in Agile/Scrum teams
• English C1 (Advanced)
```

---

## 📜 Certifications

| Certification | Issuer |
|---|---|
| Selenium in Java | Udemy |
| API Testing Expert | Postman |
| Scrum Foundations | CertiPROF |
| Advanced English C1 | Mayflower Center |
| A.S. in Computer Programming *(In Progress)* | UTN |

---

## 📬 Contact

| Channel | Link |
|---|---|
| 📧 Email | [esteban.craia@gmail.com](mailto:esteban.craia@gmail.com) |
| 💼 LinkedIn | [linkedin.com/in/esteban-craia-446a47b5](https://www.linkedin.com/in/esteban-craia-446a47b5/) |
| 📍 Location | Rosario, Argentina |
| 📱 Phone | +54 3471-15673176 |

---

<div align="center">

*Built with precision. Tested with purpose.*  
**Esteban Gabriel Craia — QA Analyst**

</div>
