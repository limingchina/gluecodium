

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
#include "smoke/fooTypes.h"
#include "string"

using fooTypes = ::smoke::fooTypes;
using fooStruct = ::smoke::fooTypes::fooStruct;
using fooEnum = ::smoke::fooTypes::fooEnum;



void register_smoke_QuxTypes(py::module_& module) {
auto cls_QuxTypes = py::class_<fooTypes>(module, "smoke_QuxTypes")
        .def(py::init<>())
        ;

auto cls_QuxStruct = py::class_<fooStruct>(cls_QuxTypes, "QuxStruct")
        .def_readwrite("qux_field", &fooStruct::FOO_FIELD)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("qux_field"))
        .def_static("qux_make", &fooStruct::FooCreate, py::arg("qux_parameter"))
        ;

auto cls_QuxEnum = py::enum_<fooEnum>(cls_QuxTypes, "QuxEnum")
        .value("QUX_ITEM", fooEnum::foo_item)
        ;


}
