

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
#include "smoke/ExposeStruct.h"
#include "string"

using ExposeStruct = ::smoke::ExposeStruct;



void register_smoke_ExposeStruct(py::module_& module) {
auto cls_ExposeStruct = py::class_<ExposeStruct>(module, "smoke_ExposeStruct")
        .def_readwrite("field", &ExposeStruct::field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("field"))
        ;


}
