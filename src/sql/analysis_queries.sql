-- Energy consumption by customer type and city
SELECT 
    customer_type,
    city,
    COUNT(DISTINCT customer_id) as customer_count,
    SUM(total_energy_purchased) as total_energy,
    AVG(avg_price_per_kwh) as avg_price,
    SUM(total_spent) as total_revenue
FROM 
    customer_analysis
GROUP BY 
    customer_type,
    city
ORDER BY 
    total_revenue DESC;

-- Provider performance analysis
SELECT 
    p.region,
    p.energy_type,
    COUNT(DISTINCT p.provider_id) as provider_count,
    SUM(p.capacity_mw) as total_capacity,
    SUM(p.total_energy_sold) as total_energy_sold,
    SUM(p.total_energy_bought) as total_energy_bought,
    AVG(p.avg_price_per_kwh) as avg_price
FROM 
    provider_analysis p
GROUP BY 
    p.region,
    p.energy_type
ORDER BY 
    total_energy_sold DESC;

-- Monthly energy price trends
SELECT 
    energy_type,
    month,
    transaction_type,
    total_energy,
    avg_price,
    transaction_count,
    total_energy / transaction_count as avg_transaction_size
FROM 
    energy_type_analysis
WHERE 
    month >= DATE_ADD('month', -12, CURRENT_DATE)
ORDER BY 
    month DESC,
    energy_type;

-- Customer segmentation by consumption
WITH customer_segments AS (
    SELECT 
        customer_id,
        customer_type,
        total_energy_purchased,
        NTILE(4) OVER (PARTITION BY customer_type ORDER BY total_energy_purchased) as consumption_quartile
    FROM 
        customer_analysis
    WHERE 
        total_energy_purchased > 0
)
SELECT 
    customer_type,
    consumption_quartile,
    COUNT(*) as customer_count,
    MIN(total_energy_purchased) as min_energy,
    MAX(total_energy_purchased) as max_energy,
    AVG(total_energy_purchased) as avg_energy
FROM 
    customer_segments
GROUP BY 
    customer_type,
    consumption_quartile
ORDER BY 
    customer_type,
    consumption_quartile; 