

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/DeclarationOrderWithFunctions.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using MainStructWithFunctions = ::smoke::DeclarationOrderWithFunctions::MainStructWithFunctions;

void register_DeclarationOrderWithFunctionsMainStructWithFunctions(py::module_& module) {
    py::class_<MainStructWithFunctions>(module, "DeclarationOrderWithFunctionsMainStructWithFunctions")
        .def_readwrite("struct_field", &MainStructWithFunctions::struct_field)
        .def(py::init<>())
        .def(py::init<::smoke::DeclarationOrderWithFunctions::FieldStruct>(), py::arg("struct_field"))
        .def("with_parameter", &MainStructWithFunctions::with_parameter, py::arg("input"))

        .def("with_return", &MainStructWithFunctions::with_return)

        .def("with_thrown", &MainStructWithFunctions::with_thrown)

        ;
}

