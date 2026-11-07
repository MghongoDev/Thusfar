-- 001_create_orders.sql
-- Creates the orders table (Postgres, per D-010).
-- Timestamps are timestamptz, which Postgres stores in UTC (per D-004).

BEGIN;

CREATE TABLE orders (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id  BIGINT        NOT NULL,
    status       TEXT          NOT NULL DEFAULT 'pending'
                 CHECK (status IN ('pending', 'paid', 'shipped', 'delivered', 'cancelled')),
    total_cents  BIGINT        NOT NULL CHECK (total_cents >= 0),
    currency     CHAR(3)       NOT NULL DEFAULT 'USD',
    created_at   TIMESTAMPTZ   NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ   NOT NULL DEFAULT now()
);

CREATE INDEX orders_customer_id_idx ON orders (customer_id);
CREATE INDEX orders_status_idx      ON orders (status);
CREATE INDEX orders_created_at_idx  ON orders (created_at);

COMMIT;

-- Down migration:
-- DROP TABLE IF EXISTS orders;
