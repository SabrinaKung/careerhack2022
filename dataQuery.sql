# Stream Analytics job Query

# Get mining data and power data from Event Hub
# then use stream analytic query to select data and output data stream to Power BI.


SELECT m.time, m.algorithms.ZHASH.speedAccepted AS data_speedAccepted, 
    m.algorithms.ZHASH.profitability AS data_profitability, 
    d.telemetry.powerConsumption2 AS powerConsumption,
    m.algorithms.ZHASH.profitability/d.telemetry.powerConsumption2 AS unitProfit
INTO PowerBIanalysis -- to power bi 
FROM mining m TIMESTAMP BY EventEnqueuedUtcTime
LEFT OUTER JOIN demoeventHub d TIMESTAMP BY EventEnqueuedUtcTime
ON DATEDIFF(minute,m,d) between 0 and 1 -- join within 1 min of demoeventHub data
WHERE d.telemetry.powerConsumption2 IS NOT null
