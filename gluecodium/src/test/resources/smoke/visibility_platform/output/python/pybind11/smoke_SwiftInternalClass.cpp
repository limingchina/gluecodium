

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SwiftInternalClass.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SwiftInternalClass = ::smoke::SwiftInternalClass;

void register_SwiftInternalClass(py::module_& module) {
    py::class_<SwiftInternalClass, std::shared_ptr<SwiftInternalClass>>(module, "SwiftInternalClass")
        ;
}

