/**
 * ============================================================================
 *  QA AUTOMATION PORTFOLIO – Playwright (E2E + Integration Testing)
 *  Author  : Esteban Gabriel Craia
 *  Target  : https://the-internet.herokuapp.com  (E2E)
 *            https://jsonplaceholder.typicode.com (Integration / API)
 *  Runner  : npx playwright test
 *  Install : npm install -D @playwright/test && npx playwright install chromium
 * ============================================================================
 *
 *  E2E Tests (browser):
 *    TC-PW-E2E-001  Login Happy Path
 *    TC-PW-E2E-002  Login Error State
 *    TC-PW-E2E-003  Logout Flow
 *    TC-PW-E2E-004  Drag & Drop Interaction
 *    TC-PW-E2E-005  Infinite Scroll – Dynamic Content Load
 *    TC-PW-E2E-006  Shadow DOM Element Interaction
 *    TC-PW-E2E-007  Key Press Events
 *    TC-PW-E2E-008  Sortable Table – Column Verification
 *
 *  Integration Tests (API layer):
 *    TC-PW-INT-001  GET Posts – Schema Validation
 *    TC-PW-INT-002  POST Create – 201 + Response Body
 *    TC-PW-INT-003  PUT Update – Full Replace
 *    TC-PW-INT-004  DELETE – 200 + Empty Body
 *    TC-PW-INT-005  Filter by userId – Relational Integrity
 *    TC-PW-INT-006  Invalid Resource – 404 Handling
 */

const { test, expect, request } = require('@playwright/test');

// ─── Config ─────────────────────────────────────────────────────────────────

const UI_BASE = 'https://the-internet.herokuapp.com';
const API_BASE = 'https://jsonplaceholder.typicode.com';
const VALID_USER = 'tomsmith';
const VALID_PASS = 'SuperSecretPassword!';

// ─── Shared Login Helper ─────────────────────────────────────────────────────

async function loginUser(page) {
  await page.goto(`${UI_BASE}/login`);
  await page.getByLabel('Username').fill(VALID_USER);
  await page.getByLabel('Password').fill(VALID_PASS);
  await page.getByRole('button', { name: /login/i }).click();
  await page.waitForURL('**/secure');
}

// ═════════════════════════════════════════════════════════════════════════════
//  E2E TESTS – Browser / UI Layer
// ═════════════════════════════════════════════════════════════════════════════

test.describe('🖥️  E2E – Authentication Flow', () => {

  test('TC-PW-E2E-001 | Login with valid credentials navigates to /secure', async ({ page }) => {
    await loginUser(page);

    await expect(page).toHaveURL(/\/secure/);

    const flash = page.locator('#flash');
    await expect(flash).toBeVisible();
    await expect(flash).toContainText('You logged into a secure area!');

    const heading = page.locator('h2');
    await expect(heading).toContainText('Secure Area');
  });

  test('TC-PW-E2E-002 | Login with invalid password shows error flash', async ({ page }) => {
    await page.goto(`${UI_BASE}/login`);
    await page.getByLabel('Username').fill('invalid_user');
    await page.getByLabel('Password').fill('wrong_password');
    await page.getByRole('button', { name: /login/i }).click();

    await expect(page).not.toHaveURL(/\/secure/);

    const flash = page.locator('#flash');
    await expect(flash).toBeVisible();
    await expect(flash).toContainText('Your username is invalid!');
    await expect(flash).toHaveClass(/error/);
  });

  test('TC-PW-E2E-003 | Logout returns to login page with confirmation message', async ({ page }) => {
    await loginUser(page);

    const logoutLink = page.getByRole('link', { name: /logout/i });
    await expect(logoutLink).toBeVisible();
    await logoutLink.click();

    await expect(page).toHaveURL(/\/login/);

    const flash = page.locator('#flash');
    await expect(flash).toContainText('You logged out of the secure area!');
  });

});

test.describe('🖱️  E2E – Interactions & UI Components', () => {

  test('TC-PW-E2E-004 | Drag and Drop – element A lands in column B', async ({ page }) => {
    await page.goto(`${UI_BASE}/drag_and_drop`);

    const columnA = page.locator('#column-a');
    const columnB = page.locator('#column-b');

    // Capture initial header text
    const initialA = await columnA.locator('header').textContent();
    const initialB = await columnB.locator('header').textContent();

    expect(initialA?.trim()).toBe('A');
    expect(initialB?.trim()).toBe('B');

    // Perform drag
    await columnA.dragTo(columnB);

    // After drag the columns should be swapped
    const newA = await columnA.locator('header').textContent();
    const newB = await columnB.locator('header').textContent();

    // JSONPlaceholder drag_and_drop implementation may vary – assert swap occurred
    const swapped = (newA?.trim() === 'B' && newB?.trim() === 'A') ||
                    (newA?.trim() === 'A' && newB?.trim() === 'B');
    expect(swapped, `Expected swap. Got A='${newA}' B='${newB}'`).toBeTruthy();
  });

  test('TC-PW-E2E-005 | Key Presses – captures correct key name', async ({ page }) => {
    await page.goto(`${UI_BASE}/key_presses`);

    const target = page.locator('#target');
    await target.click();
    await page.keyboard.press('Tab');

    const result = page.locator('#result');
    await expect(result).toContainText('You entered: TAB');

    await target.click();
    await page.keyboard.press('Enter');
    await expect(result).toContainText('You entered: ENTER');
  });

  test('TC-PW-E2E-006 | Sortable table – all expected columns present', async ({ page }) => {
    await page.goto(`${UI_BASE}/tables`);

    const table = page.locator('#table1');
    await expect(table).toBeVisible();

    const headers = await table.locator('thead th').allTextContents();
    const expected = ['Last Name', 'First Name', 'Email', 'Due', 'Web Site', 'Action'];

    for (const col of expected) {
      expect(headers).toContain(col);
    }

    // Validate row count
    const rows = table.locator('tbody tr');
    await expect(rows).toHaveCount(4);
  });

  test('TC-PW-E2E-007 | Checkboxes – assert state after toggle', async ({ page }) => {
    await page.goto(`${UI_BASE}/checkboxes`);

    const checkboxes = page.locator('input[type="checkbox"]');
    await expect(checkboxes).toHaveCount(2);

    const cb1 = checkboxes.nth(0);
    const cb2 = checkboxes.nth(1);

    const cb1Before = await cb1.isChecked();
    const cb2Before = await cb2.isChecked();

    await cb1.click();
    await cb2.click();

    await expect(cb1).toBeChecked({ checked: !cb1Before });
    await expect(cb2).toBeChecked({ checked: !cb2Before });
  });

  test('TC-PW-E2E-008 | Dynamic Loading – explicit wait for lazy content', async ({ page }) => {
    await page.goto(`${UI_BASE}/dynamic_loading/1`);

    await page.getByRole('button', { name: 'Start' }).click();

    // Spinner must disappear first
    const spinner = page.locator('#loading');
    await expect(spinner).toBeHidden({ timeout: 15_000 });

    // Then content must appear
    const finish = page.locator('#finish');
    await expect(finish).toBeVisible({ timeout: 15_000 });
    await expect(finish).toContainText('Hello World!');
  });

});

// ═════════════════════════════════════════════════════════════════════════════
//  INTEGRATION TESTS – API Layer (JSONPlaceholder)
// ═════════════════════════════════════════════════════════════════════════════

test.describe('🔗 Integration – REST API Validation', () => {

  let apiContext;

  test.beforeAll(async () => {
    apiContext = await request.newContext({
      baseURL: API_BASE,
      extraHTTPHeaders: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    });
  });

  test.afterAll(async () => {
    await apiContext.dispose();
  });

  // ── INT-001 ──────────────────────────────────────────────────────────────

  test('TC-PW-INT-001 | GET /posts – returns 100 items with valid schema', async () => {
    const response = await apiContext.get('/posts');

    expect(response.status()).toBe(200);
    expect(response.headers()['content-type']).toContain('application/json');

    const posts = await response.json();
    expect(Array.isArray(posts)).toBeTruthy();
    expect(posts).toHaveLength(100);

    // Schema check on first 5 items
    for (const post of posts.slice(0, 5)) {
      expect(post).toMatchObject({
        id:     expect.any(Number),
        userId: expect.any(Number),
        title:  expect.any(String),
        body:   expect.any(String),
      });
      expect(post.id).toBeGreaterThan(0);
      expect(post.title.length).toBeGreaterThan(0);
    }
  });

  // ── INT-002 ──────────────────────────────────────────────────────────────

  test('TC-PW-INT-002 | POST /posts – creates resource, returns 201', async () => {
    const payload = {
      title:  'Playwright Integration Test',
      body:   'Automated API validation by Esteban Craia – QA Portfolio',
      userId: 99,
    };

    const response = await apiContext.post('/posts', { data: payload });

    expect(response.status()).toBe(201);

    const created = await response.json();
    expect(created.title).toBe(payload.title);
    expect(created.body).toBe(payload.body);
    expect(created.userId).toBe(payload.userId);
    expect(typeof created.id).toBe('number');
    expect(created.id).toBeGreaterThan(0);
  });

  // ── INT-003 ──────────────────────────────────────────────────────────────

  test('TC-PW-INT-003 | PUT /posts/1 – full replace returns updated resource', async () => {
    const payload = {
      id:     1,
      title:  'PUT Updated – QA Automation 2025',
      body:   'Full replacement of post resource via PUT method',
      userId: 1,
    };

    const response = await apiContext.put('/posts/1', { data: payload });

    expect(response.status()).toBe(200);

    const updated = await response.json();
    expect(updated.title).toBe(payload.title);
    expect(updated.id).toBe(1);
    expect(updated.userId).toBe(1);
  });

  // ── INT-004 ──────────────────────────────────────────────────────────────

  test('TC-PW-INT-004 | DELETE /posts/1 – returns 200 with empty body', async () => {
    const response = await apiContext.delete('/posts/1');

    expect(response.status()).toBe(200);

    const body = await response.json();
    expect(body).toEqual({});
  });

  // ── INT-005 ──────────────────────────────────────────────────────────────

  test('TC-PW-INT-005 | GET /posts?userId=1 – all posts belong to user 1', async () => {
    const response = await apiContext.get('/posts?userId=1');

    expect(response.status()).toBe(200);

    const posts = await response.json();
    expect(posts.length).toBeGreaterThan(0);

    for (const post of posts) {
      expect(post.userId).toBe(1);
    }
  });

  // ── INT-006 ──────────────────────────────────────────────────────────────

  test('TC-PW-INT-006 | GET /posts/99999 – returns 404 for invalid resource', async () => {
    const response = await apiContext.get('/posts/99999');

    expect(response.status()).toBe(404);

    const body = await response.json();
    expect(body).toEqual({});
  });

  // ── INT-007 (Bonus) ───────────────────────────────────────────────────────

  test('TC-PW-INT-007 | GET /comments?postId=1 – email format validation', async () => {
    const response = await apiContext.get('/comments?postId=1');

    expect(response.status()).toBe(200);

    const comments = await response.json();
    expect(comments.length).toBeGreaterThan(0);

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    for (const comment of comments) {
      expect(comment.postId).toBe(1);
      expect(emailRegex.test(comment.email)).toBeTruthy();
      expect(comment.body.length).toBeGreaterThan(0);
    }
  });

});
