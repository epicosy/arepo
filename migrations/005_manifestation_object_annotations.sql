BEGIN;

-- Object locations are first-class source anchors linked to a manifestation target.
CREATE TABLE IF NOT EXISTS object_locations (
  object_location_id text PRIMARY KEY,
  target_id text NOT NULL REFERENCES targets(target_id) ON DELETE CASCADE,
  project_id text NOT NULL REFERENCES projects(project_id),
  revision_id text NOT NULL,
  artifact_id text NOT NULL REFERENCES artifacts(artifact_id),
  chain_id text NOT NULL,
  weakness_id text NOT NULL,
  line integer NOT NULL,
  start_column integer,
  end_column integer,
  name text NOT NULL,
  type text NOT NULL,
  cwe_id text NOT NULL,
  cwe_label text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS object_locations_target_idx
  ON object_locations(target_id);

-- Annotations are polymorphic across candidate-location and object-location
-- records. Their model/model_id pair identifies the annotated entity.
ALTER TABLE annotations
  DROP CONSTRAINT IF EXISTS annotations_model_id_fkey;

INSERT INTO object_locations (
  object_location_id, target_id, project_id, revision_id, artifact_id,
  chain_id, weakness_id, line, start_column, end_column, name, type,
  cwe_id, cwe_label
) VALUES (
  '4189d8c6dba4eac924383f8dfefa7b0a2571e196cc1f4733c78509ad921acbb1',
  '166d1d0864039e13c438fa27e34f557a1241dd030bdecb18ab4c9dc4abbd08f4',
  'aawc/unrar',
  '1d8ea7923dae7c8f136912b6bdca95dcb52e80bc',
  'b4914966fec23c73b8ba9336fdaa62ea549a8ea6dba1d8c24ded22b3861d47dc',
  'ce41e447466d7bceaae9771c5b1dd0b1cc8b2bea5f6ea7f3b0f9206a7b35099a',
  'f15e8310713b0a4264df3956aaeb73267484f1be3490b84c827d11a6b1e62bec',
  65, 21, 28, 'Dest[2]', 'byte',
  'CWE-787', 'Out-of-bounds Write'
)
ON CONFLICT (object_location_id) DO NOTHING;

-- Import the two source annotations for the final manifestation object.
INSERT INTO annotations (
  annotation_id, schema_version, reviewer_id, model, model_id, location_id,
  kind, status, field, taxonomy, value, confidence, notes, created_at, updated_at
) VALUES
(
  'ann-46f04c1593782122','0.5.0','1','object_location',
  '4189d8c6dba4eac924383f8dfefa7b0a2571e196cc1f4733c78509ad921acbb1',
  '4189d8c6dba4eac924383f8dfefa7b0a2571e196cc1f4733c78509ad921acbb1',
  'seed','active','resource.kind','chain-model','buffer',1.00,
  '["The affected resource is the destination window buffer."]'::jsonb,now(),now()
),
(
  'ann-bf39840eeff85d42','0.5.0','1','object_location',
  '4189d8c6dba4eac924383f8dfefa7b0a2571e196cc1f4733c78509ad921acbb1',
  '4189d8c6dba4eac924383f8dfefa7b0a2571e196cc1f4733c78509ad921acbb1',
  'seed','active','resource.state','chain-model','out-of-bounds',1.00,
  '["AddressSanitizer reports a one-byte write at the address immediately after the allocated window buffer."]'::jsonb,now(),now()
)
ON CONFLICT (annotation_id) DO NOTHING;

COMMIT;
