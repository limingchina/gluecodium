

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
#include "smoke/OuterName.h"
#include "string"

using OuterName = ::smoke::OuterName;
using InnerName = ::smoke::OuterName::InnerName;



void register_smoke_OuterName(py::module_& module) {
auto cls_OuterName = py::class_<OuterName, std::shared_ptr<OuterName>>(module, "smoke_OuterName")
        .def("__gluecodium_id__", [](const OuterName& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;

auto cls_OuterNameInnerName = py::class_<InnerName>(cls_OuterName, "InnerName")
        .def_readwrite("string_field", &InnerName::string_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("string_field"))
        ;


}
