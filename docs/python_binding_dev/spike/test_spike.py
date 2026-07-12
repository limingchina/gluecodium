import sys
import traceback

import spike_module as sm


def check(name, fn, expect_ok, expect_value=None):
    try:
        result = fn()
    except Exception as e:
        if expect_ok:
            print(f"FAIL {name}: unexpected exception {type(e).__name__}: {e}")
            return False
        print(f"PASS {name}: raised {type(e).__name__}: {e}")
        return True
    if not expect_ok:
        print(f"FAIL {name}: expected exception but got value {result!r}")
        return False
    ok = (result == expect_value)
    print(f"{'PASS' if ok else 'FAIL'} {name}: returned {result!r}"
          f"{'' if ok else f' (expected {expect_value!r})'}")
    return ok


def main():
    results = []
    results.append(check("divide ok", lambda: sm.divide(10, 2), True, 5))
    results.append(check("divide by zero", lambda: sm.divide(10, 0), False))
    results.append(check("greet ok", lambda: sm.greet("world"), True, "hello, world"))
    results.append(check("greet empty", lambda: sm.greet(""), False))
    results.append(check("sqrt_safe ok", lambda: sm.sqrt_safe(3.0), True, 9.0))
    results.append(check("sqrt_safe neg", lambda: sm.sqrt_safe(-1.0), False))

    if all(results):
        print("\nALL SPIKE CHECKS PASSED")
        sys.exit(0)
    else:
        print("\nSPIKE CHECKS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
