

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
#include "smoke/SwiftMethodOverloads.h"
#include "string"
#include "vector"

using SwiftMethodOverloads = ::smoke::SwiftMethodOverloads;



void register_smoke_SwiftMethodOverloads(py::module_& module) {
auto cls_SwiftMethodOverloads = py::class_<SwiftMethodOverloads, std::shared_ptr<SwiftMethodOverloads>>(module, "smoke_SwiftMethodOverloads")
        .def("__gluecodium_id__", [](const SwiftMethodOverloads& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("one", &SwiftMethodOverloads::one, py::arg("input"))
                .def("two", [](SwiftMethodOverloads& self, const ::std::vector< ::std::string >& input) {
                        self.two(input);
                }, py::arg("input"))
        ;


}
