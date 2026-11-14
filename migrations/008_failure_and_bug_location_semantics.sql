BEGIN;

-- Add source columns to the candidate-location record so bug localization can
-- be rendered at the exact UnpPtr token rather than only at line 16.
ALTER TABLE candidate_locations
  ADD COLUMN IF NOT EXISTS start_column integer,
  ADD COLUMN IF NOT EXISTS end_column integer,
  ADD COLUMN IF NOT EXISTS name text;

UPDATE candidate_locations
SET start_column = 41,
    end_column = 47,
    name = 'UnpPtr'
WHERE candidate_id = 'cloc-ce3eab88-dcec-4f1e-b385-53060fe19cdb';

-- This workflow captures the failure location and its observable consequence,
-- not the later propagation-chain structure or primitive source type.
ALTER TABLE object_locations
  DROP COLUMN IF EXISTS chain_id,
  DROP COLUMN IF EXISTS weakness_id,
  DROP COLUMN IF EXISTS type;

UPDATE object_locations
SET cwe_id = 'CWE-122',
    cwe_label = 'Heap-based Buffer Overflow'
WHERE object_location_id = '4189d8c6dba4eac924383f8dfefa7b0a2571e196cc1f4733c78509ad921acbb1';

-- Failure-location validation is independent from the target and reproduction.
CREATE TABLE IF NOT EXISTS object_location_reviews (
  object_location_id text PRIMARY KEY
    REFERENCES object_locations(object_location_id) ON DELETE CASCADE,
  status text NOT NULL CHECK (status IN ('pending','accepted','rejected')),
  reviewer_id text NOT NULL,
  note text,
  updated_at timestamptz NOT NULL DEFAULT now()
);

-- Correct the failure's resource semantics: an object in memory is corrupted.
UPDATE annotations
SET value = 'object',
    notes = '["The affected item is the memory object at the failure location."]'::jsonb,
    updated_at = now()
WHERE annotation_id = 'ann-46f04c1593782122';

UPDATE annotations
SET value = 'corrupted',
    notes = '["The one-byte write corrupts memory beyond the allocated heap buffer."]'::jsonb,
    updated_at = now()
WHERE annotation_id = 'ann-bf39840eeff85d42';

INSERT INTO annotations (
  annotation_id, schema_version, reviewer_id, model, model_id, location_id,
  kind, status, field, taxonomy, value, confidence, notes, created_at, updated_at
) VALUES (
  'ann-failure-class-memory',
  '0.5.0',
  '1',
  'object_location',
  '4189d8c6dba4eac924383f8dfefa7b0a2571e196cc1f4733c78509ad921acbb1',
  '4189d8c6dba4eac924383f8dfefa7b0a2571e196cc1f4733c78509ad921acbb1',
  'seed',
  'active',
  'resource.class',
  'chain-model',
  'memory',
  1.00,
  '["The corrupted object belongs to the memory resource class."]'::jsonb,
  now(),
  now()
)
ON CONFLICT (annotation_id) DO NOTHING;

-- Match the label casing requested for the bug's qualifier and operation.
UPDATE annotations
SET value = 'Incorrect', updated_at = now()
WHERE annotation_id = 'ann-ecbbc3d1c339a460';

UPDATE annotations
SET value = 'Evaluate', updated_at = now()
WHERE annotation_id = 'ann-1de8f8dbcb38d23d';

COMMIT;
