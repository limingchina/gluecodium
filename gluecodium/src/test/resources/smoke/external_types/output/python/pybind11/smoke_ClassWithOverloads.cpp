

#include <Python.h>
#include <pybind11/pybind11.h>
#include "_opaque_types.h"
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
#include "include/ExternalTypes.h"
#include "string"
#include "vector"

using ClassWithOverloads = ::smoke::ClassWithOverloads;



void register_smoke_ClassWithOverloads(py::module_& module) {
auto cls_ClassWithOverloads = py::class_<ClassWithOverloads, std::shared_ptr<ClassWithOverloads>>(module, "smoke_ClassWithOverloads")
        .def("__gluecodium_id__", [](const ClassWithOverloads& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("one_overload_not_exposed", [](ClassWithOverloads& self) {
            return self.oneOverloadNotExposed();
        })
        .def("all_overloads_exposed", [](ClassWithOverloads& self, const ::std::string& input) {
            return self.allOverloadsExposed(input);
        }, py::arg("input"))
                .def("all_overloads_exposed", [](ClassWithOverloads& self, const ::std::vector< ::std::string >& input_list) {
                        return self.allOverloadsExposed(input_list);
                }, py::arg("input_list"))
        .def("all_overloads_exposed", [](ClassWithOverloads& self, const ::std::string& input_string, const bool input_bool) {
            return self.allOverloadsExposed(input_string, input_bool);
        }, py::arg("input_string"), py::arg("input_bool"))
        ;


}
