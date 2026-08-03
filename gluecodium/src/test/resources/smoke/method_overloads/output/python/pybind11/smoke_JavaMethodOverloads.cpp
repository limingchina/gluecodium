

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
#include "gluecodium/VectorHash.h"
#include "smoke/JavaMethodOverloads.h"
#include "string"
#include "vector"

using JavaMethodOverloads = ::smoke::JavaMethodOverloads;



void register_smoke_JavaMethodOverloads(py::module_& module) {
auto cls_JavaMethodOverloads = py::class_<JavaMethodOverloads, std::shared_ptr<JavaMethodOverloads>>(module, "smoke_JavaMethodOverloads")
        .def("__gluecodium_id__", [](const JavaMethodOverloads& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("one", &JavaMethodOverloads::one, py::arg("input"))
                .def("two", [](JavaMethodOverloads& self, const ::std::vector< ::std::string >& input) {
                        self.two(input);
                }, py::arg("input"))
        ;


}
