

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
#include "gluecodium/DurationHash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/DurationMilliseconds.h"
#include "chrono"
#include "optional"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

using DurationMilliseconds = ::smoke::DurationMilliseconds;
using DurationStruct = ::smoke::DurationMilliseconds::DurationStruct;



void register_smoke_DurationMilliseconds(py::module_& module) {
auto cls_DurationMilliseconds = py::class_<DurationMilliseconds, std::shared_ptr<DurationMilliseconds>>(module, "smoke_DurationMilliseconds")
        .def("__gluecodium_id__", [](const DurationMilliseconds& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("duration_function", &DurationMilliseconds::duration_function, py::arg("input"))
        .def("nullable_duration_function", &DurationMilliseconds::nullable_duration_function, py::arg("input"))
        .def_property("duration_property", py::overload_cast<>(&DurationMilliseconds::get_duration_property, py::const_), py::overload_cast<const std::chrono::milliseconds>(&DurationMilliseconds::set_duration_property))
        ;

auto cls_DurationMillisecondsDurationStruct = py::class_<DurationStruct>(cls_DurationMilliseconds, "DurationStruct")
        .def_readwrite("duration_field", &DurationStruct::duration_field)
        .def(py::init<>())
        .def(py::init<std::chrono::milliseconds>(), py::arg("duration_field"))
        ;


}
