

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkipEnumeratorExplicitTag.h"

void register_SkipEnumeratorExplicitTag(py::module_& module) {
    py::enum_<SkipEnumeratorExplicitTag>(module, "SkipEnumeratorExplicitTag")
        .value("ZERO", SkipEnumeratorExplicitTag::ZERO)
        .value("ONE", SkipEnumeratorExplicitTag::ONE)
        .value("THREE", SkipEnumeratorExplicitTag::THREE)
        ;
}

