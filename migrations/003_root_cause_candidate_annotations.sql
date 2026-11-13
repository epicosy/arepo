BEGIN;

-- Keep candidate timestamps on the candidate record itself. The first migration
-- seeded created_at from the source candidate JSON; updated_at starts there too.
ALTER TABLE candidate_locations
  ADD COLUMN IF NOT EXISTS updated_at timestamptz;
UPDATE candidate_locations
SET updated_at = COALESCE(updated_at, created_at, now())
WHERE updated_at IS NULL;
ALTER TABLE candidate_locations
  ALTER COLUMN updated_at SET DEFAULT now(),
  ALTER COLUMN updated_at SET NOT NULL;

-- The first candidate JSON was stored under the crash-revision directory, but
-- its artifact_id identifies the patch-base function snapshot. The second
-- candidate references a revision that is not present in the project history.
UPDATE candidate_locations
SET revision_id = '637fc8446edb8444c7a66918f109f2fa552ff987',
    updated_at = COALESCE(updated_at, created_at, now())
WHERE candidate_id = 'cloc-ce3eab88-dcec-4f1e-b385-53060fe19cdb'
  AND artifact_id = 'b4914966fec23c73b8ba9336fdaa62ea549a8ea6dba1d8c24ded22b3861d47dc';

DELETE FROM candidate_locations
WHERE candidate_id = 'cloc-eaaf035d-95ab-417a-988a-3fd9ba7eb40d';

CREATE TABLE IF NOT EXISTS annotations (
  annotation_id text PRIMARY KEY,
  schema_version text NOT NULL,
  reviewer_id text NOT NULL,
  model text NOT NULL,
  model_id text NOT NULL REFERENCES candidate_locations(candidate_id) ON DELETE CASCADE,
  kind text NOT NULL,
  status text NOT NULL,
  field text NOT NULL,
  taxonomy text NOT NULL,
  value text NOT NULL,
  confidence numeric(3,2) NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
  notes jsonb NOT NULL DEFAULT '[]'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  submitted_at timestamptz,
  submitted_by text,
  review_note text
);

CREATE INDEX IF NOT EXISTS annotations_model_idx
  ON annotations(model, model_id);

-- Preserve the annotation identity, taxonomy and values, but bind the two
-- root-cause annotations to the candidate-location record that they annotate.
-- 'kind' and 'status' remain independent database attributes; they are not UI
-- controls in this workflow.
INSERT INTO annotations (
  annotation_id, schema_version, reviewer_id, model, model_id,
  kind, status, field, taxonomy, value, confidence, notes,
  created_at, updated_at
) VALUES
(
  'ann-ecbbc3d1c339a460','0.4.0','1','candidate_location',
  'cloc-ce3eab88-dcec-4f1e-b385-53060fe19cdb',
  'seed','active','qualifier','cwe-behavior-qualifier','incorrect',0.80,
  '[]'::jsonb,now(),now()
),
(
  'ann-1de8f8dbcb38d23d','0.4.0','1','candidate_location',
  'cloc-ce3eab88-dcec-4f1e-b385-53060fe19cdb',
  'seed','active','operation','bugs-framework','evaluate',0.80,
  '["the code performs a comparison to decide whether it can do an optimized copy, but it uses the wrong bound (wrong factor), so it sometimes permits a copy that exceeds the window."]'::jsonb,
  now(),now()
)
ON CONFLICT (annotation_id) DO NOTHING;

COMMIT;
