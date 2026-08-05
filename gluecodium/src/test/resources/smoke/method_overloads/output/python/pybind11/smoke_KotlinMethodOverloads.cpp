

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
#include "gluecodium/VectorHash.h"
#include "smoke/KotlinMethodOverloads.h"
#include "string"
#include "vector"

using KotlinMethodOverloads = ::smoke::KotlinMethodOverloads;



void register_smoke_KotlinMethodOverloads(py::module_& module) {
auto cls_KotlinMethodOverloads = py::class_<KotlinMethodOverloads, std::shared_ptr<KotlinMethodOverloads>>(module, "smoke_KotlinMethodOverloads")
        .def("__gluecodium_id__", [](const KotlinMethodOverloads& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("one", &KotlinMethodOverloads::one, py::arg("input"))
                .def("two", [](KotlinMethodOverloads& self, const ::std::vector< ::std::string >& input) {
                        self.two(input);
                }, py::arg("input"))
        ;


}
