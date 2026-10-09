

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
#include "smoke/fooInterface.h"
#include "smoke/fooTypes.h"
#include "cstdint"
#include "memory"
#include "string"

using fooInterface = ::smoke::fooInterface;



void register_smoke_QuxInterface(py::module_& module) {
auto cls_QuxInterface = py::class_<fooInterface, std::shared_ptr<fooInterface>>(module, "smoke_QuxInterface")
        .def("__gluecodium_id__", [](const fooInterface& self) {
            return gluecodium::python::native_identity(self);
        })
        .def("qux_method", &fooInterface::FooMethod, py::arg("qux_parameter"), py::call_guard<py::gil_scoped_release>())
        .def_static("qux_create", &fooInterface::make, py::arg("make_parameter"), py::call_guard<py::gil_scoped_release>())
        .def_property("qux_property", [](const fooInterface& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.GET_FOO_PROPERTY();
            });
        }, [](fooInterface& self, const uint32_t value) {
            gluecodium::python::call_native([&] {
                self.SET_FOO_PROPERTY(value);
            });
        })
        ;


}
