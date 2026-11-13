BEGIN;

-- Targets need their own lifecycle timestamps, separate from review records.
ALTER TABLE targets
  ADD COLUMN IF NOT EXISTS created_at timestamptz,
  ADD COLUMN IF NOT EXISTS updated_at timestamptz;

UPDATE targets t
SET created_at = COALESCE(
      t.created_at,
      (SELECT e.created_at FROM examinations e WHERE e.examination_id=t.examination_id),
      now()
    ),
    updated_at = COALESCE(
      t.updated_at,
      (SELECT tr.updated_at FROM target_reviews tr WHERE tr.target_id=t.target_id),
      t.created_at,
      (SELECT e.created_at FROM examinations e WHERE e.examination_id=t.examination_id),
      now()
    );

ALTER TABLE targets
  ALTER COLUMN created_at SET DEFAULT now(),
  ALTER COLUMN created_at SET NOT NULL,
  ALTER COLUMN updated_at SET DEFAULT now(),
  ALTER COLUMN updated_at SET NOT NULL;

-- Preserve the source location reference alongside each annotation. This
-- initial UnRAR slice uses the supplied crash-revision location record.
ALTER TABLE annotations
  ADD COLUMN IF NOT EXISTS location_id text;

UPDATE annotations
SET location_id = '07f83844735661b7e6425f154f09a1cdab4900d6a1337cf2067aa8b343aa108f'
WHERE annotation_id IN (
  'ann-ecbbc3d1c339a460',
  'ann-1de8f8dbcb38d23d'
)
AND location_id IS NULL;

-- The operation rationale is the initial reviewer note. Reviewers can submit
-- it unchanged or edit it before submission; it is not rendered as a separate
-- annotation-context block.
UPDATE annotations
SET review_note = COALESCE(review_note, notes->>0)
WHERE annotation_id = 'ann-1de8f8dbcb38d23d'
  AND review_note IS NULL;

COMMIT;
