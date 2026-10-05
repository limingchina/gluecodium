

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
#include "gluecodium/Optional.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/DurationMilliseconds.h"
#include "chrono"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

using DurationMilliseconds = ::smoke::DurationMilliseconds;
using DurationStruct = ::smoke::DurationMilliseconds::DurationStruct;



void register_smoke_DurationMilliseconds(py::module_& module) {
auto cls_DurationMilliseconds = py::class_<DurationMilliseconds, std::shared_ptr<DurationMilliseconds>>(module, "smoke_DurationMilliseconds")
        .def("__gluecodium_id__", [](const DurationMilliseconds& self) {
            return gluecodium::python::native_identity(self);
        })
        .def("duration_function", &DurationMilliseconds::duration_function, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def("nullable_duration_function", &DurationMilliseconds::nullable_duration_function, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def_property("duration_property", [](const DurationMilliseconds& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_duration_property();
            });
        }, [](DurationMilliseconds& self, const std::chrono::milliseconds value) {
            gluecodium::python::call_native([&] {
                self.set_duration_property(value);
            });
        })
        ;

auto cls_DurationMillisecondsDurationStruct = py::class_<DurationStruct>(cls_DurationMilliseconds, "DurationStruct")
        .def_property("duration_field", [](const DurationStruct& self) -> decltype(auto) {
            return
                (self.duration_field)
            ;
        }, [](DurationStruct& self, const std::chrono::milliseconds value) {

                self.duration_field = value;

        })
        .def(py::init<>())
        .def(py::init<std::chrono::milliseconds>(), py::arg("duration_field"))
        ;


}
