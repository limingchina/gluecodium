

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
#include "smoke/AttributesWithDeprecated.h"
#include "string"

using AttributesWithDeprecated = ::smoke::AttributesWithDeprecated;
using SomeStruct = ::smoke::AttributesWithDeprecated::SomeStruct;



void register_smoke_AttributesWithDeprecated(py::module_& module) {
auto cls_AttributesWithDeprecated = py::class_<AttributesWithDeprecated, std::shared_ptr<AttributesWithDeprecated>>(module, "smoke_AttributesWithDeprecated")
        .def("__gluecodium_id__", [](const AttributesWithDeprecated& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("very_fun", &AttributesWithDeprecated::very_fun)
        .def_property("prop", py::overload_cast<>(&AttributesWithDeprecated::get_prop, py::const_), py::overload_cast<const ::std::string&>(&AttributesWithDeprecated::set_prop))
        ;

auto cls_AttributesWithDeprecatedSomeStruct = py::class_<SomeStruct>(cls_AttributesWithDeprecated, "SomeStruct")
        .def_readwrite("field", &SomeStruct::field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("field"))
        ;


}
