

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/DurationHash.h"
#include "smoke/DurationInterface.h"
#include "chrono"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DurationInterface = ::gluecodium::smoke::DurationInterface;

class DurationInterfaceTrampoline : public DurationInterface {
public:
    using DurationInterface::DurationInterface;

    ::std::string duration_function(
            ::std::chrono::seconds input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string, DurationInterface, duration_function, input);
    }
};

void register_DurationInterface(py::module_& module) {
    py::class_<DurationInterface, std::shared_ptr<DurationInterface>, DurationInterfaceTrampoline>(module, "DurationInterface")
        .def("duration_function", &DurationInterface::duration_function, py::arg("input"))
        ;
}

