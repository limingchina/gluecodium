

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
#include "smoke/DeclarationOrderWithFunctions.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ReturnStruct = ::smoke::DeclarationOrderWithFunctions::ReturnStruct;

void register_smoke_DeclarationOrderWithFunctionsReturnStruct(py::module_& module) {
    py::class_<ReturnStruct>(module, "smoke_DeclarationOrderWithFunctionsReturnStruct")
        .def_readwrite("some_field", &ReturnStruct::some_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        ;
}

