BEGIN;

-- The previous local seed collapsed blank lines in these function snapshots.
-- Restore the exact benchmark source bytes so absolute source line anchors are
-- preserved in the portal (notably manifestation line 65 / Dest[2]).
UPDATE artifacts
SET content = '_forceinline void Unpack::CopyString(uint Length,uint Distance)
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
      // be replaced with ''Window[UnpPtr++ & MaxWinMask]''
      UnpPtr=(UnpPtr+1) & MaxWinMask;
    }
}'
WHERE artifact_id = 'b4914966fec23c73b8ba9336fdaa62ea549a8ea6dba1d8c24ded22b3861d47dc';

UPDATE artifacts
SET content = '_forceinline void Unpack::CopyString(uint Length,uint Distance)
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
      // be replaced with ''Window[UnpPtr++ & MaxWinMask]''
      UnpPtr=(UnpPtr+1) & MaxWinMask;
    }
}'
WHERE artifact_id = '5e53cbe3190bcadd8509fac3ace765a14746dafc72c8277d3600da82783f8554';

COMMIT;
