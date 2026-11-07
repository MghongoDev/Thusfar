-- 001_create_orders.sql
-- Creates the orders table (Postgres, per D-001).
-- All timestamps are stored in UTC (per D-004): columns are timestamptz,
-- timestamptz stores an absolute instant, and the session is pinned to UTC.
-- Plain SQL, no extensions or new dependencies.

BEGIN;

SET LOCAL TIME ZONE 'UTC';

CREATE TABLE orders (
    id             BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id    BIGINT        NOT NULL,
    status         TEXT          NOT NULL DEFAULT 'pending'
                   CHECK (status IN ('pending', 'paid', 'shipped', 'cancelled', 'refunded')),
    total_cents    BIGINT        NOT NULL CHECK (total_cents >= 0),
    currency       CHAR(3)       NOT NULL DEFAULT 'USD',
    placed_at      TIMESTAMPTZ   NOT NULL DEFAULT now(),
    created_at     TIMESTAMPTZ   NOT NULL DEFAULT now(),
    updated_at     TIMESTAMPTZ   NOT NULL DEFAULT now()
);

CREATE INDEX orders_customer_id_idx ON orders (customer_id);
CREATE INDEX orders_status_placed_at_idx ON orders (status, placed_at);

COMMENT ON COLUMN orders.placed_at  IS 'UTC (D-004)';
COMMENT ON COLUMN orders.created_at IS 'UTC (D-004)';
COMMENT ON COLUMN orders.updated_at IS 'UTC (D-004)';

COMMIT;

-- Down:
-- DROP TABLE IF EXISTS orders;
