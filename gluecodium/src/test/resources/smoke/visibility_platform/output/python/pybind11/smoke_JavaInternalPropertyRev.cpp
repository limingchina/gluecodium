

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
#include "smoke/JavaInternalPropertyRev.h"
#include "string"

using JavaInternalPropertyRev = ::smoke::JavaInternalPropertyRev;



void register_smoke_JavaInternalPropertyRev(py::module_& module) {
auto cls_JavaInternalPropertyRev = py::class_<JavaInternalPropertyRev, std::shared_ptr<JavaInternalPropertyRev>>(module, "smoke_JavaInternalPropertyRev")
        .def("__gluecodium_id__", [](const JavaInternalPropertyRev& self) {
            return gluecodium::python::native_identity(self);
        })
        .def_property("app_context", [](const JavaInternalPropertyRev& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_app_context();
            });
        }, [](JavaInternalPropertyRev& self, const ::gluecodium::optional< ::std::string >& value) {
            gluecodium::python::call_native([&] {
                self.set_app_context(value);
            });
        })
        ;


}
