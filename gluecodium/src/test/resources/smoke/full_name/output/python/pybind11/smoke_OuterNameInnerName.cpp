

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/OuterName.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InnerName = ::smoke::OuterName::InnerName;

void register_smoke_OuterNameInnerName(py::module_& module) {
    py::class_<InnerName>(module, "smoke_OuterNameInnerName")
        .def_readwrite("string_field", &InnerName::string_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("string_field"))
        ;
}

