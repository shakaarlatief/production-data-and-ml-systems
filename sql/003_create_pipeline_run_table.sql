BEGIN;

CREATE SCHEMA IF NOT EXISTS operations;

CREATE TABLE IF NOT EXISTS operations.pipeline_run (
    run_id BIGINT
        GENERATED ALWAYS AS IDENTITY
        PRIMARY KEY,

    pipeline_name TEXT NOT NULL,

    pipeline_stage TEXT NOT NULL
        CHECK (
            pipeline_stage IN (
                'raw_ingestion',
                'staging_validation',
                'analytics_build'
            )
        ),

    file_id BIGINT
        REFERENCES source.citibike_file (file_id),

    status TEXT NOT NULL
        CHECK (
            status IN (
                'running',
                'succeeded',
                'failed'
            )
        ),

    started_at TIMESTAMP WITH TIME ZONE NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    finished_at TIMESTAMP WITH TIME ZONE,

    source_row_count INTEGER
        CHECK (
            source_row_count IS NULL
            OR source_row_count >= 0
        ),

    valid_row_count INTEGER
        CHECK (
            valid_row_count IS NULL
            OR valid_row_count >= 0
        ),

    rejected_row_count INTEGER
        CHECK (
            rejected_row_count IS NULL
            OR rejected_row_count >= 0
        ),

    error_type TEXT,
    error_message TEXT,

    details JSONB NOT NULL
        DEFAULT '{}'::JSONB,

    CHECK (
        (
            status = 'running'
            AND finished_at IS NULL
        )
        OR
        (
            status IN ('succeeded', 'failed')
            AND finished_at IS NOT NULL
        )
    ),

    CHECK (
        status <> 'failed'
        OR error_message IS NOT NULL
    ),

    CHECK (
        status <> 'succeeded'
        OR (
            error_type IS NULL
            AND error_message IS NULL
        )
    )
);

CREATE INDEX IF NOT EXISTS pipeline_run_pipeline_started_at_idx
    ON operations.pipeline_run (
        pipeline_name,
        started_at DESC
    );

CREATE INDEX IF NOT EXISTS pipeline_run_file_id_idx
    ON operations.pipeline_run (file_id)
    WHERE file_id IS NOT NULL;

COMMIT;
