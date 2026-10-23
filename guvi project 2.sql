-- Total number of orders
SELECT COUNT(*) AS total_orders
FROM food_orders;

-- City-wise orders
SELECT City, COUNT(*) AS total_orders
FROM food_orders
GROUP BY City
ORDER BY total_orders DESC;

-- Average order value
SELECT AVG(Order_Value) AS average_order_value
FROM food_orders;

-- Most popular cuisine
SELECT Cuisine_Type, COUNT(*) AS order_count
FROM food_orders
GROUP BY Cuisine_Type
ORDER BY order_count DESC
LIMIT 1;

-- Average delivery time by city
SELECT
    City,
    AVG(Delivery_Time_Min) AS average_delivery_time
FROM food_orders
GROUP BY City
ORDER BY average_delivery_time;



-- Analyst Tasks (EDA & Analytics)
-- Customer & Order Analysis
-- 1.Identify top-spending customers
SELECT
    Customer_ID,
    ROUND(SUM(Final_Amount), 2) AS total_spending
FROM food_orders
GROUP BY Customer_ID
ORDER BY total_spending DESC
LIMIT 10;

-- 2.Analyze age group vs order value
SELECT
    age_group,
    COUNT(*) AS total_orders,
    ROUND(AVG(Order_Value), 2) AS average_order_value,
    ROUND(SUM(Order_Value), 2) AS total_order_value
FROM (
    SELECT
        CASE
            WHEN Customer_Age < 18 THEN 'Below 18'
            WHEN Customer_Age BETWEEN 18 AND 25 THEN '18-25'
            WHEN Customer_Age BETWEEN 26 AND 35 THEN '26-35'
            WHEN Customer_Age BETWEEN 36 AND 50 THEN '36-50'
            ELSE 'Above 50'
        END AS age_group,
        Order_Value
    FROM food_orders
) AS age_data
GROUP BY age_group
ORDER BY average_order_value DESC;

-- 3.Weekend vs weekday order patterns
SELECT
    CASE
        WHEN DAYOFWEEK(Order_Date) IN (1, 7) THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    COUNT(*) AS total_orders,
    ROUND(
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM food_orders),
        2
    ) AS order_percentage
FROM food_orders
GROUP BY
    CASE
        WHEN DAYOFWEEK(Order_Date) IN (1, 7) THEN 'Weekend'
        ELSE 'Weekday'
    END
ORDER BY total_orders DESC;

-- Revenue & Profit Analysis
-- 4.Monthly revenue trends

SELECT
    YEAR(Order_Date) AS order_year,
    MONTH(Order_Date) AS order_month,
    MONTHNAME(Order_Date) AS month_name,
    ROUND(SUM(Final_Amount), 2) AS monthly_revenue
FROM food_orders
WHERE Order_Status = 'Delivered'
GROUP BY
    YEAR(Order_Date),
    MONTH(Order_Date),
    MONTHNAME(Order_Date)
ORDER BY
    order_year,
    order_month;
    
   SELECT
    MONTHNAME(Order_Date) AS month_name,
    ROUND(SUM(Final_Amount), 2) AS monthly_revenue
FROM food_orders
WHERE Order_Status = 'Delivered'
GROUP BY
    MONTH(Order_Date),
    MONTHNAME(Order_Date)
ORDER BY
    MONTH(Order_Date); 
    
    -- 6.High-revenue cities and cuisines
    SELECT
    City,
    COUNT(*) AS total_orders,
    ROUND(SUM(Final_Amount), 2) AS total_revenue
FROM food_orders
WHERE Order_Status = 'Delivered'
GROUP BY City
ORDER BY total_revenue DESC
LIMIT 10;

-- Delivery Performance
-- 7.Average delivery time by city
SELECT
    City,
    COUNT(*) AS total_orders,
    ROUND(AVG(Delivery_Time_Min), 2) AS average_delivery_time
FROM food_orders
WHERE Order_Status = 'Delivered'
GROUP BY City
ORDER BY average_delivery_time ASC;

-- 8.Distance vs Delivery Delay Analysis
SELECT
    ROUND(Distance_km, 1) AS distance_km,
    COUNT(*) AS total_orders,
    ROUND(AVG(Delivery_Time_Min), 2) AS average_delivery_time
FROM food_orders
WHERE Order_Status = 'Delivered'
  AND Distance_km IS NOT NULL
  AND Delivery_Time_Min IS NOT NULL
GROUP BY ROUND(Distance_km, 1)
ORDER BY distance_km;

-- 10.Delivery rating vs delivery time
SELECT
    Delivery_Rating,
    COUNT(*) AS total_orders,
    ROUND(AVG(Delivery_Time_Min), 2) AS average_delivery_time
FROM food_orders
WHERE Order_Status = 'Delivered'
  AND Delivery_Rating IS NOT NULL
  AND Delivery_Time_Min IS NOT NULL
GROUP BY Delivery_Rating
ORDER BY Delivery_Rating DESC;

-- Restaurant Performance
-- 11.Cuisine-wise performance
SELECT
    Cuisine_Type,
    COUNT(*) AS total_orders,
    ROUND(SUM(Final_Amount), 2) AS total_revenue,
    ROUND(AVG(Restaurant_Rating), 2) AS average_restaurant_rating,
    ROUND(AVG(Delivery_Time_Min), 2) AS average_delivery_time,
    ROUND(AVG(Profit_Margin), 2) AS average_profit_margin
FROM food_orders
WHERE Cuisine_Type IS NOT NULL
GROUP BY Cuisine_Type
ORDER BY total_revenue DESC;

-- Operational Insights
