

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
#include "smoke/AttributesWithComments.h"
#include "string"

using AttributesWithComments = ::smoke::AttributesWithComments;
using SomeStruct = ::smoke::AttributesWithComments::SomeStruct;



void register_smoke_AttributesWithComments(py::module_& module) {
auto cls_AttributesWithComments = py::class_<AttributesWithComments, std::shared_ptr<AttributesWithComments>>(module, "smoke_AttributesWithComments")
        .def("__gluecodium_id__", [](const AttributesWithComments& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("very_fun", &AttributesWithComments::very_fun)
        .def_property("prop", py::overload_cast<>(&AttributesWithComments::get_prop, py::const_), py::overload_cast<const ::std::string&>(&AttributesWithComments::set_prop))
        ;

auto cls_AttributesWithCommentsSomeStruct = py::class_<SomeStruct>(cls_AttributesWithComments, "SomeStruct")
        .def_readwrite("field", &SomeStruct::field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("field"))
        ;


}
