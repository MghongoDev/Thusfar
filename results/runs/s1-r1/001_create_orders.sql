-- Migration 001: create orders table (PostgreSQL)
-- D-001: Postgres. D-003: plain SQL, no migration tool or extension added.
-- D-004: all timestamps are timestamptz, and the session is pinned to UTC.

BEGIN;

SET LOCAL TIME ZONE 'UTC';

CREATE TABLE orders (
    id            bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id   bigint        NOT NULL,
    status        text          NOT NULL DEFAULT 'pending'
                  CHECK (status IN ('pending', 'paid', 'shipped', 'delivered', 'cancelled')),
    total_cents   bigint        NOT NULL DEFAULT 0 CHECK (total_cents >= 0),
    currency      char(3)       NOT NULL DEFAULT 'USD',
    created_at    timestamptz   NOT NULL DEFAULT now(),
    updated_at    timestamptz   NOT NULL DEFAULT now()
);

CREATE INDEX orders_customer_id_idx ON orders (customer_id);
CREATE INDEX orders_status_created_at_idx ON orders (status, created_at);

COMMENT ON COLUMN orders.created_at IS 'UTC (D-004)';
COMMENT ON COLUMN orders.updated_at IS 'UTC (D-004)';

COMMIT;

-- Down:
-- DROP TABLE IF EXISTS orders;
