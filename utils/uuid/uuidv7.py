"""
Implementation of UUID v7
https://datatracker.ietf.org/doc/draft-ietf-uuidrev-rfc4122bis/07/
"""

import datetime
import os
import struct
import time
import uuid
from typing import Callable, Optional, Union

__all__ = (
    "uuid7",
    "uuid7str",
    "time_ns",
    "check_timing_precision",
    "uuid_to_datetime",
)

# Expose function used by uuid7() to get current time in nanoseconds
# since the Unix epoch.
time_ns = time.time_ns


def uuid7(
        ns: Optional[int] = None,
        as_type: Optional[str] = None,
        time_func: Callable[[], int] = time_ns,
        _last=[0, 0, 0, 0],
        _last_as_of=[0, 0, 0, 0],
) -> Union[uuid.UUID, str, int, bytes]:
    if ns is None:
        ns = time_func()
        last = _last
    else:
        last = _last_as_of
        ns = int(ns)  # Fail fast if not an int

    if ns == 0:
        # Special cose for all-zero uuid. Strictly speaking not a UUIDv7.
        t1 = t2 = t3 = t4 = 0
        rand = b"\0" * 6
    else:
        # Treat the first 8 bytes of the uuid as a long (t1) and two ints
        # (t2 and t3) holding 36 bits of whole seconds and 24 bits of
        # fractional seconds.
        # This gives a nominal 60ns resolution, comparable to the
        # timestamp precision in Linux (~200ns) and Windows (100ns ticks).
        sixteen_secs = 16_000_000_000
        t1, rest1 = divmod(ns, sixteen_secs)
        t2, rest2 = divmod(rest1 << 16, sixteen_secs)
        t3, _ = divmod(rest2 << 12, sixteen_secs)
        t3 |= 7 << 12  # Put uuid version in top 4 bits, which are 0 in t3

        # The next two bytes are an int (t4) with two bits for
        # the variant 2 and a 14 bit sequence counter which increments
        # if the time is unchanged.
        if t1 == last[0] and t2 == last[1] and t3 == last[2]:
            # Stop the seq counter wrapping past 0x3FFF.
            # This won't happen in practice, but if it does,
            # uuids after the 16383rd with that same timestamp
            # will not longer be correctly ordered but
            # are still unique due to the 6 random bytes.
            if last[3] < 0x3FFF:
                last[3] += 1
        else:
            last[:] = (t1, t2, t3, 0)
        t4 = (2 << 14) | last[3]  # Put variant 0b10 in top two bits

        # Six random bytes for the lower part of the uuid
        rand = os.urandom(6)

    # Build output
    if as_type == "str":
        return f"{t1:>08x}-{t2:>04x}-{t3:>04x}-{t4:>04x}-{rand.hex()}"

    r = int.from_bytes(rand, "big")
    uuid_int = (t1 << 96) + (t2 << 80) + (t3 << 64) + (t4 << 48) + r
    if as_type == "int":
        return uuid_int
    elif as_type == "hex":
        return f"{uuid_int:>032x}"
    elif as_type == "bytes":
        return uuid_int.to_bytes(16, "big")
    else:
        return uuid.UUID(int=uuid_int)


def uuid7str(ns: Optional[int] = None) -> str:
    "uuid7() as a string without creating a UUID object first."
    return uuid7(ns, as_type="str")  # type: ignore


def check_timing_precision(
    timing_func: Optional[Callable[[], int]] = None,
) -> str:

    timing_funcs = [
        ("time.time_ns()", time.time_ns),
        ("time.perf_counter_ns()", time.perf_counter_ns),
        ("datetime.datetime.utcnow", lambda: int(
            datetime.datetime.utcnow().timestamp() * 1_000_000_000)),
    ]
    if timing_func is not None:
        timing_funcs.append(("user-supplied", timing_func))

    lines = []
    for desc, fn in timing_funcs:
        started_ns = time.perf_counter_ns()
        values = set()
        ctr = 0
        while True:
            values.add(fn())
            ctr += 1
            elapsed_ns = time.perf_counter_ns() - started_ns
            if elapsed_ns > 500_000_000 or len(values) >= 1000:
                break
        precision_ns = elapsed_ns / len(values)
        ideal_precision_ns = elapsed_ns / ctr
        lines.append(
            f"{desc} has a timing precision of {precision_ns:0,.0f}ns \
rather than {ideal_precision_ns:0,.0f}ns ({ctr:,} samples of which \
{len(values):,} are distinct, in {elapsed_ns / 1_000_000_000:0.2f}s)"
        )

    return "\n".join(lines)


def timestamp_ns(
        s: Union[str, uuid.UUID, int],
        suppress_error=True,
) -> Optional[int]:
    if isinstance(s, uuid.UUID):
        x = s.bytes
    elif not s:
        x = b"\0" * 16
    elif isinstance(s, int):
        x = int.to_bytes(s, length=16, byteorder="big")
    else:  # String form that should look like a UUID
        int_uuid = int(str(s).replace("-", ""), base=16)
        x = int.to_bytes(int_uuid, length=16, byteorder="big")

    uuid_version = x[6] >> 4
    if uuid_version == 7:
        bits = struct.unpack(">IHHHHI", x)
        uuid_version = (bits[2] >> 12) & 0xF
        # uuid_variant = (bits[3] >> 62) & 0x3
        whole_secs = (bits[0] << 4) + (bits[1] >> 12)
        frac_binary = (
                ((bits[1] & 0x0FFF) << 26)
                + ((bits[2] & 0x0FFF) << 14)
                + ((bits[3] & 0x3FFF))
        )
        frac_ns, _ = divmod(frac_binary * 1_000_000_000, 1 << 38)
        ns_since_epoch = whole_secs * 1_000_000_000 + frac_ns
        return ns_since_epoch
    elif suppress_error:
        return None
    else:
        raise ValueError(
            f"{str(s)} is a version {uuid_version} UUID, not v7 so we cannot extract the timestamp."
        )


def uuid_to_datetime(
    s: Union[str, uuid.UUID, int],
    suppress_error=True,
) -> Optional[datetime.datetime]:
    ns_since_epoch = timestamp_ns(s, suppress_error=suppress_error)
    if ns_since_epoch is None:
        return None
    else:
        return datetime.datetime.fromtimestamp(
            ns_since_epoch / 1_000_000_000,
            tz=datetime.timezone.utc,
        )
