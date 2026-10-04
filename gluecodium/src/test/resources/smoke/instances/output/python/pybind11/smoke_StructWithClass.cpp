

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
#include "smoke/SimpleClass.h"
#include "smoke/StructWithClass.h"
#include "memory"

using StructWithClass = ::smoke::StructWithClass;



void register_smoke_StructWithClass(py::module_& module) {
auto cls_StructWithClass = py::class_<StructWithClass>(module, "smoke_StructWithClass")
        .def_property("class_instance", [](const StructWithClass& self) -> decltype(auto) {
            return
                (self.class_instance)
            ;
        }, [](StructWithClass& self, const ::std::shared_ptr< ::smoke::SimpleClass >& value) {

                self.class_instance = value;

        })
        .def(py::init<>())
        .def(py::init<::std::shared_ptr< ::smoke::SimpleClass >>(), py::arg("class_instance"))
        ;


}
