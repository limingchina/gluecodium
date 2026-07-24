

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/OuterStructWithFieldConstructor.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using OuterStructWithFieldConstructor = ::smoke::OuterStructWithFieldConstructor;

void register_smoke_OuterStructWithFieldConstructor(py::module_& module) {
    py::class_<OuterStructWithFieldConstructor>(module, "OuterStructWithFieldConstructor")
        .def_readwrite("outer_struct_field", &OuterStructWithFieldConstructor::outer_struct_field)
        .def(py::init<>())
        .def(py::init<::smoke::OuterStructWithFieldConstructor::InnerStructWithDefaults(), py::arg("outer_struct_field"))
        ;
}

