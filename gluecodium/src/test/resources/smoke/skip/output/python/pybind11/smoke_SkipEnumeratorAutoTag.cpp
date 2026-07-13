

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkipEnumeratorAutoTag.h"

void register_SkipEnumeratorAutoTag(py::module_& module) {
    py::enum_<SkipEnumeratorAutoTag>(module, "SkipEnumeratorAutoTag")
        .value("ONE", SkipEnumeratorAutoTag::ONE)
        .value("THREE", SkipEnumeratorAutoTag::THREE)
        ;
}

