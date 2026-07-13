

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "include/ExternalTypes.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructWithOverloads = external::ClassWithOverloads::StructWithOverloads;

void register_StructWithOverloads(py::module_& module) {
    py::class_<external::ClassWithOverloads::StructWithOverloads>(module, "StructWithOverloads")
        .def_readwrite("overloaded_accessors", &external::ClassWithOverloads::StructWithOverloads::overloadedAccessors)
        .def(py::init<int32_t>(), py::arg("overloaded_accessors"))
        .def("overloaded_method", &external::ClassWithOverloads::StructWithOverloads::overloadedMethod)
        .def("overloaded_method", &external::ClassWithOverloads::StructWithOverloads::overloadedMethod, py::arg("input"))
        .def("overloaded_method", &external::ClassWithOverloads::StructWithOverloads::overloadedMethod, py::arg("input_string"), py::arg("input_bool"))
        ;
}

