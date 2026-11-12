BEGIN;

CREATE TABLE IF NOT EXISTS candidate_locations (
  candidate_id text PRIMARY KEY,
  schema_version text NOT NULL,
  project_id text NOT NULL REFERENCES projects(project_id),
  revision_id text NOT NULL,
  target_id text NOT NULL REFERENCES targets(target_id),
  artifact_id text NOT NULL REFERENCES artifacts(artifact_id),
  reviewer_id text NOT NULL,
  line integer NOT NULL CHECK (line > 0),
  notes jsonb NOT NULL DEFAULT '[]'::jsonb,
  created_at timestamptz NOT NULL
);

CREATE TABLE IF NOT EXISTS candidate_reviews (
  candidate_id text PRIMARY KEY REFERENCES candidate_locations(candidate_id) ON DELETE CASCADE,
  status text NOT NULL CHECK (status IN ('pending','accepted','rejected')),
  reviewer_id text NOT NULL,
  note text,
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS reproductions (
  reproduction_id text PRIMARY KEY,
  schema_version text NOT NULL,
  target_id text NOT NULL REFERENCES targets(target_id),
  source_payload jsonb NOT NULL
);

CREATE TABLE IF NOT EXISTS reproduction_artifacts (
  reproduction_id text NOT NULL REFERENCES reproductions(reproduction_id) ON DELETE CASCADE,
  artifact_id text NOT NULL REFERENCES artifacts(artifact_id),
  role text NOT NULL,
  revision text NOT NULL,
  ordinal integer NOT NULL,
  PRIMARY KEY (reproduction_id, ordinal)
);

CREATE TABLE IF NOT EXISTS reproduction_reviews (
  reproduction_id text PRIMARY KEY REFERENCES reproductions(reproduction_id) ON DELETE CASCADE,
  status text NOT NULL CHECK (status IN ('pending','accepted','rejected')),
  reviewer_id text NOT NULL,
  note text,
  updated_at timestamptz NOT NULL DEFAULT now()
);

-- The legacy report seed used literal backslash-n sequences; normalize them to real newlines.
UPDATE artifacts
SET content = replace(content, E'\\n', E'\n')
WHERE artifact_type = 'crash_report';

-- Replace the initial abbreviated function payloads with the exact source snapshots.
UPDATE artifacts
SET content = $patchbase$_forceinline void Unpack::CopyString(uint Length,uint Distance)
{
  size_t SrcPtr=UnpPtr-Distance;
  if (SrcPtr<MaxWinSize-MAX_LZ_MATCH && UnpPtr<MaxWinSize-MAX_LZ_MATCH)
  {
    // If we are not close to end of window, we do not need to waste time
    // to "& MaxWinMask" pointer protection.

    byte *Src=Window+SrcPtr;
    byte *Dest=Window+UnpPtr;
    UnpPtr+=Length;

#ifdef FAST_MEMCPY
    if (Distance<Length) // Overlapping strings
#endif
      while (Length>=8)
      {
        Dest[0]=Src[0];
        Dest[1]=Src[1];
        Dest[2]=Src[2];
        Dest[3]=Src[3];
        Dest[4]=Src[4];
        Dest[5]=Src[5];
        Dest[6]=Src[6];
        Dest[7]=Src[7];

        Src+=8;
        Dest+=8;
        Length-=8;
      }
#ifdef FAST_MEMCPY
    else
      while (Length>=8)
      {
        // In theory we still could overlap here.
        // Supposing Distance == MaxWinSize - 1 we have memcpy(Src, Src + 1, 8).
        // But for real RAR archives Distance <= MaxWinSize - MAX_LZ_MATCH
        // always, so overlap here is impossible.

        // This memcpy expanded inline by MSVC. We could also use uint64
        // assignment, which seems to provide about the same speed.
        memcpy(Dest,Src,8); 

        Src+=8;
        Dest+=8;
        Length-=8;
      }
#endif

    // Unroll the loop for 0 - 7 bytes left. Note that we use nested "if"s.
    if (Length>0) { Dest[0]=Src[0];
    if (Length>1) { Dest[1]=Src[1];
    if (Length>2) { Dest[2]=Src[2];
    if (Length>3) { Dest[3]=Src[3];
    if (Length>4) { Dest[4]=Src[4];
    if (Length>5) { Dest[5]=Src[5];
    if (Length>6) { Dest[6]=Src[6]; } } } } } } } // Close all nested "if"s.
  }
  else
    while (Length-- > 0) // Slow copying with all possible precautions.
    {
      Window[UnpPtr]=Window[SrcPtr++ & MaxWinMask];
      // We need to have masked UnpPtr after quit from loop, so it must not
      // be replaced with 'Window[UnpPtr++ & MaxWinMask]'
      UnpPtr=(UnpPtr+1) & MaxWinMask;
    }
}$patchbase$
WHERE artifact_id = 'b4914966fec23c73b8ba9336fdaa62ea549a8ea6dba1d8c24ded22b3861d47dc';

UPDATE artifacts
SET content = $fix$_forceinline void Unpack::CopyString(uint Length,uint Distance)
{
  size_t SrcPtr=UnpPtr-Distance;
  if (SrcPtr<MaxWinSize-MAX_INC_LZ_MATCH && UnpPtr<MaxWinSize-MAX_INC_LZ_MATCH)
  {
    // If we are not close to end of window, we do not need to waste time
    // to "& MaxWinMask" pointer protection.

    byte *Src=Window+SrcPtr;
    byte *Dest=Window+UnpPtr;
    UnpPtr+=Length;

#ifdef FAST_MEMCPY
    if (Distance<Length) // Overlapping strings
#endif
      while (Length>=8)
      {
        Dest[0]=Src[0];
        Dest[1]=Src[1];
        Dest[2]=Src[2];
        Dest[3]=Src[3];
        Dest[4]=Src[4];
        Dest[5]=Src[5];
        Dest[6]=Src[6];
        Dest[7]=Src[7];

        Src+=8;
        Dest+=8;
        Length-=8;
      }
#ifdef FAST_MEMCPY
    else
      while (Length>=8)
      {
        // In theory we still could overlap here.
        // Supposing Distance == MaxWinSize - 1 we have memcpy(Src, Src + 1, 8).
        // But for real RAR archives Distance <= MaxWinSize - MAX_INC_LZ_MATCH
        // always, so overlap here is impossible.

        // This memcpy expanded inline by MSVC. We could also use uint64
        // assignment, which seems to provide about the same speed.
        memcpy(Dest,Src,8); 

        Src+=8;
        Dest+=8;
        Length-=8;
      }
#endif

    // Unroll the loop for 0 - 7 bytes left. Note that we use nested "if"s.
    if (Length>0) { Dest[0]=Src[0];
    if (Length>1) { Dest[1]=Src[1];
    if (Length>2) { Dest[2]=Src[2];
    if (Length>3) { Dest[3]=Src[3];
    if (Length>4) { Dest[4]=Src[4];
    if (Length>5) { Dest[5]=Src[5];
    if (Length>6) { Dest[6]=Src[6]; } } } } } } } // Close all nested "if"s.
  }
  else
    while (Length-- > 0) // Slow copying with all possible precautions.
    {
      Window[UnpPtr]=Window[SrcPtr++ & MaxWinMask];
      // We need to have masked UnpPtr after quit from loop, so it must not
      // be replaced with 'Window[UnpPtr++ & MaxWinMask]'
      UnpPtr=(UnpPtr+1) & MaxWinMask;
    }
}$fix$
WHERE artifact_id = '5e53cbe3190bcadd8509fac3ace765a14746dafc72c8277d3600da82783f8554';

INSERT INTO artifacts (
  artifact_id, project_id, revision, role, artifact_type, media_type, content
) VALUES
(
 '11b9581d0d11998646dadd0feeeb8fc94188431edd67b9a22a88e7861682e60f',
 'aawc/unrar','1d8ea7923dae7c8f136912b6bdca95dcb52e80bc','log','log',
 'text/plain',$runnerlog$+ FUZZER=unrar_fuzzer
+ shift
+ '[' '!' -v TESTCASE ']'
+ TESTCASE=/testcase
+ '[' '!' -f /testcase ']'
+ export RUN_FUZZER_MODE=interactive
+ RUN_FUZZER_MODE=interactive
+ export FUZZING_ENGINE=libfuzzer
+ FUZZING_ENGINE=libfuzzer
+ export SKIP_SEED_CORPUS=1
+ SKIP_SEED_CORPUS=1
+ run_fuzzer unrar_fuzzer -runs=1 /testcase
vm.mmap_rnd_bits = 28
/out/unrar_fuzzer -rss_limit_mb=2560 -timeout=25 -runs=1 /testcase < /dev/null
INFO: Running with entropic power schedule (0xFF, 100).
INFO: Seed: 2615484819
INFO: Loaded 1 modules   (6960 inline 8-bit counters): 6960 [0x55a555405cc0, 0x55a5554077f0),
INFO: Loaded 1 PC tables (6960 PCs): 6960 [0x55a5554077f0,0x55a555422af0),
/out/unrar_fuzzer: Running 1 inputs 1 time(s) each.
Running: /testcase
=================================================================
==14==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7fa93b0b6800 at pc 0x55a5552ea92d bp 0x7ffea233a810 sp 0x7ffea233a808
WRITE of size 1 at 0x7fa93b0b6800 thread T0
SCARINESS: 31 (1-byte-write-heap-buffer-overflow)
#0 0x55a5552ea92c in Unpack::CopyString(unsigned int, unsigned int) /src/unrar/./unpackinline.cpp:65:28
#1 0x55a5552e5fbc in Unpack::UnpackLargeBlock(UnpackThreadData&) /src/unrar/./unpack50mt.cpp
#2 0x55a5552e1f41 in Unpack::Unpack5MT(bool) /src/unrar/./unpack50mt.cpp:208:37
#3 0x55a5552ccf2b in CmdExtract::ExtractCurrentFile(Archive&, unsigned long, bool&) /src/unrar/extract.cpp
#4 0x55a5552c9e35 in CmdExtract::ExtractArchive() /src/unrar/extract.cpp:199:10
#5 0x55a5552c92c7 in CmdExtract::DoExtract() /src/unrar/extract.cpp:45:29
#6 0x55a555237699 in LLVMFuzzerTestOneInput /src/unrar/unrar_fuzzer.cc:22:15
#7 0x55a555254ae0 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const*, unsigned long) /src/llvm-project/compiler-rt/lib/fuzzer/FuzzerLoop.cpp:614:13
#8 0x55a55523fd55 in fuzzer::RunOneTest(fuzzer::Fuzzer*, char const*, unsigned long) /src/llvm-project/compiler-rt/lib/fuzzer/FuzzerDriver.cpp:327:6
#9 0x55a5552457ef in fuzzer::FuzzerDriver(int*, char***, int (*)(unsigned char const*, unsigned long)) /src/llvm-project/compiler-rt/lib/fuzzer/FuzzerDriver.cpp:862:9
#10 0x55a555270a92 in main /src/llvm-project/compiler-rt/lib/fuzzer/FuzzerMain.cpp:20:10
#11 0x7fa93f47c082 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x24082) (BuildId: 5792732f783158c66fb4f3756458ca24e46e827d)
#12 0x55a55515ec1d in _start (/out/unrar_fuzzer+0x71c1d)
DEDUP_TOKEN: Unpack::CopyString(unsigned int, unsigned int)--Unpack::UnpackLargeBlock(UnpackThreadData&)--Unpack::Unpack5MT(bool)
0x7fa93b0b6800 is located 0 bytes after 1048576-byte region [0x7fa93afb6800,0x7fa93b0b6800)
allocated by thread T0 here:
#0 0x55a5551f7c2f in malloc /src/llvm-project/compiler-rt/lib/asan/asan_malloc_linux.cpp:68:3
#1 0x55a555308363 in Unpack::Init(unsigned long, bool) /src/unrar/unpack.cpp:94:47
#2 0x55a5552ccbb0 in CmdExtract::ExtractCurrentFile(Archive&, unsigned long, bool&) /src/unrar/extract.cpp:667:18
#3 0x55a5552c9e35 in CmdExtract::ExtractArchive() /src/unrar/extract.cpp:199:10
#4 0x55a5552c92c7 in CmdExtract::DoExtract() /src/unrar/extract.cpp:45:29
#5 0x55a555237699 in LLVMFuzzerTestOneInput /src/unrar/unrar_fuzzer.cc:22:15
#6 0x55a555254ae0 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const*, unsigned long) /src/llvm-project/compiler-rt/lib/fuzzer/FuzzerLoop.cpp:614:13
#7 0x55a55523fd55 in fuzzer::RunOneTest(fuzzer::Fuzzer*, char const*, unsigned long) /src/llvm-project/compiler-rt/lib/fuzzer/FuzzerDriver.cpp:327:6
#8 0x55a5552457ef in fuzzer::FuzzerDriver(int*, char***, int (*)(unsigned char const*, unsigned long)) /src/llvm-project/compiler-rt/lib/fuzzer/FuzzerDriver.cpp:862:9
#9 0x55a555270a92 in main /src/llvm-project/compiler-rt/lib/fuzzer/FuzzerMain.cpp:20:10
#10 0x7fa93f47c082 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x24082) (BuildId: 5792732f783158c66fb4f3756458ca24e46e827d)
DEDUP_TOKEN: __interceptor_malloc--Unpack::Init(unsigned long, bool)--CmdExtract::ExtractCurrentFile(Archive&, unsigned long, bool&)
SUMMARY: AddressSanitizer: heap-buffer-overflow /src/unrar/./unpackinline.cpp:65:28 in Unpack::CopyString(unsigned int, unsigned int)
Shadow bytes around the buggy address:
0x7fa93b0b6580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0x7fa93b0b6600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0x7fa93b0b6680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0x7fa93b0b6700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0x7fa93b0b6780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7fa93b0b6800:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
0x7fa93b0b6880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
0x7fa93b0b6900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
0x7fa93b0b6980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
0x7fa93b0b6a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
0x7fa93b0b6a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
Addressable:           00
Partially addressable: 01 02 03 04 05 06 07
Heap left redzone:       fa
Freed heap region:       fd
Stack left redzone:      f1
Stack mid redzone:       f2
Stack right redzone:     f3
Stack after return:      f5
Stack use after scope:   f8
Global redzone:          f9
Global init order:       f6
Poisoned by user:        f7
Container overflow:      fc
Array cookie:            ac
Intra object redzone:    bb
ASan internal:           fe
Left alloca redzone:     ca
Right alloca redzone:    cb
==14==ABORTING
$runnerlog$
),
(
 '954a541e31c21bfd10019b4ea641455b6424b9fa977bfad25052f78be99b03dc',
 'aawc/unrar','1d8ea7923dae7c8f136912b6bdca95dcb52e80bc','execution_context','execution_context',
 'application/json',$executioncontext${
  "schema_version": "execution-context-0.1.0",
  "runtime": {
    "engine": "docker"
  },
  "image": {
    "local_id": "6db752162cb1",
    "tag": "osv-reproducer/unrar-373c1e4c118a128658b5f333af863314a3c731d3"
  },
  "container": {
    "local_id": "b03343f41d5"
  }
}
$executioncontext$
)
ON CONFLICT (artifact_id) DO UPDATE SET
  project_id=EXCLUDED.project_id,
  revision=EXCLUDED.revision,
  role=EXCLUDED.role,
  artifact_type=EXCLUDED.artifact_type,
  media_type=EXCLUDED.media_type,
  content=EXCLUDED.content;

-- The revision is derived from each candidate's storage directory. Preserve the two source records verbatim.
INSERT INTO candidate_locations (
  candidate_id,schema_version,project_id,revision_id,target_id,artifact_id,reviewer_id,line,notes,created_at
) VALUES
(
 'cloc-ce3eab88-dcec-4f1e-b385-53060fe19cdb','0.1.0','aawc/unrar',
 '1d8ea7923dae7c8f136912b6bdca95dcb52e80bc',
 '2f122ea0e46729b7cbac9361f65fb9550bfae0a1e0665c6fcb8a017371df1d81',
 'b4914966fec23c73b8ba9336fdaa62ea549a8ea6dba1d8c24ded22b3861d47dc',
 '1',16,'[]'::jsonb,'2026-11-02T15:42:53.471Z'
),
(
 'cloc-eaaf035d-95ab-417a-988a-3fd9ba7eb40d','0.1.0','aawc/unrar',
 'c3ed4a1db1f39bf4524a644cb2af81dc8cfab33f',
 '2f122ea0e46729b7cbac9361f65fb9550bfae0a1e0665c6fcb8a017371df1d81',
 'b4914966fec23c73b8ba9336fdaa62ea549a8ea6dba1d8c24ded22b3861d47dc',
 '1',16,'[]'::jsonb,'2026-11-02T15:42:53.471Z'
)
ON CONFLICT (candidate_id) DO NOTHING;

INSERT INTO candidate_reviews(candidate_id,status,reviewer_id)
SELECT candidate_id,'pending','reviewer-01' FROM candidate_locations
ON CONFLICT (candidate_id) DO NOTHING;

INSERT INTO reproductions(reproduction_id,schema_version,target_id,source_payload)
VALUES (
 '7a272de98e2ea6e5f897694c609b7ec932a51f5c414d80536b6b85598fd22451',
 'reproduction-0.2.0',
 '166d1d0864039e13c438fa27e34f557a1241dd030bdecb18ab4c9dc4abbd08f4',
 $reproduction${
  "id": "7a272de98e2ea6e5f897694c609b7ec932a51f5c414d80536b6b85598fd22451",
  "schema_version": "reproduction-0.2.0",
  "target_id": "166d1d0864039e13c438fa27e34f557a1241dd030bdecb18ab4c9dc4abbd08f4",
  "artifacts": [
    {
      "role": "execution_context",
      "revision": "1d8ea7923dae7c8f136912b6bdca95dcb52e80bc",
      "artifact_id": "954a541e31c21bfd10019b4ea641455b6424b9fa977bfad25052f78be99b03dc"
    },
    {
      "role": "log",
      "revision": "1d8ea7923dae7c8f136912b6bdca95dcb52e80bc",
      "artifact_id": "11b9581d0d11998646dadd0feeeb8fc94188431edd67b9a22a88e7861682e60f"
    }
  ]
}$reproduction$::jsonb
)
ON CONFLICT (reproduction_id) DO NOTHING;

INSERT INTO reproduction_artifacts(reproduction_id,artifact_id,role,revision,ordinal)
VALUES
('7a272de98e2ea6e5f897694c609b7ec932a51f5c414d80536b6b85598fd22451',
 '954a541e31c21bfd10019b4ea641455b6424b9fa977bfad25052f78be99b03dc',
 'execution_context','1d8ea7923dae7c8f136912b6bdca95dcb52e80bc',0),
('7a272de98e2ea6e5f897694c609b7ec932a51f5c414d80536b6b85598fd22451',
 '11b9581d0d11998646dadd0feeeb8fc94188431edd67b9a22a88e7861682e60f',
 'log','1d8ea7923dae7c8f136912b6bdca95dcb52e80bc',1)
ON CONFLICT (reproduction_id,ordinal) DO NOTHING;

INSERT INTO reproduction_reviews(reproduction_id,status,reviewer_id)
VALUES ('7a272de98e2ea6e5f897694c609b7ec932a51f5c414d80536b6b85598fd22451','pending','reviewer-01')
ON CONFLICT (reproduction_id) DO NOTHING;

COMMIT;
