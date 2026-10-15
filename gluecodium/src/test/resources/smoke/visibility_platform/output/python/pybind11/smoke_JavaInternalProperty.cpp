

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
#include "gluecodium/Optional.h"
#include "smoke/JavaInternalProperty.h"
#include "string"

using JavaInternalProperty = ::smoke::JavaInternalProperty;



void register_smoke_JavaInternalProperty(py::module_& module) {
auto cls_JavaInternalProperty = py::class_<JavaInternalProperty, std::shared_ptr<JavaInternalProperty>>(module, "smoke_JavaInternalProperty")
        .def("__gluecodium_id__", [](const JavaInternalProperty& self) {
            return gluecodium::python::native_identity(self);
        })
        .def_property("app_context", [](const JavaInternalProperty& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_app_context();
            });
        }, [](JavaInternalProperty& self, const ::gluecodium::optional< ::std::string >& value) {
            gluecodium::python::call_native([&] {
                self.set_app_context(value);
            });
        })
        ;


}
