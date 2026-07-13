

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SwiftExternalCtor.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SwiftExternalCtor = ::smoke::SwiftExternalCtor;

void register_SwiftExternalCtor(py::module_& module) {
    py::class_<SwiftExternalCtor>(module, "SwiftExternalCtor")
        .def_readwrite("field", &SwiftExternalCtor::field)
        .def(py::init<::std::string>(), py::arg("field"))
        .def("make", &SwiftExternalCtor::make, py::arg("field"))
        ;
}

