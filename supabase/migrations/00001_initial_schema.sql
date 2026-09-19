-- Cocoyo API - schéma initial (catalogue, clients, commandes)
-- Appliquer via Supabase SQL Editor ou `supabase db push`

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TYPE payment_status AS ENUM ('unpaid', 'deposit', 'paid');
CREATE TYPE delivery_status AS ENUM ('not_delivered', 'shipping', 'delivered');

CREATE TABLE clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    contact TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_clients_name ON clients (name);

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    sizes JSONB NOT NULL DEFAULT '[]'::jsonb,
    unit_price NUMERIC(12, 2) NOT NULL CHECK (unit_price >= 0),
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_products_active ON products (is_active);

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL REFERENCES clients (id) ON DELETE RESTRICT,
    ordered_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    payment_status payment_status NOT NULL DEFAULT 'unpaid',
    delivery_status delivery_status NOT NULL DEFAULT 'not_delivered',
    total_amount NUMERIC(12, 2) NOT NULL DEFAULT 0 CHECK (total_amount >= 0),
    deposit_amount NUMERIC(12, 2) NOT NULL DEFAULT 0 CHECK (deposit_amount >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_orders_client ON orders (client_id);
CREATE INDEX idx_orders_payment ON orders (payment_status);
CREATE INDEX idx_orders_delivery ON orders (delivery_status);

CREATE TABLE order_lines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders (id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products (id) ON DELETE RESTRICT,
    size TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12, 2) NOT NULL CHECK (unit_price >= 0),
    UNIQUE (order_id, product_id, size)
);

CREATE INDEX idx_order_lines_order ON order_lines (order_id);

-- RLS : back-office mono-marque, tout utilisateur authentifié
ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE order_lines ENABLE ROW LEVEL SECURITY;

CREATE POLICY clients_authenticated_all ON clients
    FOR ALL TO authenticated USING (true) WITH CHECK (true);

CREATE POLICY products_authenticated_all ON products
    FOR ALL TO authenticated USING (true) WITH CHECK (true);

CREATE POLICY orders_authenticated_all ON orders
    FOR ALL TO authenticated USING (true) WITH CHECK (true);

CREATE POLICY order_lines_authenticated_all ON order_lines
    FOR ALL TO authenticated USING (true) WITH CHECK (true);
