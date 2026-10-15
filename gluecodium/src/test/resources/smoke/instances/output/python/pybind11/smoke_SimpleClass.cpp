

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
#include "smoke/SimpleClass.h"
#include "memory"
#include "string"

using SimpleClass = ::smoke::SimpleClass;



void register_smoke_SimpleClass(py::module_& module) {
auto cls_SimpleClass = py::class_<SimpleClass, std::shared_ptr<SimpleClass>>(module, "smoke_SimpleClass")
        .def("__gluecodium_id__", [](const SimpleClass& self) {
            return gluecodium::python::native_identity(self);
        })
        .def("get_string_value", &SimpleClass::get_string_value, py::call_guard<py::gil_scoped_release>())
        .def("use_simple_class", &SimpleClass::use_simple_class, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        ;


}
