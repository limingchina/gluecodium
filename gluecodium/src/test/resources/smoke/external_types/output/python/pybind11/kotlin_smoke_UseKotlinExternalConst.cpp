

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "kotlin_smoke/UseKotlinExternalConst.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using UseKotlinExternalConst = ::kotlin_smoke::UseKotlinExternalConst;

void register_kotlin_smoke_UseKotlinExternalConst(py::module_& module) {
    py::class_<UseKotlinExternalConst>(module, "UseKotlinExternalConst")
        .def_readwrite("string_field", &UseKotlinExternalConst::string_field)
        .def(py::init<>())
        .def(py::init<::std::string(), py::arg("string_field"))
        ;
}

