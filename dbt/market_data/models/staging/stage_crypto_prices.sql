SELECT
    symbol,
    CAST(timestamp as timestamptz) as fetched_at,
    CAST(price as numeric),
    CAST(total_volume as BIGINT),
    CAST(market_cap as numeric),
    CAST(high_24h as numeric) as high_price,
    CAST(low_24h as numeric) as low_price
FROM raw.crypto_prices
WHERE price > 0