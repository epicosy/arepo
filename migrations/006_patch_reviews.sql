BEGIN;

-- Patch confirmation is distinct from the former target-definition review.
-- A previously accepted target must not be treated as a confirmed patch run.
CREATE TABLE IF NOT EXISTS patch_reviews (
  target_id text PRIMARY KEY REFERENCES targets(target_id) ON DELETE CASCADE,
  status text NOT NULL CHECK (status IN ('pending','accepted','rejected')),
  reviewer_id text NOT NULL,
  note text,
  updated_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
