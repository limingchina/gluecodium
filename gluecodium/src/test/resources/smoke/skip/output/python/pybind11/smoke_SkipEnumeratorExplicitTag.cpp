

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SkipEnumeratorExplicitTag.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SkipEnumeratorExplicitTag = ::smoke::SkipEnumeratorExplicitTag;

void register_smoke_SkipEnumeratorExplicitTag(py::module_& module) {
    py::enum_<SkipEnumeratorExplicitTag>(module, "SkipEnumeratorExplicitTag")
        .value("ZERO", SkipEnumeratorExplicitTag::ZERO)
        .value("ONE", SkipEnumeratorExplicitTag::ONE)
        .value("THREE", SkipEnumeratorExplicitTag::THREE)
        ;
}

