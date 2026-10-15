

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
#include "smoke/ScalarKeyframe.h"
#include "smoke/ScalarKeyframeTrack.h"
#include "string"
#include "vector"

using ScalarKeyframeTrack = ::smoke::ScalarKeyframeTrack;



void register_smoke_ScalarKeyframeTrack(py::module_& module) {
auto cls_ScalarKeyframeTrack = py::class_<ScalarKeyframeTrack>(module, "smoke_ScalarKeyframeTrack")
        .def_property_readonly("keyframes", [](const ScalarKeyframeTrack& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.keyframes)
            );
        })
        .def_property("easing_function", [](const ScalarKeyframeTrack& self) -> decltype(auto) {
            return
                (self.easing_function)
            ;
        }, [](ScalarKeyframeTrack& self, const ::std::string& value) {

                self.easing_function = value;

        })
        .def_property("interpolation_mode", [](const ScalarKeyframeTrack& self) -> decltype(auto) {
            return
                (self.interpolation_mode)
            ;
        }, [](ScalarKeyframeTrack& self, const ::std::string& value) {

                self.interpolation_mode = value;

        })
        .def(py::init<>())
        .def(py::init<::std::vector< ::smoke::ScalarKeyframe >, ::std::string, ::std::string>(), py::arg("keyframes"), py::arg("easing_function"), py::arg("interpolation_mode"))
        ;


}
