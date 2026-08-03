

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
#include "smoke/IncludableStruct.h"
#include "string"

using IncludableStruct = ::smoke::IncludableStruct;



void register_smoke_IncludableStruct(py::module_& module) {
auto cls_IncludableStruct = py::class_<IncludableStruct>(module, "smoke_IncludableStruct")
        .def_readwrite("field", &IncludableStruct::field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("field"))
        ;


}
