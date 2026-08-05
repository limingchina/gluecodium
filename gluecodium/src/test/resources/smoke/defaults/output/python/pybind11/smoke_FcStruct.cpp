

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FcStruct.h"
#include "string"

using FcStruct = ::smoke::FcStruct;



void register_smoke_FcStruct(py::module_& module) {
auto cls_FcStruct = py::class_<FcStruct>(module, "smoke_FcStruct")
        .def_readwrite("string_field", &FcStruct::string_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("string_field"))
        ;


}
