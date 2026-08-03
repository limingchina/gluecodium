

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
#include "smoke/JavaDeprecatedPosDefaultsCustom.h"
#include "cstdint"
#include "string"

using JavaDeprecatedPosDefaultsCustom = ::smoke::JavaDeprecatedPosDefaultsCustom;



void register_smoke_JavaDeprecatedPosDefaultsCustom(py::module_& module) {
auto cls_JavaDeprecatedPosDefaultsCustom = py::class_<JavaDeprecatedPosDefaultsCustom>(module, "smoke_JavaDeprecatedPosDefaultsCustom")
        .def_readwrite("first_init_field", &JavaDeprecatedPosDefaultsCustom::first_init_field)
        .def_readwrite("first_free_field", &JavaDeprecatedPosDefaultsCustom::first_free_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("first_free_field"))
        .def(py::init<int32_t, ::std::string>(), py::arg("first_init_field"), py::arg("first_free_field"))
        .def_static("custom", &JavaDeprecatedPosDefaultsCustom::custom)
        ;


}
