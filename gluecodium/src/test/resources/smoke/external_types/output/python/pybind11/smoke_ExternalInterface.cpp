

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
#include "foo/Bar.h"
#include "cstdint"
#include "string"

using ExternalInterface = ::smoke::ExternalInterface;
using some_Struct = ::smoke::ExternalInterface::some_Struct;
using some_Enum = ::smoke::ExternalInterface::some_Enum;



void register_smoke_ExternalInterface(py::module_& module) {
auto cls_ExternalInterface = py::class_<ExternalInterface, std::shared_ptr<ExternalInterface>>(module, "smoke_ExternalInterface")
        .def("__gluecodium_id__", [](const ExternalInterface& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;

auto cls_ExternalInterfacesome_Struct = py::class_<some_Struct>(cls_ExternalInterface, "SomeStruct")
        .def_readwrite("some_field", &some_Struct::some_Field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        ;

auto cls_ExternalInterfacesome_Enum = py::enum_<some_Enum>(cls_ExternalInterface, "SomeEnum")
        .value("SOME_VALUE", some_Enum::some_Value)
        ;


}
