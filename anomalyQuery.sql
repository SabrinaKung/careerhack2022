# Stream Analytics job Query

# Get anomaly data from Event Hub
# then use stream analytic query to select data and output data stream to Power BI.


WITH AnomalyDetectionStep AS
(
    SELECT
        EVENTENQUEUEDUTCTIME AS time,
        CAST(telemetry.powerConsumption2 AS float) AS powerconsumption,
        AnomalyDetection_SpikeAndDip(CAST(telemetry.powerConsumption2 AS float), 70, 120, 'spikesanddips')
            OVER(LIMIT DURATION(second, 80)) AS SpikeAndDipScores
    FROM AnoDet
)
SELECT
    time,
    powerconsumption,
    CAST(GetRecordPropertyValue(SpikeAndDipScores, 'Score') AS float) AS
    SpikeAndDipScore,
    CAST(GetRecordPropertyValue(SpikeAndDipScores, 'IsAnomaly') AS bigint) AS
    IsSpikeAndDipAnomaly
INTO AnomalyOutput
FROM AnomalyDetectionStep

SELECT
    time,
    powerconsumption,
    CAST(GetRecordPropertyValue(SpikeAndDipScores, 'Score') AS float) AS
    SpikeAndDipScore,
    CAST(GetRecordPropertyValue(SpikeAndDipScores, 'IsAnomaly') AS bigint) AS
    IsSpikeAndDipAnomaly
INTO control
FROM AnomalyDetectionStep