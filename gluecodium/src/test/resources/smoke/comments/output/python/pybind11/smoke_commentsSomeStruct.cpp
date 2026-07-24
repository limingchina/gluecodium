

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/Comments.h"
#include "optional"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SomeStruct = ::smoke::Comments::SomeStruct;

void register_smoke_commentsSomeStruct(py::module_& module) {
    py::class_<SomeStruct>(module, "commentsSomeStruct")
        .def_readwrite("some_field", &SomeStruct::some_field)
        .def_readwrite("nullable_field", &SomeStruct::nullable_field)
        .def(py::init<>())
        .def(py::init<bool>(py::arg("some_field")))
        .def(py::init<bool, std::optional< ::std::string >(), py::arg("some_field"), py::arg("nullable_field"))
        ;
}

