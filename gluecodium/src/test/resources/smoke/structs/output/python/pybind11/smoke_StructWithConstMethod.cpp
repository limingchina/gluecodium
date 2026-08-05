

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
#include "smoke/StructWithConstMethod.h"
#include "string"

using StructWithConstMethod = ::smoke::StructWithConstMethod;



void register_smoke_StructWithConstMethod(py::module_& module) {
auto cls_StructWithConstMethod = py::class_<StructWithConstMethod>(module, "smoke_StructWithConstMethod")
        .def_readwrite("string_field", &StructWithConstMethod::string_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("string_field"))
        .def("double_const", &StructWithConstMethod::double_const)
        ;


}
