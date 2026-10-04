

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
#include "gluecodium/TimePointHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/MixedCollectionsStruct.h"
#include "chrono"
#include "vector"

using MixedCollectionsStruct = ::smoke::MixedCollectionsStruct;



void register_smoke_MixedCollectionsStruct(py::module_& module) {
auto cls_MixedCollectionsStruct = py::class_<MixedCollectionsStruct>(module, "smoke_MixedCollectionsStruct")
        .def_property("almost_dates", [](const MixedCollectionsStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.almost_dates)
            );
        }, [](MixedCollectionsStruct& self, const ::std::vector< ::gluecodium::optional< ::std::chrono::system_clock::time_point > >& value) {

                self.almost_dates = value;

        })
        .def_property("dates", [](const MixedCollectionsStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.dates)
            );
        }, [](MixedCollectionsStruct& self, const ::std::vector< ::std::chrono::system_clock::time_point >& value) {

                self.dates = value;

        })
        .def(py::init<>())
        .def(py::init<::std::vector< ::gluecodium::optional< ::std::chrono::system_clock::time_point > >, ::std::vector< ::std::chrono::system_clock::time_point >>(), py::arg("almost_dates"), py::arg("dates"))
        ;


}
