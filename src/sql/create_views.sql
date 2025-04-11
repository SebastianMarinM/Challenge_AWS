-- View for provider analysis
CREATE OR REPLACE VIEW provider_analysis AS
SELECT 
    p.provider_id,
    p.provider_name,
    p.energy_type,
    p.capacity_mw,
    p.region,
    COUNT(t.transaction_id) as total_transactions,
    SUM(CASE WHEN t.transaction_type = 'sell' THEN t.quantity_kwh ELSE 0 END) as total_energy_sold,
    SUM(CASE WHEN t.transaction_type = 'buy' THEN t.quantity_kwh ELSE 0 END) as total_energy_bought,
    AVG(t.price_per_kwh) as avg_price_per_kwh
FROM 
    providers p
LEFT JOIN 
    transactions t ON p.provider_id = t.entity_id
GROUP BY 
    p.provider_id,
    p.provider_name,
    p.energy_type,
    p.capacity_mw,
    p.region;

-- View for customer analysis
CREATE OR REPLACE VIEW customer_analysis AS
SELECT 
    c.customer_id,
    c.customer_name,
    c.customer_type,
    c.city,
    COUNT(t.transaction_id) as total_transactions,
    SUM(t.quantity_kwh) as total_energy_purchased,
    AVG(t.price_per_kwh) as avg_price_per_kwh,
    SUM(t.total_amount) as total_spent
FROM 
    customers c
LEFT JOIN 
    transactions t ON c.customer_id = t.entity_id AND t.transaction_type = 'sell'
GROUP BY 
    c.customer_id,
    c.customer_name,
    c.customer_type,
    c.city;

-- View for energy type analysis
CREATE OR REPLACE VIEW energy_type_analysis AS
SELECT 
    t.energy_type,
    t.transaction_type,
    DATE_TRUNC('month', t.transaction_date) as month,
    COUNT(*) as transaction_count,
    SUM(t.quantity_kwh) as total_energy,
    AVG(t.price_per_kwh) as avg_price,
    MIN(t.price_per_kwh) as min_price,
    MAX(t.price_per_kwh) as max_price
FROM 
    transactions t
GROUP BY 
    t.energy_type,
    t.transaction_type,
    DATE_TRUNC('month', t.transaction_date); 