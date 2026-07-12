import sys
import datetime

import chrono_spike as cs


def check(name, got, expect):
    ok = (got == expect)
    print(f"{'PASS' if ok else 'FAIL'} {name}: got {got!r}"
          f"{'' if ok else f' (expected {expect!r})'}")
    return ok


def main():
    results = []

    # Date -> datetime.datetime.
    # NOTE: pybind11/chrono.h returns a NAIVE datetime in LOCAL time (it does not
    # attach tzinfo). The machine running this spike is at UTC+1, so the epoch
    # shows as 1970-01-01 01:00 local. This is expected pybind11 behavior; a
    # UTC-aware caster would require a custom type_caster (see plan 4.4).
    local_tz = datetime.datetime.now().astimezone().tzinfo
    epoch = cs.get_epoch()
    results.append(check("get_epoch is naive datetime",
                         isinstance(epoch, datetime.datetime) and epoch.tzinfo is None, True))
    results.append(check("get_epoch == 1970-01-01 local",
                         epoch, datetime.datetime(1970, 1, 1, 0, 0).astimezone(local_tz).replace(tzinfo=None)))

    later = cs.add_days(epoch, 1)
    results.append(check("add_days +1 == 1970-01-02 local",
                         later, datetime.datetime(1970, 1, 2, 0, 0).astimezone(local_tz).replace(tzinfo=None)))

    # datetime.datetime -> Date (round trip)
    rt = cs.add_days(datetime.datetime(2020, 5, 1, tzinfo=datetime.timezone.utc), 0)
    results.append(check("datetime arg accepted (returns datetime)",
                         isinstance(rt, datetime.datetime), True))

    # Duration -> datetime.timedelta
    d = cs.make_duration(90)
    results.append(check("make_duration is timedelta", isinstance(d, datetime.timedelta), True))
    results.append(check("make_duration == 90s", d, datetime.timedelta(seconds=90)))

    d2 = cs.double_duration(datetime.timedelta(seconds=30))
    results.append(check("double_duration(30s) == 60s",
                         d2, datetime.timedelta(seconds=60)))

    if all(results):
        print("\nALL CHRONO SPIKE CHECKS PASSED")
        sys.exit(0)
    else:
        print("\nCHRONO SPIKE CHECKS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
