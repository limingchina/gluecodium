

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
#include "gluecodium/DurationHash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/DurationSeconds.h"
#include "chrono"
#include "optional"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

using DurationSeconds = ::smoke::DurationSeconds;
using DurationStruct = ::smoke::DurationSeconds::DurationStruct;



void register_smoke_DurationSeconds(py::module_& module) {
auto cls_DurationSeconds = py::class_<DurationSeconds, std::shared_ptr<DurationSeconds>>(module, "smoke_DurationSeconds")
        .def("__gluecodium_id__", [](const DurationSeconds& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("duration_function", &DurationSeconds::duration_function, py::arg("input"))
        .def("nullable_duration_function", &DurationSeconds::nullable_duration_function, py::arg("input"))
        .def_property("duration_property", py::overload_cast<>(&DurationSeconds::get_duration_property, py::const_), py::overload_cast<const ::std::chrono::seconds>(&DurationSeconds::set_duration_property))
        ;

auto cls_DurationSecondsDurationStruct = py::class_<DurationStruct>(cls_DurationSeconds, "DurationStruct")
        .def_readwrite("duration_field", &DurationStruct::duration_field)
        .def(py::init<>())
        .def(py::init<::std::chrono::seconds>(), py::arg("duration_field"))
        ;


}
