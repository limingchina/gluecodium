

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/StructWithConstMethod.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructWithConstMethod = ::gluecodium::smoke::StructWithConstMethod;

void register_StructWithConstMethod(py::module_& module) {
    py::class_<StructWithConstMethod>(module, "StructWithConstMethod")
        .def_readwrite("string_field", &StructWithConstMethod::string_field)
        .def("double_const", &StructWithConstMethod::double_const)
        ;
}

