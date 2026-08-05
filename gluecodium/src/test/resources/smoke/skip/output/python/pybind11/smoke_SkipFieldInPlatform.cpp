

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
#include "smoke/SkipFieldInPlatform.h"
#include "cstdint"
#include "string"

using SkipFieldInPlatform = ::smoke::SkipFieldInPlatform;



void register_smoke_SkipFieldInPlatform(py::module_& module) {
auto cls_SkipFieldInPlatform = py::class_<SkipFieldInPlatform>(module, "smoke_SkipFieldInPlatform")
        .def_readwrite("int_field", &SkipFieldInPlatform::int_field)
        .def_readwrite("bool_field", &SkipFieldInPlatform::bool_field)
        .def(py::init<>())
        .def(py::init<int32_t, ::std::string, bool>(), py::arg("int_field"), py::arg("string_field"), py::arg("bool_field"))
        ;


}
