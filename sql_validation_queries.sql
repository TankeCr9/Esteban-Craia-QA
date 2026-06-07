-- ============================================================
--  QA PORTFOLIO – SQL Data Validation Queries
--  Author  : Esteban Gabriel Craia
--  Purpose : Demonstrate real-world SQL skills used in QA
--            for data validation, defect investigation,
--            and regression verification across projects.
--  Engine  : Standard SQL (compatible with PostgreSQL / MySQL
--            / SQL Server / Oracle with minor adjustments)
-- ============================================================

-- ┌─────────────────────────────────────────────────────────┐
-- │  SECTION 1 – DATA INTEGRITY CHECKS                     │
-- │  Used after deployments to verify no data was lost      │
-- │  or corrupted during migrations / releases.             │
-- └─────────────────────────────────────────────────────────┘

-- TC-SQL-001
-- Verify no NULLs exist in mandatory fields after a migration.
-- Real use case: Holistor ERP migration – Sales module.
SELECT
    id,
    client_name,
    order_date,
    total_amount,
    status
FROM orders
WHERE
    client_name  IS NULL
 OR order_date   IS NULL
 OR total_amount IS NULL
 OR status       IS NULL;
-- Expected: 0 rows. Any result = data integrity defect.


-- TC-SQL-002
-- Detect duplicate records that should be unique.
-- Real use case: Signaris wire transfer – prevent duplicate transaction IDs.
SELECT
    transaction_id,
    COUNT(*) AS occurrences
FROM wire_transfers
GROUP BY transaction_id
HAVING COUNT(*) > 1
ORDER BY occurrences DESC;
-- Expected: 0 rows. Duplicates = critical defect in financial systems.


-- TC-SQL-003
-- Check orphaned records (referential integrity violation).
-- Real use case: GuideWire migration – policy claims without a parent policy.
SELECT
    c.claim_id,
    c.policy_id,
    c.claim_date,
    c.amount
FROM claims c
LEFT JOIN policies p ON c.policy_id = p.policy_id
WHERE p.policy_id IS NULL;
-- Expected: 0 rows. Orphaned claims = broken FK constraint after migration.


-- TC-SQL-004
-- Verify row counts before and after migration match.
-- Pattern used in every migration project (Holistor, Wigou).
SELECT
    'orders_legacy'   AS source_table,
    COUNT(*)          AS total_rows
FROM orders_legacy
UNION ALL
SELECT
    'orders_migrated',
    COUNT(*)
FROM orders_migrated;
-- Compare both counts. Difference = missing or extra records.


-- ┌─────────────────────────────────────────────────────────┐
-- │  SECTION 2 – BUSINESS LOGIC VALIDATION                 │
-- │  Verifying that app logic is reflected correctly        │
-- │  in the database after processing.                      │
-- └─────────────────────────────────────────────────────────┘

-- TC-SQL-005
-- Validate wire transfer amounts match expected totals.
-- Real use case: Signaris – Intermex Direct reconciliation.
SELECT
    batch_id,
    SUM(amount)           AS db_total,
    expected_batch_total,
    SUM(amount) - expected_batch_total AS discrepancy
FROM wire_transfers wt
JOIN batch_control bc USING (batch_id)
GROUP BY batch_id, expected_batch_total
HAVING ABS(SUM(amount) - expected_batch_total) > 0.01;
-- Expected: 0 rows. Any discrepancy over $0.01 = financial defect.


-- TC-SQL-006
-- Verify insurance premium calculation is within tolerance.
-- Real use case: Wigou – GuideWire policy migration validation.
SELECT
    policy_id,
    calculated_premium,
    expected_premium,
    ABS(calculated_premium - expected_premium) AS delta,
    CASE
        WHEN ABS(calculated_premium - expected_premium) <= 0.50 THEN 'PASS'
        ELSE 'FAIL – investigate'
    END AS validation_result
FROM policy_premiums
ORDER BY delta DESC;


-- TC-SQL-007
-- Confirm all completed orders have an associated invoice.
-- Real use case: Holistor – ERP Sales module post-migration.
SELECT
    o.order_id,
    o.status,
    o.completed_at,
    i.invoice_id
FROM orders o
LEFT JOIN invoices i ON o.order_id = i.order_id
WHERE o.status = 'COMPLETED'
  AND i.invoice_id IS NULL;
-- Expected: 0 rows. A completed order with no invoice = business logic bug.


-- TC-SQL-008
-- Check appointment status transitions are valid.
-- Real use case: Doc 24 – telemedicine platform.
-- Valid flow: SCHEDULED → IN_PROGRESS → COMPLETED (or CANCELLED)
SELECT
    appointment_id,
    patient_id,
    previous_status,
    current_status,
    changed_at
FROM appointment_audit
WHERE (previous_status = 'COMPLETED'  AND current_status = 'IN_PROGRESS')
   OR (previous_status = 'CANCELLED'  AND current_status NOT IN ('SCHEDULED','CANCELLED'))
   OR (previous_status = 'IN_PROGRESS' AND current_status = 'SCHEDULED')
ORDER BY changed_at DESC;
-- Expected: 0 rows. Any result = invalid state machine transition = defect.


-- ┌─────────────────────────────────────────────────────────┐
-- │  SECTION 3 – REGRESSION VERIFICATION QUERIES           │
-- │  Run after each release to confirm previous bugs        │
-- │  have not re-appeared.                                  │
-- └─────────────────────────────────────────────────────────┘

-- TC-SQL-009
-- Regression: Verify the "zero-amount transfer" bug is fixed.
-- Bug history: BUG-2341 – system allowed $0.00 wire transfers.
SELECT
    transaction_id,
    amount,
    created_at,
    created_by
FROM wire_transfers
WHERE amount <= 0;
-- Expected: 0 rows. Any result = regression of BUG-2341.


-- TC-SQL-010
-- Regression: Ensure deleted users cannot have active sessions.
-- Bug history: BUG-1892 – soft-deleted users retained active tokens.
SELECT
    u.user_id,
    u.username,
    u.deleted_at,
    s.session_token,
    s.expires_at
FROM users u
JOIN sessions s ON u.user_id = s.user_id
WHERE u.deleted_at IS NOT NULL
  AND s.expires_at > NOW();
-- Expected: 0 rows. Any active session for a deleted user = security bug.


-- TC-SQL-011
-- Regression: Confirm stock cannot go negative (BUG-0774).
-- Real use case: Holistor – stock module.
SELECT
    product_id,
    product_name,
    current_stock,
    warehouse_id
FROM inventory
WHERE current_stock < 0
ORDER BY current_stock ASC;
-- Expected: 0 rows. Negative stock = inventory logic regression.


-- ┌─────────────────────────────────────────────────────────┐
-- │  SECTION 4 – TEST DATA MANAGEMENT                      │
-- │  Scripts for setting up and tearing down test data      │
-- │  in QA / staging environments.                          │
-- └─────────────────────────────────────────────────────────┘

-- TC-SQL-012
-- Create a controlled test user for automation suites.
-- Run in QA / staging only — never in production.
INSERT INTO users (
    user_id,
    username,
    email,
    role,
    status,
    created_at
)
VALUES (
    'test-auto-001',
    'qa_automation_user',
    'qa.automation@testenv.com',
    'standard',
    'ACTIVE',
    NOW()
)
ON CONFLICT (user_id) DO NOTHING;
-- Idempotent: safe to run multiple times without duplicating data.


-- TC-SQL-013
-- Seed a complete test scenario: user + policy + claim.
-- Real use case: Wigou – GuideWire end-to-end test setup.
BEGIN;

    INSERT INTO policies (policy_id, holder_name, product_code, start_date, end_date, premium)
    VALUES ('POL-TEST-9999', 'QA Test Holder', 'AUTO-STD', CURRENT_DATE, CURRENT_DATE + INTERVAL '1 year', 1500.00);

    INSERT INTO claims (claim_id, policy_id, claim_date, amount, status)
    VALUES ('CLM-TEST-9999', 'POL-TEST-9999', CURRENT_DATE, 500.00, 'OPEN');

COMMIT;


-- TC-SQL-014
-- Teardown: remove all test data created by automation.
-- Always run at the end of test suites in QA environments.
BEGIN;

    DELETE FROM claims   WHERE claim_id  LIKE 'CLM-TEST-%';
    DELETE FROM policies WHERE policy_id LIKE 'POL-TEST-%';
    DELETE FROM users    WHERE user_id   LIKE 'test-auto-%';
    DELETE FROM sessions WHERE user_id   LIKE 'test-auto-%';

COMMIT;
-- Keeps the QA database clean between test runs.


-- ┌─────────────────────────────────────────────────────────┐
-- │  SECTION 5 – REPORTING & METRICS QUERIES               │
-- │  For generating QA reports and tracking defect trends.  │
-- └─────────────────────────────────────────────────────────┘

-- TC-SQL-015
-- Defect distribution by severity and status.
-- Used for sprint QA reports in Azure DevOps / Jira exports.
SELECT
    severity,
    status,
    COUNT(*) AS total,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY severity), 1) AS pct_of_severity
FROM defects
WHERE project_id = 'INTERMEX-2024'
GROUP BY severity, status
ORDER BY
    CASE severity WHEN 'CRITICAL' THEN 1 WHEN 'HIGH' THEN 2 WHEN 'MEDIUM' THEN 3 ELSE 4 END,
    status;


-- TC-SQL-016
-- Test execution summary: pass rate per test cycle.
SELECT
    cycle_name,
    COUNT(*)                                             AS total_cases,
    SUM(CASE WHEN result = 'PASS'   THEN 1 ELSE 0 END) AS passed,
    SUM(CASE WHEN result = 'FAIL'   THEN 1 ELSE 0 END) AS failed,
    SUM(CASE WHEN result = 'BLOCK'  THEN 1 ELSE 0 END) AS blocked,
    ROUND(
        SUM(CASE WHEN result = 'PASS' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1
    )                                                    AS pass_rate_pct
FROM test_executions
GROUP BY cycle_name
ORDER BY cycle_name;


-- TC-SQL-017
-- Top 10 most re-opened defects (stability indicator).
SELECT
    defect_id,
    title,
    reopen_count,
    assigned_to,
    last_reopen_date
FROM defects
WHERE reopen_count > 0
ORDER BY reopen_count DESC
LIMIT 10;
-- High reopen count = unstable fix or missing regression coverage.


-- TC-SQL-018
-- Average time to resolve defects by priority (SLA tracking).
SELECT
    priority,
    COUNT(*)                                                    AS total_resolved,
    ROUND(AVG(EXTRACT(EPOCH FROM (resolved_at - created_at)) / 3600), 1) AS avg_hours_to_resolve,
    ROUND(MIN(EXTRACT(EPOCH FROM (resolved_at - created_at)) / 3600), 1) AS min_hours,
    ROUND(MAX(EXTRACT(EPOCH FROM (resolved_at - created_at)) / 3600), 1) AS max_hours
FROM defects
WHERE status = 'RESOLVED'
  AND resolved_at IS NOT NULL
GROUP BY priority
ORDER BY
    CASE priority WHEN 'P1' THEN 1 WHEN 'P2' THEN 2 WHEN 'P3' THEN 3 ELSE 4 END;
