

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
#include "foo/Bar.h"
#include "cstdint"
#include "string"

using some_Struct = ::fire::Baz::some_Struct;
using some_Enum = ::fire::Baz::some_Enum;



void register_smoke_ExternalClass(py::module_& module) {
auto cls_ExternalClass = py::class_<::fire::Baz>(module, "smoke_ExternalClass");

auto cls_ExternalClasssome_Struct = py::class_<some_Struct>(cls_ExternalClass, "SomeStruct")
        .def_readwrite("some_field", &some_Struct::some_Field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        ;

auto cls_ExternalClasssome_Enum = py::enum_<some_Enum>(cls_ExternalClass, "SomeEnum")
        .value("SOME_VALUE", some_Enum::some_Value)
        ;


}
