

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/ScalarKeyframe.h"
#include "smoke/ScalarKeyframeTrack.h"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ScalarKeyframeTrack = ::smoke::ScalarKeyframeTrack;

void register_ScalarKeyframeTrack(py::module_& module) {
    py::class_<ScalarKeyframeTrack>(module, "ScalarKeyframeTrack")
        .def_readwrite("keyframes", &ScalarKeyframeTrack::keyframes)
        .def_readwrite("easing_function", &ScalarKeyframeTrack::easing_function)
        .def_readwrite("interpolation_mode", &ScalarKeyframeTrack::interpolation_mode)
        .def(py::init<::std::vector< ::smoke::ScalarKeyframe >, ::std::string, ::std::string>(), py::arg("keyframes"), py::arg("easing_function"), py::arg("interpolation_mode"))
        ;
}

